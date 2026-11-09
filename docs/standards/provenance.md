# Provenance

**Status:** normative
**Scope:** imported artifacts, native canonical sources and their provenance lifecycle.

## Rule

Every imported file carries a provenance entry. Native authored skills, workflows
and agent sources are registered during `generate`. Provenance lives at the
repository root as `sources.lock.json`, owned by `engine/provenance.py`. The
import pipeline records imported origins; `sync_authoring()` records native
canonical sources. The catalog writer does not own this manifest. `check` remains
read-only and checks generated outputs; provenance validation runs through
`validate` and the artifact checks after generation.

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

### Native authored sources

`generate` calls `sync_authoring()` for canonical `SKILL.md` files and
`agent.source.md` files. Missing entries use `source_repo: authoring`,
`source_commit: native`, matching source/target paths and hashes, and an
`authored` transform. Existing native entries update their hashes when content
changes. Unchanged entries retain their registration timestamp. This pass does
not replace imported provenance or remove entries.

Supporting reference files still need source citations, review dates and any
required attribution in their content; native registration does not independently
register every reference file. Actually copied or adapted upstream files retain
their imported origin and license through the import pipeline.

### Portable workflow conversions

An imported workflow helper converted to Python keeps the upstream `source_path`
and `source_sha256`, records the `.py` target, and adds `converted:python` to
`transform`. Reimports preserve that reviewed Python implementation while the
upstream source hash matches. A changed or missing upstream source stops the
import before copying any action; review and update the conversion before
advancing its source hash. The text normalizer uses the Python helper commands.

### Location

`sources.lock.json` MUST stay outside timestamp-free generated directories. It carries
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
  key), `sync_authoring()` and `refresh_targets()`. `validate()` runs in
  `python3 scripts/coacus.py validate` and after writing in `generate`; a target
  whose recorded hash no longer matches disk is an error.
- `python3 scripts/coacus.py refresh` recomputes `target_sha256` from disk for
  every drifted entry (and advances `source_sha256` too when the entry is
  in-place, `source_sha256 == target_sha256`, with no `converted:` or `adapted:`
  transform). Use it after editing an imported
  file without re-running the importer; the importer's `apply` remains the
  canonical path for a fresh import.
- `engine/validators/completeness.py` (via
  `python3 scripts/coacus.py completeness`) reconciles lock targets against disk,
  flags orphan skills with no provenance, and checks source repos when present.
- `tests/test_discovery_provenance.py` covers the schema and target checks.
  `tests/test_import_licenses.py` covers the license resolution and the
  in-place relabel applied by `scripts/coacus_import.py apply`.
