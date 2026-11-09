#!/usr/bin/env python3
"""Coacus governor hook for Antigravity (cross-platform, stdlib only).

Bridges Antigravity lifecycle hooks to the shared Coacus governor.
The payload on stdin is protojson camelCase:
toolCall.name, conversationId, stepIdx, error.
  - pretool : deny spawn until host correlation and lifetime are verified.
  - posttool: preserve existing reservations when correlation is unverified.
  - preinv  : inject the concurrency budget + retry contract.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Add repo root to sys.path so engine can be imported directly
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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


def _manage_action(payload: dict):
    args = _get_nested(payload, "toolCall.args")
    if not isinstance(args, dict):
        return None
    if "Action" in args and "action" in args and args["Action"] != args["action"]:
        return None
    return args.get("Action", args.get("action"))


def main() -> int:
    """Execute governor hook actions based on CLI mode and stdin protojson."""
    mode = sys.argv[1] if len(sys.argv) > 1 else ""

    payload = _read_stdin_json() if mode in ("pretool", "posttool") else {}
    if mode == "pretool":
        tool = _get_nested(payload, "toolCall.name")
        if not isinstance(tool, str) or not tool or any(c.isspace() or not c.isprintable() for c in tool):
            sys.stdout.write(json.dumps({"decision": "deny", "reason": "Unidentifiable tool call."}) + "\n")
            return 0
        if tool == "manage_subagents":
            action = _manage_action(payload)
            if action in ("list", "kill", "kill_all"):
                sys.stdout.write('{"decision": "allow"}\n')
                return 0
            if action != "spawn":
                sys.stdout.write(json.dumps({"decision": "deny", "reason": "Unknown subagent action."}) + "\n")
                return 0
        if tool in ("invoke_subagent", "manage_subagents", "task"):
            # ponytail: host call identity and completion lifetime are unverified;
            # enable dispatch only with a verified unique, end-to-end correlation.
            sys.stdout.write(json.dumps({"decision": "deny", "reason": "Governor cannot safely correlate subagent dispatch and completion."}) + "\n")
            return 0

    if mode == "posttool":
        # A post event cannot safely identify which reservation it owns.
        sys.stdout.write("{}\n")
        return 0

    try:
        from engine.governor.ledger import Ledger, resolve_concurrency_cap
        scope = "antigravity"
        max_total = resolve_concurrency_cap(scope=scope)
        ledger = Ledger(scope=scope, max_total=max_total)
    except Exception:
        ledger = None
        max_total = 6

    if mode == "pretool":
        sys.stdout.write('{"decision": "allow"}\n')
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
            f"[CONCURRENCY GOVERNOR] Antigravity subagent dispatch is disabled until host correlation and worker lifetime are verified. Max concurrent agents counting the orchestrator = {max_total}. "
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
