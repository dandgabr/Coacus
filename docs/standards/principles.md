# Principles

**Status:** normative
**Scope:** the whole repository. These principles hold for every artifact, every
generator and every contribution.

## Core principle

> **Disk is the truth; generation is the contract.**

Every canonical artifact has exactly one source on disk. Every derived
representation is computed from that source by the engine and verified by a drift
check. A generated file that does not match a fresh regeneration is a build
error, never silent debt. No one hand-maintains a derived file, and no derived
file is treated as the source of a fact that already lives elsewhere.

Consequences that follow directly:

- A change lands in one canonical source and the derived output follows from
  `python3 scripts/coacus.py generate`.
- CI runs `python3 scripts/coacus.py check`, never `generate`. Regenerating in CI
  would rewrite the files under comparison and mask the drift it exists to catch.
- Generated files carry no timestamps, so regeneration is byte-idempotent and the
  check is deterministic.

## Principles in detail

### P1 — Sources are read-only

The import pipeline copies from a source repository. It never writes to, renames
inside, or deletes from a source repository. A source working tree is read once
and left untouched.

### P2 — Import adapts, autonomously

Import copies and adapts material into the repository's own taxonomy. Symlinks
are forbidden: every artifact is a real file whose bytes this repository owns.
Nothing at runtime reaches back into a foreign checkout. The framework is
autonomous — no path in a tracked file may depend on a machine outside this
repository.

### P3 — Changes ship through review

Work proceeds phase by phase, and each phase is authorized before it starts.
Structural change lands through a pull request that carries its generated diffs
for review. No commit rewrites a canonical structure without a reviewable diff.

### P4 — Every imported artifact carries provenance

Every imported file is recorded in `sources.lock.json` at the repository root with
its source repository, commit, path, content hash, target path, target hash,
origin license, applied transform, import run id and import timestamp. An
imported artifact without a provenance entry is an incomplete import, not a
supported state.

## Rationale

Each principle closes a failure the source repositories actually suffered:
hand-maintained copies that drift, symlinks that bind a checkout to a colleague's
disk, unreviewed structural edits, and imports with no recorded origin so dedup
and drift could not be audited. The core principle is the mechanism; the four
principles are the constraints it operates under.

## Enforcement

- The core principle and P4: `python3 scripts/coacus.py check` (drift),
  `engine/validators/completeness.py` (via `python3 scripts/coacus.py
  completeness`) reconciles sources, `sources.lock.json` and the catalog, and
  `engine/provenance.py` validates the lock schema and target existence.
- P2's no-absolute-paths rule: `engine/validators/hygiene.py` rejects
  machine-specific paths during `validate`.
- P3: the PR flow in [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) and the
  required `ci` and `secrets` checks in `.github/workflows/ci.yml`.
- CI: `.github/workflows/ci.yml` runs `validate` → `check` → `completeness` →
  tests.
