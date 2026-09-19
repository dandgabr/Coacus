"""Golden tests for the frontmatter parser (canonical sources)."""

from __future__ import annotations

import unittest

from engine.frontmatter import Document, FrontmatterError, parse

DOC = """---
name: example
description: >-
  Does things when triggered
  across multiple lines.
skills:
  - a/SKILL.md
  - b/SKILL.md
tags: []
count: 3
---

# Example Title

Body line one.
"""


class TestFrontmatter(unittest.TestCase):
    def test_parse_scalars_blocks_and_lists(self) -> None:
        doc = parse(DOC)
        self.assertEqual(doc.meta["name"], "example")
        self.assertEqual(
            doc.meta["description"], "Does things when triggered across multiple lines."
        )
        self.assertEqual(doc.meta["skills"], ["a/SKILL.md", "b/SKILL.md"])
        self.assertEqual(doc.meta["tags"], [])
        self.assertEqual(doc.meta["count"], "3")

    def test_title_from_first_h1(self) -> None:
        doc = parse(DOC)
        self.assertIsInstance(doc, Document)
        self.assertEqual(doc.title, "Example Title")

    def test_missing_opening_delimiter_raises(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("name: x\n")

    def test_missing_closing_delimiter_raises(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("---\nname: x\n")

    def test_unparseable_line_raises(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("---\nthis is not a key\n---\nbody\n")

    def test_inline_list_is_rejected(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("---\nname: x\nskills: [a, b]\n---\nbody\n")

    def test_indented_triple_dash_does_not_close(self) -> None:
        doc = parse("---\ndescription: >-\n  text\n  ---\n  more\n---\n# T\nbody\n")
        self.assertEqual(doc.meta["description"], "text --- more")

    def test_missing_close_when_indented_dash_only(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("---\nname: x\n  ---\nbody\n")


if __name__ == "__main__":
    unittest.main()
