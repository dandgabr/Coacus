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
    routing_dir = root / "knowledge/routing"
    agent_dir.mkdir(parents=True)
    skill_dir.mkdir(parents=True)
    routing_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(SAMPLE_SKILL, encoding="utf-8")
    (agent_dir / "agent.source.md").write_text(SAMPLE_AGENT, encoding="utf-8")
    (routing_dir / "lexicon.json").write_text(
        '{\n  "schema": 1,\n  "agents": {\n    "sample-agent": ["sample"]\n  }\n}\n',
        encoding="utf-8",
    )
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
        self.assertTrue((self.root / ".agents/entries/sample-agent.json").is_file())

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


class TestCliRefresh(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def test_refresh_recovers_drifted_provenance(self) -> None:
        from engine import provenance

        # A generated repo whose provenance entry then drifts on disk.
        self.assertEqual(coacus.cmd_generate(root=self.root), 0)
        lock = provenance.load(self.root)
        lock["entries"] = [
            {
                "source_repo": "skills",
                "source_commit": "deadbeef",
                "source_path": "agents/roles/sample-agent/AGENT.md",
                "source_sha256": "0" * 64,
                "target_path": "knowledge/agents/roles/sample-agent/agent.source.md",
                "target_sha256": "0" * 64,
                "origin_license": "GPL-3.0",
                "transform": ["imported"],
                "import_run_id": "seed",
                "imported_at": "2026-01-01T00:00:00Z",
                "aliases": [],
            }
        ]
        provenance.write(self.root, lock)
        self.assertEqual(coacus.cmd_validate(root=self.root), 1)
        self.assertEqual(coacus.cmd_refresh(root=self.root), 0)
        self.assertEqual(coacus.cmd_validate(root=self.root), 0)

    def test_refresh_on_clean_manifest_is_ok(self) -> None:
        self.assertEqual(coacus.cmd_refresh(root=self.root), 0)


if __name__ == "__main__":
    unittest.main()
