"""Tests for the Coacus adaptation of the imported Superpowers workflows.

Covers the pure-text normalizer in ``scripts/coacus_import.py``: the flat-name
rewrite of the upstream colon namespace, the ``docs/temp/`` output redirect, the
resolution of bare sibling workflow paths, the repair of dangling references,
and the idempotent attribution footer.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_import


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestAdaptWorkflowText(unittest.TestCase):
    def test_normalizers_are_disabled_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "methodology/workflows/brainstorming/SKILL.md"
            _write(target, "superpowers:example")
            with self.assertRaisesRegex(ValueError, "disabled"):
                coacus_import._normalize_workflow_files(root)
            self.assertEqual(target.read_text(), "superpowers:example")
            with self.assertRaisesRegex(ValueError, "disabled"):
                coacus_import._run_normalize()

    def test_superpowers_apply_refuses_without_touching_curated_workflow(self) -> None:
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "upstream/brainstorming"
            target = root / "workflows/brainstorming"
            _write(source / "SKILL.md", "unreviewed")
            _write(target / "SKILL.md", "curated")
            action = {"action": "import-workflow", "source": source, "target": target}
            with patch.object(coacus_import, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "consultative"):
                    coacus_import.apply_actions({}, [action])
            self.assertEqual((target / "SKILL.md").read_text(), "curated")


    def test_consolidated_workflow_is_not_reimported(self) -> None:
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "skills/systematic-debugging/SKILL.md", "upstream")
            manifest = {"superpowers": {"target_dir": "methodology/workflows", "consolidated": {"systematic-debugging": "diagnosing-bugs"}}}
            with patch.object(coacus_import, "_source_dir", return_value=root):
                actions = coacus_import.plan_superpowers(manifest)
            self.assertEqual(actions[0]["action"], "exclude")
            self.assertIn("consultative", actions[0]["reason"])

    def test_plan_uses_manifest_names(self) -> None:
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("brainstorming", "diagnosing-superpowers"):
                _write(root / "skills" / name / "SKILL.md", "---\nname: x\n---\n")
            manifest = {"superpowers": {"target_dir": "methodology/workflows", "name_fixes": {"diagnosing-superpowers": "diagnosing-agent-sessions"}}}
            with patch.object(coacus_import, "_source_dir", return_value=root):
                actions = coacus_import.plan_superpowers(manifest)
            self.assertEqual({a["name"] for a in actions}, {"brainstorming", "diagnosing-superpowers"})
            self.assertTrue(all(a["action"] == "exclude" for a in actions))

    def test_exceptional_name_and_flat_namespace(self) -> None:
        text = "superpowers:diagnosing-superpowers ../diagnosing-superpowers/SKILL.md"
        self.assertEqual(
            coacus_import._adapt_workflow_text(text),
            "diagnosing-agent-sessions ../diagnosing-agent-sessions/SKILL.md",
        )

    def test_colon_namespace_rewritten_to_flat_name(self) -> None:
        out = coacus_import._adapt_workflow_text(
            "Use superpowers:test-driven-development now."
        )
        self.assertIn("test-driven-development", out)
        self.assertNotIn("superpowers:", out)

    def test_urls_are_preserved(self) -> None:
        for text in (
            "See https://example.com:8443/path for details.",
            "See https://example.com/superpowers:latest for details.",
        ):
            self.assertEqual(coacus_import._adapt_workflow_text(text), text)

    def test_output_paths_redirect_to_docs_temp(self) -> None:
        text = "Save plans to `docs/superpowers/plans/x.md` and the bare `docs/superpowers` root."
        out = coacus_import._adapt_workflow_text(text)
        self.assertIn("docs/temp/plans/x.md", out)
        self.assertIn("`docs/temp` root", out)
        self.assertNotIn("docs/superpowers", out)

    def test_bare_sibling_workflow_paths_remain_flat(self) -> None:
        text = "Run `../subagent-driven-development/scripts/task-start P 1`."
        out = coacus_import._adapt_workflow_text(text)
        self.assertIn("../subagent-driven-development/scripts/task-start", out)

    def test_using_superpowers_points_at_the_local_mappings(self) -> None:
        out = coacus_import._adapt_workflow_text(
            "see the per-platform references in `../using-superpowers/references/`"
        )
        self.assertIn("../using-coacus/references/", out)
        self.assertNotIn("using-superpowers", out)

    def test_external_reference_is_repaired(self) -> None:
        out = coacus_import._adapt_workflow_text(
            "Use elements-of-style:writing-clearly-and-concisely skill if available"
        )
        self.assertIn("linguistic-en-us", out)
        self.assertNotIn("elements-of-style", out)

    def test_frontend_prohibition_is_generalized(self) -> None:
        for text in (
            "never frontend-design,\nmcp-builder, or any other implementation skill.",
            "never frontend-design, mcp-builder or another implementation skill.",
        ):
            out = coacus_import._adapt_workflow_text(text)
            self.assertIn("never an implementation skill", out)
            self.assertNotIn("frontend-design", out)

    def test_duplicated_phrase_is_collapsed(self) -> None:
        text = "see the per-harness tool mappings under references/ or the per-harness tool mappings under references/ for the path"
        out = coacus_import._adapt_workflow_text(text)
        self.assertEqual(out.count("the per-harness tool mappings under references/"), 1)


class TestAttachAttribution(unittest.TestCase):
    def test_inserted_after_frontmatter_without_extra_blank_lines(self) -> None:
        footer = coacus_import._attribution_footer("abc123")
        text = "---\nname: x\ndescription: y\n---\n\n# Title\n\nBody\n"
        out = coacus_import._attach_attribution(text, footer)
        self.assertEqual(out.count(coacus_import._ATTRIBUTION_MARK), 1)
        self.assertTrue(out.startswith("---\nname: x\ndescription: y\n---\n"))
        self.assertNotIn("\n\n\n", out)
        self.assertTrue(out.endswith("# Title\n\nBody\n"))

    def test_idempotent(self) -> None:
        footer = coacus_import._attribution_footer("abc123")
        text = "---\nname: x\ndescription: y\n---\n\n# Title\n"
        once = coacus_import._attach_attribution(text, footer)
        twice = coacus_import._attach_attribution(once, footer)
        self.assertEqual(once, twice)

    def test_footer_is_replaced_when_the_commit_changes(self) -> None:
        text = "---\nname: x\ndescription: y\n---\n\n# Title\n"
        first = coacus_import._attach_attribution(
            text, coacus_import._attribution_footer("oldsha")
        )
        second = coacus_import._attach_attribution(
            first, coacus_import._attribution_footer("newsha")
        )
        self.assertIn("@ newsha", second)
        self.assertNotIn("oldsha", second)
        self.assertEqual(second.count(coacus_import._ATTRIBUTION_MARK), 1)


class TestNormalizeWorkflowFiles(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()



class TestCorpusIsAdapted(unittest.TestCase):
    """The real corpus carries no upstream-relative artifact after normalize."""

    ROOT = Path(__file__).resolve().parents[1]

    def _superpowers_files(self) -> list[Path]:
        return coacus_import._workflow_files(self.ROOT)

    def test_no_colon_namespace_remains(self) -> None:
        for path in self._superpowers_files():
            self.assertNotIn(
                "superpowers:", path.read_text(encoding="utf-8"), msg=str(path)
            )

    def test_no_upstream_output_path_remains(self) -> None:
        for path in self._superpowers_files():
            self.assertNotIn(
                "docs/superpowers", path.read_text(encoding="utf-8"), msg=str(path)
            )

    def test_no_bare_sibling_or_excluded_skill_paths_remain(self) -> None:
        for path in self._superpowers_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("using-superpowers", text, msg=str(path))
            self.assertNotIn("../superpowers-", text, msg=str(path))

    def test_every_workflow_carries_the_attribution_footer(self) -> None:
        skills = [p for p in self._superpowers_files() if p.name == "SKILL.md"]
        self.assertTrue(skills)
        for path in skills:
            self.assertIn(
                coacus_import._ATTRIBUTION_MARK,
                path.read_text(encoding="utf-8"),
                msg=str(path),
            )

    def test_brainstorming_uses_the_local_linguistic_skill(self) -> None:
        text = (
            self.ROOT / "methodology/workflows/brainstorming/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("elements-of-style", text)
        self.assertIn("Design discipline", text)

    def test_no_upstream_implementation_skill_names_remain(self) -> None:
        for path in self._superpowers_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("frontend-design", text, msg=str(path))
            self.assertNotIn("mcp-builder", text, msg=str(path))


if __name__ == "__main__":
    unittest.main()
