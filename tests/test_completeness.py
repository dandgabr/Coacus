"""Tests for the completeness validator (F8) and the docstring generator (F7)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.generators import docstrings
from engine.validators import completeness
from tests.support import make_repo


class TestCompleteness(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.root = make_repo(self.tmp)

    def _seed_manifest(self, data: dict) -> None:
        path = self.root / completeness.MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        import json
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_missing_manifest_is_reported(self) -> None:
        # no manifest, no knowledge/skills -> gaps
        gaps = completeness.validate(self.root)
        self.assertTrue(any("missing" in g for g in gaps))

    def test_empty_targets_are_flagged(self) -> None:
        # a truly empty root (no knowledge corpus at all)
        empty = self.tmp / "empty"
        empty.mkdir()
        (empty / completeness.MANIFEST).parent.mkdir(parents=True, exist_ok=True)
        import json
        (empty / completeness.MANIFEST).write_text(json.dumps({"source_repos": {}}), encoding="utf-8")
        gaps = completeness.validate(empty)
        self.assertTrue(any("no skills imported" in g for g in gaps))
        self.assertTrue(any("no agents imported" in g for g in gaps))

    def test_ok_when_manifest_matches_empty_corpus(self) -> None:
        # a manifest with no sources and a corpus that exists but empty
        self._seed_manifest({"source_repos": {}})
        (self.root / "knowledge/skills").mkdir(parents=True, exist_ok=True)
        (self.root / "knowledge/agents").mkdir(parents=True, exist_ok=True)
        (self.root / "sources.lock.json").write_text('{"schema":1,"entries":[]}', encoding="utf-8")
        gaps = completeness.validate(self.root)
        self.assertNotIn("no skills imported under knowledge/skills", gaps)
        self.assertNotIn("no agents imported under knowledge/agents", gaps)

    def test_rename_is_recognized(self) -> None:
        # a source skill 'containers' renamed to 'program-containers' must not
        # be reported as missing.
        src = self.tmp / "src"
        (src / "skills/roles/containers").mkdir(parents=True)
        (src / "skills/roles/containers/SKILL.md").write_text("x", encoding="utf-8")
        target = self.root / "knowledge/skills/roles/program-containers"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("x", encoding="utf-8")
        self._seed_manifest({
            "source_repos": {"skills": str(src)},
            "name_dir_fixes": {"containers": "program-containers"},
        })
        # give the target a provenance entry so it is not flagged as an orphan
        import json
        (self.root / "sources.lock.json").write_text(
            json.dumps({"schema": 1, "entries": [{
                "target_path": "knowledge/skills/roles/program-containers/SKILL.md",
            }]}),
            encoding="utf-8",
        )
        gaps = completeness.validate(self.root)
        self.assertFalse(any("containers" in g and "not imported" in g for g in gaps), gaps)


class TestDocstringGenerator(unittest.TestCase):
    def test_build_includes_public_symbols(self) -> None:
        import tempfile as tf
        with tf.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module = root / "engine" / "mod.py"
            module.parent.mkdir(parents=True)
            module.write_text(
                '"""Module doc."""\n\n'
                "def public(x: int) -> int:\n"
                '    """Do a thing."""\n'
                "    return x\n\n"
                "def _private():\n"
                '    """Hidden."""\n',
                encoding="utf-8",
            )
            text = docstrings.build(root)
            self.assertIn("engine/mod.py", text)
            self.assertIn("def public(x: int) -> int", text)
            self.assertIn("Do a thing.", text)
            self.assertNotIn("_private", text)

    def test_real_repo_reference_is_current(self) -> None:
        root = Path(docstrings.__file__).resolve().parents[2]
        self.assertEqual(docstrings.check(root), [])


if __name__ == "__main__":
    unittest.main()
