# Visual review and technical gates

## Review order

1. **Identity:** face, eyes, hair, ears, clothing, footwear, silhouette, and actual anatomy. Inspect source and output side by side at matched character height. Check discrete facts (counts, sides, presence of details) separately from drawing quality: a clean back view showing two of three tails is still wrong.
2. **Motion:** recognizability without FX, support and weight, contacts that actually land, event accent, timing/spacing, proximal drive, follow-through (hair and clothing answer the body's momentum), depth, loop seam, and effects that start at their causing event and follow their driver.
3. **Pixels through time:** coherent clusters, deliberate staircase contours, stable small features, no source fragments, holes, crawling outlines, or unexplained volume changes.
4. **Export:** layers, frame order, size, transparency, colors, exposures, sheet reconstruction, and final decoded playback.

Separate written judgments. “Technical checks pass; sleeve motion still feels rigid at 1.1–1.4 seconds” is useful. “All checks pass, 95% natural” is not.

Inspect every authored frame against the accepted identity/reference set before final acceptance. In every composite frame, transitions as much as accents, every held prop shows its identifying detail, or its occlusion cannot be misread: a bare blade beside a similar object reads as that object, however briefly it shows. The eye misses these at 1×: count identity colors (eyes or lashes, gems, other markers) in every frame against the neutral pose, e.g. with `audit`'s `identity_colors`, on the character and prop layers if effects share a color. A drop flags a frame to inspect; a count cannot see adjacency, so also check that each prop reads as held by the right hand (the hand shows, or its occlusion cannot be misread) and touches no other hand, arm or similar-colored part (a dagger against the other wrist reads as one hand holding two). Recount every frame after each fix: fixes move props into new overlaps. Use a frame review log or checked frame ranges; investigate all flagged areas and view transitions, not only selected attractive frames. A contact sheet can cover the set, but face/footwear/overlap details may need individual crops.

The author misses their own regressions. Before delivering views or an animation, give a fresh reviewer (a subagent with image access, or a human) the files, identity sheet and criteria, not your conclusions. It reports blocking faults with coordinates: a wrong identity fact, a visible hole, tear or detached part, or a key pose that misreads, including a discrete fact misread through occlusion or adjacency (a dagger that appears to sit in the other hand). Fix and re-review, at most three rounds per change request (new user feedback starts a new count). Each round uses a new reviewer who sees the whole clip and is told which regions changed and what earlier rounds settled: fixes cause regressions elsewhere, and a returning reviewer rechecks only its own findings. A spot-check of a pinpoint fix is labeled a spot-check, not a round. Then report what remains. Without a reviewer, keep the gate pending.

## Edge cleanup is local and temporal

Inspect against checkerboard, light, and dark backgrounds at native size and integer nearest-neighbor zoom. Test actual alpha, not the viewer's checkerboard illusion. For deliberately crisp sprites, preserve binary transparency. Allow a different alpha policy only if the art brief actually calls for it.

Identify the cause before removing pixels:

- Source segmentation fragments: inspect the isolated source and layer; remove only verified contaminants. Preserve face/hair/ear islands that are intentional.
- Jagged cluster design: redraw a short coherent staircase/edge run, not global smoothing or blur.
- Thin support or changing depth: repair the underlying pose/envelope, not just the composite silhouette.
- Temporal crawling: align the same local anatomical region across adjacent frames and stabilize its cluster transition. Raw full-frame differences confuse correct motion with noise.
- Small isolated components: inspect them with anatomical/layer context. A 4-neighbor isolated diagonal pixel may be 8-neighbor connected; a small visible tip can be valid. Do not globally remove every component below a size threshold.

Treat sparse-contour detection as a proposal, not a deletion list. Per-layer connectivity can pass while the final composite develops a transparent pinhole where cloth and appendages meet. `audit` lists each frame's enclosed transparent regions; each is a pinhole to repair or an intentional gap to declare as `design_gaps`. Removing a single sleeve bridge can also detach a larger intentional tip. Recompose all layers after edits, inspect light and dark backgrounds, preserve thin intentional connections, and revert any new holes, flicker, or detached features.

Before review, diff each revision against the previous one and confirm it changed only where intended; stop the build when an edit fails (a silent failure leaves the revision unchanged or half edited). If the canvas, origin or timing moved, align first (by the offset, or by pairing the same poses), or every pixel shows as changed. Review three consecutive frames around each modification and the whole clip afterward. Confirm every fix on the composited export, not in the edited part: draw order or another layer can hide it. The same holds for your own check scripts: measure what is rendered and visible; a script that compares a generator's data with itself always passes. Record only what is visible there, ideally with a pixel count or difference image. Difference masks must show intentional local edits; less changed area is not itself higher quality. Do not erase shoe straps, pupils, highlights, fingers, or tail-root detail to improve a component statistic.

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
- Inspect a loop's last-to-first transition as motion. A one-shot that jumps back to its start (typically a travelling one) is a cut: declare `seam: "cut"` and note it in the final index. Identical endpoint images are neither required for every seamless loop nor proof of a good loop.

Report subjective scores only if they help the user and name the scale and evidence. Do not reuse old rejected-version scores, confuse reviewer judgment with user acceptance, or inflate motion quality from correct metadata.
