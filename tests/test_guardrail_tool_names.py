"""Tool names are matched without regard to case, and one bad policy file is not fatal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_guard

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"
DENY_ENV = {"id": "deny-env", "action": {"verb": "read", "resource": "*.env"}, "decision": "deny"}
DENY_WRITE = {"id": "deny-write", "action": {"verb": "write", "resource": "*.env"}, "decision": "deny"}


class TestToolNames(unittest.TestCase):
    def test_case_does_not_change_the_verb(self) -> None:
        for name in ("Read", "read", "READ", "Grep", "Glob", "NotebookRead"):
            with self.subTest(tool=name):
                verb = coacus_guard._action({"tool": name, "tool_input": {"path": "a.env"}})[0]
                self.assertEqual(verb, "read")
        for name in ("Write", "Edit", "MultiEdit", "NotebookEdit", "patch", "Patch"):
            with self.subTest(tool=name):
                self.assertEqual(coacus_guard._action({"tool": name, "tool_input": {"file_path": "a.env"}})[0], "write")
        self.assertEqual(coacus_guard._action({"tool": "WebSearch", "tool_input": {"query": "q"}})[0], "network")
        self.assertEqual(coacus_guard._action({"tool": "Agent", "tool_input": {"prompt": "p"}})[0], "spawn")

    def test_a_patch_names_every_file_it_touches(self) -> None:
        patch = "*** Begin Patch\n*** Update File: a.py\n*** Add File: secret.env\n*** End Patch"
        for shape in ({"tool_input": patch}, {"tool_input": {"input": patch}}, {"args": {"patch": patch}}):
            with self.subTest(shape=list(shape)):
                actions = coacus_guard._actions({"tool": "apply_patch", **shape})
                self.assertEqual(actions, [("write", "a.py"), ("write", "secret.env")])

    def test_unknown_tools_have_no_verb(self) -> None:
        self.assertEqual(coacus_guard._actions({"tool": "some_unlisted_tool", "tool_input": {}}), [("", "")])


class TestGuardEndToEnd(unittest.TestCase):
    def _run(self, payload: dict, files: dict[str, bytes]) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policies = root / "methodology/lifecycle/policies"
            policies.mkdir(parents=True)
            for name, data in files.items():
                (policies / name).write_bytes(data)
            proc = subprocess.run(
                [sys.executable, str(GUARD_CLI), "--harness", "claude-code", "--event", "tool.pre", "--root", str(root)],
                input=json.dumps(payload), capture_output=True, text=True, timeout=60,
                env={"PATH": "/usr/bin:/bin", "COACUS_POLICY_DIR": str(root / "none")})
            return json.loads(proc.stdout.strip())

    @staticmethod
    def _decision(out: dict) -> str:
        return out.get("hookSpecificOutput", {}).get("permissionDecision", "none")

    def test_title_case_tools_are_denied(self) -> None:
        doc = json.dumps({"enabled": True, "policies": [DENY_ENV, DENY_WRITE]}).encode()
        for tool, args in (("Read", {"file_path": "a.env"}), ("Grep", {"path": "a.env"}),
                           ("MultiEdit", {"file_path": "a.env"})):
            with self.subTest(tool=tool):
                self.assertEqual(self._decision(self._run({"tool": tool, "tool_input": args},
                                                         {"a.policy.json": doc})), "deny")

    def test_a_multi_file_patch_is_denied_when_any_file_is(self) -> None:
        doc = json.dumps({"enabled": True, "policies": [DENY_WRITE]}).encode()
        patch = "*** Begin Patch\n*** Update File: a.py\n*** Add File: secret.env\n*** End Patch"
        out = self._run({"tool_name": "apply_patch", "tool_input": patch}, {"a.policy.json": doc})
        self.assertEqual(self._decision(out), "deny")

    def test_a_bad_policy_file_does_not_switch_the_good_ones_off(self) -> None:
        good = json.dumps({"enabled": True, "policies": [DENY_ENV]}).encode()
        for name, data in (("0.policy.json", b"[]"), ("1.policy.json", b"\xff\xfe"),
                           ("2.policy.json", json.dumps({"enabled": True, "policies": None}).encode()),
                           ("3.policy.json", json.dumps({"enabled": True, "policies": [{"action": "exec"}]}).encode())):
            with self.subTest(bad=name):
                out = self._run({"tool": "read", "tool_input": {"file_path": "a.env"}},
                                {name: data, "9.policy.json": good})
                self.assertEqual(self._decision(out), "deny")


if __name__ == "__main__":
    unittest.main()
