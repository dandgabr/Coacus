# ADR 0019: Run every hook script with `python -I`

* **Status**: accepted
* **Date**: 2026-11-19
* **Tags**: guardrails, hooks, hardening

## Context

A hook starts from the project the agent works in. With a plain `python script.py` the
script directory, not the working directory, leads `sys.path`, but with `python -c` (the
Windows form and the launcher of ADR 0016) the working directory leads it, and any
`PYTHONPATH` or user site is read in both. A file named like a standard module in an
untrusted project could then run inside the guard. A review of the launcher found this.

## Decision

- The installer inserts `-I` after the interpreter of every hook command that runs one of
  our scripts (the template word `__COACUS_PYTHON__`), in `_hook_substitute`. The Windows
  shim and the optional launcher carry it too, and the OpenCode plugins pass it in their
  argument lists.
- The scripts already put the repository root on `sys.path` themselves, which `-I`
  needs; a test runs the session-start hook and the guard from a directory holding a
  planted `json.py`.
- A command that already starts with a flag is left alone. `_entry_owned` reads past the
  flag, so an entry from an earlier install is still recognised and replaced.

## Consequences

- A hook installed before this change runs without `-I` until the installer runs again.
- `-I` also ignores `PYTHON*` variables and the user site. No Coacus script relies on them.
- It does not stop a hostile project from placing a file the guard imports by path, which
  the self-protection policy of ADR 0015 addresses.

## Alternatives considered

- Clearing `sys.path[0]` inside each script: it runs after the imports that matter.
- `-P` alone: Python 3.11 and later only, and it leaves the user site and `PYTHON*` set.
