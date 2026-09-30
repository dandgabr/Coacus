#!/usr/bin/env python3
"""Coacus self-improvement CLI (thin dispatch over ``engine.improve``).

OPT-IN and fail-open (P2): the loop does nothing unless invoked here, and it
never touches the deterministic build contract (``generate``/``check``). In v1 it
only PROPOSES; promotion is a human PR.

Usage:
    python3 scripts/coacus_improve.py run --transcript <path.jsonl> [--source transcript]
    python3 scripts/coacus_improve.py status
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def cmd_run(args: argparse.Namespace) -> int:
    """Run the improvement pipeline once and print the summary."""
    from engine.improve import loop

    options = {
        "transcript": args.transcript,
        "memory_export": args.memory_export,
        "source": args.source,
    }
    summary = loop.run(ROOT if args.root is None else Path(args.root), options)
    print(json.dumps(summary, indent=2, sort_keys=True))
    for alarm in summary.get("alarms", []):
        print(f"  [alarm] {alarm}", file=sys.stderr)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Report the availability of each episodic source on this machine."""
    from engine.improve import sources

    registry = sources.SourceRegistry()
    sources.register_builtin(registry)
    root = ROOT if args.root is None else Path(args.root)
    statuses = {name: registry.get(name).status(root) for name in registry.names()}  # type: ignore[union-attr]
    print(json.dumps(statuses, indent=2, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to the selected subcommand."""
    parser = argparse.ArgumentParser(prog="coacus-improve", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run the improvement pipeline once (proposal-only)")
    run.add_argument("--transcript", help="path to a session transcript (JSONL)")
    run.add_argument("--memory-export", help="path to an ai-memory export (JSONL)")
    run.add_argument("--source", default="transcript", help="episodic source name")
    run.add_argument("--root", help="repository root (default: this repo)")

    status = sub.add_parser("status", help="report episodic source availability")
    status.add_argument("--root", help="repository root (default: this repo)")

    args = parser.parse_args(argv)
    if args.command == "run":
        return cmd_run(args)
    return cmd_status(args)


if __name__ == "__main__":
    raise SystemExit(main())
