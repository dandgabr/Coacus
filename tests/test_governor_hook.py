"""Run the Antigravity Python hook against its real isolated ledger."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import coacus_governor_hook

from engine.governor.ledger import Ledger


ROOT = Path(__file__).resolve().parents[1]


class TestGovernorHook(unittest.TestCase):
    def test_pretool_requires_identifiable_tool_name_without_leaking_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp)
            cases = [
                ({}, "deny"),
                ({"toolCall": {}}, "deny"),
                ({"toolCall": {"name": ""}}, "deny"),
                ({"toolCall": {"name": "  "}}, "deny"),
                ({"toolCall": {"name": "task\nother"}}, "deny"),
                ({"toolCall": {"name": ["synthetic-secret-token"]}}, "deny"),
                ({"toolCall": {"name": {"synthetic-secret-token": 1}}}, "deny"),
                ({"toolCall": {"name": "other"}}, "allow"),
            ]
            for payload, decision in cases:
                with self.subTest(payload=payload):
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), "pretool"],
                        input=json.dumps(payload), text=True, capture_output=True, env=env, check=True,
                    )
                    self.assertEqual(json.loads(result.stdout)["decision"], decision)
                    self.assertNotIn("synthetic-secret-token", result.stdout + result.stderr)

    def test_uncorrelated_spawns_fail_closed_and_post_cannot_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp)
            ledger = Ledger(Path(tmp), scope="antigravity")
            ledger.acquire("agy-test-0", timeout=0)
            for payload in (
                {"toolCall": {"name": "task"}},
                {"toolCall": {"name": "task"}, "conversationId": "test", "stepIdx": 0},
            ):
                for mode in ("pretool", "posttool"):
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), mode],
                        input=json.dumps(payload), text=True, capture_output=True, env=env, check=True,
                    )
                    if mode == "pretool":
                        self.assertEqual(json.loads(result.stdout)["decision"], "deny")
                    self.assertEqual(ledger.status()["running"], 1)

    def test_windows_spawn_denied_without_initializing_ledger(self) -> None:
        for tool, args in (("task", {}), ("invoke_subagent", {}),
                           ("manage_subagents", {"Action": "spawn"}),
                           ("manage_subagents", {"Action": "kill"}),
                           ("manage_subagents", {"Action": "list"}),
                           ("manage_subagents", {"Action": "kill_all"})):
            with self.subTest(tool=tool, args=args), \
                 patch.object(coacus_governor_hook.os, "name", "nt"), \
                 patch("engine.governor.ledger.Ledger", side_effect=AssertionError("must not initialize")) as ledger, \
                 patch.object(sys, "argv", ["hook", "pretool"]), \
                 patch.object(sys, "stdin", io.StringIO(json.dumps({"toolCall": {"name": tool, "args": args}}))), \
                 patch.object(sys, "stdout", new_callable=io.StringIO) as output:
                self.assertEqual(coacus_governor_hook.main(), 0)
                response = json.loads(output.getvalue())
                self.assertEqual(response["decision"], "allow" if args.get("Action") in ("kill", "list", "kill_all") else "deny")
                if response["decision"] == "deny":
                    self.assertIn("correlate", response["reason"])
                ledger.assert_not_called()

    def test_vendor_action_casing_and_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for args, expected in (({"Action": "spawn"}, "deny"),
                                   ({"Action": "kill"}, "allow"),
                                   ({"Action": "spawn", "action": "kill"}, "deny")):
                with self.subTest(args=args), patch.dict(os.environ, {"GOVERNOR_STATE_DIR": tmp}), \
                     patch.object(Ledger, "acquire", return_value="slot"), \
                     patch.object(sys, "argv", ["hook", "pretool"]), \
                     patch.object(sys, "stdin", io.StringIO(json.dumps({"toolCall": {"name": "manage_subagents", "args": args}}))), \
                     patch.object(sys, "stdout", new_callable=io.StringIO) as output:
                    self.assertEqual(coacus_governor_hook.main(), 0)
                    self.assertEqual(json.loads(output.getvalue())["decision"], expected)

    def test_posttool_nonspawn_never_releases_or_parks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for action in ("list", "kill", "kill_all", "unknown"):
                for error in ("", "HTTP 429"):
                    with self.subTest(action=action, error=error), \
                         patch.dict(os.environ, {"GOVERNOR_STATE_DIR": tmp}), \
                         patch.object(Ledger, "release") as release, patch.object(Ledger, "fail") as fail, \
                         patch.object(sys, "argv", ["hook", "posttool"]), \
                         patch.object(sys, "stdin", io.StringIO(json.dumps({"toolCall": {"name": "manage_subagents", "args": {"Action": action}}, "error": error}))), \
                         patch.object(sys, "stdout", new_callable=io.StringIO) as output:
                        self.assertEqual(coacus_governor_hook.main(), 0)
                        self.assertEqual(json.loads(output.getvalue()), {})
                        release.assert_not_called()
                        fail.assert_not_called()

    def test_manage_subagents_actions_with_unavailable_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "not-a-directory"
            state.write_text("x")
            for action in ("spawn", "list", "kill", "kill_all", "unknown", None):
                with self.subTest(action=action):
                    args = {} if action is None else {"action": action}
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), "pretool"],
                        input=json.dumps({"toolCall": {"name": "manage_subagents", "args": args}}),
                        text=True, capture_output=True, env=dict(os.environ, GOVERNOR_STATE_DIR=str(state)),
                        check=True, timeout=5,
                    )
                    expected = "allow" if action in ("list", "kill", "kill_all") else "deny"
                    self.assertEqual(json.loads(result.stdout)["decision"], expected)

    def test_manage_subagents_unknown_action_denied_with_healthy_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
             patch.dict(os.environ, {"GOVERNOR_STATE_DIR": tmp}), \
             patch.object(Ledger, "acquire", return_value="slot") as acquire, \
             patch.object(sys, "argv", ["hook", "pretool"]), \
             patch.object(sys, "stdin", io.StringIO('{"toolCall":{"name":"manage_subagents","args":{"action":"unknown"}}}')), \
             patch.object(sys, "stdout", new_callable=io.StringIO) as output:
            self.assertEqual(coacus_governor_hook.main(), 0)
            self.assertEqual(json.loads(output.getvalue())["decision"], "deny")
            acquire.assert_not_called()

    def test_pretool_denies_ledger_initialization_failure_without_leaking_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "synthetic-secret-token"
            state.write_text("not a directory")
            env = dict(os.environ, GOVERNOR_STATE_DIR=str(state))
            for tool in ("invoke_subagent", "manage_subagents", "task", "other"):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), "pretool"],
                    input=json.dumps({"toolCall": {"name": tool}}), text=True,
                    capture_output=True, env=env, check=True,
                )
                response = json.loads(result.stdout)
                self.assertEqual(response["decision"], "allow" if tool == "other" else "deny")
                if tool != "other":
                    self.assertTrue(response.get("reason"))
                self.assertNotIn("synthetic-secret-token", result.stdout + result.stderr)

    def test_pretool_denies_acquisition_failure_without_leaking_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/coacus_governor_hook.py"), "pretool"],
                input=json.dumps({"toolCall": {"name": "task"}, "conversationId": "synthetic secret token"}),
                text=True, capture_output=True, env=env, check=True,
            )
            response = json.loads(result.stdout)
            self.assertEqual(response["decision"], "deny")
            self.assertTrue(response.get("reason"))
            self.assertNotIn("synthetic secret token", result.stdout + result.stderr)



if __name__ == "__main__":
    unittest.main()
