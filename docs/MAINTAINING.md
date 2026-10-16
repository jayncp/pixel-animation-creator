# Maintenance and release

## Layout and responsibilities

Keep `SKILL.md` as a concise routing/decision entrypoint. Put conditional craft and backend details in references; reusable deterministic behavior in scripts; concrete output specs in assets. Keep research and release discussion here, not in the runtime prompt. Do not copy third-party skill source or media into the repository merely to support a citation.

A change in model/API options belongs in the tool adapter, not the character identity schema. A recurring artistic failure needs a targeted craft rule and a realistic behavioral case, not an arbitrary new global threshold. A technical bug needs a regression test reproducing its behavior.

## Editing and testing

1. Create a local branch; describe the request and affected stage. Preserve unrelated user edits.
2. Update the canonical reference once and link to it rather than repeat it in every file.
3. Run all Python tests and `scripts/validate_repo.py`. Test path relocation, no-overwrite, modified evidence, missing capabilities and artifact corruption, not just a happy path.
4. Run relevant `evals/scenarios.json` cases in a clean context with minimal raw inputs. Keep generated projects outside the skill tree. Label planning tests, actual generation, image inspection and real playback separately.
5. An agent review is not user acceptance. Report missing environment/permissions as blocked. Never label a scenario executed just because its prompt exists.
6. Record exact commands/runtime versions/results and remaining limits in `docs/VALIDATION.md`. Do not expose tokens, signed URLs, private notes or system prompts.
7. Update changelog and run `python scripts/refresh_manifest.py`; commit source, docs and both manifests. Do not commit credentials, local configs, virtual environments, caches, downloaded binaries or evaluation media from third parties.

## Dependency and adapter policy

Python runtime dependencies are declared in the skill's requirements file. Aseprite, its community MCP server and Blender are optional external tools, not bundled. Verify source/version/license before setup. Use project-local environments/configuration; never make a global installation an implicit side effect. Capability detection is read-only; a live model invocation may consume usage and is not a free probe.

## Release ZIP with Git history

Run `python scripts/package_repo.py /absolute/path/to/release.zip` from this repository after committing. The packager requires a clean tracked tree, validates the repository, and includes tracked files plus only safe portable Git metadata/objects. It does not copy hooks, remotes, credentials, worktree pointers, local runtime data or ignored files. It creates a real Git repository snapshot preserving commit history, not a ZIP pretending to be one.

Extract into a new directory. Run `git status --short`, `git log --oneline`, `git fsck --full`, all tests and repository validation. Verify the ZIP entry names contain no absolute or parent traversal paths and record its SHA-256. Keep ZIP/hash outside the tracked tree to avoid self-referential manifests.

ZIP preserves necessary Git object bytes; platform extraction behavior can vary. Use an archiver that extracts hidden `.git` entries. The release's Git identity is a local non-personal author label; no remote repository is configured or published.

## Coverage boundaries

Unit tests validate deterministic helpers, not artistic quality. A real reference-generation smoke test covers only its actual subject/style/provider. Passing one existing-character action cannot establish universal new-character or new-action reliability. Keep challenging motion, camera and proportion examples in the evaluation backlog rather than claim unsupported generalization.
