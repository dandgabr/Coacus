"""Calibration regression tests for the router against the real corpus.

These lock the routing quality observed during calibration: a PT-BR prompt with
accents, a paraphrased request, and a phrase trigger that must not match on a
single token. They read the committed ``.agents/routing.json``, so a lexicon edit
that regresses matching fails here.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from engine import router

ROOT = Path(__file__).resolve().parents[1]


def _top(prompt: str, n: int = 3) -> list[str]:
    return [c.name for c in router.rank(ROOT, prompt, limit=n)]


class TestRouterCalibration(unittest.TestCase):
    def test_accented_prompt_matches(self) -> None:
        # "latência" must fold to "latencia" and match; "postgres" picks the DBA.
        names = _top("preciso reduzir a latência das consultas no postgres")
        self.assertIn("code-optimizer", names)
        self.assertIn("dba-specialist", names)

    def test_mobile_pentest_routes_to_mobile_first(self) -> None:
        names = _top("faça um pentest no app android do banco")
        self.assertEqual(names[0], "mobile-security-specialist")

    def test_pqc_prompt_routes_to_cryptography(self) -> None:
        names = _top("implementar criptografia pós-quântica")
        self.assertEqual(names[0], "cryptography-specialist")

    def test_paraphrased_text_review_routes_to_linguistic(self) -> None:
        names = _top("revisar o texto do relatório em português")
        self.assertEqual(names[0], "linguistic-specialist")

    def test_pt_br_scroll_motion_routes_to_motion_specialist(self) -> None:
        # A curated PT-BR motion phrase must still match after accent folding.
        names = _top("animação ligada ao scroll com fallback")
        self.assertEqual(names[0], "ui-motion-specialist")

    def test_view_transition_routes_to_motion_specialist(self) -> None:
        names = _top("view transition with reduced motion fallback")
        self.assertEqual(names[0], "ui-motion-specialist")

    def test_sticky_sessions_do_not_route_to_motion_specialist(self) -> None:
        # Load-balancer "sticky sessions" must not hit a motion trigger; only the
        # phrases "sticky header" / "position sticky" belong to the motion lexicon.
        ranked = router.rank(ROOT, "sticky sessions load balancer", limit=5)
        self.assertTrue(ranked)
        self.assertNotEqual(ranked[0].name, "ui-motion-specialist")
        motion = [c for c in ranked if c.name == "ui-motion-specialist"]
        if motion:
            self.assertLess(motion[0].score, router.W_TRIGGER)

    def test_spring_boot_still_routes_to_java_architect(self) -> None:
        # The motion "spring physics" phrases must not steal Spring Boot prompts.
        ranked = router.rank(ROOT, "spring boot rest api", limit=3)
        names = [c.name for c in ranked]
        self.assertIn("java-enterprise-architect", names)
        self.assertNotIn("ui-motion-specialist", names)
        java = next(c for c in ranked if c.name == "java-enterprise-architect")
        self.assertEqual(java.score, ranked[0].score)

    def test_spring_physics_animation_routes_to_motion_specialist(self) -> None:
        names = _top("spring physics animation for a dialog")
        self.assertEqual(names[0], "ui-motion-specialist")

    def test_multi_word_phrase_does_not_match_on_one_token(self) -> None:
        # "sistema digital" is a computer-engineer phrase; a bare "sistema" prompt
        # must not score it on the phrase alone.
        ranked = router.rank(ROOT, "sistema", limit=5)
        computer = [c for c in ranked if c.name == "computer-engineer"]
        if computer:
            self.assertNotIn("sistema digital", computer[0].matched)

    def test_unknown_language_prompt_is_quiet(self) -> None:
        # A prompt with no domain terms should not force a candidate.
        self.assertEqual(router.rank(ROOT, "ok", min_score=5.0), [])


if __name__ == "__main__":
    unittest.main()
