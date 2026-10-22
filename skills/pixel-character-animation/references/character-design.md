# From input to pixel character and views

## Input contract

Inspect actual supplied images before deriving features. Give each source a role: identity authority, style reference, pose reference, edit target, or secondary detail. A style image must not silently override identity. When sources conflict, preserve the user's stated priority; ask only if the conflict materially changes the character. Save originals unchanged.

The reference sets the character's pixel grid ([pixel-scale.md](pixel-scale.md)): the user's pixel reference or size, otherwise the new-project default. The actor need not touch every border. Leave deliberate margins for ears, hair, hands and appendages, and align its ground line and height across views. Record the grid, canvas and any export scale separately from preview enlargement. Larger generation output is an intermediate, not the requested native sprite.

### Text-only

1. Extract explicit appearance, silhouette, costume, palette, personality and exclusions. Make modest reversible choices for unspecified details and label them, rather than ask about every color.
2. Discover an image-generation route as described in [tool-adapters.md](tool-adapters.md). Prefer the exposed built-in tool. If the tool cannot directly output pixel art on the character's grid, generate an appropriate working reference and then author the final pixel design on that grid.
3. Generate the master/reference-facing view first. Review it against the brief before propagating it into other views. Save the prompt, input role, actual provider/tool and any returned provenance; never invent seed reproducibility.
4. Pixel-author and review the master, then build the requested reference set. Check actual dimensions, alpha and visible colors after generation: a prompt asking for pixel art may still return a larger softly shaded image. Preserve it as a guide, not a finished master; do not keep retrying the same prompt in place of a permitted native-grid finishing route. Automatic approval is not required from the user at every step; retain explicit assumptions and an inspectable candidate.

### Ordinary reference image

Extract the design, not every photographic or painted detail. Identify major shapes and value groups; simplify texture into intentional clusters and material ramps. Preserve identity-critical face, trim, footwear and accessory construction. Generated stylizations can be useful drafts, but align/clean them on the actual target grid.

Do not squeeze aspect ratio to fit. Use an intentional crop only when allowed, otherwise compose within the canvas. Downsampling, palette reduction and segmentation are intermediate proposals (see compressing in [pixel-scale.md](pixel-scale.md)): inspect small features afterward, redraw collapsed eyes/straps and clean matte halos. A procedural route is not permission to replace the character with geometric placeholders.

### Pixel reference image

Recover the logical grid as described in [pixel-scale.md](pixel-scale.md) (a 1024 image may be a 4× display of 256 art). The source's grid is the character's grid unless the user asks for another; keep its pixels except requested improvements. A larger canvas (a 96×96 source on 128×128) gives the action room without changing a pixel, and a larger delivered size is then the export scale. A finer or coarser grid is redrawn, not resampled. Record which route was taken. Keep the original available for side-by-side checks.

If the source is a foreshortened action pose, keep it unchanged as the identity master and author a neutral base pose as a labeled inference. Measure proportions only from parts the perspective does not distort (often the head) and from the most extended limbs, and mark the estimates.

## Identity sheet

Record observed facts and deliberate decisions separately:

- head/body/limb proportions, silhouette and body mass;
- face/eye shape, iris/highlights where readable, expression, hair/ear construction;
- garment seams, sleeve volume, hems, socks/skin bands, shoe straps and soles;
- accessories and attachment points, asymmetry/handedness;
- appendage count (as a number), branch identity, root locations and tip shapes;
- palette roles, outline strategy (read from the source: see [pixel-art-spec.md](pixel-art-spec.md)), internal shading/AA and light convention.

Do not force human anatomy onto a creature. If the design has no feet or face, mark those checks not applicable with a reason. An action may settle a fact the source leaves uncertain (a grip, an unseen side): label the reading, keep it through the action and note any conflict with existing views.

## Multi-view construction

For a full reference-set request with unspecified views, use front, three-quarter, side, back as an explicit default. Match the supplied camera if it is intentionally top-down or isometric; do not turn a top-down game into orthographic side-view art. A subset request overrides the default. For animation continuation only, add missing views needed by the action instead of replacing an accepted set. When a single source must also be animated, make the views the action needs plus one neutral view in the source's facing for identity checks, and list other angles as optional.

Derive each view from the locked master and identity sheet; use image generation as an aid when available. Unseen surfaces are inferred designs, not recovered ground truth. Simple mirroring is acceptable only for suitably symmetric features and must be labeled. Hair parting, buckles, weapon hands and asymmetric shoes may need new drawing. So do facial features and hair: rebuild them in each view's projection instead of transplanting the front drawing (a profile eye is a narrow wedge open at the front; a profile face edge has relief). A horizontal flip is not evidence of an independently coherent opposite view. Place asymmetric parts by the character's own sides: log per view which side faces the camera (a figure facing image right shows its right side). To bring a generated guide onto the grid, follow the compressing steps in [pixel-scale.md](pixel-scale.md). Expect changed proportions.

Compare views in a same-scale panel with a landmark matrix: head height, eyes, shoulders, pelvis, knees, feet, accessory roots and tail roots, plus a row per view for each count/side/presence fact. Choose one set of joint heights as the authority, save it with the project and align every view to it. A repeat missing from one view must be explained by occlusion; generators often merge overlapping repeats. Check volume, perspective and depth order rather than demanding equal projected widths. Face and footwear need close-up review: ask whether each reads as a natural eye, hair or shoe in that view, not only whether its facts match (a front lash bar moved onto a profile passes every fact and reads as sunglasses). Mark differences as valid perspective/occlusion, intentional asymmetry, or an unresolved conflict. Reconcile conflicts before reusing the view for cels.

## Gate and deliverables

Save actual per-view PNGs on the character's grid, a review panel, identity/palette spec and source/provenance map. Judge native-size readability and enlarged pixel structure; test light/dark backgrounds. Reject unexplained feature changes, inconsistent scale, dirty contours, muddy shading, accidental extra colors and source fragments. Use [pixel-art-spec.md](pixel-art-spec.md). A panel alone is not a turntable or proof of a consistent 3D object.
