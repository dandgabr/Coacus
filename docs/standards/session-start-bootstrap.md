# SessionStart Bootstrap

**Status:** normative
**Scope:** every supported harness, and the canonical bootstrap body and entry
skill it renders.

## Rule

### Injection

The bootstrap MUST be injected at SessionStart through a per-harness hook or
plugin. Injection is what activates the framework; without it the corpus is inert,
because a model will not reliably consult skills on its own.

- A harness renders EXACTLY ONE native JSON format per harness. Emitting two keys
  is forbidden.
- Detection is by environment variable. The user's harness config is never edited
  wholesale.
- The rendered bootstrap is a generated artifact, committed and drift-checked.

### One canonical body

The bootstrap text is rendered from ONE canonical body; authoring it separately
from the entry skill would create two hand-maintained copies that drift.

- `methodology/bootstrap/session-start.canonical.md` holds ONLY the wrapper
  (`<EXTREMELY_IMPORTANT>` plus preamble) with the `{entry_skill_body}` and
  `{tool_mapping}` slots.
- The entry skill body comes from
  `methodology/workflows/using-coacus/SKILL.md` — a single source.
- `engine/generators/bootstrap.py` renders one native bootstrap body per harness
  (plus, for shapes A/C, its manifest) into `harnesses/<h>/bootstrap/`.

### Render contract

`harnesses/<h>/harness.json` is data and drives the render:

- `bootstrap.shape` — one of `A` (shell hook), `B` (in-process), `C`
  (instructions-file/rule), `native-discovery` (nothing rendered).
- `bootstrap.outputs` — path and format per output.
- `bootstrap.native_key` and `bootstrap.forbidden_keys` — the one native field to
  emit and the aliases never to emit.
- `detection`, `tool_mapping`, `tool_denylist`, `install`.
- `live_cli` (optional) — the non-interactive invocation the behavior-eval live
  runner uses for this harness (`["opencode", "run"]`, `["codex", "exec"]`,
  `["agy", "--print"]`). Absent means the harness cannot run live.

A new harness is a new data file. A new shape is an engine change.

### Anti-double-injection

- Shape A emits exactly ONE native JSON key (the `native_key` declared in
  `harness.json`) and NEVER a key listed in `forbidden_keys`. Claude Code reads
  both `additional_context` and `hookSpecificOutput` without deduplication, so
  emitting both doubles the injection.
- Shape B guards injection with an `EXTREMELY_IMPORTANT` check.

### Harnesses that render nothing

A harness may declare `bootstrap.supported: false` and render nothing (the
`native-discovery` shape) when it surfaces skills natively. Antigravity rules
are capped at 12,000 characters, so shape C content MUST respect that cap.

## Rationale

The bootstrap and the entry skill cannot diverge when there is one body. Rendered
artifacts are verifiable live with a unique-marker test on harnesses installed
locally. The engine owns a closed shape set; adding a shape is a legitimate engine
variation point.

## Enforcement

- `engine/generators/bootstrap.py` renders the artifacts and owns `check`;
  `python3 scripts/coacus.py check` fails on drift.
- `harnesses/<h>/harness.json` declares the shape, native key and forbidden keys
  the generator consumes.
- `tests/test_bootstrap.py` covers the render contract, one-key emission and the
  anti-reinjection guard.
- `evals/scenarios/bootstrap-activation/` is the behavior scenario for live
  activation.
