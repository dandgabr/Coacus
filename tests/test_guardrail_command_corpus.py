"""Regression corpus for how deny rules read shell commands.

A deny rule with ``"match": "command"`` must see the executable a command line
would run, through wrappers, ``sh -c`` strings, command substitution, pipes and
symlinks, and must not fire on a mere mention of the name. These tests lock the
current behaviour of ``engine/guardrail/evaluate.py`` so a change cannot weaken a
deny rule unnoticed.

Only deny rules are covered. The shapes in ``KNOWN_BYPASSES`` are real gaps found
by measuring the evaluator. Each is pinned to today's result (``allow``), so the
suite stays green now and fails the moment a shape is fixed; the failure message
says to move the shape into ``MUST_MATCH``. They are plain assertions rather than
``expectedFailure`` marks because that mark also hides a crash. Two end-to-end
tests assert the JSON the guard prints, because the guard always exits with code
0 and the exit code proves nothing.

``tool.post`` is never evaluated by the guard today; nothing here relies on it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.guardrail import evaluate as guard

REPO = Path(__file__).resolve().parents[1]
GUARD_CLI = REPO / "scripts/coacus_guard.py"

# A neutral binary name, so no real tool is mentioned.
TARGET = "blockedbin"

POLICY = {
    "id": "no-blockedbin",
    "action": {"verb": "exec", "resource": TARGET, "match": "command"},
    "decision": "deny",
    "on_ask_unavailable": "deny",
    "message": "blocked by the corpus policy",
}

# Command lines that must resolve to the target executable.
MUST_MATCH = {
    "plain": f"{TARGET} --flag",
    "absolute path": f"/usr/bin/{TARGET}",
    "env wrapper": f"env FOO=1 {TARGET}",
    "assignment prefix": f"FOO=1 {TARGET}",
    "sudo with option value": f"sudo -u root {TARGET}",
    "nohup": f"nohup {TARGET} &",
    "command builtin": f"command {TARGET}",
    "exec builtin": f"exec {TARGET}",
    "time": f"time {TARGET}",
    "sh -c": f"sh -c '{TARGET} --flag'",
    "bash -lc": f'bash -lc "{TARGET}"',
    "dollar substitution": f"echo $({TARGET})",
    "backtick substitution": f"echo `{TARGET}`",
    "nested dollar substitution": f"echo $(echo $({TARGET}))",
    "second stage of a pipe": f"echo hi | {TARGET}",
    "after and": f"true && {TARGET}",
    "after semicolon": f"true; {TARGET}",
    "after newline": f"true\n{TARGET}",
    "parenthesised": f"({TARGET})",
    "quoted name": f"'{TARGET}'",
    "backslash name": f"\\{TARGET}",
    "xargs": f"echo x | xargs {TARGET}",
    "setsid": f"setsid {TARGET}",
    "doas": f"doas {TARGET}",
    "timeout with duration": f"timeout 5 {TARGET}",
    "nice with value": f"nice -n 5 {TARGET}",
    "stdbuf": f"stdbuf -oL {TARGET}",
    "wrapper chain": f"sudo env FOO=1 nohup {TARGET}",
    "zsh -c": f"zsh -c '{TARGET}'",
    "dash -c": f"dash -c '{TARGET}'",
    "sh with combined flags": f"sh -ec '{TARGET}'",
    "flatpak run": f"flatpak run {TARGET}",
    "brace group": "{ " + TARGET + "; }",
    "process substitution in": f"cat <({TARGET})",
    "process substitution out": f"tee >({TARGET})",
    "eval": f"eval {TARGET}",
    "eval quoted": f"eval '{TARGET} --flag'",
    "here-string": f"bash <<< {TARGET}",
    "here-string quoted": f"bash <<< '{TARGET} --flag'",
    "find -exec": f"find . -exec {TARGET} ;",
    "find -execdir with placeholder": f"find . -execdir {TARGET} {{}} +",
    "env -S": f"env -S '{TARGET} --flag'",
    "env --split-string": f"env --split-string='{TARGET}'",
    "if condition": f"if {TARGET}; then true; fi",
    "then branch": f"if true; then {TARGET}; fi",
    "negation": f"! {TARGET}",
    "while condition": f"while {TARGET}; do true; done",
    "function body": f"f(){{ {TARGET}; }}; f",
    "coproc": f"coproc {TARGET}",
    "variable indirection": f"x={TARGET}; $x",
    "ansi-c quoting": f"$'{TARGET}' --flag",
    "ansi-c quoting in sh -c": f"bash -c $'{TARGET}'",
    "brace expansion": "{" + TARGET + ",}",
    "pipe into a bare shell": f"echo {TARGET} | sh",
    "sh -c with double dash": f"bash -c -- {TARGET}",
    "sudo then sh -c": f"sudo sh -c '{TARGET} --flag'",
    "nohup then bash -c": f"nohup bash -c '{TARGET} --flag'",
    "many sudo options": f"sudo -u root -g wheel -E {TARGET}",
    "leading redirection": f">/dev/null {TARGET}",
    "leading fd redirection": f"2>&1 {TARGET}",
    "leading input redirection": f"<in {TARGET}",
    "busybox sh": f"busybox sh -c {TARGET}",
    "busybox applet": f"busybox {TARGET}",
    "builtin exec": f"builtin exec {TARGET}",
    "su -c": f"su -c {TARGET}",
    "runuser": f"runuser -u someone -- {TARGET}",
    "watch": f"watch {TARGET}",
    "command substitution inside sh -c": f'sh -c "$(echo {TARGET})"',
    "multi-line sh -c argument": f"sh -c 'echo x\n{TARGET}'",
    "heredoc into a shell": f"sh <<EOF\n{TARGET}\nEOF",
    "source of a process substitution": f". <(echo {TARGET})",
    "source of stdin": f"source /dev/stdin <<EOF\n{TARGET}\nEOF",
    "function keyword definition": f"function f {{ {TARGET}; }}; f",
    "env with a combined -S option": f"env -vS'{TARGET}'",
    "env with a split option and value": f"env -S '{TARGET} --flag'",
    "apostrophe in a heredoc body": f"cat <<EOF\nIt's here\nEOF\n{TARGET}",
    "marker inside double quotes": f'echo "<<X"\n{TARGET}',
    "shift operator in arithmetic": f"echo $((1<<X))\n{TARGET}",
    "quoted heredoc tag": f"cat <<'EOF'\nbody\nEOF\n{TARGET}",
    "escaped heredoc tag": f"cat <<E\\OF\nbody\nEOF\n{TARGET}",
    "absolute shell heredoc": f"/bin/bash <<EOF\n{TARGET}\nEOF",
    "bash -s from a pipe": f"echo {TARGET} | bash -s",
    "bash dash from a pipe": f"echo {TARGET} | bash -",
    "sudo -s": f"echo {TARGET} | sudo -s",
    "xargs replace into sh": f"echo {TARGET} | xargs -I{{}} sh -c '{{}}'",
    "expansion inside the word": "blocked${x}bin",
    "command substitution inside the word": "blocked$(true)bin",
    "backtick inside the word": "blocked`true`bin",
    "glob star": "/usr/bin/blocked*",
    "glob question mark": "blockedbi?",
    "line continuation": "blocked\\\nbin",
    "append assignment prefix": f"A+=1 {TARGET}",
    "array assignment prefix": f"a[0]=x {TARGET}",
    "nested parens in a quoted substitution": f'echo "$( ({TARGET}) )"',
    "watch with a string": f"watch '{TARGET} -a'",
    "script with a string": f"script -qc '{TARGET}'",
    "chroot": f"chroot /srv {TARGET}",
    "strace": f"strace -f {TARGET}",
    "comment hides a heredoc marker": f"echo hi # <<EOF\n{TARGET}\nEOF",
    "comment hides a heredoc after git": f"git status # <<EOF\n{TARGET}\nEOF",
    "nice with many options": f"nice -n 1 -n 1 -n 1 -n 1 -n 1 -n 1 -n 1 -n 1 -n 1 {TARGET}",
    "env with many unsets": "env " + "-u A " * 12 + TARGET,
    "timeout with many options": "timeout -s KILL -k 1 --preserve-status --foreground -v -v -v -v -v 5 " + TARGET,
    "xargs with many options": "xargs -0 -n 1 -P 1 -r -t -L 1 -t -t -t -t -t " + TARGET,
    "trap on exit": f"trap '{TARGET}' EXIT; true",
    "trap on debug": f"trap {TARGET} DEBUG",
    "flock with a command string": f"flock /tmp/l -c 'true; {TARGET}'",
    "bash -o posix from a pipe": f"echo {TARGET} | bash -o posix",
    "bash +o posix from a pipe": f"echo {TARGET} | bash +o posix",
    "bash -O extglob from a pipe": f"echo {TARGET} | bash -O extglob",
    "BASH_ENV from a process substitution": f"BASH_ENV=<(echo {TARGET}) bash -c true",
    "case pattern inside a substitution": f'echo "$(case x in x) {TARGET};; esac)"',
    "quote inside a nested heredoc": f'echo "$(cat <<\'EOF\'\n"\nEOF\n)"\n{TARGET}\ntrue "',
    "ansi-c heredoc tag": f"cat <<$'EOF'\nEOF\n{TARGET}\n$EOF",
    "alias then use": f"shopt -s expand_aliases\nalias q={TARGET}\nq",
    "hash -p": f"hash -p /path/{TARGET} ls; ls",
    "mapfile callback": f"mapfile -C {TARGET} -c 1 x <<< a",
    "named coproc": f"coproc X {{ {TARGET}; }}",
    "su --command": f"su --command={TARGET}",
    "script --command": f"script --command={TARGET} /dev/null",
    "bash --rcfile": f"bash --rcfile <(echo {TARGET}) -i",
    "at job from a pipe": f"echo {TARGET} | at now",
    "batch job from a pipe": f"echo {TARGET} | batch",
    "gnu parallel": f"parallel ::: {TARGET}",
}

# Command lines that only mention the name and must not match.
MUST_NOT_MATCH = {
    "grep argument": f"grep {TARGET} notes.txt",
    "commit message": f'git commit -m "{TARGET}"',
    "echo argument": f"echo {TARGET}",
    "similar name": f"{TARGET}-helper --flag",
    "redirect target": f"echo x > {TARGET}",
    "redirect source": f"cat < {TARGET}",
    "here-string to cat": f"cat <<< {TARGET}",
    "eval echo": f"eval echo {TARGET}",
    "env -S echo": f"env -S 'echo {TARGET}'",
    "find -name": f"find . -name {TARGET}",
    "find -name with other exec": f"find . -name {TARGET} -exec ls {{}} ;",
    "if branch echo": f"if true; then echo {TARGET}; fi",
    "here-string echo": f"bash <<< 'echo {TARGET}'",
    "multi-line commit message": "git commit -m 'a\n\nb'",
    "heredoc commit message": f"git commit -m \"$(cat <<'EOF'\nsubject\n\n{TARGET} is banned\nEOF\n)\"",
    "heredoc into cat": f"cat <<EOF\n{TARGET} is banned\nEOF",
    "variable braces as an argument": f"echo ${{HOME}} {TARGET}",
    "home-relative command path": f"$HOME/.local/bin/tool --{TARGET}",
    "test builtin": f"[ -f {TARGET} ] && echo ok",
    "bash with a script file": f"bash scripts/run.sh {TARGET}",
    "heredoc into cat with an apostrophe": f"cat <<EOF\nIt's {TARGET}\nEOF",
    "heredoc commit message with one double quote": "git commit -m \"$(cat <<'EOF'\nsubject\n\n5\" disks\nEOF\n)\"",
    "python heredoc with an apostrophe": "python3 - <<'EOF'\n# don't panic\nx = [1]\nEOF",
    "command -v lookup": f"command -v {TARGET}",
    "empty": "",
    "blank": "   ",
}

# Mentions that a command deny rule wrongly matches today (a false positive): the
# wrapper scan reads arguments. Pinned to today's result; when fixed, move to
# MUST_NOT_MATCH.
KNOWN_FALSE_POSITIVES = {
    "sudo grep argument": f"sudo grep {TARGET} notes",
    "xargs grep argument": f"echo x | xargs grep {TARGET}",
}

# Shapes measured as NOT caught today. Each one is a bypass of a command deny rule.
KNOWN_BYPASSES: dict[str, str] = {
    # Nothing is known to slip through at the moment. A shape found later is added
    # here, pinned to "allow", until it is fixed and moved into MUST_MATCH.
}


def names(command: str) -> list[str]:
    return guard.command_candidates(command)


class TestCommandCorpus(unittest.TestCase):
    def test_golden_positives_resolve_to_the_target(self) -> None:
        for label, command in MUST_MATCH.items():
            with self.subTest(label=label):
                found, unresolved = guard.resolve_command(command)
                self.assertTrue(TARGET in found or unresolved, command)
                self.assertEqual(guard.evaluate([POLICY], "exec", command)["decision"], "deny")

    def test_golden_negatives_do_not_match(self) -> None:
        for label, command in MUST_NOT_MATCH.items():
            with self.subTest(label=label):
                self.assertNotIn(TARGET, names(command))
                self.assertEqual(guard.evaluate([POLICY], "exec", command)["decision"], "allow")

    def test_symlink_to_the_target_is_resolved(self) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks are not available on this platform")
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / TARGET
            real.write_text("", encoding="utf-8")
            link = Path(tmp) / "harmless-name"
            try:
                link.symlink_to(real)
            except OSError:
                self.skipTest("symlinks cannot be created here")
            self.assertIn(TARGET, names(str(link)))

    def test_oversize_command_is_still_read(self) -> None:
        # No timing assertion, so the test cannot flake.
        huge = "echo " + "a" * 90_000 + f" | {TARGET}"
        self.assertIn(TARGET, names(huge))

    def test_unbalanced_quotes_are_still_read(self) -> None:
        # An unparseable line is unresolved, so a command policy fails closed on it.
        found, unresolved = guard.resolve_command(f"{TARGET} 'unterminated")
        self.assertIn(TARGET, found)
        self.assertTrue(unresolved)
        self.assertEqual(guard.evaluate([POLICY], "exec", "echo 'unterminated")["decision"], "deny")

    def test_non_command_policy_still_matches_the_whole_string(self) -> None:
        plain = {**POLICY, "action": {"verb": "exec", "resource": f"*{TARGET}*"}}
        self.assertEqual(guard.evaluate([plain], "exec", f"grep {TARGET} notes.txt")["decision"], "deny")


class TestKnownGaps(unittest.TestCase):
    """Pin today's wrong answers so a fix is noticed and a crash still fails."""

    def _decision(self, command: str) -> str:
        return guard.evaluate([POLICY], "exec", command)["decision"]

    def test_every_known_bypass_is_still_allowed(self) -> None:
        for label, command in KNOWN_BYPASSES.items():
            with self.subTest(label=label):
                self.assertEqual(
                    self._decision(command), "allow",
                    f"{label!r} is now denied: move it from KNOWN_BYPASSES into MUST_MATCH",
                )

    def test_every_known_false_positive_is_still_denied(self) -> None:
        for label, command in KNOWN_FALSE_POSITIVES.items():
            with self.subTest(label=label):
                self.assertEqual(
                    self._decision(command), "deny",
                    f"{label!r} is now allowed: move it from KNOWN_FALSE_POSITIVES into MUST_NOT_MATCH",
                )

    def test_the_gap_lists_do_not_overlap_the_golden_sets(self) -> None:
        gaps = set(KNOWN_BYPASSES.values()) | set(KNOWN_FALSE_POSITIVES.values())
        self.assertFalse(gaps & (set(MUST_MATCH.values()) | set(MUST_NOT_MATCH.values())))


class TestGuardEndToEnd(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        policies = self.root / "methodology/lifecycle/policies"
        policies.mkdir(parents=True)
        document = {"schema": 1, "enabled": True, "policies": [POLICY]}
        (policies / "corpus.policy.json").write_text(json.dumps(document), encoding="utf-8")

    def _run(self, command: str) -> tuple[dict, int]:
        env = {key: value for key, value in os.environ.items()
               if key not in ("COACUS_POLICY_DIR", "CI", "COACUS_GUARD_ASK", "COACUS_GUARD_NO_ASK")}
        env["COACUS_POLICY_DIR"] = str(self.root / "no-user-policies")
        proc = subprocess.run(
            [sys.executable, str(GUARD_CLI), "--harness", "claude-code", "--event", "tool.pre",
             "--root", str(self.root)],
            input=json.dumps({"tool": "bash", "tool_input": {"command": command}}),
            capture_output=True, text=True, env=env, timeout=60,
        )
        return json.loads(proc.stdout.strip()), proc.returncode

    def test_a_wrapped_target_is_denied_in_the_printed_json(self) -> None:
        for label in ("sudo with option value", "sh -c", "dollar substitution", "second stage of a pipe"):
            with self.subTest(label=label):
                out, code = self._run(MUST_MATCH[label])
                self.assertEqual(code, 0)
                self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_a_mere_mention_is_allowed_in_the_printed_json(self) -> None:
        # The same policy denies the real command in this very root, so an empty
        # object here is an allow and not a guard that failed to load anything.
        denied, _ = self._run(MUST_MATCH["plain"])
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
        out, code = self._run(MUST_NOT_MATCH["commit message"])
        self.assertEqual(code, 0)
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
