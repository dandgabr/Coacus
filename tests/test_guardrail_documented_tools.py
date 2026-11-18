"""Every tool a harness documents maps to a verb, and the documented payloads are read.

The guard classifies a call by tool name, so a documented name with no verb is a hole:
a rule on that verb would not see it. The names come from each harness's data
(``tool_mapping`` and ``tool_denylist``), so a name added there without a verb here
fails this test. The Antigravity case also runs the real script on its documented
``toolCall`` payload, because a unit test on a flat payload once hid that the guard
could not read the name there at all.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_guard as guard

REPO = Path(__file__).resolve().parents[1]
VERBS = {
    "read a file": "read",
    "search files": "read",
    "create, edit, or delete files": "write",
    "run shell commands": "exec",
    "fetch a url": "network",
    "dispatch a subagent": "spawn",
}
# Documented tools that are neither a file, the network, a shell nor a subagent.
# ``send_message`` and ``agent_output`` are unverified: what they reach is not documented here.
NO_VERB = {
    "antigravity": {"manage_task", "send_message"},
    "claude-code": {"TodoWrite"},
    "codex": {"update_plan"},
    "command-code": {"todo_write", "agent_output"},
    "opencode": {"todowrite"},
}
HARNESSES = ("antigravity", "claude-code", "codex", "cursor", "opencode", "command-code")


def data(harness: str) -> dict:
    return json.loads((REPO / "harnesses" / harness / "harness.json").read_text(encoding="utf-8"))


def names(text: str) -> list[str]:
    """Tool names in one mapping cell: ``a / b``, with any parenthetical dropped."""
    cell = re.sub(r"\([^)]*\)", "", text)
    return [part.strip().strip("`") for part in cell.split("/") if re.fullmatch(r"[`A-Za-z0-9_ -]+", part.strip())]


def call(tool: str, harness: str) -> list[tuple[str, str]]:
    args = {"path": "/p", "url": "u", "command": "c", "prompt": "q", "query": "q"}
    return guard._actions({"tool": tool, "tool_input": args}, harness)


class TestDocumentedToolNames(unittest.TestCase):
    def test_every_mapped_tool_has_its_verb(self) -> None:
        for harness in HARNESSES:
            mapping = data(harness).get("tool_mapping", {})
            checked = {key for key in mapping if key.lower() in VERBS}
            with self.subTest(harness=harness, check="rows"):
                self.assertTrue(checked, f"no checked rows in the {harness} tool_mapping")
            for label in checked:
                for tool in names(mapping[label]):
                    with self.subTest(harness=harness, action=label, tool=tool):
                        self.assertEqual(call(tool, harness)[0][0], VERBS[label.lower()])

    def test_every_denylisted_tool_has_a_verb_or_is_exempt(self) -> None:
        for harness in HARNESSES:
            for tool in data(harness).get("tool_denylist", []):
                if tool in NO_VERB.get(harness, ()) or tool.startswith("mcp"):
                    continue
                with self.subTest(harness=harness, tool=tool):
                    self.assertNotEqual(call(tool, harness)[0][0], "", f"{tool} has no verb")

    def test_the_exemptions_really_have_no_verb(self) -> None:
        for harness, tools in NO_VERB.items():
            for tool in tools:
                with self.subTest(harness=harness, tool=tool):
                    self.assertEqual(call(tool, harness)[0][0], "")

    def test_search_tools_check_the_glob_they_were_given(self) -> None:
        cases = [
            ({"tool": "Grep", "tool_input": {"pattern": "x", "path": "/home/u", "glob": "*.env"}}, "/home/u/*.env"),
            ({"tool": "Glob", "tool_input": {"pattern": "**/.env", "path": "/home/u"}}, "/home/u/**/.env"),
            ({"tool": "grep_search", "tool_input": {"path": "/h", "include": "*.env"}}, "/h/*.env"),
        ]
        for payload, expected in cases:
            with self.subTest(tool=payload["tool"]):
                self.assertIn(("read", expected), guard._actions(payload))

    def test_a_pattern_argument_of_grep_is_a_regex_not_a_glob(self) -> None:
        found = guard._actions({"tool": "Grep", "tool_input": {"pattern": "API_KEY", "path": "/home/u"}})
        self.assertEqual(found, [("read", "/home/u")])


class TestAntigravityPayload(unittest.TestCase):
    """The documented PreToolUse input: ``{"toolCall": {"name": ..., "args": {...}}}``."""

    def test_the_name_and_arguments_are_read_from_the_tool_call(self) -> None:
        cases = [
            ("run_command", {"CommandLine": "cat .env"}, [("exec", "cat .env")]),
            ("view_file", {"AbsolutePath": "/w/.env"}, [("read", "/w/.env")]),
            ("write_to_file", {"TargetFile": "/w/a"}, [("write", "/w/a")]),
            ("multi_replace_file_content", {"TargetFile": "/w/a"}, [("write", "/w/a")]),
            ("read_url_content", {"Url": "http://x"}, [("network", "http://x")]),
            ("search_web", {"Query": "q"}, [("network", "q")]),
        ]
        for tool, args, expected in cases:
            with self.subTest(tool=tool):
                found = guard._actions({"toolCall": {"name": tool, "args": args}}, "antigravity")
                self.assertEqual(found, expected)

    def test_a_malformed_tool_call_never_raises(self) -> None:
        for call_value in (None, 5, "x", [], {"name": 5}, {"name": "view_file", "args": "x"}):
            with self.subTest(call=call_value):
                guard._actions({"toolCall": call_value}, "antigravity")

    def test_the_script_denies_a_documented_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policies = root / "methodology/lifecycle/policies"
            policies.mkdir(parents=True)
            document = {"schema": 1, "enabled": True, "policies": [
                {"id": "no-env", "action": {"verb": "read", "resource": "*/.env"}, "decision": "deny",
                 "message": "blocked"}]}
            (policies / "t.policy.json").write_text(json.dumps(document), encoding="utf-8")
            env = {k: v for k, v in os.environ.items() if k not in ("COACUS_POLICY_DIR", "CI")}
            env["COACUS_POLICY_DIR"] = str(root / "none")
            payload = {"toolCall": {"name": "view_file", "args": {"AbsolutePath": "/w/.env"}}}
            proc = subprocess.run(
                [sys.executable, str(REPO / "scripts/coacus_guard.py"), "--harness", "antigravity",
                 "--event", "tool.pre", "--root", str(root)],
                input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=60)
            self.assertEqual(json.loads(proc.stdout.strip())["decision"], "deny")


if __name__ == "__main__":
    unittest.main()
