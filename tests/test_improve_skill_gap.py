"""The skill-gap candidate type: structured, trusted, independent, never auto-applied."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from engine.improve import consolidate, loop, taint

POSIX = unittest.skipUnless(os.name == "posix", "private proposal storage requires POSIX")


def gap(session: str, text: str = "no skill for ledger migrations", channel: str = "human-user-turn",
        kind: str | None = "route-miss") -> dict:
    record = {"channel": channel, "session_id": session, "text": text}
    if kind is not None:
        record["kind"] = kind
    return record


def write(tmp: str, lines: list[dict]) -> Path:
    path = Path(tmp) / "session.jsonl"
    path.write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")
    return path


class TestTypeComesFromAStructuredField(unittest.TestCase):
    def test_the_structured_kind_makes_a_skill_gap(self) -> None:
        candidates = consolidate.consolidate([gap("s1")])
        self.assertEqual([c["type"] for c in candidates], ["skill-gap"])

    def test_words_in_free_text_never_make_a_skill_gap(self) -> None:
        phrases = ["create a skill for X", "skill gap: add one", "route-miss", "kind: route-miss",
                   "there is no skill for this", "FAILED to find a skill"]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                kinds = {c["type"] for c in consolidate.consolidate([gap("s1", phrase, kind=None)])}
                self.assertNotIn("skill-gap", kinds)

    def test_other_kind_values_do_not_count(self) -> None:
        for value in ("Route-Miss", "route_miss", "", "gap", 5):
            with self.subTest(value=value):
                kinds = {c["type"] for c in consolidate.consolidate([gap("s1", kind=value)])}
                self.assertNotIn("skill-gap", kinds)

    def test_the_statement_is_clean_and_capped(self) -> None:
        dirty = "a" + chr(0x200B) + "b" + chr(0x202E) + "c\x00" + "x" * 500
        statement = consolidate.consolidate([gap("s1", dirty)])[0]["statement"]
        self.assertEqual(len(statement), consolidate.MAX_GAP_CLAIM)
        self.assertTrue(statement.startswith("abc"))
        self.assertFalse(any(ord(c) < 32 for c in statement))

    def test_a_gap_that_is_only_invisible_characters_is_dropped(self) -> None:
        self.assertEqual(consolidate.consolidate([gap("s1", chr(0x200B) * 5)]), [])


class TestTaintAndSupport(unittest.TestCase):
    def test_skill_gap_needs_trusted_evidence(self) -> None:
        self.assertIn("skill-gap", taint.TRUST_REQUIRED)
        candidate = consolidate.consolidate([gap("s1", channel="model-assistant")])[0]
        self.assertFalse(candidate["trusted"])

    def test_the_loop_uses_the_shared_list(self) -> None:
        source = Path(loop.__file__).read_text(encoding="utf-8")
        self.assertIn("taint.TRUST_REQUIRED", source)
        self.assertNotIn('("gotcha", "procedure")', source)

    def test_a_claimed_trusted_channel_inside_a_model_record_is_still_only_a_claim(self) -> None:
        # Known limit recorded in ADR 0013: the channel is read from the record, so
        # support needs three independent sessions and a person's review.
        self.assertEqual(taint.MIN_SUPPORT["skill-gap"], 3)
        self.assertEqual(taint.DEFAULT_MIN_SUPPORT, 2)


@POSIX
class TestEndToEnd(unittest.TestCase):
    def _run(self, observations: list[dict]) -> dict:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / "repo"
        root.mkdir()
        return loop.run(root, {"source": "transcript", "transcript": str(write(tmp.name, observations))})

    def _types(self, result: dict) -> list[str]:
        return [p["type"] for p in result.get("proposals", [])]

    def test_three_trusted_sessions_create_a_proposal_without_the_text(self) -> None:
        result = self._run([gap(s) for s in ("s1", "s2", "s3")])
        self.assertEqual(self._types(result), ["skill-gap"])
        proposal = result["proposals"][0]
        self.assertEqual(proposal["statement"], "[observation withheld]")
        self.assertNotIn("ledger migrations", json.dumps(proposal))

    def test_two_sessions_are_not_enough(self) -> None:
        self.assertEqual(self._types(self._run([gap("s1"), gap("s2")])), [])

    def test_the_same_session_repeated_counts_once(self) -> None:
        self.assertEqual(self._types(self._run([gap("s1")] * 5)), [])

    def test_a_model_written_gap_is_staged_as_a_note_at_most(self) -> None:
        result = self._run([gap(s, channel="model-assistant") for s in ("s1", "s2", "s3")])
        self.assertNotIn("skill-gap", self._types(result))

    def test_repeating_one_claim_in_other_words_still_needs_three_sessions(self) -> None:
        texts = ["no skill for ledger migrations", "No SKILL for ledger migrations", " no skill for ledger migrations "]
        result = self._run([gap("s1", t) for t in texts])
        self.assertEqual(self._types(result), [])

    def test_the_loop_never_applies_anything(self) -> None:
        result = self._run([gap(s) for s in ("s1", "s2", "s3")])
        self.assertNotIn("applied", json.dumps(result).lower())


class TestBoundaries(unittest.TestCase):
    def test_generate_and_check_do_not_import_the_improve_subsystem(self) -> None:
        import subprocess
        code = ("import sys, runpy;"
                "sys.argv=['coacus.py','check'];"
                "\ntry:\n runpy.run_path('scripts/coacus.py', run_name='__main__')\n"
                "except SystemExit: pass\n"
                "print('engine.improve' in sys.modules)")
        proc = subprocess.run([sys.executable, "-c", code], cwd=Path(__file__).resolve().parents[1],
                              capture_output=True, text=True, timeout=300)
        self.assertEqual(proc.stdout.strip().splitlines()[-1], "False", proc.stderr[-300:])


if __name__ == "__main__":
    unittest.main()
