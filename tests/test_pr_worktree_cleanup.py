"""Exercise worktree cleanup against real, disposable Git repositories."""

from __future__ import annotations

import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


HELPER = (
    Path(__file__).resolve().parents[1]
    / "methodology/workflows/using-git-worktrees/scripts/pr-worktree.py"
)


@unittest.skipUnless(shutil.which("git"), "Git is required")
class TestPRWorktreeCleanup(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        self.repo = root / "main checkout"
        self.tree = root / "feature checkout"
        self.remote = root / "delivery remote.git"
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, LC_ALL="C")
        self.git("init", "--initial-branch=main", self.repo, cwd=root)
        self.git("init", "--bare", self.remote, cwd=root)
        self.git("config", "user.name", "Coacus Test")
        self.git("config", "user.email", "coacus@example.invalid")
        (self.repo / ".gitignore").write_text("local.env\n", encoding="utf-8")
        (self.repo / "tracked.txt").write_text("original\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "Initial commit")
        self.git("remote", "add", "origin", self.remote)
        self.git("worktree", "add", "-b", "feature", self.tree)
        self.oid = self.git("rev-parse", "HEAD", cwd=self.tree).strip()

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env,
            capture_output=True, text=True, check=True,
        ).stdout

    def command(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, HELPER, *args], cwd=cwd or self.repo, env=self.env,
            capture_output=True, text=True,
        )

    def mark(self):
        result = self.command("mark", self.tree)
        self.assertEqual(result.returncode, 0, result.stderr)

    def publish(self):
        self.git("push", "origin", "refs/heads/feature")

    def cleanup(self, *, head_oid=None, head_ref="refs/heads/feature", cwd=None):
        return self.command(
            "cleanup", self.tree, "--remote", "origin", "--head-ref", head_ref,
            "--head-oid", head_oid or self.oid, cwd=cwd,
        )

    def assert_kept(self, reason, **kwargs):
        result = self.cleanup(**kwargs)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(reason, result.stderr)
        self.assertTrue(self.tree.is_dir())

    def test_clean_published_worktree_is_removed_and_can_be_recreated(self):
        self.mark()
        self.publish()
        result = self.cleanup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("removed", result.stdout)
        self.assertFalse(self.tree.exists())
        self.assertEqual(self.git("rev-parse", "refs/heads/feature").strip(), self.oid)
        self.assertTrue(self.git("ls-remote", "origin", "refs/heads/feature").startswith(self.oid))
        repeated = self.cleanup()
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn("already absent", repeated.stdout)
        self.git("worktree", "add", self.tree, "feature")
        self.assert_kept("ownership")

    def test_unpublished_or_moved_remote_branch_is_preserved(self):
        self.mark()
        self.assert_kept("remote")
        self.publish()
        self.git("commit", "--allow-empty", "-m", "Advance published branch", cwd=self.tree)
        self.publish()
        self.git("reset", "--hard", self.oid, cwd=self.tree)
        self.assert_kept("remote")

    def test_push_url_rewrite_cannot_verify_a_different_remote(self):
        self.mark()
        self.publish()
        empty = self.remote.parent / "empty.git"
        self.git("init", "--bare", empty)
        self.git("config", "remote.origin.pushurl", "delivery-alias:")
        self.git("config", f"url.{empty}.insteadOf", "delivery-alias:")
        self.git("config", f"url.{self.remote}.insteadOf", str(empty))
        self.assert_kept("push destination")

    def test_unmarked_locked_or_detached_worktree_is_preserved(self):
        self.publish()
        self.assert_kept("ownership")
        self.mark()
        self.git("worktree", "lock", self.tree)
        self.assert_kept("locked")
        self.git("worktree", "unlock", self.tree)
        self.git("checkout", "--detach", cwd=self.tree)
        self.assert_kept("branch")

    def test_branch_and_commit_must_match_the_confirmed_pr(self):
        self.mark()
        self.publish()
        self.assert_kept("branch", head_ref="refs/heads/main")
        self.git("commit", "--allow-empty", "-m", "Local commit", cwd=self.tree)
        self.assert_kept("commit")

    def test_rechecks_local_commit_after_remote_verification(self):
        self.mark()
        self.publish()
        helper = runpy.run_path(str(HELPER))
        cleanup = helper["cleanup"]
        real_git = helper["git"]

        def git_with_concurrent_commit(directory, *args, **kwargs):
            result = real_git(directory, *args, **kwargs)
            if args[0] == "ls-remote":
                self.git("commit", "--allow-empty", "-m", "Concurrent commit", cwd=self.tree)
            return result

        with patch.dict(os.environ, self.env, clear=True):
            with patch.dict(cleanup.__globals__, git=git_with_concurrent_commit):
                with self.assertRaisesRegex(helper["KeepWorktree"], "commit changed"):
                    cleanup(self.tree, self.repo, "origin", "refs/heads/feature", self.oid)
        self.assertTrue(self.tree.is_dir())

    def test_tracked_untracked_and_ignored_files_are_preserved(self):
        self.mark()
        self.publish()
        for name, original in (("tracked.txt", "original\n"), ("untracked", None), ("local.env", None)):
            with self.subTest(name=name):
                path = self.tree / name
                path.write_text("local contents\n", encoding="utf-8")
                self.assert_kept("local files")
                self.assertEqual(path.read_text(encoding="utf-8"), "local contents\n")
                if original is None:
                    path.unlink()
                else:
                    path.write_text(original, encoding="utf-8")

    def test_staged_only_edit_is_preserved_even_with_an_alternate_index(self):
        self.mark()
        self.publish()
        path = self.tree / "tracked.txt"
        path.write_text("staged edit\n", encoding="utf-8")
        self.git("add", "tracked.txt", cwd=self.tree)
        path.write_text("original\n", encoding="utf-8")
        self.assert_kept("staged changes")
        self.env["GIT_INDEX_FILE"] = str(self.repo / ".git" / "index")
        self.assert_kept("Git environment")

    def test_assumed_unchanged_edits_are_preserved(self):
        self.mark()
        self.publish()
        self.git("update-index", "--assume-unchanged", "tracked.txt", cwd=self.tree)
        (self.tree / "tracked.txt").write_text("hidden edit\n", encoding="utf-8")
        self.assert_kept("index flags")

    def test_skip_worktree_edits_are_preserved(self):
        self.mark()
        self.publish()
        self.git("update-index", "--skip-worktree", "tracked.txt", cwd=self.tree)
        (self.tree / "tracked.txt").write_text("hidden edit\n", encoding="utf-8")
        self.assert_kept("index flags")

    @unittest.skipIf(os.name == "nt", "Requires POSIX change timestamps")
    def test_tracked_edit_with_original_mtime_and_size_is_preserved(self):
        self.mark()
        self.publish()
        self.git("config", "core.trustctime", "false")
        path = self.tree / "tracked.txt"
        os.utime(path, (946684800, 946684800))
        self.git("update-index", "--refresh", cwd=self.tree)
        original = path.stat()
        path.write_bytes(b"changed!\n")
        os.utime(path, ns=(original.st_atime_ns, original.st_mtime_ns))
        self.assertEqual(self.git("status", "--porcelain", cwd=self.tree), "")
        self.assert_kept("local files")

    @unittest.skipIf(os.name == "nt", "Requires POSIX executable permission bits")
    def test_executable_bit_change_is_preserved_even_if_git_config_hides_it(self):
        self.mark()
        self.publish()
        self.git("config", "core.filemode", "false")
        path = self.tree / "tracked.txt"
        path.chmod(path.stat().st_mode | 0o100)
        self.assertEqual(self.git("status", "--porcelain", cwd=self.tree), "")
        self.assert_kept("local files")

    def test_unreferenced_commit_in_worktree_history_is_preserved(self):
        self.mark()
        self.publish()
        self.git("checkout", "--detach", cwd=self.tree)
        self.git("commit", "--allow-empty", "-m", "Local experiment", cwd=self.tree)
        self.git("checkout", "feature", cwd=self.tree)
        self.assert_kept("checkout history")

    def test_private_worktree_ref_is_preserved(self):
        self.mark()
        self.publish()
        self.git("checkout", "--detach", cwd=self.tree)
        self.git("commit", "--allow-empty", "-m", "Local experiment", cwd=self.tree)
        self.git("update-ref", "refs/worktree/saved-experiment", "HEAD", cwd=self.tree)
        self.git("checkout", "feature", cwd=self.tree)
        self.assert_kept("private Git refs")

    def test_worktree_specific_git_config_is_preserved(self):
        self.mark()
        self.publish()
        self.git("config", "extensions.worktreeConfig", "true")
        self.git("config", "--worktree", "coacus.local-setting", "kept", cwd=self.tree)
        self.assert_kept("worktree-specific Git configuration")

    def test_in_progress_merge_is_preserved_even_when_status_is_clean(self):
        self.mark()
        self.publish()
        self.git("commit", "--allow-empty", "-m", "Other commit")
        self.git("merge", "--no-commit", "--no-ff", "main", cwd=self.tree)
        self.assertEqual(self.git("status", "--porcelain", cwd=self.tree), "")
        self.assert_kept("in progress")

    def test_caller_must_be_in_the_same_repository_outside_the_worktree(self):
        self.mark()
        self.publish()
        self.assert_kept("outside", cwd=self.tree)
        self.assert_kept("repository", cwd=self.remote)

    def test_primary_checkout_cannot_be_marked(self):
        result = self.command("mark", self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked worktree", result.stderr)
