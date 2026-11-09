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
        with plan.open(encoding="utf-8", newline="") as source:
            lines = source.readlines()
        out = Path(args[2]) if len(args) == 3 else _workspace(plan) / f"task-{number}-brief.md"
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(exc, file=sys.stderr)
        return 2
    heading = re.compile(r"^#+\s+Task\s+(\d+)(?:\D|$)")
    inside, fence, past_header = False, False, False
    context_depth = 0
    spec_paragraph = False
    context: list[str] = []
    selected: list[str] = []
    for line in lines:
        if line.startswith("```"):
            fence = not fence
        match = heading.match(line) if not fence else None
        if match:
            past_header = True
            inside = match.group(1) == number
        if not past_header:
            section = re.match(r"^(#+)[ \t]+(.+?)[ \t]*\r?\n?$", line) if not fence else None
            if section:
                depth = len(section.group(1))
                if context_depth and depth <= context_depth:
                    context_depth = 0
                title = re.sub(r"[ \t]+#+[ \t]*$", "", section.group(2)).strip()
                if not context_depth and title in ("Global Constraints", "Review Focus"):
                    context_depth = depth
            if not fence and line.startswith("**Spec:**"):
                spec_paragraph = True
            if spec_paragraph and (not line.strip() or section):
                spec_paragraph = False
            if context_depth or spec_paragraph:
                context.append(line)
            elif not line.strip() and context and context[-1].strip():
                context.append(line)
        if inside:
            selected.append(line)
    if not selected:
        print(f"task {number} not found in {plan}", file=sys.stderr)
        return 3
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as target:
        target.writelines(context + selected)
    print(f"wrote {out}: {len(selected)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
