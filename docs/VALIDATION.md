# Validation records

## 3.0.1 — 2026-10-22

No field test. The changes come from a research pass (owner's sources, three web tracks, five experiments on the 3.0.0 field-test rogue, kept outside this repository) and the owner's definition of grid, canvas and export scale. The owner kept Scale2x as the default export enlargement, with nearest neighbor when a direct export is asked, and asked for a README section on defaults and choices.

**Evidence behind the rules.** A recolor-only outline pass fixed a rotated boot's doubled staircase with the silhouette unchanged. Recovering a generated guide's grid worked; reducing it to the target size broke outlines, eyes and the three thigh knives and turned green spill into brown specks, and protected-role voting beat a plain majority on orphan pixels. A port of MMPX matched the delivered Scale2x output exactly on its EPX path; Scale2x rounded the 3×4 fist and blade tips, MMPX kept them, both palette-exact with binary alpha and no new holes on 21 frames.

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0, ImageMagick 7.1.2.

**Checks.** 24 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed (Claude Code 2.1.296). A fresh subagent reviewed the changed text; its findings were applied: old size wording in unchanged files, the CLI's gap coordinates, sizes that are not a multiple of the grid, effect edges against the outline strategy, the recolor pass's limits and numbers inside rules.

**Limits.** Documentation only; no helper changed. The new rules have not been rerun as fresh-context evaluations, and the experiments cover one character.

## 3.0.0 — 2026-10-21

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0, ImageMagick 7.1.2.

**Field test.** Two agents used 2.4.0 in parallel from the same read-only seed (identity, side view, char-map parts, earlier scripts) on one task: a sprint-start charge, two grey afterimages split off, the body and then each afterimage dash through one point, then the body recovers and the afterimages vanish, in a game-skill style.

| Side | Agent | Result | Time | Review rounds (blocking faults) |
| --- | --- | --- | --- | --- |
| a | Claude Code, one agent with subagent reviewers | 21 frames, 1660 ms, 368×128 logical | about 2 h | 3 → 1 → 0 |
| b | ChatGPT Work cloud multi-agent | 29 frames, 2200 ms, 448×160 logical | about 43 min | an early review of the blocked poses, then 2 → 0 → an 8-pixel spot-check, all by one reviewer |

Both sides: no image generation, actual inspection of every frame, and no continuous playback (still-only agents; b's browser failed to start). Both researched with official ability videos. The projects live outside this repository. No user acceptance is claimed. The owner judged b's result about right and left both sides' non-blocking details unfixed.

**2.4.0 changes.** Merged verdicts from both sides:

| Change | Verdict | Notes |
| --- | --- | --- |
| Identity-color counts | Worked | They cannot see adjacency, and a marker absent from every frame went unwarned. |
| Stale-gap warnings | Worked | Shown on b's fixture. |
| Rendered-pixel contacts | Worked in part | A zero-error solver still left a sole 1 px above the ground. Afterimages first reached the point only with a blade tip. |
| Effect-path lines | Worked in part | They covered tips only. b drew them alongside the first effects, not before. |
| Effect causes measured on rendered pixels | Necessary, not sufficient | Both sides' worst effect faults passed them. |
| Variant ordering, revision diffs, official ability videos | Worked | |
| Thrown-object layering | Not exercised | |

**Gaps found.**

- Afterimages. Both sides independently made the same thing: value-mapped grey copies with props in the same hands. The skill had suggested flat silhouettes.
- Effect faults that cause-and-visibility checks passed:
  - a: back-layer slivers through gaps in the body read as a ribbon;
  - b: a front flash covered an afterimage's face and hand.
- Held props. On side a, daggers read as held by the wrong hand in transition frames over two review rounds. The adjacency rule sat under "accent frames".
- Early review. b's review of the blocked poses caught a dagger read as guarding the face. a found the same fault only after effects were added.
- Review rounds. b's reviewer, reused across rounds, rechecked only its own findings.
- Revision diffs after a canvas shift showed every pixel as changed.
- Frame dumps of whole videos took 1.4 GB.

**Changes.**

- The owner set looping GIFs as the default; `seam: "cut"` keeps a travelling one-shot's restart out of motion diagnostics.
- The other findings were merged into existing rules, each as a problem class with at most one example.
- Choices the brief left open stay open: whether the target mark persists, how afterimages dissolve, how strong the effects are.
- One scenario was added.
- A fresh subagent then reviewed the whole skill. Fixed:
  - contradictions, e.g. the reviewer gate was named "candidate" both with and without a reviewer;
  - rules repeated between SKILL.md and the references;
  - over-specific wording;
  - missing-space typos in older records.

**Checks.** 24 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** One character. This closes the dagger-skill series, mostly melee; ranged skills come next. The new rules have not been rerun as fresh-context evaluations.

---

## 2.4.0 — 2026-10-21

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0.

**Field test.** An agent used 2.3.1 to continue the same rogue (files copied from the earlier projects, which stayed read-only) into a side-view charge, spinning dagger throw, blink to the dagger with a catch, and a slam that stabs it into the ground, in a game-skill style. After six revisions the owner asked for a forward-up throw and a vertical slam, and the review count restarted. The candidate is 26 frames and 1790 ms on a 480×496 world canvas, with character, flying-dagger, behind-character and in-front effect layers, an in-place character export and a root-motion table. Labels: no image generation, actual inspection of every frame, no continuous playback (still-only agent), subagent research (4 frame-stepped sources, about 20 minutes) and five independent subagent review rounds (2, 1, 1, 1, 0 blocking). The project lives outside this repository. No user acceptance is claimed.

**2.3.1 rules.**
- Effects tied to their cause: worked, and found the most defects once each cause was written as data and measured on rendered pixels.
- Secondary parts following momentum: worked only in part. Variants were assigned per frame, but drawn variants read as a hat or as horns, and small moves switched variants back and forth.

**Gaps found.** Occlusion misreads passed the author's frame review again (the 2.2.0 and 2.3.0 rule): a raised arm covered the eye, and three of the five blocking faults were regressions introduced by fixes. In one, the blue gem's pixel count was fine, but the dagger lay against the other wrist and read as one hand holding two. The two-bone IK clamped an unreachable stab target without warning, leaving the blade 5 px above the ground its cracks were drawn on. A throw released with the arm pointing along the flight left the swing smear hooking backward. A spin smear was erased whole by the rule that clears effects off the body. Twice a failed edit step still ran the build, producing a revision equal to the old one or half edited. Declared `design_gaps` went stale after pose changes without a warning.

**Changes.**
- The new `audit` options (see CHANGELOG), checked on the field project's real frames:
  - Identity-color counts flagged the covered eye of the first reviewed revision (lash 28 → 7–11 px in three frames). On the candidate they flagged only the blink frames, where the body is hidden by design.
  - The stale-gap check found one stale point in the candidate (frame 15) that the author's manual recheck had missed.
- The other findings were merged into existing rules, each with at most one example, and one scenario was added.

**Checks.** 23 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** One more character and action; the new rules have not been rerun as fresh-context evaluations. Identity-color counts flag covered markers, not misleading adjacency.

---

## 2.3.1 — 2026-10-20

**Source.** The owner asked whether the skill stresses effect–motion consistency and asked for secondary parts to follow pronounced momentum. 2.3.0 tied part-following effects to sampled paths and projectiles to their release, but had no general rule tying every effect to its causing event, and covered hair and cloth only in passing (idle, sleeves, turns, long appendages). In the third field test the first review round found hair back in its rest shape while the body still dashed. Two short rules and one review item were added; one scenario gained two checks.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** Not yet exercised in a field test; the next test is asked to report whether these rules worked.

---

## 2.3.0 — 2026-10-20

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0.

**Field test.** An agent used 2.2.0 to continue the 2.2.0 test's rogue (accepted side view and identity sheet copied in, the earlier project left read-only) into a side-view dual-dagger charge, dash and cross slash with sword-qi in a game-skill style: a 15-frame, 1560 ms animation on a 640×256 world canvas, with character, behind-character and in-front effect layers, an in-place character export and a root-motion table. Labels: no image generation, actual inspection of every frame, no continuous playback (still-only agent), subagent research (3 frame-stepped sources, about 60 minutes) and independent subagent review. The project lives outside this repository. No user acceptance is claimed.

**Gaps found.** The researched charge pose hid one dagger behind both thighs; blocking caught it there, but the same occlusion in the dash frames passed the author's frame review and was first flagged by the reviewer, the bare blade read as a fourth holster knife. A slash fragment left behind the head read as a horn. Scale2x of the flattened composite differed from the stacked layers by up to 46 px per frame, and it exposed effect pixels hidden under the character as specks. Afterimages and slashes crossing the body enclosed space in most composite frames. Three review rounds passed the candidate; the user then saw that the smears and sword-qi did not follow the blades: smears drawn around the current shoulder ended 34–38 px from the previous tip, and the X was a fixed shape off the real paths by up to 47 px. Rebuilt from sampled tip paths, sequential cuts during the dash could not cross as an X, so the cut became a scissor cut; a far-blade smear then vanished because its tip moved along the blade; and the author's first matching check compared the generator's data with itself. Three more review rounds (1, 0, 0 blocking) closed these.

**Changes.** General rules merged into existing references (see CHANGELOG), mostly extending 2.2.0 rules that worked only in part (the provisional researched view, the reviewer's occlusion check, research size, confirming fixes on the rendered result); one scenario added. No script change: `audit`, `export` and `verify-gif` agreed with the agent's own checks.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** One character and one action more; the new rules have not been rerun as fresh-context evaluations.

---

## 2.2.0 — 2026-10-20

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0.

**Field test.** An agent used 2.1.0 end to end on a user-supplied 96×96 rogue drawn in a foreshortened mid-air pose: identity sheet of 15 discrete facts, original-pose master, neutral front, three-quarter and side views at 256×256 (128 logical + Scale2x), motion research, and a 16-frame, 1680 ms side-view overhand dagger throw with the knife on a separate effect layer. Labels: actual generation (one Codex CLI 0.162.0-alpha call through the app-bundled CLI), actual inspection of every view and frame, no continuous playback (still-only agent), three independent subagent review rounds each for views and animation. The project lives outside this repository. No user acceptance is claimed.

**Gaps found.** The skill gave no route from an action-pose source to a neutral base, and its view-scope rules did not cover a single source plus one action. The researched three-quarter view failed at blocking: the near arm crossed the face at release. The generated guide drew two of three thigh knives in every view, which the 2.1.0 per-view count rule caught before conversion; its finer pixel pitch and green spill scattered outlines and mapped greys to a brown material. Shear deformed large torso leans. Scale2x closed one-pixel holes at diagonal blade tips and parallel trail lines. Effect gaps were reported with character holes in the composite. Independent rounds found nine blocking faults the author missed, two of them regressions introduced by fixes; one recorded fix was hidden in the composite by draw order until the third view round. Research took about 44 minutes for 12 sources.

**Changes.** Short general rules merged into the existing references (see CHANGELOG), each with at most one example; one behavioral scenario added. No script change: `audit`, `export`, `verify-gif` and `edge-diff` agreed with the agent's own independent checks.

**Revision round.** The user then reviewed the candidate and named three faults: an unnatural profile eye, the side hair, and a thick tan band behind the arm in early frames. The front eye's lash bar had been moved onto the profile unchanged, so every identity fact still matched; the hair used six evenly spaced parallel strand lines; the arm and torso each kept their own skin outline, which lay side by side and became a 4 px band after Scale2x (40 all-outline 2×2 blocks in the logical frames). Three more revisions, each with a fresh review round, cut the blocks to 3 point junctions with 0 blocking faults. A mis-aimed shell copy overwrote one view archive; it was recovered by deterministic re-rendering checked against a saved comparison. Five more rules (see CHANGELOG) and two scenario checks came from this round.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** The new rules come from one more character and one more action and have not been rerun as fresh-context evaluations.

---

## 2.1.0 — 2026-10-19

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0, ImageMagick 7.1.2.

**Field test.** An agent used 2.0.0 end to end on a user-supplied 96×96 three-tailed character: 256×256 front/three-quarter/side/back views, motion research, and an 18-frame, 1500 ms front-view spell cast. Labels: actual generation (three Codex CLI 0.162.0-alpha calls through the app-bundled CLI, about 65 s each, RGB output at model-chosen sizes, files written under the Codex home and copied in), actual inspection of every view and frame, sampled browser playback matched to frames, and independent subagent review rounds. The project lives outside this repository. No user acceptance is claimed.

**Gaps found.** Two macOS test failures (unresolved library root). Technical checks passed while frames had visible holes and a neck tear at layer junctions. The author's own review missed most defects that independent rounds found; views had no independent review, and the owner later found a back view with two of the three tails although the generation brief demanded three. Cut-out parts lacked hidden underpaint; a projectile froze during body holds; generated guides had grid, color, proportion and identity-fact errors when brought onto the grid; near/far sides were confused once; `edge-diff` refused a revision with an inserted frame.

**Changes.** The root fix, the enclosed-hole report and time-aligned `edge-diff` (see CHANGELOG), plus short general rules in the references. A first draft also added a playback-capture matcher, a timing summary and long incident-specific guidance; after a survey of comparable skills (Anthropic skill-authoring guidance and visual skills, OpenAI imagegen and hatch-pet, community sprite pipelines) those were dropped: the GIF decode check already proves pixels and timing, continuous viewing is left to the user, and each finding is stated once as a general rule with at most one example.

**Packaging.** A survey of publishing conventions (Agent Skills specification and its reference validator, anthropics/skills, Claude Code plugin marketplaces, Codex skills, the `npx skills` installer) found no use of publisher hash manifests, release ZIPs with Git history or repository validation beyond frontmatter. Those were removed; integrity comes from Git. The stage/evidence helper was also removed: in the field test it required a 314-line generator script and a 554-line record that duplicated the 40-line `START_HERE.md`, the final index and `project_resume.json`, and it caught no defect.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed (Claude Code 2.1.296). On the field project's real frames (18 × 384×256), `audit` listed only the source's intentional gaps in under 1 s, and `edge-diff` paired a 17-frame and an 18-frame revision by time.

**Limits.** The rules come from one character and one action and have not been rerun as fresh-context evaluations; two scenarios were added to `evals/scenarios.json` for that. The hole report is a diagnostic, not an art judgment. The live Codex result applies to that account, version and host only.

---

# Validation record — 2.0.0

Historical. The stage helper, release packager and hash manifests described here were removed in 2.1.0.

Final source validation completed 2026-10-16. Artistic and technical outcomes are deliberately separate.

## Environment and baseline

Python 3.12.14; Pillow 12.3.0. Declared support is Python 3.10+ and Pillow 10–12, not a claim that every minor version or OS was exercised. Existing exporter regression tests were retained. No new software, external paid provider, login or global configuration was required.

## Real prior-project regression

The current helper audited and re-exported actual V7 idle native-output PNGs: 30 authored frames, 3000 ms, 256×256. The new GIF retained all 30 exposures with full-canvas descriptors and exact visible RGBA by all 30 intervals; sprite-sheet RGBA was exact. New GIF SHA-256: 67fd8582f65b1db33588f88214bfcd47e2f581bb983cf2bb041b33b93e08bee3. This is a technical regression, not a new naturalness assessment or new playback claim.

## Independent review findings retained

An initial independent routing review found: old 128×128 legacy size defaulted to 256; passed artifact records ignored stale hashes; imported candidates awaiting review routed back to intake; Boolean schema_version passed as 1. These are documented failures, not hidden by later successful tests. All four were fixed and independently rerun: 128 size preserved; stale/missing completed hashes rejected; imported pending reviews stay at their own stage; Boolean schema rejected. An additional independent probe confirmed a changed declared input hash blocks ready delivery even with unchanged outputs. Checks cover declared hashes/snapshots, not undeclared semantic dependencies or the truth of visual judgments.

## Scope limitations

No claim of general one-shot quality, universal multi-view consistency, automatic motion capture, physics certification, or full provider/client/OS compatibility. Tutorial text research did not constitute new playback of all linked videos. Configuration templates were parsed, not installed. No API/CLI image-generation fallback was live-tested. Actual bounded image generation is listed separately from discovery/dry-run.

## Final checks

- 40 Python tests passed: 19 retained image/export tests and 21 stage-routing tests. ImageMagick independent decoder test ran successfully; none skipped in this environment.
- Skill frontmatter/name validator passed; repository local-link/JSON checks passed.
- Project MCP TOML and client-neutral JSON templates parsed. They remain inactive and contain placeholders.
- Real V7 idle regression passed as described above.
- Fresh-context text-to-reference smoke test partially succeeded, with final pixel-quality gate **blocked**, not passed. See [actual result and candidate](../evals/results/text-reference/RESULT.md). Two built-in generations produced recognizable identity but not a finished clean pixel master; dimensions/alpha/palette were actually measured and images reviewed.
- New-source/any-stage helper behaviors were tested independently; the rest of the [scenario matrix](../evals/scenarios.json) is a reusable evaluation plan, not a claim of ten completed artistic tasks.

## Release restoration procedure

The release is built from a clean commit and independently extracted into a new directory. Acceptance commands: git status --short (empty), git fsck --full, git log --oneline (import + revision history), all 40 tests and scripts/validate_repo.py. The packager does not include remotes, hooks, credentials or ignored runtime directories. File hashes are in CONTENT_MANIFEST.sha256; archive SHA is recorded with the delivered release, outside its contents.

Release restoration is checked after packaging; if a step fails the archive is not delivered as verified. No cross-platform or live-provider equivalence is implied.
