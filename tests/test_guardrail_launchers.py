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


# Shapes a security review found slipping through: option clusters, attached values, other
# separators and long option lists. The ones in REVIEW_RUN were run for real.
REVIEW_RUN = {
    "socat SHELL": "socat - SHELL:{T}", "git ls-remote --upload-pack=": "git ls-remote --upload-pack={T} .",
    "ssh -o with a space": "ssh -o 'ProxyCommand {T}' h",
    "ssh -o spaced equals": "ssh -o 'ProxyCommand = {T}' h", "ssh -vo cluster": "ssh -vo ProxyCommand={T} h",
}
REVIEW_DOCUMENTED = {
    "ssh -4o attached": "ssh -4oProxyCommand={T} h", "ssh LocalCommand": "ssh -o LocalCommand={T} h",
    "scp -S": "scp -S {T} a h:b", "scp -qS cluster": "scp -qS {T} a h:b", "scp -S attached": "scp -S{T} a h:b",
    "sftp -D": "sftp -D {T} h", "sftp -S": "sftp -S {T} h",
    "rsync -avze cluster": "rsync -avze {T} a h:b", "rsync -e attached": "rsync -e{T} a h:b",
    "rsync --rsh=": "rsync --rsh={T} a h:b", "rsync --rsh": "rsync --rsh {T} a h:b",
    "git clone -u": "git clone -u {T} /tmp/r d", "git clone --upload-pack": "git clone --upload-pack {T} /tmp/r d",
    "git push --receive-pack=": "git push --receive-pack={T} u",
    "git -c filter smudge": "git -c filter.x.smudge={T} checkout", "git -c merge driver": "git -c merge.x.driver={T} merge b",
    "git -c difftool cmd": "git -c difftool.x.cmd={T} difftool", "git -c core.gitProxy": "git -c core.gitProxy={T} fetch u",
    "git -c sendmailcmd": "git -c sendemail.sendmailcmd={T} send-email", "git -ckey attached": "git -ccore.pager={T} log",
    "git rebase -x attached": "git rebase -x{T} HEAD~1", "git filter-branch": "git filter-branch --tree-filter {T} HEAD",
    "GIT_PROXY_COMMAND": "GIT_PROXY_COMMAND={T} git fetch git://h/r", "export GIT_PAGER": "export GIT_PAGER={T}; git log",
    "export SUDO_EDITOR": "export SUDO_EDITOR={T}", "SYSTEMD_PAGER": "SYSTEMD_PAGER={T} systemctl status x",
    "entr -s": "entr -s '{T} a'", "watchexec string": "watchexec -e py '{T} a'", "concurrently strings": "concurrently '{T} a' 'b c'",
    "runuser -c": "runuser -l root -c '{T} a'", "parallel string": "parallel '{T} {{}}' ::: 1",
    "tmux -c": "tmux -c {T}", "tmux display-popup": "tmux display-popup -E {T}", "i3-msg quoted": "i3-msg 'exec {T}'",
    "npx --call": "npx --call='{T} a'", "npm exec --call": "npm exec --call={T}",
    "sg group command": "sg wheel {T}", "sg quoted": "sg wheel '{T} a'",
}
# Commands the walk cannot read: they must be denied, whatever the target.
REVIEW_UNRESOLVED = {
    "git --config-env": "V={T} git --config-env=core.pager=V log",
    "GIT_CONFIG_COUNT": "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.pager GIT_CONFIG_VALUE_0={T} git log",
    "export GIT_CONFIG_PARAMETERS": "export GIT_CONFIG_PARAMETERS=x",
}
# Long option lists must not push the real option out of view.
PADDED = {
    "git -c": lambda n: "git " + "-c a.b=1 " * n + "-c core.pager={T} log",
    "git rebase -x": lambda n: "git " + "-c a.b=1 " * n + "rebase -x {T} HEAD~1",
    "ssh -o": lambda n: "ssh " + "-v " * n + "-o ProxyCommand={T} h",
    "socat": lambda n: "socat " + "-d " * n + "- EXEC:{T}",
    "scp -S": lambda n: "scp " + "-q " * n + "-S {T} a h:b",
    "rsync -e": lambda n: "rsync " + "-v " * n + "-e {T} a h:b",
}
NEW_MENTIONS = [
    "ssh -o 'ProxyCommand ssh -W %h:%p jump' h", "scp -S ssh a {T}:b", "rsync -e ssh a {T}:b",
    "git log -x rebase {T}", "git -c user.name={T} commit -m x", "git clone https://example.com/{T}.git",
    "sg wheel ls", "export PATH=/usr/bin:$PATH", "export {T}_HOME=/x", "i3-msg 'workspace 2'",
    "socat - TCP:{T}:80", "tmux new -s work", "entr -s 'make'", "git push -u origin main",
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


class TestReviewFindings(unittest.TestCase):
    def test_option_forms_a_review_found_are_looked_through(self) -> None:
        for group in (REVIEW_RUN, REVIEW_DOCUMENTED):
            for label, template in group.items():
                with self.subTest(shape=label):
                    self.assertTrue(denied(template.format(T=TARGET)))

    def test_unreadable_config_routes_fail_closed(self) -> None:
        for label, template in REVIEW_UNRESOLVED.items():
            with self.subTest(shape=label):
                self.assertTrue(guard.resolve_command(template.format(T=TARGET))[1])
                self.assertTrue(denied(template.format(T=TARGET)))

    def test_long_option_lists_do_not_hide_the_option(self) -> None:
        for label, build in PADDED.items():
            for count in (5, 40, 100):
                with self.subTest(shape=label, count=count):
                    self.assertTrue(denied(build(count).format(T=TARGET)))

    def test_every_table_entry_is_looked_through(self) -> None:
        for name in sorted(guard._WRAPPERS - {"exec", "command", "builtin", "time", "script", "watch"}):
            with self.subTest(wrapper=name):
                self.assertIn(TARGET, guard.resolve_command(f"{name} {TARGET}")[0])
        for name, triggers in sorted(guard._TRIGGERED.items()):
            for trigger in sorted(triggers):
                with self.subTest(launcher=name, trigger=trigger):
                    self.assertTrue(denied(f"{name} {trigger} {TARGET}"))
        for name in sorted(guard._COMMAND_VARS):
            with self.subTest(variable=name):
                self.assertTrue(denied(f"{name}={TARGET} true"))

    def test_deep_and_wide_trigger_input_fails_closed_on_the_trigger_path(self) -> None:
        for head in ("pnpm exec", "tmux new", "uv run"):
            wide = head + " " + " ".join(["a"] * 200) + " " + TARGET
            with self.subTest(head=head, shape="wide"):
                self.assertTrue(denied(wide))
        nested = TARGET
        for _ in range(guard._MAX_DEPTH + 4):
            nested = "pnpm exec sh -c '" + nested.replace("'", "'\\''") + "'"
        self.assertTrue(denied(nested))
        chained = "pnpm exec " * (guard._MAX_DEPTH + 4) + TARGET
        self.assertTrue(denied(chained))
        too_deep = "pnpm exec " * (guard._MAX_DEPTH + 4) + "echo hi"
        self.assertTrue(guard.resolve_command(too_deep)[1])
        late_trigger = "pnpm " + "--silent " * 80 + "exec " + TARGET
        self.assertTrue(denied(late_trigger))
        wide_git = "git rebase -x " + " ".join(["a"] * 200) + " " + TARGET
        self.assertTrue(denied(wide_git))

    def test_new_branches_do_not_turn_mentions_into_matches(self) -> None:
        for template in NEW_MENTIONS:
            with self.subTest(command=template):
                self.assertFalse(denied(template.format(T=TARGET)))

    def test_a_non_ssh_command_ignores_ssh_option_words(self) -> None:
        self.assertFalse(denied("echo -o ProxyCommand=" + TARGET))
        self.assertFalse(denied("grep -S " + TARGET + " notes"))


if __name__ == "__main__":
    unittest.main()
