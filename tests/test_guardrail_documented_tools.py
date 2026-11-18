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
HARNESSES = tuple(sorted(
    d.name for d in (REPO / "harnesses").iterdir() if (d / "harness.json").is_file() and not d.name.startswith("_")))


def data(harness: str) -> dict:
    return json.loads((REPO / "harnesses" / harness / "harness.json").read_text(encoding="utf-8"))


def names(text: str) -> list[str]:
    """Tool names in one mapping cell: ``a / b``, with any parenthetical dropped."""
    cell = re.sub(r"\([^)]*\)", "", text)
    parts = [part.strip().strip("`") for part in cell.split("/")]
    kept = [part for part in parts if re.fullmatch(r"[A-Za-z0-9_ -]+", part)]
    if len(kept) != len(parts):
        return []  # a cell with prose or a command is not a list of tool names
    return kept


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


    def test_a_patch_header_inside_written_content_never_replaces_the_target(self) -> None:
        cases = [
            ({"toolCall": {"name": "write_to_file", "args": {"TargetFile": "/w/.env",
                                                           "CodeContent": "*** Update File: /tmp/ok\n"}}}, "antigravity"),
            ({"tool": "Write", "tool_input": {"file_path": "/w/.env", "content": "*** Add File: /tmp/ok"}}, "claude-code"),
            ({"tool": "edit", "tool_input": {"filePath": "/w/.env", "newString": "*** Move to: /tmp/ok"}}, "opencode"),
        ]
        for payload, harness in cases:
            with self.subTest(harness=harness):
                self.assertEqual(guard._actions(payload, harness), [("write", "/w/.env")])

    def test_a_real_patch_still_yields_one_write_per_file(self) -> None:
        text = "*** Begin Patch\n*** Update File: /a\n*** Move to: /b\n*** Delete File: /c\n"
        found = guard._actions({"tool": "apply_patch", "tool_input": {"input": text}}, "codex")
        self.assertEqual(found, [("write", "/a"), ("write", "/b"), ("write", "/c")])

    def test_a_list_of_globs_gives_one_read_per_entry(self) -> None:
        payload = {"toolCall": {"name": "grep_search", "args": {"SearchPath": "/h", "Includes": ["*.env", "*.py"]}}}
        self.assertEqual(guard._actions(payload, "antigravity"),
                         [("read", "/h"), ("read", "/h/*.env"), ("read", "/h/*.py")])

    def test_an_absolute_grep_glob_stays_under_the_searched_directory(self) -> None:
        found = guard._actions({"tool": "Grep", "tool_input": {"pattern": "x", "path": "/home/u", "glob": "/.env"}})
        self.assertIn(("read", "/home/u/.env"), found)

    def test_a_glob_tool_keeps_an_absolute_pattern_absolute(self) -> None:
        found = guard._actions({"tool": "find_by_name", "tool_input": {"SearchDirectory": "/h", "Pattern": "/etc/.env"}})
        self.assertIn(("read", "/etc/.env"), found)

    def test_a_rule_fires_for_a_glob_that_names_the_file(self) -> None:
        from engine.guardrail import evaluate as engine
        policy = {"id": "p", "action": {"verb": "read", "resource": "*/.env"}, "decision": "deny"}
        for payload in ({"tool": "Glob", "tool_input": {"pattern": ".env", "path": "/home/u"}},
                        {"tool": "Grep", "tool_input": {"pattern": "x", "path": "/home/u", "glob": ".env"}}):
            decisions = [engine.evaluate([policy], verb, resource)["decision"] for verb, resource in guard._actions(payload)]
            with self.subTest(tool=payload["tool"]):
                self.assertIn("deny", decisions)


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
            ("list_dir", {"DirectoryPath": "/home/u/.ssh"}, [("read", "/home/u/.ssh")]),
        ]
        for tool, args, expected in cases:
            with self.subTest(tool=tool):
                found = guard._actions({"toolCall": {"name": tool, "args": args}}, "antigravity")
                self.assertEqual(found, expected)

    def test_arguments_sent_as_a_json_string_are_decoded(self) -> None:
        payload = {"toolCall": {"name": "view_file", "args": json.dumps({"AbsolutePath": "/w/.env"})}}
        self.assertEqual(guard._actions(payload, "antigravity"), [("read", "/w/.env")])

    def test_odd_names_and_a_nameless_tool_call_still_find_the_tool(self) -> None:
        self.assertEqual(guard._actions({"tool": " view_file\n", "tool_input": {"path": "/a"}}), [("read", "/a")])
        both = {"tool_name": "Read", "tool_input": {"file_path": "/a"}, "toolCall": {}}
        self.assertEqual(guard._actions(both), [("read", "/a")])

    def test_unreadable_arguments_leave_an_empty_resource_not_a_crash(self) -> None:
        payload = {"toolCall": {"name": "view_file", "args": "x"}}
        self.assertEqual(guard._actions(payload, "antigravity"), [("read", "")])

    def test_a_malformed_tool_call_has_no_verb_and_never_raises(self) -> None:
        for call_value in (None, 5, "x", [], {"name": 5}):
            with self.subTest(call=call_value):
                self.assertEqual(guard._actions({"toolCall": call_value}, "antigravity"), [("", "")])

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
