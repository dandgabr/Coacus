"""CLI-level tests: generate must regenerate stale artifacts, not deadlock."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import coacus

from tests.support import SAMPLE_AGENT, SAMPLE_SKILL


def make_repo(tmp: Path) -> Path:
    root = tmp / "repo"
    agent_dir = root / "knowledge/agents/roles/sample-agent"
    skill_dir = root / "knowledge/skills/roles/sample-skill"
    agent_dir.mkdir(parents=True)
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(SAMPLE_SKILL, encoding="utf-8")
    (agent_dir / "agent.source.md").write_text(SAMPLE_AGENT, encoding="utf-8")
    return root


class TestCliGenerate(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def test_generate_succeeds_when_artifacts_absent(self) -> None:
        # No dist/ and no .agents/ exist yet: generation must create them
        # (discovery validation must run AFTER writing, not block it).
        self.assertEqual(coacus.cmd_generate(root=self.root), 0)
        self.assertTrue(
            (self.root / "knowledge/agents/roles/sample-agent/dist/AGENT.md").is_file()
        )
        self.assertTrue((self.root / ".agents/sample-agent.json").is_file())

    def test_generate_recovers_stale_fingerprint(self) -> None:
        self.assertEqual(coacus.cmd_generate(root=self.root), 0)
        source = self.root / "knowledge/agents/roles/sample-agent/agent.source.md"
        source.write_text(
            source.read_text(encoding="utf-8") + "\nExtra line.\n", encoding="utf-8"
        )
        # Stale discovery + drift exist, yet generate must fix them, not abort.
        self.assertEqual(coacus.cmd_generate(root=self.root), 0)
        self.assertEqual(coacus.cmd_check(root=self.root), 0)
        self.assertEqual(coacus.cmd_validate(root=self.root), 0)

    def test_generate_aborts_on_invalid_source(self) -> None:
        source = self.root / "knowledge/agents/roles/sample-agent/agent.source.md"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "name: sample-agent", "name: Bad Name"
            ),
            encoding="utf-8",
        )
        self.assertEqual(coacus.cmd_generate(root=self.root), 1)
        self.assertFalse((self.root / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
