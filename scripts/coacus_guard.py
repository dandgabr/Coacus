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
        # object. It throws on a deny (its only blocking mechanism) and only the
        # permission ``evaluate`` hook can turn an ask into a prompt; the plugin
        # never loosens a decision it was given.
        return json.dumps({"decision": _word(decision), "reason": message})
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


ASK_CHANNELS = ("default", "before", "evaluate")

# The only event with a rendered hook today (ADR 0012).
ENFORCED_EVENT = "tool.pre"

# OpenCode permission names to canonical verbs. Unverified against a live OpenCode V2
# run: only the documented hook contract is known, not every permission name.
_PERMISSION_VERBS = {
    "read": "read", "edit": "write", "write": "write", "patch": "write",
    "shell": "exec", "bash": "exec", "subagent": "spawn", "task": "spawn",
    "webfetch": "network",
}

# Verbs an ask may be deferred to the evaluate hook for. The hook sees a path as a
# location-relative internal path while a tool call carries the raw one, and only
# these two have documented, path-shaped resources. A command or a subagent request
# is not deferred: it degrades to the policy fallback, so it never becomes an allow.
_DEFERRABLE_VERBS = ("read", "write")


def _permission_actions(payload: dict) -> list[tuple[str, str]]:
    """Map an OpenCode permission request (``action`` + ``resources``) to canonical actions."""
    verb = _PERMISSION_VERBS.get(str(payload.get("action", "")).lower(), "")
    resources = payload.get("resources")
    if not verb or not isinstance(resources, (list, tuple)):
        return []
    return [(verb, str(item)) for item in resources if isinstance(item, (str, int, float))]


def _can_ask(root: Path, harness: str, event: str, channel: str = "default") -> bool:
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
        if capability.get("can_ask") is not True or capability.get("can_block") is not True:
            return False
        # A harness that can ask only through one channel (OpenCode's permission
        # ``evaluate`` hook) never asks on any other, or the call would slip past.
        required = capability.get("ask_channel")
        if required is None:
            return channel == "default"
        # The channel is checked against documentation only, never a live run, so it
        # needs its own explicit opt-in on top of COACUS_GUARD_ASK=1.
        if os.environ.get("COACUS_GUARD_ASK_EXPERIMENTAL", "").strip() != "1":
            return False
        return channel in ("before", "evaluate") and required == "evaluate"
    except Exception:  # any doubt, including RecursionError on hostile data, degrades
        return False


def _degrade_ask(result: dict) -> str:
    """Return the decision an unavailable ``ask`` degrades to; invalid values deny."""
    fallback = result.get("on_ask_unavailable", "deny")
    return fallback if fallback in ("allow", "deny") else "deny"


_RANK = {"allow": 0, "ask": 1, "deny": 2}


def _path_forms(resource: str) -> set[str]:
    """Every shape a hook might report for ``resource``, as far as can be known here.

    The raw string, its absolute form, its form relative to the working directory and
    to each of that directory's nearest ancestors (the project root is not known to
    the guard), and its last component.
    """
    forms = {resource, os.path.basename(resource)}
    absolute = os.path.abspath(resource)
    forms.add(absolute)
    here = Path.cwd()
    for base in [here, *list(here.parents)[:6]]:
        try:
            forms.add(os.path.relpath(absolute, base))
        except ValueError:
            continue
    forms.discard("")
    return forms


def _survives_the_hook(policies: list[dict], verb: str, resource: str, event: str = "tool.pre") -> bool:
    """True when an ask would be raised again whatever shape the hook sees.

    Only read and write are deferred. The hook receives a path in a shape this guard
    cannot know (relative to the project, to the working directory, or absolute), so
    the ask must hold for every plausible form; a policy anchored on one shape (for
    example ``sub/*`` or ``*/.env``) is not deferred and degrades to its fallback,
    which never turns it into an allow.
    """
    if verb not in _DEFERRABLE_VERBS or not resource:
        return False
    return all(
        guard.evaluate(policies, verb, form, event).get("decision") == "ask"
        for form in _path_forms(resource)
    )


def _decide(root: Path, harness: str, event: str, channel: str, verb: str, resource: str) -> tuple[str, str]:
    """Return ``(decision, message)`` for one canonical action on one channel."""
    policies = guard.load_policies(root, include_user=True)
    result = guard.evaluate(policies, verb, resource, event) if verb else {
        "decision": "allow", "policy_id": None, "message": ""
    }
    decision = result.get("decision", "allow")
    message = result.get("message", "")
    if decision == "ask":
        if _can_ask(root, harness, event, channel) and (
            channel != "before" or _survives_the_hook(policies, verb, resource, event)
        ):
            if channel == "before":
                decision = "allow"  # left to the evaluate hook, which asks
        else:
            # No human channel for this harness, event and channel: degrade per policy.
            decision = _degrade_ask(result)
    if decision == "note":
        decision = "allow"
    return decision, message


def run(harness: str, event: str, payload_text: str, root: Path, channel: str = "default") -> str:
    """Evaluate one event and return the native effect JSON (never raises).

    ``channel`` is ``default`` except for OpenCode, whose plugin calls the guard
    from ``tool.execute.before`` (``before`` when an evaluate hook is registered) and
    from the permission ``evaluate`` hook (``evaluate``).
    """
    try:
        if channel not in ASK_CHANNELS:
            channel = "default"
        if event != ENFORCED_EVENT:
            # Observe events can never deny (events.json) and no other gate event is
            # rendered yet, so nothing here may block or ask: answer "no opinion".
            return _allow(harness)
        payload = json.loads(payload_text) if payload_text.strip() else {}
        if channel == "evaluate":
            actions = _permission_actions(payload)
        else:
            actions = _actions(payload)
        decision, message = "allow", ""
        for verb, resource in actions or [("", "")]:
            one, text = _decide(root, harness, event, channel, verb, resource)
            if _RANK.get(one, 2) > _RANK[decision]:
                decision, message = one, text
        return _native(harness, decision, message)
    except Exception:  # mechanism failure (D4): allow + advisory, never brick.
        return _allow(harness)


def main(argv: list[str] | None = None) -> int:
    """Parse args, evaluate, print the native effect JSON, exit 0."""
    parser = argparse.ArgumentParser(prog="coacus-guard", description=__doc__)
    parser.add_argument("--harness", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--channel", default="default", choices=ASK_CHANNELS)
    args = parser.parse_args(argv)
    payload = sys.stdin.read()
    print(run(args.harness, args.event, payload, Path(args.root), args.channel))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
