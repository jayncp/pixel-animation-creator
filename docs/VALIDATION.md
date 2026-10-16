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
