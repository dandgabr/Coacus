"""Tests for the advisory content-rule engine (lifecycle-guardrails)."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from engine.guardrail import rules

ROOT = Path(__file__).resolve().parents[1]


def rule(**overrides) -> dict:
    base = {
        "id": 99,
        "rule": "sample",
        "field": "content",
        "operator": "contains",
        "pattern": "danger",
        "severity": "medium",
        "reminder": "avoid it",
    }
    base.update(overrides)
    return base


class TestMatching(unittest.TestCase):
    def test_contains_and_equals(self) -> None:
        self.assertTrue(rules.matches(rule(operator="contains", pattern="danger"), {"content": "a danger here"}))
        self.assertTrue(rules.matches(rule(operator="equals", pattern="x"), {"content": "x"}))
        self.assertFalse(rules.matches(rule(operator="equals", pattern="x"), {"content": "xy"}))

    def test_starts_ends_and_not_contains(self) -> None:
        self.assertTrue(rules.matches(rule(operator="starts_with", pattern="ab"), {"content": "abc"}))
        self.assertTrue(rules.matches(rule(operator="ends_with", pattern="bc"), {"content": "abc"}))
        self.assertTrue(rules.matches(rule(operator="not_contains", pattern="z"), {"content": "abc"}))

    def test_regex_match(self) -> None:
        r = rule(operator="regex_match", pattern=r"os\.system\s*\(")
        self.assertTrue(rules.matches(r, {"content": "os.system('rm -rf /')"}))
        self.assertFalse(rules.matches(r, {"content": "system.os"}))

    def test_value_list_matches_any(self) -> None:
        self.assertTrue(rules.matches(rule(), {"content": ["clean", "a danger"]}))

    def test_missing_field_does_not_match(self) -> None:
        self.assertFalse(rules.matches(rule(), {"command": "danger"}))


class TestCatalogue(unittest.TestCase):
    def setUp(self) -> None:
        self.catalogue = rules.load_catalogue(ROOT)

    def test_shipped_catalogue_is_valid(self) -> None:
        self.assertIsNotNone(self.catalogue)
        self.assertEqual(rules.lint_errors(self.catalogue), [])
        self.assertEqual(rules.lint_warnings(self.catalogue), [])

    def test_evaluate_flags_pickle(self) -> None:
        hits = rules.evaluate({"content": "pickle.loads(data)"}, self.catalogue)
        names = {h["rule"] for h in hits}
        self.assertIn("unsafe-deserialization-pickle", names)

    def test_evaluate_clean_content_is_empty(self) -> None:
        self.assertEqual(rules.evaluate({"content": "print('hello')"}, self.catalogue), [])

    def test_duplicate_id_is_an_error(self) -> None:
        bad = {"patterns": [rule(id=7, pattern="aaaa"), rule(id=7, pattern="bbbb")]}
        self.assertTrue(any("duplicate rule id" in e for e in rules.lint_errors(bad)))

    def test_bad_regex_is_an_error(self) -> None:
        bad = {"patterns": [rule(operator="regex_match", pattern="(")]}
        self.assertTrue(any("valid regular expression" in e for e in rules.lint_errors(bad)))

    def test_unknown_operator_is_an_error(self) -> None:
        bad = {"patterns": [rule(operator="wat")]}
        self.assertTrue(any("unknown operator" in e for e in rules.lint_errors(bad)))

    def test_missing_reminder_is_an_error(self) -> None:
        bad = {"patterns": [rule(reminder="")]}
        self.assertTrue(any("reminder" in e for e in rules.lint_errors(bad)))

    def test_frozen_id_removed_is_an_error(self) -> None:
        thinned = copy.deepcopy(self.catalogue)
        thinned["patterns"] = [p for p in thinned["patterns"] if p["id"] != 1]
        self.assertTrue(any("frozen rule id" in e for e in rules.lint_errors(thinned)))

    def test_over_broad_pattern_warns(self) -> None:
        self.assertTrue(any("too broad" in w for w in rules.lint_warnings({"patterns": [rule(pattern="a")]})))


if __name__ == "__main__":
    unittest.main()
