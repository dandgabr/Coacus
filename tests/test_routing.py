"""Tests for the routing index generator and validator (routing)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.generators import routing
from engine.validators import routing as routing_validator

from tests.support import make_repo


class TestRoutingGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))
        (self.root / "knowledge/routing/lexicon.json").write_text(
            json.dumps({"schema": 1, "agents": {"sample-agent": ["sample", "amostra"]}}),
            encoding="utf-8",
        )

    def test_index_carries_canonical_facts_and_triggers(self) -> None:
        index = routing.build(self.root)
        entry = index["entries"][0]
        self.assertEqual(entry["name"], "sample-agent")
        self.assertEqual(entry["category"], "roles")
        self.assertIn("sample", entry["triggers"])
        self.assertIn("knowledge/skills/roles/sample-skill/SKILL.md", entry["skills"])

    def test_written_index_is_idempotent(self) -> None:
        routing.write_all(self.root)
        first = (self.root / routing.ROUTING_PATH).read_text(encoding="utf-8")
        routing.write_all(self.root)
        second = (self.root / routing.ROUTING_PATH).read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertEqual(routing.check(self.root), [])

    def test_lexicon_covering_every_agent_passes(self) -> None:
        routing.write_all(self.root)
        self.assertEqual(routing_validator.validate_sources(self.root), [])
        self.assertEqual(routing_validator.validate_index(self.root), [])

    def test_unknown_agent_in_lexicon_fails(self) -> None:
        (self.root / "knowledge/routing/lexicon.json").write_text(
            json.dumps({"agents": {"ghost": ["x"]}}), encoding="utf-8"
        )
        errors = routing_validator.validate_sources(self.root)
        self.assertTrue(any("unknown agent" in e for e in errors))
        self.assertTrue(any("no triggers" in e for e in errors))

    def test_uppercase_trigger_fails(self) -> None:
        (self.root / "knowledge/routing/lexicon.json").write_text(
            json.dumps({"agents": {"sample-agent": ["Sample"]}}), encoding="utf-8"
        )
        errors = routing_validator.validate_sources(self.root)
        self.assertTrue(any("lowercase" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
