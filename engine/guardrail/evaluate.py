"""Evaluate PAER guardrail policies against a canonical action.

PAER = Policy over Action, Event binding, Rendering effect. This module is the
harness-agnostic core: a policy constrains an ACTION (`verb` + `resource`); the
event only decides WHEN the policy runs and whether a decision may bind.

Design notes (D4):
- Failure domains are split. `on_decision_failure` is the result when the
  evaluator ran but could not decide; `on_mechanism_failure` is the result when
  the guardrail process itself failed. A broken hook must not deny every call.
- `ask` on a harness/scope without a human channel degrades via
  `on_ask_unavailable` (never a global default).

The evaluator is deliberately small, deterministic and stdlib-only. It matches
resource patterns with `fnmatch` for read/write, and substring globs for the
other verbs. An `exec` policy may opt into ``"match": "command"`` to compare its
patterns with the executable names a shell string would run, rather than the
whole string (see :func:`command_candidates`).
"""

from __future__ import annotations

import fnmatch
import functools
import json
import os
import re
import shlex
import unicodedata
from pathlib import Path

EVENTS_PATH = "methodology/lifecycle/events.json"
# The canonical event ids; a test keeps this equal to events.json.
KNOWN_EVENTS = frozenset({
    "tool.pre", "prompt.submit", "turn.stop", "tool.post", "tool.failure",
    "session.start", "session.end", "context.precompact", "subagent.start", "subagent.stop",
})
ACTIONS_PATH = "methodology/lifecycle/actions.schema.json"
POLICIES_DIR = "methodology/lifecycle/policies"

DECISIONS = ("allow", "deny", "ask", "note")

_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]*\])?\+?=")
_SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish", "su", "sg"}
_WRAPPERS = {
    "env", "nohup", "setsid", "sudo", "doas", "timeout", "nice", "ionice", "stdbuf",
    "exec", "command", "time", "xvfb-run", "dbus-run-session", "systemd-run",
    "unbuffer", "chrt", "taskset", "flock", "script", "xargs",
    "busybox", "toybox", "builtin", "watch", "runuser", "chroot", "unshare",
    "nsenter", "strace", "ltrace", "setpriv", "prlimit", "bwrap", "firejail", "parallel",
    "pkexec", "run0", "fakeroot", "fakechroot", "faketime", "eatmydata", "torsocks",
    "proxychains", "proxychains4", "chronic", "catchsegv", "valgrind", "perf", "nsjail",
    "dbus-launch", "sshpass", "rlwrap", "setarch", "linux32", "linux64", "i386", "x86_64",
    "systemd-cat", "runcon", "cpulimit", "numactl", "screen", "dtach", "abduco", "entr",
    "watchexec", "kitty", "foot", "flatpak-spawn", "bunx", "npx", "uvx", "concurrently",
}
# Programs that run a command only after a given word or flag. Every word after the
# trigger is read as a command line, so ``npm exec -- NAME`` and ``xterm -e NAME`` match.
_TRIGGERED = {
    "npm": {"exec", "x"}, "pnpm": {"exec", "dlx", "x"}, "yarn": {"exec", "dlx"}, "bun": {"x"},
    "pipx": {"run"}, "uv": {"run"}, "poetry": {"run"}, "pipenv": {"run"}, "pdm": {"run"},
    "hatch": {"run"}, "conda": {"run"}, "mamba": {"run"}, "micromamba": {"run"},
    "bundle": {"exec"}, "rbenv": {"exec"}, "pyenv": {"exec"}, "asdf": {"exec"},
    "mise": {"exec", "x"}, "direnv": {"exec"}, "gem": {"exec"}, "guix": {"--"},
    "nix": {"run", "-c", "--command", "--"}, "nix-shell": {"--run", "--command"},
    "cargo": {"-s", "--shell"}, "nodemon": {"--exec", "-x"}, "fd": {"-x", "--exec", "-X", "--exec-batch"},
    "rg": {"--pre"}, "gdb": {"--args"}, "start-stop-daemon": {"--exec", "-x"},
    "i3-msg": {"exec"}, "swaymsg": {"exec"}, "hyprctl": {"exec"}, "xdotool": {"exec"},
    "tmux": {"new-session", "new", "new-window", "neww", "split-window", "splitw", "run-shell",
             "run", "respawn-pane", "respawn-window", "send-keys", "pipe-pane", "if-shell",
             "display-popup", "popup", "-c"},
    "wezterm": {"start", "--"},
    **{terminal: {"-e", "--", "-x", "--command", "--execute"} for terminal in (
        "xterm", "uxterm", "urxvt", "rxvt", "st", "alacritty", "konsole", "x-terminal-emulator",
        "terminator", "xfce4-terminal", "mate-terminal", "gnome-terminal", "tilix", "lxterminal")},
}
# ``git SUBCOMMAND`` words after which the rest is a command line (``git rebase -x NAME``).
_GIT_RUNNERS = {"rebase": {"-x", "--exec"}, "difftool": {"-x", "--extcmd"}, "bisect": {"run"},
                "submodule": {"foreach"},
                "filter-branch": {"--tree-filter", "--index-filter", "--msg-filter", "--env-filter",
                                  "--commit-filter", "--parent-filter", "--tag-name-filter"}}
# Variables whose value another program runs as a command.
_COMMAND_VARS = {
    "GIT_SSH_COMMAND", "GIT_SSH", "GIT_EXTERNAL_DIFF", "GIT_ASKPASS", "GIT_PAGER", "GIT_EDITOR",
    "GIT_SEQUENCE_EDITOR", "SSH_ASKPASS", "PAGER", "EDITOR", "VISUAL", "BROWSER", "LESSOPEN",
    "MANPAGER", "RSYNC_RSH", "SUDO_ASKPASS", "FCEDIT", "GIT_PROXY_COMMAND", "SUDO_EDITOR", "SYSTEMD_PAGER",
}
# ``git -c key=value`` keys whose value is a command line.
_GIT_COMMAND_KEY = re.compile(r"command|cmd|pager|editor|askpass|external|helper|program|textconv|fsmonitor|smudge|clean|process|driver|proxy|^alias\.")
_SSH_COMMAND_OPTION = re.compile(r"^(?:proxycommand|localcommand|knownhostscommand)(?:\s*=\s*|\s+)(.+)$", re.I | re.S)
# Wrappers whose argument is a whole command line in one quoted string.
_STRING_WRAPPERS = {"watch", "script", "entr", "watchexec", "concurrently", "runuser", "parallel"}
# Commands that only read a here-document as data. Any other reader (a shell,
# ``source``, ``eval``, an unknown program) has its body scanned like a script.
_DATA_READERS = {"cat", "tee", "git", "gh", "echo", "printf", "grep", "sed", "awk",
                 "wc", "sort", "head", "tail", "diff", "read", "uniq", "cut", "tr",
                 "psql", "mysql", "sqlite3", "jq", "ssh", "kubectl"}
# Interpreters read a here-document as their own language, not as shell.
_INTERPRETER = re.compile(r"^(?:python|node|nodejs|ruby|perl|php|lua|deno|bun)[\d.]*$")
_SCRIPT_WORD = re.compile(r"(?:^|[\s;&|(`])(?:\S*/)?(?:sh|bash|zsh|dash|ksh|source|eval|su|\.)(?=\s|$)")
_MAX_WORDS = 2000
_SAFE_PREFIX = re.compile(r"^(?:\$HOME|\$\{HOME\}|\$PWD|\$\{PWD\}|~)(?=/)")
_STEP_LIMIT = 5000
_LOOKAHEAD = 64
_STARTUP_VARS = {"BASH_ENV", "ENV", "PROMPT_COMMAND", "PS4", "LD_PRELOAD"}
_SHELL_OPTS_WITH_VALUE = {"-o", "+o", "-O", "+O"}
_SHELL_OPTS_RUNNING = {"--rcfile", "--init-file"}
_REDIRECT = re.compile(r"^\d*(?:>>?|<<?|>&|<&|&>)")
_BARE_REDIRECT = re.compile(r"^\d*(?:>>?|<|>&|<&|&>)$")
_KEYWORDS = {"{", "}", "if", "then", "elif", "else", "do", "while", "until", "!", "coproc"}
_FIND_EXEC = {"-exec", "-execdir", "-ok", "-okdir"}
_PROCESS_SUBST = {"<(", ">("}
_MAX_DEPTH = 8
_MAX_COMMAND_CHARS = 100_000


def load_events(root: Path) -> dict[str, dict]:
    """Load the canonical event taxonomy as ``{event_id: event}``."""
    path = root / EVENTS_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data.get("events", [])}


def user_policy_dir(env: dict | None = None, home: Path | None = None) -> Path:
    """Directory of machine-local policy files generated at install time.

    ``COACUS_POLICY_DIR`` overrides; otherwise ``$XDG_CONFIG_HOME/coacus/policies``
    or ``~/.config/coacus/policies``. These files are per-machine choices (for
    example the browsers an agent may drive) and never belong in the repository.
    """
    env = os.environ if env is None else env
    override = env.get("COACUS_POLICY_DIR")
    if override:
        return Path(override).expanduser()
    config = env.get("XDG_CONFIG_HOME")
    base = Path(config).expanduser() if config else (home or Path.home()) / ".config"
    return base / "coacus" / "policies"


def _load_dir(base: Path) -> list[dict]:
    """Load every enabled ``*.policy.json`` under ``base`` (missing dir -> none).

    One bad file, or one bad entry, is skipped on its own: it must never switch the
    other policies off. Only well-formed policy dictionaries are returned.
    """
    policies: list[dict] = []
    if not base.is_dir():
        return policies
    for path in sorted(base.glob("*.policy.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):  # includes JSONDecodeError and bad UTF-8
            continue
        if not isinstance(data, dict) or data.get("enabled") is not True:
            continue
        entries = data.get("policies")
        if not isinstance(entries, list):
            continue
        for policy in entries:
            if isinstance(policy, dict) and isinstance(policy.get("action"), dict):
                policies.append(policy)
    return policies


def load_policies(root: Path, include_user: bool = False, user_dir: Path | None = None) -> list[dict]:
    """Load every ACTIVE policy from ``methodology/lifecycle/policies/*.json``.

    A file is active only when it declares ``"enabled": true``. The shipped
    default set is empty and the reference file is disabled, so installing
    Coacus never changes a session's behaviour without an explicit opt-in (D2).

    With ``include_user`` the machine-local policies generated at install time
    (see :func:`user_policy_dir`) are appended. The runtime guard sets it; unit
    tests leave it off so they never depend on the developer's home directory.
    """
    policies = _load_dir(root / POLICIES_DIR)
    if include_user:
        policies.extend(_load_dir(user_dir or user_policy_dir()))
    return policies


def _star_match(pattern: str, value: str) -> bool:
    """Match ``pattern`` (only ``*`` is special, matching any run) against all of ``value``.

    A two-pointer scan that remembers only the last star, so the work is bounded
    by ``len(pattern) * len(value)`` and can never blow up on a hostile input.
    """
    p = v = 0
    star = -1
    mark = 0
    while v < len(value):
        if p < len(pattern) and pattern[p] == "*":
            star, mark = p, v
            p += 1
        elif p < len(pattern) and pattern[p] == value[v]:
            p += 1
            v += 1
        elif star != -1:
            mark += 1
            v = mark
            p = star + 1
        else:
            return False
    while p < len(pattern) and pattern[p] == "*":
        p += 1
    return p == len(pattern)


def _plain_match(pattern: str, value: str) -> bool:
    """The matching rules of :func:`_resource_matches` without the newline allowance."""
    if pattern in ("", "*") or fnmatch.fnmatch(value, pattern):
        return True
    if "*" in pattern:
        return _star_match(pattern, value)
    return pattern in value


def _resource_matches(pattern: str, value: str) -> bool:
    """Match a resource pattern against a concrete resource value.

    A value longer than the command cap matches every pattern (fail closed), so a
    huge input can neither stall the matcher nor slip past a rule. One trailing
    newline is ignored, as the earlier regex form did.
    """
    if pattern in ("", "*"):
        return True
    if len(value) > _MAX_COMMAND_CHARS:
        return True
    if value.endswith("\n") and _plain_match(pattern, value[:-1]):
        return True
    if fnmatch.fnmatch(value, pattern):
        return True
    # Substring form for command/host patterns (e.g. "git push*--force*").
    if "*" in pattern:
        return _star_match(pattern, value)
    return pattern in value


def _names(word: str) -> list[str]:
    """Candidate executable names for one command word (basename + symlink target)."""
    names = [os.path.basename(word)]
    if os.sep in word:
        try:
            real = os.path.realpath(os.path.expanduser(word))
        except OSError:
            real = word
        if real != word:
            names.append(os.path.basename(real))
    return [name for name in names if name]


def _heredoc_tag(text: str, index: int) -> tuple[str, int]:
    """Read a here-document tag starting at ``index``; return ``(tag, next_index)``.

    Quotes and backslashes are dropped from the tag, as the shell does, and the tag
    ends at whitespace or an operator character.
    """
    while index < len(text) and text[index] in " \t":
        index += 1
    if text.startswith("$'", index) or text.startswith('$"', index):
        index += 1  # $'EOF' is the tag EOF
    tag: list[str] = []
    quote = ""
    while index < len(text):
        ch = text[index]
        if quote:
            if ch == quote:
                quote = ""
            else:
                tag.append(ch)
        elif ch in "'\"":
            quote = ch
        elif ch == "\\" and index + 1 < len(text):
            index += 1
            tag.append(text[index])
        elif ch in " \t\n;&|<>()":
            break
        else:
            tag.append(ch)
        index += 1
    return "".join(tag), index


def _reads_as_script(line: str) -> bool:
    """True when the program that reads a here-document on ``line`` may run it."""
    if _SCRIPT_WORD.search(line):
        return True
    head = re.match(r"\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*([^\s;&|()<>]+)", line)
    if not head:
        return True
    name = os.path.basename(head.group(1))
    return name not in _DATA_READERS and not _INTERPRETER.match(name)


def _match_paren(command: str, start: int) -> int:
    """Index just past the ``)`` that closes a ``$(`` whose body starts at ``start``.

    Quotes, nested ``$(`` and here-documents inside the substitution are skipped the
    way the shell skips them, so a quote or a ``<<`` in the body cannot confuse the
    caller. Returns -1 when the substitution is never closed.
    """
    index, size, depth = start, len(command), 1
    quote = ""
    pending: list[tuple[str, bool]] = []
    while index < size:
        ch = command[index]
        if ch == "\\" and quote != "'":
            index += 2
            continue
        if quote:
            if ch == quote:
                quote = ""
            elif ch == "$" and quote == '"' and command.startswith("$(", index):
                end = _match_paren(command, index + 2)
                if end < 0:
                    return -1
                index = end
                continue
            index += 1
            continue
        if ch in "'\"":
            quote = ch
        elif command.startswith("$(", index):
            depth += 1
            index += 2
            continue
        elif command.startswith("<<", index) and not command.startswith("<<<", index):
            strip = command.startswith("<<-", index)
            tag, index = _heredoc_tag(command, index + (3 if strip else 2))
            if tag:
                pending.append((tag, strip))
            continue
        elif ch == "\n" and pending:
            index += 1
            for tag, strip in pending:
                while index < size:
                    end = command.find("\n", index)
                    end = size if end == -1 else end
                    text = command[index:end]
                    index = end + 1
                    if (text.lstrip("\t") if strip else text) == tag:
                        break
            pending = []
            continue
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return -1


def _logical_lines(command: str, state: dict | None = None) -> list[str]:
    """Split on newlines that are outside quotes, handling here-documents.

    A quoted argument that spans lines stays on one line, so it parses. A here-document
    is detected where the shell detects it (outside quotes, comments and arithmetic,
    with the tag read the way the shell reads it), and its body is consumed before any
    quote tracking, so an apostrophe in the body cannot swallow the commands after it.
    The body is data for a known data reader and a script for anything else. A command
    substitution is skipped as a unit, so quotes inside it do not leak into the outer
    quote state. A comment is dropped up to the end of its line.
    """
    command = command.replace("\\\n", "")  # line continuation
    lines: list[str] = []
    current: list[str] = []
    pending: list[tuple[str, bool]] = []
    quote = ""
    arith = 0
    index, size = 0, len(command)
    while index < size:
        ch = command[index]
        if ch == "\\" and quote != "'" and index + 1 < size:
            current.append(ch + command[index + 1])
            index += 2
            continue
        if quote == "'":
            if ch == "'":
                quote = ""
            current.append(ch)
            index += 1
            continue
        if ch == "$" and command.startswith("$(", index) and not command.startswith("$((", index):
            end = _match_paren(command, index + 2)
            if end < 0:
                if state is not None:
                    state["unresolved"] = True
                end = size
            current.append(command[index:end])
            index = end
            continue
        if quote:
            if ch == quote:
                quote = ""
            current.append(ch)
            index += 1
            continue
        if ch in "'\"":
            quote = ch
        elif ch == "#" and (not current or current[-1] in " \t;&|("):
            while index < size and command[index] != "\n":
                index += 1  # a comment: the shell ignores it, including a << inside it
            continue
        elif command.startswith("$((", index) or command.startswith("((", index):
            arith += 2
            step = 3 if command.startswith("$((", index) else 2
            current.append(command[index:index + step])
            index += step
            continue
        elif arith and ch in "()":
            arith += 1 if ch == "(" else -1
        elif command.startswith("<<", index) and not arith and not command.startswith("<<<", index):
            strip = command.startswith("<<-", index)
            tag, nxt = _heredoc_tag(command, index + (3 if strip else 2))
            if tag:
                pending.append((tag, strip))
            current.append(command[index:nxt])
            index = nxt
            continue
        elif ch == "\n":
            line = "".join(current)
            lines.append(line)
            current = []
            index += 1
            for tag, strip in pending:
                body: list[str] = []
                while index <= size:
                    end = command.find("\n", index)
                    end = size if end == -1 else end
                    text = command[index:end]
                    index = end + 1
                    if (text.lstrip("\t") if strip else text) == tag:
                        break
                    body.append(text)
                    if end == size:
                        break
                if _reads_as_script(line):
                    lines.extend(body)
            pending = []
            continue
        current.append(ch)
        index += 1
    lines.append("".join(current))
    return lines


def _substitutions(line: str) -> list[str]:
    """Inner text of every ``$(...)`` (balanced) and backtick substitution in ``line``."""
    found: list[str] = []
    index = 0
    while index < len(line):
        if line.startswith("$(", index) and not line.startswith("$((", index):
            depth, start = 1, index + 2
            cursor = start
            while cursor < len(line) and depth:
                depth += {"(": 1, ")": -1}.get(line[cursor], 0)
                cursor += 1
            found.append(line[start:cursor - 1 if depth == 0 else cursor])
            index = cursor  # nested substitutions are found by the recursive walk
            continue
        if line[index] == "`":
            end = line.find("`", index + 1)
            end = len(line) if end == -1 else end
            found.append(line[index + 1:end])
            index = end + 1
            continue
        index += 1
    return found


def _mask_substitutions(line: str) -> str:
    """Replace every ``$(...)`` and backtick substitution with the word ``$__SUBST__``.

    The lexer must not see a quote that belongs to a substitution (``"$(cat <<EOF`` with
    a ``"`` in the body), and the substitution itself is walked separately. The
    placeholder starts with ``$`` so a substitution used as a command name is still an
    expansion in command position.
    """
    out: list[str] = []
    index, size = 0, len(line)
    single = False
    while index < size:
        ch = line[index]
        if single:
            single = ch != "'"
        elif ch == "\\" and index + 1 < size:
            out.append(line[index:index + 2])
            index += 2
            continue
        elif ch == "'":
            single = True
        elif line.startswith("$(", index) and not line.startswith("$((", index):
            end = _match_paren(line, index + 2)
            out.append("$__SUBST__")
            index = size if end < 0 else end
            continue
        elif ch == "`":
            end = line.find("`", index + 1)
            out.append("$__SUBST__")
            index = size if end < 0 else end + 1
            continue
        out.append(ch)
        index += 1
    return "".join(out)


def _simple_commands(line: str, state: dict | None = None) -> list[list[str]]:
    """Split one shell line into simple commands (each a list of words).

    A line the lexer cannot parse (an unbalanced quote, or a quoted argument that
    spans lines) is marked unresolved in ``state`` and split on whitespace, so the
    caller can fail closed instead of trusting the guess.
    """
    lexer = shlex.shlex(_mask_substitutions(line), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        if state is not None:
            state["unresolved"] = True
        tokens = line.split()
    commands: list[list[str]] = [[]]
    for token in tokens:
        if token in _PROCESS_SUBST or (token and set(token) <= set(";&|()")):
            commands.append([])
        elif token and set(token) <= set(";&|()<>"):
            # A fused run such as ``(>`` or ``<((``: boundaries, then maybe a redirection.
            rest = token
            while rest:
                if rest[:2] in _PROCESS_SUBST:
                    rest = rest[2:]
                elif rest[0] in ";&|()":
                    rest = rest[1:]
                else:
                    break
                commands.append([])
            if rest:
                commands[-1].append(rest)
        else:
            commands[-1].append(token)
    return [words for words in commands if words]


def _short_value(words: list[str], position: int, letters: str) -> str | None:
    """The value of the first of ``letters`` in a short-option cluster, or None.

    Reads ``-o VALUE``, ``-oVALUE`` and clusters such as ``-vo VALUE`` or ``-4oVALUE``.
    """
    word = words[position]
    if len(word) < 2 or word[0] != "-" or word[1] == "-":
        return None
    for index, char in enumerate(word[1:], start=1):
        if char in letters:
            attached = word[index + 1:]
            if attached:
                return attached
            return words[position + 1] if position + 1 < len(words) else ""
    return None


def _assignment(word: str, depth: int, state: dict) -> list[str]:
    """Names run through one ``NAME=value`` word (a variable another program runs)."""
    name, _, value = word.partition("=")
    name = name.rstrip("+").split("[")[0]
    if name in _STARTUP_VARS or name.startswith("GIT_CONFIG"):
        state["unresolved"] = True  # a variable the shell or git runs as code
    elif name in _COMMAND_VARS and value:
        return _scan(value, depth + 1, state)
    return []


def _words_candidates(words: list[str], depth: int, state: dict) -> list[str]:
    """Candidates for one simple command given as words."""
    index = 0
    assigned: list[str] = []
    while index < len(words) and _ASSIGN.match(words[index]):
        assigned.extend(_assignment(words[index], depth, state))
        index += 1
    if index >= len(words):
        return assigned
    state["steps"] = state.get("steps", 0) + 1
    if state["steps"] > _STEP_LIMIT:
        state["unresolved"] = True
        return []
    if len(words) > _MAX_WORDS:
        state["unresolved"] = True
        return []
    rest = words[index:]
    if rest and rest[0] == "function":
        rest = rest[2:]  # ``function name {``: the name is not a command
    if len(rest) > 2 and rest[0] == "coproc" and rest[2] in ("{", "("):
        rest = rest[2:]  # ``coproc NAME { ...; }``: the name is not a command
    while rest and (rest[0] in _KEYWORDS or rest[0] == "--" or _REDIRECT.match(rest[0])
                    or (rest[0].isdigit() and len(rest) > 1 and _REDIRECT.match(rest[1]))):
        if depth >= _MAX_DEPTH:
            state["unresolved"] = True
            return []
        if rest[0].isdigit():
            rest = rest[1:]  # a file descriptor number in front of a redirection
        elif _BARE_REDIRECT.match(rest[0]):
            rest = rest[2:]  # the operator and its target
        else:
            rest = rest[1:]
    if not rest:
        return []
    first = rest[0]
    literal = _SAFE_PREFIX.sub("", first, count=1)
    if (
        "$" in literal or "`" in literal
        or (first not in ("[", "[[") and any(ch in first for ch in "*?["))
        or ("{" in first and "," in first)
    ):
        # An expansion or a glob decides the command name: it cannot be known
        # without running a shell.
        state["unresolved"] = True
    head = os.path.basename(rest[0])
    out = assigned + list(_names(rest[0]))
    if head in ("command", "type", "which") and any(w in ("-v", "-V") for w in rest[1:3]):
        return []  # a lookup, not an execution
    if head == "trap":
        operands = [w for w in rest[1:] if not w.startswith("-")]
        if operands:
            out.extend(_scan(operands[0], depth + 1, state))
        return out
    if head in ("at", "batch"):
        state["unresolved"] = True  # a job whose commands are read from stdin
    if head in ("alias", "shopt") or (head == "hash" and "-p" in rest[1:]):
        state["unresolved"] = True  # a later word may now name any program
    if head in ("mapfile", "readarray"):
        for position, word in enumerate(rest[1:-1], start=1):
            if word == "-C":
                out.extend(_scan(rest[position + 1], depth + 1, state))
    for word in rest[1:_LOOKAHEAD]:
        if word.startswith(("--command=", "--call=")):
            out.extend(_scan(word.split("=", 1)[1], depth + 1, state))
    if head == "flock":
        for position, word in enumerate(rest[1:-1], start=1):
            if word in ("-c", "--command"):
                out.extend(_scan(rest[position + 1], depth + 1, state))
    if head == "eval" and len(rest) > 1:
        out.extend(_scan(" ".join(rest[1:]), depth + 1, state))
    elif head == "find":
        for position, word in enumerate(rest[:_MAX_WORDS]):
            if word in _FIND_EXEC and position + 1 < len(rest):
                out.extend(_words_candidates(rest[position + 1:], depth + 1, state))
    elif head in ("export", "declare", "typeset", "local", "readonly"):
        for word in rest[1:]:
            if _ASSIGN.match(word):
                out.extend(_assignment(word, depth, state))
    elif head == "sg" and len([w for w in rest[1:] if w not in ("-", "-c")]) > 1:
        command = [w for w in rest[1:] if w not in ("-", "-c")][1:]
        out.extend(_words_candidates(command, depth + 1, state))
        out.extend(_scan(" ".join(command), depth + 1, state))
    elif head in _SHELLS:
        if "<<<" in rest and rest.index("<<<") + 1 < len(rest):
            out.extend(_scan(rest[rest.index("<<<") + 1], depth + 1, state))
        for position, word in enumerate(rest[1:], start=1):
            if word.startswith("-") and not word.startswith("--") and "c" in word[1:]:
                target = position + 1
                if target < len(rest) and rest[target] == "--":
                    target += 1
                if target < len(rest):
                    out.extend(_scan(rest[target], depth + 1, state))
                break
        else:
            operands: list[str] = []
            skip = False
            for word in rest[1:]:
                if skip:
                    skip = False
                elif word in _SHELL_OPTS_WITH_VALUE:
                    skip = True
                elif not word.startswith(("-", "+")):
                    operands.append(word)
            if head in ("sh", "bash", "zsh", "dash", "ksh") and "<<<" not in rest and (
                not operands or "-s" in rest[1:] or "-" in rest[1:]
            ):
                state["unresolved"] = True  # a shell that reads its script from stdin
            if any(w in _SHELL_OPTS_RUNNING for w in rest[1:]):
                state["unresolved"] = True  # a startup file the shell runs
    elif head in _WRAPPERS:
        tail = rest[1:]
        # Option values (``sudo -u root``, ``nice -n 5``) hide the real command a
        # few words later: inspect the next few words and the stripped remainder.
        for word in tail[:_LOOKAHEAD]:
            if not word.startswith("-") and not _ASSIGN.match(word):
                out.extend(_names(word))
            if head in _STRING_WRAPPERS and " " in word and not word.startswith("-"):
                out.extend(_scan(word, depth + 1, state))
        if head in ("sudo", "doas") and ("-s" in tail or "-i" in tail):
            state["unresolved"] = True  # a login or interactive shell
        if head == "xargs" and any(w.startswith(("-I", "-i", "-J")) for w in tail[:_LOOKAHEAD]) \
                and any(os.path.basename(w) in _SHELLS for w in tail[:_LOOKAHEAD]):
            state["unresolved"] = True  # the shell script is built from input
        if head == "env":
            for position, word in enumerate(tail[:_LOOKAHEAD]):
                if word.startswith("--split-string="):
                    out.extend(_scan(word.split("=", 1)[1], depth + 1, state))
                elif word == "--split-string" and position + 1 < len(tail):
                    out.extend(_scan(tail[position + 1], depth + 1, state))
                else:
                    cluster = re.match(r"^-[A-Za-z]*S(.*)$", word) if not word.startswith("--") else None
                    if cluster and cluster.group(1):
                        out.extend(_scan(cluster.group(1), depth + 1, state))
                    elif cluster and position + 1 < len(tail):
                        out.extend(_scan(tail[position + 1], depth + 1, state))
        starts = [i for i, word in enumerate(tail[:_LOOKAHEAD]) if not word.startswith("-")]
        if len(tail) > _LOOKAHEAD:
            state["unresolved"] = True  # the command may sit beyond the words inspected
        if starts and depth >= _MAX_DEPTH:
            state["unresolved"] = True
        else:
            for i in starts:
                out.extend(_words_candidates(tail[i:], depth + 1, state))
    elif head in (".", "source"):
        operands = [w for w in rest[1:] if not w.startswith("-")]
        if not operands or operands[0].startswith(("/dev/stdin", "/dev/fd/", "/proc/self/fd/")):
            state["unresolved"] = True  # sourced from a pipe or a process substitution
    elif head == "git":
        has_clone = "clone" in rest[1:]
        for position, word in enumerate(rest[1:], start=1):
            following = rest[position + 1] if position + 1 < len(rest) else ""
            if word == "-c" or (word.startswith("-c") and "=" in word and not word.startswith("--")):
                key, _, value = (following if word == "-c" else word[2:]).partition("=")
                if value and _GIT_COMMAND_KEY.search(key.lower()):
                    out.extend(_scan(value.lstrip("!"), depth + 1, state))
            elif word.startswith(("--exec=", "--extcmd=", "--upload-pack=", "--receive-pack=")):
                out.extend(_scan(word.split("=", 1)[1], depth + 1, state))
            elif word in ("--exec", "--extcmd", "--upload-pack", "--receive-pack") or (word == "-u" and has_clone):
                out.extend(_scan(following, depth + 1, state))
            elif word.startswith("--config-env"):
                state["unresolved"] = True  # a config value read from a variable
        for sub, triggers in _GIT_RUNNERS.items():
            if sub in rest[1:]:
                at = rest.index(sub, 1)
                for position, word in enumerate(rest[at + 1:], start=at + 1):
                    if word in triggers:
                        out.extend(_trigger_candidates(rest[position + 1:], depth + 1, state))
                    elif "-x" in triggers and word.startswith("-x") and len(word) > 2:
                        out.extend(_scan(word[2:], depth + 1, state))
    elif head in ("ssh", "scp", "sftp"):
        for position in range(1, len(rest)):
            option = _short_value(rest, position, "o")
            match = _SSH_COMMAND_OPTION.match(option.strip()) if option else None
            if match:
                out.extend(_scan(match.group(1), depth + 1, state))
            if head != "ssh":
                program = _short_value(rest, position, "S" if head == "scp" else "SD")
                if program:
                    out.extend(_scan(program, depth + 1, state))
    elif head == "rsync":
        for position, word in enumerate(rest[1:], start=1):
            shell = _short_value(rest, position, "e")
            if word.startswith("--rsh="):
                shell = word.split("=", 1)[1]
            elif word == "--rsh":
                shell = rest[position + 1] if position + 1 < len(rest) else ""
            if shell:
                out.extend(_scan(shell, depth + 1, state))
    elif head == "socat":
        for word in rest[1:]:
            for marker in ("EXEC:", "SYSTEM:", "SHELL:"):
                if marker in word.upper():
                    out.extend(_scan(word[word.upper().index(marker) + len(marker):].split(",")[0], depth + 1, state))
    elif head in _TRIGGERED:
        if depth >= _MAX_DEPTH:
            state["unresolved"] = True
            return out
        triggers = _TRIGGERED[head]
        for position, word in enumerate(rest[1:_LOOKAHEAD], start=1):
            flag = word.split("=", 1)[0] if word.startswith("--") else word
            parts = word.split(None, 1)
            if len(parts) == 2 and parts[0] in triggers and not word.startswith("-"):
                out.extend(_scan(parts[1], depth + 1, state))  # ``i3-msg 'exec NAME'``
            if flag in triggers:
                inline = word.split("=", 1)[1] if word.startswith("--") and "=" in word else ""
                after = ([inline] if inline else []) + rest[position + 1:]
                out.extend(_trigger_candidates(after, depth + 1, state))
        if len(rest) > _LOOKAHEAD:
            state["unresolved"] = True
    elif head == "flatpak" and "run" in rest:
        after = [word for word in rest[rest.index("run") + 1:] if not word.startswith("-")]
        if after:
            out.append(after[0])
    return out


def _trigger_candidates(words: list[str], depth: int, state: dict) -> list[str]:
    """Names run by the words after a trigger.

    A quoted command line is scanned; plain words are read from each non-option word
    in turn, because an option value (``tmux -c DIR``) can hide the real command.
    """
    out: list[str] = []
    stripped = [w for w in words if w != "--"]
    for position, word in enumerate(stripped[:_LOOKAHEAD]):
        if word.startswith("-"):
            continue
        if any(ch in word for ch in " ;|&$`"):
            out.extend(_scan(word, depth, state))
        out.extend(_words_candidates(stripped[position:], depth, state))
    if len(stripped) > _LOOKAHEAD:
        state["unresolved"] = True
    return out


def _scan(command: str, depth: int, state: dict) -> list[str]:
    """Walk ``command`` and collect executable names; mark ``state`` when unresolved.

    A command is unresolved when it is longer than the cap or nests deeper than
    the depth limit: the walk cannot say what it runs, so the caller must not
    treat the empty answer as "nothing to block".
    """
    if not command or not command.strip():
        return []
    state["steps"] = state.get("steps", 0) + 1
    if len(command) > _MAX_COMMAND_CHARS or depth > _MAX_DEPTH or state["steps"] > _STEP_LIMIT:
        state["unresolved"] = True
        return []
    if "$(" in command and re.search(r"\bcase\b", command):
        state["unresolved"] = True  # a case pattern's ``)`` ends a substitution early
    out: list[str] = []
    for line in _logical_lines(command, state):
        for words in _simple_commands(line, state):
            out.extend(_words_candidates(words, depth, state))
        for inner in _substitutions(line):
            out.extend(_scan(inner, depth + 1, state))
    return out


@functools.lru_cache(maxsize=256)
def _resolve_cached(command: str) -> tuple[tuple[str, ...], bool]:
    """Memoized walk: a rule set evaluates the same command once per policy."""
    state = {"unresolved": False, "steps": 0}
    try:
        return tuple(_scan(command, 0, state)), state["unresolved"]
    except Exception:  # best effort: an unexpected parse failure is unresolved
        return (), True


def resolve_command(command: str) -> tuple[list[str], bool]:
    """Return ``(executable names, unresolved)`` for a shell string (never raises)."""
    names, unresolved = _resolve_cached(command)
    return list(names), unresolved


def command_candidates(command: str, _depth: int = 0) -> list[str]:
    """Executable names a shell string would run (best-effort, never raises).

    Walks every simple command, skips env assignments, looks through known
    launch wrappers (``env``, ``nohup``, ``sudo``, ``timeout``...), recurses into
    ``sh -c`` / ``bash -lc`` strings and ``$(...)`` / backticks, and resolves
    symlinks. Arguments are never candidates, so ``grep chrome notes.txt`` or
    ``git commit -m "mention chrome"`` do not match a policy on ``chrome``.
    Use :func:`resolve_command` to also learn whether the walk gave up.
    """
    names, _ = resolve_command(command)
    return names


def _action_of(policy: dict) -> tuple[str, str]:
    action = policy.get("action", {})
    return str(action.get("verb", "")), str(action.get("resource", ""))


def _patterns_of(policy: dict) -> list[str]:
    """Resource patterns of a policy: ``resource`` may be a string or a list."""
    resource = policy.get("action", {}).get("resource", "")
    if isinstance(resource, list):
        return [str(item) for item in resource]
    return [str(resource)]


def _policy_matches(policy: dict, resource: str) -> bool:
    """True when the policy's resource pattern(s) match ``resource``.

    ``"match": "command"`` compares each pattern with the executable names the
    command would run instead of the whole string, so a policy on a binary name
    does not fire on a mere mention of it.
    """
    patterns = _patterns_of(policy)
    if policy.get("action", {}).get("match") == "command":
        names, unresolved = resolve_command(resource)
        if unresolved:
            return True  # fail closed: the walk cannot say what this command runs
        return any(fnmatch.fnmatchcase(name, pattern) for name in names for pattern in patterns)
    if _action_of(policy)[0] in ("mcp", "prompt", "output", "stop"):
        # Tool names are identifiers, not paths: ``mcp__Server__Tool`` and the lower-case
        # form a harness may send are the same tool, so neither spelling can dodge a rule.
        # A prompt is prose: the case of a word never decides whether a rule applies.
        resource = resource.lower()
        patterns = [pattern.lower() for pattern in patterns]
        if _action_of(policy)[0] in ("prompt", "output", "stop"):
            # Full-width letters and invisible format characters must not dodge a prose rule.
            resource = _fold_prompt(resource)
            patterns = [_fold_prompt(pattern) for pattern in patterns]
    return any(_resource_matches(pattern, resource) for pattern in patterns)


def _fold_prompt(text: str) -> str:
    """NFKC-fold ``text`` and drop format (``Cf``) characters, then lower-case it."""
    folded = unicodedata.normalize("NFKC", text)
    return "".join(ch for ch in folded if unicodedata.category(ch) != "Cf").casefold()


def _fallback_of(policy: dict) -> str:
    """The ``on_ask_unavailable`` value of a policy; anything but allow or deny is deny."""
    value = policy.get("on_ask_unavailable", "deny")
    return value if value in ("allow", "deny") else "deny"


def _applies(policy: dict, verb: str, resource: str, event: str) -> bool:
    """True when ``policy`` is for this verb and event and its pattern matches ``resource``."""
    try:
        p_verb, _ = _action_of(policy)
        if p_verb != verb:
            return False
        # An output rule means something on tool.post only, and a stop rule on turn.stop only,
        # so each defaults there.
        bound = policy.get("event", {"output": "tool.post", "stop": "turn.stop"}.get(p_verb, "tool.pre"))
        if isinstance(bound, str) and bound in KNOWN_EVENTS and bound != event:
            return False
        # A missing event means tool.pre. An unknown, misspelled or non-string
        # value is not skipped: the policy applies on every event, so a typo can
        # never switch a rule off.
        return _policy_matches(policy, resource)
    except Exception:  # a malformed entry must not stop the other policies
        return False


def notes(policies: list[dict], verb: str, resource: str, event: str) -> list[str]:
    """Messages of the ``note`` policies that match one action, in policy order.

    ``evaluate`` never reports a note (it ranks below allow), so an event whose only
    effect is a note reads them here.
    """
    return [str(p.get("message", "")) for p in policies
            if isinstance(p, dict) and str(p.get("decision", "")) == "note" and _applies(p, verb, resource, event)]


def evaluate(policies: list[dict], verb: str, resource: str, event: str = "tool.pre") -> dict:
    """Evaluate policies against one action; return the most restrictive decision.

    Precedence is monotonic (the composition law): ``deny > ask > allow > note``.
    An event with no matching policy yields ``allow``. When several ``ask``
    policies match, the fallback used where nobody can be asked is the strictest
    of their ``on_ask_unavailable`` values (``deny`` beats ``allow``; a missing or
    invalid value counts as ``deny``), so the result never depends on file order.
    The reported ``policy_id`` and ``message`` are those of the first policy that
    holds the winning fallback. A policy binds one event (``"event"``, default
    ``tool.pre``) and is skipped when ``event`` is a different one, so a rule
    written for a tool call never fires on a prompt or a stop.
    """
    order = {"deny": 3, "ask": 2, "allow": 1, "note": 0}
    best = {"decision": "allow", "policy_id": None, "message": ""}
    asks: list[dict] = []
    for policy in policies:
        if not _applies(policy, verb, resource, event):
            continue
        decision = str(policy.get("decision", "allow"))
        if decision not in order:
            decision = "deny"  # an unknown or misspelled decision must not allow
        if decision == "ask":
            asks.append(policy)
        if order.get(decision, 0) > order.get(best["decision"], 0):
            best = {
                "decision": decision,
                "policy_id": policy.get("id"),
                "message": str(policy.get("message", "")),
                "on_ask_unavailable": _fallback_of(policy),
            }
    if best["decision"] == "ask" and asks:
        winner = next((p for p in asks if _fallback_of(p) == "deny"), asks[0])
        best = {
            "decision": "ask",
            "policy_id": winner.get("id"),
            "message": str(winner.get("message", "")),
            "on_ask_unavailable": _fallback_of(winner),
        }
    return best
