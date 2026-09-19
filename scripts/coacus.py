#!/usr/bin/env python3
"""Coacus thin CLI: generate | check | validate.

Deterministic build tooling for the framework (ADR-0004, ADR-0013, ADR-0014).

Validation is split in two layers:
- SOURCE errors (agents, skills, hygiene) gate ``generate`` — invalid canonical
  sources never produce committed artifacts.
- ARTIFACT errors (discovery manifests, provenance) validate the GENERATED
  outputs. They run AFTER writing in ``generate`` (a stale discovery
  fingerprint is exactly what regeneration fixes), and alongside sources in
  ``validate``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import provenance  # noqa: E402
from engine.generators import (  # noqa: E402
    agent_manifests,
    bootstrap,
    catalog,
    discovery,
    mcp_configs,
)
from engine.validators import agents as agent_validator  # noqa: E402
from engine.validators import discovery as discovery_validator  # noqa: E402
from engine.validators import hygiene  # noqa: E402
from engine.validators import mcps as mcp_validator  # noqa: E402
from engine.validators import skills as skill_validator  # noqa: E402


def source_errors(root: Path) -> list[str]:
    """Canonical-source contract violations (block generation)."""
    return (
        agent_validator.validate(root)
        + skill_validator.validate(root)
        + mcp_validator.validate(root)
        + hygiene.validate(root)
    )


def artifact_errors(root: Path) -> list[str]:
    """Generated-artifact violations (checked after writing / on validate)."""
    return discovery_validator.validate(root) + provenance.validate(root)


def _warnings(root: Path) -> list[str]:
    return skill_validator.warnings(root)


def _print(items: list[str], label: str) -> None:
    for item in items:
        print(f"  [{label}] {item}")


def cmd_generate(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    root = root or ROOT
    errors = source_errors(root)
    if errors:
        print("cannot generate: source validation failed")
        _print(errors, "error")
        return 1
    written = (
        agent_manifests.write_all(root)
        + mcp_configs.write_all(root)
        + bootstrap.write_all(root)
        + discovery.write_all(root)
    )
    written_paths = catalog.write(root)
    print(f"generated {len(written)} manifest/bootstrap file(s)")
    for path in written_paths:
        print(f"generated {path.relative_to(root)}")
    warnings = _warnings(root)
    if warnings:
        _print(warnings, "warn")
    after = artifact_errors(root)
    if after:
        print("generated artifacts remain inconsistent:")
        _print(after, "error")
        return 1
    return 0


def cmd_check(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    root = root or ROOT
    drift = (
        agent_manifests.check(root)
        + mcp_configs.check(root)
        + bootstrap.check(root)
        + discovery.check(root)
        + catalog.check(root)
    )
    if drift:
        print("DRIFT detected — run: python3 scripts/coacus.py generate")
        _print(drift, "drift")
        return 1
    print("no drift: generated artifacts are up to date")
    return 0


def cmd_toon(args: argparse.Namespace) -> int:
    from engine import toon  # noqa: E402

    path = Path(args.path)
    if not path.is_file():
        print(f"not found: {path}")
        return 1
    errors = toon.validate(path.read_text(encoding="utf-8"))
    if errors:
        print(f"{len(errors)} TOON error(s):")
        _print(errors, "error")
        return 1
    print("TOON payload OK")
    return 0


def cmd_validate(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    root = root or ROOT
    warnings = _warnings(root)
    if warnings:
        _print(warnings, "warn")
    errors = source_errors(root) + artifact_errors(root)
    if errors:
        print(f"{len(errors)} validation error(s):")
        _print(errors, "error")
        return 1
    print("validation OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="regenerate dist/, .agents/ and catalog/")
    sub.add_parser("check", help="fail if generated artifacts are stale")
    sub.add_parser("validate", help="run schema and hygiene validators")
    toon = sub.add_parser("toon", help="validate a TOON handoff payload file")
    toon.add_argument("path", help="path to a file containing a TOON payload")
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "check":
        return cmd_check(args)
    if args.command == "toon":
        return cmd_toon(args)
    return cmd_validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
