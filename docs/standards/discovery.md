# Discovery

**Status:** normative
**Scope:** every agent session operating in this repository, and the generated
manifests under `.agents/`.

## Rule

Discovery is static and deterministic. Manifests under `.agents/` are GENERATED
from disk and drift-checked; agents read them once per session and never re-scan
directories per turn.

### Single-scan rule

At session start, read the generated indexes ONCE:

- `.agents/skills.json`, `.agents/mcps.json`, `.agents/agents.json` — consolidated
  by-kind indexes, each `{entries: [{path}]}`.
- `.agents/routing.json` — the routing index (`routing`), which merges each
  agent's canonical facts with the curated bilingual triggers so the router
  (`engine/router.py`) selects agents without re-scanning the tree.
- `.agents/entries/<name>.json` — per-agent entries
  `{name, description, category, source, dist, fingerprint}`.

After that, rely on session memory. Re-running `find`, recursive `ls` or a fresh
directory walk to rediscover assets on every turn is prohibited. Re-scan only
when the user states that an agent or skill was added or changed during the
session.

### Manifest contract

- Per-agent entries MUST carry every key, and the file stem MUST equal the entry
  `name`.
- `source` and `dist` MUST be relative in-repo paths. Absolute, empty or
  upward-escaping paths are rejected.
- The `fingerprint` is RECOMPUTED from the source bytes (sha256, first 16 hex
  characters). A tampered or stale entry fails even before the drift check, and
  regeneration is what fixes it.
- Every `source` MUST exist and every `dist` MUST be a directory.

The `entries/` subdirectory keeps agent names from colliding with the consolidated
stems.

### Escape hatch

Move to a database-backed index only if the inventory grows past a few hundred
assets or semantic search becomes a requirement. Until then the static manifests
are the contract.

## Rationale

Discovery has to be deterministic and cheap. A model that re-walks the tree every
turn spends context and latency to rediscover facts it already read, and two
scans can disagree. Generated manifests with recomputed fingerprints make the
index verifiable and make staleness a build error.

## Enforcement

- `engine/validators/discovery.py` (via `python3 scripts/coacus.py validate` and
  after writing in `generate`) checks per-agent keys, stem/name equality, safe
  relative paths, source existence, dist existence and the recomputed fingerprint.
- `engine/generators/discovery.py` writes the consolidated manifests;
  `python3 scripts/coacus.py check` fails on drift.
- `AGENTS.md` states the single-scan rule for every agent in the repository.
- `tests/test_discovery.py` and `tests/test_discovery_provenance.py` cover the
  contracts.
