# Validation records

## 2.2.0 — 2026-10-20

Environment: macOS 26.0.1 arm64, Python 3.12.12 in a project-local uv venv outside this repository, Pillow 12.3.0.

**Field test.** An agent used 2.1.0 end to end on a user-supplied 96×96 rogue drawn in a foreshortened mid-air pose: identity sheet of 15 discrete facts, original-pose master, neutral front, three-quarter and side views at 256×256 (128 logical + Scale2x), motion research, and a 16-frame, 1680 ms side-view overhand dagger throw with the knife on a separate effect layer. Labels: actual generation (one Codex CLI 0.162.0-alpha call through the app-bundled CLI), actual inspection of every view and frame, no continuous playback (still-only agent), three independent subagent review rounds each for views and animation. The project lives outside this repository. No user acceptance is claimed.

**Gaps found.** The skill gave no route from an action-pose source to a neutral base, and its view-scope rules did not cover a single source plus one action. The researched three-quarter view failed at blocking: the near arm crossed the face at release. The generated guide drew two of three thigh knives in every view, which the 2.1.0 per-view count rule caught before conversion; its finer pixel pitch and green spill scattered outlines and mapped greys to a brown material. Shear deformed large torso leans. Scale2x closed one-pixel holes at diagonal blade tips and parallel trail lines. Effect gaps were reported with character holes in the composite. Independent rounds found nine blocking faults the author missed, two of them regressions introduced by fixes; one recorded fix was hidden in the composite by draw order until the third view round. Research took about 44 minutes for 12 sources.

**Changes.** Short general rules merged into the existing references (see CHANGELOG), each with at most one example; one behavioral scenario added. No script change: `audit`, `export`, `verify-gif` and `edge-diff` agreed with the agent's own independent checks.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed.

**Limits.** The new rules come from one more character and one more action and have not been rerun as fresh-context evaluations.

---

## 2.1.0 — 2026-10-19

Environment: macOS 26.0.1 arm64, Python3.12.12 in a project-local uv venv outside this repository, Pillow12.3.0, ImageMagick7.1.2.

**Field test.** An agent used 2.0.0 end to end on a user-supplied 96×96 three-tailed character: 256×256 front/three-quarter/side/back views, motion research, and an 18-frame, 1500 ms front-view spell cast. Labels: actual generation (three Codex CLI 0.162.0-alpha calls through the app-bundled CLI, about 65 s each, RGB output at model-chosen sizes, files written under the Codex home and copied in), actual inspection of every view and frame, sampled browser playback matched to frames, and independent subagent review rounds. The project lives outside this repository. No user acceptance is claimed.

**Gaps found.** Two macOS test failures (unresolved library root). Technical checks passed while frames had visible holes and a neck tear at layer junctions. The author's own review missed most defects that independent rounds found; views had no independent review, and the owner later found a back view with two of the three tails although the generation brief demanded three. Cut-out parts lacked hidden underpaint; a projectile froze during body holds; generated guides had grid, color, proportion and identity-fact errors when brought onto the grid; near/far sides were confused once; `edge-diff` refused a revision with an inserted frame.

**Changes.** The root fix, the enclosed-hole report and time-aligned `edge-diff` (see CHANGELOG), plus short general rules in the references. A first draft also added a playback-capture matcher, a timing summary and long incident-specific guidance; after a survey of comparable skills (Anthropic skill-authoring guidance and visual skills, OpenAI imagegen and hatch-pet, community sprite pipelines) those were dropped: the GIF decode check already proves pixels and timing, continuous viewing is left to the user, and each finding is stated once as a general rule with at most one example.

**Packaging.** A survey of publishing conventions (Agent Skills specification and its reference validator, anthropics/skills, Claude Code plugin marketplaces, Codex skills, the `npx skills` installer) found no use of publisher hash manifests, release ZIPs with Git history or repository validation beyond frontmatter. Those were removed; integrity comes from Git. The stage/evidence helper was also removed: in the field test it required a 314-line generator script and a 554-line record that duplicated the 40-line `START_HERE.md`, the final index and `project_resume.json`, and it caught no defect.

**Checks.** 22 Python tests passed, none skipped; `scripts/validate_repo.py` passed; `claude plugin validate .` passed (Claude Code 2.1.296). On the field project's real frames (18 × 384×256), `audit` listed only the source's intentional gaps in under 1 s, and `edge-diff` paired a 17-frame and an 18-frame revision by time.

**Limits.** The rules come from one character and one action and have not been rerun as fresh-context evaluations; two scenarios were added to `evals/scenarios.json` for that. The hole report is a diagnostic, not an art judgment. The live Codex result applies to that account, version and host only.

---

# Validation record — 2.0.0

Final source validation completed2026-10-16. Artistic and technical outcomes are deliberately separate.

## Environment and baseline

Python3.12.14; Pillow12.3.0. Declared support is Python3.10+ and Pillow10–12, not a claim that every minor version or OS was exercised. Existing exporter regression tests were retained. No new software, external paid provider, login or global configuration was required.

## Real prior-project regression

The current helper audited and re-exported actual V7 idle native-output PNGs:30 authored frames,3000ms,256×256. The new GIF retained all30 exposures with full-canvas descriptors and exact visible RGBA by all30 intervals; sprite-sheet RGBA was exact. New GIF SHA-256:67fd8582f65b1db33588f88214bfcd47e2f581bb983cf2bb041b33b93e08bee3. This is a technical regression, not a new naturalness assessment or new playback claim.

## Independent review findings retained

An initial independent routing review found: old128×128 legacy size defaulted to256; passed artifact records ignored stale hashes; imported candidates awaiting review routed back to intake; Boolean schema_version passed as1. These are documented failures, not hidden by later successful tests. All four were fixed and independently rerun:128 size preserved; stale/missing completed hashes rejected; imported pending reviews stay at their own stage; Boolean schema rejected. An additional independent probe confirmed a changed declared input hash blocks ready delivery even with unchanged outputs. Checks cover declared hashes/snapshots, not undeclared semantic dependencies or the truth of visual judgments.

## Scope limitations

No claim of general one-shot quality, universal multi-view consistency, automatic motion capture, physics certification, or full provider/client/OS compatibility. Tutorial text research did not constitute new playback of all linked videos. Configuration templates were parsed, not installed. No API/CLI image-generation fallback was live-tested. Actual bounded image generation is listed separately from discovery/dry-run.

## Final checks

-40 Python tests passed:19 retained image/export tests and21 stage-routing tests. ImageMagick independent decoder test ran successfully; none skipped in this environment.
- Skill frontmatter/name validator passed; repository local-link/JSON checks passed.
- Project MCP TOML and client-neutral JSON templates parsed. They remain inactive and contain placeholders.
- Real V7 idle regression passed as described above.
- Fresh-context text-to-reference smoke test partially succeeded, with final pixel-quality gate **blocked**, not passed. See [actual result and candidate](../evals/results/text-reference/RESULT.md). Two built-in generations produced recognizable identity but not a finished clean pixel master; dimensions/alpha/palette were actually measured and images reviewed.
- New-source/any-stage helper behaviors were tested independently; the rest of the [scenario matrix](../evals/scenarios.json) is a reusable evaluation plan, not a claim of ten completed artistic tasks.

## Release restoration procedure

The release is built from a clean commit and independently extracted into a new directory. Acceptance commands: git status --short (empty), git fsck --full, git log --oneline (import + revision history), all40 tests and scripts/validate_repo.py. The packager does not include remotes, hooks, credentials or ignored runtime directories. File hashes are in CONTENT_MANIFEST.sha256; archive SHA is recorded with the delivered release, outside its contents.

Release restoration is checked after packaging; if a step fails the archive is not delivered as verified. No cross-platform or live-provider equivalence is implied.
