# ADR-0004: Catalog Generated From Disk

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D3

## Context

The `skills` hub suffered inventory drift by construction: CATALOGO.md declared
199 skills vs 200 on disk; skills.json had 193 entries vs 200; README counts
were stale. A new framework must make drift impossible, not merely detectable.

## Decision

Option A: the catalog (`catalog/catalog.json` plus human indexes) is GENERATED
from disk — disk is the single truth. `python3 scripts/coacus.py check`
regenerates in memory and fails CI on any un-regenerated diff (CI wiring lands
in F2; today the check runs locally via `scripts/coacus.py check`). Generated
files contain no timestamps so regeneration is idempotent.

## Consequences

Manual catalog editing is meaningless (overwritten); contributors only add
sources and run `generate`. Inherited drift is reconciled during migration (F6).

## Evidence

* Note (F2, 2026-09-18): CI wiring **authored** — `.github/workflows/ci.yml` runs
  `check` as a gate (never `generate`); active once committed, pushed and
  required by a ruleset.

`skills/scripts/generate_catalog.py:1-191`; `skills/scripts/validate_skills.py:5-180`;
map findings S1–S4.
