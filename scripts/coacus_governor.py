#!/usr/bin/env python3
"""Thin CLI over the concurrency governor (D6/ADR-0007).

Mirrors the reference command surface so harness adapters (the OpenCode gate
plugin) can call it directly:

    coacus_governor.py acquire <caller> [orchestrator-yes|no] [timeout-secs] [max-total]
    coacus_governor.py release <caller>
    coacus_governor.py fail    <caller>
    coacus_governor.py paused
    coacus_governor.py status  [max-total]
    coacus_governor.py reset

``acquire`` prints the token on success (exit 0) or nothing (exit 1) when the
cap stayed saturated past the timeout.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.governor.ledger import Ledger  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus-governor", description=__doc__)
    parser.add_argument(
        "action",
        choices=["acquire", "release", "fail", "paused", "status", "health", "reset"],
    )
    parser.add_argument("caller", nargs="?", default="")
    parser.add_argument("orchestrator", nargs="?", default="no")
    parser.add_argument("timeout", nargs="?", type=float, default=30.0)
    parser.add_argument("max_total", nargs="?", type=int, default=None)
    args = parser.parse_args(argv)

    ledger = Ledger(max_total=args.max_total)
    if args.action == "acquire":
        token = ledger.acquire(
            args.caller or "unknown",
            orchestrator=args.orchestrator == "yes",
            timeout=args.timeout,
        )
        if token:
            print(token)
            return 0
        return 1
    if args.action == "release":
        ledger.release(args.caller or "unknown")
        return 0
    if args.action == "fail":
        ledger.fail(args.caller or "unknown")
        return 0
    if args.action == "reset":
        ledger.reset()
        return 0
    if args.action == "paused":
        for row in ledger.paused():
            print(f"{row['caller']} attempts={row['attempts']} retry_after_s={row['retry_after_s']}")
        return 0
    if args.action == "health":
        # Wiring check: ledger dir writable, lock acquirable, cap read.
        token = ledger.acquire("__health__", timeout=1.0)
        ok = token is not None
        if ok:
            ledger.release("__health__")
        status = ledger.status()
        print(
            f"health={'ok' if ok else 'fail'} dir={ledger.dir} "
            f"max={status['max']} running={status['running']}"
        )
        return 0 if ok else 1
    status = ledger.status()
    print(
        f"running={status['running']} paused={status['paused']} max={status['max']} "
        f"orchestrator={str(status['orchestrator_present']).lower()} "
        f"slots_free={status['slots_free']}"
    )
    for line in status["ledger"]:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
