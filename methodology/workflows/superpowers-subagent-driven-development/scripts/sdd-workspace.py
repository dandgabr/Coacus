#!/usr/bin/env python3
"""Resolve a plan-scoped, git-ignored workspace in the current repository."""

from __future__ import annotations

import subprocess
import sys
from itertools import chain, count
from pathlib import Path


def workspace(plan: Path) -> Path:
    plan = plan.resolve(strict=True)
    if not plan.is_file():
        raise ValueError(f"no such plan file: {plan}")
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    base = root / ".superpowers" / "sdd"
    slug = plan.stem
    if slug in ("", ".", ".."):
        raise ValueError(f"cannot derive a workspace name from: {plan}")
    try:
        owner = plan.relative_to(root).as_posix()
    except ValueError:
        owner = plan.as_posix()
    candidates = chain(
        [base / slug, base / f"{slug}-{plan.parent.name}"],
        (base / f"{slug}-{plan.parent.name}-{n}" for n in count(2)),
    )
    for directory in candidates:
        marker = directory / "plan-path"
        if marker.exists() and marker.read_text(encoding="utf-8").strip() != owner:
            continue
        directory.mkdir(parents=True, exist_ok=True)
        marker.write_text(owner + "\n", encoding="utf-8")
        (base / ".gitignore").write_text("*\n", encoding="utf-8")
        return directory
    raise ValueError("no free plan workspace")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: sdd-workspace.py PLAN_FILE", file=sys.stderr)
        return 2
    try:
        print(workspace(Path(args[0])))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
