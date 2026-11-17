# Evidence

**Status:** normative
**Scope:** every verification, audit or reconstruction claim the framework makes —
in an eval, a review, a plan or an agent's final report.

## Rule

A claim is only as strong as the evidence cited for it, and the default when
evidence is incomplete is **not** success.

### The evidence envelope

Every observation carries a small, provider-neutral record:

- **confidence** — `observed` (measured here), `derived` (computed from
  observations) or `inferred` (reasoned).
- **authority** — where it came from: shipped artifact, controlled replay,
  historical reference, an external service, or analyst inference.
- **limitations** — never empty; what the observation does NOT establish.
- **subject** — what was observed, with a content digest.
- **evidence_links** — the ids of related observations.

An evidence identifier is DERIVED from the record's semantic content and
recomputed on read; a record whose id does not match its content is rejected, not
trusted.

### Tri-state, fail-closed verification

A verification reports one status per claim from `pass`, `fail`, `unsupported`,
`truncated`, `unknown`, `skipped`. The aggregate is fail-closed:

- `fail` dominates.
- **`fail`, `unknown`, `unsupported`, `truncated` and `skipped` never aggregate to
  `pass`.**
- A `pass` claim MUST cite at least one evidence id; a missing id injects an
  `unknown` rather than rounding up.

**Absence from incomplete evidence is never behavioral absence.** Missing
coverage, an unsupported capability or a conflicting observation stays explicit as
an unknown.

### The completion ledger

`engine/verify/ledger.py` builds a ledger with a per-status count and an overall
status; `complete` is true only when every claim passes and at least one exists.
`python3 scripts/coacus.py verify-ledger <path>` validates a ledger file.

### Mapping coverage outcomes onto the ledger

An audit or review that declares a list of surfaces (endpoints, modules, controls)
reports an outcome per surface so that "no finding" never reads as "clean". No new
ledger status is introduced; each outcome maps onto the existing ones:

| Outcome | Where it goes |
|---|---|
| A finding was reported | `fail` |
| Nothing found, with evidence | `pass`, citing at least one evidence id |
| More investigation is needed | `unknown` in the ledger, plus an `open` or `investigating` entry in the residual-unknown registry |
| Not applicable | left out of the ledger; the reason is recorded once in the scope list |
| Dropped by adversarial validation | the validation record in `review-findings-pipeline`; the surface's own status still comes from the other rows |

`skipped` is not used for "not applicable": it never aggregates to `pass`, so one
such surface would stop the ledger from ever being complete. The ledger belongs to
one run and is not persisted into memory. The scope list fixes the granularity of a
surface. Adapted from patterns recorded in ADR 0009 (revision `6337341602be6aa5860b1e83138f03bdd0b78f71`, reviewed 2026-11-17; see [`THIRD-PARTY-NOTICES.md`](../../THIRD-PARTY-NOTICES.md)).

### The residual-unknown registry

`engine/verify/unknowns.py` records what is not yet known as a revisioned entry:
status `open | investigating | blocked | contradicted | resolved`, a severity,
`required_authority` (what class of evidence would settle it),
`recommended_probes`, supporting versus contradicting evidence ids (an id may not
appear on both sides), and a resolution disposition. Every update is a new
revision, guarded by an expected revision; a `verified` resolution MUST cite
evidence.

## Rationale

Two failure modes recur when a model reports on its own work: it rounds a partial
result up to success, and it treats missing evidence as a quiet negative. Encoding
the tri-state, the fail-closed aggregation and the "cite evidence to claim pass"
rule as data — not prose — makes the honest report the only one a validator
accepts, and keeps what is still unknown visible as a first-class artifact.

## Enforcement

- `engine/verify/ledger.py` and `engine/verify/unknowns.py` are stdlib-only; each
  rejects a tampered record via a recomputed digest.
- `python3 scripts/coacus.py verify-ledger <path>` is the ledger command surface.
- `tests/test_verify.py` covers the aggregation law, the evidence requirement and
  the revision guard.
