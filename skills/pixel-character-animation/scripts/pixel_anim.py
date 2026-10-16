#!/usr/bin/env python3
"""Portable pixel-animation diagnostics and lossless exports. No art synthesis."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def asset(root, name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or Path(name).is_absolute():
        raise ValueError(f"Asset path must be a nonempty relative path: {name!r}")
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Asset path escapes manifest root: {name}")
    if not path.is_file():
        raise ValueError(f"Asset does not exist: {name}")
    return path


def load_manifest(path):
    path = Path(path).resolve()
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("Manifest root must be an object")
    for field in ("loop", "binary_alpha"):
        if field in doc and not isinstance(doc[field], bool):
            raise ValueError(f"{field} must be a boolean")
    if not isinstance(doc.get("topology", []), list) or any(not isinstance(g, dict) for g in doc.get("topology", [])):
        raise ValueError("topology must be an array of objects")
    if doc.get("schema_version") != 1:
        raise ValueError("Manifest schema_version must be 1")
    entries = doc.get("frames")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Manifest frames must be a nonempty ordered array")
    frames = []
    root = path.parent
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"Frame {i} must be an object")
        duration = entry.get("duration_ms")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            raise ValueError(f"Frame {i} duration_ms must be a positive integer")
        file = asset(root, entry.get("path"))
        with Image.open(file) as source:
            if getattr(source, "n_frames", 1) != 1:
                raise ValueError(f"Frame {i} must be a still image, not animation")
            im = source.convert("RGBA")
        if not isinstance(entry.get("anchors", {}), dict):
            raise ValueError(f"Frame {i} anchors must be an object")
        for name, xy in entry.get("anchors", {}).items():
            if not isinstance(xy, list) or len(xy) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in xy):
                raise ValueError(f"Frame {i} anchor {name}: expected two finite coordinates")
        frames.append(im)
    size = frames[0].size
    if any(im.size != size for im in frames):
        raise ValueError("All frames must have the same dimensions")
    if "canvas" in doc and doc["canvas"] != list(size):
        raise ValueError(f"Manifest canvas {doc['canvas']} differs from images {size}")
    return doc, frames, root


def pixels(im):
    """Pillow 10–12 compatible, without newer getdata deprecation warnings."""
    method = getattr(im, "get_flattened_data", None)
    return method() if method else im.getdata()


def visual_bytes(im):
    """Ignore meaningless RGB values under fully transparent pixels."""
    out = bytearray()
    for r, g, b, a in pixels(im.convert("RGBA")):
        out.extend((r, g, b, a) if a else (0, 0, 0, 0))
    return bytes(out)


def components(im, neighbors=8):
    w, h = im.size
    data = list(pixels(im.getchannel("A")))
    remaining = {i for i, a in enumerate(data) if a}
    offsets = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
               if (dx or dy) and (neighbors == 8 or abs(dx) + abs(dy) == 1)]
    result = []
    while remaining:
        start = remaining.pop()
        todo, points = [start], [start]
        while todo:
            i = todo.pop()
            x, y = i % w, i // w
            for dx, dy in offsets:
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h:
                    j = yy * w + xx
                    if j in remaining:
                        remaining.remove(j)
                        points.append(j)
                        todo.append(j)
        result.append(points)
    return sorted(result, key=len, reverse=True)


def track_report(doc):
    entries = doc["frames"]
    starts, now = [], 0
    for e in entries:
        starts.append(now)
        now += e["duration_ms"]
    names = sorted({k for e in entries for k in e.get("anchors", {})})
    tracks = {}
    pair_count = len(entries) if doc.get("loop", False) and len(entries) > 1 else len(entries) - 1
    for name in names:
        steps = []
        for i in range(pair_count):
            j = (i + 1) % len(entries)
            a, b = entries[i].get("anchors", {}).get(name), entries[j].get("anchors", {}).get(name)
            if a is None or b is None:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            d = math.hypot(dx, dy)
            steps.append({"from_frame": i, "to_frame": j, "at_ms": starts[i],
                          "dt_ms": entries[i]["duration_ms"], "dx": dx, "dy": dy,
                          "distance_px": round(d, 6),
                          "speed_px_per_second": round(d * 1000 / entries[i]["duration_ms"], 6),
                          "loop_seam": j == 0})
        tracks[name] = {"samples_present": sum(name in e.get("anchors", {}) for e in entries),
                        "largest_steps": sorted(steps, key=lambda s: s["distance_px"], reverse=True)[:10],
                        "highest_speeds": sorted(steps, key=lambda s: s["speed_px_per_second"], reverse=True)[:10],
                        "all_steps": steps}
    return {"duration_ms": now, "frame_onsets_ms": starts, "tracks": tracks,
            "interpretation": "Onset-to-onset sampled displacement divided by the earlier exposure. This is diagnostic, not a naturalness score."}


def audit(doc, frames, root):
    errors, warnings, records = [], [], []
    colors, runs = set(), []
    previous = None
    t = 0
    for i, (entry, im) in enumerate(zip(doc["frames"], frames)):
        rgba = list(pixels(im))
        alphas = sorted({p[3] for p in rgba})
        colors.update(p[:3] for p in rgba if p[3])
        if doc.get("binary_alpha", True) and any(a not in (0, 255) for a in alphas):
            errors.append(f"Frame {i} contains nonbinary alpha")
        d = entry["duration_ms"]
        if d % 10:
            warnings.append(f"Frame {i} exposure {d}ms is not exactly representable in GIF")
        if d < 20:
            warnings.append(f"Frame {i} exposure {d}ms may be clamped by some GIF viewers")
        vb = visual_bytes(im)
        if vb == previous:
            runs[-1]["duration_ms"] += d
            runs[-1]["last_frame"] = i
        else:
            runs.append({"first_frame": i, "last_frame": i, "start_ms": t, "duration_ms": d})
        previous = vb
        records.append({"frame": i, "path": entry["path"], "sha256": sha(asset(root, entry["path"])),
                        "duration_ms": d, "start_ms": t, "bbox": im.getbbox(), "alpha_values": alphas})
        t += d
    if len(colors) > 255:
        warnings.append(f"{len(colors)} visible colors exceed this helper's 255-color transparent GIF limit; PNG/sheet remain lossless")
    topology = []
    for group in doc.get("topology", []):
        paths = group.get("paths")
        if not isinstance(paths, list) or len(paths) != len(frames):
            raise ValueError("Each topology.paths array must have one layer/mask path per frame")
        radius = group.get("root_radius", 2)
        if isinstance(radius, bool) or not isinstance(radius, (int, float)) or not math.isfinite(radius) or radius < 0:
            raise ValueError("topology.root_radius must be a finite nonnegative number")
        rows = []
        for i, name in enumerate(paths):
            with Image.open(asset(root, name)) as source:
                mask = source.convert("RGBA")
            if mask.size != frames[i].size:
                raise ValueError(f"Topology mask {name} has wrong size")
            row = {"frame": i}
            root_xy = doc["frames"][i].get("anchors", {}).get(group.get("root_anchor"))
            for conn in (4, 8):
                comps = components(mask, conn)
                row[f"components_{conn}"] = len(comps)
                row[f"small_components_{conn}"] = [len(c) for c in comps if len(c) <= 4]
                if root_xy is not None:
                    root_free = [c for c in comps if not any(math.hypot(p % mask.width - root_xy[0], p // mask.width - root_xy[1]) <= radius for p in c)]
                    row[f"root_free_pixels_{conn}"] = sum(map(len, root_free))
            rows.append(row)
        topology.append({"name": group.get("name", "unnamed"), "root_anchor": group.get("root_anchor"),
                         "root_radius": radius, "frames": rows})
    return {"technical_pass": not errors, "naturalness": "not_assessed_by_this_script",
            "errors": errors, "warnings": warnings, "canvas": list(frames[0].size),
            "authored_frames": len(frames), "duration_ms": t, "visible_rgb_colors": len(colors),
            "effective_exact_pose_holds": runs, "loop_requested": bool(doc.get("loop", False)),
            "first_last_visible_equal": visual_bytes(frames[0]) == visual_bytes(frames[-1]),
            "frames": records, "timing": track_report(doc), "topology": topology,
            "topology_note": "Component/root statistics are diagnostics, not permission to delete small clusters. A connected root does not prove tip continuity."}


def matte(im, background=(44, 48, 56)):
    base = Image.new("RGBA", im.size, background + (255,))
    base.alpha_composite(im)
    return base.convert("RGB")


def contact(doc, frames, output, columns=6, scale=2):
    if columns < 1 or scale < 1:
        raise ValueError("columns and scale must be positive integers")
    w, h = frames[0].size
    cw, ch = w * scale + 12, h * scale + 32
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (columns * cw, rows * ch), (30, 33, 38))
    draw = ImageDraw.Draw(sheet)
    t = 0
    for i, (entry, im) in enumerate(zip(doc["frames"], frames)):
        x, y = (i % columns) * cw + 6, (i // columns) * ch + 6
        sheet.paste(matte(im).resize((w * scale, h * scale), Image.Resampling.NEAREST), (x, y))
        draw.text((x, y + h * scale + 3), f"F{i:03d} {t}ms +{entry['duration_ms']}", fill=(235, 235, 235))
        t += entry["duration_ms"]
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def exact_palette(frames):
    colors = sorted({p[:3] for im in frames for p in pixels(im) if p[3]})
    if len(colors) > 255:
        raise ValueError(f"Exact GIF requires <=255 visible colors with reserved transparency; found {len(colors)}. Do not silently quantize.")
    if any(p[3] not in (0, 255) for im in frames for p in pixels(im)):
        raise ValueError("Exact GIF cannot preserve nonbinary alpha")
    mapping = {c: i + 1 for i, c in enumerate(colors)}
    palette = [0, 0, 0] + [v for c in colors for v in c]
    palette += [0] * (768 - len(palette))
    out = []
    for im in frames:
        p = Image.new("P", im.size)
        p.putpalette(palette)
        p.putdata([mapping[px[:3]] if px[3] else 0 for px in pixels(im)])
        p.info["transparency"] = 0
        out.append(p)
    return out


def gif_structure(path):
    """Read GIF block boundaries, not pixel data; no external decoder needed."""
    data = Path(path).read_bytes()
    if data[:6] not in (b"GIF87a", b"GIF89a") or len(data) < 14:
        raise ValueError("Invalid GIF header")
    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")
    pos = 13 + (3 * (2 ** ((data[10] & 7) + 1)) if data[10] & 128 else 0)
    images, controls = [], []
    current = None

    def skip_subblocks(offset):
        while True:
            if offset >= len(data): raise ValueError("Truncated GIF subblocks")
            size = data[offset]
            offset += 1
            if not size: return offset
            offset += size
            if offset > len(data): raise ValueError("Truncated GIF subblock payload")

    while pos < len(data):
        marker = data[pos]
        pos += 1
        if marker == 0x3B:
            break
        if marker == 0x21:
            if pos >= len(data): raise ValueError("Truncated GIF extension")
            label = data[pos]
            pos += 1
            if label == 0xF9:
                if pos + 6 > len(data) or data[pos] != 4:
                    raise ValueError("Invalid GIF graphic control extension")
                current = {"duration_ms": int.from_bytes(data[pos + 2:pos + 4], "little") * 10,
                           "disposal": (data[pos + 1] >> 2) & 7,
                           "transparent_index": data[pos + 4] if data[pos + 1] & 1 else None}
                controls.append(current)
            pos = skip_subblocks(pos)
        elif marker == 0x2C:
            if pos + 9 > len(data): raise ValueError("Truncated GIF image descriptor")
            left, top, w, h = [int.from_bytes(data[pos + i:pos + i + 2], "little") for i in (0, 2, 4, 6)]
            packed = data[pos + 8]
            pos += 9
            if packed & 128: pos += 3 * 2 ** ((packed & 7) + 1)
            pos += 1  # LZW minimum code size
            pos = skip_subblocks(pos)
            images.append({"rect": [left, top, w, h], "full_canvas": (left, top, w, h) == (0, 0, width, height),
                           "interlaced": bool(packed & 64), "control": current})
            current = None
        else:
            raise ValueError(f"Unexpected GIF block marker {marker:#x}")
    if not images:
        raise ValueError("GIF has no image frames")
    return {"canvas": [width, height], "background_index": data[11],
            "all_frames_full_canvas": all(i["full_canvas"] for i in images), "images": images}


def write_full_canvas_gif(indexed, durations, path, loop):
    """Use public still-GIF saves, then join their complete image blocks.

    Pillow save_all(optimize=False) still crops animation frame rectangles.
    Full-canvas noninterlaced descriptors avoid the observed GIMP artifact
    while retaining disposal=2, exact palette, alpha and authored exposures.
    """
    header = None
    chunks = []
    for im, duration in zip(indexed, durations):
        buffer = io.BytesIO()
        im.save(buffer, format="GIF", duration=duration, transparency=0,
                background=0, disposal=2, optimize=False, interlace=False)
        data = buffer.getvalue()
        end = 13 + (3 * 2 ** ((data[10] & 7) + 1) if data[10] & 128 else 0)
        if data[-1:] != b";":
            raise ValueError("Still GIF encoder did not emit expected trailer")
        if header is None:
            header = data[:end]
        elif data[:end] != header:
            raise ValueError("Still GIF palette or logical screen differs between frames")
        chunks.append(data[end:-1])
    if header is None:
        raise ValueError("Cannot export an empty GIF")
    extension = b"!\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00" if loop else b""
    Path(path).write_bytes(header + extension + b"".join(chunks) + b";")
    structure = gif_structure(path)
    if len(structure["images"]) != len(indexed) or not structure["all_frames_full_canvas"]:
        raise ValueError("Compatibility GIF did not retain all full-canvas authored frames")
    if any(i["interlaced"] or i["control"] is None or i["control"]["disposal"] != 2 or i["control"]["transparent_index"] != 0 for i in structure["images"]):
        raise ValueError("Compatibility GIF control fields differ from expected values")
    return structure


def verify_gif(doc, frames, path):
    encoded, durations = [], []
    with Image.open(path) as gif:
        for i in range(gif.n_frames):
            gif.seek(i)
            encoded.append(gif.convert("RGBA"))
            durations.append(gif.info.get("duration", 0))
        loop = gif.info.get("loop")
    if (doc.get("loop", False) and loop != 0) or (not doc.get("loop", False) and loop is not None):
        raise ValueError("GIF loop extension differs from manifest loop setting")
    expected = [e["duration_ms"] for e in doc["frames"]]
    if sum(durations) != sum(expected):
        raise ValueError(f"GIF duration mismatch: {sum(durations)} != {sum(expected)}")
    if any(d <= 0 for d in durations):
        raise ValueError("Decoded GIF has nonpositive exposure")
    i = j = 0
    remain_a, remain_b = expected[0], durations[0]
    intervals = 0
    while i < len(frames) and j < len(encoded):
        if frames[i].size != encoded[j].size or visual_bytes(frames[i]) != visual_bytes(encoded[j]):
            raise ValueError(f"Decoded GIF pixel mismatch: source frame {i}, encoded frame {j}")
        dt = min(remain_a, remain_b)
        remain_a -= dt
        remain_b -= dt
        intervals += 1
        if remain_a == 0:
            i += 1
            if i < len(frames): remain_a = expected[i]
        if remain_b == 0:
            j += 1
            if j < len(encoded): remain_b = durations[j]
    if i != len(frames) or j != len(encoded):
        raise ValueError("GIF timing interval traversal did not end together")
    return {"exact_visible_rgba": True, "duration_ms": sum(durations),
            "authored_frames": len(frames), "encoded_frames": len(encoded),
            "compared_intervals": intervals, "loop_extension": loop, "sha256": sha(path)}


def export(doc, frames, output_dir, columns=8, no_gif=False, force=False):
    out = Path(output_dir)
    names = ["sprite_sheet.png", "sprite_sheet.json", "export_validation.json"]
    if not no_gif: names.append("animation.gif")
    if not force and any((out / name).exists() for name in names):
        raise ValueError("Output files already exist; choose a new revision directory or explicitly use --force")
    if columns < 1:
        raise ValueError("columns must be positive")
    durations = [e["duration_ms"] for e in doc["frames"]]
    indexed = None
    if not no_gif:
        if any(d % 10 for d in durations):
            raise ValueError("GIF exposures must be multiples of 10ms. Choose explicit timing changes, or --no-gif; no silent rounding.")
        if any(d > 655350 for d in durations):
            raise ValueError("GIF exposure exceeds the format's 16-bit delay field")
        indexed = exact_palette(frames)
    out.mkdir(parents=True, exist_ok=True)
    columns = min(columns, len(frames))
    w, h = frames[0].size
    sheet = Image.new("RGBA", (columns * w, math.ceil(len(frames) / columns) * h))
    entries = []
    t = 0
    for i, (e, im) in enumerate(zip(doc["frames"], frames)):
        x, y = (i % columns) * w, (i // columns) * h
        sheet.paste(im, (x, y))
        entries.append({"index": i, "source": e["path"], "rect": [x, y, w, h],
                        "start_ms": t, "duration_ms": e["duration_ms"]})
        t += e["duration_ms"]
    sheet_path = out / "sprite_sheet.png"
    sheet.save(sheet_path)
    with Image.open(sheet_path) as reread:
        for e, expected in zip(entries, frames):
            x, y, w, h = e["rect"]
            if reread.crop((x, y, x + w, y + h)).tobytes() != expected.tobytes():
                raise ValueError("Saved sheet differs from source frame")
    dump(out / "sprite_sheet.json", {"schema_version": 1, "image": "sprite_sheet.png",
         "canvas": list(frames[0].size), "loop": bool(doc.get("loop", False)),
         "duration_ms": t, "frames": entries})
    validation = {"sheet_exact_rgba": True, "sheet_sha256": sha(sheet_path),
                  "naturalness": "not_assessed_by_this_script"}
    if indexed is not None:
        gif_path = out / "animation.gif"
        structure = write_full_canvas_gif(indexed, durations, gif_path, bool(doc.get("loop", False)))
        validation["gif"] = verify_gif(doc, frames, gif_path)
        validation["gif"]["all_frames_full_canvas"] = structure["all_frames_full_canvas"]
        validation["gif"]["encoding"] = "full_canvas_noninterlaced_shared_palette_disposal_2"
    dump(out / "export_validation.json", validation)
    return validation


def edge_diff(before_doc, before_frames, after_doc, after_frames):
    """Propose suspicious changes in a same-pose cleanup, never delete pixels."""
    if len(before_frames) != len(after_frames):
        raise ValueError("Edge comparison requires equal authored frame counts")
    if [e["duration_ms"] for e in before_doc["frames"]] != [e["duration_ms"] for e in after_doc["frames"]]:
        raise ValueError("Edge-only comparison requires unchanged timing")
    rows = []
    for i, (before, after) in enumerate(zip(before_frames, after_frames)):
        if before.size != after.size:
            raise ValueError("Edge comparison requires matching canvas sizes")
        a, b = list(pixels(before)), list(pixels(after))
        w, h = before.size
        changed = [n for n, (x, y) in enumerate(zip(a, b)) if (x if x[3] else (0, 0, 0, 0)) != (y if y[3] else (0, 0, 0, 0))]
        erased = [n for n in changed if a[n][3] and not b[n][3]]
        suspicious = []
        for n in erased:
            x, y = n % w, n // w
            neighbors = sum(bool(b[yy * w + xx][3])
                for yy in range(max(0, y - 1), min(h, y + 2))
                for xx in range(max(0, x - 1), min(w, x + 2))
                if (xx, yy) != (x, y))
            if neighbors >= 5:
                suspicious.append([x, y])
        c_before, c_after = len(components(before, 8)), len(components(after, 8))
        rows.append({"frame": i, "changed_visible_pixels": len(changed),
                     "erased_visible_pixels": len(erased),
                     "added_visible_pixels": sum(not a[n][3] and bool(b[n][3]) for n in changed),
                     "possible_new_pinholes_xy": suspicious,
                     "components_8_before": c_before, "components_8_after": c_after,
                     "component_count_increased": c_after > c_before})
    return {"same_timing": True, "frames": rows,
            "frames_needing_junction_review": [r["frame"] for r in rows if r["possible_new_pinholes_xy"] or r["component_count_increased"]],
            "naturalness": "not_assessed_by_this_script",
            "interpretation": "Heuristic proposals only. Compare final composited character and relevant isolated layers on light/dark backgrounds; inspect adjacent frames. Small components and diagonal connections can be intentional. No automatic deletion or acceptance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("audit", "timing", "contact", "export", "verify-gif", "edge-diff"):
        p = sub.add_parser(name)
        p.add_argument("manifest")
        if name in ("audit", "timing", "contact", "edge-diff"):
            p.add_argument("--out", required=True)
        if name in ("contact", "export"):
            p.add_argument("--columns", type=int, default=6 if name == "contact" else 8)
        if name == "contact": p.add_argument("--scale", type=int, default=2)
        if name == "export":
            p.add_argument("--out-dir", required=True)
            p.add_argument("--no-gif", action="store_true")
            p.add_argument("--force", action="store_true")
        if name == "verify-gif": p.add_argument("gif")
        if name == "edge-diff": p.add_argument("candidate_manifest")
    args = parser.parse_args()
    try:
        doc, frames, root = load_manifest(args.manifest)
        if args.command == "audit":
            result = audit(doc, frames, root)
            dump(args.out, result)
            print(json.dumps({"technical_pass": result["technical_pass"], "errors": result["errors"], "warnings": result["warnings"]}))
            return 0 if result["technical_pass"] else 2
        if args.command == "edge-diff":
            after_doc, after_frames, _ = load_manifest(args.candidate_manifest)
            dump(args.out, edge_diff(doc, frames, after_doc, after_frames))
        elif args.command == "timing":
            dump(args.out, track_report(doc))
        elif args.command == "contact":
            contact(doc, frames, args.out, args.columns, args.scale)
        elif args.command == "export":
            print(json.dumps(export(doc, frames, args.out_dir, args.columns, args.no_gif, args.force)))
        elif args.command == "verify-gif":
            print(json.dumps(verify_gif(doc, frames, args.gif)))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
