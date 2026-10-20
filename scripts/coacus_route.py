#!/usr/bin/env python3
"""Select agents for a prompt (routing) — manual and automated modes.

    coacus_route.py "<prompt>" [--top N] [--all] [--raw] [--min-score X] # Mode A
    coacus_route.py --list [--category C] [--grep TERM]                  # Mode M
    coacus_route.py --agents name1,name2                                # Mode M

Mode A (automated curation) ranks the agents against the prompt and presents
the best candidates. In interactive terminals, output is formatted ergonomically
using Cognitive UX Laws (Fitts's Law quick actions, Cowan 4±1 chunking, Von Restorff
isolation, and Hick's Law progressive disclosure). When piped or given --raw, it prints
standard TSV: ``score<TAB>name<TAB>category<TAB>matched``.
Mode M (manual) browses or validates an explicit selection; an unknown name is an
error with suggestions and a non-zero exit.

The command only PROPOSES; it never spawns an agent. ``--max-slots`` caps the
proposal at the governor's free slots so a caller cannot over-subscribe.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import router  # noqa: E402
from engine.governor.ledger import Ledger  # noqa: E402

DEFAULT_INTERACTIVE_TOP = 4


def _free_slots() -> int:
    """Free governor slots (orchestrator included); a safe default on failure."""
    try:
        return int(Ledger().status()["slots_free"])
    except Exception:
        return 0


def format_candidates(
    candidates: list[router.Candidate],
    *,
    raw: bool = False,
    use_color: bool = False,
    total_matches: int | None = None,
) -> str:
    """Format candidate agent proposals for CLI output.

    When raw=True, outputs standard TSV (score\\tname\\tcategory\\tmatched).
    When raw=False, outputs human-first presentation with Von Restorff isolation,
    Cowan chunking (4±1), and Fitts zero-distance quick action on the last line.
    """
    if raw or not candidates:
        return "\n".join(
            f"{c.score:.1f}\t{c.name}\t{c.category}\t{','.join(c.matched)}"
            for c in candidates
        )

    bold = "\033[1m" if use_color else ""
    dim = "\033[2m" if use_color else ""
    cyan = "\033[36m" if use_color else ""
    reset = "\033[0m" if use_color else ""

    lines: list[str] = []
    top = candidates[0]
    alternatives = candidates[1:]

    # Primary recommendation (Von Restorff isolation)
    matched_str = ", ".join(top.matched) if top.matched else "general"
    lines.append(
        f"{bold}{cyan}★ PRIMARY RECOMMENDATION:{reset} {bold}{top.name}{reset} "
        f"{dim}({top.category} | score {top.score:.1f}){reset}"
    )
    if top.description:
        desc = top.description.strip().split("\n")[0]
        lines.append(f"  {dim}{desc}{reset}")
    lines.append(f"  {dim}Matched triggers: {matched_str}{reset}")

    # Alternatives chunked (Miller/Cowan 4±1)
    if alternatives:
        lines.append("")
        lines.append(f"{bold}Specialist Alternatives:{reset}")
        for c in alternatives:
            c_matched = ", ".join(c.matched) if c.matched else "intent"
            lines.append(
                f"  • {bold}{c.name}{reset} {dim}({c.category} | score {c.score:.1f}) — {c_matched}{reset}"
            )

    if total_matches is not None and total_matches > len(candidates):
        more_count = total_matches - len(candidates)
        lines.append(
            f"  {dim}... and {more_count} more candidates (use --all or --top <N> to view all){reset}"
        )

    # Immediate action on very last line (Fitts's Law / KLM)
    lines.append("")
    lines.append(f"Quick action: python3 scripts/coacus_install.py antigravity --agents {top.name}")

    return "\n".join(lines)


def _cmd_rank(args: argparse.Namespace, root: Path) -> int:
    prompt = args.prompt
    is_tty = sys.stdout.isatty()
    is_raw = bool(args.raw or not is_tty)
    no_color = bool(os.getenv("NO_COLOR") or os.getenv("TERM") == "dumb")
    use_color = is_tty and not no_color and not is_raw

    # Progressive disclosure limit (Hick's Law):
    limit = args.top
    if limit is None and not args.all and not is_raw:
        limit = DEFAULT_INTERACTIVE_TOP

    if args.max_slots:
        free = _free_slots()
        limit = free if limit is None else min(limit, free)

    # Fetch candidates with optional limit
    all_candidates = router.rank(root, prompt, limit=None, min_score=args.min_score)
    if not all_candidates:
        print("no agent above the score threshold", file=sys.stderr if not is_raw else sys.stdout)
        return 1

    if args.rerank:
        all_candidates = router.rerank(all_candidates, prompt, args.rerank)

    total_matches = len(all_candidates)
    selected = all_candidates[:limit] if limit is not None else all_candidates

    output = format_candidates(
        selected,
        raw=is_raw,
        use_color=use_color,
        total_matches=total_matches,
    )
    print(output)
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
    parser.add_argument("--all", action="store_true", help="show all candidates without capping")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="force raw tab-separated output (default when piped or non-TTY)",
    )
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
