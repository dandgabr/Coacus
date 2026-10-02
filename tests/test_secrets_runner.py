"""Verify scanner downloads before extracting the single executable."""

from __future__ import annotations

import hashlib
import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path


class TestSecretsRunner(unittest.TestCase):
    def test_verified_archives_extract_only_the_executable(self) -> None:
        from scripts.coacus_secrets import install_binary
        for windows in (False, True):
            with self.subTest(windows=windows), tempfile.TemporaryDirectory() as tmp:
                buffer = io.BytesIO()
                name = "gitleaks.exe" if windows else "gitleaks"
                if windows:
                    with zipfile.ZipFile(buffer, "w") as archive:
                        archive.writestr(name, b"binary")
                        archive.writestr("../../escape", b"ignore")
                else:
                    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
                        member = tarfile.TarInfo(name)
                        member.size = 6
                        archive.addfile(member, io.BytesIO(b"binary"))
                content = buffer.getvalue()
                target = Path(tmp) / name
                install_binary(content, hashlib.sha256(content).hexdigest(), target)
                self.assertEqual(target.read_bytes(), b"binary")
                self.assertEqual([p.name for p in target.parent.iterdir()], [name])

    def test_checksum_mismatch_writes_nothing(self) -> None:
        from scripts.coacus_secrets import install_binary
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "gitleaks"
            with self.assertRaises(ValueError):
                install_binary(b"untrusted", "0" * 64, target)
            self.assertFalse(target.exists())
