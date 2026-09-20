# Corpus migration (F6)

Coacus was assembled by importing two external source repositories into the
repository's own taxonomy. This document records where the material came from,
how it was mapped and deduplicated, how provenance is kept, and how the
translation was handled. The decision is ratified as
[ADR-0017](adr/ADR-0017-corpus-import-and-taxonomy.md).

The import is reproducible: `templates/import/import-manifest.json` is the
single data file that drives it, and `scripts/coacus_import.py` performs it.

## Source repositories

| Key | Repository | Imported |
|---|---|---|
| `skills` | the skills hub (skills + agents) | skills, agents |
| `superpowers` | the Superpowers workflow collection | workflows |
| `agente-arquitetura-si` | architecture-SI agent and document pipeline | **excluded from import** |

`agente-arquitetura-si` is listed in `exclude_import_from`. The importer enforces
the exclusion on the actual action sources, so even a malformed manifest cannot
read that repository. Its pipeline was ported by hand into
`verticals/architecture_si/` instead ([ADR-0012](adr/ADR-0012-ingestion-dispatcher.md)),
and its templates were copied once into `templates/domains/architecture_si/`
([ADR-0010](adr/ADR-0010-single-source-scripts-templates.md)).

Each provenance entry records the source commit at import time. The F6 run used
a dirty working tree for `skills`, so the recorded commit carries a `+dirty`
suffix.

## Taxonomy mapping

The source category trees do not match Coacus. All mapping rules live in
`import-manifest.json` as data:

| Source tree | Rule | Target |
|---|---|---|
| `languages`, `framework`, `mapping`, `roles` | `category_map` (identity or rename) | `languages`, `frameworks`, `mapping`, `roles` |
| `databases` | `category_map` | `data` |
| `cloud-infra` | `category_map` | `infrastructure` |
| `engineering-practices`, `patterns` | `category_map` | `engineering/practices`, `engineering/patterns` |
| `linguistics` | `category_map` | `domains/linguistics` |
| `security/*` | `security_map` | `security/ai`, `security/appsec`, `security/iam`, `security/crypto`, `security/grc`, `security/operations` |
| `programs/*` | `programs_map` | `infrastructure`, `security/tooling`, `mapping`, `data`, `platforms` |
| `domains/academic-*` | `domains_map` prefix rule | `domains/academic` |
| `domains/*` | `domains_map` | `domains/industry` or `languages` |

The security tree has per-skill overrides where a source subcategory is too
coarse. For example `pentest-cloud-aws-azure-gcp` and `bug-bounty-methodology`
move from `security/appsec` to `security/offensive`, and
`edr-evasion-endpoint-security`, `memory-manipulation` and
`windows-internals-security` move to `security/platform`. The same pattern
applies to `security/grc` and the `programs` map.

The result is the ten top-level categories documented in
[`architecture.md`](architecture.md): `data`, `domains`, `engineering`,
`frameworks`, `infrastructure`, `languages`, `mapping`, `platforms`, `roles`,
`security`.

### Directory renames

`name_dir_fixes` renames directories whose names collide with the `program-*`
convention or conflict with the flat skill namespace. The recorded renames are
`containers` → `program-containers`, `github-actions` → `program-github-actions`,
`markmap` → `program-markmap` and `moodle` → `program-moodle`. Renames are
recorded in each entry's `transform` (`renamed:dir`) and, for searchability, as
`aliases` where applicable.

### Agent path remapping

An imported `AGENT.md` references skills with the old taxonomy. The importer
converts `AGENT.md` into the canonical `agent.source.md` and rewrites every
`skills:` frontmatter path and inline `SKILL.md` link to the new
repository-root-relative location. Paths are written root-relative because that
is the agent-source contract ([ADR-0002](adr/ADR-0002-agent-manifests-single-source.md)).
Cross-skill links inside imported bodies are resolved against the current tree,
tolerating renames through the `program-` and `superpowers-` variants.

## Deduplication

Three dedup mechanisms keep the corpus from carrying redundant artifacts.

### Blocked source repository

`agente-arquitetura-si` is excluded entirely (see above). Its scripts and
templates were reconciled into the single-source locations rather than copied.

### Excluded and replaced artifacts

- `using-superpowers` is excluded: the native `using-coacus` entry workflow
  replaces it.
- `template-skill` is excluded by `exclude_skills`.
- The Superpowers workflows are kept but namespaced `superpowers-<name>` and
  moved to `methodology/workflows/`, so they can never collide with a
  skill name.

### Agent merges

The manifest declares three merges, mapping source agent names to a single
canonical target:

| Target | Sources | Outcome |
|---|---|---|
| `code-explorer` | `explore`, `code-researcher` | merged; both source charters concatenated, skills unioned |
| `security-architect` | `arquiteto-seguranca` | declared; source is in the excluded repo |
| `documenter` | `documentador` | declared; source is in the excluded repo |

A merge runs only when at least two of its declared sources are present in the
importable tree. `code-explorer` merged `explore` + `code-researcher`; the other
two had a single importable source, so they were imported as ordinary agents
from the `skills` repository. The merge declarations remain in the manifest for
when those sources become importable. The `code-explorer` merge records
`aliases: ["code-researcher"]` and `transform: [..., "merged:code-researcher"]`,
so the old name remains discoverable.

### Scripts and templates

`document_converter.py` and `document_analyzer.py` existed as byte-identical
copies across two repositories, and most templates did too
([ADR-0010](adr/ADR-0010-single-source-scripts-templates.md)). The import keeps
one copy: pipeline code under `verticals/architecture_si/`, shared templates
under `templates/domains/architecture_si/`.

## Provenance

Every imported file is recorded in `sources.lock.json` at the repository root
([ADR-0015](adr/ADR-0015-provenance-manifest-location.md)). It is deliberately
outside `catalog/`: provenance entries carry `imported_at`, and a timestamped
file inside the generated surface would make `coacus.py check` fail forever.

Entries are keyed for two purposes:

- **Dedup key** — `(source_repo, source_commit, source_path)`. Re-running `apply`
  replaces the entry for a target instead of duplicating it, so import is
  idempotent.
- **Drift key** — `target_sha256`. `engine/provenance.validate` checks that every
  recorded target still exists.

Each entry carries `source_repo`, `source_commit`, `source_path`,
`source_sha256`, `target_path`, `target_sha256`, `origin_license`, `transform`,
`import_run_id`, `imported_at`, and an optional `aliases` list. The F6 corpus
produced 1163 entries (1096 from `skills`, 67 from `superpowers`); 370 carry the
`translated` transform and 58 carry `converted:agent.source.md`. Imported files
whose content is still non-English carry `pending-translation` until the
translation pass clears it.

## Translation policy

The repository language is English ([ADR-0001](adr/ADR-0001-language-policy.md)).
Legacy PT-BR content was **translated at import, never copied verbatim**. The
`linguistic-specialist` agent performs the translation, under orchestrator
governance.

- The importer detects non-English content heuristically and tags it
  `pending-translation`; English files are tagged only `imported`.
- Translation replaces the tag with `translated` in `transform`.
- `engine/validators/language.py` and the skill warning pass flag remaining
  non-English prose. Fenced code blocks, inline code and link targets are
  excluded from the check, so quoted examples and identifiers do not trigger it.
- Four skills are explicitly exempt from the language warning because they
  intentionally contain non-English material: `linguistic-pt-br`,
  `documentation-designer`, `python-performance-parallelism` and `lang-rust`.

The warning remains non-blocking until completeness verification. F7/F8 close
the gap; `engine/validators/completeness.py` reconciles the source repositories,
the lock file and the catalog to prove nothing was left behind.

## Running the import

```bash
python3 scripts/coacus_import.py plan   # print action counts, write nothing
python3 scripts/coacus_import.py apply  # copy, record provenance, prune orphans
```

`apply` then prunes orphaned generated output (per-agent `.agents/entries/` and
`dist/` whose source no longer exists) and rewrites stale internal links. It
does not run `generate`; run `python3 scripts/coacus.py generate` afterwards and
commit the result.
