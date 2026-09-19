#!/usr/bin/env python3
"""Coacus installer: activate rendered artifacts into a harness.

The repository GENERATES the per-harness artifacts (ADR-0016); this script
INSTALLS them into a harness's own discovery locations. It is explicit and
idempotent — nothing runs at session start, and it never rewrites a harness
config file wholesale.

Mechanisms (verified, see docs/install.md):

- opencode    plugin -> <config_dir>/plugins/coacus.js  (`__COACUS_ROOT__`
              substituted), plus skill trees mirrored under <config_dir>/skills/.
- claude-code skills   -> <config_dir>/skills/<skill>/  (documented personal path)
              hook     -> plugin staged at <config_dir>/plugins/coacus/ with the
              script at bootstrap/session-start.sh (matching hooks.json).
- antigravity plugin   -> <config_dir>/config/plugins/coacus/ + path registered
              in <config_dir>/config/plugins.json        (backup first).
- codex       skills   -> <config_dir>/skills/<skill>/    (native discovery).
- cursor      not installed (no live SessionStart hook); prints guidance only.

Usage:
    python3 scripts/coacus_install.py <harness|all> [--dry-run] [--uninstall]
    python3 scripts/coacus_install.py opencode --config-dir /tmp/oc

A manifest (`coacus-install.json`) is written next to each target so re-runs
are idempotent and `--uninstall` removes exactly what was installed.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_NAME = "coacus-install.json"
SKILL_ROOTS = ("methodology/workflows", "knowledge/skills")


def _home() -> Path:
    return Path.home()


def default_config_dir(harness: str, home: Path) -> Path:
    return {
        "opencode": home / ".config" / "opencode",
        "claude-code": home / ".claude",
        "antigravity": home / ".gemini",
        "codex": home / ".codex",
        "cursor": home / ".cursor",
    }[harness]


def discover_skills(root: Path) -> list[Path]:
    """All skill directories (the parent of a SKILL.md) in the repository."""
    found: list[Path] = []
    for top in SKILL_ROOTS:
        base = root / top
        if base.is_dir():
            found.extend(sorted(p.parent for p in base.rglob("SKILL.md")))
    return found


def _skill_files(skill_dir: Path) -> list[Path]:
    """Every file belonging to a skill, so companions (references/) travel too."""
    return sorted(p for p in skill_dir.rglob("*") if p.is_file())


def _plan_skills(root: Path, skills_dir: Path) -> list[tuple[Path, str]]:
    """Mirror every skill tree (SKILL.md + references/examples/scripts)."""
    plan: list[tuple[Path, str]] = []
    for skill in discover_skills(root):
        for source in _skill_files(skill):
            relative = source.relative_to(skill)
            target = skills_dir / skill.name / relative
            plan.append((target, source.read_text(encoding="utf-8")))
    return plan


def _plan_opencode(root: Path, config_dir: Path) -> list[tuple[Path, str]]:
    """Plugin + mirrored skill trees for opencode."""
    source = root / "harnesses/opencode/bootstrap/coacus.js"
    content = source.read_text(encoding="utf-8").replace(
        "__COACUS_ROOT__", root.as_posix()
    )
    plan: list[tuple[Path, str]] = [(config_dir / "plugins" / "coacus.js", content)]
    plan += _plan_skills(root, config_dir / "skills")
    return plan


def _plan_claude(root: Path, config_dir: Path) -> list[tuple[Path, str]]:
    """Skills + a hook plugin whose script path matches the generated hooks.json."""
    plan = _plan_skills(root, config_dir / "skills")
    plugin = config_dir / "plugins" / "coacus"
    plan.append(
        (
            plugin / ".claude-plugin" / "plugin.json",
            json.dumps(
                {
                    "name": "coacus",
                    "description": "Coacus agentic framework bootstrap",
                    "version": "0.1.0",
                    "hooks": "./hooks/hooks.json",
                },
                indent=2,
            )
            + "\n",
        )
    )
    # hooks.json commands "${CLAUDE_PLUGIN_ROOT}/bootstrap/session-start.sh",
    # so the script MUST land under bootstrap/ (not hooks/).
    plan.append(
        (
            plugin / "hooks" / "hooks.json",
            (root / "harnesses/claude-code/bootstrap/hooks.json").read_text(encoding="utf-8"),
        )
    )
    plan.append(
        (
            plugin / "bootstrap" / "session-start.sh",
            (root / "harnesses/claude-code/bootstrap/session-start.sh").read_text(
                encoding="utf-8"
            ),
        )
    )
    return plan


def _plan_antigravity(root: Path, config_dir: Path) -> list[tuple[Path, str]]:
    plugin = config_dir / "config" / "plugins" / "coacus"
    plan = _plan_skills(root, plugin / "skills")
    for name in ("plugin.json", "ANTIGRAVITY.md"):
        source = root / "harnesses/antigravity/bootstrap" / name
        plan.append((plugin / name, source.read_text(encoding="utf-8")))
    return plan


def plan(harness: str, root: Path, config_dir: Path) -> list[tuple[Path, str]]:
    if harness == "opencode":
        return _plan_opencode(root, config_dir)
    if harness == "claude-code":
        return _plan_claude(root, config_dir)
    if harness == "antigravity":
        return _plan_antigravity(root, config_dir)
    if harness == "codex":
        return _plan_skills(root, config_dir / "skills")
    return []


def _register_antigravity_path(config_dir: Path, plugin_dir: Path) -> None:
    """Add the plugin path to <config_dir>/config/plugins.json (backup first)."""
    registry = config_dir / "config" / "plugins.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    data: dict = {"entries": []}
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {"entries": []}
        shutil.copy2(registry, registry.with_suffix(".json.bak"))
    entries = data.setdefault("entries", [])
    if not any(e.get("path") == plugin_dir.as_posix() for e in entries):
        entries.append({"path": plugin_dir.as_posix()})
    registry.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def install(
    harness: str, root: Path, config_dir: Path, dry_run: bool
) -> dict[str, object]:
    files = plan(harness, root, config_dir)
    if dry_run:
        return {"harness": harness, "files": [str(t) for t, _ in files], "dry_run": True}
    written: list[str] = []
    for target, content in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(target.as_posix())
    if harness == "antigravity":
        _register_antigravity_path(config_dir, config_dir / "config" / "plugins" / "coacus")
    manifest = config_dir / MANIFEST_NAME
    manifest.write_text(
        json.dumps({"harness": harness, "files": written}, indent=2) + "\n",
        encoding="utf-8",
    )
    return {"harness": harness, "files": written, "manifest": manifest.as_posix()}


def _contained(path: Path, root: Path) -> bool:
    """True only if ``path`` resolves inside ``root`` (blocks manifest tampering)."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def uninstall(harness: str, config_dir: Path, dry_run: bool = False) -> dict[str, object]:
    manifest = config_dir / MANIFEST_NAME
    if not manifest.is_file():
        return {"harness": harness, "removed": [], "note": "no manifest"}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    planned: list[str] = []
    skipped: list[str] = []
    for path in data.get("files", []):
        target = Path(path)
        if not _contained(target, config_dir):
            skipped.append(path)
            continue
        if target.is_file():
            if not dry_run:
                target.unlink()
            planned.append(path)
    if not dry_run:
        manifest.unlink()
    return {"harness": harness, "removed": planned, "skipped": skipped, "dry_run": dry_run}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus-install", description=__doc__)
    parser.add_argument(
        "harness",
        choices=["opencode", "claude-code", "antigravity", "codex", "cursor", "all"],
    )
    parser.add_argument("--config-dir", help="override the harness config directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)

    if args.harness == "cursor":
        print("cursor: no live SessionStart hook; render deferred (see docs/install.md)")
        return 0

    harnesses = (
        ["opencode", "claude-code", "antigravity", "codex"]
        if args.harness == "all"
        else [args.harness]
    )
    results = []
    for harness in harnesses:
        config_dir = Path(args.config_dir) if args.config_dir else default_config_dir(
            harness, _home()
        )
        if args.uninstall:
            results.append(uninstall(harness, config_dir, dry_run=args.dry_run))
        else:
            results.append(install(harness, ROOT, config_dir, args.dry_run))
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
