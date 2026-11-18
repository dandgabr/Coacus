"""The installer warns when an ask policy will degrade, and asks before continuing."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import coacus_install

REPO = Path(__file__).resolve().parents[1]


def ask_doc(fallback="deny", enabled=True, policy_id="ask-env") -> dict:
    return {"schema": 1, "enabled": enabled, "policies": [
        {"id": policy_id, "action": {"verb": "read", "resource": "**/.env"},
         "decision": "ask", "on_ask_unavailable": fallback}]}


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(item.relative_to(path)).encode())
        digest.update(item.read_bytes())
    return digest.hexdigest()


class TestAskWarnings(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.user_dir = Path(self._tmp.name) / "policies"
        self.user_dir.mkdir()

    def _write(self, doc: dict, name: str = "a.policy.json") -> None:
        (self.user_dir / name).write_text(json.dumps(doc), encoding="utf-8")

    def _warn(self, harnesses, env=None, extra=None) -> list[dict]:
        return coacus_install.ask_warnings(REPO, harnesses, extra, self.user_dir, env or {})

    def test_no_ask_policy_means_no_warning(self) -> None:
        self.assertEqual(self._warn(["codex"]), [])

    def test_a_harness_that_cannot_ask_is_named(self) -> None:
        self._write(ask_doc())
        warnings = self._warn(["codex"], {"COACUS_GUARD_ASK": "1"})
        self.assertEqual([w["reason"] for w in warnings], ["the harness cannot ask"])
        self.assertEqual(warnings[0]["degrades_to"], "deny")
        self.assertFalse(warnings[0]["fails_open"])

    def test_a_harness_that_can_ask_warns_only_without_the_opt_in(self) -> None:
        self._write(ask_doc())
        self.assertEqual(self._warn(["claude-code"], {"COACUS_GUARD_ASK": "1"}), [])
        off = self._warn(["claude-code"], {})
        self.assertEqual(len(off), 1)
        self.assertIn("COACUS_GUARD_ASK=1", off[0]["reason"])

    def test_cursor_cannot_ask_and_opencode_can_through_its_channel(self) -> None:
        self._write(ask_doc())
        env = {"COACUS_GUARD_ASK": "1"}
        self.assertEqual(len(self._warn(["cursor"], env)), 1)
        self.assertEqual(self._warn(["opencode"], env), [])

    def test_an_allow_fallback_is_flagged_as_failing_open(self) -> None:
        self._write(ask_doc(fallback="allow"))
        self.assertTrue(self._warn(["codex"])[0]["fails_open"])

    def test_missing_or_invalid_fallback_counts_as_deny(self) -> None:
        for bad in ("ask", "note", None):
            doc = ask_doc()
            if bad is None:
                del doc["policies"][0]["on_ask_unavailable"]
            else:
                doc["policies"][0]["on_ask_unavailable"] = bad
            self._write(doc)
            with self.subTest(bad=bad):
                self.assertEqual(self._warn(["codex"])[0]["degrades_to"], "deny")

    def test_a_disabled_document_does_not_count(self) -> None:
        self._write(ask_doc(enabled=False))
        self.assertEqual(self._warn(["codex"]), [])

    def test_policies_generated_in_this_run_count(self) -> None:
        self.assertEqual(len(self._warn(["codex"], extra=[ask_doc(policy_id="fresh")])), 1)

    def test_deny_and_allow_policies_do_not_warn(self) -> None:
        doc = ask_doc()
        doc["policies"][0]["decision"] = "deny"
        self._write(doc)
        self.assertEqual(self._warn(["codex"]), [])

    def test_malformed_policies_values_never_crash(self) -> None:
        for bad in (None, 5, "x", {"a": 1}, [1, "x", None]):
            self._write({"schema": 1, "enabled": True, "policies": bad})
            with self.subTest(bad=bad):
                self.assertEqual(self._warn(["codex"]), [])

    def test_the_off_switches_are_named(self) -> None:
        self._write(ask_doc())
        for name in ("CI", "COACUS_GUARD_NO_ASK"):
            with self.subTest(switch=name):
                warnings = self._warn(["claude-code"], {"COACUS_GUARD_ASK": "1", name: "1"})
                self.assertEqual(len(warnings), 1)
                self.assertIn("switched off", warnings[0]["reason"])

    def test_falsy_off_switch_values_do_not_warn(self) -> None:
        self._write(ask_doc())
        for value in ("", "0", "false", "No", "OFF"):
            with self.subTest(value=value):
                self.assertEqual(self._warn(["claude-code"], {"COACUS_GUARD_ASK": "1", "CI": value}), [])

    def test_opencode_warns_for_an_ask_it_cannot_defer(self) -> None:
        shell = {"schema": 1, "enabled": True, "policies": [
            {"id": "ask-shell", "action": {"verb": "exec", "resource": "*deploy*"},
             "decision": "ask", "on_ask_unavailable": "allow"}]}
        self._write(shell)
        warnings = self._warn(["opencode"], {"COACUS_GUARD_ASK": "1"})
        self.assertEqual(len(warnings), 1)
        self.assertTrue(warnings[0]["fails_open"])
        self.assertIn("only for a read or a write", warnings[0]["reason"])
        self.assertEqual(self._warn(["claude-code"], {"COACUS_GUARD_ASK": "1"}), [])

    def test_unreadable_policy_files_are_skipped(self) -> None:
        (self.user_dir / "broken.policy.json").write_text("{not json", encoding="utf-8")
        self.assertEqual(self._warn(["codex"]), [])


class TestInstallerConfirmation(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        base = Path(self._tmp.name)
        self.config = base / "cfg"
        self.config.mkdir()
        self.policies = base / "policies"
        self.policies.mkdir()
        (self.policies / "a.policy.json").write_text(json.dumps(ask_doc()), encoding="utf-8")
        self.env = {k: v for k, v in os.environ.items() if k not in ("CI", "COACUS_GUARD_ASK")}
        self.env["COACUS_POLICY_DIR"] = str(self.policies)

    def _run(self, extra=None, *, interactive: bool, answer="") -> tuple[int, str, str, mock.Mock]:
        argv = ["codex", "--config-dir", str(self.config), "--skills", "using-coacus",
                "--agents", "general", "--browser-policy", "off", "--skills-mode", "copy",
                "--force", *(extra or [])]
        confirm = mock.Mock(return_value=answer)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(coacus_install, "_is_interactive", return_value=interactive), \
                mock.patch.object(coacus_install, "_confirm", confirm), \
                mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = coacus_install.main(argv, REPO)
        return code, out.getvalue(), err.getvalue(), confirm

    def test_non_interactive_warns_on_stderr_and_continues(self) -> None:
        code, out, err, confirm = self._run(interactive=False)
        confirm.assert_not_called()
        self.assertIn("will not prompt anyone", err)
        self.assertEqual(json.loads(out)[0]["ask_warnings"][0]["policy"], "ask-env")
        self.assertEqual(code, 0)

    def test_yes_continues_without_a_prompt(self) -> None:
        code, out, err, confirm = self._run(["--yes"], interactive=True)
        confirm.assert_not_called()
        self.assertIn("will not prompt anyone", err)
        self.assertEqual(code, 0)

    def test_dry_run_never_prompts(self) -> None:
        _, _, _, confirm = self._run(["--dry-run"], interactive=True)
        confirm.assert_not_called()

    def test_yes_answer_continues(self) -> None:
        for answer in ("y", "Y", "yes", " YES \n"):
            with self.subTest(answer=answer):
                code, _, _, confirm = self._run(interactive=True, answer=answer)
                confirm.assert_called_once()
                self.assertEqual(code, 0)

    def test_any_other_answer_cancels_and_changes_nothing(self) -> None:
        for answer in ("", "n", "N", "no", "maybe", "\n"):
            with self.subTest(answer=answer):
                before = tree_hash(Path(self._tmp.name))
                code, out, _, _ = self._run(interactive=True, answer=answer)
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(out)[0]["error"], "installation cancelled")
                self.assertEqual(tree_hash(Path(self._tmp.name)), before)

    def test_eof_and_interrupt_count_as_no(self) -> None:
        for exc in (EOFError, KeyboardInterrupt):
            with self.subTest(exc=exc.__name__):
                before = tree_hash(Path(self._tmp.name))
                with mock.patch.object(coacus_install, "_confirm", side_effect=exc), \
                        mock.patch.object(coacus_install, "_is_interactive", return_value=True), \
                        mock.patch.dict(os.environ, self.env, clear=True), \
                        mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                        contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
                    code = coacus_install.main(
                        ["codex", "--config-dir", str(self.config), "--skills", "using-coacus",
                         "--agents", "general", "--browser-policy", "off", "--force"], REPO)
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(out.getvalue())[0]["error"], "installation cancelled")
                self.assertEqual(tree_hash(Path(self._tmp.name)), before)

    def test_no_ask_policy_means_no_prompt_and_no_warning(self) -> None:
        (self.policies / "a.policy.json").unlink()
        code, out, err, confirm = self._run(interactive=True, answer="n")
        confirm.assert_not_called()
        self.assertNotIn("will not prompt", err)
        self.assertNotIn("ask_warnings", json.loads(out)[0])
        self.assertEqual(code, 0)

    def test_stdout_stays_a_single_json_document(self) -> None:
        _, out, _, _ = self._run(interactive=False)
        json.loads(out)

    def test_verify_reports_the_warning_without_changing_the_exit_code(self) -> None:
        self._run(["--yes"], interactive=False)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = coacus_install.main(["codex", "--config-dir", str(self.config), "--verify"], REPO)
        report = json.loads(out.getvalue())
        self.assertIn("ask_warnings", report[0])
        self.assertEqual(code, 0 if all(item.get("ok") for item in report) else 1)

    def test_verify_with_a_malformed_policy_file_still_prints_json(self) -> None:
        (self.policies / "bad.policy.json").write_text(
            json.dumps({"schema": 1, "enabled": True, "policies": None}), encoding="utf-8")
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(coacus_install, "_home", return_value=Path(self._tmp.name) / "home"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            coacus_install.main(["codex", "--config-dir", str(self.config), "--verify"], REPO)
        json.loads(out.getvalue())


if __name__ == "__main__":
    unittest.main()
