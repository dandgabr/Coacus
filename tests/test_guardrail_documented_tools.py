"""Every tool a harness documents for an action maps to that action's verb.

The tool-mapping references list, per harness, which native tool performs each
action. The guard classifies a call by tool name, so a documented name with no verb
is a hole: a ``read`` rule would not see it. The tables are read from the references,
so a name added there without a verb here fails this test.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts import coacus_guard as guard

REFERENCES = Path(__file__).resolve().parents[1] / "methodology/workflows/using-coacus/references"
VERBS = {
    "read a file": "read",
    "search files": "read",
    "create, edit, or delete files": "write",
    "run shell commands": "exec",
    "fetch a url": "network",
    "dispatch a subagent": "spawn",
}
ROW = re.compile(r"^\|\s*(?P<action>[^|]+?)\s*\|\s*(?P<tools>[^|]+?)\s*\|\s*$")


def documented(harness: str) -> list[tuple[str, str]]:
    """``(tool, verb)`` pairs the harness reference documents for the checked actions."""
    pairs = []
    for line in (REFERENCES / f"{harness}-tools.md").read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        verb = VERBS.get(match.group("action").lower()) if match else None
        if verb:
            pairs += [(name, verb) for name in re.findall(r"`([^`]+)`", match.group("tools"))]
    return pairs


class TestDocumentedToolNames(unittest.TestCase):
    def test_every_documented_tool_has_its_verb(self) -> None:
        for harness in ("antigravity", "claude-code", "codex", "opencode"):
            pairs = documented(harness)
            self.assertTrue(pairs, f"no checked rows found in the {harness} reference")
            for tool, verb in pairs:
                with self.subTest(harness=harness, tool=tool):
                    found = guard._actions({"tool": tool, "tool_input": {"path": "/p", "url": "u"}}, harness)
                    self.assertEqual(found[0][0], verb)

    def test_search_tools_are_read_actions_for_a_read_rule(self) -> None:
        for tool in ("grep_search", "find_by_name", "Grep", "Glob"):
            with self.subTest(tool=tool):
                found = guard._actions({"tool": tool, "tool_input": {"path": "/home/u/.env"}})
                self.assertEqual(found, [("read", "/home/u/.env")])


if __name__ == "__main__":
    unittest.main()
