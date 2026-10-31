import unittest
from pathlib import Path

from scripts.coacus_install import _codex_profile_visible


class CodexRepositoryProfileTests(unittest.TestCase):
    def test_profile_resolves_against_repository_skills(self):
        root = Path(__file__).resolve().parents[1]
        visible = _codex_profile_visible(root)
        self.assertIn("brainstorming", visible)
        self.assertIn("using-coacus", visible)
