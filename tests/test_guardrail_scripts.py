"""Tests for the rendered guardrail hook and the PAER runtime evaluator.

These execute the artifacts directly (no live harness needed), so a deny, a
fail-open mechanism failure and the single-JSON contract are proven
deterministically. A live eval would only show that the model reports a denial.
"""

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


def run_guard(
    harness: str, payload: str, root: Path, env: dict[str, str] | None = None
) -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, str(GUARD_CLI), "--harness", harness, "--event", "tool.pre",
         "--root", str(root)],
        input=payload,
        capture_output=True,
        text=True,
        env=env,
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

    def test_antigravity_allow_is_an_explicit_decision(self) -> None:
        # Antigravity requires `decision` on PreToolUse: an empty object is read
        # as a denial, which would block every call.
        out, code = run_guard("antigravity", json.dumps(
            {"tool": "read", "tool_input": {"filePath": "repo/README.md"}}
        ), self.root)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"decision": "allow"})

    def test_antigravity_mechanism_failure_keeps_the_explicit_allow(self) -> None:
        # D4 (fail-open) must still hold where `{}` would be read as a deny.
        out, code = run_guard("antigravity", "not-json", self.root)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"decision": "allow"})

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


ASK_PAYLOAD = json.dumps({"tool": "bash", "tool_input": {"command": "git push origin main"}})
CAN_ASK = {"can_ask": True, "can_block": True}


def ask_root(tmp: str, fallback: str = "deny", capabilities: dict | None = None) -> Path:
    """Build a root with one enabled `ask` policy and optional harness capability data."""
    root = Path(tmp)
    policies = root / "methodology/lifecycle/policies"
    policies.mkdir(parents=True)
    policy = {
        "schema": 1,
        "enabled": True,
        "policies": [{
            "id": "confirm-push",
            "action": {"verb": "exec", "resource": "git push*"},
            "decision": "ask",
            "on_ask_unavailable": fallback,
            "message": "confirm the push",
        }],
    }
    (policies / "ask.policy.json").write_text(json.dumps(policy), encoding="utf-8")
    for harness, capability in (capabilities or {}).items():
        folder = root / "harnesses" / harness
        folder.mkdir(parents=True)
        data = {"lifecycle": {"events": {"tool.pre": capability}}}
        (folder / "harness.json").write_text(json.dumps(data), encoding="utf-8")
    return root


class TestAskCapability(unittest.TestCase):
    """`ask` is rendered only where the harness has a human channel (ADR 0002)."""

    def _run(self, harness, fallback="deny", capabilities=None, env=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = ask_root(tmp, fallback, capabilities)
            out, code = run_guard(harness, ASK_PAYLOAD, root, env)
        self.assertEqual(code, 0)
        self.assertEqual(out.count("\n"), 0)
        return json.loads(out)

    def test_capable_harnesses_render_ask(self) -> None:
        caps = {"claude-code": CAN_ASK, "cursor": CAN_ASK, "antigravity": CAN_ASK}
        claude = self._run("claude-code", capabilities=caps)
        self.assertEqual(claude["hookSpecificOutput"]["permissionDecision"], "ask")
        self.assertEqual(self._run("cursor", capabilities=caps)["permission"], "ask")
        self.assertEqual(self._run("antigravity", capabilities=caps)["decision"], "ask")

    def test_ask_is_not_degraded_by_the_fallback_when_capable(self) -> None:
        caps = {"claude-code": CAN_ASK}
        out = self._run("claude-code", fallback="allow", capabilities=caps)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_incapable_harness_degrades_to_the_policy_fallback(self) -> None:
        caps = {"codex": {"can_ask": False, "can_block": True}}
        denied = self._run("codex", fallback="deny", capabilities=caps)
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(self._run("codex", fallback="allow", capabilities=caps), {})

    def test_missing_capability_data_degrades(self) -> None:
        out = self._run("claude-code", fallback="deny", capabilities={})
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_can_ask_without_can_block_degrades(self) -> None:
        caps = {"claude-code": {"can_ask": True, "can_block": False}}
        out = self._run("claude-code", fallback="deny", capabilities=caps)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_operator_switch_forces_degradation(self) -> None:
        caps = {"claude-code": CAN_ASK}
        env = {**os.environ, "COACUS_GUARD_NO_ASK": "1"}
        out = self._run("claude-code", fallback="deny", capabilities=caps, env=env)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
        env["COACUS_GUARD_NO_ASK"] = "0"
        out = self._run("claude-code", fallback="deny", capabilities=caps, env=env)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_invalid_fallback_fails_closed(self) -> None:
        caps = {"codex": {"can_ask": False, "can_block": True}}
        out = self._run("codex", fallback="ask", capabilities=caps)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_unsafe_harness_name_never_reads_outside_the_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = ask_root(tmp, capabilities={"claude-code": CAN_ASK})
            for name in ("../claude-code", "claude-code/..", "", "a b", "claude\ncode"):
                with self.subTest(name=name):
                    self.assertFalse(coacus_guard._can_ask(root, name, "tool.pre"))

    def test_shipped_capability_data_matches_the_documented_channels(self) -> None:
        expected = {"claude-code": True, "cursor": True, "antigravity": True,
                    "codex": False, "command-code": False, "opencode": False}
        for harness, can_ask in expected.items():
            with self.subTest(harness=harness):
                self.assertIs(coacus_guard._can_ask(REPO, harness, "tool.pre"), can_ask)


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
