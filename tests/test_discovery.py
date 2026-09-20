"""Tests for consolidated discovery manifest generation (discovery)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.generators import discovery

SKILL = "---\nname: {n}\ndescription: x\n---\n\n# {n}\nbody\n"
MCP = "---\nname: {n}\ndescription: x\ntransport: stdio\ncommand: npx\n---\n\n# {n}\nbody\n"


def make_repo(tmp: Path) -> Path:
    root = tmp / "repo"
    (root / "knowledge/skills/roles/one").mkdir(parents=True)
    (root / "knowledge/skills/roles/one/SKILL.md").write_text(
        SKILL.format(n="one"), encoding="utf-8"
    )
    (root / "methodology/workflows/two").mkdir(parents=True)
    (root / "methodology/workflows/two/SKILL.md").write_text(
        SKILL.format(n="two"), encoding="utf-8"
    )
    (root / "knowledge/mcps/ctx").mkdir(parents=True)
    (root / "knowledge/mcps/ctx/MCP.md").write_text(MCP.format(n="ctx"), encoding="utf-8")
    return root


class TestDiscovery(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def test_build_lists_both_skill_roots(self) -> None:
        data = discovery.build(self.root)
        paths = [e["path"] for e in data["skills"]["entries"]]
        self.assertIn("knowledge/skills/roles/one", paths)
        self.assertIn("methodology/workflows/two", paths)

    def test_build_lists_mcps(self) -> None:
        data = discovery.build(self.root)
        self.assertEqual(
            [e["path"] for e in data["mcps"]["entries"]], ["knowledge/mcps/ctx"]
        )

    def test_write_then_check_clean(self) -> None:
        discovery.write_all(self.root)
        self.assertEqual(discovery.check(self.root), [])
        for name in discovery.MANIFESTS:
            self.assertTrue((self.root / f".agents/{name}.json").is_file())

    def test_drift_detected(self) -> None:
        discovery.write_all(self.root)
        (self.root / ".agents/skills.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual(
            discovery.check(self.root), [".agents/skills.json: out of date (run generate)"]
        )

    def test_manifest_is_valid_json_entries(self) -> None:
        discovery.write_all(self.root)
        data = json.loads((self.root / ".agents/skills.json").read_text())
        self.assertIn("entries", data)
        self.assertTrue(all("path" in e for e in data["entries"]))

    def test_consolidated_stems_do_not_collide_with_agent_names(self) -> None:
        # Regression: an agent literally named 'skills' must not overwrite the
        # consolidated skills.json; per-agent manifests live under entries/.
        from engine.generators import agent_manifests
        from engine.validators import discovery as discovery_validator

        source = self.root / "knowledge/agents/roles/skills/agent.source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nname: skills\ncategory: roles\ndescription: x\nskills: []\n---\n\n# skills\nbody\n",
            encoding="utf-8",
        )
        outputs = agent_manifests.expected_outputs(self.root)
        self.assertIn(".agents/entries/skills.json", outputs)
        self.assertNotIn(".agents/skills.json", outputs)
        agent_manifests.write_all(self.root)
        discovery.write_all(self.root)
        # Both manifest kinds must coexist and validate.
        self.assertTrue((self.root / ".agents/skills.json").is_file())
        self.assertTrue((self.root / ".agents/entries/skills.json").is_file())
        self.assertEqual(discovery_validator.validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
