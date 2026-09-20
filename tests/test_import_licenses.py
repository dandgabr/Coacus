"""Tests for the import pipeline's provenance license labeling."""

from __future__ import annotations

import unittest

from scripts import coacus_import


class TestOriginLicense(unittest.TestCase):
    def test_declared_license_is_used(self) -> None:
        manifest = {"licenses": {"superpowers": "MIT"}}
        self.assertEqual(coacus_import._origin_license(manifest, "superpowers"), "MIT")

    def test_missing_license_falls_back_to_pointer(self) -> None:
        manifest = {"licenses": {}}
        self.assertEqual(
            coacus_import._origin_license(manifest, "skills"), "see source repo"
        )

    def test_no_licenses_key_falls_back_to_pointer(self) -> None:
        self.assertEqual(
            coacus_import._origin_license({}, "skills"), "see source repo"
        )


class TestRelabelLicenses(unittest.TestCase):
    def test_relabels_matching_entries_only(self) -> None:
        lock = {
            "entries": [
                {"source_repo": "skills", "origin_license": "see source repo"},
                {"source_repo": "superpowers", "origin_license": "see source repo"},
                {"source_repo": "unknown", "origin_license": "see source repo"},
            ]
        }
        manifest = {"licenses": {"skills": "GPL-3.0", "superpowers": "MIT"}}
        relabeled = coacus_import._relabel_licenses(lock, manifest)
        self.assertEqual(relabeled, 2)
        self.assertEqual(lock["entries"][0]["origin_license"], "GPL-3.0")
        self.assertEqual(lock["entries"][1]["origin_license"], "MIT")
        # An undeclared repo keeps its pointer rather than claiming a license.
        self.assertEqual(lock["entries"][2]["origin_license"], "see source repo")

    def test_relabel_is_idempotent(self) -> None:
        lock = {
            "entries": [{"source_repo": "skills", "origin_license": "GPL-3.0"}]
        }
        manifest = {"licenses": {"skills": "GPL-3.0"}}
        relabeled = coacus_import._relabel_licenses(lock, manifest)
        self.assertEqual(relabeled, 0)

    def test_entries_without_source_repo_are_ignored(self) -> None:
        lock = {"entries": [{"origin_license": "see source repo"}]}
        relabeled = coacus_import._relabel_licenses(lock, {"licenses": {"skills": "GPL-3.0"}})
        self.assertEqual(relabeled, 0)

    def test_empty_lock_is_safe(self) -> None:
        self.assertEqual(coacus_import._relabel_licenses({}, {"licenses": {}}), 0)


if __name__ == "__main__":
    unittest.main()
