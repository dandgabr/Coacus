# 0007. Cross-Platform OS Independence and Python-Exclusive Scripting

Date: 2026-10-01

## Status

accepted

## Context

Coacus is designed to run across multiple AI coding harnesses (OpenCode, Claude Code,
Antigravity, Codex, Cursor, Command Code) and across heterogeneous operating systems
(Windows, Linux, macOS).

Historically, harness hook wrappers and some workflow utilities relied on bash shell
scripts (`.sh`), such as `governor-hook.sh`, `coacus-guard.sh`, and `session-start.sh`.
On Windows environments—especially inside the Google Antigravity IDE and modern Windows
terminals running PowerShell or Command Prompt (`cmd.exe`)—these bash scripts failed to
execute directly or spawned unwanted external shell console windows via process creation,
breaking the automated developer experience.

## Decision

1. **Python 3.10+ Standard Library Only**: All framework runtime hooks, background
   scripts, generators, CLI tools, and workflow utilities MUST be authored in pure
   Python (version 3.10+, stdlib only, zero external runtime dependencies).
2. **Deprecation of Shell Wrappers**: All hook wrappers (`governor-hook.sh`,
   `coacus-guard.sh`, `session-start.sh`) are replaced by direct Python scripts
   (`scripts/coacus_governor_hook.py`, `scripts/coacus_session_start.py`, and direct
   invocations of `scripts/coacus_guard.py`).
3. **Cross-Platform Host Bootstrap Exception**: Two single-purpose host bootstrappers
   are maintained at the root: `install.sh` for POSIX systems (Linux/macOS) and
   `install.ps1` for Windows. Their sole responsibility is verifying Python 3.10+
   availability, bootstrapping a virtual environment (`.venv`), and executing Coacus
   generators and installers.
4. **Portability Rule**: Convention 9 in `AGENTS.md` and `docs/standards/secrets-portability.md`
   forbid authoring new `.sh`, `.bash`, `.cmd`, or `.ps1` files for framework logic.
5. **Native Plugin Adapters**: OpenCode retains the JavaScript required by its
   in-process plugin API. It delegates operational evaluation and governor
   commands to Python without introducing shell wrappers.

## Consequences

- Hook tooling has no Bash, WSL or Git Bash runtime dependency. Linux, macOS and
  Windows CI check portable hook and workflow contracts.
- The installer records its interpreter and quotes commands for the host. The
  interpreter and repository must remain available; moving either requires
  reinstallation.
- SessionStart emits generated JSON with repository paths resolved. Lifecycle
  evaluators and governor operations share Python tooling.

## Implementation record — 2026-10-02

PRs #60/#61 completed the migration and were integrated into `main` as `f7f464a`.
The [implementation report](../reports/2026-10-02-python-only-migration.md) records
converted scripts, regression fixes, portability CI, local verification and the
separately authorized cache/history cleanup.

## Alternatives considered

- Requiring Bash or a POSIX compatibility layer would retain a host dependency
  for ordinary hooks and workflow operations.
- Shell wrappers around Python would duplicate quoting and installation
  behavior across operating systems.
- A standalone Python process would not implement OpenCode's in-process
  JavaScript plugin interface.
