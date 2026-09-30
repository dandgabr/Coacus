"""Tests for the rendered guardrail hook and the PAER runtime evaluator.

These execute the artifacts directly (no live harness needed), so a deny, a
fail-open mechanism failure and the single-JSON contract are proven
deterministically. A live eval would only show that the model reports a denial.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.guardrail import evaluate as guard

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"

POLICY = {
    "schema": 1,
    "enabled": True,
    "policies": [
        {
            "id": "no-secret-reads",
            "action": {"verb": "read", "resource": "**/.env"},
            "decision": "deny",
            "on_ask_unavailable": "deny",
            "message": "blocked",
        }
    ],
}


def enabled_root(tmp: str) -> Path:
    root = Path(tmp)
    policies = root / "methodology/lifecycle/policies"
    policies.mkdir(parents=True)
    (policies / "test.policy.json").write_text(json.dumps(POLICY), encoding="utf-8")
    return root


def run_guard(harness: str, payload: str, root: Path) -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, str(GUARD_CLI), "--harness", harness, "--event", "tool.pre",
         "--root", str(root)],
        input=payload,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip(), proc.returncode


class TestGuardRuntime(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = enabled_root(self._tmp.name)

    def test_deny_on_secret_read(self) -> None:
        out, code = run_guard("claude-code", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/.env"}}
        ), self.root)
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(
            payload["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_allow_on_benign_read(self) -> None:
        out, _ = run_guard("claude-code", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/README.md"}}
        ), self.root)
        self.assertEqual(out, "{}")

    def test_mechanism_failure_is_fail_open_not_fail_deny(self) -> None:
        # D4: a broken guard must not deny every call.
        out, code = run_guard("claude-code", "not-json", self.root)
        self.assertEqual(code, 0)
        self.assertEqual(out, "{}")

    def test_stdout_is_exactly_one_json_document(self) -> None:
        out, _ = run_guard("claude-code", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/.env"}}
        ), self.root)
        json.loads(out)  # raises if not a single valid document
        self.assertEqual(out.count("\n"), 0)

    def test_cursor_uses_flat_permission_key(self) -> None:
        out, _ = run_guard("cursor", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/.env"}}
        ), self.root)
        self.assertEqual(json.loads(out)["permission"], "deny")

    def test_antigravity_uses_decision_key(self) -> None:
        out, _ = run_guard("antigravity", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/.env"}}
        ), self.root)
        self.assertEqual(json.loads(out)["decision"], "deny")

    def test_disabled_policy_is_not_enforced(self) -> None:
        # D2: the shipped default set is disabled; nothing is denied.
        out, _ = run_guard("claude-code", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/.env"}}
        ), REPO)
        self.assertEqual(out, "{}")


class TestEvaluator(unittest.TestCase):
    def test_precedence_is_monotonic(self) -> None:
        policies = [
            {"id": "a", "action": {"verb": "exec", "resource": "rm*"}, "decision": "ask"},
            {"id": "b", "action": {"verb": "exec", "resource": "rm -rf /"}, "decision": "deny"},
        ]
        result = guard.evaluate(policies, "exec", "rm -rf /")
        self.assertEqual(result["decision"], "deny")

    def test_no_match_allows(self) -> None:
        result = guard.evaluate([], "read", "anything")
        self.assertEqual(result["decision"], "allow")


if __name__ == "__main__":
    unittest.main()
