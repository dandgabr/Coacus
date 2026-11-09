# Antigravity JSON Configuration

Use the configuration formats documented for the selected Antigravity surface.
See the official [MCP configuration guide](https://antigravity.google/docs/mcp)
and [plugin guide](https://www.antigravity.google/docs/plugins).

## MCP configuration

Global and workspace MCP configuration uses an `mcpServers` object. A local
stdio server uses `command`, optional `args`, `env`, and `cwd`; a remote server
uses `serverUrl` with supported optional authentication properties.

```json
{
  "mcpServers": {
    "catalog": {
      "command": "python3",
      "args": ["/path/to/catalog_server.py"]
    }
  }
}
```

Plugins can bundle their server entries in `mcp_config.json`. Antigravity's
global MCP config is separate from plugin configuration. Do not create or edit
a `plugins.json` registry: current plugin activation is managed through the
documented plugin folders and UI/CLI commands.

## Plugin manifest

`plugin.json` marks a plugin directory and carries supported metadata such as
`name` and `description`. Skills, agents, rules, hooks, and MCP servers are
discovered from their documented plugin paths; the manifest does not enumerate
those files.
