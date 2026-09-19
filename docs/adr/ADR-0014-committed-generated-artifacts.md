# ADR-0014: Generated Artifacts Are Committed

* Status: accepted (2026-09-18, F0 gate, user-confirmed)
* Deciders: repository owner

## Context

`dist/`, `catalog/` and `.agents/` are generated. Committing them costs larger
diffs; not committing them forces every harness consumer to build before use
and hides drift until runtime.

## Decision

Commit generated artifacts to git. A drift check
(`python3 scripts/coacus.py check`) compares disk against a fresh regeneration
and fails on any diff (CI wiring lands in F2). Generated files contain no
timestamps so the check is deterministic.

## Consequences

Harnesses consume the repository as-is (clone → activate); every PR exposes
generated diffs for review; contributors must run `generate` before committing.

## Related

ADR-0002 (agent manifests), ADR-0004 (catalog), ADR-0006 (discovery),
ADR-0009 (bootstrap render).
