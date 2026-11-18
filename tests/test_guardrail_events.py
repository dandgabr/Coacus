"""A policy binds one event; the guard decides only on the event that is rendered."""

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


def policy(event=None, decision="deny", resource="*.env", verb="read") -> dict:
    result = {"id": f"p-{event}", "action": {"verb": verb, "resource": resource}, "decision": decision}
    if event is not None:
        result["event"] = event
    return result


class TestEventBinding(unittest.TestCase):
    def test_a_policy_without_an_event_binds_tool_pre(self) -> None:
        self.assertEqual(guard.evaluate([policy()], "read", "x.env")["decision"], "deny")
        self.assertEqual(guard.evaluate([policy()], "read", "x.env", "tool.post")["decision"], "allow")

    def test_a_policy_fires_only_on_its_own_event(self) -> None:
        for bound in ("tool.pre", "tool.post", "prompt.submit", "turn.stop"):
            for current in ("tool.pre", "tool.post", "prompt.submit", "turn.stop"):
                with self.subTest(bound=bound, current=current):
                    expected = "deny" if bound == current else "allow"
                    got = guard.evaluate([policy(bound)], "read", "x.env", current)["decision"]
                    self.assertEqual(got, expected)

    def test_an_explicit_tool_pre_policy_equals_the_default(self) -> None:
        self.assertEqual(guard.evaluate([policy("tool.pre")], "read", "x.env")["decision"], "deny")

    def test_the_event_filter_also_applies_to_ask_fallbacks(self) -> None:
        asks = [policy("tool.post", "ask"), policy("tool.pre", "ask")]
        asks[0]["on_ask_unavailable"] = "allow"
        asks[1]["on_ask_unavailable"] = "deny"
        result = guard.evaluate(asks, "read", "x.env")
        self.assertEqual(result["on_ask_unavailable"], "deny")
        self.assertEqual(result["policy_id"], "p-tool.pre")


class TestGuardEnforcesOnlyToolPre(unittest.TestCase):
    def _run(self, harness: str, event: str) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "methodology/lifecycle/policies"
            directory.mkdir(parents=True)
            document = {"schema": 1, "enabled": True, "policies": [policy("tool.post"), policy()]}
            (directory / "e.policy.json").write_text(json.dumps(document), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(GUARD_CLI), "--harness", harness, "--event", event, "--root", str(root)],
                input=json.dumps({"tool": "read", "tool_input": {"filePath": "a.env"}}),
                capture_output=True, text=True, timeout=60,
                env={"PATH": "/usr/bin:/bin", "COACUS_POLICY_DIR": str(root / "none")})
            return json.loads(proc.stdout.strip())

    def test_tool_pre_denies_and_other_events_say_nothing(self) -> None:
        denied = self._run("claude-code", "tool.pre")
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
        for event in ("tool.post", "prompt.submit", "turn.stop"):
            with self.subTest(event=event):
                self.assertEqual(self._run("claude-code", event), {})

    def test_antigravity_answers_an_explicit_allow_on_other_events(self) -> None:
        self.assertEqual(self._run("antigravity", "tool.post"), {"decision": "allow"})


class TestHarnessDataMatchesVendorDocs(unittest.TestCase):
    """Cells corrected against the vendor documentation of 2026-11-18."""

    def _cap(self, harness: str, event: str) -> dict:
        data = json.loads((REPO / "harnesses" / harness / "harness.json").read_text(encoding="utf-8"))
        return data["lifecycle"]["events"][event]

    def test_corrected_cells(self) -> None:
        self.assertFalse(self._cap("claude-code", "prompt.submit")["can_ask"])
        self.assertTrue(self._cap("codex", "prompt.submit")["can_block"])
        self.assertFalse(self._cap("cursor", "turn.stop")["can_block"])

    def test_no_event_other_than_tool_pre_may_ask(self) -> None:
        for path in sorted((REPO / "harnesses").glob("*/harness.json")):
            events = json.loads(path.read_text(encoding="utf-8")).get("lifecycle", {}).get("events", {})
            for event, cap in events.items():
                if event != "tool.pre":
                    with self.subTest(harness=path.parent.name, event=event):
                        self.assertFalse(cap.get("can_ask"))


if __name__ == "__main__":
    unittest.main()
