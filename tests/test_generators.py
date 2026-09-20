"""Golden tests for agent manifest generation (agent-manifests)."""

from __future__ import annotations

import json
import unittest

from engine.generators import agent_manifests, catalog

from tests.support import EXPECTED_REL_FROM_DIST, EXPECTED_SKILL_REL, make_repo


class TestAgentGeneration(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(self._tmp_path())
        self.outputs = agent_manifests.expected_outputs(self.root)

    def _tmp_path(self):
        from pathlib import Path

        return Path(self._tmp.name)

    def test_emits_all_representation_targets(self) -> None:
        expected_keys = {
            "knowledge/agents/roles/sample-agent/dist/AGENT.md",
            "knowledge/agents/roles/sample-agent/dist/agent.yaml",
            "knowledge/agents/roles/sample-agent/dist/agent.json",
            "knowledge/agents/roles/sample-agent/dist/plugin.json",
            ".agents/entries/sample-agent.json",
        }
        self.assertEqual(set(self.outputs), expected_keys)

    def test_agent_md_links_skills_with_relative_depth(self) -> None:
        agent_md = self.outputs[
            "knowledge/agents/roles/sample-agent/dist/AGENT.md"
        ]
        self.assertIn(f"[sample-skill]({EXPECTED_REL_FROM_DIST})", agent_md)
        self.assertIn("coacus:generated:skills", agent_md)
        # title comes from the canonical H1, never duplicated
        self.assertEqual(agent_md.count("# Sample Agent"), 1)
        self.assertIn("Sample instruction body.", agent_md)

    def test_yaml_uses_inherit_model_and_relative_tool_paths(self) -> None:
        yaml_text = self.outputs[
            "knowledge/agents/roles/sample-agent/dist/agent.yaml"
        ]
        self.assertIn("model: inherit", yaml_text)
        self.assertIn(f"path: {EXPECTED_REL_FROM_DIST}", yaml_text)
        self.assertIn("type: skill_integration", yaml_text)

    def test_agent_json_carries_instruction_and_skills(self) -> None:
        payload = json.loads(
            self.outputs["knowledge/agents/roles/sample-agent/dist/agent.json"]
        )
        self.assertEqual(payload["name"], "sample-agent")
        self.assertEqual(payload["skills"], [EXPECTED_SKILL_REL])
        self.assertIn("Sample instruction body.", payload["instruction"])

    def test_discovery_entry_has_fingerprint(self) -> None:
        entry = json.loads(self.outputs[".agents/entries/sample-agent.json"])
        self.assertEqual(entry["name"], "sample-agent")
        self.assertEqual(len(entry["fingerprint"]), 16)
        self.assertTrue(entry["source"].endswith("agent.source.md"))

    def test_write_then_check_is_clean(self) -> None:
        agent_manifests.write_all(self.root)
        catalog.write(self.root)
        self.assertEqual(agent_manifests.check(self.root), [])
        self.assertEqual(catalog.check(self.root), [])

    def test_tampering_is_detected_as_drift(self) -> None:
        agent_manifests.write_all(self.root)
        catalog.write(self.root)
        target = (
            self.root
            / "knowledge/agents/roles/sample-agent/dist/AGENT.md"
        )
        target.write_text("tampered\n", encoding="utf-8")
        self.assertEqual(
            agent_manifests.check(self.root),
            ["knowledge/agents/roles/sample-agent/dist/AGENT.md: out of date (run generate)"],
        )

    def test_orphan_dist_files_are_detected(self) -> None:
        import shutil

        agent_manifests.write_all(self.root)
        catalog.write(self.root)
        shutil.rmtree(self.root / "knowledge/agents/roles/sample-agent")
        drift = agent_manifests.check(self.root)
        self.assertTrue(any("orphan" in item for item in drift))
        self.assertTrue(any(item.endswith(".agents/entries/sample-agent.json: orphan (source removed — delete or restore it)") for item in drift))

    def test_non_list_skills_raise(self) -> None:
        source = self.root / "knowledge/agents/roles/sample-agent/agent.source.md"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "skills:\n  - knowledge/skills/roles/sample-skill/SKILL.md",
                "skills: knowledge/skills/roles/sample-skill/SKILL.md",
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            agent_manifests.expected_outputs(self.root)


class TestCatalog(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(self._tmp_path())

    def _tmp_path(self):
        from pathlib import Path

        return Path(self._tmp.name)

    def test_catalog_counts_disk_truth(self) -> None:
        data = catalog.build(self.root)
        self.assertEqual(data["counts"], {"agents": 1, "skills": 1, "mcps": 0})
        self.assertEqual(data["agents"][0]["name"], "sample-agent")
        self.assertEqual(data["skills"][0]["name"], "sample-skill")

    def test_catalog_has_no_timestamps(self) -> None:
        self.assertNotIn("generated_at", json.dumps(catalog.build(self.root)))

    def test_index_markdown_is_generated(self) -> None:
        catalog.write(self.root)
        index = (self.root / "catalog/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("# Coacus Catalog Index", index)
        self.assertIn("1 skill(s) · 1 agent(s) · 0 MCP(s)", index)
        self.assertIn("sample-agent", index)

    def test_index_drift_is_detected(self) -> None:
        catalog.write(self.root)
        index = self.root / "catalog/INDEX.md"
        index.write_text("tampered\n", encoding="utf-8")
        self.assertEqual(
            catalog.check(self.root), ["catalog/INDEX.md: out of date (run generate)"]
        )


if __name__ == "__main__":
    unittest.main()
