# ADR-0005: MCP Definition Uses a Single Source With Generation

* Status: accepted (2026-09-18, F0 gate); **amended at F3 (2026-09-19) to Option B**
* Deciders: repository owner
* Decision ID: D4

## Context

`skills` ships only the MCP template triple (`MCP.md` + `mcp.json` +
`mcp_config.json`) with 7 empty categories and 0 registered servers. A
definition format must be fixed before populating. The triple keeps three
hand-maintained copies of the same facts, which drifts (the exact failure
ADR-0002/0010 exist to prevent).

## Decision

**Amended (F3): Option B — one source + generation.** Each MCP lives at
`knowledge/mcps/<mcp>/MCP.md` (flat, globally unique name). Its frontmatter
carries the server declaration (`name`, `description`, `transport`,
`command`/`args` or `remote_url`, `env_vars` as NAMES only, `capabilities`,
`requires`, `docs`, `author`, `license`, `version`). The generator
(`engine/generators/mcp_configs.py`) derives `dist/mcp.json` (harness
declaration) and `dist/mcp_config.json` (setup metadata), committed and
drift-checked (ADR-0014). `transport` uses the set accepted by this contract
(`stdio`/`http`/`streamable-http`/`sse`; `stdio` and `streamable-http` are the
current MCP spec transports, `http`/`sse` are kept for compatibility); secrets
stay as `{env:VAR}`.

*Original F0 decision (superseded):* hand-authored triple, Option A.

## Consequences

The trigger for moving to Option B was F3 itself — fixing the contract before
populating, at zero MCPs, rather than waiting for a count threshold. A single
source removes the triple-drift class. The validator (`engine/validators/mcps.py`)
checks the source contract; `mcp_configs.check` owns dist/ coherence and orphans.

## Evidence

`skills/mcps/_template/{MCP.md,mcp.json,mcp_config.json}` (upstream `skills`
repo — not imported here); `skills/MCPS.md:1-56` (upstream);
`skills/mcps/_template/mcp.json` (capabilities as object; `{env:VAR}` rule, upstream).
