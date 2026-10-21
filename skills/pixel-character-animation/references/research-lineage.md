# Craft and workflow lineage

Research refreshed 2026-10-16. Sources guide decisions; they do not replace inspection of a particular character or action. Detailed adopt/reject rationale and limits are in the repository's `docs/RESEARCH.md`; this reference remains usable when the skill folder is copied alone.

## Pixel art

- [Cure, Pixel Art Tutorial](https://pixeljoint.com/forum/forum_posts.asp?TID=11299): purposeful palettes, clusters, banding. No universal palette count; intentional isolated detail can be valid.
- [Saint11, Cluster Sketching](https://saint11.art/pixel_art_articles/article2/): mass-first construction and deliberate edge steps.
- [Saint11, Anti-Alias and Banding](https://saint11.art/pixel_art_articles/article5/): style-aware manual AA, not general blur or automatic contour bands.
- [SLYNYRD, Human Anatomy](https://www.slynyrd.com/blog/2019/5/21/pixelblog-17-human-anatomy) and [Realistic Anatomy](https://www.slynyrd.com/blog/2024/3/25/pixelblog-49-realistic-human-anatomy): gesture/wireframe/masses and cross-view landmarks. Do not hardcode their six/eight-head examples.

## Animation

- [Saint11, A Basic Aseprite Animation](https://saint11.art/pixel_art_articles/article3/): key poses, timing/spacing and editable-source practices.
- [Animation Mentor, Timing and Spacing](https://www.animationmentor.com/blog/tutorial-animate-with-timing-and-spacing-in-mind/), [Anticipation](https://www.animationmentor.com/blog/anticipation-the-12-basic-principles-of-animation/), [Overlap](https://www.animationmentor.com/blog/follow-through-and-overlapping-action-the-12-basic-principles-of-animation/): readable causality, phase relationships, weighted timing, not universal phase ratios.
- [Animation Mentor, Character Size](https://www.animationmentor.com/blog/tutorial-animating-big-and-small-characters/): adapt reach/clearance and motion to target proportions rather than copy a realistic skeleton.
- Earlier study sources: [SLYNYRD intro to animation](https://www.slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation), [melee attacks](https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks), [top-down characters](https://www.slynyrd.com/blog/2025/3/24/pixelblog-55-top-down-character-animation). Exercise-specific counts/timings are not defaults.

## Skill structure

Public [OpenAI imagegen](https://github.com/openai/skills/blob/main/skills/.system/imagegen/SKILL.md), [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md), [Remotion best-practices](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/SKILL.md), and [Anthropic skills](https://github.com/anthropics/skills) informed conditional references, spec/provenance separation, reusable deterministic helpers and isolated realistic evaluations. Do not transplant their product-specific dimensions, renderers or generic GIF effects into pixel-character requirements.

## Evidence boundaries

Research text was inspected; not all tutorial media was accessible for visual playback. New actions need their own actual reference observation. Prior character repairs and GIF interoperability failures inform tests but do not prove universal art quality. The skill specifies an iterative method, not a guaranteed outcome. Do not ship third-party media or software merely because sources are linked.
