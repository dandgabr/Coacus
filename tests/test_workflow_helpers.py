"""Exercise installed workflow helpers through their Python CLIs."""

from __future__ import annotations

import subprocess
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / "methodology/workflows/superpowers-subagent-driven-development/scripts"
EXEC = ROOT / "methodology/workflows/superpowers-executing-plans/scripts"


class TestWorkflowHelpers(unittest.TestCase):
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
            brief = repo / ".superpowers/sdd/plan/task-1-brief.md"
            self.assertIn("Do A.", brief.read_text())
            self.assertNotIn("Do B.", brief.read_text())
            (repo / "change.txt").write_text("changed\n")
            subprocess.run(["git", "-C", str(repo), "add", "change.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "change"], check=True)
            head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            subprocess.run([sys.executable, str(SDD / "review-package.py"), str(plan), base, head], cwd=repo, check=True)
            self.assertIn("change.txt", (repo / f".superpowers/sdd/plan/review-{base[:7]}..{head[:7]}.diff").read_text())

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
            self.assertFalse((repo / ".superpowers/sdd/plan/progress.md").exists())
            env = dict(os.environ, PYTHONIOENCODING="cp1252")
            good = subprocess.run([sys.executable, str(EXEC / "task-done.py"), str(plan), "1", base, "--", sys.executable, "-c", "print('tests passed'); print(chr(233))"], cwd=repo, capture_output=True, encoding="cp1252", env=env, check=True)
            self.assertIn("Task 1: complete", good.stdout)
            self.assertIn("tests passed", (repo / ".superpowers/sdd/plan/progress.md").read_text())


if __name__ == "__main__":
    unittest.main()
