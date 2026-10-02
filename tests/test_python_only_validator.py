"""The hygiene gate rejects operational shell scripts, including extensionless ones."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.validators import hygiene


class TestPythonOnlyValidator(unittest.TestCase):
    def test_rejects_shell_extension_and_extensionless_shebang(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "methodology/workflows/example/scripts"
            folder.mkdir(parents=True)
            (folder / "hook.sh").write_text("echo legacy\n")
            (folder / "helper").write_text("#!/usr/bin/env bash\necho legacy\n")
            errors = hygiene.validate(root)
            self.assertTrue(any("hook.sh" in error for error in errors))
            self.assertTrue(any("helper" in error for error in errors))

    def test_checks_root_scripts_and_disguised_shebangs_but_allows_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "install.sh").write_text("#!/usr/bin/env bash\n")
            (root / "install.ps1").write_text("Write-Host bootstrap\n")
            (root / "legacy.cmd").write_text("echo old\n")
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "disguised.py").write_text("#!/usr/bin/env sh\necho old\n")
            errors = hygiene.validate(root)
            self.assertTrue(any("legacy.cmd" in error for error in errors))
            self.assertTrue(any("disguised.py" in error for error in errors))
            self.assertFalse(any("install.sh" in error or "install.ps1" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
