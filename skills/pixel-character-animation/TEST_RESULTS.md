# Portable-helper validation

Validated on 2026-10-15 with Python 3.12.14 and Pillow 12.3.0. No packages were installed and no external service was used for these tests. Declared runtime support is Python 3.10+ and Pillow 10–12; other version combinations were not independently exercised.

## Executed tests

Command from an ordinary working directory:

`python -m unittest discover -s pixel-character-animation/tests -v`

All 19 tests passed, including the optional independent ImageMagick decode test in this runtime. They cover:

- Exact timed GIF and PNG-sheet reconstruction.
- Correct handling of duplicate holds and coalesced encoded frames.
- Actual-duration displacement/speed calculations and loop seam tracks.
- Loop metadata verification and deliberate nonloop output.
- Execution after relocation, with spaces in paths and unrelated current directory.
- Rejection of absolute/escaping paths and symlinks outside the project.
- Rejection of invalid durations, nonfinite anchors, and incorrect dimensions.
- Binary-alpha enforcement for crisp/GIF output and PNG-only fallback.
- Refusal of silent GIF timing rounding or palette quantization.
- Detection of altered source pixels or timings during GIF verification.
- Protection from accidental output overwrite.
- Nearest-neighbor contact-sheet creation.
- Distinct 4- and 8-neighbor connectivity diagnostics, without deleting source pixels.
- Transparent-frame disposal erasing prior visible poses correctly.
- Recomposition exposing a new junction pinhole, plus a one-pixel bridge removal disconnecting a tip.
- Every authored GIF exposure retained as a full-canvas noninterlaced descriptor with explicit transparency/disposal.
- Independent ImageMagick coalescing and exact visible-RGBA comparison when that existing program is available.

## Real-study regression

The helper also audited and exported the frozen V6 idle's 30 source PNGs with their native exposure durations. Results: 256×256, binary alpha, 3000 ms, technical audit without warnings, exact RGBA sheet reconstruction, and an exact visible-RGBA GIF. The initial multi-frame encoder coalesced the source into 28 encoded frames and all 30 time intervals matched. After the interoperability correction below, the same sequence was re-exported as 30 full-canvas encoded frames with the same exact pixels and 3000 ms timing.

This check exercised a real project sequence, not only synthetic fixtures. It did not generate a new action or conduct a new visual/playback acceptance review. Synthetic/encoding tests are not evidence that the skill can autonomously create production-quality animation. Behavioral use and actual multimodal review remain necessary.

## Observed GIF interoperability failure and bounded correction

An independent short-request test created a new two-projectile combo. Its first delivery GIF had 49 authored poses encoded as 47 cropped GIF rectangles over 2660 ms. Pillow round-trip checks passed, and GIMP imported all cropped layers with exact pixels and offsets. However, actual GIMP animation playback displayed horizontal and vertical brown streaks absent from the source PNGs. Thus the observed failure was GIMP playback/compositing interoperability, not evidence that all GIF decoders were wrong or that the source art contained those lines. The initial autonomous test was not a clean first-pass success.

The helper now exports each authored pose as a full-canvas, noninterlaced GIF image descriptor, retains the shared exact palette, transparency/background index 0, disposal method 2, and original exposure durations. It avoids relying on `optimize=False` to disable cropping, because that flag did not do so in the observed Pillow path. The corrected combo retained all 49 poses and 2660 ms. Pillow and independent ImageMagick coalescing both matched all visible RGBA pixels. Actual GIMP 1× playback of the corrected candidate was then reviewed on 2026-10-15 at 11:56–11:57 UTC: the brown streaks and bands were absent, and the visible charge, push, and recovery remained stable. The companion project preserves the original failure and corrected playback evidence. This observed playback result is separate from decoder equality, not inferred from it.

The change is limited to encoding/interoperability. It does not establish a universal one-call animation-quality guarantee or upgrade programmatically generated native files into editor-opened/exported verification.

## Package scope

The ZIP is portable content only. Structural checks verify required frontmatter, local reference targets, a clean file inventory, and extraction integrity. It is not installed, published, or synchronized to any personal account. There are no bundled credentials, machine-specific runtimes, software binaries, third-party tutorial images, or historical authorization grants.
