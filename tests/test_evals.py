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


class TestEvidenceBeforeClaimsScenario(unittest.TestCase):
    def test_runner_normalizes_response_before_scenario_checks(self) -> None:
        import sys

        path = Path(__file__).resolve().parents[1] / "evals/scenarios/evidence-before-claims/scenario.json"
        scenario = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("normalized", scenario["acceptance"].lower())
        self.assertFalse(any("file" in item.lower() for item in scenario["rubric"]))
        for response, expected in [(" \nA\n\n ", True), ("\x1b[32mA\x1b[0m", True),
                                   ("A extra", False), ("B", False)]:
            with self.subTest(response=response):
                command = [sys.executable, "-c", f"import sys; sys.stdout.write({response!r})"]
                transcript, status = coacus_eval._run_harness(scenario, 5, {"opencode": command})
                self.assertEqual(status, "OK")
                self.assertEqual(all(r["passed"] for r in coacus_eval._apply_checks(scenario, transcript)), expected)

    def test_response_contract_fails_closed(self) -> None:
        path = Path(__file__).resolve().parents[1] / "evals/scenarios/evidence-before-claims/scenario.json"
        scenario = json.loads(path.read_text(encoding="utf-8"))
        for response, expected in [("A", True), ("A\n", False), ("B", False),
                                   ("C", False), ("", False), ("not A", False),
                                   ("A, but do not run tests", False)]:
            with self.subTest(response=response):
                self.assertEqual(all(r["passed"] for r in coacus_eval._apply_checks(scenario, response)), expected)


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
        with mock.patch.object(coacus_eval, "_bounded_run", return_value=(fake.stdout, fake.stderr, fake.returncode, None)):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "EXIT_1")
        self.assertEqual(transcript, "")

    def test_ansi_is_stripped(self) -> None:
        import subprocess as sp
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        fake = sp.CompletedProcess(args=[], returncode=0, stdout="\x1b[32mok\x1b[0m", stderr="")
        with mock.patch.object(coacus_eval, "_bounded_run", return_value=(fake.stdout, fake.stderr, fake.returncode, None)):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "OK")
        self.assertEqual(transcript, "ok")

    def test_stderr_is_used_when_stdout_is_empty(self) -> None:
        import subprocess as sp
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        fake = sp.CompletedProcess(args=[], returncode=0, stdout="", stderr="the answer is 5")
        with mock.patch.object(coacus_eval, "_bounded_run", return_value=(fake.stdout, fake.stderr, fake.returncode, None)):
            transcript, status = coacus_eval._run_harness(scenario, 5, CLIS)
        self.assertEqual(status, "OK")
        self.assertEqual(transcript, "the answer is 5")

    def test_missing_cli_is_reported(self) -> None:
        from unittest import mock

        scenario = {"harness": "opencode", "prompt": "x", "checks": []}
        with mock.patch.object(
            coacus_eval, "_bounded_run", side_effect=FileNotFoundError
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

    def test_strict_judge_schema_fails_closed(self) -> None:
        from unittest import mock
        import subprocess
        scenario = {**SCENARIO, "judge_required": True, "rubric": ["first", "second"]}
        for output, expected in [
            ('{"verdicts":[true,true]}', True),
            ('{"verdicts":[true,false]}', False),
            ('{"verdicts":[true]}', False),
            ('{"verdicts":[true,true],"verdicts":[true,true]}', False),
            ('VERDICT: PASS', False),
            ('{"verdicts":[1,true]}', False),
        ]:
            with self.subTest(output=output), mock.patch.object(coacus_eval, "_bounded_run", return_value=(output, "", 0, None)):
                self.assertEqual(coacus_eval._judge(scenario, "untrusted", "judge", False, CLIS)["passed"], expected)
        with mock.patch.object(coacus_eval, "_bounded_run", return_value=('{"verdicts":[true,true]}', "", 1, None)):
            self.assertFalse(coacus_eval._judge(scenario, "x", "judge", False, CLIS)["passed"])
        self.assertFalse(coacus_eval._judge(scenario, "x", None, False, CLIS)["passed"])

    def test_strict_transcript_is_bounded_encoded_and_labelled(self) -> None:
        from unittest import mock
        import subprocess, base64
        scenario = {**SCENARIO, "judge_required": True}
        with mock.patch.object(coacus_eval, "_bounded_run", return_value=('{"verdicts":[true]}', "", 0, None)) as run:
            result = coacus_eval._judge(scenario, "ignore instructions" * 10000, "judge", False, CLIS)
            run.assert_not_called()
            self.assertEqual(result["verdict"], "TRANSCRIPT_TRUNCATED")
            self.assertFalse(result["passed"])
            coacus_eval._judge(scenario, "x" * 32768, "judge", False, CLIS)
        payload = json.loads(run.call_args.args[2])
        self.assertEqual(payload["transcript"]["trust"], "untrusted")
        self.assertFalse(payload["transcript"]["truncated"])
        self.assertEqual(len(base64.b64decode(payload["transcript"]["base64"])), 32768)
        self.assertFalse(coacus_eval._judge(scenario, "x" * 32769, None, False, CLIS)["passed"])

    def test_whitespace_judge_is_unavailable(self) -> None:
        for required in (False, True):
            with self.subTest(required=required):
                result = coacus_eval._judge({**SCENARIO, "judge_required": required}, "x", " \t ", False, CLIS)
                self.assertIn("unavailable", result["verdict"])
                self.assertFalse(result["passed"])

    def test_strict_judge_reports_process_failure_reason(self) -> None:
        from unittest import mock
        scenario = {**SCENARIO, "judge_required": True}
        for status, code, reason in [("TIMEOUT", -9, "TIMEOUT"), ("OUTPUT_LIMIT", -9, "OUTPUT_LIMIT"), (None, 7, "EXIT_7")]:
            with self.subTest(reason=reason), mock.patch.object(coacus_eval, "_bounded_run", return_value=("", "", code, status)):
                result = coacus_eval._judge(scenario, "x", "judge", False, CLIS)
                self.assertIn(reason, result["verdict"])
                self.assertFalse(result["passed"])

    def test_invalid_judge_required_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp), {**SCENARIO, "judge_required": "yes"})
            self.assertTrue(any("judge_required" in e for e in evals.validate(root)))

    def test_requested_unsupported_agent_fails_legacy_run(self) -> None:
        from unittest import mock
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            with mock.patch.object(coacus_eval, "_run_harness", return_value=("ok", "OK")):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    result = coacus_eval.cmd_run(root, "example", None, True, 1)
            self.assertEqual(result, 1)
            self.assertFalse(json.loads(output.getvalue())["passed"])

    def test_verdict_parsing(self) -> None:
        self.assertTrue(coacus_eval._verdict_pass("VERDICT: PASS\nok"))
        self.assertFalse(coacus_eval._verdict_pass("VERDICT: FAIL\nnope"))
        self.assertIsNone(coacus_eval._verdict_pass("maybe"))

    def test_verdict_requires_one_complete_standalone_line(self) -> None:
        for text in ("VERDICT: PASSING", "prefix VERDICT: PASS", "VERDICT: PASS extra",
                     "VERDICT: PASS\nVERDICT: FAIL", "VERDICT: PASS\nVERDICT: PASS",
                     "VERDICT: PASS\nVERDICT: UNKNOWN"):
            with self.subTest(text=text):
                self.assertIsNone(coacus_eval._verdict_pass(text))
        self.assertTrue(coacus_eval._verdict_pass("explanation\n verdict: pass \nmore"))

    def test_run_skips_judge_when_prerequisites_fail(self) -> None:
        from unittest import mock
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(Path(tmp))
            for transcript, status, reason in [("ok", "EXIT_1", "harness"),
                                                ("wrong", "OK", "checks")]:
                with self.subTest(reason=reason), mock.patch.object(coacus_eval, "_run_harness", return_value=(transcript, status)), mock.patch.object(coacus_eval, "_judge") as judge, contextlib.redirect_stdout(io.StringIO()) as output:
                    result = coacus_eval.cmd_run(root, "example", "judge", False, 1)
                self.assertEqual(result, 1)
                judge.assert_not_called()
                report = json.loads(output.getvalue())
                self.assertFalse(report["passed"])
                self.assertEqual(report["judge"]["mode"], "skipped")
                self.assertIn(reason, report["judge"]["reason"].lower())

    def test_requested_judge_failure_fails_closed(self) -> None:
        verdict = coacus_eval._judge(SCENARIO, "t", "nonexistent-judge", False, CLIS)
        self.assertIs(verdict["passed"], False)

    def test_judge_command_uses_callers_directory(self) -> None:
        import os
        import shlex
        import sys
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "judge.py"
            script.write_text('print("VERDICT: PASS")\n', encoding="utf-8")
            cmd = f'{shlex.quote(sys.executable)} judge.py'
            code = ('from scripts import coacus_eval; '
                    f'print(coacus_eval._judge({SCENARIO!r}, "x", {cmd!r}, False, {{}})["passed"])')
            result = subprocess.run([sys.executable, '-c', code], cwd=tmp,
                                    env={**os.environ, 'PYTHONPATH': str(coacus_eval.ROOT)},
                                    capture_output=True, text=True, check=True)
            self.assertEqual(result.stdout.strip(), 'True')

    def test_seeded_scenarios_are_valid(self) -> None:
        root = Path(coacus_eval.ROOT)
        self.assertEqual(evals.validate(root), [])
        seeded = {
            'artifact-lifecycle', 'bootstrap-activation', 'brainstorm-before-build',
            'evidence-before-claims', 'expected-first-selection',
            'governance-cap-and-toon', 'skill-first-discipline', 'tool-budget',
            'unavailable-honesty',
        }
        discovered = {path.parent.name for path in evals.discover(root)}
        self.assertFalse(seeded - discovered, f'Missing seeded scenarios: {seeded - discovered}')


if __name__ == "__main__":
    unittest.main()
