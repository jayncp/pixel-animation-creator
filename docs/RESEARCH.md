# Research and design rationale

Accessed 2026-10-16. This is a paraphrased synthesis, not copied tutorial or skill source. Source pages can change. No popularity or production-readiness claim is inferred from repository names.

## Pixel craft and motion

| Primary source | Adopted | Not universalized |
| --- | --- | --- |
| [Cure: Pixel Art Tutorial](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) | Deliberate pixel control, purposeful palette, clusters and banding review | A single color-count ceiling, deletion of every isolated pixel |
| [Saint11: Cluster Sketching](https://saint11.art/pixel_art_articles/article2/) | Masses before detail, intentional contour run lengths | Monotone run lengths on all fur/corners |
| [Saint11: Anti-Alias and Banding](https://saint11.art/pixel_art_articles/article5/) | Sparse manual AA when useful, inspect contour-following bands | Blur, matte halos, mandatory AA or its absolute prohibition |
| [SLYNYRD: Human Anatomy](https://www.slynyrd.com/blog/2019/5/21/pixelblog-17-human-anatomy) | Gesture → wireframe → masses → silhouette | Six-head proportions for every character |
| [SLYNYRD: Realistic Anatomy](https://www.slynyrd.com/blog/2024/3/25/pixelblog-49-realistic-human-anatomy) | Comparable landmarks and front/side construction | Eight-head model as anatomical truth |
| [Saint11: A Basic Aseprite Animation](https://saint11.art/pixel_art_articles/article3/) | Key-pose construction, deliberate timing/spacing, editable sources | Tutorial-specific pixel increments or hold durations |
| [Animation Mentor: Timing and Spacing](https://www.animationmentor.com/blog/tutorial-animate-with-timing-and-spacing-in-mind/) | Reference → major poses → purposeful retiming | Equal frame duration implies uniform motion |
| [Animation Mentor: Anticipation](https://www.animationmentor.com/blog/anticipation-the-12-basic-principles-of-animation/) | Preparation matched to action/causality | Large wind-up for every gameplay action |
| [Animation Mentor: Overlap](https://www.animationmentor.com/blog/follow-through-and-overlapping-action-the-12-basic-principles-of-animation/) | Driver/dependent mass separation, lag and settle | Every tail must be passive or identical one-frame offset |
| [Animation Mentor: Character Size](https://www.animationmentor.com/blog/tutorial-animating-big-and-small-characters/) | Adjust source motion to target reach/size/clearance | Small always fast, large always slow |

This research pass inspected accessible article text and links; linked tutorial media could not all be visually retrieved. It does not claim a new frame-by-frame video analysis of those examples. The runtime skill explicitly requires actual accessible motion-reference observation for a new action. Multi-view consistency and character-specific physical plausibility remain judgments on actual project images, not conclusions supplied by general tutorial text.

## Pixel detail and scale

Accessed 2026-10-21. A research pass on outline and color craft, per-frame pixel faults, effects and scaling: three sources from the owner, three web tracks, and five experiments on the field-test rogue. The notes and experiments live outside this repository.

| Source | Adopted | Not universalized |
| --- | --- | --- |
| [xccds: Pixel Art Book](https://github.com/xccds/pixel-art-book) (owner) | Craft rules as measurable checks (run lengths, L-corners, value separation); scripts list pixel faults, the eye judges structure | Its numeric thresholds as pass marks |
| [Colorify resize docs](https://comeixalpha.github.io/docs/universal_params/resize) (owner) | Nearest neighbor for enlarging pixel art; averaging filters only as an intermediate when shrinking | Its image-to-block-art mapping |
| [xxwywzy: pixel art tutorial part 1](https://xxwywzy.github.io/2019/06/22/pixel-1/) (owner) | Introductory; covered by the other sources | |
| [Saint11: Pixel Art Tutorials](https://saint11.art/blog/pixel-art-tutorials/) | Redraw rather than rescale; outlines cost space at small sizes; dark-then-white effect onset; dissolve order; no wind-up frame on player attacks | Card frame counts and timings |
| [Lospec: Pixel Art Outlines](https://lospec.com/articles/pixel-art-outlines/), [Pixel Parmesan: Resolution](https://pixelparmesan.com/choosing-the-right-resolution-for-your-pixel-art/) | Outlines for contrast, colored outlines from the adjacent ramp; the smallest necessary detail sets resolution | Lit-side outline lightening or broken outlines on unknown backgrounds |
| [McGuire & Gagiu: MMPX](https://jcgt.org/published/0010/02/04/), [Scale2x](https://www.scale2x.it/) | Scale2x stays the default export enlargement (owner's choice), with nearest neighbor on request and MMPX as an option that keeps fists and tips that EPX rounds; either filter as a draft for a finer grid | Treating a filtered export as added detail |
| [unfake.js](https://github.com/jenissimo/unfake.js), [PixelOE](https://github.com/KohakuBlueleaf/PixelOE), [OKLab](https://bottosson.github.io/posts/oklab/) | Grid recovery for generated pixel-look images; protected roles win the block vote; perceptual matching within a material ramp | Learned pixelization (heavy, license limits); averaging samplers |

Experiments: a recolor-only pass removed L-corners from a rotated boot without changing its silhouette. Automatic compression of a generated guide recovered its grid (about 6.31 px per cell), but the reduction to the target was only a draft; protected-role voting left fewer orphan pixels than a plain majority. A port of the paper's MMPX listing, whose EPX path reproduced the delivered Scale2x frames exactly, kept a 3×4 fist and blade tips that Scale2x rounded.

## Public skill structures inspected

| Source | Adopt | Reject / constrain |
| --- | --- | --- |
| [OpenAI imagegen](https://github.com/openai/skills/blob/main/skills/.system/imagegen/SKILL.md) | Input roles, preserve/change brief, capability-specific routing, local asset persistence | Generated pixel-looking art automatically counts as native-grid final |
| [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | Thin entrypoint, progressive references, deterministic helpers and realistic tests | A large framework or file count as a goal |
| [Anthropic algorithmic-art](https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/SKILL.md) | Separate aesthetic choices from infrastructure, actual parameter provenance | Fixed p5.js runtime or geometry substituted for character drawing |
| [Anthropic canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md) | Design intention and focused refinement rather than extra decoration | Generic prestige language or fictitious user perfection demands as acceptance |
| [Anthropic slack-gif-creator](https://github.com/anthropics/skills/blob/main/skills/slack-gif-creator/SKILL.md) | Dedicated builder/validator, output target separate from masters | Bicubic transforms, thick outlines, gradients and sine waves as pixel defaults |
| [Remotion best-practices](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/SKILL.md) | Conditional routing, preserve user edits, preview separate from final render | React/Remotion as mandatory sprite tooling |
| [OpenAI hatch-pet](https://github.com/openai/skills/blob/main/skills/.curated/hatch-pet/SKILL.md) | Canonical identity, artifact-backed completion, deterministic atlas geometry | App-specific dimensions/states/FX rules imposed on general animation |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Isolated realistic evaluation, old/new baseline, objective and qualitative checks | Numeric pass rates as proof of beauty/naturalness |

An attempted current official develop-web-game skill URL returned 404; mirrors were not treated as current official evidence. These are operational patterns, not independent evidence that any cited skill reliably produces excellent pixel animation.

## Tool findings

- Existing Codex CLI 0.159.2 help was inspected; no dedicated image-generation subcommand. `--image` is an input option, not evidence of generation access.
- Existing image adapter dry-run succeeded without a live API call; it did not create an image. Model/transparent-output capability differs across interfaces/versions, so inspect the chosen route instead of hardcoding a universal model assertion.
- Community [Vollkorn-Games Aseprite MCP](https://github.com/Vollkorn-Games/aseprite-mcp), reviewed commit28900e757d7e5c18515ad0a95558acde1865aad2, previously supported actual native pixel/cel editing and export in this experiment. It is not an official Aseprite product. Its license does not grant permission to redistribute Aseprite itself.
- Aseprite 1.3.18.6-dev version check worked with local XDG configuration; a default config attempt failed on filesystem permissions. No new installation or license acceptance occurred.
- Blender 4.3.2 help/version and prior actual armature/projection scripts support the optional local proxy route. A proxy is not automatic mocap, texture synthesis or a naturalness certificate.
- MCP config examples were parsed, not activated. Other operating systems, clients and live API providers were not all tested.

Tool sources and project-scoped templates are in the skill's [tool adapter reference](../skills/pixel-character-animation/references/tool-adapters.md). No third-party code, tutorial media or tool binaries are redistributed here.

## Retained empirical lessons

The prior character experiment supplied real failure cases: source fragments contaminating head crops, far-sleeve depth errors, tail branch jumps, uniform perceived rhythm despite nonlinear easing, and one-pixel cleanup detaching cloth. Preserve those targeted checks without hardcoding that character's anatomy.

The prior double-projectile forward test exposed cropped-GIF playback streaks despite successful decoding. The exporter therefore uses full-canvas descriptors and independent decoder checks, but still requires actual player review. Its success for one character is not a general new-character benchmark.
