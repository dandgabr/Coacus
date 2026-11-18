"""The ``mcp`` verb: a policy can constrain a tool served by an MCP server by name."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.guardrail import evaluate as guard
from scripts import coacus_guard

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"


def policy(resource: str, decision: str = "deny") -> dict:
    return {"id": "p", "action": {"verb": "mcp", "resource": resource}, "decision": decision,
            "on_ask_unavailable": "deny"}


class TestClassification(unittest.TestCase):
    def test_mcp_names_become_the_mcp_verb(self) -> None:
        for tool in ("mcp__playwright__browser_navigate", "MCP__Server__Tool", "MCP:some_tool", "mcp:x"):
            with self.subTest(tool=tool):
                verb, resource = coacus_guard._actions({"tool": tool, "tool_input": {"url": "x"}})[0]
                self.assertEqual(verb, "mcp")
                self.assertEqual(resource, tool.lower())

    def test_native_and_unknown_tools_keep_their_verbs(self) -> None:
        self.assertEqual(coacus_guard._actions({"tool": "Bash", "tool_input": {"command": "ls"}})[0][0], "exec")
        self.assertEqual(coacus_guard._actions({"tool": "Read", "tool_input": {"path": "a"}})[0][0], "read")
        self.assertEqual(coacus_guard._actions({"tool": "mcpish", "tool_input": {}})[0], ("", ""))
        # Antigravity documents mcp_<server>_<tool>; the prefix is classified though unproven.
        self.assertEqual(coacus_guard._actions({"tool": "mcp_probe_echo"})[0], ("mcp", "mcp_probe_echo"))


class TestOpenCodeNames(unittest.TestCase):
    """OpenCode 2.3.0 sends an MCP tool as ``<server>_<tool>``, observed in a live run."""

    def test_a_non_native_tool_is_an_mcp_action_on_opencode_only(self) -> None:
        payload = {"tool": "probe_echo", "tool_input": {"text": "hi"}}
        self.assertEqual(coacus_guard._actions(payload, "opencode"), [("mcp", "probe_echo")])
        self.assertEqual(coacus_guard._actions(payload, "claude-code"), [("", "")])
        self.assertEqual(coacus_guard._actions(payload), [("", "")])

    def test_native_opencode_tools_keep_their_verbs(self) -> None:
        for tool, args, verb in (("shell", {"command": "ls"}, "exec"), ("read", {"path": "a"}, "read"),
                                 ("write", {"path": "a", "content": "x"}, "write")):
            with self.subTest(tool=tool):
                self.assertEqual(coacus_guard._actions({"tool": tool, "tool_input": args}, "opencode")[0][0], verb)

    def test_the_fallback_names_the_tool_not_a_constant(self) -> None:
        for tool in ("other_tool", "web_fetch", "files_read", "docs_search"):
            with self.subTest(tool=tool):
                self.assertEqual(coacus_guard._actions({"tool": tool}, "opencode"), [("mcp", tool)])

    def test_an_mcp_tool_named_like_a_native_one_still_gets_its_mcp_rule(self) -> None:
        # A server called ``web`` serving ``fetch`` arrives as web_fetch, which the shared
        # tables call a network tool; a ``shell``-like server tool as ``run_command``.
        for tool in ("web_fetch", "web_search", "run_command", "read_file", "write_file", "str_replace_editor"):
            with self.subTest(tool=tool):
                self.assertEqual(coacus_guard._actions({"tool": tool, "tool_input": {"url": "x"}}, "opencode"),
                                 [("mcp", tool)])
                self.assertNotEqual(coacus_guard._actions({"tool": tool, "tool_input": {}}, "claude-code")[0][0], "mcp")

    def test_native_tools_without_a_verb_are_not_mcp(self) -> None:
        for tool in sorted(coacus_guard.OPENCODE_UNCLASSIFIED):
            with self.subTest(tool=tool):
                self.assertEqual(coacus_guard._actions({"tool": tool, "tool_input": {}}, "opencode"), [("", "")])

    def test_every_native_name_keeps_the_verb_the_shared_tables_give_it(self) -> None:
        for tool in sorted(coacus_guard.OPENCODE_NATIVE - {"execute"}):
            with self.subTest(tool=tool):
                self.assertNotEqual(coacus_guard._actions({"tool": tool, "tool_input": {}}, "opencode")[0][0], "mcp")

    def test_execute_is_both_exec_and_a_nameable_mcp_action(self) -> None:
        actions = coacus_guard._actions({"tool": "execute", "tool_input": {"code": "return 1"}}, "opencode")
        self.assertEqual(actions, [("exec", ""), ("mcp", "execute")])
        self.assertEqual(guard.evaluate([policy("execute")], "mcp", "execute")["decision"], "deny")

    def test_only_opencode_gets_the_fallback(self) -> None:
        payload = {"tool": "other_tool"}
        for harness in ("claude-code", "codex", "cursor", "antigravity", "command-code", ""):
            with self.subTest(harness=harness):
                self.assertEqual(coacus_guard._actions(payload, harness), [("", "")])

    def test_an_mcp_permission_on_the_evaluate_channel_maps_to_nothing(self) -> None:
        # The deny holds through the before hook; an ask on an mcp tool falls back to its
        # on_ask_unavailable value because only a read or a write is deferred to evaluate.
        self.assertEqual(coacus_guard._permission_actions({"action": "probe_echo", "resources": ["x"]}), [])

    def test_an_empty_tool_name_stays_without_a_verb(self) -> None:
        self.assertEqual(coacus_guard._actions({"tool_input": {}}, "opencode"), [("", "")])

    def test_the_cli_denies_an_opencode_mcp_tool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "methodology/lifecycle/policies"
            directory.mkdir(parents=True)
            (directory / "a.policy.json").write_text(
                json.dumps({"schema": 1, "enabled": True, "policies": [policy("probe_*")]}), encoding="utf-8")
            env = {k: v for k, v in os.environ.items() if k not in ("COACUS_POLICY_DIR", "CI")}
            env["COACUS_POLICY_DIR"] = str(root / "none")
            proc = subprocess.run(
                [sys.executable, str(GUARD_CLI), "--harness", "opencode", "--event", "tool.pre",
                 "--channel", "before", "--root", str(root)],
                input=json.dumps({"tool": "probe_echo", "tool_input": {}}),
                capture_output=True, text=True, env=env, timeout=60)
            self.assertEqual(json.loads(proc.stdout)["decision"], "deny")


class TestMatching(unittest.TestCase):
    def decide(self, rule: dict, tool: str) -> str:
        return guard.evaluate([rule], "mcp", tool)["decision"]

    def test_a_server_glob_denies_its_tools_only(self) -> None:
        rule = policy("mcp__playwright__*")
        self.assertEqual(self.decide(rule, "mcp__playwright__browser_navigate"), "deny")
        self.assertEqual(self.decide(rule, "mcp__rea__open_binary"), "allow")

    def test_matching_ignores_case_on_both_sides(self) -> None:
        self.assertEqual(self.decide(policy("mcp__Playwright__*"), "mcp__playwright__browser_click"), "deny")
        self.assertEqual(self.decide(policy("mcp__playwright__*"), "MCP__PLAYWRIGHT__BROWSER_CLICK"), "deny")

    def test_an_exact_tool_name_is_enough(self) -> None:
        rule = policy("mcp__rea__push_adb_file")
        self.assertEqual(self.decide(rule, "mcp__rea__push_adb_file"), "deny")
        self.assertEqual(self.decide(rule, "mcp__rea__pull_adb_file"), "allow")

    def test_an_mcp_rule_never_fires_on_another_verb(self) -> None:
        self.assertEqual(guard.evaluate([policy("*playwright*")], "exec", "mcp__playwright__x")["decision"], "allow")
        read_rule = {"id": "r", "action": {"verb": "read", "resource": "mcp__*"}, "decision": "deny"}
        self.assertEqual(guard.evaluate([read_rule], "mcp", "mcp__x__y")["decision"], "allow")

    def test_case_folding_is_limited_to_the_mcp_verb(self) -> None:
        for verb in ("write", "read", "exec", "network", "spawn"):
            with self.subTest(verb=verb):
                rule = {"id": "w", "action": {"verb": verb, "resource": "SECRET.txt"}, "decision": "deny"}
                self.assertEqual(guard.evaluate([rule], verb, "secret.txt")["decision"], "allow")

    def test_a_star_server_star_pattern_spans_the_harness_naming_schemes(self) -> None:
        rule = policy("*playwright*")
        for tool in ("mcp__playwright__browser_click", "playwright_browser_click", "mcp_playwright_browser_click"):
            with self.subTest(tool=tool):
                self.assertEqual(self.decide(rule, tool), "deny")
        # Cursor sends no server name, so a rule cannot tell servers apart there.
        self.assertEqual(self.decide(rule, "MCP:browser_click"), "allow")
        self.assertEqual(self.decide(policy("mcp__playwright__*"), "playwright_browser_click"), "allow")

    def test_ask_falls_back_where_nobody_can_be_asked(self) -> None:
        result = guard.evaluate([policy("mcp__x__*", "ask")], "mcp", "mcp__x__y")
        self.assertEqual((result["decision"], result["on_ask_unavailable"]), ("ask", "deny"))


class TestEndToEnd(unittest.TestCase):
    def test_the_printed_json_denies_an_mcp_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "methodology/lifecycle/policies"
            directory.mkdir(parents=True)
            (directory / "a.policy.json").write_text(
                json.dumps({"schema": 1, "enabled": True, "policies": [policy("mcp__blocked__*")]}),
                encoding="utf-8")
            env = {k: v for k, v in os.environ.items()
                   if k not in ("COACUS_POLICY_DIR", "CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
            env["COACUS_POLICY_DIR"] = str(root / "none")

            def run(tool: str) -> dict:
                proc = subprocess.run(
                    [sys.executable, str(GUARD_CLI), "--harness", "claude-code", "--event", "tool.pre",
                     "--root", str(root)],
                    input=json.dumps({"tool_name": tool, "tool_input": {"x": 1}}),
                    capture_output=True, text=True, env=env, timeout=60)
                return json.loads(proc.stdout.strip())

            self.assertEqual(run("mcp__blocked__go")["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertEqual(run("mcp__other__go"), {})


class TestDocumentedCoverage(unittest.TestCase):
    def test_every_harness_without_documented_mcp_coverage_declares_a_gap(self) -> None:
        for harness in ("codex", "opencode", "antigravity", "cursor"):
            data = json.loads((REPO / f"harnesses/{harness}/harness.json").read_text(encoding="utf-8"))
            reasons = [g["reason"] for g in data["lifecycle"]["gaps"] if g["event"] == "tool.pre"]
            with self.subTest(harness=harness):
                self.assertTrue(any("MCP" in r for r in reasons))


if __name__ == "__main__":
    unittest.main()
