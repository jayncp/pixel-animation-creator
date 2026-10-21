import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pixel_anim.py"
spec = importlib.util.spec_from_file_location("pixel_anim", SCRIPT)
pa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa)


class PixelAnimationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.frames = []
        for x in (1, 1, 3, 2):
            im = Image.new("RGBA", (8, 8))
            ImageDraw.Draw(im).rectangle((x, 2, x + 2, 5), fill=(240, 160, 60, 255))
            self.frames.append(im)
        self.doc = {"schema_version": 1, "canvas": [8, 8], "loop": True,
                    "frames": [{"path": f"frames/f{i:03d}.png", "duration_ms": d,
                                "anchors": {"wrist": [x, 2]}}
                               for i, (x, d) in enumerate(zip((1, 1, 3, 2), (100, 120, 20, 160)))]}
        self.manifest = self.write(self.root, self.doc, self.frames)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, root, doc, frames):
        for entry, im in zip(doc["frames"], frames):
            path = root / entry["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            im.save(path)
        path = root / "action.json"
        pa.dump(path, doc)
        return path

    def test_audit_duplicates_and_timing(self):
        doc, frames, root = pa.load_manifest(self.manifest)
        result = pa.audit(doc, frames, root)
        self.assertTrue(result["technical_pass"])
        self.assertEqual(result["duration_ms"], 400)
        self.assertEqual(result["effective_exact_pose_holds"][0]["duration_ms"], 220)
        self.assertEqual(result["naturalness"], "not_assessed_by_this_script")
        steps = result["timing"]["tracks"]["wrist"]["all_steps"]
        self.assertEqual(steps[1]["dt_ms"], 120)
        self.assertAlmostEqual(steps[1]["speed_px_per_second"], 2 * 1000 / 120, places=5)
        self.assertTrue(steps[-1]["loop_seam"])

    def test_exact_gif_and_sheet(self):
        result = pa.export(self.doc, self.frames, self.root / "export")
        self.assertTrue(result["gif"]["exact_visible_rgba"])
        self.assertEqual(result["gif"]["duration_ms"], 400)
        self.assertTrue(result["sheet_exact_rgba"])
        self.assertEqual(result["gif"]["loop_extension"], 0)
        self.assertLessEqual(result["gif"]["encoded_frames"], 4)

    def test_full_canvas_gif_descriptors_preserve_every_exposure(self):
        out = self.root / "full-canvas"
        pa.export(self.doc, self.frames, out)
        structure = pa.gif_structure(out / "animation.gif")
        self.assertTrue(structure["all_frames_full_canvas"])
        self.assertEqual(len(structure["images"]), len(self.frames))
        self.assertEqual([i["control"]["duration_ms"] for i in structure["images"]], [100, 120, 20, 160])
        for frame in structure["images"]:
            self.assertEqual(frame["rect"], [0, 0, 8, 8])
            self.assertFalse(frame["interlaced"])
            self.assertEqual(frame["control"]["disposal"], 2)
            self.assertEqual(frame["control"]["transparent_index"], 0)

    def test_independent_imagemagick_decode_if_available(self):
        executable = shutil.which("magick") or shutil.which("convert")
        if not executable:
            self.skipTest("Optional independent ImageMagick decoder is not available")
        version = subprocess.run([executable, "-version"], text=True, capture_output=True, timeout=15)
        if "ImageMagick" not in version.stdout:
            self.skipTest("Executable is not ImageMagick")
        out = self.root / "independent"
        pa.export(self.doc, self.frames, out)
        proc = subprocess.run([executable, str(out / "animation.gif"), "-coalesce", "PNG32:" + str(out / "decoded-%03d.png")], text=True, capture_output=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        decoded = sorted(out.glob("decoded-*.png"))
        self.assertEqual(len(decoded), len(self.frames))
        for path, expected in zip(decoded, self.frames):
            with Image.open(path) as actual:
                self.assertEqual(actual.size, expected.size)
                self.assertEqual(pa.visual_bytes(actual), pa.visual_bytes(expected))

    def test_no_implicit_loop(self):
        self.doc["loop"] = False
        result = pa.export(self.doc, self.frames, self.root / "export")
        self.assertIsNone(result["gif"]["loop_extension"])
        self.assertEqual(len(pa.track_report(self.doc)["tracks"]["wrist"]["all_steps"]), 3)

    def test_relocation_cli_from_unrelated_cwd(self):
        target = self.root / "relocated with spaces"
        shutil.copytree(self.root / "frames", target / "frames")
        shutil.copy(self.manifest, target / "action.json")
        out = target / "review.json"
        proc = subprocess.run([sys.executable, str(SCRIPT), "audit", str(target / "action.json"), "--out", str(out)], cwd=self.root.parent, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(out.read_text())["technical_pass"])

    def test_path_escape_and_absolute_rejected(self):
        for bad in ("../outside.png", str(self.root / "frames/f000.png")):
            self.doc["frames"][0]["path"] = bad
            pa.dump(self.manifest, self.doc)
            with self.assertRaises(ValueError): pa.load_manifest(self.manifest)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            path = Path(outside) / "outside.png"
            self.frames[0].save(path)
            link = self.root / "link.png"
            link.symlink_to(path)
            self.doc["frames"][0]["path"] = "link.png"
            pa.dump(self.manifest, self.doc)
            with self.assertRaises(ValueError): pa.load_manifest(self.manifest)

    def test_symlinked_library_root_is_resolved(self):
        # Library callers may pass an unresolved root (macOS temp dirs live under the
        # /var -> /private/var symlink); containment must compare resolved paths.
        with tempfile.TemporaryDirectory() as other:
            alias = Path(other) / "alias"
            alias.symlink_to(self.root, target_is_directory=True)
            doc, frames, _ = pa.load_manifest(alias / "action.json")
            self.assertTrue(pa.audit(doc, frames, alias)["technical_pass"])
            with self.assertRaises(ValueError): pa.asset(alias, "../outside.png")

    def test_enclosed_holes_reported_and_declared_gaps(self):
        ring = Image.new("RGBA", (8, 8))
        ImageDraw.Draw(ring).rectangle((1, 1, 5, 5), fill=(40, 50, 60, 255))
        ring.putpixel((3, 3), (0, 0, 0, 0))
        # closed only by a diagonal step: still enclosed for 4-connected background
        for p in ((6, 6), (7, 6), (6, 7)): ring.putpixel(p, (40, 50, 60, 255))
        holes = pa.hole_records(pa.enclosed_holes(ring), 8)
        self.assertEqual([h["pixels"] for h in holes], [1])
        self.assertEqual(holes[0]["bbox"], [3, 3, 4, 4])
        open_edge = ring.copy()
        open_edge.putpixel((3, 1), (0, 0, 0, 0))
        open_edge.putpixel((3, 2), (0, 0, 0, 0))
        self.assertEqual(pa.enclosed_holes(open_edge), [])
        self.frames = [ring] * 4
        self.write(self.root, self.doc, self.frames)
        result = pa.audit(self.doc, self.frames, self.root)
        self.assertTrue(result["technical_pass"])
        self.assertEqual(result["frames_with_undeclared_holes"], [0, 1, 2, 3])
        self.assertTrue(any("enclosed transparent" in w for w in result["warnings"]))
        for entry in self.doc["frames"]: entry["design_gaps"] = [[3, 3]]
        result = pa.audit(self.doc, self.frames, self.root)
        self.assertEqual(result["frames_with_undeclared_holes"], [])
        self.assertTrue(result["frames"][0]["enclosed_holes"][0]["declared"])
        self.doc["frames"][0]["design_gaps"] = [[3.5, 3]]
        pa.dump(self.manifest, self.doc)
        with self.assertRaises(ValueError): pa.load_manifest(self.manifest)

    def test_identity_colors_and_stale_design_gaps(self):
        for i, im in enumerate(self.frames):
            if i != 2:
                im.putpixel((self.doc["frames"][i]["anchors"]["wrist"][0], 3), (200, 20, 40, 255))
        self.doc["identity_colors"] = {"gem": ["#c81428"]}
        self.doc["frames"][0]["design_gaps"] = [[0, 0]]
        self.write(self.root, self.doc, self.frames)
        doc, frames, root = pa.load_manifest(self.manifest)
        result = pa.audit(doc, frames, root)
        self.assertTrue(result["technical_pass"])
        self.assertEqual([r["identity_counts"]["gem"] for r in result["frames"]], [1, 1, 0, 1])
        self.assertTrue(any("'gem'" in w and "[2]" in w for w in result["warnings"]))
        self.assertTrue(any(w.startswith("Frame 0 design_gaps [[0, 0]]") for w in result["warnings"]))
        self.doc["identity_colors"] = {"gem": ["c81428"]}
        pa.dump(self.manifest, self.doc)
        with self.assertRaises(ValueError): pa.load_manifest(self.manifest)

    def test_edge_diff_pairs_frames_by_time_after_inserting_a_frame(self):
        before = {"frames": [{"duration_ms": 100}, {"duration_ms": 100}]}
        after = {"frames": [{"duration_ms": 100}, {"duration_ms": 40}, {"duration_ms": 60}]}
        solid = Image.new("RGBA", (8, 8))
        ImageDraw.Draw(solid).rectangle((1, 1, 5, 5), fill=(40, 50, 60, 255))
        holed = solid.copy()
        holed.putpixel((3, 3), (0, 0, 0, 0))
        result = pa.edge_diff(before, [solid, solid], after, [solid, solid, holed])
        self.assertFalse(result["same_timing"])
        self.assertEqual([(r["start_ms"], r["duration_ms"], r["before_frame"], r["after_frame"]) for r in result["frames"]],
                         [(0, 100, 0, 0), (100, 40, 1, 1), (140, 60, 1, 2)])
        self.assertEqual(result["frames"][2]["new_enclosed_holes"][0]["pixels"], 1)
        self.assertEqual(result["frames_needing_junction_review"], [2])
        after["frames"][2]["design_gaps"] = [[3, 3]]
        self.assertFalse(pa.edge_diff(before, [solid, solid], after, [solid, solid, solid])["frames_needing_junction_review"])
        self.assertTrue(pa.edge_diff(before, [solid, solid], before, [solid, solid])["same_timing"])
        with self.assertRaises(ValueError):
            pa.edge_diff(before, [solid, solid], {"frames": [{"duration_ms": 150}]}, [solid])

    def test_nonbinary_alpha_audit_and_gif_rejected(self):
        self.frames[0].putpixel((0, 0), (10, 20, 30, 128))
        self.write(self.root, self.doc, self.frames)
        self.assertFalse(pa.audit(self.doc, self.frames, self.root)["technical_pass"])
        with self.assertRaises(ValueError): pa.export(self.doc, self.frames, self.root / "bad")
        pa.export(self.doc, self.frames, self.root / "png-only", no_gif=True)

    def test_fractional_gif_time_refused_not_rounded(self):
        self.doc["frames"][0]["duration_ms"] = 33
        with self.assertRaises(ValueError): pa.export(self.doc, self.frames, self.root / "bad")
        self.assertFalse((self.root / "bad").exists())

    def test_palette_overflow_refused(self):
        im = Image.new("RGBA", (16, 16))
        im.putdata([(i, 255 - i, 10, 255) for i in range(256)])
        with self.assertRaises(ValueError): pa.exact_palette([im])

    def test_existing_export_is_not_overwritten(self):
        out = self.root / "export"
        pa.export(self.doc, self.frames, out)
        before = (out / "animation.gif").read_bytes()
        with self.assertRaises(ValueError): pa.export(self.doc, self.frames, out)
        self.assertEqual((out / "animation.gif").read_bytes(), before)

    def test_corrupted_pixel_or_timing_detected(self):
        out = self.root / "export"
        pa.export(self.doc, self.frames, out)
        changed = [im.copy() for im in self.frames]
        changed[2].putpixel((0, 0), (1, 2, 3, 255))
        with self.assertRaises(ValueError): pa.verify_gif(self.doc, changed, out / "animation.gif")
        self.doc["frames"][2]["duration_ms"] += 10
        with self.assertRaises(ValueError): pa.verify_gif(self.doc, self.frames, out / "animation.gif")

    def test_contact_sheet_and_diagonal_components(self):
        path = self.root / "review/contact.png"
        pa.contact(self.doc, self.frames, path, columns=2, scale=3)
        with Image.open(path) as im:
            self.assertEqual(im.size, (72, 112))
        im = Image.new("RGBA", (3, 3))
        im.putpixel((0, 0), (1, 1, 1, 255))
        im.putpixel((1, 1), (1, 1, 1, 255))
        self.assertEqual(len(pa.components(im, 4)), 2)
        self.assertEqual(len(pa.components(im, 8)), 1)

    def test_topology_reports_without_deleting(self):
        mask = Image.new("RGBA", (8, 8))
        for p in ((1, 2), (2, 2), (7, 7)): mask.putpixel(p, (1, 1, 1, 255))
        mask.save(self.root / "mask.png")
        self.doc["topology"] = [{"name": "appendage", "paths": ["mask.png"] * 4,
                                 "root_anchor": "wrist", "root_radius": 1}]
        result = pa.audit(self.doc, self.frames, self.root)
        self.assertEqual(result["topology"][0]["frames"][0]["root_free_pixels_8"], 1)
        self.assertTrue(result["technical_pass"])
        with Image.open(self.root / "mask.png") as im:
            self.assertEqual(im.getpixel((7, 7)), (1, 1, 1, 255))

    def test_transparent_frame_erases_previous_pose(self):
        self.frames[2] = Image.new("RGBA", (8, 8), (99, 88, 77, 0))
        result = pa.export(self.doc, self.frames, self.root / "transparent")
        self.assertTrue(result["gif"]["exact_visible_rgba"])

    def test_loop_metadata_mismatch_detected(self):
        out = self.root / "export"
        pa.export(self.doc, self.frames, out)
        self.doc["loop"] = False
        with self.assertRaises(ValueError): pa.verify_gif(self.doc, self.frames, out / "animation.gif")

    def test_multilayer_cleanup_junction_and_bridge(self):
        # Both isolated layer chunks appear plausible, but removing their
        # meeting pixel exposes a hole in the final recomposite.
        back = Image.new("RGBA", (8, 8))
        front = Image.new("RGBA", (8, 8))
        ImageDraw.Draw(back).rectangle((1, 1, 5, 5), fill=(40, 50, 60, 255))
        back.putpixel((3, 3), (0, 0, 0, 0))
        front.putpixel((3, 3), (100, 120, 130, 255))
        original = Image.alpha_composite(back, front)
        cleaned_front = Image.new("RGBA", (8, 8))
        candidate = Image.alpha_composite(back, cleaned_front)
        one = {"frames": [{"duration_ms": 100}]}
        result = pa.edge_diff(one, [original], one, [candidate])
        self.assertEqual(result["frames"][0]["possible_new_pinholes_xy"], [[3, 3]])
        self.assertEqual(result["frames_needing_junction_review"], [0])
        # Removing one intentionally thin bridge disconnects a valid tip.
        bridge = Image.new("RGBA", (8, 8))
        ImageDraw.Draw(bridge).line((1, 2, 5, 2), fill=(40, 50, 60, 255))
        broken = bridge.copy()
        broken.putpixel((3, 2), (0, 0, 0, 0))
        result = pa.edge_diff(one, [bridge], one, [broken])
        self.assertTrue(result["frames"][0]["component_count_increased"])
        self.assertEqual(bridge.getpixel((3, 2))[3], 255)

    def test_invalid_duration_size_and_anchor(self):
        for value in (0, -10, True, 1.5):
            self.doc["frames"][0]["duration_ms"] = value
            pa.dump(self.manifest, self.doc)
            with self.assertRaises(ValueError): pa.load_manifest(self.manifest)
        self.doc["frames"][0]["duration_ms"] = 100
        self.doc["frames"][0]["anchors"]["wrist"] = [float("nan"), 2]
        pa.dump(self.manifest, self.doc)
        with self.assertRaises(ValueError): pa.load_manifest(self.manifest)
        self.doc["frames"][0]["anchors"]["wrist"] = [1, 2]
        self.doc["canvas"] = [9, 9]
        pa.dump(self.manifest, self.doc)
        with self.assertRaises(ValueError): pa.load_manifest(self.manifest)


if __name__ == "__main__":
    unittest.main()
