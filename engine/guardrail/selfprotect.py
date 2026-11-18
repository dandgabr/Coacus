"""The opt-in policy that stops the agent's write tools from editing the guardrail itself.

The shipped source is ``methodology/lifecycle/policies/self-protection.policy.json``
(disabled, like every shipped policy). The installer writes an enabled, machine-local
copy into the user policy directory when the person chooses it. It is a speed bump and
a visible tripwire, not a sandbox: a shell redirection is not a write tool (ADR 0015).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

SOURCE = "methodology/lifecycle/policies/self-protection.policy.json"
POLICY_FILE = "self-protection.policy.json"
GENERATED_BY = "coacus-install"
RELEASE_HOW = (
    "The person releases it, never the agent: edit the file in their own terminal, or set "
    '"enabled": false in the installed self-protection.policy.json, make the change, then set '
    "it back (or run: python3 scripts/coacus_install.py <harness> --self-protection on)."
)


def build_policy(root: Path, policy_dir: Path) -> dict:
    """Return the enabled policy document, also covering the actual policy directory.

    A custom policy directory (``COACUS_POLICY_DIR`` or ``--browser-policy-dir``) would
    otherwise sit outside the shipped patterns.
    """
    document = json.loads((root / SOURCE).read_text(encoding="utf-8"))
    document = copy.deepcopy(document)
    document["enabled"] = True
    document["generated"] = {"by": GENERATED_BY}
    resource = policy_dir.resolve().as_posix().rstrip("/") + "/*"
    template = document["policies"][0]
    if all(p["action"]["resource"] != resource for p in document["policies"]):
        extra = copy.deepcopy(template)
        extra.update(id="guard-policy-dir-actual", title="Block writes to the policy directory in use")
        extra["action"] = {"verb": "write", "resource": resource}
        document["policies"].append(extra)
    return document


def write_policy(directory: Path, document: dict) -> Path:
    """Write the document into ``directory`` and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / POLICY_FILE
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
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
    return "active" if isinstance(data, dict) and data.get("enabled") is True else "disabled"
