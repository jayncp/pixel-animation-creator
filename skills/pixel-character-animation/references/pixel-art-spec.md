# Pixel-art specification and visual heuristics

These are style-aware review criteria, not a universal numerical definition of pixel art. See [research-lineage.md](research-lineage.md) for primary artists and limits.

## Decide and record

- Pixel grid, canvas and export scale ([pixel-scale.md](pixel-scale.md)). Previews use integer nearest-neighbor enlargement; exports use the recorded export method.
- Outline strategy, transparent silhouette policy and target background. With a source, read its strategy (black, a dark of each material, selective, none) rather than pick a "best" one, and apply it to every view and frame, new parts and copies of the character, unless a grid change calls for another approach.
- Palette roles and intended budget based on actual materials: base, light/shadow, accents and shared ramps. Prefer reusing colors to adding nearly identical shades. Do not impose a magic maximum or sacrifice a distinguishing feature just to reduce a count.
- Light direction and value hierarchy. Shared colors can connect ramps across materials; hue shifts are optional design choices, not mandatory effects.
- Detail priorities: silhouette and face/footwear/accessories before incidental texture. Which features must remain readable at native size?

## Review on the actual native grid

**Clusters:** block coherent large masses before tiny texture. Inspect orphan dots, noisy checker patterns and thin unstable slivers. Eyes, highlights, fingers and fur tips can legitimately be single pixels. Connectivity statistics are flags, never automatic deletion orders.

**Contours/jaggies:** a smooth intended curve needs deliberate staircase runs. Look for accidental short–long–short jumps and uneven thickness; repair pixel placement locally. A straight slope reads cleanest with runs of n and n+1 px in a steady rhythm, a curve with runs that shrink and then grow. A 1 px line steps diagonally: an extra pixel in the inner corner of a step (an L-corner) thickens and jags it, unless the drawing has a real corner there (elbow, blade tip). Corners, jagged fur and angular fabric do not need monotonically changing runs. “Clean” does not mean abolishing the pixel staircase.

**Outlines:** where the source outlines the silhouette, the outline stays closed and darker than the fill beside it (a light, saturated line reads as a glow). A colored outline takes a darker step of the adjacent material's ramp, so new parts and copies derive theirs the same way instead of picking new colors; pure black stays where the source uses it (pupils, lashes). Interior lines separate overlapping forms, darker where the depth jump is larger, and can be left out within one surface or where colors already separate. Lightening the contour on the lit side (selout) needs a known background; switch the outline's color partway along a straight run rather than at a step, and recompute it per frame from the light direction.

**Banding:** parallel contour/shadow strips can flatten shape or exaggerate stair steps. Describe volume with purposeful clusters instead of stacking equal-width outlines. Do not automatically erase stripes or seams that belong to the design. Evenly spaced, equal-length interior lines (hair strands, folds, fur) also read as a pattern; vary their length, spacing and direction and carry the volume with mid-tones.

**Shading:** use value separation to keep masses readable. Avoid pillow shading that follows every edge regardless of the light. Avoid gradients/dither that obscure a small face or cause temporal shimmer. Dither is available as a deliberate material/style choice, not a default conversion filter.

**Anti-aliasing:** default to a crisp transparent outer silhouette for sprites on unknown backgrounds. Manual AA works inward: a few opaque intermediate colors inside the silhouette on long steps, none on 45° or straight lines. This differs from blurred resizing and semi-transparent matte fringes. If the brief calls for soft effects or partial alpha, record that separately from the character mask; keep a lossless RGBA export and disclose GIF limitations.

**Value and color:** in grayscale the silhouette, face, hands and props stay separate; steps of one material's ramp are spaced in value, and two nearly equal steps merge. Where a ramp shifts hue (warmer lights, cooler shadows, or per the declared light), identity colors still win (neutral grey hair stays neutral). Keep large areas calm and spend saturation on small accents and effects. Materials differ by contrast (metal: small hard highlights; cloth: low contrast). Each color needs enough area to read, and more frames favor fewer colors, since each must stay stable.

**Faces and hands** carry identity at small sizes: eyes drawn larger and simpler than anatomy, readable in two colors before shading, with a highlight, if used, on the lit side that stays in place across frames; hands keep enough pixels and contrast to read in fast frames. A rim light (a 1 px light edge inside the contour on the lit side) can separate a figure from a dark background.

**Palette:** count visible colors, inspect near duplicates, test material separation and contrast. Reducing colors is a reviewed edit, not a quality score. Keep a shared stable palette across views/cels unless illumination/FX change is intentional. Lossy JPEG is not a pixel master.

**Grid consistency:** avoid mixed accidental pixel scales and noninteger blurred transforms. Rotation/resampling of source cards requires cleanup of silhouette, small features and thickness. Do not hide artifacts with global smoothing. Resizing, export enlargement (with its hole and layer checks) and rotation are covered in [pixel-scale.md](pixel-scale.md).

## Reference and temporal consistency

Compare identity landmarks across views. During animation, inspect every authored frame for feature drift, volume changes, holes, source flecks, shoe/sock loss and asymmetry errors. Compare neighboring frames aligned to the anatomical region, not only whole-frame differences. Keep intentional smears and squash/stretch distinct from accidental melting.

View character-only and composite on light, dark and checker backgrounds at native size and integer zoom. Quick readability tests are easy to generate and worth looking at: a one-color silhouette (pose and props still read), grayscale (value separation), and 1× with a slight blur (what survives is the focus; what vanishes is decoration). Changing one layer can create a hole only after compositing; recompose and recheck. Restore a thin bridge or cluster if cleanup detaches cloth. A zero-noise detector result is not the goal; coherent readable art is.
