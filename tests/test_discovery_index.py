"""Tests for the Agent Skills discovery index and the grouping manifest."""

from __future__ import annotations

import gzip
import hashlib
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

from engine.generators import discovery_index, groups


def write_skill(root: Path, name: str, frontmatter: str = "") -> Path:
    directory = root / "knowledge" / "skills" / "engineering" / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: >-\n  Does {name}.\n{frontmatter}---\n\n"
        f"# {name}\n\nBody.\n",
        encoding="utf-8",
    )
    return directory


class TestDiscoveryIndex(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_skill_md_and_archive_types(self) -> None:
        write_skill(self.root, "solo")
        with_extra = write_skill(self.root, "with-files")
        (with_extra / "references").mkdir()
        (with_extra / "references" / "note.md").write_text("x\n", encoding="utf-8")
        index = discovery_index.build(self.root)
        by_name = {s["name"]: s for s in index["skills"]}
        self.assertEqual(by_name["solo"]["type"], "skill-md")
        self.assertEqual(by_name["with-files"]["type"], "archive")
        self.assertTrue(by_name["solo"]["digest"].startswith("sha256:"))

    def test_build_is_deterministic(self) -> None:
        write_skill(self.root, "a-skill")
        self.assertEqual(discovery_index.build(self.root), discovery_index.build(self.root))
        archive = write_skill(self.root, "b-skill")
        (archive / "extra.txt").write_text("data\n", encoding="utf-8")
        self.assertEqual(
            discovery_index.build(self.root)["skills"],
            discovery_index.build(self.root)["skills"],
        )

    def test_gzip_is_valid_and_depends_only_on_the_input(self) -> None:
        for size in (0, 1, 65535, 65536, 200_000):
            data = bytes(i % 251 for i in range(size))
            stream = discovery_index.deterministic_gzip(data)
            self.assertEqual(gzip.decompress(stream), data, size)
            self.assertEqual(stream, discovery_index.deterministic_gzip(data), size)
        # A fixed value, so a different machine (or a different zlib) cannot drift unnoticed.
        self.assertEqual(
            hashlib.sha256(discovery_index.deterministic_gzip(b"abc")).hexdigest(),
            "f31b3021082ff798b6d0b88824263adf13c8b2d7a2c6b16fd256619ab7d08da9",
        )

    def test_the_digest_does_not_use_a_compressor(self) -> None:
        # The bytes of a deflate stream differ between zlib and zlib-ng; the digest must not
        # depend on either, so a build that cannot compress at all still gives the same digest.
        directory = write_skill(self.root, "bundle")
        (directory / "references").mkdir()
        (directory / "references" / "notes.md").write_text("notes\n", encoding="utf-8")
        expected = discovery_index.build(self.root)["skills"][0]["digest"]
        refuse = mock.Mock(side_effect=AssertionError("a compressor was used"))
        with mock.patch.object(zlib, "compressobj", refuse), mock.patch.object(gzip, "compress", refuse):
            self.assertEqual(discovery_index.build(self.root)["skills"][0]["digest"], expected)

    def test_tool_leftovers_are_not_part_of_a_skill(self) -> None:
        directory = write_skill(self.root, "clean")
        before = discovery_index.build(self.root)["skills"][0]
        (directory / "__pycache__").mkdir()
        (directory / "__pycache__" / "helper.cpython-314.pyc").write_bytes(b"\x00\x01")
        (directory / ".DS_Store").write_bytes(b"x")
        after = discovery_index.build(self.root)["skills"][0]
        self.assertEqual(after, before)
        self.assertEqual(after["type"], "skill-md")

    def test_internal_skill_is_excluded(self) -> None:
        write_skill(self.root, "public-skill")
        write_skill(self.root, "secret-skill", frontmatter="metadata:\n  internal: true\n")
        names = {s["name"] for s in discovery_index.build(self.root)["skills"]}
        self.assertIn("public-skill", names)
        self.assertNotIn("secret-skill", names)

    def test_write_then_check_has_no_drift(self) -> None:
        write_skill(self.root, "a-skill")
        discovery_index.write(self.root)
        self.assertEqual(discovery_index.check(self.root), [])

    def test_archive_digest_changes_with_content(self) -> None:
        d = write_skill(self.root, "b-skill")
        (d / "x.txt").write_text("one\n", encoding="utf-8")
        first = discovery_index.build(self.root)["skills"][0]["digest"]
        (d / "x.txt").write_text("two\n", encoding="utf-8")
        second = discovery_index.build(self.root)["skills"][0]["digest"]
        self.assertNotEqual(first, second)


class TestGroups(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_groups_by_category_and_skips_internal(self) -> None:
        write_skill(self.root, "a-skill")
        write_skill(self.root, "hidden", frontmatter="metadata:\n  internal: true\n")
        data = groups.build(self.root)
        titles = {g["title"]: g["skills"] for g in data["groups"]}
        self.assertIn("engineering", titles)
        self.assertIn("a-skill", titles["engineering"])
        self.assertNotIn("hidden", titles.get("engineering", []))

    def test_write_then_check_has_no_drift(self) -> None:
        write_skill(self.root, "a-skill")
        groups.write(self.root)
        self.assertEqual(groups.check(self.root), [])


if __name__ == "__main__":
    unittest.main()
