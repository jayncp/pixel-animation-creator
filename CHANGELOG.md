# Changelog

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
