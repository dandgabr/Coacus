# MCP Definition

**Status:** normative
**Scope:** every MCP server declaration under `knowledge/mcps/<mcp>/` and its
generated configuration.

## Rule

Each MCP lives in exactly ONE canonical source: `knowledge/mcps/<mcp>/MCP.md`.
MCP names form a FLAT, globally unique namespace; the directory name MUST equal
the frontmatter `name` and be kebab-case.

The generator (`engine/generators/mcp_configs.py`) derives two committed,
drift-checked artifacts under `dist/`:

- `dist/mcp.json` — the harness server declaration (name, transport,
  command/args or remote url, `{env:VAR}` placeholders, capabilities).
- `dist/mcp_config.json` — setup metadata (description, requires, env VAR names,
  docs, author, license, version).

### Source frontmatter

| Key | Rule |
|---|---|
| `name` | kebab-case, equals the directory, globally unique |
| `description` | REQUIRED |
| `transport` | one of `stdio`, `http`, `streamable-http`, `sse` |
| `command` / `args` | REQUIRED for `stdio` |
| `remote_url` | REQUIRED for `http`, `streamable-http` and `sse` |
| `env_vars` | list of NAMES only, upper-case (`^[A-Z][A-Z0-9_]*$`) |
| `capabilities` | mapping (tools, resources, prompts) |
| `requires`, `docs`, `author`, `license`, `version` | declared metadata |

`stdio` and `streamable-http` are the current MCP spec transports; `http` and
`sse` are kept for compatibility.

### Secrets

`env_vars` carries names, never values. Any secret placeholder in the source MUST
be written as `{env:VAR}` and is resolved at activation time. Secret values never
enter the repository, and generated configs never carry them.

## Rationale

A hand-maintained triple (`MCP.md` + `mcp.json` + `mcp_config.json`) keeps three
copies of the same facts and drifts — the exact failure single-source generation
exists to prevent. Fixing the contract before populating the registry, at one
declared MCP, removed the triple-drift class at zero migration cost.

## Enforcement

- `engine/validators/mcps.py` (via `python3 scripts/coacus.py validate`) checks
  the source contract: frontmatter, kebab-case name equal to the directory, flat
  namespace uniqueness, transport enum, command/url requirements, capabilities
  shape and upper-case env var names.
- `engine/generators/mcp_configs.py` owns `check`, which validates `dist/`
  coherence and orphan detection at the artifact layer, so an edited source never
  deadlocks `generate`. `python3 scripts/coacus.py check` runs it.
- `tests/test_mcp.py` covers the source and dist contracts.
