"""Regression checks for the Bandit workflow's interpreter selection."""

import unittest
from pathlib import Path


class BanditWorkflowTest(unittest.TestCase):
    def test_install_and_scan_use_same_interpreter(self):
        workflow = (Path(__file__).resolve().parents[1] / '.github/workflows/bandit.yml').read_text()
        self.assertIn('python3 -m pip install --break-system-packages bandit bandit-sarif-formatter', workflow)
        self.assertIn('python3 -m bandit -f sarif', workflow)
        self.assertNotIn('import bandit_sarif_formatter', workflow)


if __name__ == '__main__':
    unittest.main()
