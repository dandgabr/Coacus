"""Safety checks for the opt-in Command Code local-model probe."""

from __future__ import annotations

import contextlib
import io
import unittest
from unittest.mock import patch

from evals import command_code_mod_probe


class CommandCodeModProbeTests(unittest.TestCase):
    def test_event_filter_does_not_emit_untrusted_values(self) -> None:
        sensitive = ["synthetic-token-123", "person@example.test", "00000000-0000-0000-0000-000000000000"]
        frames = [{"event": {"type": value, "body": sensitive}} for value in sensitive]
        frames.extend([{"event": {"type": []}}, {"event": {"type": "mod_error", "body": sensitive}}])
        self.assertEqual(command_code_mod_probe.selected_events(frames), ["mod_error"])

    def test_missing_cli_is_reported_without_exposing_environment(self) -> None:
        output = io.StringIO()
        secret = "synthetic-token-123"
        with patch.dict("os.environ", {"PATH": "", "EXAMPLE_SECRET": secret}, clear=True):
            with contextlib.redirect_stdout(output):
                result = command_code_mod_probe.main()
        self.assertEqual(result, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertEqual(output.getvalue().count('"status": "unavailable"'), 2)
