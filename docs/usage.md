# Usage

Every command below was verified against the scripts in `scripts/`. Run them
from the repository root. Python 3.14 is the CI target; the stdlib is the only
dependency for the core tooling.

## Build and verify

```bash
python3 scripts/coacus.py generate   # regenerate dist/, harnesses/<h>/bootstrap/, .agents/ and catalog/
python3 scripts/coacus.py check      # fail if generated artifacts are stale
python3 scripts/coacus.py validate   # run source + artifact validators
python3 -m unittest discover -s tests  # deterministic suite (206 tests)
```

`generate` gates on **source** errors: invalid canonical sources never produce
artifacts. It then writes the generated files and checks the **artifact**
outputs. If artifacts remain inconsistent after writing, it exits non-zero.
Non-blocking warnings (language markers, oversized descriptions) print as
`[warn]`.

`check` compares disk against a fresh in-memory regeneration and exits 1 on any
diff. It never writes. Generated files carry no timestamps, so the check is
deterministic.

`validate` runs source and artifact validators together and prints warnings
first.

### Validate a TOON payload

```bash
python3 scripts/coacus.py toon path/to/payload.toon
```

The validator enforces required fields, the `@STATUS` enum
(`OK | CONFLICT | BLOCKED | NEED_INFO`), relative `@FILES` paths and rejects
secret-shaped literals in any field.

## Install into a harness

Rendered artifacts are committed; installing them is a separate, explicit step.

```bash
python3 scripts/coacus_install.py opencode
python3 scripts/coacus_install.py all
python3 scripts/coacus_install.py opencode --dry-run     # preview targets
python3 scripts/coacus_install.py opencode --uninstall   # remove a previous install
python3 scripts/coacus_install.py opencode --config-dir /tmp/oc  # test location
python3 scripts/coacus_install.py codex --only security,engineering  # partial install
python3 scripts/coacus_install.py codex --skills 'lang-*'
python3 scripts/coacus_install.py --list                 # categories and skill names
```

Run `generate` first. The installer writes a `coacus-install.json` manifest next
to each target, so re-runs are idempotent and `--uninstall` removes exactly what
was installed. All five harnesses install (`opencode`, `claude-code`,
`antigravity`, `codex`, `cursor`), or `all` for every one of them. `--only`
filters by category (top-level or nested segment; `workflows` for the process
collection) and `--skills` by name glob; both are comma-separated and AND-ed.

Per-harness behavior and manual paths are in [`install.md`](install.md).

## Governor

Bound concurrent subagents and handle rate limits.

```bash
python3 scripts/coacus_governor.py acquire <caller> [orchestrator-yes|no] [timeout-secs] [max-total]
python3 scripts/coacus_governor.py release <caller>
python3 scripts/coacus_governor.py fail    <caller>   # mark a caller that hit a rate limit
python3 scripts/coacus_governor.py paused             # backoff hints for parked callers
python3 scripts/coacus_governor.py status [max-total] # running/paused/max/slots_free
python3 scripts/coacus_governor.py health             # ledger dir + lock + cap
python3 scripts/coacus_governor.py reset
```

`acquire` prints the token and exits 0 on success, or prints nothing and exits 1
when the cap stayed saturated past the timeout. The default cap is 5, orchestrator
included. Knobs: `ORCH_MAX_CONCURRENT`, `GOVERNOR_STATE_DIR`,
`GOVERNOR_LEASE_SECONDS`. See [orchestration-governance](standards/orchestration-governance.md).

`status` example output:

```text
running=0 paused=0 max=5 orchestrator=false slots_free=5
```

## Behavior evals

Two tiers ([testing](standards/testing.md)). Static is
deterministic and blocking; live needs a harness CLI and credentials and never
runs in CI.

```bash
python3 scripts/coacus_eval.py validate                 # static scenario gate
python3 scripts/coacus_eval.py run --scenario bootstrap-activation
python3 scripts/coacus_eval.py run --judge-cmd "my-judge"
python3 scripts/coacus_eval.py run --judge-agent
```

`run` drives the scenario's harness CLI, applies deterministic checks
(`contains`, `not_contains`, `regex`) and passes the `rubric` to the judge.
`--judge-cmd` receives `{"scenario": ..., "transcript": ...}` as JSON on stdin
and must print a verdict line. `--judge-agent` routes the rubric through the
same harness as a subagent. Transcripts are redacted by default; set
`COACUS_EVAL_VERBOSE=1` for a bounded local excerpt. The four seeded scenarios
and the scenario schema are documented in [`../evals/README.md`](../evals/README.md).

## architecture_si vertical

Document ingestion and analysis over one dispatcher
([knowledge-ingestion](standards/knowledge-ingestion.md)).

```bash
python3 scripts/coacus_vertical.py formats
python3 scripts/coacus_vertical.py ingest report.pdf
python3 scripts/coacus_vertical.py ingest report.pdf out.md
python3 scripts/coacus_vertical.py ingest --dir docs/ --toc-only
python3 scripts/coacus_vertical.py ingest --dir docs/ --split-chapters
python3 scripts/coacus_vertical.py analyze out.md
python3 scripts/coacus_vertical.py analyze --dir docs/ --json
```

`formats` lists the registered extensions: `.csv .doc .docx .htm .html .json
.log .pdf .ppt .pptx .rtf .tsv .txt .yaml .yml`. `ingest` writes Markdown next
to the input when no output path is given. `analyze` prints a human report or,
with `--json`, a stable JSON structure (outline, metrics, diagram/table counts,
security keyword hits).

## Corpus import

The F6 importer is driven by `templates/import/import-manifest.json` and records
provenance in `sources.lock.json` ([provenance](standards/provenance.md)).

```bash
python3 scripts/coacus_import.py plan  [--source skills|superpowers|agents]
python3 scripts/coacus_import.py apply [--source skills|superpowers|agents]
```

`plan` writes nothing and prints action counts. `apply` copies, refreshes
provenance and prunes orphaned generated output. Re-running is idempotent: the
dedup key is `(source_repo, source_commit, source_path)`. See
[`migration.md`](migration.md).

## Full local gate

The same sequence CI runs:

```bash
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 -m unittest discover -s tests
```

CI (`ci` job) runs these three and never runs `generate`. The `secrets` job runs
gitleaks against the checked-out state. Both are required by the `main` ruleset.
