# Antigravity Plugins

Antigravity plugins bundle skills, custom subagents, rules, MCP server
configuration, and lifecycle hooks. See the [official plugin guide](https://www.antigravity.google/docs/plugins)
for the current schema and surface-specific installation locations.

## Plugin layout

```text
plugins/<plugin-name>/
├── plugin.json
├── mcp_config.json
├── hooks.json
├── skills/<skill-name>/SKILL.md
├── agents/<agent-name>.md
└── rules/<rule-name>.md
```

`plugin.json` is the required marker. Its supported metadata is `name` and
`description`; the manifest is not a file registry. Antigravity discovers
components from their documented directories. There is no `plugins.json`
registry to edit.

## Install and validate

Use the Customizations UI or the `agy plugin` commands for plugin management.
`agy plugin validate <path>` checks a staged plugin before activation;
`agy plugin list --json` reports installed plugins and bundled paths.

Global plugin locations vary by Antigravity surface. Consult the official guide
for the selected App, CLI, or IDE rather than assuming one path applies to all.
Coacus currently stages its adapter under `~/.gemini/config/plugins/coacus/`.

## Coacus on-demand profile

Coacus's default Antigravity profile keeps complete canonical skill and agent
sources under the plugin's opaque `catalog/` data directory. A compact rule and
local MCP server search and return selected instructions. Only compact native
agent selectors remain under `agents/`, so Antigravity can still start those
roles as subagents. Use `--antigravity-profile full` to install the full native
skill and agent bodies instead.

Do not put private state or secrets in a plugin. The catalog contains public,
versioned Coacus instructions and must remain self-contained after installation.
