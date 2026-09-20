# ADR-0017: Corpus Import Uses a Data-Driven Manifest and a Reorganized Taxonomy

* Status: accepted (2026-09-20, F6)
* Deciders: repository owner
* Related: ADR-0001 (language policy), ADR-0002 (agent single source), ADR-0004 (catalog from disk), ADR-0010 (single source for scripts and templates), ADR-0015 (provenance manifest)
* Supersedes: none

## Context

Coacus was assembled by importing two external source repositories — the
`skills` hub (skills + agents) and the `superpowers` workflow collection — plus
the `agente-arquitetura-si` document pipeline. The corpora arrived with:

- incompatible and overlapping category trees (`languages`, `framework`,
  `databases`, `cloud-infra`, `programs`, `security/*`, `domains/*`);
- duplicate artifacts: `document_converter.py` and `document_analyzer.py` were
  byte-identical across two repositories, most templates were identical, and two
  agent roles (`explore`, `code-researcher`) overlapped;
- PT-BR content that cannot ship under ADR-0001;
- no recorded origin for any artifact, so dedup and drift could not be audited.

Importing by hand would reproduce the exact failure ADR-0004 and ADR-0010 exist
to prevent: multiple hand-maintained copies that drift. The import had to be
reproducible, auditable and idempotent.

## Decision

Option A: **import from a data-driven manifest, into a reorganized taxonomy,
behind a dedup gate, with full provenance and full translation.**

- **Data-driven manifest.** All import rules live in
  `templates/import/import-manifest.json`: `source_repos`, `exclude_import_from`,
  `category_map`, `security_map`, `programs_map`, `domains_map`,
  `exclude_skills`, `name_dir_fixes`, `agent_merges` and the `superpowers`
  namespace. `scripts/coacus_import.py` reads the manifest and contains no
  repository-specific mapping. Correcting a mapping is a manifest edit.
- **Reorganized taxonomy.** The corpus is normalized into ten top-level
  categories under `knowledge/skills/`: `data`, `domains`, `engineering`,
  `frameworks`, `infrastructure`, `languages`, `mapping`, `platforms`, `roles`,
  `security`. Per-skill overrides exist where a source subcategory is too
  coarse (for example `pentest-cloud-aws-azure-gcp` moves to
  `security/offensive`).
- **Dedup gate.** `agente-arquitetura-si` is excluded from import by
  `exclude_import_from`, enforced against the actual action sources — a
  malformed manifest cannot read it. `using-superpowers` is excluded (replaced
  by the native `using-coacus`); `template-skill` is excluded. Declared agent
  merges union content rather than drop it: `explore` + `code-researcher` →
  `code-explorer`, with the old name kept as an alias. Scripts and templates
  live once, under `verticals/architecture_si/` and
  `templates/domains/architecture_si/` (ADR-0010).
- **Provenance.** Every imported file is recorded in `sources.lock.json` at the
  repository root (ADR-0015) with `source_repo`, `source_commit`, `source_path`,
  `source_sha256`, `target_path`, `target_sha256`, `origin_license`,
  `transform`, `import_run_id` and `imported_at`. Dedup key:
  `(source_repo, source_commit, source_path)`. Drift key: `target_sha256`.
  Re-running `apply` replaces the entry for a target, so import is idempotent.
- **Translation.** PT-BR content is translated to English at import, never
  copied (ADR-0001). The importer tags non-English files
  `pending-translation`; translation replaces it with `translated`. Translation
  is delegated to the `linguistic-specialist` agent under orchestrator
  governance.

## Consequences

- The import is reproducible from the manifest and its source commits; the
  manifest is the single place to correct a category or a rename.
- The taxonomy is stable and enumerable: ten categories, one flat skill
  namespace, `program-*`/`superpowers-*` prefixes preventing collisions.
- Dedup is enforced structurally, not by review: an excluded repository cannot
  be read, a merge cannot drop a charter, and a duplicate script has one home.
- Every imported byte is traceable to a source commit and hash, and every
  transformation (rename, merge, conversion, translation) is a recorded
  `transform` token.
- A dirty source working tree is recorded as `<commit>+dirty`, so provenance
  never claims a clean commit it did not have.
- `sources.lock.json` must stay outside the generated surface: it carries
  timestamps and would otherwise break the ADR-0014 idempotency contract.
- Completeness remains an open obligation until F8. The read-only audit
  (`engine/validators/completeness.py`) reconciles source repos, lock file and
  catalog to prove nothing was left behind.

## Evidence

`templates/import/import-manifest.json` (all mapping and dedup rules);
`scripts/coacus_import.py` (manifest reader, exclusion gate, merge, provenance
writer); `sources.lock.json` (1163 entries: 1096 from `skills`, 67 from
`superpowers`; 370 `translated`, 58 `converted:agent.source.md`, 20
`renamed:dir`, 1 `merged:code-researcher`); `docs/migration.md`;
`engine/validators/completeness.py`; catalog totals 199 skills + 15 workflows =
214 entries, 58 agents, 1 MCP.
