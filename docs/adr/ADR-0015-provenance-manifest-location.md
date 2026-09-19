# ADR-0015: Provenance Manifest Lives at the Repository Root

* Status: accepted (2026-09-18, F2 planning, user-confirmed)
* Deciders: repository owner
* Related: P4 (provenance premise), ADR-0014 (committed generated artifacts)

## Context

Premise P4 requires every imported artifact to record its origin
(repo/commit/path/hash) for traceability and safe dedup. The obvious home,
`catalog/SOURCES.json`, conflicts with ADR-0014: the catalog generator is
timestamp-free and byte-idempotent, while provenance entries carry
`imported_at` at import time. A timestamped file inside the generated surface
would make `coacus.py check` fail forever.

## Decision

Provenance lives at the repository root as `sources.lock.json`, owned by
`engine/provenance.py` and populated by the F6 import pipeline — never by the
catalog generator, and never part of the `generate`/`check` surface. The seed
is `{"schema": 1, "entries": []}`.

Entry fields: `source_repo`, `source_commit`, `source_path`,
`source_sha256`, `target_path`, `target_sha256`, `origin_license`,
`transform` (normalizations/renames/translations applied), `import_run_id`,
`imported_at`. Dedup key: `(source_repo, source_commit, source_path)`;
drift key: `target_sha256` (dedup and drift enforcement are performed by the
F6 import pipeline; this module owns the schema and target-existence check).

Optional per-entry key: `aliases` (searchable alternate names created by
import-time renames, e.g. `containers` → `program-containers`).

## Consequences

Import provenance is auditable and dedup-safe without violating the
idempotency contract of generated artifacts. Renames applied at import (e.g.
`programs/containers` → `program-containers`, ADR-0001 translations) are
recorded in `transform` and in the optional `aliases` list. Dedup/drift keys
are documented here and enforced by the F6 import pipeline.
