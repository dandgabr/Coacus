"""Safety checks for the brainstorm workflow's local server lifecycle."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "methodology/workflows/brainstorming/scripts"


def load_script(name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


start_server = load_script("start_server")
stop_server = load_script("stop_server")


class TestBrainstormServerHelpers(unittest.TestCase):
    def test_default_session_directory_uses_system_temp_directory(self) -> None:
        expected = Path(tempfile.gettempdir()).resolve() / "brainstorm-audit-session"
        self.assertEqual(start_server.default_session_dir("audit-session"), expected)

    def test_stop_preserves_project_directory_containing_brainstorm_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session_dir = Path(temp) / "my-brainstorm-project"
            state_dir = session_dir / "state"
            state_dir.mkdir(parents=True)
            (state_dir / "server.pid").write_text("987654321\n", encoding="utf-8")

            with mock.patch.object(
                stop_server.os, "kill", side_effect=[None, ProcessLookupError]
            ):
                result = stop_server.main([str(session_dir)])

            self.assertEqual(result, 0)
            self.assertTrue(session_dir.is_dir())

    def test_stale_pid_preserves_ephemeral_session_and_marks_stopped(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            session_dir = Path(temp) / "brainstorm-audit-cleanup"
            state_dir = session_dir / "state"
            state_dir.mkdir(parents=True)
            pid_file = state_dir / "server.pid"
            pid_file.write_text("987654321\n", encoding="utf-8")
            with mock.patch.object(stop_server.os, "pidfd_open", side_effect=ProcessLookupError):
                result = stop_server.main([str(session_dir)])
            self.assertEqual(result, 0)
            self.assertTrue(session_dir.is_dir())
            self.assertFalse(pid_file.exists())
            self.assertIn('"reason": "stale_pid"', (state_dir / "server-stopped").read_text())


if __name__ == "__main__":
    unittest.main()
