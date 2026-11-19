"""The skill-gap candidate type: structured, trusted, independent, never auto-applied."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
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


class StateDirCase(unittest.TestCase):
    """Runs each test with the miss log in a private temporary state directory."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.state = Path(self._tmp.name) / "state"
        self.repo = Path(self._tmp.name) / "repo"
        self.repo.mkdir()
        env = {k: v for k, v in os.environ.items() if k not in (route_miss.ENV_SWITCH, "XDG_STATE_HOME")}
        env["COACUS_STATE_DIR"] = str(self.state)
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.log = route_miss.log_path()

    def write_log(self, records: list[dict], text: str | None = None) -> None:
        self.log.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.log.parent, 0o700)
        body = text if text is not None else "\n".join(json.dumps(x) for x in records) + "\n"
        self.log.write_text(body, encoding="utf-8")
        os.chmod(self.log, 0o600)

    def opt_in(self):
        return mock.patch.dict(os.environ, {route_miss.ENV_SWITCH: "1"})


@POSIX
class TestEndToEnd(StateDirCase):
    def _run(self, records: list[dict]) -> dict:
        self.write_log(records)
        return loop.run(self.repo, {"source": "route-miss"})

    def _types(self, result: dict) -> list[str]:
        return [p["type"] for p in result.get("proposals", [])]

    def test_three_interactive_sessions_create_a_proposal_without_the_text(self) -> None:
        result = self._run([miss(s) for s in ("d1", "d2", "d3")])
        self.assertEqual(self._types(result), ["skill-gap"])
        proposal = result["proposals"][0]
        self.assertEqual(proposal["statement"], "[observation withheld]")
        self.assertNotIn("ledger migrations", json.dumps(proposal))

    def test_two_sessions_are_not_enough(self) -> None:
        self.assertEqual(self._types(self._run([miss("d1"), miss("d2")])), [])

    def test_the_same_session_repeated_counts_once(self) -> None:
        self.assertEqual(self._types(self._run([miss("d1")] * 5)), [])

    def test_a_miss_from_a_non_interactive_run_never_becomes_a_gap(self) -> None:
        result = self._run([miss(s, interactive=False) for s in ("d1", "d2", "d3")])
        self.assertEqual(self._types(result), [])

    def test_non_interactive_misses_add_no_session(self) -> None:
        records = [miss("d1"), miss("d2"), miss("d3", interactive=False), miss("d4", interactive=False)]
        self.assertEqual(self._types(self._run(records)), [])

    def test_one_claim_repeated_with_other_casing_in_one_session_counts_once(self) -> None:
        texts = ["no skill for ledger migrations", "No SKILL for ledger migrations", " no skill for ledger migrations "]
        self.assertEqual(self._types(self._run([miss("d1", t) for t in texts])), [])

    def test_the_improve_branch_also_needs_enough_trusted_sessions(self) -> None:
        # A close catalog target would route a single-session claim to "improve".
        (self.repo / "catalog").mkdir(parents=True)
        (self.repo / "catalog/catalog.json").write_text(json.dumps(
            {"skills": [{"name": "ledger-migrations", "path": "x"}], "agents": []}), encoding="utf-8")
        for sessions, expected in ((["d1"], []), (["d1", "d2", "d3"], ["skill-gap"])):
            with self.subTest(sessions=sessions):
                result = self._run([miss(s, "ledger migrations rollback tooling") for s in sessions])
                self.assertEqual(self._types(result), expected)

    def test_fields_a_record_adds_about_trust_are_ignored(self) -> None:
        forged = [miss(s, interactive=False, kind="other", channel="human-user-turn", session_id=f"x{s}")
                  for s in ("d1", "d2", "d3")]
        self.write_log(forged)
        built = route_miss.RouteMissSource().read(self.repo, {})
        self.assertEqual({o["channel"] for o in built}, {"model-assistant"})
        self.assertEqual({o["kind"] for o in built}, {"route-miss"})
        self.assertFalse(any(o["session_id"].startswith("x") for o in built))
        self.assertNotIn("skill-gap", self._types(loop.run(self.repo, {"source": "route-miss"})))

    def test_only_a_true_interactive_flag_earns_the_trusted_channel(self) -> None:
        for value in ("true", 1, "yes", None, [True]):
            with self.subTest(value=value):
                self.write_log([miss("d1", interactive=value)])
                built = route_miss.RouteMissSource().read(self.repo, {})
                self.assertEqual(built[0]["channel"], "model-assistant")

    def test_the_session_text_is_cleaned_and_capped(self) -> None:
        self.write_log([miss("d 1/\x00\u202e;rm" + "x" * 200)])
        session = route_miss.RouteMissSource().read(self.repo, {})[0]["session_id"]
        self.assertLessEqual(len(session), 64)
        self.assertRegex(session, r"^[A-Za-z0-9._:-]+$")
        self.write_log([miss("")])
        self.assertEqual(route_miss.RouteMissSource().read(self.repo, {})[0]["session_id"], "route:unknown")

    def test_the_claim_is_capped_and_blank_or_non_string_text_is_skipped(self) -> None:
        self.write_log([miss("d1", "z" * 900), miss("d2", "   "), {"text": 5, "interactive": True}, miss("d3")])
        built = route_miss.RouteMissSource().read(self.repo, {})
        self.assertEqual([len(o["text"]) for o in built][0], route_miss.MAX_CLAIM)
        self.assertEqual(len(built), 2)

    def test_a_raw_line_separator_inside_a_record_does_not_split_it(self) -> None:
        text = "ledger" + chr(0x2028) + "migrations"
        self.write_log([], json.dumps(miss("d1", text), ensure_ascii=False) + "\n")
        built = route_miss.RouteMissSource().read(self.repo, {})
        self.assertEqual([o["text"] for o in built], [text])

    def test_the_reader_stops_at_its_line_cap_and_byte_cap(self) -> None:
        records = [miss(f"d{i}") for i in range(route_miss.MAX_LINES + 50)]
        self.write_log(records)
        built = route_miss.RouteMissSource().read(self.repo, {})
        self.assertEqual(len(built), route_miss.MAX_LINES)
        self.assertEqual(built[-1]["session_id"], f"d{route_miss.MAX_LINES + 49}")  # the newest are kept
        self.write_log([], json.dumps(miss("d1", "a")) + "\n" + "x" * (route_miss.MAX_BYTES + 10))
        self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])  # no whole line in the tail

    def test_a_symlinked_log_is_not_read(self) -> None:
        real = Path(self._tmp.name) / "elsewhere.jsonl"
        real.write_text(json.dumps(miss("d1")) + "\n", encoding="utf-8")
        os.chmod(real, 0o600)
        self.log.parent.mkdir(parents=True, mode=0o700)
        self.log.symlink_to(real)
        self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])

    def test_a_state_location_inside_the_scanned_repository_is_refused(self) -> None:
        inside = self.repo / "state"
        with mock.patch.dict(os.environ, {"COACUS_STATE_DIR": str(inside)}):
            hostile = route_miss.log_path()
            hostile.parent.mkdir(parents=True, mode=0o700)
            hostile.write_text("\n".join(json.dumps(miss(s)) for s in ("d1", "d2", "d3")) + "\n", encoding="utf-8")
            os.chmod(hostile, 0o600)
            self.assertIsNone(route_miss.log_path(self.repo))
            self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])
            self.assertEqual(self._types(loop.run(self.repo, {"source": "route-miss"})), [])

    def test_a_relative_state_location_is_refused(self) -> None:
        with mock.patch.dict(os.environ, {"COACUS_STATE_DIR": "relative/dir"}):
            self.assertIsNone(route_miss.log_path())
            self.assertEqual(route_miss.RouteMissSource().status(self.repo), "absent_by_config")

    def test_a_log_that_others_can_read_or_write_is_not_trusted(self) -> None:
        for mode in (0o644, 0o660, 0o606, 0o666):
            with self.subTest(mode=oct(mode)):
                self.write_log([miss("d1")])
                os.chmod(self.log, mode)
                self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])
        self.write_log([miss("d1")])
        os.chmod(self.log.parent, 0o755)  # nosec B103  # Test fixture that builds an open directory on purpose.
        self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])

    def test_a_log_owned_by_someone_else_is_not_trusted(self) -> None:
        self.write_log([miss("d1")])
        with mock.patch.object(route_miss.os, "geteuid", return_value=os.geteuid() + 1):
            self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])

    def test_a_fifo_in_place_of_the_log_neither_hangs_the_reader_nor_the_writer(self) -> None:
        self.log.parent.mkdir(parents=True, mode=0o700)
        os.mkfifo(self.log, 0o600)
        self.assertEqual(route_miss.RouteMissSource().read(self.repo, {}), [])
        with self.opt_in():
            self.assertFalse(route_miss.record_miss(self.repo, "p", True))

    def test_status_distinguishes_a_present_log_from_an_absent_one(self) -> None:
        source = route_miss.RouteMissSource()
        self.assertEqual(source.status(self.repo), "absent_by_config")
        self.write_log([miss("d1")])
        self.assertEqual(source.status(self.repo), "present")

    def test_the_cli_runs_the_source(self) -> None:
        self.write_log([miss(s) for s in ("d1", "d2", "d3")])
        env = {**os.environ, "COACUS_STATE_DIR": str(self.state)}
        proc = subprocess.run([sys.executable, "scripts/coacus_improve.py", "run", "--source", "route-miss",
                               "--root", str(self.repo)], cwd=Path(__file__).resolve().parents[1],
                              capture_output=True, text=True, env=env, timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr[-300:])
        self.assertEqual([p["type"] for p in json.loads(proc.stdout)["proposals"]], ["skill-gap"])
        status = subprocess.run([sys.executable, "scripts/coacus_improve.py", "status", "--root", str(self.repo)],
                                cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True,
                                env=env, timeout=120)
        self.assertEqual(json.loads(status.stdout)["route-miss"], "present")

    def test_a_gap_declared_in_a_transcript_is_ordinary_text(self) -> None:
        records = [{"kind": "route-miss", "channel": "human-user-turn", "session_id": s,
                    "text": "no skill for ledger migrations"} for s in ("s1", "s2", "s3")]
        path = write(self._tmp.name, records)
        result = loop.run(self.repo, {"source": "transcript", "transcript": str(path)})
        self.assertNotIn("skill-gap", self._types(result))

    def test_known_limit_whoever_writes_the_log_can_invent_sessions_and_the_flag(self) -> None:
        # Recorded in ADR 0013: the log is owner-local state. A writer of the file can
        # write three days and the interactive flag; the human review is the control.
        self.assertEqual(self._types(self._run([miss(s) for s in ("a", "b", "c")])), ["skill-gap"])


@POSIX
class TestProducer(StateDirCase):
    def test_it_writes_nothing_unless_opted_in(self) -> None:
        for value in (None, "", "0", "false", "no", "off"):
            env = {k: v for k, v in os.environ.items() if k != route_miss.ENV_SWITCH}
            if value is not None:
                env[route_miss.ENV_SWITCH] = value
            with self.subTest(value=value), mock.patch.dict(os.environ, env, clear=True):
                self.assertFalse(route_miss.record_miss(self.repo, "no skill for x", True))
                self.assertFalse(self.log.exists())

    def test_the_log_is_outside_the_repository_and_private(self) -> None:
        with self.opt_in():
            self.assertTrue(route_miss.record_miss(self.repo, "y" * 900, True))
        self.assertEqual(os.listdir(self.repo), [])
        self.assertEqual(self.log.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.log.parent.stat().st_mode & 0o777, 0o700)
        record = json.loads(self.log.read_text(encoding="utf-8"))
        self.assertEqual(len(record["text"]), route_miss.MAX_CLAIM)
        self.assertIs(record["interactive"], True)
        self.assertRegex(record["session"], r"^route:\d{4}-\d{2}-\d{2}$")

    def test_the_default_location_follows_the_state_home(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "COACUS_STATE_DIR"}
        env["XDG_STATE_HOME"] = str(self.state)
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(route_miss.log_path(), self.state / "coacus" / route_miss.LOG_NAME)

    def test_the_run_is_interactive_only_with_a_terminal_on_both_ends(self) -> None:
        for stdin, stdout, expected in ((True, True, True), (True, False, False), (False, True, False), (False, False, False)):
            with self.subTest(stdin=stdin, stdout=stdout), self.opt_in(), \
                    mock.patch.object(sys.stdin, "isatty", return_value=stdin), \
                    mock.patch.object(sys.stdout, "isatty", return_value=stdout):
                self.log.unlink(missing_ok=True)
                route_miss.record_miss(self.repo, "p")
                self.assertIs(json.loads(self.log.read_text(encoding="utf-8"))["interactive"], expected)

    def test_blank_and_non_string_prompts_are_not_recorded(self) -> None:
        with self.opt_in():
            for prompt in ("", "   ", None, 5):
                self.assertFalse(route_miss.record_miss(self.repo, prompt, True))

    def test_a_full_log_keeps_the_newest_lines_and_keeps_recording(self) -> None:
        self.write_log([miss(f"d{i}") for i in range(route_miss.MAX_LINES)])
        with self.opt_in():
            self.assertTrue(route_miss.record_miss(self.repo, "newest", True))
        lines = self.log.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), route_miss.MAX_LINES)
        self.assertEqual(json.loads(lines[-1])["text"], "newest")
        self.assertEqual(json.loads(lines[0])["session"], f"d{route_miss.MAX_LINES // 2}")

    def test_the_byte_cap_never_leaves_a_log_the_reader_rejects(self) -> None:
        wide = "\u4e00" * route_miss.MAX_CLAIM
        with self.opt_in():
            for _ in range(route_miss.MAX_LINES + 20):
                route_miss.record_miss(self.repo, wide, True)
        self.assertLessEqual(self.log.stat().st_size, route_miss.MAX_BYTES)
        self.assertGreater(len(route_miss.RouteMissSource().read(self.repo, {})), 0)

    def test_a_prompt_that_cannot_be_encoded_never_raises_or_leaves_a_broken_line(self) -> None:
        with self.opt_in():
            route_miss.record_miss(self.repo, "bad \udcff byte", True)
        if self.log.exists():
            for line in self.log.read_text(encoding="utf-8").splitlines():
                json.loads(line)

    def test_a_symlinked_log_is_never_written_through(self) -> None:
        target = Path(self._tmp.name) / "victim.txt"
        target.write_text("keep", encoding="utf-8")
        os.chmod(target, 0o600)
        self.log.parent.mkdir(parents=True, mode=0o700)
        self.log.symlink_to(target)
        with self.opt_in():
            self.assertFalse(route_miss.record_miss(self.repo, "p", True))
        self.assertEqual(target.read_text(encoding="utf-8"), "keep")

    def test_a_shared_state_directory_is_refused(self) -> None:
        self.state.mkdir(mode=0o700)
        os.chmod(self.state, 0o777)  # nosec B103  # Test fixture that builds a world-writable directory on purpose.
        with self.opt_in():
            self.assertFalse(route_miss.record_miss(self.repo, "p", True))
        self.assertFalse(self.log.exists())

    def test_a_log_with_loose_permissions_is_not_appended_to(self) -> None:
        self.write_log([miss("d1")])
        os.chmod(self.log, 0o644)
        with self.opt_in():
            self.assertFalse(route_miss.record_miss(self.repo, "p", True))

    def test_concurrent_writers_lose_no_line_and_tear_none(self) -> None:
        import threading
        with self.opt_in():
            workers = [threading.Thread(target=lambda n=n: [route_miss.record_miss(self.repo, f"w{n}-{i}", True) for i in range(40)])
                       for n in range(6)]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()
        texts = [json.loads(line)["text"] for line in self.log.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(sorted(texts), sorted(f"w{n}-{i}" for n in range(6) for i in range(40)))

    def test_a_writer_waits_for_the_lock_held_by_another(self) -> None:
        import fcntl
        import threading
        import time
        self.state.mkdir(mode=0o700)
        holder = os.open(self.state / (route_miss.LOG_NAME + ".lock"), os.O_WRONLY | os.O_CREAT, 0o600)
        fcntl.flock(holder, fcntl.LOCK_EX)
        try:
            with self.opt_in():
                writer = threading.Thread(target=route_miss.record_miss, args=(self.repo, "waiting", True))
                writer.start()
                time.sleep(0.4)
                self.assertFalse(self.log.exists(), "the writer did not wait for the lock")
                fcntl.flock(holder, fcntl.LOCK_UN)
                writer.join(timeout=10)
        finally:
            os.close(holder)
        self.assertEqual(json.loads(self.log.read_text(encoding="utf-8"))["text"], "waiting")

    def test_a_harness_session_marker_means_the_run_is_not_interactive(self) -> None:
        data = self.repo / "harnesses" / "x" / "harness.json"
        data.parent.mkdir(parents=True)
        data.write_text(json.dumps({"session_markers": ["COACUS_TEST_SESSION"]}), encoding="utf-8")
        for marker, expected in ((None, True), ("1", False)):
            with self.subTest(marker=marker), self.opt_in(), \
                    mock.patch.object(sys.stdin, "isatty", return_value=True), \
                    mock.patch.object(sys.stdout, "isatty", return_value=True):
                env = {k: v for k, v in os.environ.items() if k != "COACUS_TEST_SESSION"}
                if marker:
                    env["COACUS_TEST_SESSION"] = marker
                self.log.unlink(missing_ok=True)
                with mock.patch.dict(os.environ, env, clear=True):
                    route_miss.record_miss(self.repo, "p")
                self.assertIs(json.loads(self.log.read_text(encoding="utf-8"))["interactive"], expected)

    def test_unreadable_harness_data_means_not_interactive(self) -> None:
        data = self.repo / "harnesses" / "x" / "harness.json"
        data.parent.mkdir(parents=True)
        data.write_text("{not json", encoding="utf-8")
        with self.opt_in(), mock.patch.object(sys.stdin, "isatty", return_value=True), \
                mock.patch.object(sys.stdout, "isatty", return_value=True):
            route_miss.record_miss(self.repo, "p")
        self.assertIs(json.loads(self.log.read_text(encoding="utf-8"))["interactive"], False)

    def test_an_unwritable_location_never_raises(self) -> None:
        self.state.write_text("a file, not a directory", encoding="utf-8")
        with self.opt_in():
            self.assertFalse(route_miss.record_miss(self.repo, "p", True))

    def test_the_router_writes_a_line_on_a_miss_and_nothing_on_a_match(self) -> None:
        import scripts.coacus_route as router_cli
        root = Path(__file__).resolve().parents[1]
        args = router_cli.argparse.Namespace(prompt="", raw=True, top=None, all=False, max_slots=0,
                                             min_score=router_cli.router.DEFAULT_MIN_SCORE, rerank=None)
        with self.opt_in(), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            args.prompt = "security architecture threat model review"
            self.assertEqual(router_cli._cmd_rank(args, root), 0)
            self.assertFalse(self.log.exists())
            args.prompt = "qqqqzzzz xxkkjj wwvvuu"
            self.assertEqual(router_cli._cmd_rank(args, root), 1)
        self.assertEqual(json.loads(self.log.read_text(encoding="utf-8"))["text"], "qqqqzzzz xxkkjj wwvvuu")

    def test_a_failure_while_logging_never_changes_the_router_result(self) -> None:
        import scripts.coacus_route as router_cli
        with mock.patch("engine.improve.sources.route_miss.record_miss", side_effect=RuntimeError("simulated failure")):
            router_cli._log_miss(self.repo, "p")


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
