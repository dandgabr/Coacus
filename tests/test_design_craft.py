"""Tests for the deterministic Design Craft validator and CLI."""

from __future__ import annotations

import unittest
from engine.validators.design_craft import scan_text
from scripts import coacus_design_lint


class TestDesignCraftValidator(unittest.TestCase):
    def test_detects_gray_on_color(self) -> None:
        snippet = '<button className="bg-blue-600 text-slate-400 font-medium">Click</button>'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("gray-on-color", rule_ids)

    def test_detects_ai_gradient(self) -> None:
        snippet = '<div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-8">Hero</div>'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("ai-color-palette", rule_ids)

    def test_detects_italic_serif_in_heading(self) -> None:
        snippet = '<h2>Supercharge your <span className="font-serif italic text-purple-400">productivity</span> today</h2>'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("italic-serif", rule_ids)

    def test_detects_hero_eyebrow_pill(self) -> None:
        snippet = '<div className="rounded-full border border-neutral-700 bg-neutral-800/50 px-3 py-1 text-xs">✨ Introducing v2.0</div>'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("hero-eyebrow", rule_ids)

    def test_detects_icon_tile(self) -> None:
        snippet = '<div className="rounded-xl bg-indigo-50 p-3 w-12 h-12"><svg className="w-6 h-6 text-indigo-600" /></div>'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("icon-tile", rule_ids)

    def test_detects_bounce_easing(self) -> None:
        snippet = 'transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);'
        findings = scan_text(snippet)
        rule_ids = [f.rule_id for f in findings]
        self.assertIn("bounce-easing", rule_ids)

    def test_clean_design_passes_without_findings(self) -> None:
        snippet = """
        <section className="bg-neutral-900 text-neutral-100 p-8">
          <p className="text-xs font-semibold tracking-wider uppercase text-amber-400">Release Notes</p>
          <h1 className="font-sans text-3xl font-bold tracking-tight">System Architecture Overview</h1>
          <div className="p-6 border border-white/10 rounded-lg">
            <h3 className="text-lg font-medium">Modular Ingestion Pipeline</h3>
            <p className="text-sm text-neutral-400 mt-2">Zero dependencies, portable runtime engine.</p>
          </div>
        </section>
        """
        findings = scan_text(snippet)
        self.assertEqual(findings, [])

    def test_cli_self_test_runs_cleanly(self) -> None:
        res = coacus_design_lint._run_self_tests()
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
