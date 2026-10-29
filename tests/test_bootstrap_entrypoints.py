"""Exercise the POSIX bootstrap without installing Python or touching harnesses."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name == "posix", "POSIX bootstrap requires bash")
class BootstrapTests(unittest.TestCase):
    def test_incompatible_existing_environment_stops_before_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copy(ROOT / "install.sh", root / "install.sh")
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            fake_python = fake_bin / "python3.14"
            fake_python.write_text(f"#!{sys.executable}\nprint('3.12')\n", encoding="utf-8")
            fake_python.chmod(0o755)
            venv_python = root / ".venv" / "bin" / "python"
            venv_python.parent.mkdir(parents=True)
            venv_python.write_text(f"#!{sys.executable}\nimport sys\nsys.exit(1)\n", encoding="utf-8")
            venv_python.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:/usr/bin:/bin"
            result = subprocess.run(
                ["bash", str(root / "install.sh"), "codex"],
                cwd=root, env=env, text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Existing .venv requires Python 3.12+", result.stdout)
            self.assertNotIn("Installing language-gate dependencies", result.stdout)

    def test_fresh_environment_installs_gate_dependencies_before_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copy(ROOT / "install.sh", root / "install.sh")
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            fake_python = fake_bin / "python3.14"
            fake_python.write_text(
                f"#!{sys.executable}\n"
                "import json, os, pathlib, shutil, sys\n"
                "args = sys.argv[1:]\n"
                "events = pathlib.Path(os.environ['COACUS_TEST_EVENTS'])\n"
                "with events.open('a') as out: out.write(json.dumps(args) + '\\n')\n"
                "if args and args[0] == '-c': print('3.12'); sys.exit(0)\n"
                "if args[:2] == ['-m', 'venv']:\n"
                "  dest = pathlib.Path(args[2]) / 'bin' / 'python'\n"
                "  dest.parent.mkdir(parents=True); shutil.copy(sys.argv[0], dest); dest.chmod(0o755); sys.exit(0)\n"
                "marker = events.parent / 'dependencies-ready'\n"
                "if args[:3] == ['-m', 'pip', 'install']:\n"
                "  marker.touch(); sys.exit(0)\n"
                "if args[:2] == ['scripts/coacus.py', 'generate']:\n"
                "  sys.exit(0 if marker.exists() else 7)\n"
                "if args and args[0] == 'scripts/coacus_install.py': sys.exit(0)\n"
                "sys.exit(8)\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:/usr/bin:/bin"
            env["COACUS_TEST_EVENTS"] = str(root / "events.jsonl")
            result = subprocess.run(
                ["bash", str(root / "install.sh"), "codex"],
                cwd=root, env=env, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            events = [json.loads(line) for line in (root / "events.jsonl").read_text().splitlines()]
            installs = [e for e in events if e[:3] == ["-m", "pip", "install"]]
            self.assertEqual(len(installs), 1)
            self.assertIn("lingua-language-detector==2.2.0", installs[0])
            self.assertIn("wordfreq==3.1.1", installs[0])
            self.assertLess(events.index(installs[0]), events.index(["scripts/coacus.py", "generate"]))


if __name__ == "__main__":
    unittest.main()
