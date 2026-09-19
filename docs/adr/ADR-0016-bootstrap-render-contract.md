# ADR-0016: SessionStart Bootstrap Is Rendered From One Canonical Body

* Status: accepted (2026-09-19, F3)
* Deciders: repository owner
* Decision ID: D8 (render contract)
* Related: ADR-0009 (bootstrap injection), ADR-0003 (adapters), ADR-0014 (committed generated artifacts)

## Context

ADR-0009 fixes *that* the bootstrap is injected at SessionStart, one native
format per harness. It does not fix *how* the content is produced. Authoring the
bootstrap text separately from the entry skill would create two hand-maintained
copies — drift by construction (ADR-0010).

## Decision

One canonical body, rendered per harness:

- `methodology/bootstrap/session-start.canonical.md` holds ONLY the wrapper
  (`<EXTREMELY_IMPORTANT>` + preamble) with `{entry_skill_body}` and
  `{tool_mapping}` slots.
- The entry skill body comes from
  `methodology/workflows/using-coacus/SKILL.md` (single source).
- `harnesses/<h>/harness.json` is data: `bootstrap.shape` (`A` shell-hook,
  `B` in-process, `C` instructions-file, `native-discovery` none),
  `outputs` (path+format), `native_key`/`forbidden_keys`, `detection`,
  `tool_mapping`, `tool_denylist`, `install`.
- `engine/generators/bootstrap.py` renders one native bootstrap BODY per harness
  (plus, for shapes A/C, its manifest) into `harnesses/<h>/bootstrap/`, committed
  and drift-checked (ADR-0014). A new harness is a new data file; a new shape is
  an engine change.
- Anti-double-injection: shape A emits exactly one native JSON key (the
  `native_key` declared in `harness.json`, e.g.
  `hookSpecificOutput.additionalContext`) and never a key listed in
  `forbidden_keys` (Claude Code reads both fields without dedup); shape B guards
  with an `EXTREMELY_IMPORTANT` check.

`bootstrap.supported: false` harnesses render nothing: Codex uses
`native-discovery` (no SessionStart hook); Cursor is a stub until a live
acceptance test is possible.

## Consequences

The bootstrap and the entry skill cannot diverge — there is one body. Rendered
artifacts are verifiable live (unique-marker test) for harnesses installed
locally. The engine owns the closed shape set; adding a shape is a legitimate
OCP variation point.

## Evidence

`superpowers/hooks/session-start:1-49` (cats the skill); `superpowers/.opencode/plugins/superpowers.js`
(reads + strips; message transform + guard); `superpowers/docs/porting-to-a-new-harness.md:225-300`
(shapes A/B/C and the routing table).