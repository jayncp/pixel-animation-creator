# Portable CLI and manifest

The helper automates validation, contact sheets, sampled timing diagnostics, and exact GIF/sprite-sheet encoding. It does not choose good key poses, generate new characters, repair arbitrary edges, or perform visual review. Those are authored and reviewed by the agent using the workflow.

## Manifest

Create `action.json` in the project root. Copy the structure from `assets/action_manifest.example.json`, replacing example paths, canvas, durations, and coordinates with actual data. Its frame files are intentionally not bundled demo art. Required fields:

- `schema_version: 1`.
- `frames`: explicit ordered array of `{ "path": "relative/frame.png", "duration_ms": 100 }` objects. Do not rely on lexicographic file ordering.
- Optional `canvas: [width,height]`, `loop: true/false`, `binary_alpha: true/false` (default true).
- Optional per-frame `anchors`: named finite `[x,y]` coordinates of the actual rendered pose at that frame's onset. Use consistent origin/branch identity. Include world/screen and root-relative tracks under distinct names if useful. Do not report an unused rig track as if it drove the image.
- Optional `topology`: array of objects with `name`, `paths` (one transparent layer/mask image per frame), `root_anchor` (an anchor name), and `root_radius` (pixels, default 2). The alpha channel defines the mask. For tails/appendages, provide union masks plus individual branches when available. Binary black/white images with fully opaque alpha are not transparency masks.

All input paths must stay under the manifest directory, including symlink resolution. This avoids inherited absolute paths and hidden dependencies. Set the manifest root high enough to encompass legitimate source assets. The helper validates path/shape constraints but does not authorize executing other project scripts.

## Commands

Run from any directory; substitute the actual extracted skill and project paths. No command installs software, calls a service, or modifies input frames.

```sh
python /path/to/pixel-character-animation/scripts/pixel_anim.py audit /path/to/project/action.json --out /path/to/project/review/technical.json
python /path/to/pixel-character-animation/scripts/pixel_anim.py timing /path/to/project/action.json --out /path/to/project/review/timing.json
python /path/to/pixel-character-animation/scripts/pixel_anim.py contact /path/to/project/action.json --out /path/to/project/review/contact.png --columns 6 --scale 2
python /path/to/pixel-character-animation/scripts/pixel_anim.py export /path/to/project/action.json --out-dir /path/to/project/export
python /path/to/pixel-character-animation/scripts/pixel_anim.py verify-gif /path/to/project/action.json /path/to/project/export/animation.gif
python /path/to/pixel-character-animation/scripts/pixel_anim.py edge-diff /path/to/project/before.json /path/to/project/after.json --out /path/to/project/review/edge_changes.json
```

Inspect the contact image with an image-capable tool and watch the GIF in an actual player at 1×. These commands do not do that for you. An exact round-trip through the encoder’s own decoder does not guarantee another application’s playback/compositing behavior. Inspect the actual delivery GIF in the intended player, not merely its imported layers.

`audit` reports image hashes, transparency, dimensions, visible color count, exact consecutive pose holds, frame onsets, optional track diagnostics, and optional topology. It exits 2 on technical errors; warnings are not automatic failures. “technical_pass” is deliberately separate from “naturalness: not_assessed_by_this_script.” No metric authorizes indiscriminate pixel deletion.

`export` writes `animation.gif`, `sprite_sheet.png`, `sprite_sheet.json`, and `export_validation.json`. It reserves one palette entry for transparent pixels and supports up to 255 visible RGB colors. It refuses alpha loss or silent color quantization. GIF exposures must be positive multiples of 10 ms within GIF's delay range. Use `--no-gif` for lossless PNG sheet output if a GIF cannot represent the source, then author/review a palette or timing change if desired. Very short GIF delays may be clamped by viewers even when encoded correctly.

GIF verification decodes the finished file and compares visible RGBA for every source/encoded time interval. Other encoders may merge identical poses, so the verifier does not require equal frame counts. This helper deliberately retains every authored exposure as a full-canvas, noninterlaced image descriptor with a shared exact palette and disposal method 2. It uses public still-GIF encoding plus block assembly because Pillow’s multi-frame save can crop rectangles even with optimize=False. That cropped form decoded correctly in the observed test but produced streaks in GIMP animation playback; full-canvas descriptors are a compatibility safeguard, not proof that all players behave identically. Colors underneath fully transparent pixels are ignored, while the sprite sheet preserves complete source RGBA. New exports refuse existing output files; choose a new revision directory. `--force` is an explicit overwrite option, not a default.

The topology diagnostic reports 4- and 8-neighbor components and pixels in components not touching a configured root neighborhood. It does not infer hidden skeletons, correct depth, branch continuity, or artistic intent. Root coordinates and radius must actually represent the source. For tip continuity, supply consistent anchor tracks and inspect actual frames.

`edge-diff` compares equal-frame, equal-timing cleanup candidates. Run it on the actual composited character and, where useful, on the responsible isolated layers. It flags newly transparent pixels surrounded by at least five visible neighbors and increases in 8-connected component count. This is a deliberately simple proposal generator, not a complete hole detector or an artistic veto. Real limb movement or valid separated effects can change component counts. Visually inspect flagged regions plus neighboring frames; a clean report does not prove clean edges.

## Tests and dependency scope

Python 3.10+ and Pillow 10–12 are the declared runtime. Tests were executed with the version recorded in `TEST_RESULTS.md`; no claim is made that every supported minor version was exercised. Run:

```sh
python -m unittest discover -s /path/to/pixel-character-animation/tests -v
```

Tests generate temporary synthetic frames, exercise the CLI/library behavior, and check pixel/timing equality, portability, duplicate holds, loop seam tracking, corruption detection, exact GIF limits, path containment, non-overwrite behavior, full-canvas GIF descriptors, and a recomposited multilayer junction/one-pixel bridge fixture. If ImageMagick is already available, an additional test independently coalesces the GIF and compares pixels; it is skipped, not installed, otherwise. The format-level descriptor test still runs without it. An independent decoder test cannot substitute for checking a player whose animation compositing differs from its import decoding. They establish tool behavior, not animation quality.
