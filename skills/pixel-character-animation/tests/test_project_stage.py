import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'project_stage.py'
MODULE = importlib.util.spec_from_file_location('project_stage', SCRIPT)
p = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(p)


class ProjectStageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'candidate.png').write_bytes(b'fixture: file existence, not image validation')
        (self.root / 'review.txt').write_text('Reviewed frame edges and played the candidate at 1x.')
        self.spec = p.new_spec()

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = p.main(['--root', str(self.root), *args])
        return status, json.loads(out.getvalue())

    def complete(self, stage):
        record = self.spec['stages'][stage]
        record['status'] = 'passed'
        record['artifacts'] = [{'path': 'candidate.png', 'role': 'imported candidate',
                                'sha256': hashlib.sha256((self.root / 'candidate.png').read_bytes()).hexdigest(),
                                'provenance': {'kind': 'imported', 'source': 'user supplied pack',
                                               'justification': 'Preserve existing motion; only repair its edges.'}}]
        for kind, gate in record['gates'].items():
            gate['status'] = 'passed'
            evidence = {'path': 'review.txt', 'observation': 'Checked the supplied candidate for this scoped task.'}
            if kind == 'visual':
                evidence.update(reviewer_type='agent', reviewer='reviewer A', method='actual frames and 1x playback')
            gate['evidence'] = [evidence]

    def test_defaults_and_override(self):
        self.assertEqual(self.spec['canvas'], {'width': 256, 'height': 256})
        self.assertEqual(p.new_spec(canvas=(128, 96))['canvas'], {'width': 128, 'height': 96})
        for canvas in ((0, 32), (-1, 32), (True, 32), ('32', 32)):
            with self.assertRaises(ValueError):
                p.new_spec(canvas=canvas)
        code, result = self.run_cli('init', '--canvas', '512x128')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads((self.root / result['created']).read_text())['canvas']['height'], 128)

    def test_every_input_and_entry_stage(self):
        for input_type in p.INPUT_TYPES:
            for stage in p.STAGES:
                spec = p.new_spec(input_type=input_type, entry_stage=stage)
                self.assertEqual(spec['entry_stage'], stage)
                self.assertTrue(p.check(self.root, spec)['technical_validation'])
                self.assertTrue(all(record['status'] == 'pending' for record in spec['stages'].values()))

    def test_entry_does_not_fabricate_predecessors(self):
        self.spec['entry_stage'] = 'cleanup'
        result = p.route(self.root, self.spec, 'cleanup')
        self.assertEqual(result['next_stage'], 'intake')
        self.assertIn('animation', result['missing_prerequisites'])
        self.assertEqual(result['reuse'], [])

    def test_edge_repair_reuses_imported_animation(self):
        self.complete('animation')
        result = p.route(self.root, self.spec, 'cleanup')
        self.assertEqual(result['next_stage'], 'cleanup')
        self.assertEqual(result['missing_prerequisites'], [])
        self.assertEqual(result['reuse'], ['animation'])
        self.assertNotIn('views', result['remaining_stages'])

    def test_complete_target_is_reused(self):
        self.complete('delivery')
        result = p.route(self.root, self.spec, 'delivery')
        self.assertTrue(result['ready'])
        self.assertIsNone(result['next_stage'])

    def test_missing_or_unjustified_import_cannot_pass(self):
        self.complete('animation')
        del self.spec['stages']['animation']['artifacts'][0]['provenance']['justification']
        self.assertNotIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])
        self.spec['stages']['animation']['artifacts'][0]['path'] = 'absent.png'
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])

    def test_metadata_does_not_approve_visuals(self):
        self.complete('animation')
        gate = self.spec['stages']['animation']['gates']['visual']
        gate['evidence'] = []
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        self.assertNotIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])
        gate['status'] = 'pending'
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])

    def test_visual_review_identity_and_blockers_are_required(self):
        self.complete('animation')
        gate = self.spec['stages']['animation']['gates']['visual']
        del gate['evidence'][0]['reviewer_type']
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        gate['evidence'][0]['reviewer_type'] = 'agent'
        gate['status'] = 'blocked'
        gate['reason'] = 'No actual-speed playback tool available.'
        self.assertNotIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])

    def test_existing_design_skips_intake_but_not_views_or_research(self):
        self.complete('design')
        result = p.route(self.root, self.spec, 'blocking')
        self.assertEqual(result['reuse'], ['design'])
        self.assertEqual(result['missing_prerequisites'], ['views', 'research'])
        self.assertEqual(result['next_stage'], 'views')

    def test_na_requires_explicit_evidence(self):
        record = self.spec['stages']['views']
        record['status'] = 'not_applicable'
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        record.update(reason='Single fixed-view idle needs no additional views.',
                      evidence=[{'path': 'review.txt', 'observation': 'Action stays in the imported fixed view.'}])
        self.assertTrue(p.check(self.root, self.spec)['technical_validation'])

    def test_no_overwrite_and_read_only_commands(self):
        self.assertEqual(self.run_cli('init')[0], 0)
        path = self.root / 'project_spec.json'
        spec = json.loads(path.read_text())
        spec['custom_future_field'] = {'retained': [1, 2, 3]}
        path.write_text(json.dumps(spec))
        original = path.read_bytes()
        self.assertEqual(self.run_cli('init')[0], 2)
        self.assertEqual(self.run_cli('check')[0], 0)
        self.assertEqual(self.run_cli('route', 'delivery')[0], 0)
        self.assertEqual(path.read_bytes(), original)

    def test_legacy_snapshot_is_not_migration_or_approval(self):
        legacy = self.root / 'project_resume.json'
        legacy.write_text(json.dumps({'canvas': [64, 64], 'approved': True, 'custom': 'keep', 'master': '/old/path.png'}))
        original = legacy.read_bytes()
        code, _ = self.run_cli('init', '--input-type', 'existing_project', '--entry-stage', 'cleanup', '--legacy-profile', 'project_resume.json')
        self.assertEqual(code, 0)
        spec = json.loads((self.root / 'project_spec.json').read_text())
        self.assertEqual(spec['legacy_profile']['snapshot']['custom'], 'keep')
        self.assertEqual(spec['canvas']['width'], 64)
        self.assertEqual(spec['stages']['animation']['gates']['visual']['status'], 'pending')
        self.assertEqual(legacy.read_bytes(), original)
        code, _ = self.run_cli('--spec', 'project_resume.json', 'check')
        self.assertEqual(code, 1)
        self.assertEqual(legacy.read_bytes(), original)

    def test_legacy_canvas_recognition_override_and_malformed(self):
        for key in ('current_working_canvas', 'canvas'):
            for value in ([128, 96], {'width': 128, 'height': 96}, '128x96'):
                self.assertEqual(p.legacy_canvas({key: value}), (128, 96))
        self.assertEqual(p.legacy_canvas({'current_working_canvas': [128, 128], 'canvas': [256, 256]}), (128, 128))
        for value in (None, [0, 12], {'width': 12}, 'unknown'):
            with self.assertRaises(ValueError):
                p.legacy_canvas({'canvas': value})
        legacy = self.root / 'legacy.json'
        legacy.write_text(json.dumps({'current_working_canvas': [128, 128]}))
        self.assertEqual(self.run_cli('init', '--input-type', 'existing_project', '--legacy-profile', 'legacy.json', '--canvas', '64x96')[0], 0)
        self.assertEqual(json.loads((self.root / 'project_spec.json').read_text())['canvas'], {'width': 64, 'height': 96})
        legacy.write_text(json.dumps({'canvas': 'unknown'}))
        self.assertEqual(self.run_cli('--spec', 'new.json', 'init', '--input-type', 'existing_project', '--legacy-profile', 'legacy.json')[0], 2)
        self.assertFalse((self.root / 'new.json').exists())

    def test_changed_accepted_bytes_are_stale_and_edits_preserved(self):
        self.complete('animation')
        self.assertTrue(p.check(self.root, self.spec)['technical_validation'])
        candidate = self.root / 'candidate.png'
        candidate.write_bytes(b'externally edited artwork')
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        result = p.route(self.root, self.spec, 'cleanup')
        self.assertEqual(result['next_stage'], 'animation')
        self.assertNotIn('animation', result['reuse'])
        self.assertTrue(any('stale sha256' in error for error in result['stage_errors']['animation']))
        self.assertEqual(candidate.read_bytes(), b'externally edited artwork')

    def test_completed_artifact_without_hash_cannot_be_reused(self):
        self.complete('animation')
        del self.spec['stages']['animation']['artifacts'][0]['sha256']
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        self.assertEqual(p.route(self.root, self.spec, 'cleanup')['next_stage'], 'animation')
        self.assertNotIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])

    def test_imported_pending_reviews_do_not_rebuild_predecessors(self):
        self.complete('animation')
        record = self.spec['stages']['animation']
        record['status'] = 'pending'
        record['gates']['visual']['status'] = 'pending'
        record['gates']['native_reopen'] = {'status': 'blocked', 'evidence': []}
        result = p.route(self.root, self.spec, 'cleanup')
        self.assertEqual(result['next_stage'], 'animation')
        self.assertEqual(result['missing_prerequisites'], ['animation'])
        self.assertEqual(result['pending_gates']['animation'], ['visual', 'native_reopen'])
        record['status'] = 'passed'
        record['gates']['visual']['status'] = 'passed'
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])

    def test_declared_global_input_hash_blocks_route_when_stale(self):
        self.complete('delivery')
        master = self.root / 'master.png'
        master.write_bytes(b'original master')
        original_hash = hashlib.sha256(master.read_bytes()).hexdigest()
        for key in ('inputs', 'reference_views'):
            self.spec[key] = [{'path': 'master.png', 'sha256': original_hash}]
            self.assertTrue(p.route(self.root, self.spec, 'delivery')['ready'])
            master.write_bytes(b'changed master')
            result = p.route(self.root, self.spec, 'delivery')
            self.assertFalse(result['ready'])
            self.assertIsNone(result['next_stage'])
            self.assertTrue(any('stale/invalid declared input' in error for error in result['errors']))
            self.assertEqual(master.read_bytes(), b'changed master')
            master.write_bytes(b'original master')
            self.spec[key] = []

    def test_per_stage_input_snapshot_stale_or_missing_hash(self):
        self.complete('animation')
        stage = self.spec['stages']['animation']
        source = self.root / 'source.png'
        source.write_bytes(b'original source')
        stage['input_artifacts'] = [{'path': 'source.png', 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}]
        self.assertIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])
        source.write_bytes(b'changed source')
        self.assertNotIn('animation', p.route(self.root, self.spec, 'cleanup')['reuse'])
        self.assertTrue(any('input_artifacts: stale sha256' in error for error in p.check(self.root, self.spec)['stage_errors']['animation']))
        del stage['input_artifacts'][0]['sha256']
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])

    def test_boolean_schema_version_is_not_integer_version(self):
        self.spec['schema_version'] = True
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        self.assertFalse(p.route(self.root, self.spec, 'delivery')['ready'])

    def test_paths_and_symlinks(self):
        for value in ('../escape', '/tmp/absolute', 'a/../../escape', 'C:/escape', 'a\\b', '.', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                p.safe_path(self.root, value, must_exist=False)
        (self.root / 'link').symlink_to(self.root / 'candidate.png')
        (self.root / 'dangling').symlink_to(self.root / 'missing')
        (self.root / 'folder').symlink_to(self.root, target_is_directory=True)
        for value in ('link', 'dangling', 'folder/review.txt'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                p.safe_path(self.root, value, must_exist=False)
        self.assertEqual(self.run_cli('--spec', '../escape.json', 'init')[0], 2)
        self.assertEqual(self.run_cli('--spec', 'dangling', 'init')[0], 2)

    def test_invalid_shapes_are_reported(self):
        for value in ([], None, 'legacy'):
            self.assertFalse(p.check(self.root, value)['technical_validation'])
        self.spec['stages']['animation'] = None
        self.assertFalse(p.check(self.root, self.spec)['technical_validation'])
        self.assertEqual(p.route(self.root, self.spec, 'cleanup')['next_stage'], 'intake')


if __name__ == '__main__':
    unittest.main()
