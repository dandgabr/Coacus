"""Browser detection and selection for the agent browser policy.

At install time Coacus can detect which web browsers exist on the machine, let
the user pick which ones an agent may drive (a primary and an optional
fallback) and render a deny policy for every other known browser. The policy is
machine-local data (``user_policy_dir``), never committed to the repository.

The module is stdlib-only and side-effect free except for the explicit
``write_policy`` / ``remove_policy`` helpers. Detection takes its probes as
parameters so tests never depend on the developer's machine.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

CATALOG_PATH = "methodology/lifecycle/browsers.json"
POLICY_FILE = "browser.policy.json"
GENERATED_BY = "coacus_install"


def load_catalog(root: Path) -> dict:
    """Load the browser catalogue (``methodology/lifecycle/browsers.json``)."""
    return json.loads((root / CATALOG_PATH).read_text(encoding="utf-8"))


def _catalog_index(catalog: dict) -> dict[str, dict]:
    return {entry["id"]: entry for entry in catalog.get("browsers", [])}


def flatpak_apps() -> set[str]:
    """Installed Flatpak application ids (empty when Flatpak is absent or fails)."""
    if not shutil.which("flatpak"):
        return set()
    try:
        done = subprocess.run(
            ["flatpak", "list", "--app", "--columns=application"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    return {line.strip() for line in done.stdout.splitlines() if line.strip()}


def detect(
    catalog: dict,
    which: Callable[[str], str | None] = shutil.which,
    exists: Callable[[str], bool] = os.path.exists,
    flatpak: set[str] | None = None,
) -> list[dict]:
    """Return the catalogue browsers present on this machine, in catalogue order.

    A browser counts as installed when one of its binary names resolves on
    ``PATH``, one of its well-known absolute paths exists, or its Flatpak
    application id is installed. Each result is ``{"id", "name", "binary"}``
    where ``binary`` is the first probe that matched (for display).
    """
    apps = flatpak_apps() if flatpak is None else flatpak
    found: list[dict] = []
    for entry in catalog.get("browsers", []):
        binary = ""
        for name in entry.get("binaries", []):
            resolved = which(name)
            if resolved:
                binary = resolved
                break
        if not binary:
            for path in entry.get("paths", []):
                if exists(path):
                    binary = path
                    break
        if not binary:
            for app in entry.get("flatpak", []):
                if app in apps:
                    binary = f"flatpak:{app}"
                    break
        if binary:
            found.append({"id": entry["id"], "name": entry.get("name", entry["id"]), "binary": binary})
    return found


def choose(
    catalog: dict,
    detected: list[dict],
    primary: str | None = None,
    fallback: str | None = None,
) -> dict:
    """Pick the primary and optional fallback browser.

    Without ``primary`` the first detected browser in the catalogue's
    ``preference`` order wins and there is no fallback. An explicit choice must be
    a detected browser and the fallback must differ from the primary; violations
    raise ``ValueError`` so the installer can stop before writing anything.
    """
    present = [entry["id"] for entry in detected]
    if not present:
        raise ValueError("no known browser is installed on this machine")
    if primary is None:
        order = [b for b in catalog.get("preference", []) if b in present]
        primary = (order or present)[0]
    if primary not in present:
        raise ValueError(f"primary browser {primary!r} is not installed (detected: {', '.join(present)})")
    if fallback is not None:
        if fallback not in present:
            raise ValueError(f"fallback browser {fallback!r} is not installed (detected: {', '.join(present)})")
        if fallback == primary:
            raise ValueError("fallback must differ from the primary browser")
    return {"primary": primary, "fallback": fallback, "detected": present}


def build_policy(catalog: dict, selection: dict) -> dict:
    """Render the machine-local policy document for a selection.

    Every catalogue browser that is neither the primary nor the fallback gets
    three ``deny`` policies: launching it (``exec`` matched against executable
    names, so a mere mention does not fire), and reading or writing its profile
    directories. Allowed browsers get no policy: the rule is "agents drive only
    the browsers the user selected".
    """
    allowed = {selection["primary"], selection.get("fallback")} - {None}
    policies: list[dict] = []
    for entry in catalog.get("browsers", []):
        if entry["id"] in allowed:
            continue
        name = entry.get("name", entry["id"])
        base = {
            "on_ask_unavailable": "deny",
            "on_decision_failure": "deny",
            "on_mechanism_failure": "allow",
            "severity": "high",
            "evidence": "documented",
        }
        exec_names = list(entry.get("binaries", []))
        exec_names += [os.path.basename(p) for p in entry.get("paths", [])]
        exec_names += list(entry.get("flatpak", []))
        policies.append({
            "id": f"browser-exec-{entry['id']}",
            "title": f"Agents do not launch {name}",
            "action": {"verb": "exec", "resource": sorted(set(exec_names)), "match": "command"},
            "decision": "deny",
            "message": f"{name} is not an approved automation browser on this machine; "
                       f"use {selection['primary']}.",
            **base,
        })
        profiles = [f"*/{p.strip('/')}/*" for p in entry.get("profiles", [])]
        profiles += [f"*/{p.strip('/')}" for p in entry.get("profiles", [])]
        if profiles:
            for verb in ("read", "write"):
                policies.append({
                    "id": f"browser-{verb}-{entry['id']}-profile",
                    "title": f"Agents do not {verb} the {name} profile",
                    "action": {"verb": verb, "resource": sorted(set(profiles))},
                    "decision": "deny",
                    "message": f"The {name} profile holds the user's personal data and is "
                               f"off limits to agents.",
                    **base,
                })
    return {
        "schema": 1,
        "enabled": True,
        "description": "GENERATED by the Coacus installer from the browsers detected on this "
                       "machine. Agents may drive only the selected browsers; every other known "
                       "browser is denied. Re-run the installer to change the selection.",
        "generated": {"by": GENERATED_BY, **selection},
        "policies": policies,
    }


def write_policy(directory: Path, document: dict) -> Path:
    """Write the generated policy document into ``directory`` and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / POLICY_FILE
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path


def remove_policy(directory: Path) -> bool:
    """Delete the generated policy; return True when a file was removed.

    Only a file this installer generated (``generated.by``) is removed, so a
    hand-written ``browser.policy.json`` is never destroyed.
    """
    path = directory / POLICY_FILE
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if data.get("generated", {}).get("by") != GENERATED_BY:
        return False
    path.unlink()
    return True


def read_selection(directory: Path) -> dict | None:
    """Return the recorded selection of a generated policy, or ``None``."""
    path = directory / POLICY_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    generated = data.get("generated")
    if not isinstance(generated, dict) or generated.get("by") != GENERATED_BY:
        return None
    return {k: generated.get(k) for k in ("primary", "fallback", "detected")}


def prompt_selection(
    catalog: dict,
    detected: list[dict],
    ask: Callable[[str], str] = input,
    say: Callable[[str], None] = print,
) -> dict | None:
    """Interactively choose the primary and fallback; ``None`` means "skip".

    Lists the detected browsers, proposes the catalogue's preferred one as the
    default primary and offers "no fallback" as the default fallback. An empty
    answer accepts the default; ``skip`` leaves the policy off.
    """
    if not detected:
        say("browser policy: no known browser detected; skipping.")
        return None
    default = choose(catalog, detected)["primary"]
    say("Browsers detected on this machine:")
    for number, entry in enumerate(detected, start=1):
        say(f"  {number}. {entry['name']} ({entry['id']}) - {entry['binary']}")
    say("Agents will be allowed to drive only the browsers you select; every other "
        "known browser is denied.")

    def pick(label: str, default_id: str | None, allow_none: bool) -> str | None:
        ids = [entry["id"] for entry in detected]
        while True:
            hint = default_id or ("none" if allow_none else "")
            answer = ask(f"{label} [{hint}]: ").strip().lower()
            if not answer:
                return default_id
            if answer == "skip":
                raise KeyboardInterrupt
            if allow_none and answer == "none":
                return None
            if answer.isdigit() and 1 <= int(answer) <= len(ids):
                return ids[int(answer) - 1]
            if answer in ids:
                return answer
            say(f"  unknown choice {answer!r}; use a number, an id, 'none' or 'skip'.")

    try:
        primary = pick("Primary browser for agents (or 'skip')", default, False)
        while True:
            fallback = pick("Fallback browser (or 'none')", None, True)
            if fallback is None or fallback != primary:
                break
            say("  the fallback must differ from the primary.")
    except KeyboardInterrupt:
        return None
    return choose(catalog, detected, primary=primary, fallback=fallback)
