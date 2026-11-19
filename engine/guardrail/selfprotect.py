"""The opt-in policy that stops the agent's write tools from editing the guardrail itself.

The shipped source is ``methodology/lifecycle/policies/self-protection.policy.json``
(disabled, like every shipped policy). The installer writes an enabled, machine-local
copy into the user policy directory when the person chooses it. It is a speed bump and
a visible tripwire, not a sandbox: a shell redirection is not a write tool (ADR 0015).
"""

from __future__ import annotations

import copy
import json
import os
import tempfile
from pathlib import Path

SOURCE = "methodology/lifecycle/policies/self-protection.policy.json"
POLICY_FILE = "self-protection.policy.json"
GENERATED_BY = "coacus-install"
RELEASE_HOW = (
    "The person releases it, never the agent: edit the file in their own terminal, or set "
    '"enabled": false in the installed self-protection.policy.json, make the change, then set '
    "it back (or run: python3 scripts/coacus_install.py <harness> --self-protection on)."
)


def _extra(template: dict, identifier: str, title: str, resource: str) -> dict:
    extra = copy.deepcopy(template)
    extra.update(id=identifier, title=title)
    extra["action"] = {"verb": "write", "resource": resource}
    return extra


def build_policy(root: Path, policy_dir: Path) -> dict:
    """Return the enabled policy document.

    The shipped file is checked first: every rule must be a ``deny`` on ``write``, so an
    edited source cannot install a protection that does nothing. Two rules are added for
    this machine: the policy directory actually in use (a custom ``COACUS_POLICY_DIR`` or
    ``--browser-policy-dir`` sits outside the shipped patterns) and the top of the Coacus
    tree, where a module named like a standard one would shadow it when the guard starts.
    """
    document = copy.deepcopy(json.loads((root / SOURCE).read_text(encoding="utf-8")))
    policies = document.get("policies")
    if not isinstance(policies, list) or not policies:
        raise ValueError("the shipped self-protection policy has no rules")
    for policy in policies:
        action = policy.get("action") if isinstance(policy, dict) else None
        if not isinstance(action, dict) or action.get("verb") != "write" or policy.get("decision") != "deny":
            raise ValueError("every self-protection rule must deny a write")
    document["enabled"] = True
    document["generated"] = {"by": GENERATED_BY}
    template = policies[0]
    wanted = [
        ("guard-policy-dir-actual", "Block writes to the policy directory in use",
         policy_dir.resolve().as_posix().rstrip("/") + "/*"),
        ("guard-root-modules", "Block writes to modules at the top of the Coacus tree",
         root.resolve().as_posix().rstrip("/") + "/*.py"),
    ]
    for identifier, title, resource in wanted:
        if all(p["action"]["resource"] != resource for p in policies):
            policies.append(_extra(template, identifier, title, resource))
    return document


def write_policy(directory: Path, document: dict) -> Path:
    """Write the document into ``directory`` atomically and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / POLICY_FILE
    handle, temporary = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(document, indent=2) + "\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    return path


def remove_policy(directory: Path) -> bool:
    """Delete the generated policy; a hand-written file of the same name is kept."""
    path = directory / POLICY_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(data, dict) or (data.get("generated") or {}).get("by") != GENERATED_BY:
        return False
    path.unlink()
    return True


def status(directory: Path) -> str:
    """``active``, ``disabled`` (file present, not enabled) or ``absent``."""
    try:
        data = json.loads((directory / POLICY_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "absent"
    if not isinstance(data, dict) or data.get("enabled") is not True:
        return "disabled"
    return "active" if isinstance(data.get("policies"), list) and data["policies"] else "disabled"
