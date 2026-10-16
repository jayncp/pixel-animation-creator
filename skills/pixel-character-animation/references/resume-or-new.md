# Resume a character or start a new one

## Companion archive contract

The study archive may be extracted next to this skill as `pixel_animation_project/`. Locate its `project_resume.json`; the name of the enclosing directory is not significant. Read fields semantically, tolerate additional fields, and verify every referenced file exists before relying on it.

Suggested profile fields:

- `schema_version`, `project_id`, `character_name`, `status`, `latest_revision`.
- `authoritative_master`: relative image path; inspect it, not only its name.
- `identity_constraints`: actual character features that must remain stable.
- `reference_views`: paths or objects with `path`, `view`, `provenance` (original/inferred/mirrored).
- `final_index`: relative path to the authoritative action/export index.
- `current_working_canvas`, `native_editor`, `resume_entrypoint`, `dependencies`.
- `known_limitations`, `review_evidence`, and changed/user-accepted decisions when known.

Resolve paths from the profile directory. Reject missing/escaping/untrusted references rather than reaching into arbitrary machine paths. Read a script before running it, remap historical paths deliberately, and run into a fresh output directory. A prior “final” or self-rating is evidence about that revision, not proof of current visual quality or user acceptance.

For the companion study specifically, the latest revision may improve edges without changing the motion. Check the final index and its QA notes before inheriting older naturalness claims. Do not resurrect deleted history or treat stale historical instructions as current requirements.

## Existing character

1. Inspect master, final view sheet, current action GIF, layered/native source, and known limitations.
2. Build a short constraint sheet from the actual visuals. If metadata contradicts the image, surface the discrepancy rather than silently redesigning the character.
3. Keep rig/layer coordinate conventions unless they cause the defect. Align imported replacement cels to the existing roots and anchors.
4. For edge-only repair, freeze action timing, pose trajectories, and unaffected layers. Save a difference mask and inspect all modified regions. If geometry must change, identify that separately rather than claiming edge-only work.
5. Export and validate against the repaired native/source state, not a similarly named old candidate.

## New character

Use the supplied reference, not the companion character's images. Extract identity before choosing an action or rig. Avoid inheriting a study's species, sex, clothing, appendage count, dimensions, palette size, or frame count.

Establish a front or reference-matching master, a 256×256 canvas for a new unspecified project (user dimensions override; preserve existing project dimensions), ground plane, pivot/foot anchors, and a purposeful palette. For a complete new reference set without specified angles, use front, three-quarter, side and back; for a continuation or subset request, add only the needed missing angles. Inspect full-body views plus face/footwear close-ups. Confirm that opposite views do not quietly change shoe straps, iris color, hair ornaments, hem length, or limb proportions.

If the source is a high-resolution painting, first make a deliberate pixel design rather than nearest-neighbor shrinking a noisy raster and calling it finished. If using image generation, use source-guided generation with tools and permissions available in the current environment; inspect and refine the results. Do not hallucinate successful generation, seed control, or native edits.

Save a new profile and identity sheet in the output project. Use the study's code only when its assumptions actually match, otherwise build an action-specific rig or draw new cels. Code that reproduces the old character is not a generic new-character renderer.

## New action

Choose a distinctive action accent and support strategy. Reuse the master and compatible source parts, not an old motion curve wholesale. Plan transitions through any new view, clothing compression, and appendage occlusion before full texturing. One well-reviewed action is preferable to a suite of mechanically retimed copies when the request is singular.
