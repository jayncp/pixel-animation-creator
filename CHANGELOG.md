# Changelog

## 2.4.0 — 2026-10-21

From a fourth field test: the same rogue charges, throws a spinning dagger, blinks to it, catches it and slams down. The owner changed it mid-test to a forward-up throw and a vertical slam.

- Audit: optional `identity_colors` counts small identity markers per frame and warns where one falls below half its peak; declared `design_gaps` that lie in no enclosed region are reported as stale.
- Motion:
  - contacts are confirmed on rendered pixels and read as the intended kind, with rig shortfalls reported;
  - paths that effects will follow are drawn as lines while blocking;
  - a thrown object leaves along the hand's velocity, not the arm;
  - each effect's cause is recorded and measured against the rendered part, and every effect stays visible in the composite;
  - secondary-motion variants read as the same part and are ordered as a decay, without A/B/A flicker.
- Checks: identity-color counts plus what each held prop touches, recounted after every fix; each revision is diffed against the previous one before review.
- Research: official ability and move videos as a source.
- Delivery: an object that leaves the character gets its own layer, with a held-plus-in-flight count per frame.

## 2.3.1 — 2026-10-20

From the owner's review after the third field test. Guidance only; scripts and tests are unchanged.

- Motion: every effect starts at the time and place of the event that causes it and moves with, or stays behind, the part that drives it; pronounced momentum shows in the loose parts the design already has (trail, lift or compress, overshoot, settle), with drawn variants for a fixed-part rig and no added parts.
- Checks: the motion review covers secondary parts answering the body's momentum and effects tied to their causing event.

## 2.3.0 — 2026-10-20

From a third field test (the same rogue continued from accepted views → a side-view dual-dagger charge, dash and cross slash with sword-qi, game-skill style) and the user's review of its effects. Guidance only; scripts and tests are unchanged.

- Motion: effects that follow a part (smears, trails, slash marks left in the air) are drawn from the part's tip path sampled in world coordinates, body travel included, widening toward the swing pivot; a thrust sweeps almost no smear; when real paths cannot make the wanted shape, the motion changes, not the effect's position; researched poses and prop placements are provisional like the researched view; a stylized-skill note (exaggeration through pose, holds, travel and effects; opaque afterimages and rimmed pale effects under binary alpha).
- Research: live action only when weight or contact is in question; a switch rule for sites that block automated fetching.
- Views: an action may settle a fact the source leaves uncertain, labeled and kept consistent.
- Checks: every held prop readable in each accent frame, or its occlusion unmisreadable, in the author's own frame review; own check scripts measure rendered, visible pixels; composite-only enclosures classified as effect-made.
- Delivery: effects layered by depth with the stacking order; in-place frames with a root table and/or a wide canvas for a travelling action, with the effects' coordinate space; separately upscaled layers stacked into the composite, hidden lower-layer pixels cleared and single-pixel seams sealed.

## 2.2.0 — 2026-10-20

From a second field test (96×96 pixel character drawn in a foreshortened mid-air pose → neutral base and views → side-view dagger throw). Guidance only; scripts and tests are unchanged.

- Views: a foreshortened action-pose source stays the identity master while the neutral base is a labeled inference; view scope for a single source plus one action; one saved set of joint heights as the cross-view authority; guide-to-grid mapping by hue class, with spill removal and outlines re-derived from material boundaries; facial features and hair rebuilt in each view's projection and reviewed for how they read there.
- Motion: a researched camera view stays provisional until the accent poses keep the face and held props readable; a default research size; rotated parts instead of shear for large torso leans; one contour where separately outlined same-material parts touch at the same depth.
- Checks: holes at both logical and export size after Scale2x; every fix confirmed on the composited export; reviewers are told what changed since the last round and judge discrete facts as they read at 1×; character and composite audited separately; `design_gaps` use frame-image coordinates; `edge-diff` after geometry edits; review rounds counted per change request; evenly spaced interior lines treated as banding.
- Delivery: fixed-legend text maps as an editable fallback without a native editor; archive copies written once.

## 2.1.0 — 2026-10-19

From a field test (96×96 pixel character → 256 views → spell-cast animation) and the owner's review; streamlined after a survey of comparable image/sprite skills.

- Fix path containment when a library caller passes an unresolved manifest root (two tests failed on macOS).
- `audit` reports each frame's enclosed transparent regions; frames may declare intentional `design_gaps`.
- `edge-diff` pairs frames by time interval, so inserted or retimed frames can be compared, and reports new holes.
- Rules: check discrete identity facts (counts, sides, presence) per view; a fresh independent reviewer before a candidate, at most three rounds; honest playback wording for still-only agents; cut-out underpaint and overlapping joints; effect timing independent of body holds; near/far side logging; guide-to-grid conversion and noninteger size routes.
- Codex adapter: app-bundled CLI discovery and the field-tested command shape.
- Publishing: MIT license (repository root and skill folder), Claude Code marketplace entry, install commands in the README, `license`/`compatibility`/`metadata.version` frontmatter.
- Removed mechanisms that no publishing convention uses or that duplicated other records: per-file hash manifests and their refresh script, the release-ZIP packager, the `project_stage.py` stage/evidence helper with its spec reference, example and tests (projects keep `START_HERE.md`, `project_resume.json` and a final index), `TEST_RESULTS.md` and `requirements-tested.txt`. The Chinese guide moved into the README; `validate_repo.py` now checks only frontmatter, local links and JSON.

## 2.0.0 — 2026-10-16

- Reposition as end-to-end pixel-character design and animation from text, ordinary images, pixel references or any existing stage.
- Default new reference canvases to 256×256; retain explicit user sizes and existing-project dimensions.
- Add multi-view design/identity, style-aware pixel standards and researched proportion-aware motion planning.
- Preserve variable timing, selective in-betweens, temporal edge cleanup, every-authored-frame review and actual playback gates.
- Add portable project-stage specifications, evidence-aware routing and local-only tool configuration templates.
- Clarify actual built-in/Codex/API capabilities, costs/permissions, native-editor and playback limits.
- Package as a real Git repository with research rationale, tests, evaluation scenarios and maintenance/release guidance.

## Imported v7 baseline

The initial commit preserves the previously delivered reference-led animation skill and its export/QA tools. This is an import commit, not a reconstruction of all earlier animation experiment history. Character-specific assets remain in their companion project archive.
