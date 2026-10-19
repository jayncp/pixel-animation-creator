# Test results — 2026-10-19

macOS 26.0.1 arm64, Python3.12.12, Pillow12.3.0, ImageMagick7.1.2 available. All43 tests passed: 22 pixel_anim tests and 21 project_stage tests; none skipped. Declared Python3.10+/Pillow10–12 support is not a claim every version or OS was tested.

On 2026-10-16 (Python3.12.14, Pillow12.3.0) 40 tests passed on another platform; on macOS two of them failed because a library call compared an unresolved temporary root (`/var` → `/private/var`) with resolved asset paths. That is fixed and covered by a platform-independent symlinked-root test.

Tests cover exact GIF/sheet pixels and time intervals, full-canvas descriptors, duplicate holds, transparency clearing, palette/timing refusal, path safety, relocation/no-overwrite, corrupted exports, multilayer bridge/pinhole fixtures, enclosed holes with declared design gaps, time-aligned edge comparison, 256 default/user override, old-project canvas preservation, any-stage/imported routing, required recorded reviews, stale/missing output hashes, stale declared inputs, stage input snapshots and strict schema version.

The suite is technical evidence, not a naturalness score. Actual image/player inspection remains necessary. See repository docs/VALIDATION.md for scope and field-test results; copied-alone skill users can rerun the bundled tests.
