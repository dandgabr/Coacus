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

    def test_claims_sharing_a_long_prefix_stay_separate_candidates(self) -> None:
        prefix = "x" * (consolidate.MAX_GAP_CLAIM + 50)
        candidates = consolidate.consolidate([gap("s1", prefix + " one"), gap("s2", prefix + " two")])
        self.assertEqual(len(candidates), 2)

    def test_a_gap_that_is_only_invisible_characters_is_dropped(self) -> None:
        self.assertEqual(consolidate.consolidate([gap("s1", chr(0x200B) * 5)]), [])


class TestTaintAndSupport(unittest.TestCase):
    def test_skill_gap_needs_trusted_evidence(self) -> None:
        self.assertIn("skill-gap", taint.TRUST_REQUIRED)
        candidate = consolidate.consolidate([gap("s1", channel="model-assistant")])[0]
        self.assertFalse(candidate["trusted"])

    def test_the_shared_list_covers_every_type_that_needs_trust(self) -> None:
        self.assertEqual(set(taint.TRUST_REQUIRED), {"gotcha", "procedure", "skill-gap"})
        self.assertEqual(taint.MIN_SUPPORT["skill-gap"], 3)

    def test_trusted_sessions_counts_distinct_sessions_of_trusted_units_only(self) -> None:
        candidate = {"evidence": [
            {"channel": "human-user-turn", "session_id": "a"}, {"channel": "repo-file", "session_id": "a"},
            {"channel": "human-user-turn", "session_id": "b"}, {"channel": "tool-result", "session_id": "c"}]}
        self.assertEqual(taint.trusted_sessions(candidate), 2)


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

    def test_one_claim_repeated_with_other_casing_in_one_session_counts_once(self) -> None:
        texts = ["no skill for ledger migrations", "No SKILL for ledger migrations", " no skill for ledger migrations "]
        self.assertEqual(self._types(self._run([gap("s1", t) for t in texts])), [])

    def test_several_trusted_channels_inside_one_session_count_once(self) -> None:
        records = [gap("s1", channel=c) for c in ("human-user-turn", "repo-file")]
        records += [gap("s2", channel="human-user-turn")]
        self.assertEqual(self._types(self._run(records)), [])

    def test_untrusted_units_do_not_add_sessions(self) -> None:
        records = [gap("s1"), gap("s2"), gap("s3", channel="tool-result"), gap("s4", channel="model-assistant")]
        self.assertEqual(self._types(self._run(records)), [])

    def test_the_improve_branch_also_needs_enough_trusted_sessions(self) -> None:
        # A close catalog target would route a single-session claim to "improve".
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / "repo"
        (root / "catalog").mkdir(parents=True)
        (root / "catalog/catalog.json").write_text(json.dumps(
            {"skills": [{"name": "ledger-migrations", "path": "x"}], "agents": []}), encoding="utf-8")
        for sessions, expected in ((["s1"], []), (["s1", "s2", "s3"], ["skill-gap"])):
            with self.subTest(sessions=sessions):
                path = write(tmp.name, [gap(s, "ledger migrations rollback tooling") for s in sessions])
                result = loop.run(root, {"source": "transcript", "transcript": str(path)})
                self.assertEqual([p["type"] for p in result.get("proposals", [])], expected)

    def test_known_limit_invented_session_ids_still_count(self) -> None:
        # Recorded in ADR 0013: the session id is read from the record, so a writer of
        # the record can invent three. The human review of the proposal is the control.
        self.assertEqual(self._types(self._run([gap(s) for s in ("a", "b", "c")])), ["skill-gap"])


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
