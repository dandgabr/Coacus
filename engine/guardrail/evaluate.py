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
other verbs.
"""

from __future__ import annotations

import fnmatch
import json
from pathlib import Path

EVENTS_PATH = "methodology/lifecycle/events.json"
ACTIONS_PATH = "methodology/lifecycle/actions.schema.json"
POLICIES_DIR = "methodology/lifecycle/policies"

DECISIONS = ("allow", "deny", "ask", "note")


def load_events(root: Path) -> dict[str, dict]:
    """Load the canonical event taxonomy as ``{event_id: event}``."""
    path = root / EVENTS_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    return {e["id"]: e for e in data.get("events", [])}


def load_policies(root: Path) -> list[dict]:
    """Load every ACTIVE policy from ``methodology/lifecycle/policies/*.json``.

    A file is active only when it declares ``"enabled": true``. The shipped
    default set is empty and the reference file is disabled, so installing
    Coacus never changes a session's behaviour without an explicit opt-in (D2).
    """
    base = root / POLICIES_DIR
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


def _resource_matches(pattern: str, value: str) -> bool:
    """Match a resource pattern against a concrete resource value."""
    if pattern in ("", "*"):
        return True
    if fnmatch.fnmatch(value, pattern):
        return True
    # Substring form for command/host patterns (e.g. "git push*--force*").
    if "*" in pattern:
        import re

        regex = "^" + re.escape(pattern).replace(r"\*", ".*") + "$"
        return re.search(regex, value) is not None
    return pattern in value


def _action_of(policy: dict) -> tuple[str, str]:
    action = policy.get("action", {})
    return str(action.get("verb", "")), str(action.get("resource", ""))


def evaluate(policies: list[dict], verb: str, resource: str) -> dict:
    """Evaluate policies against one action; return the most restrictive decision.

    Precedence is monotonic (the composition law): ``deny > ask > allow > note``.
    An event with no matching policy yields ``allow``.
    """
    order = {"deny": 3, "ask": 2, "allow": 1, "note": 0}
    best = {"decision": "allow", "policy_id": None, "message": ""}
    for policy in policies:
        p_verb, p_resource = _action_of(policy)
        if p_verb != verb:
            continue
        if not _resource_matches(p_resource, resource):
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
