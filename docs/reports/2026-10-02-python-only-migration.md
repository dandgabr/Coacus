# Python-only tooling migration and integration

Recorded: 2026-10-02. This is a historical implementation and verification
record. The integrated source baseline is
[`f7f464a`](https://github.com/dandgabr/Coacus/commit/f7f464abd5250641883c8c7941f1c9d3867b8fc1).
Current installation instructions live in [install.md](../install.md).

## Scope and outcome

The audit found operational Bash hooks and extensionless workflow helpers still
present after the initial portability changes. They were converted to Python
using the standard library and the repository's supported Python floor.
Only root `install.sh` and `install.ps1` remain as host Python/venv bootstraps.
OpenCode retains the JavaScript required by its native plugin API and invokes
Python for operational guardrail evaluation and governor commands.

The work implements [ADR 0007](../decisions/0007-cross-platform-os-independence.md)
and the [portability standard](../standards/secrets-portability.md).

## Implementation

### Bootstrap and lifecycle hooks

| Adapter | Activation | Operational hook implementation |
|---|---|---|
| OpenCode | In-process JavaScript bootstrap | Native adapters invoke Python guardrail and governor CLIs. |
| Claude Code | Generated SessionStart JSON staged in the Coacus plugin | Python SessionStart runner and direct Python guardrail command. |
| Antigravity | Generated rule packaged as a plugin | Central Python governor hook and direct Python guardrail command. |
| Codex | Generated SessionStart JSON in the repository | Python SessionStart runner and direct Python guardrail command. |
| Cursor | Generated SessionStart JSON in the repository | Python SessionStart runner and direct Python guardrail command. |
| Command Code | Generated SessionStart JSON in the repository | Python commands merged into harness settings. |

- Removed generated `session-start.sh`, `coacus-guard.sh` and
  `governor-hook.sh` wrappers. Changed their manifests and generators, then
  regenerated bootstrap outputs rather than maintaining separate sources.
- SessionStart parses JSON, resolves repository placeholders inside its values
  and serializes the native context safely, including the Codex skill-search path.
- Fixed the central Antigravity governor hook's ledger call to use `timeout`.
  Regression tests exercise acquisition, release and rate-limit parking.

### Workflow helpers and provenance

Converted helpers:

- `superpowers-subagent-driven-development/scripts/sdd-workspace.py`
- `superpowers-subagent-driven-development/scripts/task-brief.py`
- `superpowers-subagent-driven-development/scripts/review-package.py`
- `superpowers-executing-plans/scripts/task-start.py`
- `superpowers-executing-plans/scripts/task-done.py`

Workflow instructions and review prompts now invoke `.py` files. The helpers
resolve plan-specific workspaces, extract task briefs, package commit ranges,
print review bases and record completion after successful tests. The completion
helper retains raw child output and tolerates native encodings in displayed
summaries. Successful output under `cp1252` and failed tests that must leave no
completion entry are both covered.

The lock records `converted:python`, new target paths and refreshed target
hashes while retaining upstream source paths, commits and hashes. Reimports
preserve reviewed conversions when upstream hashes match; changed or missing
sources stop the import before any action is copied. Normalization includes
Python assets and rewrites helper commands idempotently. Provenance refresh
preserves upstream hashes on `converted:` and `adapted:` entries, including
entries whose original source and target hashes were equal.

### Installer and host portability

- Commands use the installation's interpreter rather than assuming `python3`
  exists on PATH. POSIX arguments are quoted before installation.
- Windows command arguments are encoded as base64 JSON and decoded by a Python
  shim to avoid shell expansion in repository paths. Unsupported expansion
  characters in interpreter paths are rejected before installation.
- JavaScript adapters receive paths as escaped JavaScript string literals.
- Reinstallation retires only manifest-owned legacy wrappers and helpers,
  normalizes Windows separators and preserves unowned user files.
- Skill installation excludes Python bytecode and `__pycache__` directories.
- Verification checks every expected Coacus hook entry in merged configuration;
  one remaining guardrail cannot hide a missing bootstrap entry.
- The root installers now install before verifying via `--verify-after-install`.
  Undetected harnesses are skipped. The PowerShell bootstrap propagates venv,
  generation and installation failures.
- The Codex compact native profile and bootstrap context limit were preserved
  while stacking the migration over the preceding catalog correction.

### Validation, review and CI

- Hygiene validation rejects operational shell extensions and shell shebangs,
  including extensionless helpers and generated hook directories.
- `scripts/coacus_secrets.py` replaces CI's inline shell downloader. It selects
  the host's publisher binary, verifies its pinned checksum and extracts only
  the executable before scanning with redaction.
- Linux/macOS/Windows CI checks portable hook and workflow contracts at the
  supported Python floor.
- Independent review and the Windows CI run exposed command quoting, native
  child-output encoding, provenance refresh and manifest-separator defects.
  Corrections were verified by regressions or the previously failing Windows job.
- Bandit reported the generated-command shell fixture and the fixed HTTPS
  scanner download. The call sites document targeted `B602`/`B310` suppressions;
  the security workflows subsequently passed.

## Integration history

| Change | Integration |
|---|---|
| Compact Codex catalog and on-demand search | [PR #60](https://github.com/dandgabr/Coacus/pull/60), based on `main`. |
| Python migration and Windows manifest correction | [PR #61](https://github.com/dandgabr/Coacus/pull/61), merged into the PR #60 branch. |
| Targeted Bandit annotations | Commit `b808aaa` on the PR #60 branch. |
| Combined result | PR #60 merged into `main` as `f7f464a`. |

After the approved merge, the checkout switched to `main` and advanced by
fast-forward to remote `main`. The following commands confirmed an identical
commit, divergence `0 0` and no local changes at the end of integration:

```text
git rev-parse main origin/main
git rev-list --left-right --count main...origin/main
git status --porcelain
```

## Verification evidence

These commands passed on the integrated checkout using the project venv:

```bash
.venv/bin/python scripts/coacus.py validate
.venv/bin/python scripts/coacus.py check
.venv/bin/python scripts/coacus.py completeness
.venv/bin/python -m unittest discover -s tests
```

Observed outputs were `validation OK`,
`no drift: generated artifacts are up to date`,
`completeness OK: nothing left behind` and a successful complete test run.
Run the test command to obtain the current test count.

CI, secrets and portable-hook jobs passed. Linux, macOS and Windows smoke
contracts passed. CodeQL language analyses and Bandit checks on the integration
branch passed. The main CI run is
[`37017920596`](https://github.com/dandgabr/Coacus/actions/runs/37017920596).

### Harness verification

| Adapter | Existing installation refreshed and verified | Isolated install and drift check | SessionStart exercise |
|---|---|---|---|
| OpenCode | `ok: true` | Passed | Native plugin contract tested in the suite. |
| Claude Code | No existing local installation | Passed | JSON command passed. |
| Antigravity | `ok: true` | Passed | Rule activation; Python governor contract tested in the suite. |
| Codex | `ok: true`; compact profile preserved | Passed | JSON command passed, including the installed local command. |
| Cursor | No existing local installation | Passed | JSON command passed. |
| Command Code | `ok: true` | Passed | JSON command passed. |

Existing installations had empty `missing`, `drifted` and `extra_in_manifest`
arrays after refresh. They were verified again after cache cleanup. All adapters
were also installed in temporary configuration directories; their planned files
contained no `.sh` files.

These results cover installer output, drift, payload execution and tested runtime
contracts. They do not assert live end-to-end sessions for every vendor
application. Claude Code and Cursor used isolated installations because they
were not installed locally.

## Authorized local cleanup

The inventory found no `.sh` files in installed Coacus artifacts. Remaining files
belonged to harness snapshots, historical projects or third-party plugin caches.
The user selected removal of cache/history residues while preserving plugins.

Seven historical `.sh` files were removed: three Codex shell snapshots, three
Antigravity GTK/Flatpak theme helpers and a dictionary-maintenance helper in an
Antigravity scratch venv. Cleanup scopes were `~/.codex/shell_snapshots/` and
`~/.gemini/antigravity-cli/brain/`; plugin and skill directories were excluded.
No `.sh` files remained in the cleaned scopes. Third-party plugin scripts were
preserved, and the four existing Coacus installations still reported `ok: true`
after cleanup. This was a local operation; it did not add cache/history deletion
to the installer or suppress future snapshots created by a harness.
