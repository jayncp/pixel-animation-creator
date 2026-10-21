# Maintenance and release

## Layout and responsibilities

Keep `SKILL.md` as a concise routing/decision entrypoint. Put conditional craft and backend details in references; reusable deterministic behavior in scripts; concrete output specs in assets. Keep research and release discussion here, not in the runtime prompt. Do not copy third-party skill source or media into the repository merely to support a citation.

A change in model/API options belongs in the tool adapter, not the character identity schema. A recurring artistic failure needs a targeted craft rule and a realistic behavioral case, not an arbitrary new global threshold. A technical bug needs a regression test reproducing its behavior.

## Editing and testing

1. Create a local branch; describe the request and affected stage. Preserve unrelated user edits.
2. Update the canonical reference once and link to it rather than repeat it in every file.
3. Run all Python tests and `scripts/validate_repo.py`. Test path relocation, no-overwrite, missing capabilities and artifact corruption, not just a happy path.
4. Run relevant `evals/scenarios.json` cases in a clean context with minimal raw inputs. Keep generated projects outside the skill tree. Label planning tests, actual generation, image inspection and real playback separately.
5. An agent review is not user acceptance. Report missing environment/permissions as blocked. Never label a scenario executed just because its prompt exists.
6. Record exact commands/runtime versions/results and remaining limits in `docs/VALIDATION.md`. Do not expose tokens, signed URLs, private notes or system prompts.
7. Update the changelog and the `metadata.version` in `SKILL.md` together. Do not commit credentials, local configs, virtual environments, caches, downloaded binaries or evaluation media from third parties.

## Dependency and adapter policy

Python runtime dependencies are declared in the skill's requirements file. Aseprite, its community MCP server and Blender are optional external tools, not bundled. Verify source/version/license before setup. Use project-local environments/configuration; never make a global installation an implicit side effect. Capability detection is read-only; a live model invocation may consume usage and is not a free probe.

## Release

The source is published at https://github.com/jayncp/pixel-animation-creator; Git commits provide integrity, so no hash manifests are kept. For a release: tests and `scripts/validate_repo.py` pass, `claude plugin validate .` passes when the Claude Code CLI is available, the changelog and `metadata.version` agree, then tag `vX.Y.Z` on main. Installers copy only `skills/pixel-character-animation/`, which therefore carries its own `LICENSE.txt` and `requirements.txt`. For a Claude.ai upload, zip that folder: `cd skills && zip -r pixel-character-animation.zip pixel-character-animation`.

The first three commits use a local non-personal author label; later commits use the maintainer's own Git identity.

## Coverage boundaries

Unit tests validate deterministic helpers, not artistic quality. A real reference-generation smoke test covers only its actual subject/style/provider. Passing one existing-character action cannot establish universal new-character or new-action reliability. Keep challenging motion, camera and proportion examples in the evaluation backlog rather than claim unsupported generalization. Field tests through 3.0.0 cover one front-view spell cast and a series of side-view dagger skills, mostly melee, on one character; ranged skills are next.
