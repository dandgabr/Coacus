#!/usr/bin/env python3
"""Write a review package for a nonempty descendant commit range."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (3, 4):
        print("usage: review-package.py PLAN_FILE BASE HEAD [OUTFILE]", file=sys.stderr)
        return 2
    plan, base, head = Path(args[0]), args[1], args[2]
    if not plan.is_file():
        print(f"no such plan file: {plan}", file=sys.stderr)
        return 2
    try:
        git("rev-parse", "--verify", base)
        git("rev-parse", "--verify", head)
        if subprocess.run(["git", "merge-base", "--is-ancestor", base, head]).returncode != 0:
            print(f"HEAD is not a descendant of BASE: {base}..{head}", file=sys.stderr)
            return 3
        count = int(git("rev-list", "--count", f"{base}..{head}"))
        if count == 0:
            print(f"empty commit range: {base}..{head}", file=sys.stderr)
            return 3
        if len(args) == 4:
            out = Path(args[3])
        else:
            script = Path(__file__).with_name("sdd-workspace.py")
            directory = Path(subprocess.check_output([sys.executable, str(script), str(plan)], text=True).strip())
            out = directory / f"review-{git('rev-parse', '--short', base).strip()}..{git('rev-parse', '--short', head).strip()}.diff"
        content = (f"# Review package: {base}..{head}\n\n## Commits\n" + git("log", "--oneline", f"{base}..{head}")
                   + "\n## Files changed\n" + git("diff", "--stat", f"{base}..{head}")
                   + "\n## Diff\n" + git("diff", "-U10", f"{base}..{head}"))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print(f"wrote {out}: {count} commit(s), {out.stat().st_size} bytes")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
