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
import json
import os
import re
import shlex
from pathlib import Path

EVENTS_PATH = "methodology/lifecycle/events.json"
ACTIONS_PATH = "methodology/lifecycle/actions.schema.json"
POLICIES_DIR = "methodology/lifecycle/policies"

DECISIONS = ("allow", "deny", "ask", "note")

_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish", "su"}
_WRAPPERS = {
    "env", "nohup", "setsid", "sudo", "doas", "timeout", "nice", "ionice", "stdbuf",
    "exec", "command", "time", "xvfb-run", "dbus-run-session", "systemd-run",
    "unbuffer", "chrt", "taskset", "flock", "script", "xargs",
    "busybox", "toybox", "builtin", "watch", "runuser",
}
_STEP_LIMIT = 5000
_LOOKAHEAD = 8
_REDIRECT = re.compile(r"^\d*(?:>>?|<<?|>&|<&|&>)")
_BARE_REDIRECT = re.compile(r"^\d*(?:>>?|<|>&|<&|&>)$")
_HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
_KEYWORDS = {"{", "}", "if", "then", "elif", "else", "do", "while", "until", "!", "coproc"}
_FIND_EXEC = {"-exec", "-execdir", "-ok", "-okdir"}
_PROCESS_SUBST = {"<(", ">("}
_SUBSHELL = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")
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
    """Load every enabled ``*.policy.json`` under ``base`` (missing dir -> none)."""
    policies: list[dict] = []
    if not base.is_dir():
        return policies
    for path in sorted(base.glob("*.policy.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("enabled") is not True:
            continue
        for policy in data.get("policies", []):
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


def _logical_lines(command: str) -> list[str]:
    """Split on newlines that are outside quotes; skip heredoc bodies of non-shells.

    A quoted argument that spans lines stays on one line, so it parses. The body of
    a here-document is data unless the command that reads it is a shell, which
    would run it; for a shell the body lines are scanned like any other.
    """
    lines: list[str] = []
    current: list[str] = []
    quote = ""
    escaped = False
    for ch in command:
        if escaped:
            escaped = False
        elif ch == "\\" and quote != "'":
            escaped = True
        elif quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif ch == "\n":
            lines.append("".join(current))
            current = []
            continue
        current.append(ch)
    lines.append("".join(current))
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        out.append(line)
        index += 1
        marker = _HEREDOC.search(line) if "<<<" not in line else None
        if marker and not re.search(r"(?:^|[\s;&|(])(?:sh|bash|zsh|dash|ksh)\b", line):
            tag = marker.group(2)
            while index < len(lines) and lines[index].strip() != tag:
                index += 1
            index += 1  # the terminator
    return out


def _simple_commands(line: str, state: dict | None = None) -> list[list[str]]:
    """Split one shell line into simple commands (each a list of words).

    A line the lexer cannot parse (an unbalanced quote, or a quoted argument that
    spans lines) is marked unresolved in ``state`` and split on whitespace, so the
    caller can fail closed instead of trusting the guess.
    """
    lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
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


def _words_candidates(words: list[str], depth: int, state: dict) -> list[str]:
    """Candidates for one simple command given as words."""
    index = 0
    while index < len(words) and _ASSIGN.match(words[index]):
        index += 1
    if index >= len(words):
        return []
    state["steps"] = state.get("steps", 0) + 1
    if state["steps"] > _STEP_LIMIT:
        state["unresolved"] = True
        return []
    rest = words[index:]
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
    if first.startswith("$") or ("{" in first and "," in first and not first.startswith("{")) \
            or (first.startswith("{") and "," in first and first.endswith("}")):
        # Expansion decides the command name: it cannot be known without a shell.
        state["unresolved"] = True
    head = os.path.basename(rest[0])
    out = list(_names(rest[0]))
    if head == "eval" and len(rest) > 1:
        out.extend(_scan(" ".join(rest[1:]), depth + 1, state))
    elif head == "find":
        for position, word in enumerate(rest):
            if word in _FIND_EXEC and position + 1 < len(rest):
                out.extend(_words_candidates(rest[position + 1:], depth + 1, state))
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
            if head in ("sh", "bash", "zsh", "dash", "ksh") and len(rest) == 1:
                state["unresolved"] = True  # a bare shell reads its script from stdin
    elif head in _WRAPPERS:
        tail = rest[1:]
        # Option values (``sudo -u root``, ``nice -n 5``) hide the real command a
        # few words later: inspect the next few words and the stripped remainder.
        for word in tail[:_LOOKAHEAD]:
            if not word.startswith("-") and not _ASSIGN.match(word):
                out.extend(_names(word))
        if head == "env":
            for position, word in enumerate(tail):
                if word in ("-S", "--split-string") and position + 1 < len(tail):
                    out.extend(_scan(tail[position + 1], depth + 1, state))
                elif word.startswith("--split-string="):
                    out.extend(_scan(word.split("=", 1)[1], depth + 1, state))
                elif word.startswith("-S") and len(word) > 2:
                    out.extend(_scan(word[2:], depth + 1, state))
        starts = [i for i, word in enumerate(tail[:_LOOKAHEAD]) if not word.startswith("-")]
        if starts and depth >= _MAX_DEPTH:
            state["unresolved"] = True
        else:
            for i in starts:
                out.extend(_words_candidates(tail[i:], depth + 1, state))
    elif head == "flatpak" and "run" in rest:
        after = [word for word in rest[rest.index("run") + 1:] if not word.startswith("-")]
        if after:
            out.append(after[0])
    return out


def _scan(command: str, depth: int, state: dict) -> list[str]:
    """Walk ``command`` and collect executable names; mark ``state`` when unresolved.

    A command is unresolved when it is longer than the cap or nests deeper than
    the depth limit: the walk cannot say what it runs, so the caller must not
    treat the empty answer as "nothing to block".
    """
    if not command or not command.strip():
        return []
    if len(command) > _MAX_COMMAND_CHARS or depth > _MAX_DEPTH:
        state["unresolved"] = True
        return []
    out: list[str] = []
    for line in _logical_lines(command):
        for words in _simple_commands(line, state):
            out.extend(_words_candidates(words, depth, state))
        for match in _SUBSHELL.finditer(line):
            out.extend(_scan(match.group(1) or match.group(2) or "", depth + 1, state))
    return out


def resolve_command(command: str) -> tuple[list[str], bool]:
    """Return ``(executable names, unresolved)`` for a shell string (never raises)."""
    state = {"unresolved": False}
    try:
        return _scan(command, 0, state), state["unresolved"]
    except Exception:  # best effort: an unexpected parse failure is unresolved
        return [], True


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
    return any(_resource_matches(pattern, resource) for pattern in patterns)


def _fallback_of(policy: dict) -> str:
    """The ``on_ask_unavailable`` value of a policy; anything but allow or deny is deny."""
    value = policy.get("on_ask_unavailable", "deny")
    return value if value in ("allow", "deny") else "deny"


def evaluate(policies: list[dict], verb: str, resource: str) -> dict:
    """Evaluate policies against one action; return the most restrictive decision.

    Precedence is monotonic (the composition law): ``deny > ask > allow > note``.
    An event with no matching policy yields ``allow``. When several ``ask``
    policies match, the fallback used where nobody can be asked is the strictest
    of their ``on_ask_unavailable`` values (``deny`` beats ``allow``; a missing or
    invalid value counts as ``deny``), so the result never depends on file order.
    The reported ``policy_id`` and ``message`` are those of the first policy that
    holds the winning fallback.
    """
    order = {"deny": 3, "ask": 2, "allow": 1, "note": 0}
    best = {"decision": "allow", "policy_id": None, "message": ""}
    asks: list[dict] = []
    for policy in policies:
        p_verb, _ = _action_of(policy)
        if p_verb != verb:
            continue
        if not _policy_matches(policy, resource):
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
