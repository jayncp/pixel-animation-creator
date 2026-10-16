#!/usr/bin/env python3
"""Portable, evidence-based project bookkeeping; never generates or reviews art."""
import argparse
import hashlib
import json
import re
from pathlib import Path

STAGES = ('intake', 'design', 'views', 'research', 'blocking', 'animation', 'cleanup', 'delivery')
INPUT_TYPES = ('text', 'general_image', 'pixel_image', 'existing_project')
STATUSES = ('pending', 'passed', 'blocked', 'not_applicable')
DEPENDENCIES = {
    'intake': (), 'design': ('intake',), 'views': ('design',),
    'research': ('design',), 'blocking': ('views', 'research'),
    'animation': ('blocking',), 'cleanup': ('animation',), 'delivery': ('cleanup',),
}
VISUAL_STAGES = {'design', 'views', 'blocking', 'animation', 'cleanup', 'delivery'}


def safe_path(root, value, must_exist=True):
    """Reject absolute paths, parent traversal and symlinks, including dangling ones."""
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('path must be a nonempty portable relative path')
    path = Path(value)
    if path.is_absolute() or '..' in path.parts or re.match(r'^[A-Za-z]:', value):
        raise ValueError('path must stay inside the project root: ' + value)
    root = Path(root).resolve(strict=True)
    candidate = root
    for part in path.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError('symlink is not permitted: ' + value)
    if candidate == root or not candidate.resolve().is_relative_to(root):
        raise ValueError('path must name a file inside the project root: ' + value)
    if must_exist and not candidate.is_file():
        raise ValueError('missing regular file: ' + value)
    return candidate


def required_gates(stage):
    return ('technical', 'visual') if stage in VISUAL_STAGES else ('technical',)


def new_spec(input_type='text', canvas=(256, 256), entry_stage='intake'):
    if input_type not in INPUT_TYPES or entry_stage not in STAGES:
        raise ValueError('unknown input type or entry stage')
    if len(canvas) != 2 or any(type(n) is not int or n <= 0 for n in canvas):
        raise ValueError('canvas dimensions must be positive integers')
    return {
        'schema_version': 1,
        'input_type': input_type,
        'canvas': {'width': canvas[0], 'height': canvas[1]},
        'entry_stage': entry_stage,
        'scope': {'request': '', 'preserve': [], 'excluded': []},
        'inputs': [],
        'identity_spec': {},
        'reference_views': [],
        'motion_research': [],
        'timing_events': [],
        'acceptance_notes': [],
        'stages': {
            stage: {
                'status': 'pending', 'artifacts': [],
                'gates': {kind: {'status': 'pending', 'evidence': []}
                          for kind in required_gates(stage)},
            } for stage in STAGES
        },
    }


def evidence_errors(root, evidence, visual=False):
    errors = []
    if not isinstance(evidence, list) or not evidence:
        return ['actual evidence is required']
    for item in evidence:
        if not isinstance(item, dict):
            errors.append('evidence must be an object')
            continue
        try:
            path = safe_path(root, item.get('path'))
            errors += hash_errors(path, item.get('sha256'))
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
        if not isinstance(item.get('observation'), str) or not item['observation'].strip():
            errors.append('evidence needs a concrete observation')
        if visual:
            if item.get('reviewer_type') not in ('human', 'agent'):
                errors.append('visual evidence needs reviewer_type human or agent')
            for field in ('reviewer', 'method'):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append('visual evidence needs ' + field)
    return errors


def hash_errors(path, expected, required=False):
    if expected is None and not required:
        return []
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', expected):
        return ['explicit sha256 is required for completed artifacts' if required else 'invalid sha256']
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return [] if digest.hexdigest() == expected.lower() else ['stale sha256: file bytes changed: ' + str(path.name)]


def artifact_errors(root, artifacts, require_hash=False, verify_hash=True):
    errors = []
    if not isinstance(artifacts, list):
        errors.append('artifacts must be a list')
        artifacts = []
    if require_hash and not artifacts:
        errors.append('passed stage requires an actual artifact')
    for item in artifacts:
        if not isinstance(item, dict):
            errors.append('artifact must be an object')
            continue
        try:
            path = safe_path(root, item.get('path'))
            if verify_hash:
                errors += hash_errors(path, item.get('sha256'), require_hash)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
        if not isinstance(item.get('role'), str) or not item['role'].strip():
            errors.append('artifact needs a role')
        provenance = item.get('provenance')
        if not isinstance(provenance, dict) or provenance.get('kind') not in ('authored', 'imported', 'generated', 'derived', 'mirrored', 'inferred'):
            errors.append('artifact needs explicit provenance.kind')
        elif provenance['kind'] != 'authored' and not provenance.get('source'):
            errors.append('non-authored artifact needs provenance.source')
        if isinstance(provenance, dict) and provenance.get('kind') == 'imported' and not provenance.get('justification'):
            errors.append('imported prerequisite needs provenance.justification')
    return errors


def stage_errors(root, name, record):
    if not isinstance(record, dict):
        return ['stage record must be an object']
    errors = []
    status = record.get('status')
    if status not in STATUSES:
        errors.append('invalid stage status')
    if status == 'not_applicable':
        if not isinstance(record.get('reason'), str) or not record['reason'].strip():
            errors.append('not_applicable needs a scope-specific reason')
        errors += evidence_errors(root, record.get('evidence'))
        return errors
    errors += artifact_errors(root, record.get('artifacts', []), require_hash=status == 'passed')
    snapshots = record.get('input_artifacts', [])
    if not isinstance(snapshots, list):
        errors.append('input_artifacts must be a list')
        snapshots = []
    for item in snapshots:
        try:
            path = safe_path(root, item.get('path') if isinstance(item, dict) else None)
            errors.extend('input_artifacts: ' + error for error in hash_errors(path, item.get('sha256'), required=True))
        except (ValueError, OSError) as exc:
            errors.append('input_artifacts: ' + str(exc))
    gates = record.get('gates', {})
    if not isinstance(gates, dict):
        errors.append('gates must be an object')
        gates = {}
    for kind in dict.fromkeys((*required_gates(name), *gates)):
        gate = gates.get(kind)
        if not isinstance(gate, dict):
            errors.append(kind + ' gate is missing')
            continue
        gate_status = gate.get('status')
        if gate_status not in STATUSES:
            errors.append(kind + ': invalid gate status')
        if status == 'passed' and gate_status not in ('passed', 'not_applicable'):
            errors.append(kind + ': gate is not complete')
        if gate_status in ('passed', 'not_applicable'):
            if gate_status == 'not_applicable' and not gate.get('reason'):
                errors.append(kind + ': not_applicable needs a reason')
            errors.extend(kind + ': ' + err for err in evidence_errors(
                root, gate.get('evidence'), visual=kind == 'visual' and gate_status == 'passed'))
    return errors


def check(root, spec):
    """Validate recorded evidence structurally, NOT its truth or artistic quality."""
    errors = []
    if not isinstance(spec, dict):
        return {'technical_validation': False, 'errors': ['project spec must be an object'], 'stage_errors': {}}
    if type(spec.get('schema_version')) is not int or spec['schema_version'] != 1:
        errors.append('unsupported/missing schema_version; legacy profiles are read-only inputs, not v1 specs')
    if spec.get('input_type') not in INPUT_TYPES:
        errors.append('invalid input_type')
    if spec.get('entry_stage') not in STAGES:
        errors.append('invalid entry_stage')
    canvas = spec.get('canvas', {})
    if not isinstance(canvas, dict) or any(type(canvas.get(k)) is not int or canvas[k] <= 0 for k in ('width', 'height')):
        errors.append('canvas width and height must be positive integers')
    stages = spec.get('stages', {})
    if not isinstance(stages, dict):
        errors.append('stages must be an object')
        stages = {}
    details = {stage: stage_errors(root, stage, stages.get(stage)) for stage in STAGES}
    for key in ('inputs', 'reference_views'):
        values = spec.get(key, [])
        if not isinstance(values, list):
            errors.append(key + ' must be a list')
            continue
        for item in values:
            try:
                path = safe_path(root, item.get('path') if isinstance(item, dict) else None)
                errors.extend(key + ': stale/invalid declared input: ' + error
                              for error in hash_errors(path, item.get('sha256')))
            except (ValueError, OSError) as exc:
                errors.append(key + ': ' + str(exc))
    return {'technical_validation': not errors and not any(details.values()),
            'errors': errors, 'stage_errors': details,
            'notice': 'Structural/file checks only. No visual approval is created or verified by this tool.'}


def route(root, spec, target):
    if target not in STAGES:
        raise ValueError('unknown target stage')
    report = check(root, spec)
    if report['errors']:
        return {'target': target, 'next_stage': None, 'errors': report['errors'], 'ready': False}
    stages = spec['stages']
    missing, reused, visited = [], [], set()

    def visit(stage):
        if stage in visited:
            return
        visited.add(stage)
        record = stages.get(stage, {})
        if isinstance(record, dict) and record.get('status') in ('passed', 'not_applicable') and not report['stage_errors'][stage]:
            reused.append(stage)
            return  # A validated imported result is a boundary, not a demand to remake history.
        artifacts = record.get('artifacts', []) if isinstance(record, dict) else []
        imported_boundary = (bool(artifacts) and isinstance(artifacts, list)
                             and not artifact_errors(root, artifacts, verify_hash=False)
                             and all(item['provenance']['kind'] == 'imported' for item in artifacts))
        if not imported_boundary:
            for dependency in DEPENDENCIES[stage]:
                visit(dependency)
        missing.append(stage)
    visit(target)
    return {'target': target, 'next_stage': missing[0] if missing else None,
            'missing_prerequisites': [stage for stage in missing if stage != target],
            'remaining_stages': missing, 'reuse': reused, 'ready': not missing,
            'stage_errors': {stage: report['stage_errors'][stage] for stage in missing},
            'pending_gates': {
                stage: [kind for kind, gate in stages.get(stage, {}).get('gates', {}).items()
                        if isinstance(gate, dict) and gate.get('status') not in ('passed', 'not_applicable')]
                for stage in missing if isinstance(stages.get(stage), dict)
                and isinstance(stages[stage].get('gates'), dict)},
            'notice': 'Recorded visual reviews are supplied by humans/agents, not inferred from metadata.'}


def legacy_canvas(snapshot):
    """Recognize legacy canvas forms; never guess past a malformed declared canvas."""
    if not isinstance(snapshot, dict):
        if snapshot is None:
            return (256, 256)
        raise ValueError('legacy profile is not an object; specify --canvas explicitly')
    for key in ('current_working_canvas', 'canvas'):
        if key not in snapshot:
            continue
        value = snapshot[key]
        if isinstance(value, dict):
            dims = (value.get('width'), value.get('height'))
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            dims = tuple(value)
        elif isinstance(value, str) and re.fullmatch(r'[1-9][0-9]*[x×][1-9][0-9]*', value):
            dims = tuple(map(int, re.split('[x×]', value)))
        else:
            raise ValueError('unrecognized legacy ' + key + '; specify --canvas explicitly')
        if any(type(n) is not int or n <= 0 for n in dims):
            raise ValueError('invalid legacy ' + key + '; specify --canvas explicitly')
        return dims
    return (256, 256)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.', help='project root; all stored paths are relative to it')
    parser.add_argument('--spec', default='project_spec.json', help='project-relative spec path')
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--input-type', choices=INPUT_TYPES, default='text')
    init.add_argument('--entry-stage', choices=STAGES, default='intake')
    init.add_argument('--canvas', help='WIDTHxHEIGHT; default 256x256, or recognized legacy dimensions')
    init.add_argument('--legacy-profile', help='existing project-relative JSON profile, read without modification')
    sub.add_parser('check')
    routing = sub.add_parser('route')
    routing.add_argument('target', choices=STAGES)
    args = parser.parse_args(argv)
    try:
        root = Path(args.root).resolve(strict=True)
        path = safe_path(root, args.spec, must_exist=args.command != 'init')
        if args.command == 'init':
            snapshot = None
            if args.legacy_profile:
                legacy = safe_path(root, args.legacy_profile)
                snapshot = json.loads(legacy.read_text(encoding='utf-8'))
            if args.canvas is not None:
                if not re.fullmatch(r'[1-9][0-9]*x[1-9][0-9]*', args.canvas):
                    raise ValueError('--canvas must be WIDTHxHEIGHT with positive integers')
                canvas = tuple(map(int, args.canvas.split('x')))
            else:
                canvas = legacy_canvas(snapshot) if args.input_type == 'existing_project' else (256, 256)
            spec = new_spec(args.input_type, canvas, args.entry_stage)
            if args.legacy_profile:
                spec['legacy_profile'] = {'path': args.legacy_profile, 'snapshot': snapshot,
                                          'note': 'Read-only import; no artifacts or approvals inferred. Original is unchanged.'}
            with path.open('x', encoding='utf-8') as stream:
                json.dump(spec, stream, indent=2, ensure_ascii=False)
                stream.write('\n')
            result = {'created': args.spec, 'entry_stage': args.entry_stage, 'gates': 'pending'}
        else:
            spec = json.loads(path.read_text(encoding='utf-8'))
            result = check(root, spec) if args.command == 'check' else route(root, spec, args.target)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result.get('errors') or result.get('technical_validation') is False else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
