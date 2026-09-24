# Provenance

**Status:** normative
**Scope:** every imported artifact and the import pipeline.

## Rule

Every imported file carries a provenance entry. Provenance lives at the repository
root as `sources.lock.json`, owned by `engine/provenance.py` and populated ONLY by
the import pipeline. The catalog generator never writes it, and it is never part
of the `generate`/`check` surface.

The seed is `{"schema": 1, "entries": []}`.

### Entry fields

Required per entry:

| Field | Meaning |
|---|---|
| `source_repo` | Source repository identifier |
| `source_commit` | Source commit; a dirty tree is recorded `<commit>+dirty` |
| `source_path` | Path inside the source repository |
| `source_sha256` | Content hash of the source file |
| `target_path` | Repository-relative target |
| `target_sha256` | Content hash of the imported file |
| `origin_license` | License carried by the origin (resolved from the import manifest's `licenses` map; `see source repo` when undeclared) |
| `transform` | Normalizations applied (rename, merge, conversion, translation) |
| `import_run_id` | Import run that produced the entry |
| `imported_at` | Import timestamp |

Optional: `aliases` — searchable alternate names created by import-time renames
(for example `containers` → `program-containers`).

### Keys

- Dedup key: `(source_repo, source_commit, source_path)`. Re-running `apply`
  REPLACES the entry for a target, so import is idempotent.
- Drift key: `target_sha256`.

### Location

`sources.lock.json` MUST stay outside the generated surface. It carries
`imported_at`, and a timestamped file inside `catalog/` would make the
idempotency check fail forever.

## Rationale

Principle P4 requires every imported artifact to record its origin so traceability,
dedup and drift can be audited. A dedicated root-level manifest keeps that audit
possible without violating the timestamp-free, byte-idempotent contract of
generated artifacts.

## Enforcement

- `engine/provenance.py` owns the schema, the seed, `validate()` (the required
  keys, the `aliases` list shape, target existence and the `target_sha256` drift
  key) and `refresh_targets()`. `validate()` runs in
  `python3 scripts/coacus.py validate` and after writing in `generate`; a target
  whose recorded hash no longer matches disk is an error.
- `python3 scripts/coacus.py refresh` recomputes `target_sha256` from disk for
  every drifted entry (and advances `source_sha256` too when the entry is
  in-place, `source_sha256 == target_sha256`). Use it after editing an imported
  file without re-running the importer; the importer's `apply` remains the
  canonical path for a fresh import.
- `engine/validators/completeness.py` (via
  `python3 scripts/coacus.py completeness`) reconciles lock targets against disk,
  flags orphan skills with no provenance, and checks source repos when present.
- `tests/test_discovery_provenance.py` covers the schema and target checks.
  `tests/test_import_licenses.py` covers the license resolution and the
  in-place relabel applied by `scripts/coacus_import.py apply`.
