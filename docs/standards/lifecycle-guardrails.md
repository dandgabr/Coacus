# Lifecycle Guardrails

**Status:** normative
**Scope:** the portable lifecycle-hook and guardrail layer rendered per harness.

## Rule

A guardrail is authored once and rendered natively per harness. The model is
**PAER** — Policy over Action, Event binding, Rendering effect:

- **Action** — the portable subject: `verb` (`exec`, `read`, `write`, `network`,
  `spawn`, `delegate`) plus a normalized `resource`. Defined in
  `methodology/lifecycle/actions.schema.json`.
- **Policy** — authored once in `methodology/lifecycle/policies/*.policy.json`.
- **Event** — when the policy is consulted; the canonical taxonomy lives in
  `methodology/lifecycle/events.json`. An event has a `class`:
  `gate` (may `allow`/`deny`/`ask`), `observe` (advisory only, never denies), or
  `lifecycle` (injection or loop trigger).
- **Rendering effect** — the harness-native encoding, emitted by the guardrail
  generator.

### Capability data

`harnesses/<h>/harness.json` carries a `lifecycle` block with per-event
capabilities (`support`, `can_block`, `can_ask`, `effect`, `evidence`, `resolved`,
`source`) and declared `gaps`. A harness without a `lifecycle` block is a
**closed** capability: nothing renders and nothing installs. The capability
matrix (`docs/reference/lifecycle-matrix.md`) is GENERATED from this data and
carries each cell's evidence class; a bare boolean is forbidden.

### Decisions and failure

- The canonical decision set is `allow | deny | ask`. `ask` is valid only where
  the harness exposes a human channel (`can_ask`); elsewhere it degrades by the
  policy's `on_ask_unavailable`.
- Decisions compose monotonically: `deny > ask > allow`. Adding a hook can only
  make the outcome stricter.
- Failure domains are split: `on_decision_failure` (the evaluator ran but could
  not decide) defaults to `deny`; `on_mechanism_failure` (the guardrail process
  itself failed) defaults to `allow` plus an advisory. A broken hook MUST NOT
  deny every call.

### Installation

- Ownership is per entry id, never a repository path. `--uninstall` removes every
  Coacus id; `--verify` proves presence and, where possible, position.
- The installer REFUSES to install a `deny` policy whose bound event is not
  `can_block` on that harness; `--allow-advisory` records the downgrade.
- A `deny` whose event has no native home is refused, not silently dropped.

## Rationale

Event names are the least portable axis; the policy is the most portable. Inverting
the conventional event-centric model puts the authored judgment in the shared
layer and leaves only the binding per harness. The capability data keeps the
framework honest: what a harness cannot enforce is declared, generated into the
matrix with its evidence class, and refused at install rather than degraded in
silence.

## Enforcement

- `engine/validators/harnesses.py` validates every `lifecycle` block against the
  canonical taxonomy and the registered plugin kinds.
- `engine/generators/guardrails.py` renders the native artifacts;
  `engine/generators/lifecycle.py` renders the matrix; `scripts/coacus.py check`
  fails on drift.
- `scripts/coacus_guard.py` evaluates policies at runtime; the generated hooks
  call it and never re-implement a decision.
- `tests/test_lifecycle.py` covers the render contract, the matrix and the
  validator; `tests/test_guardrail_scripts.py` executes the rendered hook.
