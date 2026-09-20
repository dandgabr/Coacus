# Generated Artifacts

**Status:** normative
**Scope:** `catalog/`, `.agents/`, every `dist/` folder,
`harnesses/<h>/bootstrap/`, and `docs/reference/python-api.md`.

## Catalog is generated from disk

The catalog — `catalog/catalog.json` (machine index) and `catalog/INDEX.md`
(human index) — is GENERATED from disk. Disk is the single truth. Manual catalog
editing is meaningless: it is overwritten on the next `generate`.

Contributors add canonical sources and run `generate`. They do not edit counts,
tables or entries by hand. Inherited inventory drift is reconciled by
regeneration, not by patching the catalog.

`catalog/catalog.json` carries a `counts` object. `python3 scripts/coacus.py
completeness` compares those counts against a fresh build from live disk and
reports any mismatch as a gap.

Prose is not exempt: the README corpus table and the LIVING documentation
(`README.md`, `CONTRIBUTING.md`, `evals/README.md`, `docs/architecture.md`,
`docs/usage.md`, `docs/install.md`, `docs/extending.md`, `docs/roadmap.md`,
`docs/standards/*.md`) state counts that the catalog and the lock already know.
`engine/validators/docs.py` reconciles every declared number against the measured
one during `validate`, so a hand-copied count that drifts is a build error (D5 —
counts are measured, never copied). Historical records are exempt by design:
`CHANGELOG.md` and `docs/migration.md` describe past states, and a paragraph that
marks its era ("as of F6") is not a current claim. Volatile numbers that have no
generator — the test count — are never stated as a fixed value; the docs give the
command to measure them instead.

## Generated artifacts are committed

Generated artifacts are committed to git. A harness consumes the repository as-is
(clone → activate); it does not build before use, and drift cannot hide until
runtime.

The drift check `python3 scripts/coacus.py check` compares disk against a fresh
in-memory regeneration and fails on any diff. Generated files contain no
timestamps, so regeneration is byte-idempotent and the check is deterministic.

CI runs `check` and NEVER `generate`. Regenerating in CI would rewrite the very
files under comparison. There is no CI auto-commit. Contributors must run
`generate` before committing.

## Generated surfaces

| Surface | Generator | Verified by |
|---|---|---|
| `agents/**/dist/{AGENT.md,agent.yaml,agent.json,plugin.json}` | `engine/generators/agent_manifests.py` | `check` + `engine/validators/agents.py` |
| `knowledge/mcps/**/dist/{mcp.json,mcp_config.json}` | `engine/generators/mcp_configs.py` | `check` + `engine/validators/mcps.py` |
| `harnesses/<h>/bootstrap/*` | `engine/generators/bootstrap.py` | `check` |
| `catalog/{catalog.json,INDEX.md}` | `engine/generators/catalog.py` | `check` + `completeness` |
| `.agents/{skills,mcps,agents}.json` + `.agents/entries/<name>.json` | `engine/generators/discovery.py` and `agent_manifests.py` | `check` + `engine/validators/discovery.py` |
| `docs/reference/python-api.md` | `engine/generators/docstrings.py` | `check` |

`python3 scripts/coacus.py generate` gates on SOURCE errors before writing:
invalid canonical sources never produce committed artifacts. It writes the
artifacts, then checks ARTIFACT errors (stale discovery fingerprints, provenance
targets) and exits non-zero if anything remains inconsistent.

## Rationale

Committing generated output costs larger diffs. Not committing it forces every
consumer to build before use and hides drift until runtime. The catalog generator
stays timestamp-free precisely so the committed artifact and the fresh
regeneration can be compared byte-for-byte.

`sources.lock.json` is deliberately OUTSIDE this surface: it carries
`imported_at` timestamps and would otherwise break idempotency. See
[`provenance.md`](provenance.md).

## Enforcement

- `python3 scripts/coacus.py check` runs every generator's `check()`
  (`agent_manifests`, `mcp_configs`, `bootstrap`, `discovery`, `catalog`,
  `docstrings`).
- `python3 scripts/coacus.py completeness` reconciles catalog counts, lock
  targets and orphan skills (`engine/validators/completeness.py`).
- `python3 scripts/coacus.py validate` reconciles the README corpus table against
  the catalog and the lock (`engine/validators/docs.py`,
  `tests/test_docs_counts.py`).
- `.github/workflows/ci.yml` runs both gates and never `generate`.
- `tests/test_idempotency.py` asserts `generate` twice produces an identical tree
  and that generated files contain no timestamps.
