# Usage

Every command below was verified against the scripts in `scripts/`. Run them
from the repository root. Python 3.10+ is supported (Python 3.14 is the CI target);
the stdlib is the only dependency for the core tooling.

## 🌟 1-Click Universal Bootstrap (Recommended)

Bootstrap Python, the virtual environment, artifact generation, and verified installation:

```bash
# Linux / macOS
./install.sh [harness|all]

# Windows (PowerShell)
.\install.ps1 [harness|all]
```

## Build and verify

```bash
python3 scripts/coacus.py generate   # regenerate dist/, harnesses/<h>/bootstrap/, .agents/ and catalog/
python3 scripts/coacus.py check      # fail if generated artifacts are stale
python3 scripts/coacus.py validate   # run source + artifact validators
python3 -m unittest discover -s tests  # deterministic suite
```

`generate` gates on **source** errors: invalid canonical sources never produce
artifacts. It also records a provenance entry for every authored skill, workflow
and agent ([provenance](standards/provenance.md)); the write is idempotent. It
then writes the generated files and checks the **artifact** outputs. If artifacts
remain inconsistent after writing, it exits non-zero. Non-blocking warnings
(language markers, oversized descriptions) print as `[warn]`.

`check` compares disk against a fresh in-memory regeneration and exits 1 on any
diff. It never writes. Generated files carry no timestamps, so the check is
deterministic.

`validate` runs source and artifact validators together and prints warnings
first. A moving version pin with no resolution anchor is an **error**
([version-freshness](standards/version-freshness.md)), so the gate blocks a
training-memory pin from entering the corpus. A provenance target whose recorded
hash no longer matches disk is also an error: the lock must not lie about the
corpus ([provenance](standards/provenance.md)).

### Evidence in process workflows

The process skills require a claim to name the exact manifest or artifact copy
that supplied its evidence. A summary such as `0 entries` does not distinguish
absence from an unreachable, locked or differently scoped store; read the exact
error or result before concluding that something is absent. Delegated reviews
identify the path the worker read and carry its evidence back to the caller.

Plan snippets describe intent at the time of writing. After an interface
changes, check the current definition and correct later references in both code
and the plan. The compiler or repository validation gate checks those references.

Credential metadata inspection requires the user's authorization. Read key
names, types or lengths without exposing values. Redact captured output before
printing it and test that redaction with synthetic data. The entry skill carries
these rules into generated harness bootstraps.

### Repair drifted provenance

```bash
python3 scripts/coacus.py refresh   # re-hash drifted targets in sources.lock.json
```

`refresh` recomputes `target_sha256` from disk for every entry whose recorded
hash drifted (editing an imported file without re-running the importer). It is
idempotent, verifies the result and exits non-zero if any error remains.

### Audit version pins

```bash
python3 scripts/coacus.py freshness            # read-only inventory of moving pins
python3 scripts/coacus.py freshness --references  # also scan references/ assets
```

The command is offline and deterministic: it lists every moving release pin with
`resolved` or `UNRESOLVED`, exits 1 if any pin is unresolved, and never fetches
the network. Resolution itself follows the
[version-freshness](standards/version-freshness.md) standard.

### Find a canonical skill

Search the generated skill catalog or resolve a known entry by its exact name:

```text
python3 scripts/coacus_skill_search.py search "session coordination" --top 3
python3 scripts/coacus_skill_search.py show gnome-shell-extension-development
```

Search matches canonical names and descriptions; it does not search reference
contents. Read the selected skill and follow its pointers for branch-specific
guidance. The [desktop extension reference map](reference/desktop-extension-practices.md)
provides task-based entry points for preferences, accounts, themes, and updates.

### Select agents (routing)

```bash
python3 scripts/coacus_route.py "<prompt>" --top 4 --max-slots   # Mode A: automated
python3 scripts/coacus_route.py --list --category cybersecurity # Mode M: browse
python3 scripts/coacus_route.py --agents mobile-security-specialist,dba-specialist  # Mode M: validate
```

Mode A ranks the agents for a prompt from the generated routing index
(`.agents/routing.json`) and is offline and deterministic; `--max-slots` caps the
proposal at the governor's free slots. Mode M browses or validates an explicit
selection — an unknown name is an error with suggestions. `--rerank "<command>"`
plugs in an optional semantic reranker behind the same interface and fails open.
See [routing](standards/routing.md) and the
[tutorials](tutorials/) for a guided walkthrough of each mode.

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
python3 scripts/coacus_install.py all --verify-after-install # install, then verify detected harnesses
python3 scripts/coacus_install.py opencode --dry-run     # preview targets
python3 scripts/coacus_install.py opencode --uninstall   # remove a previous install
python3 scripts/coacus_install.py opencode --config-dir /tmp/oc  # test location
python3 scripts/coacus_install.py codex --only security,engineering  # partial install
python3 scripts/coacus_install.py codex --skills 'lang-*'
python3 scripts/coacus_install.py codex --agents 'qa-*'   # filter agents only
python3 scripts/coacus_install.py --list                 # categories and skill names
python3 scripts/coacus_install.py antigravity --verify   # read-only: counts + drift, exit non-zero on mismatch
```

Run `generate` first. The installer writes a `coacus-install.json` manifest next
to each target, so re-runs are idempotent and `--uninstall` removes exactly what
was installed. Supported adapters are `opencode`, `claude-code`, `antigravity`,
`codex`, `cursor` and `command-code`; `all` installs those detected on the host.
`--only` filters by category (top-level or nested segment; `workflows` for
the process collection) across **both** skills and agents; `--skills` and
`--agents` narrow one tree each by name glob. All are comma-separated and
AND-ed.

`--verify` is read-only; `--verify-after-install` performs installation first.
An `all --verify` run also checks absent installations and fails when a manifest
is missing. To verify an existing installation, select its harness and use the
interpreter that installed it. The root bootstrap scripts use the project venv:
`.venv/bin/python` on Linux/macOS and `.venv\Scripts\python.exe` on Windows.

Operational hooks call Python directly. SessionStart reads generated JSON and
resolves repository placeholders before emitting native context. OpenCode uses
JavaScript for the vendor plugin interface and delegates runtime evaluation and
governor operations to Python. Only root `install.sh` and `install.ps1` remain
as host bootstrap scripts. See the
[upgrade procedure](install.md#upgrading-a-legacy-shell-installation).

### Workflow helpers

Run helpers from the target project's checkout and invoke them through their
resolved workflow skill paths. The helper paths below are relative to each
skill directory; resolve `PLAN_FILE` relative to the project checkout, and use
`TASK_NUMBER` to identify its numbered task. Test commands are an argument list
after `--`; the helper does not interpret shell pipelines or variable expansion.

| Workflow | Python helper | Purpose |
|---|---|---|
| `superpowers-subagent-driven-development` | `scripts/sdd-workspace.py PLAN_FILE` | Resolve a plan-specific workspace. |
| `superpowers-subagent-driven-development` | `scripts/task-brief.py PLAN_FILE TASK_NUMBER [OUTFILE]` | Extract a task brief. |
| `superpowers-subagent-driven-development` | `scripts/review-package.py PLAN_FILE BASE HEAD [OUTFILE]` | Package a nonempty descendant commit range. |
| `superpowers-executing-plans` | `scripts/task-start.py PLAN_FILE TASK_NUMBER` | Print the brief path and review base. |
| `superpowers-executing-plans` | `scripts/task-done.py PLAN_FILE TASK_NUMBER BASE -- TEST_COMMAND [ARGS...]` | Record completion only after successful tests. |

Prefix each resolved helper path with the Python interpreter command. The original test output
is retained in the task log; its displayed summary tolerates undecodable bytes
and redirected output using a native Windows encoding.
Workspace and commit-review operations require the Git CLI on PATH.

### Secret scan

```bash
python3 scripts/coacus_secrets.py
```

The runner downloads the host's pinned scanner binary, checks its publisher
checksum, extracts only the executable, and scans the checkout with redacted
matches. The download requires network access. The tooling uses the standard
library; the scanner is an external executable supplied by its publisher.

`command-code` differs from the hook harnesses: it merges its `SessionStart`
entry into `~/.commandcode/settings.json` (Command Code keeps hooks there, not in
a `hooks.json`), merges the `context7` server into `~/.commandcode/mcp.json`, and
writes its user rules to `~/.commandcode/AGENTS.md` only when that file does not
yet exist. It shares the `~/.agents/skills/` tree with Codex and Cursor.

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
`COACUS_EVAL_VERBOSE=1` for a bounded local excerpt. The six seeded scenarios
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

## Guardrails (PAER)

Policies are authored once in `methodology/lifecycle/policies/*.policy.json` and
are active only when the file declares `"enabled": true` (the default set is empty
and disabled — [ADR 0006](decisions/0006-default-policy-posture.md)). A harness's
capability to enforce each event is data in `harness.json.lifecycle`; the matrix in
`docs/reference/lifecycle-matrix.md` is generated from it.

```bash
# Evaluate one event against the active policies (native effect JSON on stdout):
echo '{"tool":"read","tool_input":{"filePath":"repo/.env"}}' \
  | python3 scripts/coacus_guard.py --harness claude-code --event tool.pre

# Install refuses a deny the harness cannot block; --allow-advisory records the downgrade:
python3 scripts/coacus_install.py claude-code
python3 scripts/coacus_install.py claude-code --allow-advisory
```

See [`lifecycle-guardrails`](standards/lifecycle-guardrails.md). The generated
hook shell scripts are executed directly by `tests/test_guardrail_scripts.py`.

## Self-improvement (opt-in)

The end-of-session loop is opt-in and fail-open; it PROPOSES and never applies
([ADR 0005](decisions/0005-part-b-boundary-and-one-way-interface.md)). It is never
called from `generate`/`check`/CI.

```bash
python3 scripts/coacus_improve.py status           # episodic source availability
python3 scripts/coacus_improve.py run --transcript session.jsonl
```

The `transcript` source is the portable default; `ai-memory` is optional and its
absence by configuration is a safe no-op. See
[`self-improvement-loop`](standards/self-improvement-loop.md).

## Full local gate

The same sequence CI runs:

```bash
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 scripts/coacus.py completeness
python3 -m unittest discover -s tests
```

CI (`ci` job) runs these four and never runs `generate`. The `secrets` job runs
gitleaks against the checked-out state. Both are required by the `main` ruleset.
