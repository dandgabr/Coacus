"""Check that links added under ADR 0009 resolve to a file and, where given, a heading.

No validator in the repository checks markdown links or anchors, so this test does it
for the files touched by the change. Adapted from patterns recorded in ADR 0009 (see
THIRD-PARTY-NOTICES.md, revision 6337341602be6aa5860b1e83138f03bdd0b78f71, reviewed
2026-11-17).
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

SOURCES = [
    "docs/standards/untrusted-content.md",
    "knowledge/skills/security/operations/untrusted-content-security/SKILL.md",
    "knowledge/skills/security/operations/untrusted-content-security/references/untrusted-data-frame.md",
    "knowledge/skills/engineering/practices/guardrail-authoring/SKILL.md",
    "knowledge/skills/engineering/practices/guardrail-authoring/references/closed-question-judge.md",
    "knowledge/skills/engineering/practices/review-findings-pipeline/SKILL.md",
    "knowledge/skills/domains/industry/ai-model-evaluation/SKILL.md",
    "knowledge/skills/security/ai/ai-agentic-security/SKILL.md",
    "methodology/workflows/diagnosing-bugs/SKILL.md",
    "methodology/workflows/subagent-driven-development/SKILL.md",
    "methodology/workflows/using-coacus/references/research-trust-boundary.md",
]

LINK = re.compile(r"\]\(([^)\s]+)\)")


def _slug(heading):
    """Return the GitHub-style anchor of a heading line's text."""
    text = heading.strip().lower().replace("`", "")
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def _anchors(path):
    """Return the set of heading anchors of a markdown file, ignoring code fences."""
    found = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            match = re.match(r"#{1,6}\s+(.*)", line)
            if match:
                found.add(_slug(match.group(1)))
    return found


class LinkResolution(unittest.TestCase):
    def test_relative_links_and_anchors_resolve(self):
        checked = 0
        for relative in SOURCES:
            source = ROOT / relative
            text = source.read_text(encoding="utf-8")
            for target in LINK.findall(text):
                if re.match(r"[a-z]+:", target) or target.startswith("#"):
                    continue
                path_part, _, anchor = target.partition("#")
                resolved = (source.parent / path_part).resolve()
                with self.subTest(source=relative, target=target):
                    self.assertTrue(resolved.exists(), f"missing file for {target}")
                    if anchor and resolved.suffix == ".md":
                        self.assertIn(anchor, _anchors(resolved))
                    checked += 1
        self.assertGreater(checked, 10)

    def test_anchors_added_by_this_change_exist(self):
        wanted = {
            "docs/standards/evidence.md": "the-evidence-envelope",
            "knowledge/skills/engineering/practices/guardrail-authoring/SKILL.md":
                "conservative-tool--missing-cli-fallback-policy",
        }
        for relative, anchor in wanted.items():
            with self.subTest(file=relative):
                self.assertIn(anchor, _anchors(ROOT / relative))


if __name__ == "__main__":
    unittest.main()
