"""Tests for the deterministic agent router (routing)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine import router

from tests.support import make_repo


def _repo_with_index(tmp: Path) -> Path:
    """A tiny repo whose routing index has two distinguishable agents."""
    root = make_repo(tmp)
    entries = [
        {
            "name": "sample-agent",
            "category": "roles",
            "description": "Samples things.",
            "skills": [],
            "triggers": ["sample", "amostra", "exemplo"],
        },
        {
            "name": "database-agent",
            "category": "data",
            "description": "Handles databases.",
            "skills": [],
            "triggers": ["banco", "database", "sql"],
        },
    ]
    (root / ".agents").mkdir(exist_ok=True)
    (root / ".agents/routing.json").write_text(
        json.dumps({"schema": 1, "entries": entries}), encoding="utf-8"
    )
    return root


class TestRouterRank(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = _repo_with_index(Path(self._tmp.name))

    def test_trigger_match_wins(self) -> None:
        ranked = router.rank(self.root, "preciso de um exemplo")
        self.assertTrue(ranked)
        self.assertEqual(ranked[0].name, "sample-agent")
        self.assertIn("exemplo", ranked[0].matched)

    def test_prompt_with_only_stopwords_returns_nothing(self) -> None:
        self.assertEqual(router.rank(self.root, "the a of to de da"), [])

    def test_below_threshold_is_dropped(self) -> None:
        self.assertEqual(router.rank(self.root, "banco", min_score=99.0), [])

    def test_limit_truncates(self) -> None:
        ranked = router.rank(self.root, "sample database", limit=1)
        self.assertEqual(len(ranked), 1)

    def test_ranking_is_deterministic(self) -> None:
        first = router.rank(self.root, "banco de dados")
        second = router.rank(self.root, "banco de dados")
        self.assertEqual([c.name for c in first], [c.name for c in second])


class TestRouterResolve(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = _repo_with_index(Path(self._tmp.name))

    def test_exact_name_resolves(self) -> None:
        matched, errors = router.resolve(self.root, ["sample-agent"])
        self.assertEqual(errors, [])
        self.assertEqual(matched[0]["name"], "sample-agent")

    def test_alias_resolves(self) -> None:
        matched, errors = router.resolve(self.root, ["banco"])
        self.assertEqual(errors, [])
        self.assertEqual(matched[0]["name"], "database-agent")

    def test_unknown_name_suggests(self) -> None:
        matched, errors = router.resolve(self.root, ["sample-agentt"])
        self.assertEqual(matched, [])
        self.assertTrue(errors)
        self.assertIn("did you mean", errors[0])


class TestRouterRerank(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = _repo_with_index(Path(self._tmp.name))

    def test_reranker_reorders(self) -> None:
        candidates = router.rank(self.root, "sample database")
        self.assertGreaterEqual(len(candidates), 2)
        # A command that prints the reverse order.
        reordered = router.rerank(
            candidates,
            "sample database",
            "python3 -c \"import json,sys; d=json.load(sys.stdin); "
            "[print(c['name']) for c in reversed(d['candidates'])]\"",
        )
        self.assertEqual(reordered[0].name, candidates[-1].name)

    def test_missing_reranker_fails_open(self) -> None:
        candidates = router.rank(self.root, "sample database")
        same = router.rerank(candidates, "sample database", "definitely-not-a-command-xyz")
        self.assertEqual([c.name for c in same], [c.name for c in candidates])


if __name__ == "__main__":
    unittest.main()
