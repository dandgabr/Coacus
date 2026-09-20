"""Tests for the SessionStart bootstrap renderer (session-start-bootstrap)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine import frontmatter
from engine.generators import bootstrap

ENTRY = """---
name: using-coacus
description: >-
  Establishes how to work in a Coacus repository. Use when starting any task.
---

# Using Coacus

ENTRY-BODY-MARKER
"""

WRAPPER = """<EXTREMELY_IMPORTANT>
You have Coacus.

{entry_skill_body}

{tool_mapping}
</EXTREMELY_IMPORTANT>
"""


def make_repo(tmp: Path) -> Path:
    root = tmp / "repo"
    (root / "methodology/bootstrap").mkdir(parents=True)
    (root / "methodology/workflows/using-coacus").mkdir(parents=True)
    (root / "methodology/bootstrap/session-start.canonical.md").write_text(
        WRAPPER, encoding="utf-8"
    )
    (root / "methodology/workflows/using-coacus/SKILL.md").write_text(
        ENTRY, encoding="utf-8"
    )
    return root


def write_harness(root: Path, name: str, data: dict) -> None:
    directory = root / "harnesses" / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "harness.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )


class TestBootstrapRender(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def test_shape_b_injects_entry_body_and_mapping(self) -> None:
        write_harness(
            self.root,
            "opencode",
            {
                "name": "opencode",
                "bootstrap": {
                    "supported": True,
                    "shape": "B",
                    "outputs": [{"path": "harnesses/opencode/bootstrap/coacus.js", "format": "js"}],
                },
                "tool_mapping": {"run shell commands": "bash"},
            },
        )
        outputs = bootstrap.expected_outputs(self.root)
        plugin = outputs["harnesses/opencode/bootstrap/coacus.js"]
        self.assertIn("ENTRY-BODY-MARKER", plugin)
        self.assertIn("run shell commands -> bash", plugin)
        self.assertIn("EXTREMELY_IMPORTANT", plugin)

    def test_shape_b_does_not_register_repo_skill_paths(self) -> None:
        # Registering the repo skill roots bypasses a partial install: the
        # harness discovers the installed skills tree natively instead.
        write_harness(
            self.root,
            "opencode",
            {
                "name": "opencode",
                "bootstrap": {
                    "supported": True,
                    "shape": "B",
                    "outputs": [{"path": "harnesses/opencode/bootstrap/coacus.js", "format": "js"}],
                },
                "tool_mapping": {"run shell commands": "bash"},
            },
        )
        outputs = bootstrap.expected_outputs(self.root)
        plugin = outputs["harnesses/opencode/bootstrap/coacus.js"]
        self.assertNotIn("SKILL_PATHS", plugin)
        self.assertNotIn("skills.paths", plugin)

    def test_shape_a_emits_single_native_key(self) -> None:
        write_harness(
            self.root,
            "claude-code",
            {
                "name": "claude-code",
                "bootstrap": {
                    "supported": True,
                    "shape": "A",
                    "native_key": "hookSpecificOutput.additionalContext",
                    "forbidden_keys": ["additional_context"],
                    "outputs": [
                        {"path": "harnesses/claude-code/bootstrap/session-start.sh", "format": "sh"},
                        {"path": "harnesses/claude-code/bootstrap/hooks.json", "format": "json"},
                    ],
                },
                "tool_mapping": {},
            },
        )
        outputs = bootstrap.expected_outputs(self.root)
        script = outputs["harnesses/claude-code/bootstrap/session-start.sh"]
        self.assertNotIn("additional_context", script)
        self.assertIn("hookSpecificOutput", script)
        hooks = json.loads(outputs["harnesses/claude-code/bootstrap/hooks.json"])
        self.assertIn("SessionStart", hooks["hooks"])

    def test_shape_a_rejects_native_key_in_forbidden(self) -> None:
        write_harness(
            self.root,
            "claude-code",
            {
                "name": "claude-code",
                "bootstrap": {
                    "supported": True,
                    "shape": "A",
                    "native_key": "additional_context",
                    "forbidden_keys": ["additional_context"],
                    "outputs": [
                        {"path": "harnesses/claude-code/bootstrap/session-start.sh", "format": "sh"},
                    ],
                },
                "tool_mapping": {},
            },
        )
        with self.assertRaises(ValueError):
            bootstrap.expected_outputs(self.root)

    def test_shape_c_emits_context_and_manifest(self) -> None:
        write_harness(
            self.root,
            "antigravity",
            {
                "name": "antigravity",
                "bootstrap": {
                    "supported": True,
                    "shape": "C",
                    "outputs": [
                        {"path": "harnesses/antigravity/bootstrap/coacus-rule.md", "format": "md"},
                        {"path": "harnesses/antigravity/bootstrap/plugin.json", "format": "json"},
                    ],
                },
                "tool_mapping": {},
            },
        )
        outputs = bootstrap.expected_outputs(self.root)
        rule = outputs["harnesses/antigravity/bootstrap/coacus-rule.md"]
        self.assertIn("ENTRY-BODY-MARKER", rule)
        self.assertIn("activation: always_on", rule)
        manifest = json.loads(
            outputs["harnesses/antigravity/bootstrap/plugin.json"]
        )
        # Antigravity's plugin.json schema allows only name + description.
        self.assertEqual(set(manifest), {"name", "description"})
        self.assertNotIn("contextFileName", manifest)

    def test_shape_c_caps_rule_length(self) -> None:
        write_harness(
            self.root,
            "antigravity",
            {
                "name": "antigravity",
                "bootstrap": {
                    "supported": True,
                    "shape": "C",
                    "outputs": [
                        {"path": "harnesses/antigravity/bootstrap/coacus-rule.md", "format": "md"},
                    ],
                },
                "tool_mapping": {},
            },
        )
        # The entry body is tiny here, so simulate the cap directly.
        big = {"name": "antigravity", "bootstrap": {"supported": True, "shape": "C",
               "outputs": [{"path": "harnesses/antigravity/bootstrap/coacus-rule.md", "format": "md"}]}}
        rendered = bootstrap._render_shape_c(big, "x" * 20000)
        rule = rendered["harnesses/antigravity/bootstrap/coacus-rule.md"]
        self.assertLess(len(rule), 12000)
        self.assertIn("truncated", rule)

    def test_native_discovery_renders_nothing(self) -> None:
        write_harness(
            self.root,
            "codex",
            {"name": "codex", "bootstrap": {"supported": False, "shape": "native-discovery"}},
        )
        self.assertEqual(bootstrap.expected_outputs(self.root), {})

    def test_unsupported_renders_nothing(self) -> None:
        write_harness(
            self.root,
            "cursor",
            {"name": "cursor", "bootstrap": {"supported": False, "shape": "A"}},
        )
        self.assertEqual(bootstrap.expected_outputs(self.root), {})

    def test_render_is_idempotent(self) -> None:
        write_harness(
            self.root,
            "opencode",
            {
                "name": "opencode",
                "bootstrap": {
                    "supported": True,
                    "shape": "B",
                    "outputs": [{"path": "harnesses/opencode/bootstrap/coacus.js", "format": "js"}],
                },
                "tool_mapping": {},
            },
        )
        bootstrap.write_all(self.root)
        first = bootstrap.check(self.root)
        bootstrap.write_all(self.root)
        self.assertEqual(first, [])
        self.assertEqual(bootstrap.check(self.root), [])

    def test_one_top_level_key_per_bootstrap_output(self) -> None:
        # Guard against double injection: any rendered JSON bootstrap must carry
        # exactly one top-level key (session-start-bootstrap).
        write_harness(
            self.root,
            "claude-code",
            {
                "name": "claude-code",
                "bootstrap": {
                    "supported": True,
                    "shape": "A",
                    "native_key": "hookSpecificOutput",
                    "outputs": [
                        {"path": "harnesses/claude-code/bootstrap/hooks.json", "format": "json"},
                    ],
                },
                "tool_mapping": {},
            },
        )
        for rel, content in bootstrap.expected_outputs(self.root).items():
            if rel.endswith(".json") and "bootstrap/" in rel:
                data = json.loads(content)
                self.assertNotIn("additional_context", json.dumps(data))
                self.assertEqual(set(data), {"hooks"})


if __name__ == "__main__":
    unittest.main()
