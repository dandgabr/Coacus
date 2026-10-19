"""Tests for the repository-wide language contract."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.validators import language


class TestRepositoryLanguage(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        (self.root / "config" / "language-exceptions.json").write_text(
            '{"exceptions": []}\n', encoding="utf-8"
        )

    def test_non_markdown_document_is_scanned(self) -> None:
        (self.root / "notes.txt").write_text("Este texto está em português e precisa ser revisado.", encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("notes.txt" in error and "non-English" in error for error in errors))

    def test_extensionless_text_artifact_is_scanned(self) -> None:
        (self.root / "NOTICE").write_text("Este documento está em português para todos.", encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("NOTICE" in error for error in errors))

    def test_unknown_extension_utf8_text_artifact_is_scanned(self) -> None:
        (self.root / "notes.customtext").write_text(
            "Este documento está em português para todos.", encoding="utf-8"
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("notes.customtext" in error for error in errors))

    def test_undecodable_text_artifact_fails_closed(self) -> None:
        (self.root / "notes.txt").write_bytes(b"invalid \xff utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("needs human review" in error for error in errors))

    def test_binary_artifact_is_not_treated_as_prose(self) -> None:
        (self.root / "image.png").write_bytes(b"\x89PNG\x00binary")
        self.assertEqual(language.repository_errors(self.root), [])

    def test_html_visible_text_and_comments_are_scanned(self) -> None:
        (self.root / "page.html").write_text(
            "<html><body>Este conteúdo precisa ser revisado agora.</body><!-- comentário em português --></html>",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("page.html" in error for error in errors))

    def test_structured_configuration_checks_comments_and_human_labels(self) -> None:
        (self.root / "settings.yml").write_text(
            "name: Olá mundo\nidentifier: dado-portugues\n# Configuração do agente\n",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("settings.yml" in error for error in errors))
        self.assertFalse(any("dado-portugues" in error for error in errors))

    def test_ambiguous_text_fails_needs_human_review(self) -> None:
        (self.root / "short.md").write_text("Olá mundo", encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("needs human review" in error for error in errors))

    def test_ascii_only_foreign_diagram_label_is_classified(self) -> None:
        (self.root / "diagram.md").write_text(
            "```text\nProcessos / Apps\n```\n", encoding="utf-8"
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("non-English" in error or "needs human review" in error
                            for error in errors))

    def test_ascii_only_foreign_code_comment_is_classified(self) -> None:
        (self.root / "sample.py").write_text("# Vendas Totais\n", encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("non-English" in error or "needs human review" in error
                            for error in errors))

    def test_ascii_only_noun_heavy_foreign_prose_is_classified(self) -> None:
        (self.root / "notes.txt").write_text(
            "Especialistas compartilham conhecimento livremente.", encoding="utf-8"
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("non-English" in error or "needs human review" in error
                            for error in errors))

    def test_foreign_sentence_inside_english_paragraph_is_classified(self) -> None:
        (self.root / "mixed-paragraph.md").write_text(
            "This setting should be tested. A configuração deve ser testada com cuidado. "
            "Then continue with the next step.\n",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("mixed-paragraph.md" in error for error in errors))

    def test_foreign_word_inside_english_sentence_is_classified(self) -> None:
        (self.root / "mixed-sentence.md").write_text(
            "This setting explains how configuração is handled in the system.\n",
            encoding="utf-8",
        )
        self.assertTrue(any("mixed-sentence.md" in error
                            for error in language.repository_errors(self.root)))

    def test_single_english_technical_word_does_not_rescue_foreign_prose(self) -> None:
        (self.root / "mixed.txt").write_text(
            "O metodo para security detection funciona.", encoding="utf-8"
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("mixed.txt" in error and ("non-English" in error or "needs human review" in error)
                            for error in errors))

    def test_english_scientific_prose_is_not_misclassified_as_latin(self) -> None:
        (self.root / "science.txt").write_text(
            "Senior specialist agent in Chemical Engineering, Synthesis and Industrial Processes, "
            "covering mass and energy balances, chemical kinetics, reactor design, organic and "
            "inorganic synthesis, instrumental analysis, solution thermodynamics and transport phenomena.",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertEqual(errors, [])

    def test_foreign_prose_around_math_is_still_classified(self) -> None:
        (self.root / "equation.md").write_text(
            "A equacao demonstra processo importante: $x = \\frac{a}{b}$.\n",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("non-English" in error or "needs human review" in error
                            for error in errors))

    def test_markdown_heading_and_list_prose_are_scanned(self) -> None:
        text = "# Processos de vendas totais\n\n- Especialistas compartilham conhecimento livremente.\n"
        segments = language._segments(Path("labels.md"), text)
        self.assertEqual(len(segments), 1)
        self.assertIn("Processos de vendas totais", segments[0][1])
        self.assertIn("Especialistas compartilham conhecimento livremente", segments[0][1])
        (self.root / "labels.md").write_text(text, encoding="utf-8")
        errors = language.repository_errors(self.root)
        self.assertTrue(any("labels.md" in error and ("non-English" in error or "needs human review" in error)
                            for error in errors))

    def test_non_python_inline_code_comment_is_scanned(self) -> None:
        (self.root / "sample.ts").write_text(
            "const total = 1; // Especialistas compartilham conhecimento livremente.\n",
            encoding="utf-8",
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("sample.ts" in error and ("non-English" in error or "needs human review" in error)
                            for error in errors))

    def test_python_cli_help_string_is_scanned(self) -> None:
        (self.root / "cli.py").write_text(
            'import argparse\nparser = argparse.ArgumentParser()\n'
            'parser.add_argument("--mode", help="Configure o modo de segurança")\n',
            encoding="utf-8",
        )
        self.assertTrue(any("cli.py" in error for error in language.repository_errors(self.root)))

    def test_single_word_portuguese_user_label_is_scanned(self) -> None:
        (self.root / "labels.py").write_text('label = "Saida"\n', encoding="utf-8")
        self.assertTrue(any("labels.py" in error for error in language.repository_errors(self.root)))

    def test_yaml_prompt_and_instruction_fields_are_scanned(self) -> None:
        (self.root / "prompt.yml").write_text(
            "prompt: Configure o modo de segurança\ninstructions: Ajuste as regras cuidadosamente\n",
            encoding="utf-8",
        )
        self.assertTrue(any("prompt.yml" in error for error in language.repository_errors(self.root)))

    def test_custom_yaml_block_scalar_is_scanned(self) -> None:
        (self.root / "custom.yml").write_text(
            "custom_payload: |\n  Configure o sistema com segurança\n", encoding="utf-8"
        )
        self.assertTrue(any("custom.yml" in error for error in language.repository_errors(self.root)))

    def test_generic_source_string_values_are_scanned(self) -> None:
        (self.root / "ui.js").write_text(
            'const banner = "Configure o sistema com segurança";\n', encoding="utf-8"
        )
        (self.root / "ui.py").write_text(
            'title_text = "Configure o sistema com segurança"\n'
            'labels = ["Ajuste as regras cuidadosamente"]\n'
            'tip = "Não compartilhe a chave privada"\n', encoding="utf-8"
        )
        (self.root / "list.js").write_text(
            'const labels = ["Ajuste as regras cuidadosamente"];\n', encoding="utf-8"
        )
        errors = language.repository_errors(self.root)
        self.assertTrue(any("ui.js" in error for error in errors))
        self.assertTrue(any("ui.py" in error for error in errors))
        self.assertTrue(any("list.js" in error for error in errors))

    def test_graphviz_label_is_scanned(self) -> None:
        (self.root / "flow.dot").write_text(
            'digraph G { start [label="Configuração segura"]; }\n', encoding="utf-8"
        )
        self.assertTrue(any("flow.dot" in error for error in language.repository_errors(self.root)))

    def test_graphviz_boolean_edges_are_not_isolated_language_samples(self) -> None:
        segments = language._segments(
            Path("flow.dot"), 'digraph G { a [label="Start"]; a -> b [label="no"]; }\n'
        )
        self.assertNotIn((1, "no"), segments)

    def test_comment_marker_inside_string_is_not_treated_as_comment(self) -> None:
        self.assertEqual(language._code_segments(
            Path("sample.ts"), 'const url = "https://example.com/path";\n',
        ), [])

    def test_identifier_lists_and_types_are_structural_not_prose(self) -> None:
        self.assertTrue(language._looks_like_code("1. Claude Code / OpenCode / Codex / Aider"))
        self.assertTrue(language._looks_like_code("threadManager, agentThreadId"))
        self.assertTrue(language._looks_like_code("type Album typeof album"))
        self.assertTrue(language._looks_like_code("-*- mode: ruby -*- vi: set ft=ruby :"))
        self.assertTrue(language._looks_like_code("nord0: #2E3440 (Deepest) nord1: #3B4252 (Surface)"))
        self.assertTrue(language._looks_like_code("a1b2c3d4e5f6g7h8i9j0"))
        self.assertFalse(language._looks_like_code("Saida"))
        self.assertFalse(language._looks_like_code("English installation instructions"))
        self.assertTrue(language._looks_like_code("6c."))

    def test_consecutive_markdown_headings_share_context(self) -> None:
        segments = language._segments(
            Path("labels.md"), "# Platform Architect\n\n## Description and Purpose\n\nEnglish prose follows.\n"
        )
        self.assertTrue(any("Platform Architect" in text and "Description and Purpose" in text
                            and "English prose follows" in text
                            for _, text in segments))

    def test_exact_hash_exception_is_path_scoped(self) -> None:
        text = "Este é um exemplo bilíngue aprovado para o roteador."
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        (self.root / "config" / "samples.txt").write_text(text, encoding="utf-8")
        (self.root / "config" / "language-exceptions.json").write_text(json.dumps({"exceptions": [{
            "path": "config/samples.txt", "scope": "segment", "sha256": digest,
            "reason": "Preserved bilingual router example.",
        }]}), encoding="utf-8")
        self.assertEqual(language.repository_errors(self.root), [])
        (self.root / "elsewhere.txt").write_text(text, encoding="utf-8")
        self.assertTrue(any("elsewhere.txt" in error for error in language.repository_errors(self.root)))

    def test_missing_lingua_fails_closed(self) -> None:
        with patch.object(language, "LanguageDetectorBuilder", None):
            errors = language.repository_errors(self.root)
        self.assertTrue(any("lingua-language-detector" in error and "required" in error for error in errors))

    def test_missing_lexical_analyzer_fails_closed(self) -> None:
        with patch.object(language, "zipf_frequency", None):
            errors = language.repository_errors(self.root)
        self.assertTrue(any("wordfreq==3.1.1" in error and "required" in error for error in errors))

    def test_markdown_fences_preserve_following_line_numbers_and_scan_literals(self) -> None:
        text = "```python\nmessage = 'Este conteúdo está em português e precisa revisão'\n```\n\nEnglish prose follows here.\n"
        segments = language._segments(Path("sample.md"), text)
        self.assertTrue(any(line == 2 and "português" in value for line, value in segments))
        self.assertTrue(any(line == 5 for line, _ in segments))

    def test_json_segment_locations_preserve_duplicates(self) -> None:
        text = '{\n  "description": "Este texto está em português agora",\n  "summary": "Este texto está em português agora"\n}'
        segments = language._segments(Path("data.json"), text)
        self.assertEqual([line for line, _ in segments], [2, 3])

    def test_duplicate_exact_exceptions_fail_closed(self) -> None:
        text = "Approved bilingual routing phrase."
        digest = hashlib.sha256(text.encode()).hexdigest()
        item = {"path": "config/sample.txt", "scope": "segment", "sha256": digest, "reason": "Approved router trigger in tests."}
        path = self.root / "config" / "sample.txt"
        path.write_text(text, encoding="utf-8")
        manifest = self.root / "config" / "language-exceptions.json"
        manifest.write_text(json.dumps({"exceptions": [item, item]}), encoding="utf-8")
        errors = language._load_exceptions(self.root)[1]
        self.assertTrue(any("duplicate exception" in error for error in errors))

    def test_exact_file_hash_exception_is_path_and_content_scoped(self) -> None:
        text = "approved bilingual route terms and English metadata"
        target = self.root / "config" / "routes.json"
        target.write_text(text, encoding="utf-8")
        item = {
            "path": "config/routes.json", "scope": "file",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "reason": "Approved bilingual router data, exact reviewed file snapshot.",
        }
        (self.root / "config" / "language-exceptions.json").write_text(
            json.dumps({"exceptions": [item]}), encoding="utf-8"
        )
        self.assertEqual(language.repository_errors(self.root), [])
        target.write_text(text + " Este texto está em português para teste.", encoding="utf-8")
        self.assertTrue(any("needs human review" in error or "non-English" in error
                            for error in language.repository_errors(self.root)))


if __name__ == "__main__":
    unittest.main()
