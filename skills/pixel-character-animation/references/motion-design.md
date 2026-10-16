# Motion design and temporal continuity

## Time and spacing are separate controls

Represent authored poses with exposure durations in milliseconds. Record event times such as preparation, accent/release, maximum reach, support, recovery, and settle. The animation must make sense in real time, not only by frame number.

For onset pose samples p[i], the displacement is p[i+1]−p[i], and the elapsed time is the exposure duration of frame i. Report speed as displacement / elapsed seconds, while remembering this is sampled motion, not a physical ground-truth velocity. Inspect vector direction and the trajectory, not only maximum magnitude. A large fast step may be intentional; a smaller alternating-direction step may be a bad jitter.

Equal frame durations do not imply uniform speed. Repeated identical poses create effective holds; nonuniform position spacing can create acceleration with equal exposures. Conversely, merely varying GIF durations does not make incoherent poses natural. Distinguish authored poses, encoded frames, exact duplicate runs, and preview event frames.

## Blocking before detail

Choose sufficient key poses to read the action without effects. Plan support-foot planted intervals and swing intervals, pelvis/chest changes, gaze/head intent, hand path, and cloth/appendage following. Keep body volume and limb length stable; explain apparent shortening through depth, not unexplained stretching.

Typical choices, not universal recipes:

- Idle: asymmetric breathing/settling, small regional motion, stable feet, delayed hair/cloth. Do not scale the whole body. A single repeating GIF with one blink repeats that blink every cycle; do not claim it is random or independent. Use a longer authored cycle or runtime state machine if nonperiodic behavior is actually requested.
- Projectile: readable gathering or aim where appropriate, concentrated proximal drive, fast release, brief extension, delayed sleeve motion, longer recovery. The projectile separates at an explicit release event and is no longer attached to the hand afterward.
- Barrier/support: a distinct opening accent followed by believable sustained support and small adjustments, not the projectile action in slow motion.
- Turn/whip: gaze can lead; torso/pelvis rotate and transfer support; hair/tails trail. Add genuinely drawn transition views or local contour transitions where view-card changes pop.

Avoid equal-phase body bobbing and generic smoothstep on every channel. Allow counter-motion and settling with decreasing amplitude. Tune the phase relationships to the action, not a fixed one-frame delay on everything.

## Selective in-betweens

Inspect where motion information is missing. Add a pose on a problematic arc, depth transition, large tip jump, or slow recovery, placing it according to the desired path and timing. Retain the neighboring event times when possible. More frames are not automatically smoother or stronger; uniform interpolation can erase the accent and expose distorted source textures for longer.

Use a short smear only if it describes the path and reads at full speed. Do not blur, crossfade whole view cards, or use translucent doubled silhouettes to conceal a turn.

## Appendage continuity

For tails, long hair, ribbons, capes, or cables, retain branch identity and continuous roots/control points throughout the whole action. Keep a common coordinate system; log root-relative tips as well as world/screen tips to separate body movement from appendage movement. Inspect all branches over all frames, including the loop seam and occluded intervals.

Root-connected pixels can still encode a teleporting or swapped tail. A union centroid can hide two branches exchanging positions. Use named per-branch tracks, curve overlays, actual tip clusters, and a global review. Do not infer continuity from one fixed troublesome pair or a successful nearest-neighbor matching alone.

Depth order must change coherently. When a branch goes behind the body, record its hidden trajectory rather than shortening or reassigning it. Do not “repair” a true source-segmentation fragment by incorrectly changing the real tail path.

## Cloth and far-arm geometry

Maintain an anatomically plausible elbow/wrist route, shoulder attachment, and a sleeve envelope enclosing that route. Projected sleeve width and length should decrease or change overlap as the arm recedes. A texture card cannot substitute for this volume indefinitely. Check neutral holds because a formerly fast geometric defect may become obvious after retiming.

Isolate head, torso, and far-arm layers when a white flap appears near the jaw. Identify its origin before editing. Revise the responsible cel/geometry, retain hand targets if appropriate, then check changes in adjacent frames and all related exports.

## Optional research control

When the user asks to study why motion improved, compare an unchanged baseline, identical-pixel timing-only version, and full timing/spacing/pose revision. Keep each at its authored speed. In a synchronized comparison, append neutral end holds only to the preview. Do not stretch each clip to the same length or claim pixels are unchanged without decoding and comparing them.
