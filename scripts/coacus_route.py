#!/usr/bin/env python3
"""Select agents for a prompt (routing) — manual and automated modes.

    coacus_route.py "<prompt>" [--top N] [--min-score X] [--max-slots]   # Mode A
    coacus_route.py --list [--category C] [--grep TERM]                  # Mode M
    coacus_route.py --agents name1,name2                                # Mode M

Mode A (automated curation) ranks the agents against the prompt and prints the
best candidates, one per line: ``score<TAB>name<TAB>category<TAB>matched``.
Mode M (manual) browses or validates an explicit selection; an unknown name is an
error with suggestions and a non-zero exit.

The command only PROPOSES; it never spawns an agent. ``--max-slots`` caps the
proposal at the governor's free slots so a caller cannot over-subscribe.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import router  # noqa: E402
from engine.governor.ledger import Ledger  # noqa: E402


def _free_slots() -> int:
    """Free governor slots (orchestrator included); a safe default on failure."""
    try:
        return int(Ledger().status()["slots_free"])
    except Exception:
        return 0


def _cmd_rank(args: argparse.Namespace, root: Path) -> int:
    prompt = args.prompt
    limit = args.top
    if args.max_slots:
        limit = _free_slots() if limit is None else min(limit, _free_slots())
    candidates = router.rank(root, prompt, limit=limit, min_score=args.min_score)
    if not candidates:
        print("no agent above the score threshold")
        return 1
    if args.rerank:
        candidates = router.rerank(candidates, prompt, args.rerank)
    for c in candidates:
        print(f"{c.score:.1f}\t{c.name}\t{c.category}\t{','.join(c.matched)}")
    return 0


def _cmd_list(args: argparse.Namespace, root: Path) -> int:
    for entry in router.list_agents(root, category=args.category, grep=args.grep):
        print(f"{entry.get('name')}\t{entry.get('category')}\t{entry.get('description')}")
    return 0


def _cmd_agents(args: argparse.Namespace, root: Path) -> int:
    names = [n for part in args.agents for n in part.split(",")]
    matched, errors = router.resolve(root, names)
    for entry in matched:
        print(f"{entry.get('name')}\t{entry.get('category')}")
    for error in errors:
        print(f"[error] {error}", file=sys.stderr)
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to the selected routing mode."""
    parser = argparse.ArgumentParser(prog="coacus-route", description=__doc__)
    parser.add_argument("prompt", nargs="?", default="", help="prompt to route (Mode A)")
    parser.add_argument("--top", type=int, default=None, help="maximum candidates to print")
    parser.add_argument("--min-score", type=float, default=router.DEFAULT_MIN_SCORE)
    parser.add_argument(
        "--rerank",
        default=None,
        help="optional semantic reranker command (reads JSON on stdin, prints names)",
    )
    parser.add_argument(
        "--max-slots",
        action="store_true",
        help="cap the proposal at the governor's free slots",
    )
    parser.add_argument("--list", action="store_true", help="list agents (Mode M)")
    parser.add_argument("--category", default=None, help="filter --list by category")
    parser.add_argument("--grep", default=None, help="filter --list by substring")
    parser.add_argument(
        "--agents",
        action="append",
        default=[],
        help="validate an explicit selection, comma-separated (Mode M)",
    )
    args = parser.parse_args(argv)
    root = ROOT

    if args.agents:
        return _cmd_agents(args, root)
    if args.list:
        return _cmd_list(args, root)
    if args.prompt:
        return _cmd_rank(args, root)
    parser.error("provide a prompt, --list, or --agents")


if __name__ == "__main__":
    raise SystemExit(main())
