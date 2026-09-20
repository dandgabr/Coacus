"""Tests for prose-count reconciliation (D5 — counts are measured, never copied)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.validators import docs

from tests.support import make_repo

README = """# Repo

### Corpus

| Asset | Count | Breakdown |
|---|---|---|
| Skills | 1 | one |
| Agents | 1 | one |
| Workflows | 0 | none |
| MCPs | 0 | none |
| Catalog | 1 | one |
| Provenance | 1 | one |
"""


class TestDocsCounts(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))
        (self.root / "README.md").write_text(README, encoding="utf-8")
        (self.root / "catalog").mkdir(exist_ok=True)
        (self.root / "catalog/catalog.json").write_text(
            json.dumps({"counts": {"skills": 1, "agents": 1, "mcps": 0}}),
            encoding="utf-8",
        )
        (self.root / "sources.lock.json").write_text(
            json.dumps({"schema": 1, "entries": [{"target_path": "x"}]}),
            encoding="utf-8",
        )

    def test_matching_counts_pass(self) -> None:
        self.assertEqual(docs.validate(self.root), [])

    def test_stale_count_fails(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8").replace(
                "| Provenance | 1 |", "| Provenance | 42 |"
            ),
            encoding="utf-8",
        )
        errors = docs.validate(self.root)
        self.assertTrue(any("Provenance" in e and "42" in e for e in errors))

    def test_missing_readme_is_not_an_error(self) -> None:
        (self.root / "README.md").unlink()
        self.assertEqual(docs.validate(self.root), [])

    def test_prose_count_in_living_doc_fails(self) -> None:
        (self.root / "docs").mkdir(exist_ok=True)
        (self.root / "docs/architecture.md").write_text(
            "# Architecture\n\nIt holds 42 skills across categories.\n",
            encoding="utf-8",
        )
        errors = docs.validate(self.root)
        self.assertTrue(any("architecture.md" in e and "42" in e for e in errors))

    def test_historical_paragraph_is_exempt(self) -> None:
        (self.root / "docs").mkdir(exist_ok=True)
        (self.root / "docs/roadmap.md").write_text(
            "# Roadmap\n\nDelivered (as of F6) 199 knowledge skills and 58 agents.\n",
            encoding="utf-8",
        )
        self.assertEqual(docs.validate(self.root), [])

    def test_skill_entries_is_not_matched_as_skills(self) -> None:
        (self.root / "docs").mkdir(exist_ok=True)
        (self.root / "docs/architecture.md").write_text(
            "# Architecture\n\n1 catalog skill entry, 1 skill, 1 agent.\n",
            encoding="utf-8",
        )
        self.assertEqual(docs.validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
