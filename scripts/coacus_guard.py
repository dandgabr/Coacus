#!/usr/bin/env python3
"""Coacus guardrail runtime: evaluate PAER policies for one lifecycle event.

The generated native hooks (shape A Python commands, shape B JS plugins) call this
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

An ``ask`` decision is rendered as ``ask`` only when the operator opted in with
``COACUS_GUARD_ASK=1`` AND the harness declares a human channel for the event
(``can_ask`` and ``can_block`` in ``harness.json``). ``COACUS_GUARD_NO_ASK`` and a
set ``CI`` variable always win and force the degradation. In every other case
(the default, no capability data, a harness without a human channel) it degrades
to the matched policy's ``on_ask_unavailable``, which fails closed to ``deny`` when
absent or invalid. The hook payload carries no headless or subagent signal, so
asking is opt-in: a run with no human present cannot be detected from here.

Always exits 0: the decision travels in the JSON, not the exit code (OpenCode has
no exit code; Claude's exit-2 path is reserved for the explicit deny render).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.guardrail import evaluate as guard  # noqa: E402

# Tool names are compared in lower case, so ``Read`` and ``read`` are one tool.
READ_TOOLS = {"read", "read_file", "view_file", "grep", "glob", "list", "ls", "notebookread",
              "view", "cat", "search_files", "find_files"}
WRITE_TOOLS = {"write", "edit", "write_file", "edit_file", "apply_patch", "write_to_file",
               "replace_file_content", "multiedit", "patch", "notebookedit", "str_replace_editor",
               "create_file", "delete_file"}
EXEC_TOOLS = {"bash", "shell", "shell_command", "run_command", "terminal", "exec", "execute"}
NETWORK_TOOLS = {"fetch", "webfetch", "web_fetch", "read_url_content", "fetch_url", "websearch",
                 "web_search"}
SPAWN_TOOLS = {"task", "agent", "spawn_agent", "invoke_subagent", "manage_subagents", "subagent"}
_PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.MULTILINE)


def _first(mapping: dict, keys: tuple[str, ...], default: str = "") -> str:
    """First present, non-empty string value among ``keys``.

    An argv list (some harnesses pass ``["bash", "-lc", "cmd"]``) is rendered as
    one shell string so ``exec`` policies see the real command, not a Python repr.
    """
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, (list, tuple)) and value:
            return shlex.join(str(part) for part in value)
        if value is not None and str(value).strip():
            return str(value)
    return default


def _patch_paths(args: dict) -> list[str]:
    """File paths named inside an ``apply_patch`` style patch text, in order."""
    for value in args.values():
        if isinstance(value, str):
            found = [p.strip() for p in _PATCH_FILE.findall(value)]
            if found:
                return found
    return []


def _actions(payload: dict) -> list[tuple[str, str]]:
    """Map a native payload to canonical ``(verb, resource)`` pairs.

    Usually one. A patch that touches several files yields one write per file, so a
    policy on any of them is consulted.
    """
    tool = _first(payload, ("tool", "tool_name", "toolName", "name")).lower()
    args = payload.get("tool_input") or payload.get("args") or payload.get("toolCall") or {}
    if isinstance(args, str):
        args = {"input": args}
    if not isinstance(args, dict):
        args = {}
    path = _first(args, ("filePath", "file_path", "path", "target_file", "notebook_path", "pattern"))
    command = _first(args, ("command", "CommandLine", "cmd"))
    if tool in READ_TOOLS:
        return [("read", path)]
    if tool in WRITE_TOOLS:
        patched = _patch_paths(args)
        if patched:
            return [("write", item) for item in patched]
        return [("write", path)]
    if tool in EXEC_TOOLS:
        return [("exec", command)]
    if tool in NETWORK_TOOLS:
        return [("network", _first(args, ("url", "uri", "query")))]
    if tool in SPAWN_TOOLS:
        return [("spawn", _first(args, ("prompt", "description", "name")))]
    return [("", "")]


def _action(payload: dict) -> tuple[str, str]:
    """Map a native payload to its first canonical (verb, resource)."""
    return _actions(payload)[0]


def _allow(harness: str) -> str:
    """Render the 'permit, no opinion' effect for a harness.

    On most harnesses an empty object means "no opinion" and the tool proceeds.
    Antigravity is the exception: its PreToolUse contract makes ``decision``
    REQUIRED, and an object without it is read as a denial ("tool call denied by
    pre-tool hook:" with an empty reason). So Coacus must answer ``allow``
    explicitly there, otherwise an unopinionated guard blocks every tool call.
    """
    if harness == "antigravity":
        return json.dumps({"decision": "allow"})
    return "{}"


def _word(decision: str) -> str:
    """Return the native decision word: ``ask`` only for an exact ask, else ``deny``."""
    return "ask" if decision == "ask" else "deny"


def _native(harness: str, decision: str, message: str) -> str:
    """Render the harness-native effect JSON.

    The effect encodings are engine data (PAER 'Rendering effect' layer): a
    harness with no deny render yields ``{}`` (no opinion).
    """
    if decision == "allow":
        return _allow(harness)
    if harness in ("claude-code", "codex", "command-code"):
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": _word(decision),
                    "permissionDecisionReason": message,
                }
            }
        )
    if harness == "cursor":
        return json.dumps(
            {"permission": _word(decision), "user_message": message}
        )
    if harness == "antigravity":
        return json.dumps(
            {"decision": _word(decision), "reason": message}
        )
    if harness == "opencode":
        # OpenCode has no native effect JSON: the generated plugin reads this
        # object and throws on a deny, which is its only blocking mechanism.
        return json.dumps({"decision": "deny", "reason": message})
    return "{}"


def _env_on(name: str) -> bool:
    """Return True when environment variable ``name`` is set to a truthy value."""
    return os.environ.get(name, "").strip().lower() not in ("", "0", "false", "no", "off")


def _safe_harness_name(harness: str) -> bool:
    """Return True for a name of lowercase ASCII letters, digits and dashes.

    The first character must be a letter or a digit, so a name never looks like a
    command-line option.
    """
    return bool(harness) and harness[0].isalnum() and all(
        ch.isascii() and (ch.islower() or ch.isdigit() or ch == "-") for ch in harness
    )


def _can_ask(root: Path, harness: str, event: str) -> bool:
    """Return True only when asking is opted in and ``harness`` has a human channel.

    Asking needs ``COACUS_GUARD_ASK=1``; ``COACUS_GUARD_NO_ASK`` or a set ``CI``
    answers False first. The capability is read from
    ``harnesses/<harness>/harness.json`` under ``root``. Any doubt (unsafe harness
    name, an event other than ``tool.pre`` (the only one rendered), missing or
    unreadable data, a capability without ``can_block``, any error while reading)
    answers False so the caller degrades instead of asking.
    """
    if _env_on("COACUS_GUARD_NO_ASK") or _env_on("CI"):
        return False
    if os.environ.get("COACUS_GUARD_ASK", "").strip() != "1":
        return False
    if event != "tool.pre" or not _safe_harness_name(harness):
        return False
    try:
        data = json.loads((root / "harnesses" / harness / "harness.json").read_text(encoding="utf-8"))
        capability = data["lifecycle"]["events"][event]
        return capability.get("can_ask") is True and capability.get("can_block") is True
    except Exception:  # any doubt, including RecursionError on hostile data, degrades
        return False


def _degrade_ask(result: dict) -> str:
    """Return the decision an unavailable ``ask`` degrades to; invalid values deny."""
    fallback = result.get("on_ask_unavailable", "deny")
    return fallback if fallback in ("allow", "deny") else "deny"


_RANK = {"allow": 0, "note": 0, "ask": 1, "deny": 2}


def run(harness: str, event: str, payload_text: str, root: Path) -> str:
    """Evaluate one event and return the native effect JSON (never raises)."""
    try:
        payload = json.loads(payload_text) if payload_text.strip() else {}
        policies = guard.load_policies(root, include_user=True)
        result = {"decision": "allow", "policy_id": None, "message": ""}
        for verb, resource in _actions(payload):
            if not verb:
                continue
            one = guard.evaluate(policies, verb, resource)
            if _RANK.get(one.get("decision", "allow"), 2) > _RANK.get(result["decision"], 0):
                result = one
        decision = result.get("decision", "allow")
        message = result.get("message", "")
        if decision == "ask" and not _can_ask(root, harness, event):
            # No human channel for this harness and event: degrade per policy.
            decision = _degrade_ask(result)
        if decision == "note":
            decision = "allow"
        return _native(harness, decision, message)
    except Exception:  # mechanism failure (D4): allow + advisory, never brick.
        return _allow(harness)


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
