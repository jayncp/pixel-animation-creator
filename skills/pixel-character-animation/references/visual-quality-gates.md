# Visual review and technical gates

## Review order

1. **Identity:** face, eyes, hair, ears, clothing, footwear, silhouette, and actual anatomy. Inspect source and output side by side at matched character height.
2. **Motion:** recognizability without FX, support and weight, event accent, timing/spacing, proximal drive, follow-through, depth, and loop seam.
3. **Pixels through time:** coherent clusters, deliberate staircase contours, stable small features, no source fragments, holes, crawling outlines, or unexplained volume changes.
4. **Export:** layers, frame order, size, transparency, colors, exposures, sheet reconstruction, and final decoded playback.

Separate written judgments. “Technical checks pass; sleeve motion still feels rigid at 1.1–1.4 seconds” is useful. “All checks pass, 95% natural” is not.

## Edge cleanup is local and temporal

Inspect against checkerboard, light, and dark backgrounds at native size and integer nearest-neighbor zoom. Test actual alpha, not the viewer's checkerboard illusion. For deliberately crisp sprites, preserve binary transparency. Allow a different alpha policy only if the art brief actually calls for it.

Identify the cause before removing pixels:

- Source segmentation fragments: inspect the isolated source and layer; remove only verified contaminants. Preserve face/hair/ear islands that are intentional.
- Jagged cluster design: redraw a short coherent staircase/edge run, not global smoothing or blur.
- Thin support or changing depth: repair the underlying pose/envelope, not just the composite silhouette.
- Temporal crawling: align the same local anatomical region across adjacent frames and stabilize its cluster transition. Raw full-frame differences confuse correct motion with noise.
- Small isolated components: inspect them with anatomical/layer context. A 4-neighbor isolated diagonal pixel may be 8-neighbor connected; a small visible tip can be valid. Do not globally remove every component below a size threshold.

Treat sparse-contour detection as a proposal, not a deletion list. Per-layer connectivity can pass while the final composite develops a transparent pinhole where cloth and appendages meet. Removing a single sleeve bridge can also detach a larger intentional tip. Recompose all layers after edits, inspect light and dark backgrounds, preserve thin intentional connections, and revert any new holes, flicker, or detached features.

Review three consecutive frames around each modification and the whole clip afterward. Difference masks must show intentional local edits; less changed area is not itself higher quality. Do not erase shoe straps, pupils, highlights, fingers, or tail-root detail to improve a component statistic.

For appendage topology, inspect root overlap, union and branch connectivity, and main-body thickness. Clearly label connectivity definitions and root neighborhoods. An 8-connected result is not proof of strong volume or natural motion; erosion can be diagnostic but is not a deletion prescription.

## Evidence to record

Maintain a short review log with artifact path/hash, revision, reviewer, viewing method, actual playback speed, regions/frames inspected, defects found, changes made, and remaining limits. A screenshot proves a frame was visible, not how long a reviewer watched. Record playback only when genuinely observed with an available player.

Use contact sheets to find frame-level errors and playback to evaluate timing. Visually inspect actual generated images using an image-capable tool. Do not substitute code inspection, numerical QA, or a verbal description of what an animation ought to look like. If a required visual/playback capability is unavailable, deliver a labeled candidate with that review pending rather than inventing completion.

## Export checks

- PNG frames have intended dimensions, consistent origin, and correct transparency.
- Authored exposures survive native and GIF export; GIF uses 10 ms units, and viewers may clamp very short frames.
- Compare decoded GIF by the union of source/encoded time boundaries. Frame counts can differ when exact duplicate poses are merged.
- Require lossless visible RGB/alpha where promised. Use an exact shared palette if it fits; otherwise use PNG/APNG or a declared, reviewed palette reduction. Do not silently quantize a control experiment.
- Reconstruct the sprite sheet against each frame and its timing JSON.
- Reopen the native document; check layer/cel order, frame exposures, and exported pixels. Programmatic candidates are not proof of native edits.
- Inspect first-to-last transition as motion. Identical endpoint images are neither required for every seamless loop nor proof of a good loop.

Report subjective scores only if they help the user and name the scale and evidence. Do not reuse old rejected-version scores, confuse reviewer judgment with user acceptance, or inflate motion quality from correct metadata.
