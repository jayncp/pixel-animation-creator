# Inactive project-local templates

These `.example` files are not executable or installed configuration. Every `<...>` value requires substitution with a verified absolute path. Create the referenced project-local directories only during authorized setup.

- `codex-project.toml.example`: merge its server table into the current project's `.codex/config.toml`, preserving existing settings and trust controls.
- `mcp-client.json.example`: client-neutral schema example only. Consult the selected client's documentation for its supported project-scoped location and keys. Do not assume this is a Claude Desktop global configuration or copy it into one.

No template installs software, starts a server, stores credentials, changes permissions or authorizes access. Use stdio and retain the host sandbox. If project-scoped configuration is unsupported or denied, stop setup rather than altering global configuration. Linux XDG isolation was verified; validate other platforms separately. See `../../references/tool-adapters.md`.
