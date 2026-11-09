"""Verify scanner downloads before extracting the single executable."""

from __future__ import annotations

import hashlib
import io
import os
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch


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

    def test_staging_excludes_untracked_and_symlink_targets(self) -> None:
        from scripts.coacus_secrets import stage_tracked_files
        if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
            self.skipTest("secure directory-relative open unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            dest = Path(tmp) / "staged"
            root.mkdir()
            dest.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "odd\nname").write_text("tracked synthetic")
            (root / "untracked").write_text("untracked synthetic")
            (root / "link").symlink_to("untracked")
            subprocess.run(["git", "-C", str(root), "add", "odd\nname", "link"], check=True)
            stage_tracked_files(root, dest)
            self.assertEqual((dest / "odd\nname").read_text(), "tracked synthetic")
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ["odd\nname"])

    def test_scanner_output_is_suppressed_for_synthetic_payload(self) -> None:
        from scripts.coacus_secrets import main
        payload = "address@example.invalid 123e4567-e89b-12d3-a456-426614174000 synthetic-token"
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"archive"
        real_run = subprocess.run
        def fake_run(args, **kwargs):
            if len(args) > 1 and args[1] in ("git", "dir"):
                return real_run([__import__("sys").executable, "-c",
                                 "import sys; print(sys.argv[1]); print(sys.argv[1], file=sys.stderr)", payload], **kwargs)
            return real_run(args, **kwargs)
        with tempfile.TemporaryDirectory() as tmp, \
             patch("scripts.coacus_secrets.platform.system", return_value="Linux"), \
             patch("scripts.coacus_secrets.platform.machine", return_value="x86_64"), \
             patch("scripts.coacus_secrets.urllib.request.urlopen", return_value=response), \
             patch("scripts.coacus_secrets.install_binary"), \
             patch("scripts.coacus_secrets.stage_tracked_files"), \
             patch("scripts.coacus_secrets.subprocess.run", side_effect=fake_run), \
             patch("sys.stdout", new_callable=io.StringIO) as out, \
             patch("sys.stderr", new_callable=io.StringIO) as err:
            self.assertEqual(main(["--root", tmp]), 0)
            for item in payload.split():
                self.assertNotIn(item, out.getvalue() + err.getvalue())

    def test_staging_fails_on_git_error(self) -> None:
        from scripts.coacus_secrets import stage_tracked_files
        if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
            self.skipTest("secure directory-relative open unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(subprocess.CalledProcessError):
                stage_tracked_files(Path(tmp), Path(tmp))

    def test_unsupported_staging_fails_closed(self) -> None:
        from scripts.coacus_secrets import stage_tracked_files
        with patch.object(os, "supports_dir_fd", set()), \
             patch("scripts.coacus_secrets.subprocess.run") as run:
            with self.assertRaises(RuntimeError):
                stage_tracked_files(Path("unused"), Path("unused"))
            run.assert_not_called()

    def test_intermediate_symlink_is_not_followed(self) -> None:
        from scripts.coacus_secrets import stage_tracked_files
        if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
            self.skipTest("secure directory-relative open unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root, dest, outside = (Path(tmp) / name for name in ("repo", "out", "outside"))
            for directory in (root, dest, outside):
                directory.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "nested").mkdir()
            (root / "nested" / "file").write_text("tracked")
            subprocess.run(["git", "-C", str(root), "add", "nested/file"], check=True)
            (root / "nested" / "file").unlink()
            (root / "nested").rmdir()
            (outside / "file").write_text("synthetic outside")
            (root / "nested").symlink_to(outside, target_is_directory=True)
            stage_tracked_files(root, dest)
            self.assertFalse((dest / "nested").exists())

    def test_worktree_and_staging_failures_fail_closed(self) -> None:
        from scripts.coacus_secrets import main
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"archive"
        with tempfile.TemporaryDirectory() as tmp, \
             patch("scripts.coacus_secrets.platform.system", return_value="Linux"), \
             patch("scripts.coacus_secrets.platform.machine", return_value="x86_64"), \
             patch("scripts.coacus_secrets.urllib.request.urlopen", return_value=response), \
             patch("scripts.coacus_secrets.install_binary"), \
             patch("scripts.coacus_secrets.stage_tracked_files") as stage, \
             patch("scripts.coacus_secrets.subprocess.run") as run:
            run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=1)]
            self.assertEqual(main(["--root", tmp]), 1)
            run.reset_mock(side_effect=True)
            run.return_value.returncode = 0
            stage.side_effect = RuntimeError("synthetic")
            self.assertEqual(main(["--root", tmp]), 1)
            self.assertEqual(run.call_count, 1)

    def test_scans_silently_and_propagates_history_failure(self) -> None:
        from scripts.coacus_secrets import main
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"archive"
        with tempfile.TemporaryDirectory() as tmp, \
             patch("scripts.coacus_secrets.platform.system", return_value="Linux"), \
             patch("scripts.coacus_secrets.platform.machine", return_value="x86_64"), \
             patch("scripts.coacus_secrets.urllib.request.urlopen", return_value=response), \
             patch("scripts.coacus_secrets.install_binary"), \
             patch("scripts.coacus_secrets.stage_tracked_files") as stage, \
             patch("scripts.coacus_secrets.subprocess.run") as run:
            run.side_effect = [MagicMock(returncode=1), MagicMock(returncode=0)]
            self.assertEqual(main(["--root", tmp]), 1)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertEqual([command[1] for command in commands], ["git", "dir"])
            self.assertIn("--log-opts=--all", commands[0])
            self.assertEqual(commands[1][-1], str(stage.call_args.args[1]))
            for call in run.call_args_list:
                self.assertEqual(call.kwargs["stdout"], subprocess.DEVNULL)
                self.assertEqual(call.kwargs["stderr"], subprocess.DEVNULL)
                self.assertIn("--redact", call.args[0])

    def test_checksum_mismatch_writes_nothing(self) -> None:
        from scripts.coacus_secrets import install_binary
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "gitleaks"
            with self.assertRaises(ValueError):
                install_binary(b"untrusted", "0" * 64, target)
            self.assertFalse(target.exists())
