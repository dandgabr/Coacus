"""Tests for the TOON payload parser/validator (D7/ADR-0008)."""

from __future__ import annotations

import unittest

from engine import toon

VALID = """@FROM: agent-a
@TO: orchestrator
@STATUS: OK
@CTX: COACUS-F4-task
@FILES: engine/governor/ledger.py:1-120;tests/test_governor.py:1-90
@SUMMARY: implemented the governor ledger
@ACTION_NEEDED: review and merge
"""


class TestToon(unittest.TestCase):
    def test_valid_payload(self) -> None:
        self.assertEqual(toon.validate(VALID), [])
        self.assertTrue(toon.is_valid(VALID))

    def test_parse_fields(self) -> None:
        fields = toon.parse(VALID)
        self.assertEqual(fields["@FROM"], "agent-a")
        self.assertEqual(fields["@STATUS"], "OK")

    def test_missing_required_field(self) -> None:
        text = VALID.replace("@CTX: COACUS-F4-task\n", "")
        errors = toon.validate(text)
        self.assertTrue(any("@CTX" in e for e in errors))

    def test_invalid_status(self) -> None:
        text = VALID.replace("@STATUS: OK", "@STATUS: DONE")
        errors = toon.validate(text)
        self.assertTrue(any("@STATUS" in e for e in errors))

    def test_unknown_field_is_rejected(self) -> None:
        text = VALID + "@EXTRA: nope\n"
        errors = toon.validate(text)
        self.assertTrue(any("unknown field" in e for e in errors))

    def test_absolute_path_in_files_is_rejected(self) -> None:
        text = VALID.replace(
            "@FILES: engine/governor/ledger.py:1-120;tests/test_governor.py:1-90",
            "@FILES: /home/dev/secret.py:1-5",
        )
        errors = toon.validate(text)
        self.assertTrue(any("relative" in e for e in errors))

    def test_secret_in_files_is_rejected(self) -> None:
        text = VALID.replace(
            "@FILES: engine/governor/ledger.py:1-120;tests/test_governor.py:1-90",
            "@FILES: config.py:1-3 AKIAIOSFODNN7EXAMPLE",
        )
        errors = toon.validate(text)
        self.assertTrue(any("secret" in e for e in errors))

    def test_empty_payload(self) -> None:
        self.assertTrue(toon.validate("no fields here"))

    def test_optional_fields_may_be_absent(self) -> None:
        text = "@FROM: a\n@TO: b\n@STATUS: NEED_INFO\n@CTX: c\n@SUMMARY: s\n"
        self.assertEqual(toon.validate(text), [])

    def test_path_with_colon_is_not_truncated(self) -> None:
        # Regression: a relative path containing ':' must stay relative-valid.
        text = VALID.replace(
            "@FILES: engine/governor/ledger.py:1-120;tests/test_governor.py:1-90",
            "@FILES: weird:name/f.py:1-5",
        )
        self.assertEqual(toon.validate(text), [])

    def test_files_entry_without_path_is_rejected(self) -> None:
        text = VALID.replace(
            "@FILES: engine/governor/ledger.py:1-120;tests/test_governor.py:1-90",
            "@FILES: :1-5",
        )
        errors = toon.validate(text)
        self.assertTrue(any("no path" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
