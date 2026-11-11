import shlex
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import coacus_eval


class LegacyJudgeSafetyTests(unittest.TestCase):
    def test_legacy_agent_is_not_invoked(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'invoked'
            code = f'open({str(marker)!r}, "w").write("invoked")'
            result = coacus_eval._judge({'harness': 'test'}, 'untrusted', None, True,
                                        {'test': [sys.executable, '-c', code]})
            self.assertFalse(marker.exists())
            self.assertIs(result['passed'], False)
            self.assertIn('isolation', result['verdict'])

    def test_legacy_command_output_limit_fails_closed(self):
        cmd = shlex.join([sys.executable, '-c', 'print("VERDICT: PASS" + "x" * 1200000)'])
        result = coacus_eval._judge({'harness': 'test'}, 'data', cmd, False, {})
        self.assertIs(result['passed'], False)
        self.assertIn('OUTPUT_LIMIT', result['verdict'])

    def test_unrecognized_legacy_verdict_fails_closed(self):
        cmd = shlex.join([sys.executable, '-c', 'print("uncertain")'])
        result = coacus_eval._judge({'harness': 'test'}, 'data', cmd, False, {})
        self.assertIs(result['passed'], False)

    def test_legacy_command_receives_original_payload_and_explicit_verdict(self):
        code = 'import json,sys; p=json.load(sys.stdin); print("VERDICT: PASS" if p["transcript"] == "data" else "VERDICT: FAIL")'
        result = coacus_eval._judge({'harness': 'test'}, 'data', shlex.join([sys.executable, '-c', code]), False, {})
        self.assertIs(result['passed'], True)
