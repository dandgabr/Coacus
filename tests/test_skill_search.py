"""Search the canonical Coacus skill catalog from any working directory."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_skill_search


class SkillSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "catalog").mkdir()
        entries = []
        for name, description in (
            ("db-migration", "Create and verify database migrations."),
            ("web-review", "Review web accessibility."),
        ):
            path = self.root / "knowledge" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                f"---\nname: {name}\ndescription: {description}\n---\n# {name}\n",
                encoding="utf-8",
            )
            entries.append({"name": name, "path": path.relative_to(self.root).as_posix()})
        (self.root / "catalog/catalog.json").write_text(
            json.dumps({"skills": entries}), encoding="utf-8"
        )

    def test_search_returns_absolute_path_for_matching_skill(self) -> None:
        results = coacus_skill_search.search(self.root, "database migration")
        self.assertEqual([item.name for item in results], ["db-migration"])
        self.assertEqual(results[0].path, self.root / "knowledge/db-migration/SKILL.md")
        self.assertTrue(results[0].path.is_absolute())

    def test_search_keeps_partial_matches_when_query_is_more_specific(self) -> None:
        results = coacus_skill_search.search(self.root, "database index")
        self.assertEqual([item.name for item in results], ["db-migration"])

    def test_show_rejects_unknown_and_duplicate_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown skill"):
            coacus_skill_search.show(self.root, "missing")
        catalog = self.root / "catalog/catalog.json"
        data = json.loads(catalog.read_text())
        data["skills"].append(dict(data["skills"][0]))
        catalog.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ambiguous skill"):
            coacus_skill_search.show(self.root, "db-migration")

    def test_rejects_catalog_path_escape_and_malformed_catalog(self) -> None:
        catalog = self.root / "catalog/catalog.json"
        catalog.write_text('{"skills": [{"name":"escape", "path":"../secret/SKILL.md"}]}')
        with self.assertRaisesRegex(ValueError, "outside repository"):
            coacus_skill_search.search(self.root, "escape")
        catalog.write_text("not-json", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "catalog"):
            coacus_skill_search.search(self.root, "escape")


if __name__ == "__main__":
    unittest.main()
