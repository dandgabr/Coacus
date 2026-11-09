"""Check the curation record's coverage and binding to reviewed source files.

These are record-integrity checks, not a visual or agent-behavior oracle.
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/reviews/interface-skills-2026-10-19.json"


class InterfaceSkillReviewTests(unittest.TestCase):
    def read_record(self):
        self.assertTrue(RECORD.is_file(), "the completed review needs a durable coverage record")
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_visual_review_covers_its_frozen_inventory_once(self):
        record = self.read_record()
        actual = set(record["frozen_visual_inventory"])
        entries = record["visual_skills"]
        self.assertEqual(len(entries), len({entry["name"] for entry in entries}))
        self.assertEqual({entry["name"] for entry in entries}, actual)
        for entry in entries:
            with self.subTest(skill=entry["name"]):
                self.assertIn(entry["decision"], {"update", "no-change"})
                self.assertTrue(entry["rationale"].strip())
                self.assertTrue(entry["limitations"].strip())
                self.assertTrue(entry["reviewed_files"])

    def test_reviewed_file_bindings_are_safe_and_well_formed(self):
        record = self.read_record()
        for entry in record["visual_skills"] + record["shared_skills"]:
            for item in entry["reviewed_files"]:
                relative = Path(item["path"])
                with self.subTest(file=relative):
                    self.assertFalse(relative.is_absolute())
                    self.assertNotIn("..", relative.parts)
                    self.assertRegex(item["sha256"], r"^[a-f0-9]{64}$")
        # Historical evidence must not freeze the live corpus forever. Delivery
        # performs the actual current-file binding check separately.

    def test_lessons_and_behavior_cases_have_explicit_dispositions(self):
        record = self.read_record()
        self.assertEqual({x["id"] for x in record["lessons"]},
                         {f"L{i:02d}" for i in range(1, 25)})
        self.assertEqual({x["id"] for x in record["scenarios"]},
                         {f"S{i:02d}" for i in range(1, 19)})
        for case in record["scenarios"]:
            self.assertIn(case["status"], {"pass", "fail", "unknown", "unsupported", "skipped"})
            self.assertTrue(case["evidence"])
            self.assertTrue(case["limitations"])


if __name__ == "__main__":
    unittest.main()
