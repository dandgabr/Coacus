# Antigravity MCP Servers

Antigravity supports local `stdio` servers and remote MCP endpoints. MCP servers
can be configured globally or bundled in an enabled plugin. See the [official MCP guide](https://antigravity.google/docs/mcp)
for supported fields and surface-specific configuration paths.

## Configuration

An MCP config contains an `mcpServers` object. A local process uses `command`
and optional `args`, `env`, and `cwd`:

```json
{
  "mcpServers": {
    "local-catalog": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

Plugin-level configuration lives in `mcp_config.json`. Use absolute runtime
paths when a local server needs to run outside the active workspace. Keep
canonical source files portable; resolve machine-specific paths during
installation.

Remote servers use `serverUrl` and optional supported authentication fields.
Do not copy legacy `url` examples into current Antigravity MCP configurations.

## Diagnostics and permissions

Use `/mcp` in Antigravity CLI to inspect server status and connection logs. The
App and IDE expose MCP management in their Customizations interfaces. Tool
access is subject to Antigravity permissions; the default may require approval
for MCP calls.

## Coacus catalog server

Coacus installs a local, standard-library Python MCP server in its Antigravity
plugin. Its bounded `search` tool returns catalog metadata; `get` returns one
canonical skill or agent source; `get_reference` returns a supporting file
inside that capability's directory. The server uses a generated static index
and does not require the Coacus checkout after installation.
