# Pixel scale: grid, canvas, export

Three sizes describe the art; record them separately in the project record.

- **Pixel grid.** Set when the character reference is made, from the user's pixel reference (its native grid) or requested pixel size, otherwise a 256×256 canvas per view for a new project. One cell is one pixel, and the character's size in cells sets how much detail it can carry; record the reference canvas and the character's height in cells.
- **Canvas.** The area around the character. A 96×96 pixel source can sit unchanged on a 128×128 canvas that leaves room to move. Animation and effect canvases grow or shrink with the content (a wide slash, a projectile's flight); the character keeps the reference's grid and is never rescaled to fit.
- **Export scale.** An integer N applied only at export, to the finished frames; the grid does not change (a 128 canvas exports at 256 with N = 2). The default enlargement is Scale2x (Scale3x for 3×, Scale2x twice for 4×, nearest neighbor for other factors): each pixel becomes an N×N block whose sub-pixels may take a neighbor's color, so diagonal steps smooth slightly and small shapes round. When the user asks for a direct export, use nearest neighbor: every pixel becomes a plain N×N block. MMPX is an option that keeps corners and small shapes better. The 1× frames remain the master: audit, diff and review pixel structure there. Make the N× copies after the 1× frames pass review, name them with the factor, export and verify them from their own manifest, and record N and the method.

A size in a request can mean the grid, the canvas or the export; record the reading. When a pixel reference sets the grid, a larger requested size is usually met by the export scale, unless the user asks for more detail. If the size is not a multiple of the grid, widen the canvas to one that divides it (96 art on a 128 canvas, exported at 2× as 256), or ask. Changing the grid is redrawing, not resampling: a finer grid adds detail, a coarser one compresses it.

## Choosing and recovering a grid

The smallest feature that must read sets the scale; for a character it is usually the eyes. List the identity features with their size in pixels on the planned grid: a feature under 1 px is enlarged or dropped on purpose, never lost in conversion. A larger grid is not automatically better: every frame has more pixels to keep consistent, and empty area invites noise.

- Pixel art shown enlarged (a 1024 image of 256 art): confirm the integer factor and recover the grid by nearest sampling.
- A generated pixel-look image has its own grid, often noninteger, offset and drifting. Find the pitch from the spacing of color edges (per-column and per-row edge profiles, or their FFT) and the offset that aligns them, snap each cell boundary to the nearest edge peak so drift does not accumulate, then sample cell centers. Most cells should then be one color; if they are not, the grid is wrong or the image is painterly: use the landmark route below.

Recovering a source's own grid is nearly lossless. Moving to a different grid is the separate step below.

## Compressing to a coarser grid

Any automatic reduction yields a draft to redraw, not the result.

1. Cut the character out at the source resolution first. Transparent pixels never take part in color statistics, and background spill is removed before sampling; otherwise it lands as specks of a similar material.
2. Take scale from body landmarks shared with the master (head height, eyes, feet), not the bounding box.
3. Give each block a locked-palette color, never an average. A plain majority loses every line narrower than about half a block (outlines, pupils, mouths, straps): let these protected roles win once they cover a fair share of the block, or leave outlines out of the vote and re-derive them from material boundaries.
4. Match colors in a perceptual space such as OKLab and within the region's own material ramp: neutrals only to neutrals (a dark grey must not become a dark brown), a skin–outline blend never to hair.
5. Redraw what the reduction broke, comparing with the source side by side: a continuous contour, eyes and face, counts of repeated parts, leftover specks.

The smaller the grid, the more is chosen rather than kept: masses first, then the signature details; let the rest go. Outlines take a large share of a small sprite, so drop interior lines, use a colored or selective outline, merge close ramp steps or enlarge the head and eyes as the size requires. A drawing approach suited to the size (no outline, chunkier proportions) is legitimate; record it as a change.

## Adding detail on a finer grid

Export enlargement adds no authored detail, Scale2x included. A finer grid is redrawn. For an exact doubling, a color-preserving 2× gives a draft (palette-exact, binary alpha kept): Scale2x (EPX) rounds small shapes, so a small fist becomes an oval and blade tips blunt, while MMPX (McGuire & Gagiu 2021) keeps corners, tips and single pixels better. Either draft keeps 2 px lines and 2×2 single features beside new 1 px steps, which reads as two pixel sizes. Bring every visible feature to the new unit (1 px outlines, reshaped eyes and highlights, redone dither) and spend the added detail on identity features first, from the locked palette or deliberate new ramp steps; otherwise keep the old grid and use the export scale. Other ratios are redrawn without that draft.

Blending upscalers (bilinear, hqx, xBR, AI upscalers) invent colors and partial alpha: never use them for a master or a review image. Run any automatic pass identically on every frame and keep hand-added details attached to the parts that carry them, or they flicker.

## Export checks

Scale2x and MMPX change the drawing slightly, so review their copies at export size, held props and small features first. If a grip or tip stops reading (Scale2x can turn a small fist into an oval), adjust the 1× drawing, or note it and offer MMPX or a direct export. Nearest-neighbor copies equal the 1× frames block for block and need none of the checks below.

- The filter turns a 1 px change into a change of shape: fix flicker at 1× first.
- Thin shapes joined only diagonally (blade tips, staircase diagonals, close parallel lines) can enclose new one-pixel holes: check enclosed holes at both sizes, and give thin shapes 4-connected runs or wider spacing.
- When layers are delivered separately, upscale each layer and stack the results to make the composite, since the filter of a flattened image differs where layers meet. Clear lower-layer pixels hidden under an upper layer (rounding exposes them) and seal single-pixel seams where two touching layers both round inward.

## Rotation

Rotation resamples too. A RotSprite-like route (color-preserving magnify, rotate with nearest sampling, reduce) keeps lines best; clean silhouette, small features and line thickness afterwards, as in the cut-out notes of [motion-design.md](motion-design.md).
