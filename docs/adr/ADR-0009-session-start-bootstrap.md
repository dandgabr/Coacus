# ADR-0009: SessionStart Bootstrap Injection

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D8

## Context

Central finding of `superpowers`: without SessionStart injection, skills are
dead weight — the model will not reliably consult them.

## Decision

Option A: inject the bootstrap at SessionStart via a per-harness hook/plugin.
A single canonical bootstrap content (`methodology/bootstrap/session-start.canonical.md`,
F3) is rendered by `harnesses/<h>/` into EXACTLY ONE native JSON format per
harness (Claude Code reads both `additional_context` and `hookSpecificOutput`
without dedup — emitting both causes double injection). Detection is by env
var; the user's harness config is never edited directly. One acceptance test
(F3): a clean session must auto-trigger the entry workflow skill.

## Consequences

Bootstrap render is a generated artifact (ADR-0014); smoke tests run per
supported harness; a negative test guards against double injection.

* Note (F3, 2026-09-19): the render contract is fixed in ADR-0016 (one canonical
  body from the entry skill; `harness.json` drives shapes A/B/C/native-discovery).

## Evidence

`superpowers/hooks/session-start:1-49`; `superpowers/.opencode/plugins/superpowers.js:124-137`;
`superpowers/CLAUDE.md:78-82`.
