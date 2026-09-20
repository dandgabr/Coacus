# Corpus and Taxonomy

**Status:** normative
**Scope:** the imported corpus under `knowledge/`, the import manifest, and the
rules that keep the corpus organized, deduplicated and traceable.

## Rule

### Data-driven import

All import rules live in `templates/import/import-manifest.json`. The importer
(`scripts/coacus_import.py`) reads the manifest and contains NO
repository-specific mapping. Correcting a category or a rename is a manifest
edit, not a code change.

The manifest declares: `source_repos`, `exclude_import_from`, `category_map`,
`security_map`, `programs_map`, `domains_map`, `exclude_skills`, `name_dir_fixes`,
`agent_merges` and the `superpowers` namespace.

### Taxonomy

The corpus is normalized into TEN top-level categories under `knowledge/skills/`:
`data`, `domains`, `engineering`, `frameworks`, `infrastructure`, `languages`,
`mapping`, `platforms`, `roles`, `security`.

- Per-skill overrides exist where a source subcategory is too coarse (for example
  `pentest-cloud-aws-azure-gcp` → `security/offensive`).
- The skill namespace is FLAT. Collisions are prevented by prefixes:
  `program-*` for tooling and `superpowers-*` for imported process workflows.
- Process workflows live under `methodology/workflows/`.

### Dedup gate

Deduplication is structural, not a review habit:

- `agente-arquitetura-si` is excluded by `exclude_import_from`, enforced against
  the actual action sources, so a malformed manifest cannot read it.
- `using-superpowers` is excluded (replaced by the native `using-coacus`);
  `template-skill` is excluded.
- Declared agent merges UNION content rather than drop it — for example
  `explore` + `code-researcher` → `code-explorer`, with the old name kept as an
  alias.
- Scripts and templates live once, under `verticals/architecture_si/` and
  `templates/domains/architecture_si/`.

### Translation

Non-English source content is translated during import, never copied. The importer
tags a non-English file `pending-translation`; translation replaces the tag with
`translated`. Translation is delegated to the `linguistic-specialist` agent under
orchestrator governance. See [`english-only.md`](english-only.md).

### Provenance

Every imported file is recorded in `sources.lock.json`. The full entry schema,
the dedup key `(source_repo, source_commit, source_path)`, the drift key
`target_sha256` and the `<commit>+dirty` convention are defined in
[`provenance.md`](provenance.md).

## Rationale

The source corpora arrived with overlapping category trees, byte-identical
scripts, two overlapping agent roles and no recorded origin. Importing by hand
would reproduce the exact failure single-source generation exists to prevent.
Driving the import from a manifest makes it reproducible from the source commits;
the taxonomy makes it enumerable; the dedup gate makes redundancy a build error;
provenance makes every imported byte traceable.

## Enforcement

- `scripts/coacus_import.py` reads the manifest, applies the exclusion gate, the
  merges and the provenance writer; `python3 scripts/coacus_import.py plan` is the
  dry-run surface.
- `engine/validators/completeness.py` (via
  `python3 scripts/coacus.py completeness`) reconciles source repositories, the
  lock file and the catalog to prove nothing was left behind, including excluded
  skills, merged sources and rename targets.
- `engine/validators/skills.py` enforces the placement depth and the flat
  namespace.
- `tests/test_completeness.py` covers the reconciliation.
