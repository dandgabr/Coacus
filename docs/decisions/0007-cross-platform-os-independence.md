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

## Consequences

- **Positive**: Coacus installs and runs seamlessly on Windows without requiring WSL,
  Cygwin, or Git Bash on the system PATH.
- **Positive**: IDE hook execution (such as Antigravity `hooks.json`) runs cleanly via
  `python "<path>"` without popup consoles or shell syntax incompatibilities.
- **Positive**: One consistent execution model and debugging story across all operating
  systems.
- **Neutral**: Hook execution requires Python on the host PATH (which is already a base
  requirement of Coacus).
