# Single Source

**Status:** normative
**Scope:** scripts, templates, and every artifact that could otherwise exist as a
copy.

## Rule

A script or template lives in exactly ONE place in this repository and is consumed
by path. No copy without a verified hash.

- Scripts live under `engine/` (core tooling) and `scripts/` (thin CLIs). Domain
  pipelines live under `verticals/`.
- Templates live under `templates/`: `templates/authoring/` for artifact
  scaffolds, `templates/domains/` for domain templates,
  `templates/import/import-manifest.json` for import rules.
- Cross-imports between converters are forbidden. The dispatcher is the single
  entrypoint (see [`knowledge-ingestion.md`](knowledge-ingestion.md)).

If a transient copy must exist during a migration, it MUST be hash-verified
against its origin and tracked to closure. Divergence fails the build. A published
package (pip) is deferred until external consumers exist.

## Rationale

The source repositories carried byte-identical copies of the same scripts and
near-identical template sets. Copies without canonicity rot: one gets fixed, the
other does not, and nothing in the build notices. A single home plus a hash guard
makes duplication a build error.

## Enforcement

- `python3 scripts/coacus.py check` compares every generated surface against a
  fresh regeneration and fails on drift — this catches divergence in anything
  derived from a single source.
- `engine/validators/hygiene.py` rejects cross-cutting violations (absolute paths,
  secrets, tool names) over the canonical directories in which copies would hide.
- `python3 scripts/coacus.py completeness` reconciles imported scripts and
  templates against `sources.lock.json`, so a duplicate that arrives without a
  recorded origin is surfaced as a gap.
- `tests/test_idempotency.py` asserts regeneration is byte-identical.
