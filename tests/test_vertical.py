"""Tests for the architecture_si vertical: dispatcher OCP + analyzer (F6c)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine import dispatcher
from verticals.architecture_si.pipelines.analyze import analyzer


class TestDispatcher(unittest.TestCase):
    def setUp(self) -> None:
        dispatcher.load_handlers()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_formats_registered(self) -> None:
        exts = dispatcher.supported_extensions()
        for ext in (".pdf", ".docx", ".pptx", ".html", ".csv", ".json", ".txt", ".md"):
            # .md is handled as a passthrough by the caller, not a converter
            if ext == ".md":
                continue
            self.assertIn(ext, exts, ext)

    def test_txt_conversion(self) -> None:
        src = self.dir / "note.txt"
        src.write_text("hello world", encoding="utf-8")
        out = dispatcher.convert(str(src))
        self.assertTrue(Path(out).is_file())
        self.assertIn("hello world", Path(out).read_text(encoding="utf-8"))

    def test_csv_conversion_builds_table(self) -> None:
        src = self.dir / "data.csv"
        src.write_text("a,b\n1,2\n", encoding="utf-8")
        out = Path(dispatcher.convert(str(src))).read_text(encoding="utf-8")
        self.assertIn("| a | b |", out)
        self.assertIn("| 1 | 2 |", out)

    def test_json_conversion_fences(self) -> None:
        src = self.dir / "cfg.json"
        src.write_text('{"k": "v"}', encoding="utf-8")
        out = Path(dispatcher.convert(str(src))).read_text(encoding="utf-8")
        self.assertIn("```json", out)

    def test_unsupported_format_raises(self) -> None:
        src = self.dir / "weird.xyz"
        src.write_text("x", encoding="utf-8")
        with self.assertRaises(ValueError):
            dispatcher.convert(str(src))

    def test_missing_file_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            dispatcher.convert(str(self.dir / "absent.txt"))

    def test_extension_registration_is_open_closed(self) -> None:
        from engine.dispatcher import register_converter

        @register_converter(".custom-ext")
        def _handler(input_path: str, output_path: str | None = None) -> str:
            return input_path

        self.assertIn(".custom-ext", dispatcher.supported_extensions())

    def test_default_output_avoids_stem_collision(self) -> None:
        # a.txt and a.csv must not both write a.md
        txt = self.dir / "a.txt"
        csv = self.dir / "a.csv"
        txt.write_text("text", encoding="utf-8")
        csv.write_text("x,y\n1,2\n", encoding="utf-8")
        out_txt = dispatcher.convert(str(txt))
        out_csv = dispatcher.convert(str(csv))
        self.assertNotEqual(out_txt, out_csv)
        self.assertTrue(Path(out_txt).is_file() and Path(out_csv).is_file())

    def test_options_forwarded_to_handler(self) -> None:
        # pdf is the only handler taking toc_only; verify the dispatcher routes
        # extra options without crashing on handlers that ignore them.
        src = self.dir / "b.txt"
        src.write_text("body", encoding="utf-8")
        out = dispatcher.convert(str(src), toc_only=True)
        self.assertTrue(Path(out).is_file())


class TestAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_analyze_markdown(self) -> None:
        doc = self.dir / "doc.md"
        doc.write_text(
            "# Title\n\n## Section\n\nWe use mTLS and OWASP ASVS.\n\n"
            "```mermaid\ngraph TD\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n",
            encoding="utf-8",
        )
        result = analyzer.analyze_markdown(str(doc))
        self.assertEqual(result.file_name, "doc.md")
        self.assertGreaterEqual(len(result.headings), 2)
        self.assertEqual(result.mermaid_diagrams_count, 1)
        self.assertGreaterEqual(result.tables_count, 1)
        self.assertIn("Protocols & Controls", result.security_keywords_detected)
        self.assertIn("Standards", result.security_keywords_detected)

    def test_human_report_contains_stats(self) -> None:
        doc = self.dir / "d.md"
        doc.write_text("# H\n\ntext", encoding="utf-8")
        report = analyzer.human_report(analyzer.analyze_markdown(str(doc)))
        self.assertIn("Analysis report: d.md", report)


if __name__ == "__main__":
    unittest.main()
