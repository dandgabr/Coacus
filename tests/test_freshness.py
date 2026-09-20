"""Tests for the version-freshness warnings (version-freshness)."""

from __future__ import annotations

import unittest

from engine.validators import freshness

from tests.support import make_repo


class TestFreshnessValidator(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile
        from pathlib import Path

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def _skill(self):
        return self.root / "knowledge/skills/roles/sample-skill/SKILL.md"

    def _write(self, body: str) -> None:
        self._skill().write_text(
            "---\n"
            "name: sample-skill\n"
            "description: >-\n"
            "  Samples artifacts when asked to.\n"
            "tags: []\n"
            "---\n"
            "\n"
            "# Sample Skill\n"
            "\n"
            f"{body}\n",
            encoding="utf-8",
        )

    def test_clean_repo_has_no_warnings(self) -> None:
        self.assertEqual(freshness.warnings(self.root), [])

    def test_unanchored_pin_warns(self) -> None:
        self._write("Targets OWASP API Security Top 10 2023 and MASVS v2.1.0.")
        notes = freshness.warnings(self.root)
        self.assertGreaterEqual(len(notes), 1)
        self.assertTrue(any("unanchored version pin" in n for n in notes))

    def test_anchored_pin_passes(self) -> None:
        self._write(
            "Targets MASVS v2.1.0, resolved 2026-09-20 from "
            "https://mas.owasp.org/MASVS/."
        )
        self.assertEqual(freshness.warnings(self.root), [])

    def test_moving_release_pins_are_detected(self) -> None:
        self._write("Targets OWASP Top 10 2025, MASVS v2.1.0 and CIS Controls v8.1.")
        notes = freshness.warnings(self.root)
        self.assertGreaterEqual(len(notes), 3)
        kinds = "\n".join(notes)
        self.assertIn("owasp", kinds)
        self.assertIn("masvs", kinds)
        self.assertIn("controls", kinds)

    def test_stable_document_identifiers_are_not_flagged(self) -> None:
        self._write("Cite RFC 9110, ISO/IEC 9899:2024 and FIPS 203 as normative.")
        self.assertEqual(freshness.warnings(self.root), [])

    def test_revision_suffixed_nist_pin_is_detected(self) -> None:
        self._write("Grounded in NIST SP 800-61r3 and NIST SP 800-53 Rev. 5.")
        notes = freshness.warnings(self.root)
        self.assertEqual(len(notes), 2)
        self.assertTrue(all("nist" in n for n in notes))

    def test_version_independent_prose_is_not_flagged(self) -> None:
        self._write("Separate duties and verify every trust boundary.")
        self.assertEqual(freshness.warnings(self.root), [])

    def test_report_marks_unresolved_and_resolved(self) -> None:
        self._write("Targets MASVS v2.1.0 without a source.")
        rows = freshness.report(self.root)
        self.assertTrue(any(r.startswith("UNRESOLVED") for r in rows))
        self._write(
            "Targets MASVS v2.1.0, resolved 2026-09-20 from "
            "https://github.com/OWASP/masvs."
        )
        rows = freshness.report(self.root)
        self.assertTrue(rows)
        self.assertTrue(all(r.startswith("resolved") for r in rows))

    def test_validate_is_a_hard_gate(self) -> None:
        self._write("Targets CIS Controls v8.1 without a source.")
        self.assertNotEqual(freshness.validate(self.root), [])

    def test_explicit_unverified_with_reason_is_accepted(self) -> None:
        # The standard's honest terminal state: a pin that could not be resolved.
        self._write(
            "## Version Sources\n\nMoving release pins resolved 2026-09-20:\n\n"
            "- **MASVS v2.1.0** (unverified) — publisher unreachable offline"
        )
        self.assertEqual(freshness.validate(self.root), [])
        rows = freshness.report(self.root)
        self.assertTrue(rows)
        self.assertTrue(all(r.startswith("unverified") for r in rows))

    def test_bare_unverified_marker_is_not_enough(self) -> None:
        self._write("Targets MASVS v2.1.0 (unverified).")
        self.assertNotEqual(freshness.validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
