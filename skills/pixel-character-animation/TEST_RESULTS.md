# Test results — 2026-10-16

Python3.12.14, Pillow12.3.0. All40 tests passed:19 pixel_anim tests and21 project_stage tests. ImageMagick was available and its independent-decoder regression ran; no skipped tests. Declared Python3.10+/Pillow10–12 support is not a claim every version was tested.

Tests cover exact GIF/sheet pixels and time intervals, full-canvas descriptors, duplicate holds, transparency clearing, palette/timing refusal, path safety, relocation/no-overwrite, corrupted exports, multilayer bridge/pinhole fixtures,256 default/user override, old-project canvas preservation, any-stage/imported routing, required recorded reviews, stale/missing output hashes, stale declared inputs, stage input snapshots and strict schema version.

Independent behavior review found and fixed four stage-helper defects before release. The40-test suite is technical evidence, not a naturalness score. A real30-frame/3000ms prior idle export was exact. A fresh text-based robot generation test produced a recognizable256 candidate but failed the clean-pixel gate; it is not advertised as completed pixel art.

Actual image/player inspection remains necessary. See repository docs/VALIDATION.md for scope, independent review and release extraction checks; copied-alone skill users can rerun the bundled tests.
