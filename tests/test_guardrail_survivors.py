"""Fail-closed branches that review mutation testing showed were not guarded."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from engine.guardrail import evaluate as guard
from scripts import coacus_guard

REPO = Path(__file__).resolve().parents[1]


def fake_root(channel) -> Path:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    shutil.copytree(REPO / "harnesses/opencode", root / "harnesses/opencode")
    path = root / "harnesses/opencode/harness.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    cap = data["lifecycle"]["events"]["tool.pre"]
    if channel is None:
        cap.pop("ask_channel", None)
    else:
        cap["ask_channel"] = channel
    path.write_text(json.dumps(data), encoding="utf-8")
    fake_root.keep = getattr(fake_root, "keep", []) + [tmp]
    return root


class TestAskChannelValue(unittest.TestCase):
    ENV = {"COACUS_GUARD_ASK": "1", "COACUS_GUARD_ASK_EXPERIMENTAL": "1"}

    def test_only_the_evaluate_channel_value_is_recognised(self) -> None:
        with mock.patch.dict(os.environ, self.ENV, clear=True):
            for value in ("evaluate", "prompt", "", "EVALUATE", 5, None):
                root = fake_root(value if value is not None else "__absent__")
                with self.subTest(value=value):
                    asks = coacus_guard._can_ask(root, "opencode", "tool.pre", "evaluate")
                    self.assertEqual(asks, value == "evaluate")

    def test_a_harness_without_a_channel_asks_only_on_default(self) -> None:
        with mock.patch.dict(os.environ, self.ENV, clear=True):
            root = fake_root(None)
            self.assertTrue(coacus_guard._can_ask(root, "opencode", "tool.pre", "default"))
            self.assertFalse(coacus_guard._can_ask(root, "opencode", "tool.pre", "evaluate"))
            self.assertFalse(coacus_guard._can_ask(root, "opencode", "tool.pre", "before"))


class TestPathForms(unittest.TestCase):
    ASK = {"id": "a", "action": {"verb": "read", "resource": "*"}, "decision": "ask"}

    def test_forms_include_absolute_relative_and_last_component(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            os.chdir(tmp)
            try:
                forms = coacus_guard._path_forms("sub/.env")
                real = os.path.realpath(tmp)
                self.assertIn("sub/.env", forms)
                self.assertIn(".env", forms)
                self.assertTrue(any(f.endswith("/sub/.env") and f.startswith("/") for f in forms))
                self.assertIn(os.path.relpath(os.path.join(real, "sub/.env"), os.path.dirname(real)), forms)
            finally:
                os.chdir(old)

    def test_an_ask_that_only_matches_a_relative_form_is_not_deferred(self) -> None:
        # A policy anchored on a path relative to an ancestor of the working directory
        # matches one form only; every form must ask for the call to be deferred.
        policy = {"id": "a", "action": {"verb": "read", "resource": "*/.env"}, "decision": "ask"}
        self.assertFalse(coacus_guard._survives_the_hook([policy], "read", ".env"))
        self.assertTrue(coacus_guard._survives_the_hook([self.ASK], "read", ".env"))


class TestWalkLimits(unittest.TestCase):
    def test_exceeding_the_step_limit_marks_the_command_unresolved(self) -> None:
        state = {"unresolved": False, "steps": guard._STEP_LIMIT}
        guard._words_candidates(["echo", "hi"], 0, state)
        self.assertTrue(state["unresolved"])
        state = {"unresolved": False, "steps": guard._STEP_LIMIT}
        guard._scan("echo hi", 0, state)
        self.assertTrue(state["unresolved"])

    def test_keyword_and_redirection_stripping_respects_the_depth_cap(self) -> None:
        state = {"unresolved": False}
        guard._words_candidates(["!", "echo", "hi"], guard._MAX_DEPTH, state)
        self.assertTrue(state["unresolved"])

    def test_an_internal_error_in_the_walk_is_unresolved(self) -> None:
        guard._resolve_cached.cache_clear()
        with mock.patch.object(guard, "_scan", side_effect=RuntimeError("boom")):
            self.assertEqual(guard.resolve_command("anything at all"), ([], True))
        guard._resolve_cached.cache_clear()


if __name__ == "__main__":
    unittest.main()
