#!/usr/bin/env python3
"""Extract one numbered task from a Markdown implementation plan."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

def _workspace(plan: Path) -> Path:
    script = Path(__file__).with_name("sdd-workspace.py")
    return Path(subprocess.check_output([sys.executable, str(script), str(plan)], text=True).strip())


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (2, 3) or not args[1].isdigit():
        print("usage: task-brief.py PLAN_FILE TASK_NUMBER [OUTFILE]", file=sys.stderr)
        return 2
    plan, number = Path(args[0]), args[1]
    try:
        lines = plan.read_text(encoding="utf-8").splitlines(keepends=True)
        out = Path(args[2]) if len(args) == 3 else _workspace(plan) / f"task-{number}-brief.md"
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(exc, file=sys.stderr)
        return 2
    heading = re.compile(r"^#+\s+Task\s+(\d+)(?:\D|$)")
    inside, fence = False, False
    selected: list[str] = []
    for line in lines:
        if line.startswith("```"):
            fence = not fence
        match = heading.match(line) if not fence else None
        if match:
            inside = match.group(1) == number
        if inside:
            selected.append(line)
    if not selected:
        print(f"task {number} not found in {plan}", file=sys.stderr)
        return 3
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(selected), encoding="utf-8")
    print(f"wrote {out}: {len(selected)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
