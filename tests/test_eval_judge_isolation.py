"""Security boundary for required live-evaluation judges."""

import json
import shlex
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.coacus_eval import _judge, cmd_run
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import os


class JudgeIsolationTests(unittest.TestCase):
    def test_required_agent_never_executes_harness_even_with_command(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            code = f"from pathlib import Path; Path({str(marker)!r}).touch(); print('{{\"verdicts\": [true]}}')"
            scenario = {"harness": "test", "judge_required": True, "rubric": ["safe"]}
            result = _judge(scenario, "untrusted", shlex.join([sys.executable, "-c", code]), True,
                            {"test": [sys.executable, "-c", code]})
            self.assertFalse(result["passed"])
            self.assertFalse(marker.exists())

    def test_report_exposes_safe_reason_without_judge_output(self):
        scenario = {"harness": "test", "judge_required": True, "rubric": ["safe"], "checks": []}
        for status in ("TIMEOUT", "OUTPUT_LIMIT", "UNSUPPORTED_PLATFORM", "secret status"):
            with self.subTest(status=status), patch.dict(os.environ, {"COACUS_EVAL_VERBOSE": "0"}), \
                 patch("scripts.coacus_eval.scenario_validator.validate", return_value=[]), \
                 patch("scripts.coacus_eval._scenarios", return_value={"case": scenario}), \
                 patch("scripts.coacus_eval._live_clis", return_value={"test": ["test"]}), \
                 patch("scripts.coacus_eval._run_harness", return_value=("secret transcript", "OK")), \
                 patch("scripts.coacus_eval._bounded_run", return_value=("secret stdout", "secret stderr", 1, status)):
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(cmd_run(Path('.'), 'case', 'judge', False, 1), 1)
                report = json.loads(output.getvalue())
                self.assertEqual(report['judge']['reason_code'], status if status != 'secret status' else 'JUDGE_EXIT')
                self.assertNotIn('secret', output.getvalue())

    def test_required_external_command_is_allowed(self):
        scenario = {"harness": "test", "judge_required": True, "rubric": ["safe"]}
        code = "import json,sys; json.load(sys.stdin); print(json.dumps({'verdicts':[True]}))"
        result = _judge(scenario, "untrusted", shlex.join([sys.executable, "-c", code]), False, {})
        self.assertTrue(result["passed"])


if __name__ == "__main__":
    unittest.main()
