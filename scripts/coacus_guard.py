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

Events: ``tool.pre`` decides, blocks and may ask; ``prompt.submit`` can block a prompt;
``tool.post`` can only add a note for the model (ADR 0016, ADR 0018); any other event
answers "no opinion". On OpenCode an ``ask`` for a read or write is decided through the permission ``evaluate``
hook, and the harness approves it by itself under ``--auto``.

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
import posixpath
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
              "view", "cat", "search_files", "find_files", "grep_search", "find_by_name",
              "list_dir"}
# Read tools that scan a directory: a rule on a file name never sees the files inside
# the directory they were pointed at, so the glob they were given is checked as well.
PATCH_TOOLS = {"apply_patch", "patch"}
SEARCH_TOOLS = {"grep", "glob", "grep_search", "find_by_name", "search_files", "find_files"}
GLOB_KEYS = ("glob", "include", "Includes", "Pattern")
# For these the ``pattern`` argument is itself a file glob (for ``grep`` it is a regex).
GLOB_TOOLS = {"glob", "find_by_name", "find_files"}
WRITE_TOOLS = {"write", "edit", "write_file", "edit_file", "apply_patch", "write_to_file",
               "replace_file_content", "multiedit", "patch", "notebookedit", "str_replace_editor",
               "create_file", "delete_file", "multi_replace_file_content"}
EXEC_TOOLS = {"bash", "shell", "shell_command", "run_command", "terminal", "exec", "execute"}
NETWORK_TOOLS = {"fetch", "webfetch", "web_fetch", "read_url_content", "fetch_url", "websearch",
                 "web_search", "search_web"}
SPAWN_TOOLS = {"task", "agent", "spawn_agent", "invoke_subagent", "manage_subagents", "subagent"}
# Tools served by an MCP server: Claude Code sends ``mcp__server__tool``, Cursor ``MCP:tool``.
MCP_PREFIXES = ("mcp_", "mcp:")
# OpenCode names an MCP tool ``<server>_<tool>``, so its own tools are told apart by exact
# name, never by the shared tables: a server called ``web`` serving ``fetch`` arrives as
# ``web_fetch``, which the shared tables would call a network tool. ``apply_patch`` is the
# one native name with an underscore.
OPENCODE_NATIVE = {"read", "grep", "glob", "list", "write", "edit", "patch", "apply_patch",
                   "multiedit", "shell", "bash", "execute", "webfetch", "websearch", "task"}
# OpenCode tools that are not MCP and have no verb here (no rule can name them).
OPENCODE_UNCLASSIFIED = {"todowrite", "todoread", "skill", "question", "lsp", "batch"}
_PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.MULTILINE)


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


def _norm(path: str) -> str:
    """Collapse ``./``, ``//`` and ``x/../`` so a spelling cannot dodge a path pattern.

    Symlinks and letter case are not resolved: a pattern sees the path as the tool sent it.
    """
    return posixpath.normpath(path) if path and "\\" not in path else path


def _globs(args: dict, keys: tuple[str, ...]) -> list[str]:
    """Every glob a search call carries: a string, or each entry of a list of strings."""
    out: list[str] = []
    for key in keys:
        value = args.get(key)
        for item in value if isinstance(value, (list, tuple)) else [value]:
            if isinstance(item, str) and item.strip() and item not in out:
                out.append(item)
    return out


def _patch_paths(args: dict) -> list[str]:
    """File paths named inside an ``apply_patch`` style patch text, in order.

    Only for the patch tools: a ``write`` or ``edit`` carries file content, and content
    that spells a patch header must never replace the path the tool really writes.
    """
    for value in args.values():
        if isinstance(value, str):
            found = [(a or b).strip() for a, b in _PATCH_FILE.findall(value)]
            if found:
                return found
    return []


def _actions(payload: dict, harness: str = "") -> list[tuple[str, str]]:
    """Map a native payload to canonical ``(verb, resource)`` pairs.

    Usually one. A patch that touches several files yields one write per file, so a
    policy on any of them is consulted. On OpenCode an MCP tool arrives as
    ``<server>_<tool>`` (observed on 2.3.0), so any tool that is not in its exact native
    list is an ``mcp`` action named by that raw tool name.
    """
    call = payload.get("toolCall")
    tool = ""
    if isinstance(call, dict):
        # Antigravity: {"toolCall": {"name": ..., "args": {...}}} (its documented PreToolUse input).
        tool = _first(call, ("name", "tool")).strip().lower()
        args = call.get("args") or {}
    if not tool:
        tool = _first(payload, ("tool", "tool_name", "toolName", "name")).strip().lower()
        args = payload.get("tool_input") or payload.get("args") or call or {}
    if isinstance(args, str):
        try:
            decoded = json.loads(args)
        except ValueError:
            decoded = None
        args = decoded if isinstance(decoded, dict) else {"input": args}
    if not isinstance(args, dict):
        args = {}
    # The capitalised spellings are Antigravity's style (``CommandLine``); only that one is
    # confirmed, the rest are unverified (see the antigravity gap in harness.json).
    path = _first(args, ("filePath", "file_path", "path", "target_file", "notebook_path", "AbsolutePath",
                         "TargetFile", "SearchPath", "SearchDirectory", "DirectoryPath", "pattern"))
    command = _first(args, ("command", "CommandLine", "cmd"))
    if tool.startswith(MCP_PREFIXES):
        return [("mcp", tool)]  # the tool's own name; its arguments have no common shape
    if harness == "opencode" and tool:
        if tool in OPENCODE_UNCLASSIFIED:
            return [("", "")]
        if tool not in OPENCODE_NATIVE:
            return [("mcp", tool)]
        if tool == "execute":
            # Code mode: it carries code, not a command, and the code can reach the network
            # itself. A rule can name it as an mcp action; command rules cannot read it.
            return [("exec", command), ("mcp", tool)]
    if tool in READ_TOOLS:
        found = [("read", _norm(path))]
        if tool in SEARCH_TOOLS:
            keys = GLOB_KEYS + (("pattern",) if tool in GLOB_TOOLS else ())
            for glob in _globs(args, keys):
                if glob == path:
                    continue
                # A search glob is relative to the directory searched, even with a leading
                # slash (ripgrep reads ``/.env`` as ``<dir>/.env``); a find tool's absolute
                # pattern is absolute, so that one is kept as given.
                rooted = glob if tool in GLOB_TOOLS and glob.startswith("/") else glob.lstrip("/")
                found.append(("read", _norm(posixpath.join(path, rooted)) if path and path != glob else rooted))
        return found
    if tool in WRITE_TOOLS:
        patched = _patch_paths(args) if tool in PATCH_TOOLS else []
        if patched:
            return [("write", _norm(item)) for item in patched]
        return [("write", _norm(path))]
    if tool in EXEC_TOOLS:
        return [("exec", command)]
    if tool in NETWORK_TOOLS:
        return [("network", _first(args, ("url", "uri", "query", "Url", "URL", "Query")))]
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


def _prompt_effect(harness: str, decision: str, message: str) -> str:
    """Render the answer to ``prompt.submit``: a block with a reason, or no opinion.

    Claude Code stops the prompt with ``{"decision": "block", "reason": ...}`` and shows the
    reason to the user. A prompt is never asked about: nothing here can reach a human.
    """
    if decision == "allow" or harness != "claude-code":
        return "{}"
    # By default Claude Code appends the original prompt to the block message and keeps it in
    # the transcript; suppress the echo so a blocked secret is not printed back.
    return json.dumps({
        "decision": "block",
        "reason": message or "Blocked by a Coacus guardrail policy.",
        "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "suppressOriginalPrompt": True},
    })


OUTPUT_NOTE_CHARS = 2000
OUTPUT_WINDOW_CHARS = guard._MAX_COMMAND_CHARS - 10  # a longer value would match every pattern
OUTPUT_WINDOW_OVERLAP = 4096  # a marker up to this long cannot fall between two windows
OUTPUT_MAX_CHARS = 8_000_000  # beyond this the rest of an output is not read


def _output_text(payload: object) -> str:
    """The text a tool returned, from the ``tool_response`` of a ``PostToolUse`` payload.

    The shape differs per tool and the documentation gives only Bash (``stdout`` and
    ``stderr``). Any other value is scanned as its JSON text, which escapes quotes and
    newlines, so a pattern that needs those does not match there.
    """
    response = payload.get("tool_response") if isinstance(payload, dict) else None
    if isinstance(response, dict) and any(isinstance(response.get(k), str) for k in ("stdout", "stderr")):
        text = "\n".join(str(response.get(k) or "") for k in ("stdout", "stderr"))
    elif isinstance(response, str):
        text = response
    elif response is None:
        text = ""
    else:
        text = json.dumps(response, ensure_ascii=False, sort_keys=True, default=str)
    return text


def _output_windows(text: str) -> list[str]:
    """Split a folded output into overlapping windows that each fit under the match cap."""
    text = guard._fold_prompt(text)[:OUTPUT_MAX_CHARS]
    step = OUTPUT_WINDOW_CHARS - OUTPUT_WINDOW_OVERLAP
    return [text[start:start + OUTPUT_WINDOW_CHARS] for start in range(0, max(len(text), 1), step)]


def _output_effect(harness: str, decision: str, message: str) -> str:
    """Render the answer to ``tool.post``: a note for the model, never a block.

    The tool has already run, so there is nothing to refuse. Claude Code puts
    ``additionalContext`` next to the tool result; anything but an allow becomes that note.
    """
    if decision == "allow" or harness != "claude-code":
        return _allow(harness)
    note = (message or "A Coacus guardrail policy matched this tool output.")[:OUTPUT_NOTE_CHARS]
    return json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}})


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

# Events the guard decides on (ADR 0012, ADR 0016). ``prompt.submit`` has a hook only
# where the harness data names a native hook for it, and only when an enabled policy
# binds the event; every other event answers "no opinion".
ENFORCED_EVENT = "tool.pre"
PROMPT_EVENT = "prompt.submit"
OUTPUT_EVENT = "tool.post"
ENFORCED_EVENTS = (ENFORCED_EVENT, PROMPT_EVENT, OUTPUT_EVENT)

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
    name, an event other than ``tool.pre`` (rendered, with prompt.submit and tool.post), missing or
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
        # Seen live on OpenCode 2.3.0 (ADR 0010). Under --auto that harness approves an ask
        # by itself, which this process cannot detect, so only a deny is a barrier there.
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
        if event not in ENFORCED_EVENTS:
            # Observe events can never deny (events.json) and no other gate event is
            # rendered yet, so nothing here may block or ask: answer "no opinion".
            return _allow(harness)
        payload = json.loads(payload_text) if payload_text.strip() else {}
        if event == PROMPT_EVENT:
            text = payload.get("prompt") if isinstance(payload, dict) else None
            named = payload.get("hook_event_name") if isinstance(payload, dict) else None
            decision, message = "allow", ""
            if isinstance(text, str) and text and named in (None, "UserPromptSubmit"):
                decision, message = _decide(root, harness, event, "default", "prompt", text)
                if decision != "allow" and len(text) > guard._MAX_COMMAND_CHARS:
                    message = (f"This prompt is longer than {guard._MAX_COMMAND_CHARS} characters, which a prompt "
                               f"rule cannot scan, so it is blocked as a whole. {message}").strip()
            return _prompt_effect(harness, decision, message)
        if event == OUTPUT_EVENT:
            named = payload.get("hook_event_name") if isinstance(payload, dict) else None
            text = _output_text(payload) if named in (None, "PostToolUse") else ""
            decision, message = "allow", ""
            if text:
                policies = guard.load_policies(root, include_user=True)
                found = []
                for window in _output_windows(text):
                    found = guard.notes(policies, "output", window, event)
                    if found:
                        break
                if found:
                    decision, message = "note", " ".join(m for m in found if m)
            return _output_effect(harness, decision, message)
        if channel == "evaluate":
            actions = _permission_actions(payload)
        else:
            actions = _actions(payload, harness)
        decision, message = "allow", ""
        for verb, resource in actions or [("", "")]:
            one, text = _decide(root, harness, event, channel, verb, resource)
            if _RANK.get(one, 2) > _RANK[decision]:
                decision, message = one, text
        return _native(harness, decision, message)
    except Exception as exc:  # mechanism failure (D4): allow + advisory, never brick.
        sys.stderr.write(f"coacus-guard: mechanism failure ({type(exc).__name__}); allowing\n")
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
