"""Exercise installed workflow helpers through their Python CLIs."""

from __future__ import annotations

import subprocess
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / "methodology/workflows/subagent-driven-development/scripts"
EXEC = ROOT / "methodology/workflows/executing-plans/scripts"


class TestWorkflowHelpers(unittest.TestCase):
    def test_brief_retains_multiline_spec_and_constraints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            plan = repo / "plan.md"
            brief = repo / "brief.md"
            plan.write_text("# Plan\n\n**Spec:** first line\nsecond line\n\n## Global Constraints\nKeep this.\n\n## Task 1: First\nDo A.\n\n## Task 2: Second\nDo B.\n")
            subprocess.run([sys.executable, str(SDD / "task-brief.py"), str(plan), "1", str(brief)], check=True)
            text = brief.read_text()
            self.assertIn("**Spec:** first line\nsecond line", text)
            self.assertIn("Keep this.", text)
            self.assertIn("Do A.", text)
            self.assertNotIn("Do B.", text)

    def test_brief_workspace_and_review_range(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            plan = repo / "plan.md"
            plan.write_text("# Plan\n\n## Task 1: First\nDo A.\n\n## Task 2: Second\nDo B.\n")
            subprocess.run(["git", "-C", str(repo), "add", "plan.md"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
            base = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            subprocess.run([sys.executable, str(SDD / "task-brief.py"), str(plan), "1"], cwd=repo, check=True)
            brief = repo / ".coacus/sdd/plan/task-1-brief.md"
            self.assertIn("Do A.", brief.read_text())
            self.assertNotIn("Do B.", brief.read_text())
            (repo / "change.txt").write_text("changed\n")
            subprocess.run(["git", "-C", str(repo), "add", "change.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "change"], check=True)
            head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            subprocess.run([sys.executable, str(SDD / "review-package.py"), str(plan), base, head], cwd=repo, check=True)
            self.assertIn("change.txt", (repo / f".coacus/sdd/plan/review-{base[:7]}..{head[:7]}.diff").read_text())

    def test_brief_includes_shared_sections_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            plan = repo / "plan.md"
            brief = repo / "brief.md"
            plan.write_text(
                "# Plan\n\n## Global Constraints\nShared constraint.\n"
                "### Details\nNested constraint.\n\n## Review Focus\nShared review focus.\n"
                "\n## Task 1: First\nFirst task only.\n"
                "\n## Task 2: Second\nSecond task only.\n"
            )
            subprocess.run([sys.executable, str(SDD / "task-brief.py"), str(plan), "2", str(brief)], check=True, capture_output=True)
            text = brief.read_text()
            for expected in ("Shared constraint.", "Nested constraint.", "Shared review focus.", "Second task only."):
                self.assertIn(expected, text)
            self.assertNotIn("First task only.", text)
            self.assertNotIn("Task 1: First", text)

    def test_review_package_multi_commit_and_invalid_ranges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def git(*args: str) -> str:
                return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE).strip()

            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            git("config", "user.email", "test@example.com")
            git("config", "user.name", "Test")
            plan = repo / "plan.md"
            plan.write_text("## Task 1: First\nDo A.\n")
            git("add", "plan.md")
            git("commit", "-qm", "base")
            base = git("rev-parse", "HEAD")
            commits = []
            for name in ("first.txt", "second.txt"):
                (repo / name).write_text(f"content for {name}\n")
                git("add", name)
                git("commit", "-qm", f"add {name}")
                commits.append(git("rev-parse", "--short", "HEAD"))
            head = git("rev-parse", "HEAD")
            out = repo / "review.diff"
            command = [sys.executable, str(SDD / "review-package.py"), str(plan)]
            result = subprocess.run([*command, base, head, str(out)], cwd=repo, capture_output=True, text=True, check=True)
            self.assertIn("2 commit(s)", result.stdout)
            text = out.read_text()
            commits_section = text.split("## Commits\n", 1)[1].split("\n## Files changed\n", 1)[0]
            for commit in commits:
                self.assertIn(commit, commits_section)
            for name in ("first.txt", "second.txt"):
                self.assertIn(f"diff --git a/{name} b/{name}", text)
                self.assertIn(f"+content for {name}", text)

            git("checkout", "--orphan", "unrelated")
            git("rm", "-q", "-rf", ".")
            (repo / "orphan.txt").write_text("orphan\n")
            git("add", "orphan.txt")
            git("commit", "-qm", "unrelated")
            unrelated = git("rev-parse", "HEAD")
            plan.write_text("## Task 1: First\nDo A.\n")
            for start, end in (("invalid-revision", head), (head, base), (base, unrelated), (base, base)):
                with self.subTest(start=start, end=end):
                    rejected = repo / "rejected.diff"
                    result = subprocess.run([*command, start, end, str(rejected)], cwd=repo, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(rejected.exists())

    def test_task_done_records_only_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            plan = repo / "plan.md"
            plan.write_text("## Task 1: First\nDo A.\n")
            subprocess.run(["git", "-C", str(repo), "add", "plan.md"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
            base = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            start = subprocess.run([sys.executable, str(EXEC / "task-start.py"), str(plan), "1"], cwd=repo, text=True, capture_output=True, check=True)
            self.assertIn("base: " + base, start.stdout)
            self.assertIn("brief: ", start.stdout)
            bad = subprocess.run([sys.executable, str(EXEC / "task-done.py"), str(plan), "1", base, "--", sys.executable, "-c", "raise SystemExit(7)"], cwd=repo)
            self.assertEqual(bad.returncode, 7)
            self.assertFalse((repo / ".coacus/sdd/plan/progress.md").exists())
            env = dict(os.environ, PYTHONIOENCODING="cp1252")
            good = subprocess.run([sys.executable, str(EXEC / "task-done.py"), str(plan), "1", base, "--", sys.executable, "-c", "print('tests passed'); print(chr(233))"], cwd=repo, capture_output=True, encoding="cp1252", env=env, check=True)
            self.assertIn("Task 1: complete", good.stdout)
            self.assertIn("tests passed", (repo / ".coacus/sdd/plan/progress.md").read_text())


if __name__ == "__main__":
    unittest.main()
