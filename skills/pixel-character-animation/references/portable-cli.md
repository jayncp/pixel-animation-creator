# Portable CLI and manifest

The helper automates validation, contact sheets, sampled timing diagnostics, and exact GIF/sprite-sheet encoding. It does not choose good key poses, generate new characters, repair arbitrary edges, or perform visual review. Those are authored and reviewed by the agent using the workflow.

## Manifest

Create `action.json` in the project root. Copy the structure from `assets/action_manifest.example.json`, replacing example paths, canvas, durations, and coordinates with actual data. Its frame files are intentionally not bundled demo art. Required fields:

- `schema_version: 1`.
- `frames`: explicit ordered array of `{ "path": "relative/frame.png", "duration_ms": 100 }` objects. Do not rely on lexicographic file ordering.
- Optional `canvas: [width,height]`, `loop: true/false` (default true), `binary_alpha: true/false` (default true).
- Optional `seam: "motion"/"cut"` (default `"motion"`): how a looping clip's last frame meets its first. `"cut"` declares a jump (a one-shot, travelling skill restarting at its origin), so timing leaves out that step and `audit` does not compare the first and last frames.
- Optional per-frame `anchors`: named finite `[x,y]` coordinates of the actual rendered pose at that frame's onset. Use consistent origin/branch identity. Include world/screen and root-relative tracks under distinct names if useful. Do not report an unused rig track as if it drove the image.
- Optional per-frame `design_gaps`: integer `[x,y]` pixels inside intentional enclosed transparent regions; holes containing one are reported as declared. Coordinates are in that frame image's pixels (export scale if frames were enlarged, not the logical canvas). `audit` warns about a declared point that lies in no enclosed region, which is stale after a pose change.
- Optional `identity_colors`: `{ "name": ["#rrggbb", ...] }`, the colors of small identity markers (eye or lash, gems). `audit` counts them per frame and warns where a count falls below half its peak in the clip, or is zero in every frame (a wrong code or an undrawn marker). This proposes frames to inspect for occlusion; a hidden frame (a blink) or a color shared with effects also triggers it.
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

`audit` reports image hashes, transparency, dimensions, visible color count, exact consecutive pose holds, frame onsets, optional track diagnostics, optional topology, each frame's enclosed transparent regions (undeclared ones and stale `design_gaps` are warnings) and optional identity-color counts. It exits 2 on technical errors; warnings are not automatic failures. “technical_pass” is deliberately separate from “naturalness: not_assessed_by_this_script.” No metric authorizes indiscriminate pixel deletion. Audit a character-only manifest and the composite separately: gaps between effect strokes and a projectile are not character holes; declare them or draw the effect so it does not enclose space. When effects cross the body in most frames (afterimages, slashes), classify rather than hand-declare: a composite region that is not enclosed in the character layer is effect-made. Keeping back-layer effects 1 px clear of the silhouette and dropping specks left after occlusion prevents most of them.

`export` writes `animation.gif`, `sprite_sheet.png`, `sprite_sheet.json`, and `export_validation.json`. It reserves one palette entry for transparent pixels and supports up to 255 visible RGB colors. It refuses alpha loss or silent color quantization. GIF exposures must be positive multiples of 10 ms within GIF's delay range. Use `--no-gif` for lossless PNG sheet output if a GIF cannot represent the source, then author/review a palette or timing change if desired. Very short GIF delays may be clamped by viewers even when encoded correctly.

GIF verification decodes the finished file and compares visible RGBA for every source/encoded time interval. Other encoders may merge identical poses, so the verifier does not require equal frame counts. This helper deliberately retains every authored exposure as a full-canvas, noninterlaced image descriptor with a shared exact palette and disposal method 2. It uses public still-GIF encoding plus block assembly because Pillow’s multi-frame save can crop rectangles even with optimize=False. That cropped form decoded correctly in the observed test but produced streaks in GIMP animation playback; full-canvas descriptors are a compatibility safeguard, not proof that all players behave identically. Colors underneath fully transparent pixels are ignored, while the sprite sheet preserves complete source RGBA. New exports refuse existing output files; choose a new revision directory. `--force` is an explicit overwrite option, not a default.

The topology diagnostic reports 4- and 8-neighbor components and pixels in components not touching a configured root neighborhood. It does not infer hidden skeletons, correct depth, branch continuity, or artistic intent. Root coordinates and radius must actually represent the source. For tip continuity, supply consistent anchor tracks and inspect actual frames.

`edge-diff` compares a cleanup candidate with its predecessor, pairing frames by the time interval in which both are visible, so inserted or retimed frames are allowed when the total duration matches (pose changes then also appear as edits). Run it on the actual composited character and, where useful, on the responsible isolated layers. It flags newly transparent pixels surrounded by at least five visible neighbors, new undeclared enclosed holes and increases in 8-connected component count. This is a deliberately simple proposal generator, not a complete hole detector or an artistic veto. Real limb movement or valid separated effects can change component counts. Visually inspect flagged regions plus neighboring frames; a clean report does not prove clean edges. After geometry edits it can propose many concave contour corners; rely on the enclosed-hole report and spot-check the proposals.

## Tests and dependency scope

Python 3.10+ and Pillow 10–12 are the declared runtime; tested versions are recorded in the repository's docs/VALIDATION.md, and no claim is made that every supported minor version was exercised. Run:

```sh
python -m unittest discover -s /path/to/pixel-character-animation/tests -v
```

Tests generate temporary synthetic frames, exercise the CLI/library behavior, and check pixel/timing equality, portability, duplicate holds, the loop default and loop seam tracking (including declared cuts), corruption detection, exact GIF limits, path containment (including a symlinked library root), non-overwrite behavior, enclosed holes, identity-color counts (including a marker absent from every frame), stale design gaps, time-aligned edge comparison, full-canvas GIF descriptors, and a recomposited multilayer junction/one-pixel bridge fixture. If ImageMagick is already available, an additional test independently coalesces the GIF and compares pixels; it is skipped, not installed, otherwise. The format-level descriptor test still runs without it. An independent decoder test cannot substitute for checking a player whose animation compositing differs from its import decoding. They establish tool behavior, not animation quality.
