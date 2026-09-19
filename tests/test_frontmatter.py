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

    def test_inline_list_is_accepted(self) -> None:
        doc = parse("---\nname: x\nskills: [a, b]\ntags: []\n---\nbody\n")
        self.assertEqual(doc.meta["skills"], ["a", "b"])
        self.assertEqual(doc.meta["tags"], [])

    def test_nested_map_is_accepted(self) -> None:
        doc = parse(
            "---\nname: x\nmetadata:\n  type: defensive\n  phase: analysis\n"
            "  tools:\n    - opengrep\n    - semgrep\n---\nbody\n"
        )
        self.assertEqual(doc.meta["metadata"]["type"], "defensive")
        self.assertEqual(doc.meta["metadata"]["phase"], "analysis")
        self.assertEqual(doc.meta["metadata"]["tools"], ["opengrep", "semgrep"])

    def test_multiline_plain_scalar_is_accepted(self) -> None:
        doc = parse(
            "---\nname: x\ndescription: Does things\n  across two lines.\n---\nbody\n"
        )
        self.assertEqual(doc.meta["description"], "Does things across two lines.")

    def test_same_indent_nested_list_is_accepted(self) -> None:
        doc = parse(
            "---\nname: x\nmetadata:\n  mitre:\n  - T1068\n  - T1203\n"
            "  type: defensive\n---\nbody\n"
        )
        self.assertEqual(doc.meta["metadata"]["mitre"], ["T1068", "T1203"])
        self.assertEqual(doc.meta["metadata"]["type"], "defensive")

    def test_quoted_scalars_are_unquoted(self) -> None:
        doc = parse('---\nname: "cloud-aws"\ndescription: \'Quoted text.\'\n---\nbody\n')
        self.assertEqual(doc.meta["name"], "cloud-aws")
        self.assertEqual(doc.meta["description"], "Quoted text.")

    def test_quoted_multiline_scalar_is_unquoted(self) -> None:
        doc = parse('---\nname: x\ndescription: "Does things\n  across lines."\n---\nbody\n')
        self.assertEqual(doc.meta["description"], "Does things across lines.")

    def test_plain_scalar_keeps_inner_quotes(self) -> None:
        # Regression: "He said \"hi\"" must not lose its trailing quote.
        doc = parse('---\nname: x\ntitle: He said "hi"\n---\nbody\n')
        self.assertEqual(doc.meta["title"], 'He said "hi"')

    def test_inline_list_keeps_quoted_comma(self) -> None:
        # Regression: a comma inside a quoted item is not a separator.
        doc = parse('---\nname: x\ntags: ["a,b", c]\n---\nbody\n')
        self.assertEqual(doc.meta["tags"], ["a,b", "c"])

    def test_indented_triple_dash_does_not_close(self) -> None:
        doc = parse("---\ndescription: >-\n  text\n  ---\n  more\n---\n# T\nbody\n")
        self.assertEqual(doc.meta["description"], "text --- more")

    def test_missing_close_when_indented_dash_only(self) -> None:
        with self.assertRaises(FrontmatterError):
            parse("---\nname: x\n  ---\nbody\n")


if __name__ == "__main__":
    unittest.main()
