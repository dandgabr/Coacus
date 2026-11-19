"""The improvement loop rejects a proposal that names or routes to a protected surface."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from engine.improve import loop, protected, route, sources, verify

REPO = Path(__file__).resolve().parents[1]


class Fixture:
    name = "fixture"

    def __init__(self, text: str) -> None:
        self.text = text

    def status(self, root):
        return "present"

    def read(self, root, options):
        return [{"channel": "human-user-turn", "session_id": s, "text": self.text} for s in ("s1", "s2")]


class TestMatching(unittest.TestCase):
    def test_every_listed_surface_matches_itself(self) -> None:
        for pattern in protected.PROTECTED:
            sample = pattern.replace("*", "claude-code") + ("x.py" if pattern.endswith("/") else "")
            with self.subTest(pattern=pattern):
                self.assertEqual(protected.is_protected(sample), pattern)
                self.assertEqual(protected.mentions(f"please change {sample} soon"), pattern)

    def test_near_misses_are_not_protected(self) -> None:
        for path in ("engine/improved/x.py", "engine/guardrails/x.py", "docs/standards/evidence.md.bak",
                     "my-AGENTS.md", "scripts/coacus_eval.pyc", "evals/scenarios-old/a.json"):
            with self.subTest(path=path):
                self.assertIsNone(protected.is_protected(path))
        self.assertIsNone(protected.mentions("the engine improves; read evidence.md only as a word"))

    def test_folding_and_traversal(self) -> None:
        for text in ("ENGINE\\IMPROVE\\verify.py", "./AGENTS.md", "docs/x/../../AGENTS.md",
                     "ｅngine/guardrail/evaluate.py", "engine/gu​ardrail/evaluate.py",
                     "/engine/verify/ledger.py"):
            with self.subTest(text=text):
                self.assertIsNotNone(protected.mentions(text))

    def test_bad_input_never_raises(self) -> None:
        for value in (None, 5, "", "   ", b"x", ["AGENTS.md"]):
            self.assertIsNone(protected.is_protected(value))
            self.assertIsNone(protected.mentions(value))


class TestDocumentStaysInSync(unittest.TestCase):
    def test_the_standard_lists_exactly_the_engine_constant(self) -> None:
        text = (REPO / "docs/standards/self-improvement-loop.md").read_text(encoding="utf-8")
        section = text[text.index("The loop never edits its protected surfaces"):]
        section = section[:section.index("The list is")]
        listed = set(re.findall(r"`([^`]+)`", section))
        self.assertEqual(listed, set(protected.PROTECTED))


class TestLadder(unittest.TestCase):
    def _verify(self, statement: str) -> dict:
        candidate = {"statement": statement, "support": 2, "trusted": True, "evidence": []}
        return verify.verify(REPO, candidate, route.route(REPO, candidate))

    def test_a_statement_naming_a_protected_file_fails_rung_0a(self) -> None:
        result = self._verify("a wholly novel xyzzy quux insight: relax engine/guardrail/evaluate.py")
        self.assertFalse(result["passed"])
        self.assertFalse(result["protected"]["ok"])
        self.assertIn("engine/guardrail/", result["protected"]["reason"])

    def test_an_ordinary_statement_still_passes(self) -> None:
        self.assertTrue(self._verify("a wholly novel xyzzy quux insight")["passed"])

    def test_a_catalog_target_on_a_protected_path_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog").mkdir()
            (root / "catalog" / "catalog.json").write_text(
                '{"skills": [{"name": "guard-rules", "path": "docs/standards/lifecycle-guardrails.md"}], "agents": []}',
                encoding="utf-8")
            ok, reason = verify.protected_ok(root, {"statement": "plain words"}, {"target": "guard-rules"})
            self.assertFalse(ok)
            self.assertIn("routes to", reason)
            self.assertTrue(verify.protected_ok(root, {"statement": "plain words"}, {"target": None})[0])


class TestLoop(unittest.TestCase):
    def _run(self, text: str) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            registry = sources.SourceRegistry()
            registry.register(Fixture(text))
            return loop.run(root, {"source": "fixture"}, registry=registry)

    def test_a_poisoned_observation_is_not_staged(self) -> None:
        self.assertEqual(self._run("novel xyzzy quux: weaken harnesses/codex/bootstrap/guardrail-hooks.json")["proposals"], [])

    def test_the_same_observation_without_the_path_is_staged(self) -> None:
        self.assertEqual(len(self._run("novel xyzzy quux insight")["proposals"]), 1)


if __name__ == "__main__":
    unittest.main()
