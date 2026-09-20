# TOON Protocol

**Status:** normative
**Scope:** every agent-to-agent handoff payload. JSON remains the format for
machine contracts (APIs, manifests); TOON is for prose handoffs.

## Rule

Agent handoffs MUST use a TOON payload with these fields:

```text
@FROM: <emitter>
@TO: <receiver-or-orchestrator>
@STATUS: <OK | CONFLICT | BLOCKED | NEED_INFO>
@CTX: <concise-context-id>
@FILES: <path:lines>;<path:lines>
@SUMMARY: <ultra-compact summary>
@ACTION_NEEDED: <objective next step>
```

Required: `@FROM`, `@TO`, `@STATUS`, `@CTX`, `@SUMMARY`. Optional: `@FILES`,
`@ACTION_NEEDED`.

### Field rules

- `@STATUS` MUST be exactly one of `OK`, `CONFLICT`, `BLOCKED`, `NEED_INFO`.
- `@FILES` paths MUST be repository-relative. Absolute paths are rejected. Paths
  that escape upward (`..` components) are rejected. A `:<range>` or `:N` suffix
  is a line locator, not part of the path.
- A field MUST NOT carry a secret-shaped literal (access keys, tokens, private
  keys) in any field, including `@SUMMARY` and `@ACTION_NEEDED`.
- Duplicate fields are rejected; each field appears once.

### Conflict mediation

Conflict resolution flows through the orchestrator with TOON evidence in
`@FILES`. When agents disagree on a contract, they exchange TOON payloads focused
on the disagreement until they converge.

## Rationale

TOON is token-compact and machine-parseable: a handoff costs a handful of lines
instead of a verbose JSON conversation, which lowers latency and removes syntactic
noise. Fixing the field set and the status enum lets a validator reject malformed
handoffs mechanically.

## Enforcement

- `engine/toon.py` validates required fields, the status enum, relative `@FILES`
  paths (no absolute paths, no `..` escapes), unknown fields and secret-like
  literals.
- `python3 scripts/coacus.py toon <file>` runs that validator; it exits non-zero
  on any error.
- `tests/test_toon.py` covers the field, status, path and secret rules.
