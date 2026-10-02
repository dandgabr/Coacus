"""Cross-platform hook generation and execution contracts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import base64
import shlex
from pathlib import Path

from engine.generators import bootstrap
from scripts import coacus_install
from engine.governor.ledger import Ledger


ROOT = Path(__file__).resolve().parents[1]


class TestPythonOnlyHooks(unittest.TestCase):
    def test_windows_command_encodes_dynamic_arguments(self) -> None:
        argv = ["C:/Python/python.exe", "C:/repo&tools/scripts/helper.py", "%VAR%", "!value!"]
        with patch.object(coacus_install.os, "name", "nt"):
            command = coacus_install._command(argv)
        self.assertNotIn("repo&tools", command)
        self.assertNotIn("%VAR%", command)
        self.assertTrue(command.startswith('"C:/Python/python.exe" -c '))
        shim = shlex.split(command)[2]
        encoded = shim.split("b64decode('", 1)[1].split("'", 1)[0]
        self.assertEqual(json.loads(base64.b64decode(encoded)), argv[1:])
        self.assertTrue(coacus_install._entry_owned({"command": command}, {"/scripts/helper.py"}))

    def test_skill_install_omits_python_runtime_caches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            (skill / "helper.py").write_text("print('portable')\n")
            cache = skill / "__pycache__"
            cache.mkdir()
            (cache / "helper.cpython-310.pyc").write_bytes(b"cache")
            (skill / "helper.pyc").write_bytes(b"cache")
            self.assertEqual(coacus_install._skill_files(skill), [skill / "helper.py"])

    def test_session_start_payloads_execute_with_python(self) -> None:
        outputs = bootstrap.expected_outputs(ROOT)
        for harness in ("claude-code", "codex", "cursor", "command-code"):
            with self.subTest(harness=harness):
                rel = f"harnesses/{harness}/bootstrap/session-start.json"
                self.assertIn(rel, list(outputs))
                payload = json.loads(outputs[rel])
                expected = "additional_context" if harness == "cursor" else "hookSpecificOutput"
                self.assertEqual(set(payload), {expected})
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/coacus_session_start.py"), str(ROOT / rel)],
                    capture_output=True, text=True, check=True,
                )
                expected_payload = json.loads(coacus_install._substitute_json(
                    json.dumps(payload), "__COACUS_ROOT__", ROOT.as_posix()))
                self.assertEqual(json.loads(result.stdout), expected_payload)

    def test_generated_hooks_use_python_entrypoints(self) -> None:
        outputs = bootstrap.expected_outputs(ROOT)
        for path, content in outputs.items():
            if path.startswith("harnesses/") and path.endswith("hooks.json"):
                self.assertNotIn(".sh", content, path)
        self.assertFalse(any(path.endswith(".sh") for path in outputs))

    def test_installed_claude_command_runs_with_spaces_and_shell_characters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo&tools%COACUS_TEST_VAR%!literal'$"
            config = Path(tmp) / "config spaces"
            for rel in ("scripts/coacus_session_start.py",
                        "harnesses/claude-code/bootstrap/hooks.json",
                        "harnesses/claude-code/bootstrap/session-start.json",
                        "methodology/workflows/using-coacus/SKILL.md"):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            coacus_install.install("claude-code", root, config, dry_run=False)
            doc = json.loads((config / "plugins/coacus/hooks/hooks.json").read_text())
            command = doc["hooks"]["SessionStart"][0]["hooks"][0]["command"]
            # Exercise the harness shell contract with our generated fixture command.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)  # nosec B602
            self.assertEqual(set(json.loads(result.stdout)), {"hookSpecificOutput"})

    def test_reinstall_retires_manifest_owned_wrappers_and_workflow_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "codex"
            wrapper = config / "coacus/session-start.sh"
            helper = config.parent / ".agents/skills/superpowers-executing-plans/scripts/task-start"
            unowned = config / "user.sh"
            for target in (wrapper, helper, unowned):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("#!/usr/bin/env bash\necho old\n")
            (config / coacus_install.MANIFEST_NAME).write_text(json.dumps({"files": [str(wrapper), str(helper)]}))
            coacus_install.install("codex", ROOT, config, dry_run=False,
                                   skills=["superpowers-executing-plans"], agents=["no-match"])
            self.assertFalse(wrapper.exists())
            self.assertFalse(helper.exists())
            self.assertTrue(unowned.exists())
            self.assertTrue(helper.with_suffix(".py").exists())

    @unittest.skipUnless(shutil.which("node"), "OpenCode adapter requires Node")
    def test_native_opencode_adapter_calls_python_from_quoted_paths(self) -> None:
        import os
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo spaces 'quote"
            config = Path(tmp) / "config spaces"
            for rel in ("harnesses/opencode/bootstrap/coacus.js",
                        "harnesses/opencode/bootstrap/governor-gate.js",
                        "scripts/coacus_governor.py", "engine/__init__.py",
                        "engine/governor/__init__.py", "engine/governor/ledger.py"):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            coacus_install.install("opencode", root, config, dry_run=False)
            plugin = (config / "plugins/coacus-governor.js").as_uri()
            code = f"import {{ CoacusGovernor }} from {json.dumps(plugin)}; const hooks = await CoacusGovernor(); await hooks['tool.execute.before']({{tool:'task',sessionID:'test',callID:'1'}},{{args:{{}}}});"
            state = Path(tmp) / "state"
            env = dict(os.environ, GOVERNOR_STATE_DIR=str(state), ORCH_MAX_CONCURRENT="3")
            result = subprocess.run([shutil.which("node"), "--input-type=module", "-e", code], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Ledger(state, max_total=3).status()["running"], 1)


if __name__ == "__main__":
    unittest.main()
