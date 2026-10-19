"""Tests for the Antigravity on-demand capability package."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_install
from scripts.coacus_catalog_mcp import Catalog, handle_message, serve


class TestCatalogMcp(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        skill = self.root / "corpus/knowledge/skills/security/ai/agent-risk/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: agent-risk\ndescription: Test skill\n---\n\nSKILL BODY\n", encoding="utf-8")
        reference = skill.parent / "references/guide.md"
        reference.parent.mkdir()
        reference.write_text("REFERENCE BODY\n", encoding="utf-8")
        agent = self.root / "corpus/knowledge/agents/security/ai/agent.source.md"
        agent.parent.mkdir(parents=True)
        agent.write_text(
            "---\nname: ai-security\ndescription: Test agent\nskills:\n  - knowledge/skills/security/ai/agent-risk/SKILL.md\n---\n\nAGENT BODY\n",
            encoding="utf-8",
        )
        (self.root / "catalog").mkdir()
        (self.root / "catalog/index.json").write_text(
            json.dumps(
                {
                    "schema": 1,
                    "skills": [
                        {
                            "name": "agent-risk",
                            "kind": "skill",
                            "category": "security/ai",
                            "description": "Test skill",
                            "source": "knowledge/skills/security/ai/agent-risk/SKILL.md",
                            "payload": "corpus/knowledge/skills/security/ai/agent-risk/SKILL.md",
                        }
                    ],
                    "agents": [
                        {
                            "name": "ai-security",
                            "kind": "agent",
                            "category": "security/ai",
                            "description": "Test agent",
                            "source": "knowledge/agents/security/ai/agent.source.md",
                            "payload": "corpus/knowledge/agents/security/ai/agent.source.md",
                            "skills": ["agent-risk"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.catalog = Catalog(self.root)

    def test_search_is_deterministic_and_filters_by_kind(self) -> None:
        result = self.catalog.search("security", kind="agent", limit=4)
        self.assertEqual([entry["name"] for entry in result], ["ai-security"])
        self.assertEqual(result[0]["kind"], "agent")

    def test_get_returns_canonical_body_and_agent_skill_associations(self) -> None:
        skill = self.catalog.get("agent-risk", kind="skill")
        agent = self.catalog.get("ai-security", kind="agent")
        self.assertIn("SKILL BODY", skill["content"])
        self.assertEqual(agent["associated_skills"], ["agent-risk"])
        self.assertIn("AGENT BODY", agent["content"])

    def test_reference_read_is_confined_to_capability_directory(self) -> None:
        result = self.catalog.get_reference("agent-risk", "references/guide.md")
        self.assertEqual(result["content"], "REFERENCE BODY\n")
        with self.assertRaises(ValueError):
            self.catalog.get_reference("agent-risk", "../../agents/ai-security/agent.source.md")

    def test_unknown_capability_and_reference_are_reported(self) -> None:
        with self.assertRaises(KeyError):
            self.catalog.get("missing", kind="skill")
        with self.assertRaises(FileNotFoundError):
            self.catalog.get_reference("agent-risk", "references/missing.md")

    def test_mcp_initialize_and_tools_list(self) -> None:
        init = handle_message(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
            self.catalog,
        )
        self.assertEqual(init["result"]["protocolVersion"], "2025-03-26")
        listed = handle_message(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            self.catalog,
        )
        self.assertEqual(
            {tool["name"] for tool in listed["result"]["tools"]},
            {"search", "get", "get_reference"},
        )

    def test_mcp_initialize_negotiates_supported_versions_and_rejects_missing(self) -> None:
        unknown = handle_message(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2026-07-28"}},
            self.catalog,
        )
        self.assertEqual(unknown["result"]["protocolVersion"], "2025-11-25")
        missing = handle_message(
            {"jsonrpc": "2.0", "id": 2, "method": "initialize", "params": {}},
            self.catalog,
        )
        self.assertEqual(missing["error"]["code"], -32602)

    def test_stdio_protocol_keeps_stdout_machine_readable(self) -> None:
        request = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}})
        output = io.StringIO()
        serve(io.StringIO(request + "\n"), output, self.catalog)
        messages = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(messages, [{"jsonrpc": "2.0", "id": 1, "result": {}}])

    def test_stdio_entrypoint_handles_initialize_and_tool_call(self) -> None:
        runtime = self.root / "coacus_catalog_mcp.py"
        source = Path(__file__).resolve().parents[1] / "scripts/coacus_catalog_mcp.py"
        shutil.copyfile(source, runtime)
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get", "arguments": {"kind": "skill", "name": "agent-risk"}}},
        ]
        process = subprocess.run(
            [sys.executable, str(runtime)],
            input="\n".join(json.dumps(request) for request in requests) + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        messages = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual([message["id"] for message in messages], [1, 2])
        self.assertIn("SKILL BODY", messages[1]["result"]["content"][0]["text"])
        self.assertEqual(process.stderr, "")


class TestAntigravityOnDemandInstall(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.root = self.base / "repo"
        skills = self.root / "knowledge/skills/security/ai/agent-risk"
        skills.mkdir(parents=True)
        (skills / "SKILL.md").write_text(
            "---\nname: agent-risk\ndescription: Risk review\n---\n\nFULL SKILL SOURCE MARKER\n",
            encoding="utf-8",
        )
        (skills / "references").mkdir()
        (skills / "references/guide.md").write_text("reference\n", encoding="utf-8")
        agent = self.root / "knowledge/agents/security/ai-security"
        agent.mkdir(parents=True)
        (agent / "agent.source.md").write_text(
            "---\nname: ai-security\ndescription: Security agent\nskills:\n  - knowledge/skills/security/ai/agent-risk/SKILL.md\n---\n\nFULL AGENT SOURCE MARKER\n",
            encoding="utf-8",
        )
        anti = self.root / "harnesses/antigravity/bootstrap"
        anti.mkdir(parents=True)
        (anti / "plugin.json").write_text('{"name":"coacus"}\n', encoding="utf-8")
        (anti / "coacus-rule.md").write_text("# Full rule\n", encoding="utf-8")
        (self.root / "harnesses/antigravity/coacus-on-demand-rule.md").write_text(
            "---\ntrigger: always_on\n---\nUse the Coacus catalog MCP.\n",
            encoding="utf-8",
        )
        (self.root / "scripts").mkdir()
        (self.root / "scripts/coacus_catalog_mcp.py").write_text("# runtime\n", encoding="utf-8")
        mcp = self.root / "knowledge/mcps/coacus-catalog"
        mcp.mkdir(parents=True)
        (mcp / "MCP.md").write_text(
            "---\nname: coacus-catalog\ndescription: Catalog\ntransport: stdio\n"
            "command: python3\nargs:\n  - coacus_catalog_mcp.py\n---\n# Catalog\n",
            encoding="utf-8",
        )
        self.config = self.base / "gemini"

    def test_on_demand_plan_keeps_sources_out_of_native_skill_roots(self) -> None:
        files = coacus_install.plan(
            "antigravity", self.root, self.config, antigravity_profile="on-demand"
        )
        planned = {target.relative_to(self.config).as_posix(): content for target, content in files}
        plugin = "config/plugins/coacus/"
        self.assertIn(plugin + "catalog/index.json", planned)
        self.assertIn(plugin + "catalog/corpus/knowledge/skills/security/ai/agent-risk/SKILL.md", planned)
        self.assertNotIn(plugin + "skills/agent-risk/SKILL.md", planned)
        self.assertIn(plugin + "agents/ai-security/agent.md", planned)
        self.assertIn("coacus-catalog", str(planned[plugin + "agents/ai-security/agent.md"]))
        self.assertNotIn("FULL AGENT SOURCE MARKER", str(planned[plugin + "agents/ai-security/agent.md"]))
        self.assertIn(plugin + "coacus_catalog_mcp.py", planned)
        mcp = json.loads(str(planned[plugin + "mcp_config.json"]))
        self.assertIn("coacus-catalog", mcp["mcpServers"])
        self.assertIn(plugin + "rules/coacus.md", planned)

    def test_full_profile_preserves_legacy_native_install(self) -> None:
        files = coacus_install.plan(
            "antigravity", self.root, self.config, antigravity_profile="full"
        )
        planned = {target.relative_to(self.config).as_posix(): content for target, content in files}
        self.assertIn("config/plugins/coacus/skills/agent-risk/SKILL.md", planned)
        self.assertIn("FULL AGENT SOURCE MARKER", str(planned["config/plugins/coacus/agents/ai-security/agent.md"]))
        self.assertIn("config/plugins/coacus/rules/coacus.md", planned)

    def test_install_verify_and_uninstall_record_profile(self) -> None:
        result = coacus_install.install(
            "antigravity", self.root, self.config, dry_run=False, force=True,
            antigravity_profile="on-demand",
        )
        self.assertIn("coacus-install.json", result["manifest"])
        manifest = json.loads((self.config / coacus_install.MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(manifest["antigravity_profile"], "on-demand")
        self.assertTrue(coacus_install.verify("antigravity", self.root, self.config)["ok"])
        coacus_install.install(
            "antigravity", self.root, self.config, dry_run=False, force=True,
            antigravity_profile="on-demand",
        )
        self.assertTrue(coacus_install.verify("antigravity", self.root, self.config)["ok"])
        (self.config / "config/plugins/coacus/catalog/corpus/knowledge/skills/security/ai/agent-risk/SKILL.md").write_text(
            "tampered\n", encoding="utf-8"
        )
        self.assertFalse(coacus_install.verify("antigravity", self.root, self.config)["ok"])
        removed = coacus_install.uninstall("antigravity", self.root, self.config)
        self.assertTrue(removed["removed"])
        self.assertFalse((self.config / "config/plugins/coacus").exists())

    def test_switching_from_full_to_on_demand_removes_owned_native_files(self) -> None:
        coacus_install.install(
            "antigravity", self.root, self.config, dry_run=False, force=True,
            antigravity_profile="full",
        )
        plugin = self.config / "config/plugins/coacus"
        native_skill = plugin / "skills/agent-risk/SKILL.md"
        self.assertTrue(native_skill.is_file())

        coacus_install.install(
            "antigravity", self.root, self.config, dry_run=False, force=True,
            antigravity_profile="on-demand",
        )

        self.assertFalse(native_skill.exists())
        self.assertFalse((plugin / "skills").exists())
        self.assertTrue(coacus_install.verify("antigravity", self.root, self.config)["ok"])


@unittest.skipUnless(shutil.which("agy"), "Antigravity CLI is available only on equipped Linux hosts")
class TestLinuxAntigravityRuntime(unittest.TestCase):
    def test_complete_catalog_is_retrievable_and_plugin_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / ".gemini"
            result = coacus_install.install(
                "antigravity", coacus_install.ROOT, config, dry_run=False, force=True,
                antigravity_profile="on-demand",
            )
            self.assertFalse(result.get("error"), result)
            report = coacus_install.verify("antigravity", coacus_install.ROOT, config)
            self.assertTrue(report["ok"], report)
            plugin = config / "config/plugins/coacus"
            self.assertFalse((plugin / "skills").exists())

            expected = json.loads((coacus_install.ROOT / "catalog/catalog.json").read_text(encoding="utf-8"))
            installed = json.loads((plugin / "catalog/index.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {row["name"] for row in installed["skills"]},
                {row["name"] for row in expected["skills"]},
            )
            self.assertEqual(
                {row["name"] for row in installed["agents"]},
                {row["name"] for row in expected["agents"]},
            )

            validation = subprocess.run(
                ["agy", "plugin", "validate", str(plugin)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

            first_skill = installed["skills"][0]
            server = subprocess.run(
                [sys.executable, str(plugin / "coacus_catalog_mcp.py")],
                input="\n".join(
                    json.dumps(request)
                    for request in (
                        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
                        {"jsonrpc": "2.0", "method": "notifications/initialized"},
                        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get", "arguments": {"kind": "skill", "name": first_skill["name"]}}},
                    )
                ) + "\n",
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(server.returncode, 0, server.stderr)
            payload = json.loads(server.stdout.splitlines()[1])["result"]["content"][0]["text"]
            self.assertEqual(json.loads(payload)["fingerprint"], first_skill["fingerprint"])


if __name__ == "__main__":
    unittest.main()
