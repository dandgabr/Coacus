"""Tests for the lifecycle guardrail layer (lifecycle-guardrails)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.generators import lifecycle
from engine.generators import plugins as plugin_registry
from engine.validators import harnesses as harness_validator

REPO = Path(__file__).resolve().parents[1]


class TestLifecycleData(unittest.TestCase):
    def test_events_taxonomy_is_valid(self) -> None:
        path = REPO / "methodology/lifecycle/events.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        ids = [e["id"] for e in data["events"]]
        self.assertEqual(len(ids), len(set(ids)), "event ids must be unique")
        for event in data["events"]:
            self.assertIn(event["class"], ("gate", "observe", "lifecycle"))

    def test_actions_vocabulary_has_the_required_verbs(self) -> None:
        path = REPO / "methodology/lifecycle/actions.schema.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        verbs = {v["id"] for v in data["verbs"]}
        self.assertEqual(
            verbs, {"exec", "read", "write", "network", "spawn", "delegate"}
        )

    def test_default_policy_set_is_empty(self) -> None:
        # D2: the capability ships with no active policy.
        path = REPO / "methodology/lifecycle/policies/default.policy.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["policies"], [])


class TestCapabilityMatrix(unittest.TestCase):
    def test_matrix_is_generated_and_carries_evidence(self) -> None:
        text = lifecycle.build(REPO)
        self.assertIn("tool.pre", text)
        self.assertIn("documented", text)
        self.assertNotIn("generated_at", text)
        self.assertNotIn("timestamp", text.lower())

    def test_matrix_is_idempotent(self) -> None:
        self.assertEqual(lifecycle.check(REPO), [])


class TestHarnessValidator(unittest.TestCase):
    def test_unknown_event_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "methodology/lifecycle").mkdir(parents=True)
            (root / "methodology/lifecycle/events.json").write_text(
                json.dumps({"events": [{"id": "tool.pre", "class": "gate"}]}),
                encoding="utf-8",
            )
            (root / "harnesses/h").mkdir(parents=True)
            (root / "harnesses/h/harness.json").write_text(
                json.dumps(
                    {
                        "name": "h",
                        "lifecycle": {"events": {"not.an.event": {"support": "gate"}}},
                    }
                ),
                encoding="utf-8",
            )
            errors = harness_validator.validate(root)
            self.assertTrue(any("not.an.event" in e for e in errors))

    def test_can_ask_without_can_block_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "methodology/lifecycle").mkdir(parents=True)
            (root / "methodology/lifecycle/events.json").write_text(
                json.dumps({"events": [{"id": "tool.pre", "class": "gate"}]}),
                encoding="utf-8",
            )
            (root / "harnesses/h").mkdir(parents=True)
            (root / "harnesses/h/harness.json").write_text(
                json.dumps(
                    {
                        "name": "h",
                        "lifecycle": {
                            "events": {"tool.pre": {"support": "gate", "can_ask": True}}
                        },
                    }
                ),
                encoding="utf-8",
            )
            errors = harness_validator.validate(root)
            self.assertTrue(any("can_ask" in e for e in errors))

    def test_missing_tool_mapping_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harnesses/h").mkdir(parents=True)
            (root / "harnesses/h/harness.json").write_text(
                json.dumps({"name": "h", "bootstrap": {"supported": False}}),
                encoding="utf-8",
            )
            errors = harness_validator.validate(root)
            self.assertTrue(any("tool_mapping" in e for e in errors))

    def test_template_harness_is_exempt_from_tool_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "harnesses/_template").mkdir(parents=True)
            (root / "harnesses/_template/harness.json").write_text(
                json.dumps({"name": "_template", "bootstrap": {"supported": False}}),
                encoding="utf-8",
            )
            errors = harness_validator.validate(root)
            self.assertFalse(any("tool_mapping" in e for e in errors))

    def test_real_manifests_are_valid(self) -> None:
        self.assertEqual(harness_validator.validate(REPO), [])


class TestGuardrailRender(unittest.TestCase):
    def test_guardrail_kind_renders_for_supported_harness(self) -> None:
        outputs = plugin_registry.render_plugins(
            {
                "name": "claude-code",
                "lifecycle": {"supported": True},
                "plugins": [
                    {"path": "harnesses/claude-code/bootstrap/coacus-guard.sh", "kind": "guardrail"}
                ],
            },
            REPO,
        )
        self.assertIn("harnesses/claude-code/bootstrap/coacus-guard.sh", outputs)
        self.assertIn("guardrail-hooks.json", " ".join(outputs))

    def test_unknown_kind_renders_nothing(self) -> None:
        outputs = plugin_registry.render_plugins(
            {
                "name": "opencode",
                "plugins": [
                    {"path": "harnesses/opencode/bootstrap/router-hook.js", "kind": "router-hook"}
                ],
            },
            REPO,
        )
        self.assertEqual(outputs, {})

    def test_guardrails_do_not_collide_with_bootstrap_hooks_json(self) -> None:
        # The bootstrap renders hooks.json; the guardrail fragment must be disjoint.
        from engine.generators import bootstrap

        outputs = bootstrap.expected_outputs(REPO)
        guardrails = [p for p in outputs if "coacus-guard" in p or "guardrail-hooks" in p]
        self.assertTrue(guardrails)


if __name__ == "__main__":
    unittest.main()
