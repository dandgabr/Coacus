#!/usr/bin/env python3
"""Coacus governor hook for Antigravity (cross-platform, stdlib only).

Bridges Antigravity lifecycle hooks to the shared Coacus governor.
The payload on stdin is protojson camelCase:
toolCall.name, conversationId, stepIdx, error.
  - pretool : acquire a slot before a subagent spawn.
  - posttool: release the slot, or mark PAUSED on a rate-limit (429).
  - preinv  : inject the concurrency budget + retry contract.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Add repo root to sys.path so engine can be imported directly
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

RATE_RE = re.compile(
    r"(429|Too Many Requests|rate.?limit|quota exceeded|RPM|TPM|tokens_per_minute|tokens per minute)",
    re.IGNORECASE,
)


def _get_nested(data: dict, path: str):
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _read_stdin_json() -> dict:
    try:
        content = sys.stdin.read()
        if not content.strip():
            return {}
        return json.loads(content)
    except Exception:
        return {}


def _slot_id(payload: dict) -> str:
    conv = _get_nested(payload, "conversationId") or "none"
    step = _get_nested(payload, "stepIdx")
    step_str = "none" if step is None else str(step)
    return f"agy-{conv}-{step_str}"


def main() -> int:
    """Execute governor hook actions based on CLI mode and stdin protojson."""
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    max_total = int(os.environ.get("ORCH_MAX_CONCURRENT", "5"))

    try:
        from engine.governor.ledger import Ledger
        ledger = Ledger(max_total=max_total)
    except Exception:
        ledger = None

    if mode == "pretool":
        payload = _read_stdin_json()
        tool = _get_nested(payload, "toolCall.name") or ""
        if tool in ("invoke_subagent", "manage_subagents", "task") and ledger:
            try:
                ledger.acquire(_slot_id(payload), orchestrator=False, timeout_seconds=30)
            except Exception:
                pass
        sys.stdout.write("{}\n")
        return 0

    if mode == "posttool":
        payload = _read_stdin_json()
        err = _get_nested(payload, "error") or ""
        slot = _slot_id(payload)
        if err and RATE_RE.search(str(err)):
            if ledger:
                try:
                    ledger.fail(slot)
                except Exception:
                    pass
            msg = (
                f"Rate-limit (429) detected in a spawned agent. Mark that task PAUSED, "
                f"wait until fewer than {max_total} agents run (counting you), then relaunch it "
                f"with exponential backoff. Do NOT relaunch while the cap is saturated."
            )
            sys.stdout.write(json.dumps({"ephemeralMessage": msg}) + "\n")
            return 0
        else:
            if ledger:
                try:
                    ledger.release(slot)
                except Exception:
                    pass
            sys.stdout.write("{}\n")
            return 0

    if mode == "preinv":
        status_line = f"running=0 paused=0 max={max_total} slots_free={max_total}"
        if ledger:
            try:
                st = ledger.status()
                status_line = (
                    f"running={st['running']} paused={st['paused']} max={st['max']} "
                    f"orchestrator={str(st['orchestrator_present']).lower()} "
                    f"slots_free={st['slots_free']}"
                )
            except Exception:
                pass
        msg = (
            f"[CONCURRENCY GOVERNOR] Max concurrent agents counting the orchestrator = {max_total}. "
            f"Current ledger: {status_line}. Do not spawn a new subagent while running >= cap: "
            f"enqueue it (QUEUED) and wait for a running agent to finish. If a subagent fails with "
            f"HTTP 429 / Too Many Requests / quota, kill it, mark it PAUSED, wait until running < cap "
            f"and relaunch with exponential backoff."
        )
        sys.stdout.write(json.dumps({"injectSteps": [{"ephemeralMessage": msg}]}) + "\n")
        return 0

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
