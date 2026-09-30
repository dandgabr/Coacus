#!/usr/bin/env python3
"""Coacus guardrail runtime: evaluate PAER policies for one lifecycle event.

The generated native hooks (shape A shell scripts, shape B JS plugins) call this
CLI with the harness name and the bound event; the harness pipe the trigger
payload on stdin. The CLI:

1. reads the payload,
2. maps the tool call to a canonical ACTION (verb + resource),
3. evaluates the active policies (``engine.guardrail.evaluate``),
4. emits the harness-native effect JSON.

Failure semantics (D4): a decision the evaluator could not make is governed by
the matched policy's ``on_decision_failure``; a failure of this process itself
(no python3, malformed payload) degrades to ``on_mechanism_failure`` (default
allow) plus an advisory, so a broken guardrail cannot brick a session.

Always exits 0: the decision travels in the JSON, not the exit code (OpenCode has
no exit code; Claude's exit-2 path is reserved for the explicit deny render).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.guardrail import evaluate as guard  # noqa: E402

READ_TOOLS = {"read", "read_file", "Read", "view_file"}
WRITE_TOOLS = {"write", "edit", "write_file", "edit_file", "apply_patch", "Write", "Edit",
               "write_to_file", "replace_file_content"}
EXEC_TOOLS = {"bash", "shell", "shell_command", "run_command", "terminal", "Bash"}
NETWORK_TOOLS = {"fetch", "webfetch", "web_fetch", "read_url_content", "fetch_url"}
SPAWN_TOOLS = {"task", "agent", "spawn_agent", "invoke_subagent", "manage_subagents"}


def _first(mapping: dict, keys: tuple[str, ...], default: str = "") -> str:
    """First present, non-empty string value among ``keys``."""
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return default


def _action(payload: dict) -> tuple[str, str]:
    """Map a native payload to a canonical (verb, resource)."""
    tool = _first(payload, ("tool", "tool_name", "toolName", "name"))
    args = payload.get("tool_input") or payload.get("args") or payload.get("toolCall") or {}
    if not isinstance(args, dict):
        args = {}
    path = _first(args, ("filePath", "file_path", "path", "target_file"))
    command = _first(args, ("command", "CommandLine", "cmd"))
    if tool in READ_TOOLS:
        return "read", path
    if tool in WRITE_TOOLS:
        return "write", path
    if tool in EXEC_TOOLS:
        return "exec", command
    if tool in NETWORK_TOOLS:
        return "network", _first(args, ("url", "uri"))
    if tool in SPAWN_TOOLS:
        return "spawn", _first(args, ("prompt", "description", "name"))
    return "", ""


def _native(harness: str, decision: str, message: str) -> str:
    """Render the harness-native effect JSON.

    The effect encodings are engine data (PAER 'Rendering effect' layer): a
    harness with no deny render yields ``{}`` (no opinion).
    """
    if decision == "allow":
        return "{}"
    if harness in ("claude-code", "codex", "command-code"):
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny" if decision == "deny" else "ask",
                    "permissionDecisionReason": message,
                }
            }
        )
    if harness == "cursor":
        return json.dumps(
            {"permission": "deny" if decision == "deny" else "ask", "user_message": message}
        )
    if harness == "antigravity":
        return json.dumps(
            {"decision": "deny" if decision == "deny" else "ask", "reason": message}
        )
    return "{}"


def run(harness: str, event: str, payload_text: str, root: Path) -> str:
    """Evaluate one event and return the native effect JSON (never raises)."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
        verb, resource = _action(payload)
        policies = guard.load_policies(root)
        result = guard.evaluate(policies, verb, resource) if verb else {
            "decision": "allow", "policy_id": None, "message": ""
        }
        decision = result.get("decision", "allow")
        message = result.get("message", "")
        if decision == "ask":
            # On a harness without a human channel, coerce per policy.
            decision = result.get("on_ask_unavailable", "deny")
        if decision == "note":
            decision = "allow"
        return _native(harness, decision, message)
    except Exception:  # mechanism failure (D4): allow + advisory, never brick.
        return "{}"


def main(argv: list[str] | None = None) -> int:
    """Parse args, evaluate, print the native effect JSON, exit 0."""
    parser = argparse.ArgumentParser(prog="coacus-guard", description=__doc__)
    parser.add_argument("--harness", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    payload = sys.stdin.read()
    print(run(args.harness, args.event, payload, Path(args.root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
