"""Tests for MCP generation and validation (D4/mcp-definition amended)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.generators import mcp_configs
from engine.validators import mcps

MCP_SOURCE = """---
name: sample-mcp
description: >-
  Connects to a sample service. Use when testing MCP generation.
transport: stdio
command: npx
args:
  - -y
  - "@scope/sample-mcp"
env_vars:
  - SAMPLE_KEY
capabilities:
  tools: true
  resources: false
capabilities_extra: {}
---

# Sample MCP

Body.
"""


def make_mcp(root: Path, text: str = MCP_SOURCE) -> Path:
    directory = root / "knowledge" / "mcps" / "sample-mcp"
    directory.mkdir(parents=True)
    source = directory / "MCP.md"
    source.write_text(text, encoding="utf-8")
    return source


class TestMcpGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_emits_dist_declaration_and_config(self) -> None:
        make_mcp(self.root)
        outputs = mcp_configs.expected_outputs(self.root)
        self.assertEqual(
            set(outputs),
            {
                "knowledge/mcps/sample-mcp/dist/mcp.json",
                "knowledge/mcps/sample-mcp/dist/mcp_config.json",
            },
        )
        server = json.loads(outputs["knowledge/mcps/sample-mcp/dist/mcp.json"])
        self.assertEqual(server["transport"], "stdio")
        self.assertEqual(server["command"], "npx")
        self.assertEqual(server["env"]["SAMPLE_KEY"], "{env:SAMPLE_KEY}")
        self.assertEqual(server["capabilities"]["tools"], True)

    def test_config_lists_env_names_not_values(self) -> None:
        make_mcp(self.root)
        outputs = mcp_configs.expected_outputs(self.root)
        config = json.loads(outputs["knowledge/mcps/sample-mcp/dist/mcp_config.json"])
        self.assertEqual(config["env_vars"], ["SAMPLE_KEY"])
        self.assertNotIn("value", json.dumps(config).lower())

    def test_write_then_check_is_clean(self) -> None:
        make_mcp(self.root)
        mcp_configs.write_all(self.root)
        self.assertEqual(mcp_configs.check(self.root), [])

    def test_orphan_dist_is_detected(self) -> None:
        make_mcp(self.root)
        mcp_configs.write_all(self.root)
        # Remove only the SOURCE, leaving the generated dist/ behind.
        (self.root / "knowledge/mcps/sample-mcp/MCP.md").unlink()
        drift = mcp_configs.check(self.root)
        self.assertTrue(any("orphan" in d for d in drift))

    def test_no_timestamps(self) -> None:
        make_mcp(self.root)
        for content in mcp_configs.expected_outputs(self.root).values():
            self.assertNotIn("timestamp", content.lower())


class TestMcpValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"

    def test_valid_source_passes(self) -> None:
        make_mcp(self.root)
        self.assertEqual(mcps.validate(self.root), [])

    def test_bad_transport_fails(self) -> None:
        make_mcp(self.root, MCP_SOURCE.replace("transport: stdio", "transport: local"))
        errors = mcps.validate(self.root)
        self.assertTrue(any("transport" in e for e in errors))

    def test_stdio_without_command_fails(self) -> None:
        text = MCP_SOURCE.replace("command: npx\n", "")
        make_mcp(self.root, text)
        errors = mcps.validate(self.root)
        self.assertTrue(any("requires 'command'" in e for e in errors))

    def test_http_without_url_fails(self) -> None:
        text = MCP_SOURCE.replace("transport: stdio", "transport: http").replace(
            "command: npx", "remote_unused: x"
        )
        make_mcp(self.root, text)
        errors = mcps.validate(self.root)
        self.assertTrue(any("requires 'remote_url'" in e for e in errors))

    def test_lowercase_env_name_fails(self) -> None:
        make_mcp(self.root, MCP_SOURCE.replace("  - SAMPLE_KEY", "  - sample_key"))
        errors = mcps.validate(self.root)
        self.assertTrue(any("upper-case name" in e for e in errors))

    def test_duplicate_mcp_name_fails(self) -> None:
        import shutil

        make_mcp(self.root)
        shutil.copytree(
            self.root / "knowledge/mcps/sample-mcp",
            self.root / "knowledge/mcps/other-mcp",
        )
        errors = mcps.validate(self.root)
        self.assertTrue(any("duplicate MCP name" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
