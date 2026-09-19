# ADR-0005: MCP Definition Uses the Triple Format

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D4

## Context

`skills` ships only the MCP template triple (`MCP.md` + `mcp.json` +
`mcp_config.json`) with 7 empty categories and 0 registered servers. A
definition format must be fixed before populating.

## Decision

Option A short-term: keep the triple per MCP under `knowledge/mcps/<mcp>/`,
with `transport` + `capabilities` declared and secrets interpolated as
`{env:VAR}`. It evolves to option B (one canonical source + generated
per-harness configs) once the catalog grows beyond a handful of MCPs.

## Consequences

Every registered MCP carries the triple; coherence validation and secret
checks land with the MCP validator in F3.

## Evidence

`skills/mcps/_template/{MCP.md,mcp.json,mcp_config.json}`; `skills/MCPS.md:1-56`.
