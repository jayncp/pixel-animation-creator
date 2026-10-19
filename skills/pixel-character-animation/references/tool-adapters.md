# Tool routing and project-local adapters

Read only when selecting or configuring tools. Capability checks do not authorize paid calls, uploads, installation, login, or broader access. Keep source assets immutable and write versioned outputs. Follow the host's actual image-editing constraints as well as tool availability. If a needed pixel-finishing route is disallowed, do not substitute another utility to evade that restriction: mark the gate blocked and request the specific permitted route. Availability alone is not authority.

## Image generation

1. Prefer the current host's **available native image-generation tool** for raster character references, views, and pose guides. Inspect its actual schema; tool names/arguments differ by host. Inspect edit inputs, request real alpha when supported, copy selected outputs into the project, and log provenance. Generated guides are not automatically a temporally consistent animation.
2. Honor an explicitly selected provider/model. Confirm its actual image-generation/edit/alpha capabilities, credential readiness, data destination and spending authorization. Never silently substitute a provider/model, upload private references, or ask for secrets in chat.
3. On another agent, detect an existing Codex installation without inference calls: `command -v codex`, `codex --version`, `codex --help`, `codex exec --help`; if `command -v` fails, also check for an app-bundled CLI, and `codex features list` is a read-only feature-flag probe. Installation, login, image-input flags and model names do **not** prove imagegen access or free usage. Do not install Codex just to probe it.
4. Codex orchestration is optional only after the selected session's actual imagegen capability and authorization are established. The shape below generated images in one field test (see repository docs/VALIDATION.md). It may consume usage; do not use it as a free capability probe. Replace placeholders and inspect local help first:

```sh
codex exec --cd "$PROJECT" --sandbox workspace-write --skip-git-repo-check --json \
  --output-last-message "$PROJECT/logs/imagegen-result.txt" -i "$PROJECT/refs/master_preview.png" -- \
  "Use the available native image-generation tool for the approved brief. Copy the selected image byte-for-byte into this project. Do not install, change provider, invoke a paid fallback, or change global config. If imagegen is absent, report unavailable." < /dev/null
```

`-i` attaches a reference image; drop it for text-only briefs. Without `< /dev/null` the command can wait on stdin. Generated files land under the Codex home directory, outside the project, hence the copy; output may be RGB without alpha at a size the model chooses.

No dedicated `codex image generate` command or direct Codex image endpoint was established. Never invent commands, feature toggles, endpoints, or extract authentication tokens. Do not bypass sandbox/approval rules. If no route is verified, ask for a provider or supplied images and continue independent planning/local work.

The **OpenAI API CLI is separate from Codex CLI**. Its current official docs describe `openai images generate`; verify that installed executable's version/help before use. A host-provided imagegen script may instead offer `generate`, `edit`, and `--dry-run`. Reuse the selected adapter rather than assuming every host ships one. Model/API capabilities drift: research found current API docs advertising preview transparency while an installed adapter rejected it. Check the actual adapter/model/version and inspect resulting alpha; do not silently switch models.

Sources: [Codex commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [OpenAI API CLI](https://developers.openai.com/api/docs/libraries/openai-cli).

## Local setup contract

Reuse existing safe executables first. Put approved dependencies in `.venv/` or `tools/`, caches/config/temp in `.local/`, and logs/output in the project. Use explicit executable paths and command-scoped environment variables. Ignore credentials, environment files, caches and virtual environments in version control. Never copy authentication stores, modify shell profiles, use global package installs, register a global MCP, or weaken host trust settings. Obtain required setup permissions first; these files do not grant them.

Example Python isolation: `python -m venv .venv`, then `.venv/bin/python -m pip ...` with reviewed, pinned requirements. This is a setup pattern, not an instruction to install automatically. Blender has its own Python; exchange JSON/PNG with the venv instead of assuming venv packages are visible to `bpy`.

The [TOML](../assets/tool-configs/codex-project.toml.example) and [JSON](../assets/tool-configs/mcp-client.json.example) files are **inactive templates with invalid placeholder paths**, not installed configuration. Substitute verified absolute paths. Merge only the needed entry into the host's documented project-scoped config; preserve existing settings. Codex supports project `.codex/config.toml`; other clients have different locations and trust/restart requirements. If project config is unavailable or denied, do not fall back to global mutation.

## Aseprite: native pixel edits and export

[Community Aseprite MCP](https://github.com/Vollkorn-Games/aseprite-mcp) uses Node, Aseprite batch mode and Lua. The verified source revision is `28900e757d7e5c18515ad0a95558acde1865aad2`; inspect current source before installing/running a different revision. Use stdio, not an exposed unauthenticated HTTP listener. The MCP server's MIT license does not license redistribution of the separate Aseprite binary. Do not bundle binaries or credentials in this skill.

Useful tools: `draw_pixels`, `render_sprite`, `save_sprite`, `export_gif`, `export_spritesheet`, `batch_export`, `get_sprite_info`. Inspect current schemas before calls; retain editable layers/timing/tags. Read-only tool filtering is not a filesystem sandbox.

Command shape after approved setup and local directories exist:

```sh
ASEPRITE_PATH="$PROJECT/tools/aseprite/bin/aseprite" \
XDG_CONFIG_HOME="$PROJECT/.local/config" TMPDIR="$PROJECT/.local/tmp" \
MCP_TRANSPORT=stdio node "$PROJECT/tools/aseprite-mcp/build/index.js"
```

`ASEPRITE_PATH` selects the binary. Source also supports `MCP_TOOLSETS`, `MCP_EXCLUDE_TOOLS` and `MCP_READ_ONLY=true`. Linux project-local XDG config was verified; check platform-specific isolation on other operating systems. Do not assume a local MCP can access only this project: keep host permissions restrictive.

Without MCP support, an inspected project Lua script can use direct CLI:

```sh
XDG_CONFIG_HOME="$PROJECT/.local/config" "$ASEPRITE" -b \
  --script-param output="$PROJECT/output/animation-v1.aseprite" \
  --script "$PROJECT/scripts/build_animation.lua"
```

The Lua script must implement the `output` parameter. This is direct CLI, not MCP execution. Sources: [Aseprite CLI](https://www.aseprite.org/docs/cli/), [Codex project MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [project configuration](https://learn.chatgpt.com/docs/config-file/config-basic).

## Blender: optional local motion/projection proxy

Prefer existing Blender CLI for blockout, armatures, camera/occlusion tests and projection validation; no Blender MCP/addon is required. Inspect scripts and `.blend` inputs; disable automatic startup/driver execution. A proxy verifies motion geometry, not identity, pixel craftsmanship or naturalness.

```sh
BLENDER_USER_RESOURCES="$PROJECT/.local/blender" \
BLENDER_USER_CONFIG="$PROJECT/.local/blender/config" TMPDIR="$PROJECT/.local/tmp" \
blender --background --factory-startup --disable-autoexec \
  --python-exit-code 1 --python "$PROJECT/scripts/build_rig.py" -- \
  --project "$PROJECT"
```

`build_rig.py` is a project script, not bundled here; it must parse arguments after `--`. Use Blender's bundled `bpy`, save a `.blend` plus landmark/camera/timing metadata, and match authored frame exposure. When opening a `.blend`, set output/render options after loading it and put render actions last. Source: [official Blender command-line reference](https://docs.blender.org/manual/en/4.1/advanced/command_line/arguments.html); local version-matched `blender --help` is authoritative for installed flags.

## Evidence level (2026-10-16)

- **Live discovery only:** Codex 0.159.2 help/version; Blender 4.3.2 help/version; Aseprite 1.3.18.6-dev version with project-local XDG config. No generation/render was performed in adapter research.
- **Dry-run:** installed host imagegen adapter generated a request preview without API credentials or a paid call. Not evidence of account/model access.
- **Historical project results:** the named Aseprite edit/export tools succeeded; Blender armature/projection scripts produced validation artifacts. These do not mean MCP generated the character or Blender rendered every final pixel.
- **Live generation (2026-10-16):** the Codex command shape above, through an app-bundled CLI; the result applies to that account, version and host only.
- **Documented/template only:** new project configs and setup patterns above. Verify in the destination environment before declaring them operational.

Record actual route, executable version, source revision, input/output hashes, alpha/dimensions and validation level. Exclude secrets from manifests and logs.
