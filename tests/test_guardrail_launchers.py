"""Programs that run another program from their arguments or environment.

A command deny rule must look through them. Each shape below was measured against the
walk before it was added; the ones in ``CONFIRMED`` were also run for real and did
execute the target. A mere mention of the name must still pass.
"""

from __future__ import annotations

import unittest

from engine.guardrail import evaluate as guard

TARGET = "blockedbin"
POLICY = {"id": "no-blockedbin", "action": {"verb": "exec", "resource": TARGET, "match": "command"},
          "decision": "deny"}

# Shapes run for real: the target executed.
CONFIRMED = {
    "pnpm exec": "pnpm exec {T}", "uv run": "uv run {T}", "tmux new-session": "tmux new-session -d '{T}'",
    "git rebase -x": "git rebase -x {T} HEAD~1", "git -c core.sshCommand": "git -c core.sshCommand={T} fetch u",
    "dbus-launch": "dbus-launch {T}", "setarch": "setarch x86_64 {T}", "linux64": "linux64 {T}",
    "systemd-cat": "systemd-cat {T}", "socat EXEC": "socat - EXEC:{T}", "sshpass": "sshpass -p x {T}",
    "GIT_SSH_COMMAND": "GIT_SSH_COMMAND={T} git fetch u", "ssh ProxyCommand": "ssh -o ProxyCommand={T} h",
    "rsync -e": "rsync -e {T} a h:b", "git bisect run": "git bisect run {T}",
}
# Shapes the tool documents as running a command; not executed here.
DOCUMENTED = {
    "npx": "npx {T}", "npm exec": "npm exec -- {T}", "yarn exec": "yarn exec {T}", "pipx run": "pipx run {T}",
    "uvx": "uvx {T}", "poetry run": "poetry run {T}", "bundle exec": "bundle exec {T}", "mise exec": "mise exec -- {T}",
    "nix-shell --run": "nix-shell --run '{T}'", "gdb --args": "gdb -batch -ex run --args {T}",
    "xterm -e": "xterm -e {T}", "gnome-terminal --": "gnome-terminal -- {T}", "kitty": "kitty {T}",
    "screen": "screen -dm {T}", "fd -x": "fd -x {T}", "i3-msg exec": "i3-msg exec {T}",
    "valgrind": "valgrind {T}", "pkexec": "pkexec {T}", "faketime": "faketime now {T}", "sg -c": "sg users -c '{T}'",
    "start-stop-daemon": "start-stop-daemon --start --exec {T}", "git submodule foreach": "git submodule foreach {T}",
    "git difftool -x": "git difftool -x {T}", "git rebase --exec=": "git rebase --exec={T} HEAD~1",
    "GIT_PAGER": "GIT_PAGER={T} git log", "EDITOR": "EDITOR={T} git commit -e", "nested": "npx npx {T}",
    "under sudo": "sudo tmux new-session -d {T}",
}
MENTIONS = [
    "npm install {T}", "npm run build {T}", "git commit -m {T}", "git log --grep {T}",
    "git -c user.name={T} commit -m x", "tmux send-keys -t 1 x", "rsync -av a {T}:b", "xterm -T {T}",
    "EDITOR=vim git commit", "git rebase -i HEAD~2", "uv pip install {T}", "gem install {T}",
    "fd {T}", "rg {T} src", "echo {T} | tee x", "ssh host {T}",
]


def denied(command: str) -> bool:
    return guard.evaluate([POLICY], "exec", command)["decision"] == "deny"


class TestLaunchers(unittest.TestCase):
    def test_confirmed_launchers_are_looked_through(self) -> None:
        for label, template in CONFIRMED.items():
            with self.subTest(launcher=label):
                self.assertTrue(denied(template.format(T=TARGET)))

    def test_documented_launchers_are_looked_through(self) -> None:
        for label, template in DOCUMENTED.items():
            with self.subTest(launcher=label):
                self.assertTrue(denied(template.format(T=TARGET)))

    def test_a_mention_beside_a_launcher_is_still_allowed(self) -> None:
        for template in MENTIONS:
            command = template.format(T=TARGET)
            with self.subTest(command=command):
                self.assertFalse(denied(command))

    def test_a_launcher_inside_a_shell_wrapper_is_still_found(self) -> None:
        for template in ("sh -c 'npx {T}'", "echo $(uv run {T})", "true && pnpm exec {T}", "env X=1 tmux new -d {T}"):
            with self.subTest(command=template):
                self.assertTrue(denied(template.format(T=TARGET)))

    def test_deep_launcher_nesting_fails_closed(self) -> None:
        command = "npx " * (guard._MAX_DEPTH + 4) + TARGET
        self.assertTrue(denied(command))

    def test_many_words_after_a_trigger_fail_closed(self) -> None:
        self.assertTrue(denied("npx " + " ".join(["a"] * 200) + " " + TARGET))


if __name__ == "__main__":
    unittest.main()
