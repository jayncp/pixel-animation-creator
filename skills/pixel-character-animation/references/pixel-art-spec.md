# Pixel-art specification and visual heuristics

These are style-aware review criteria, not a universal numerical definition of pixel art. See [research-lineage.md](research-lineage.md) for primary artists and limits.

## Decide and record

- Native per-view canvas: 256×256 for a new unspecified project, or user/existing-project size.
- Logical grid and intended 1× display size; preview scale uses integer nearest-neighbor enlargement.
- Outline treatment (full, selective, or none), transparent silhouette policy and target background.
- Palette roles and intended budget based on actual materials: base, light/shadow, accents and shared ramps. Prefer reusing colors to adding nearly identical shades. Do not impose a magic maximum or sacrifice a distinguishing feature just to reduce a count.
- Light direction and value hierarchy. Shared colors can connect ramps across materials; hue shifts are optional design choices, not mandatory effects.
- Detail priorities: silhouette and face/footwear/accessories before incidental texture. Which features must remain readable at native size?

## Review on the actual native grid

**Clusters:** block coherent large masses before tiny texture. Inspect orphan dots, noisy checker patterns and thin unstable slivers. Eyes, highlights, fingers and fur tips can legitimately be single pixels. Connectivity statistics are flags, never automatic deletion orders.

**Contours/jaggies:** a smooth intended curve needs deliberate staircase runs. Look for accidental short–long–short jumps and uneven thickness; repair pixel placement locally. Corners, jagged fur and angular fabric do not need monotonically changing runs. “Clean” does not mean abolishing the pixel staircase.

**Banding:** parallel contour/shadow strips can flatten shape or exaggerate stair steps. Describe volume with purposeful clusters instead of stacking equal-width outlines. Do not automatically erase stripes or seams that belong to the design.

**Shading:** use value separation to keep masses readable. Avoid pillow shading that follows every edge regardless of the light. Avoid gradients/dither that obscure a small face or cause temporal shimmer. Dither is available as a deliberate material/style choice, not a default conversion filter.

**Anti-aliasing:** default to a crisp transparent outer silhouette for sprites on unknown backgrounds. Sparse opaque intermediate colors inside a cluster may be appropriate manual AA. This differs from blurred resizing and semi-transparent matte fringes. If the brief calls for soft effects or partial alpha, record that separately from the character mask; keep a lossless RGBA export and disclose GIF limitations.

**Palette:** count visible colors, inspect near duplicates, test material separation and contrast. Reducing colors is a reviewed edit, not a quality score. Keep a shared stable palette across views/cels unless illumination/FX change is intentional. Lossy JPEG is not a pixel master.

**Grid consistency:** avoid mixed accidental pixel scales and noninteger blurred transforms. Rotation/resampling of source cards requires cleanup of silhouette, small features and thickness. Do not hide artifacts with global smoothing. A color-preserving 2× such as Scale2x can close new one-pixel holes where thin shapes join only diagonally (blade tips, staircase diagonals, close parallel lines): check enclosed holes at both logical and export size, and give thin shapes 4-connected runs or wider spacing.

## Reference and temporal consistency

Compare identity landmarks across views. During animation, inspect every authored frame for feature drift, volume changes, holes, source flecks, shoe/sock loss and asymmetry errors. Compare neighboring frames aligned to the anatomical region, not only whole-frame differences. Keep intentional smears and squash/stretch distinct from accidental melting.

View character-only and composite on light, dark and checker backgrounds at native size and integer zoom. Changing one layer can create a hole only after compositing; recompose and recheck. Restore a thin bridge or cluster if cleanup detaches cloth. A zero-noise detector result is not the goal; coherent readable art is.
