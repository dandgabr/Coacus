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
from unittest import mock

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
ASK_VARS = ("COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK", "CI")


def clean_env(**extra: str) -> dict[str, str]:
    """Return the process environment without the ask switches, plus ``extra``."""
    env = {k: v for k, v in os.environ.items() if k not in ASK_VARS}
    env.update(extra)
    return env


def ask_root(tmp: str, fallback: str | None = "deny", capabilities: dict | None = None) -> Path:
    """Build a root with one enabled `ask` policy and optional harness capability data."""
    root = Path(tmp)
    policies = root / "methodology/lifecycle/policies"
    policies.mkdir(parents=True)
    entry = {
        "id": "confirm-push",
        "action": {"verb": "exec", "resource": "git push*"},
        "decision": "ask",
        "message": "confirm the push",
    }
    if fallback is not None:
        entry["on_ask_unavailable"] = fallback
    policy = {"schema": 1, "enabled": True, "policies": [entry]}
    (policies / "ask.policy.json").write_text(json.dumps(policy), encoding="utf-8")
    for harness, capability in (capabilities or {}).items():
        write_harness(root, harness, {"lifecycle": {"events": {"tool.pre": capability}}})
    return root


def write_harness(root: Path, harness: str, data: object) -> None:
    """Write ``data`` as the harness.json of ``harness`` under ``root``."""
    folder = root / "harnesses" / harness
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "harness.json").write_text(json.dumps(data), encoding="utf-8")


def can_ask(root: Path, harness: str, event: str = "tool.pre", **env: str) -> bool:
    """Call the capability check with a controlled environment."""
    with mock.patch.dict(os.environ, clean_env(**env), clear=True):
        return coacus_guard._can_ask(root, harness, event)


def decision_of(output: dict) -> str:
    """Return the decision word of a native effect, whatever the harness shape."""
    if "hookSpecificOutput" in output:
        return output["hookSpecificOutput"]["permissionDecision"]
    return output.get("permission") or output.get("decision") or "none"


class TestAskCapability(unittest.TestCase):
    """`ask` is rendered only on opt-in and only where the harness has a human channel."""

    def _run(self, harness, fallback="deny", capabilities=None, **env):
        with tempfile.TemporaryDirectory() as tmp:
            root = ask_root(tmp, fallback, capabilities)
            out, code = run_guard(harness, ASK_PAYLOAD, root, clean_env(**env))
        self.assertEqual(code, 0)
        self.assertEqual(out.count("\n"), 0)
        return json.loads(out)

    def test_default_degrades_even_when_the_harness_is_capable(self) -> None:
        out = self._run("claude-code", capabilities={"claude-code": CAN_ASK})
        self.assertEqual(decision_of(out), "deny")

    def test_opted_in_capable_harnesses_render_ask(self) -> None:
        caps = {"claude-code": CAN_ASK, "cursor": CAN_ASK, "antigravity": CAN_ASK}
        for harness in caps:
            with self.subTest(harness=harness):
                out = self._run(harness, capabilities=caps, COACUS_GUARD_ASK="1")
                self.assertEqual(decision_of(out), "ask")

    def test_opt_in_needs_exactly_one(self) -> None:
        caps = {"claude-code": CAN_ASK}
        for value in ("", "0", "true", "yes", "2", "ask"):
            with self.subTest(value=value):
                out = self._run("claude-code", capabilities=caps, COACUS_GUARD_ASK=value)
                self.assertEqual(decision_of(out), "deny")

    def test_opt_in_tolerates_surrounding_whitespace(self) -> None:
        out = self._run("claude-code", capabilities={"claude-code": CAN_ASK}, COACUS_GUARD_ASK=" 1 ")
        self.assertEqual(decision_of(out), "ask")

    def test_off_switches_always_win(self) -> None:
        caps = {"claude-code": CAN_ASK}
        for extra in ({"COACUS_GUARD_NO_ASK": "1"}, {"CI": "true"}, {"CI": "1"}):
            with self.subTest(extra=extra):
                out = self._run("claude-code", capabilities=caps, COACUS_GUARD_ASK="1", **extra)
                self.assertEqual(decision_of(out), "deny")
        for extra in ({"COACUS_GUARD_NO_ASK": " 0 "}, {"COACUS_GUARD_NO_ASK": " "},
                      {"CI": "false"}, {"CI": "0"}):
            with self.subTest(extra=extra):
                out = self._run("claude-code", capabilities=caps, COACUS_GUARD_ASK="1", **extra)
                self.assertEqual(decision_of(out), "ask")

    def test_ask_is_not_degraded_by_the_fallback_when_it_can_be_asked(self) -> None:
        out = self._run("claude-code", fallback="allow", capabilities={"claude-code": CAN_ASK},
                        COACUS_GUARD_ASK="1")
        self.assertEqual(decision_of(out), "ask")

    def test_incapable_harness_degrades_to_the_policy_fallback(self) -> None:
        caps = {"codex": {"can_ask": False, "can_block": True}}
        denied = self._run("codex", fallback="deny", capabilities=caps, COACUS_GUARD_ASK="1")
        self.assertEqual(decision_of(denied), "deny")
        allowed = self._run("codex", fallback="allow", capabilities=caps, COACUS_GUARD_ASK="1")
        self.assertEqual(allowed, {})

    def test_missing_capability_data_degrades(self) -> None:
        out = self._run("claude-code", capabilities={}, COACUS_GUARD_ASK="1")
        self.assertEqual(decision_of(out), "deny")

    def test_invalid_or_missing_fallback_fails_closed(self) -> None:
        caps = {"codex": {"can_ask": False, "can_block": True}}
        for fallback in ("ask", "note", "", None):
            with self.subTest(fallback=fallback):
                out = self._run("codex", fallback=fallback, capabilities=caps, COACUS_GUARD_ASK="1")
                self.assertEqual(decision_of(out), "deny")

    def test_degrade_ask_helper(self) -> None:
        self.assertEqual(coacus_guard._degrade_ask({}), "deny")
        self.assertEqual(coacus_guard._degrade_ask({"on_ask_unavailable": None}), "deny")
        self.assertEqual(coacus_guard._degrade_ask({"on_ask_unavailable": "note"}), "deny")
        self.assertEqual(coacus_guard._degrade_ask({"on_ask_unavailable": "allow"}), "allow")
        self.assertEqual(coacus_guard._degrade_ask({"on_ask_unavailable": "deny"}), "deny")


class TestCanAskGate(unittest.TestCase):
    """Direct checks of the capability gate: every doubt answers False."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def test_both_flags_must_be_exactly_true(self) -> None:
        for bad in ("true", 1, [1], {"x": 1}, None, 0):
            for key in ("can_ask", "can_block"):
                capability = {"can_ask": True, "can_block": True, key: bad}
                with self.subTest(key=key, value=repr(bad)):
                    write_harness(self.root, "claude-code", {"lifecycle": {"events": {"tool.pre": capability}}})
                    self.assertFalse(can_ask(self.root, "claude-code", COACUS_GUARD_ASK="1"))
        write_harness(self.root, "claude-code", {"lifecycle": {"events": {"tool.pre": CAN_ASK}}})
        self.assertTrue(can_ask(self.root, "claude-code", COACUS_GUARD_ASK="1"))

    def test_the_event_must_match(self) -> None:
        events = {"tool.pre": CAN_ASK, "tool.post": {"can_ask": False, "can_block": False}}
        write_harness(self.root, "claude-code", {"lifecycle": {"events": events}})
        self.assertTrue(can_ask(self.root, "claude-code", "tool.pre", COACUS_GUARD_ASK="1"))
        self.assertFalse(can_ask(self.root, "claude-code", "tool.post", COACUS_GUARD_ASK="1"))
        self.assertFalse(can_ask(self.root, "claude-code", "no.such.event", COACUS_GUARD_ASK="1"))

    def test_malformed_capability_files_degrade_without_raising(self) -> None:
        folder = self.root / "harnesses" / "claude-code"
        folder.mkdir(parents=True)
        target = folder / "harness.json"
        bodies = [
            "not json",
            '{"lifecycle": []}',
            '{"lifecycle": {"events": {"tool.pre": "gate"}}}',
            '{"lifecycle": {"events": []}}',
            "[" * 100000,
            "",
        ]
        for body in bodies:
            with self.subTest(body=body[:30]):
                target.write_text(body, encoding="utf-8")
                self.assertFalse(can_ask(self.root, "claude-code", COACUS_GUARD_ASK="1"))

    def test_unreadable_file_degrades(self) -> None:
        (self.root / "harnesses" / "claude-code" / "harness.json").mkdir(parents=True)
        self.assertFalse(can_ask(self.root, "claude-code", COACUS_GUARD_ASK="1"))

    def test_unsafe_harness_names_never_read_outside_the_capability_folder(self) -> None:
        write_harness(self.root, "claude-code", {"lifecycle": {"events": {"tool.pre": CAN_ASK}}})
        planted = self.root / "claude-code"
        planted.mkdir()
        (planted / "harness.json").write_text(
            json.dumps({"lifecycle": {"events": {"tool.pre": CAN_ASK}}}), encoding="utf-8"
        )
        names = ["../claude-code", "claude-code/..", "", "a b", "claude\ncode", "Claude-Code",
                 "cl" + chr(0xE5) + "ude-code", "claude_code"]
        for name in names:
            with self.subTest(name=name):
                self.assertFalse(can_ask(self.root, name, COACUS_GUARD_ASK="1"))

    def test_shipped_capability_data_matches_the_documented_channels(self) -> None:
        expected = {"claude-code": True, "cursor": True, "antigravity": True,
                    "codex": False, "command-code": False, "opencode": False}
        shipped = {p.name for p in (REPO / "harnesses").iterdir() if p.is_dir()} - {"_template"}
        self.assertEqual(shipped, set(expected), "a new harness must declare its ask channel here")
        for harness, wanted in expected.items():
            with self.subTest(harness=harness):
                self.assertIs(can_ask(REPO, harness, COACUS_GUARD_ASK="1"), wanted)


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
