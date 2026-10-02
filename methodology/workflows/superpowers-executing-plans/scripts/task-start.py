#!/usr/bin/env python3
"""Write a task brief and print the current commit as its review base."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: task-start.py PLAN_FILE TASK_NUMBER", file=sys.stderr)
        return 2
    brief = Path(__file__).resolve().parents[2] / "superpowers-subagent-driven-development/scripts/task-brief.py"
    result = subprocess.run([sys.executable, str(brief), *args], capture_output=True, text=True)
    if result.returncode:
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    output = result.stdout.strip()
    if not output.startswith("wrote ") or ": " not in output:
        print(f"task-brief did not report a path: {output}", file=sys.stderr)
        return 1
    print("brief: " + output[6:].rsplit(": ", 1)[0])
    try:
        print("base: " + subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip())
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
