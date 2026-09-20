# Testing

**Status:** normative
**Scope:** `tests/` and `evals/`, and every contribution that changes behavior.

## Rule

Testing has TWO layers. Deterministic infrastructure and LLM behavior are different
problems; mixing them produces flaky CI or untested behavior. They MUST NOT be
merged.

### Layer 1 — deterministic infrastructure (`tests/`)

- Stdlib `unittest`, ZERO runtime dependencies.
- Runs on every commit as a BLOCKING gate.
- Covers schemas, generators, idempotency, deduplication, the governor, the TOON
  validator, the installer and the vertical dispatcher.

```bash
python3 -m unittest discover -s tests
```

### Layer 2 — behavior evaluation (`evals/`)

Behaviour evaluation has two tiers:

- **static** — the scenario-schema validator (`engine/validators/evals.py`).
  Deterministic, no LLM, part of `validate`, BLOCKING.
- **live** — real agent sessions driven by `scripts/coacus_eval.py`, with a fixed
  rubric and a pluggable or agent judge. ADVISORY: local/manual only, NEVER blocks
  CI, because it needs an installed harness CLI and credentials.

Scenarios live at `evals/scenarios/<id>/scenario.json`. The static schema checks
`id`, `title`, `harness`, `prompt`, `checks`, `rubric` and `acceptance`, requires
a known target harness, checks that every check is well-formed, and rejects any
scenario string carrying a secret or an absolute path.

## Rationale

Structural regressions — schemas, generators, idempotency, dedup — are caught
deterministically. Behavioral quality is tracked without destabilizing the gate.
A live eval that needs credentials must never be able to fail a pull request for
infrastructure reasons.

## Enforcement

- `.github/workflows/ci.yml` runs `python3 -m unittest discover -s tests` as a
  blocking step.
- `engine/validators/evals.py` runs inside `python3 scripts/coacus.py validate`
  and rejects malformed scenarios; the D12 scan reuses
  `engine/validators/hygiene.py` patterns.
- `.github/workflows/evals.yml` runs `python3 scripts/coacus_eval.py validate` on
  a schedule and on manual dispatch, so scenario drift is caught outside PRs.
- `tests/test_evals.py` covers the scenario schema contract.
