#!/usr/bin/env python3
"""Run a task's test command and record successful completion."""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Execute the test argv and append the ledger only on success."""
    sys.stdout.reconfigure(errors="backslashreplace")
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 5 or args[3] != "--":
        print("usage: task-done.py PLAN_FILE TASK_NUMBER BASE -- TEST_COMMAND [ARGS...]", file=sys.stderr)
        return 2
    plan, number, base = Path(args[0]), args[1], args[2]
    command = args[4:]
    if subprocess.run(["git", "rev-parse", "--verify", "--quiet", base], capture_output=True).returncode:
        print(f"bad BASE: {base}", file=sys.stderr)
        return 2
    workspace_script = Path(__file__).resolve().parents[2] / "superpowers-subagent-driven-development/scripts/sdd-workspace.py"
    workspace = subprocess.run([sys.executable, str(workspace_script), str(plan)], capture_output=True, text=True)
    if workspace.returncode:
        print(workspace.stderr, end="", file=sys.stderr)
        return workspace.returncode
    directory = Path(workspace.stdout.strip())
    log = directory / f"task-{number}-tests.log"
    with log.open("w", encoding="utf-8") as stream:
        try:
            status = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT).returncode
        except OSError as exc:
            stream.write(str(exc) + "\n")
            status = 127
    # A child writes bytes directly to the log descriptor, potentially using a
    # native encoding. Preserve the raw log and tolerate undecodable summaries.
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    print("\n".join(lines[-5:]))
    if status:
        print(f"task-done: test command exited {status}; Task {number} NOT recorded (full output: {log})", file=sys.stderr)
        return status
    short_base = subprocess.check_output(["git", "rev-parse", "--short=7", base], text=True).strip()
    short_head = subprocess.check_output(["git", "rev-parse", "--short=7", "HEAD"], text=True).strip()
    ledger = directory / "progress.md"
    if not ledger.exists():
        ledger.write_text(f"# SDD ledger — plan: {plan}\n", encoding="utf-8")
    line = f"Task {number}: complete (commits {short_base}..{short_head}, tests: {shlex.join(command)} -> {next((line for line in reversed(lines) if line.strip()), '')})"
    with ledger.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
    print("ledger: " + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
