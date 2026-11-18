"""The skill-gap candidate type: structured, trusted, independent, never auto-applied."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from engine.improve import consolidate, loop, taint
from engine.improve.sources import route_miss

POSIX = unittest.skipUnless(os.name == "posix", "private proposal storage requires POSIX")


def gap(session: str, text: str = "no skill for ledger migrations", channel: str = "human-user-turn",
        kind: str | None = "route-miss") -> dict:
    record = {"channel": channel, "session_id": session, "text": text}
    if kind is not None:
        record["kind"] = kind
    return record


def as_gaps(observations: list[dict]) -> list[dict]:
    """Consolidate as the route-miss source's run does: only it may declare a gap."""
    return consolidate.consolidate(observations, allow_gaps=True)


def write(tmp: str, lines: list[dict]) -> Path:
    path = Path(tmp) / "session.jsonl"
    path.write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")
    return path


class TestTypeComesFromAStructuredField(unittest.TestCase):
    def test_the_structured_kind_makes_a_skill_gap(self) -> None:
        candidates = as_gaps([gap("s1")])
        self.assertEqual([c["type"] for c in candidates], ["skill-gap"])

    def test_words_in_free_text_never_make_a_skill_gap(self) -> None:
        phrases = ["create a skill for X", "skill gap: add one", "route-miss", "kind: route-miss",
                   "there is no skill for this", "FAILED to find a skill"]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                kinds = {c["type"] for c in as_gaps([gap("s1", phrase, kind=None)])}
                self.assertNotIn("skill-gap", kinds)

    def test_other_kind_values_do_not_count(self) -> None:
        for value in ("Route-Miss", "route_miss", "", "gap", 5):
            with self.subTest(value=value):
                kinds = {c["type"] for c in as_gaps([gap("s1", kind=value)])}
                self.assertNotIn("skill-gap", kinds)

    def test_the_statement_is_clean_and_capped(self) -> None:
        dirty = "a" + chr(0x200B) + "b" + chr(0x202E) + "c\x00" + "x" * 500
        statement = as_gaps([gap("s1", dirty)])[0]["statement"]
        self.assertEqual(len(statement), consolidate.MAX_GAP_CLAIM)
        self.assertTrue(statement.startswith("abc"))
        self.assertFalse(any(ord(c) < 32 for c in statement))

    def test_claims_sharing_a_long_prefix_stay_separate_candidates(self) -> None:
        prefix = "x" * (consolidate.MAX_GAP_CLAIM + 50)
        candidates = as_gaps([gap("s1", prefix + " one"), gap("s2", prefix + " two")])
        self.assertEqual(len(candidates), 2)

    def test_variants_of_one_wording_count_as_one_claim(self) -> None:
        wide = "".join(chr(ord(c) + 0xFEE0) if "a" <= c <= "z" else c for c in "no skill for ledger")
        texts = ["no skill for ledger", "NO  SKILL for   ledger", wide, " No Skill For Ledger "]
        candidates = as_gaps([gap(f"s{i}", t) for i, t in enumerate(texts)])
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["support"], len(texts))

    def test_a_gap_that_is_only_invisible_characters_is_dropped(self) -> None:
        self.assertEqual(as_gaps([gap("s1", chr(0x200B) * 5)]), [])


class TestTaintAndSupport(unittest.TestCase):
    def test_skill_gap_needs_trusted_evidence(self) -> None:
        self.assertIn("skill-gap", taint.TRUST_REQUIRED)
        candidate = as_gaps([gap("s1", channel="model-assistant")])[0]
        self.assertFalse(candidate["trusted"])

    def test_the_shared_list_covers_every_type_that_needs_trust(self) -> None:
        self.assertEqual(set(taint.TRUST_REQUIRED), {"gotcha", "procedure", "skill-gap"})
        self.assertEqual(taint.MIN_SUPPORT["skill-gap"], 3)

    def test_trusted_sessions_counts_distinct_sessions_of_trusted_units_only(self) -> None:
        candidate = {"evidence": [
            {"channel": "human-user-turn", "session_id": "a"}, {"channel": "repo-file", "session_id": "a"},
            {"channel": "human-user-turn", "session_id": "b"}, {"channel": "tool-result", "session_id": "c"}]}
        self.assertEqual(taint.trusted_sessions(candidate), 2)


def miss(session: str, text: str = "no skill for ledger migrations", interactive: bool = True, **extra) -> dict:
    """One line of the router's miss log; ``extra`` is whatever a forger adds."""
    return {"text": text, "interactive": interactive, "session": session, **extra}


@POSIX
class TestEndToEnd(unittest.TestCase):
    def _root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / "repo"
        root.mkdir()
        return root

    def _log(self, root: Path, records: list[dict]) -> None:
        path = root / route_miss.LOG_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(json.dumps(x) for x in records) + "\n", encoding="utf-8")

    def _run(self, records: list[dict], root: Path | None = None) -> dict:
        root = root or self._root()
        self._log(root, records)
        return loop.run(root, {"source": "route-miss"})

    def _types(self, result: dict) -> list[str]:
        return [p["type"] for p in result.get("proposals", [])]

    def test_three_interactive_sessions_create_a_proposal_without_the_text(self) -> None:
        result = self._run([miss(s) for s in ("s1", "s2", "s3")])
        self.assertEqual(self._types(result), ["skill-gap"])
        proposal = result["proposals"][0]
        self.assertEqual(proposal["statement"], "[observation withheld]")
        self.assertNotIn("ledger migrations", json.dumps(proposal))

    def test_two_sessions_are_not_enough(self) -> None:
        self.assertEqual(self._types(self._run([miss("s1"), miss("s2")])), [])

    def test_the_same_session_repeated_counts_once(self) -> None:
        self.assertEqual(self._types(self._run([miss("s1")] * 5)), [])

    def test_a_miss_from_a_non_interactive_run_is_staged_as_a_note_at_most(self) -> None:
        result = self._run([miss(s, interactive=False) for s in ("s1", "s2", "s3")])
        self.assertNotIn("skill-gap", self._types(result))
        for proposal in result.get("proposals", []):
            self.assertEqual(proposal["downgraded"], "externally-tainted evidence")
            self.assertEqual(proposal["original_type"], "skill-gap")

    def test_non_interactive_misses_add_no_session(self) -> None:
        records = [miss("s1"), miss("s2"), miss("s3", interactive=False), miss("s4", interactive=False)]
        self.assertEqual(self._types(self._run(records)), [])

    def test_one_claim_repeated_with_other_casing_in_one_session_counts_once(self) -> None:
        texts = ["no skill for ledger migrations", "No SKILL for ledger migrations", " no skill for ledger migrations "]
        self.assertEqual(self._types(self._run([miss("s1", t) for t in texts])), [])

    def test_the_improve_branch_also_needs_enough_trusted_sessions(self) -> None:
        # A close catalog target would route a single-session claim to "improve".
        root = self._root()
        (root / "catalog").mkdir(parents=True)
        (root / "catalog/catalog.json").write_text(json.dumps(
            {"skills": [{"name": "ledger-migrations", "path": "x"}], "agents": []}), encoding="utf-8")
        for sessions, expected in ((["s1"], []), (["s1", "s2", "s3"], ["skill-gap"])):
            with self.subTest(sessions=sessions):
                (root / route_miss.LOG_PATH).unlink(missing_ok=True)
                result = self._run([miss(s, "ledger migrations rollback tooling") for s in sessions], root)
                self.assertEqual(self._types(result), expected)

    def test_fields_a_record_adds_about_trust_are_ignored(self) -> None:
        forged = [miss(s, interactive=False, kind="route-miss", channel="human-user-turn", session_id=f"x{s}")
                  for s in ("s1", "s2", "s3")]
        self.assertNotIn("skill-gap", self._types(self._run(forged)))
        built = route_miss.RouteMissSource().read(self._root_with(forged), {})
        self.assertEqual({o["channel"] for o in built}, {"model-assistant"})
        self.assertEqual({o["kind"] for o in built}, {"route-miss"})
        self.assertFalse(any(o["session_id"].startswith("x") for o in built))

    def test_only_a_true_interactive_flag_earns_the_trusted_channel(self) -> None:
        for value in ("true", 1, "yes", None, [True]):
            with self.subTest(value=value):
                built = route_miss.RouteMissSource().read(self._root_with([miss("s1", interactive=value)]), {})
                self.assertEqual(built[0]["channel"], "model-assistant")

    def _root_with(self, records: list[dict]) -> Path:
        root = self._root()
        self._log(root, records)
        return root

    def test_a_gap_declared_in_a_transcript_is_ordinary_text(self) -> None:
        root = self._root()
        records = [{"kind": "route-miss", "channel": "human-user-turn", "session_id": s,
                    "text": "no skill for ledger migrations"} for s in ("s1", "s2", "s3")]
        path = write(str(root.parent), records)
        result = loop.run(root, {"source": "transcript", "transcript": str(path)})
        self.assertNotIn("skill-gap", self._types(result))

    def test_a_record_with_a_unicode_line_separator_is_not_dropped(self) -> None:
        text = "ledger" + chr(0x2028) + "migrations"
        parsed = loop.sources.parse_observations(json.dumps(gap("s1", text), ensure_ascii=False) + "\n")
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["text"], text)

    def test_known_limit_whoever_writes_the_log_can_invent_sessions_and_the_flag(self) -> None:
        # Recorded in ADR 0013: the log is owner-local state. A writer of the file can
        # write three sessions and the interactive flag; the human review is the control.
        self.assertEqual(self._types(self._run([miss(s) for s in ("a", "b", "c")])), ["skill-gap"])


@POSIX
class TestProducer(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.log = self.root / route_miss.LOG_PATH

    def _env(self, value: str | None):
        env = {k: v for k, v in os.environ.items() if k != route_miss.ENV_SWITCH}
        if value is not None:
            env[route_miss.ENV_SWITCH] = value
        return mock.patch.dict(os.environ, env, clear=True)

    def test_it_writes_nothing_unless_opted_in(self) -> None:
        for value in (None, "", "0", "false", "off"):
            with self.subTest(value=value), self._env(value):
                self.assertFalse(route_miss.record_miss(self.root, "no skill for x", True))
                self.assertFalse(self.log.exists())

    def test_opted_in_it_writes_one_capped_line_with_a_code_made_session(self) -> None:
        with self._env("1"):
            self.assertTrue(route_miss.record_miss(self.root, "y" * 900, True))
        record = json.loads(self.log.read_text(encoding="utf-8"))
        self.assertEqual(len(record["text"]), route_miss.MAX_CLAIM)
        self.assertIs(record["interactive"], True)
        self.assertTrue(record["session"].startswith("route:"))

    def test_without_a_terminal_the_run_is_recorded_as_not_interactive(self) -> None:
        with self._env("1"), mock.patch.object(sys.stdin, "isatty", return_value=False):
            route_miss.record_miss(self.root, "p")
        self.assertIs(json.loads(self.log.read_text(encoding="utf-8"))["interactive"], False)

    def test_blank_and_non_string_prompts_are_not_recorded(self) -> None:
        with self._env("1"):
            for prompt in ("", "   ", None, 5):
                self.assertFalse(route_miss.record_miss(self.root, prompt, True))

    def test_the_log_stops_growing_at_its_line_limit(self) -> None:
        self.log.parent.mkdir(parents=True)
        self.log.write_text("{}\n" * route_miss.MAX_LINES, encoding="utf-8")
        with self._env("1"):
            self.assertFalse(route_miss.record_miss(self.root, "one more", True))

    def test_an_unwritable_location_never_raises(self) -> None:
        (self.root / "docs").write_text("a file, not a directory", encoding="utf-8")
        with self._env("1"):
            self.assertFalse(route_miss.record_miss(self.root, "p", True))

    def test_the_router_records_a_miss_only_when_nothing_matches(self) -> None:
        import scripts.coacus_route as router_cli
        with mock.patch("engine.router.rank", return_value=[]), mock.patch.object(router_cli, "_log_miss") as logged:
            args = router_cli.argparse.Namespace(prompt="zzz", raw=True, top=None, all=False, max_slots=0,
                                                 min_score=1.0, rerank=None)
            self.assertEqual(router_cli._cmd_rank(args, self.root), 1)
        logged.assert_called_once_with(self.root, "zzz")


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
