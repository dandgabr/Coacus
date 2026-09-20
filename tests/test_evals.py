"""Tests for the behavior-eval scenario validator and runner helpers (D10)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.validators import evals
from scripts import coacus_eval

SCENARIO = {
    "id": "example",
    "title": "Example scenario",
    "harness": "opencode",
    "prompt": "Do the thing.",
    "checks": [{"kind": "contains", "value": "ok"}],
    "rubric": ["The reply says ok."],
    "acceptance": "Says ok.",
}

# A live-CLI map as the runner would read it from harness.json.
CLIS = {"opencode": ["opencode", "run"], "codex": ["codex", "exec"]}


def make_repo(tmp: Path, scenario: dict = SCENARIO) -> Path:
    root = tmp / "repo"
    (root / "harnesses/opencode").mkdir(parents=True)
    (root / "harnesses/opencode/harness.json").write_text(
        json.dumps({"name": "opencode"}), encoding="utf-8"
    )
    directory = root / "evals/scenarios" / scenario["id"]
    directory.mkdir(parents=True)
    (directory / "scenario.json").write_text(json.dumps(scenario), encoding="utf-8")
    return root


class TestEvalValidator(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = make_repo(Path(self._tmp.name))

    def test_valid_scenario_passes(self) -> None:
        self.assertEqual(evals.validate(self.root), [])

    def test_unknown_harness_fails(self) -> None:
        root = make_repo(Path(self._tmp.name) / "b", {**SCENARIO, "harness": "ghost"})
        self.assertTrue(any("unknown harness" in e for e in evals.validate(root)))

    def test_missing_key_fails(self) -> None:
        scenario = {k: v for k, v in SCENARIO.items() if k != "rubric"}
        root = make_repo(Path(self._tmp.name) / "c", scenario)
        self.assertTrue(any("missing key 'rubric'" in e for e in evals.validate(root)))

    def test_bad_check_kind_fails(self) -> None:
        bad = {**SCENARIO, "checks": [{"kind": "whatever", "value": "x"}]}
        root = make_repo(Path(self._tmp.name) / "d", bad)
        self.assertTrue(any("kind" in e for e in evals.validate(root)))

    def test_bad_regex_fails(self) -> None:
        bad = {**SCENARIO, "checks": [{"kind": "regex", "value": "("}]}
        root = make_repo(Path(self._tmp.name) / "e", bad)
        self.assertTrue(any("bad regex" in e for e in evals.validate(root)))

    def test_absolute_path_in_prompt_fails(self) -> None:
        bad = {**SCENARIO, "prompt": "read /home/dev/x"}
        root = make_repo(Path(self._tmp.name) / "f", bad)
        self.assertTrue(any("absolute path" in e for e in evals.validate(root)))

    def test_id_directory_mismatch_fails(self) -> None:
        root = make_repo(Path(self._tmp.name) / "g")
        (root / "evals/scenarios/example/scenario.json").write_text(
            json.dumps({**SCENARIO, "id": "other"}), encoding="utf-8"
        )
        self.assertTrue(any("directory name" in e for e in evals.validate(root)))

    def test_regex_without_value_does_not_crash(self) -> None:
        bad = {**SCENARIO, "checks": [{"kind": "regex"}]}
        root = make_repo(Path(self._tmp.name) / "h", bad)
        errors = evals.validate(root)  # must not raise KeyError
        self.assertTrue(any("non-empty string 'value'" in e for e in errors))

    def test_non_string_harness_does_not_crash(self) -> None:
        bad = {**SCENARIO, "harness": ["opencode"]}
        root = make_repo(Path(self._tmp.name) / "i", bad)
        errors = evals.validate(root)  # must not raise TypeError
        self.assertTrue(any("'harness' must be a string" in e for e in errors))

    def test_non_string_check_value_is_rejected(self) -> None:
        bad = {**SCENARIO, "checks": [{"kind": "contains", "value": 5}]}
        root = make_repo(Path(self._tmp.name) / "j", bad)
        self.assertTrue(any("non-empty string" in e for e in evals.validate(root)))

    def test_non_string_title_is_rejected(self) -> None:
        bad = {**SCENARIO, "title": ["x"]}
        root = make_repo(Path(self._tmp.name) / "k", bad)
        self.assertTrue(any("'title' must be a string" in e for e in evals.validate(root)))

    def test_secret_in_rubric_is_rejected(self) -> None:
        bad = {**SCENARIO, "rubric": ["leaked AKIAIOSFODNN7EXAMPLE here"]}
        root = make_repo(Path(self._tmp.name) / "l", bad)
        self.assertTrue(any("aws-access-key" in e for e in evals.validate(root)))

    def test_absolute_path_in_acceptance_is_rejected(self) -> None:
        bad = {**SCENARIO, "acceptance": "reads /home/dev/notes.md"}
        root = make_repo(Path(self._tmp.name) / "m", bad)
        self.assertTrue(any("absolute path" in e for e in evals.validate(root)))

    def test_malformed_harness_manifest_is_reported(self) -> None:
        root = make_repo(Path(self._tmp.name) / "n")
        (root / "harnesses/opencode/harness.json").write_text("{ nope", encoding="utf-8")
        self.assertTrue(any("unreadable harness manifest" in e for e in evals.validate(root)))


class TestEvalRunnerHelpers(unittest.TestCase):
    def test_checks_contains_and_not_contains(self) -> None:
        scenario = {
            "checks": [
                {"kind": "contains", "value": "hello"},
                {"kind": "not_contains", "value": "none"},
            ]
        }
        results = coacus_eval._apply_checks(scenario, "well hello there")
        self.assertTrue(all(r["passed"] for r in results))

    def test_regex_check(self) -> None:
        scenario = {"checks": [{"kind": "regex", "value": "(?i)cap.*5"}]}
        results = coacus_eval._apply_checks(scenario, "the CAP is 5")
        self.assertTrue(results[0]["passed"])

    def test_nonzero_exit_is_not_ok(self) -> None:
        import subprocess as sp
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        fake = sp.CompletedProcess(args=[], returncode=1, stdout="partial", stderr="auth")
        with mock.patch.object(coacus_eval.subprocess, "run", return_value=fake):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "EXIT_1")
        self.assertEqual(transcript, "")

    def test_ansi_is_stripped(self) -> None:
        import subprocess as sp
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        fake = sp.CompletedProcess(args=[], returncode=0, stdout="\x1b[32mok\x1b[0m", stderr="")
        with mock.patch.object(coacus_eval.subprocess, "run", return_value=fake):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "OK")
        self.assertEqual(transcript, "ok")

    def test_stderr_is_used_when_stdout_is_empty(self) -> None:
        import subprocess as sp
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        fake = sp.CompletedProcess(args=[], returncode=0, stdout="", stderr="the answer is 5")
        with mock.patch.object(coacus_eval.subprocess, "run", return_value=fake):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "OK")
        self.assertEqual(transcript, "the answer is 5")

    def test_missing_cli_is_reported(self) -> None:
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        with mock.patch.object(
            coacus_eval.subprocess, "run", side_effect=FileNotFoundError
        ):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertTrue(status.startswith("NO_CLI"))

    def test_harness_without_live_cli_is_no_runner(self) -> None:
        scenario = {"harness": "cursor", "prompt": "x", "checks": []}
        transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "NO_RUNNER (cursor)")

    def test_live_clis_read_from_harness_json(self) -> None:
        clis = coacus_eval._live_clis(Path(coacus_eval.ROOT))
        self.assertEqual(clis["codex"], ["codex", "exec"])
        self.assertEqual(clis["antigravity"], ["agy", "--print"])

    def test_verdict_parsing(self) -> None:
        self.assertTrue(coacus_eval._verdict_pass("VERDICT: PASS\nok"))
        self.assertFalse(coacus_eval._verdict_pass("VERDICT: FAIL\nnope"))
        self.assertIsNone(coacus_eval._verdict_pass("maybe"))

    def test_judge_cmd_failure_is_advisory(self) -> None:
        from unittest import mock

        scenario = {"harness": "opencode", "checks": [], "rubric": ["r"]}
        with mock.patch.object(
            coacus_eval.subprocess, "run", side_effect=FileNotFoundError
        ):
            verdict = coacus_eval._judge(scenario, "t", "nonexistent-judge", False, CLIS)
        self.assertIsNone(verdict["passed"])

    def test_seeded_scenarios_are_valid(self) -> None:
        root = Path(coacus_eval.ROOT)
        self.assertEqual(evals.validate(root), [])
        self.assertEqual(len(evals.discover(root)), 6)


if __name__ == "__main__":
    unittest.main()
