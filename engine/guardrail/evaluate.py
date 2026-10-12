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
_SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish"}
_WRAPPERS = {
    "env", "nohup", "setsid", "sudo", "doas", "timeout", "nice", "ionice", "stdbuf",
    "exec", "command", "time", "xvfb-run", "dbus-run-session", "systemd-run",
    "unbuffer", "chrt", "taskset", "flock", "script", "xargs",
}
_SUBSHELL = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")
_MAX_DEPTH = 4


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


def _resource_matches(pattern: str, value: str) -> bool:
    """Match a resource pattern against a concrete resource value."""
    if pattern in ("", "*"):
        return True
    if fnmatch.fnmatch(value, pattern):
        return True
    # Substring form for command/host patterns (e.g. "git push*--force*").
    if "*" in pattern:
        regex = "^" + re.escape(pattern).replace(r"\*", ".*") + "$"
        return re.search(regex, value) is not None
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


def _simple_commands(line: str) -> list[list[str]]:
    """Split one shell line into simple commands (each a list of words)."""
    lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = line.split()
    commands: list[list[str]] = [[]]
    for token in tokens:
        if token and set(token) <= set(";&|()"):
            commands.append([])
        else:
            commands[-1].append(token)
    return [words for words in commands if words]


def _words_candidates(words: list[str], depth: int) -> list[str]:
    """Candidates for one simple command given as words."""
    index = 0
    while index < len(words) and _ASSIGN.match(words[index]):
        index += 1
    if index >= len(words):
        return []
    rest = words[index:]
    head = os.path.basename(rest[0])
    out = list(_names(rest[0]))
    if head in _SHELLS:
        for position, word in enumerate(rest[1:], start=1):
            if word.startswith("-") and not word.startswith("--") and "c" in word[1:]:
                if position + 1 < len(rest):
                    out.extend(command_candidates(rest[position + 1], depth + 1))
                break
    elif head in _WRAPPERS:
        tail = rest[1:]
        # Option values (``sudo -u root``, ``nice -n 5``) hide the real command a
        # few words later: inspect the next few words and the stripped remainder.
        for word in tail[:4]:
            if not word.startswith("-") and not _ASSIGN.match(word):
                out.extend(_names(word))
        stripped = [word for word in tail if not word.startswith("-")]
        if stripped and depth < _MAX_DEPTH:
            out.extend(_words_candidates(stripped, depth + 1))
    elif head == "flatpak" and "run" in rest:
        after = [word for word in rest[rest.index("run") + 1:] if not word.startswith("-")]
        if after:
            out.append(after[0])
    return out


def command_candidates(command: str, _depth: int = 0) -> list[str]:
    """Executable names a shell string would run (best-effort, never raises).

    Walks every simple command, skips env assignments, looks through known
    launch wrappers (``env``, ``nohup``, ``sudo``, ``timeout``...), recurses into
    ``sh -c`` / ``bash -lc`` strings and ``$(...)`` / backticks, and resolves
    symlinks. Arguments are never candidates, so ``grep chrome notes.txt`` or
    ``git commit -m "mention chrome"`` do not match a policy on ``chrome``.
    """
    if _depth > _MAX_DEPTH or not command or not command.strip():
        return []
    out: list[str] = []
    for line in command.splitlines() or [command]:
        for words in _simple_commands(line):
            out.extend(_words_candidates(words, _depth))
        for match in _SUBSHELL.finditer(line):
            out.extend(command_candidates(match.group(1) or match.group(2) or "", _depth + 1))
    return out


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
        names = command_candidates(resource)
        return any(fnmatch.fnmatchcase(name, pattern) for name in names for pattern in patterns)
    return any(_resource_matches(pattern, resource) for pattern in patterns)


def evaluate(policies: list[dict], verb: str, resource: str) -> dict:
    """Evaluate policies against one action; return the most restrictive decision.

    Precedence is monotonic (the composition law): ``deny > ask > allow > note``.
    An event with no matching policy yields ``allow``.
    """
    order = {"deny": 3, "ask": 2, "allow": 1, "note": 0}
    best = {"decision": "allow", "policy_id": None, "message": ""}
    for policy in policies:
        p_verb, _ = _action_of(policy)
        if p_verb != verb:
            continue
        if not _policy_matches(policy, resource):
            continue
        decision = str(policy.get("decision", "allow"))
        if order.get(decision, 0) > order.get(best["decision"], 0):
            best = {
                "decision": decision,
                "policy_id": policy.get("id"),
                "message": str(policy.get("message", "")),
                "on_ask_unavailable": policy.get("on_ask_unavailable", "deny"),
            }
    return best
