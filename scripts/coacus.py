#!/usr/bin/env python3
"""Coacus thin CLI: generate | check | validate.

Deterministic build tooling for the framework (generated-artifacts, secrets-portability, generated-artifacts).

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
    docstrings,
    mcp_configs,
    routing,
)
from engine.validators import agents as agent_validator  # noqa: E402
from engine.validators import completeness as completeness_validator  # noqa: E402
from engine.validators import discovery as discovery_validator  # noqa: E402
from engine.validators import docs as docs_validator  # noqa: E402
from engine.validators import evals as eval_validator  # noqa: E402
from engine.validators import freshness as freshness_validator  # noqa: E402
from engine.validators import hygiene  # noqa: E402
from engine.validators import language as language_validator  # noqa: E402
from engine.validators import mcps as mcp_validator  # noqa: E402
from engine.validators import routing as routing_validator  # noqa: E402
from engine.validators import skills as skill_validator  # noqa: E402


def source_errors(root: Path) -> list[str]:
    """Canonical-source contract violations (block generation)."""
    return (
        agent_validator.validate(root)
        + skill_validator.validate(root)
        + mcp_validator.validate(root)
        + hygiene.validate(root)
        + eval_validator.validate(root)
        + freshness_validator.validate(root)
        + routing_validator.validate_sources(root)
    )


def artifact_errors(root: Path) -> list[str]:
    """Generated-artifact violations (checked after writing / on validate)."""
    return (
        discovery_validator.validate(root)
        + provenance.validate(root)
        + docs_validator.validate(root)
        + routing_validator.validate_index(root)
    )


def _warnings(root: Path) -> list[str]:
    return skill_validator.warnings(root) + language_validator.validate(root)


def _print(items: list[str], label: str) -> None:
    for item in items:
        print(f"  [{label}] {item}")


def cmd_generate(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    """Regenerate every derived artifact; return a non-zero exit on failure."""
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
        + routing.write_all(root)
    )
    written_paths = catalog.write(root) + [docstrings.write(root)]
    from datetime import datetime, timezone  # noqa: E402

    authored = provenance.sync_authoring(
        root, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    if authored:
        print(f"recorded {len(authored)} authored provenance entrie(s)")
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
    """Fail if any generated artifact has drifted from its source."""
    root = root or ROOT
    drift = (
        agent_manifests.check(root)
        + mcp_configs.check(root)
        + bootstrap.check(root)
        + discovery.check(root)
        + routing.check(root)
        + catalog.check(root)
        + docstrings.check(root)
    )
    if drift:
        print("DRIFT detected — run: python3 scripts/coacus.py generate")
        _print(drift, "drift")
        return 1
    print("no drift: generated artifacts are up to date")
    return 0


def cmd_toon(args: argparse.Namespace) -> int:
    """Validate a TOON handoff payload file; print errors and return the exit code."""
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


def cmd_completeness(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    """Reconcile the corpus against its sources; fail if anything is unreconciled."""
    root = root or ROOT
    gaps = completeness_validator.validate(root)
    if gaps:
        print(f"{len(gaps)} completeness gap(s):")
        _print(gaps, "gap")
        return 1
    print("completeness OK: nothing left behind")
    return 0


def cmd_freshness(args: argparse.Namespace, root: Path | None = None) -> int:
    """Read-only, offline inventory of moving version pins (version-freshness)."""
    root = root or ROOT
    rows = freshness_validator.report(root, include_references=args.references)
    unresolved = [r for r in rows if r.startswith("UNRESOLVED")]
    print(f"{len(rows)} version pin(s); {len(unresolved)} unresolved")
    for row in rows:
        print(f"  {row}")
    return 1 if unresolved else 0


def cmd_validate(_args: argparse.Namespace | None = None, root: Path | None = None) -> int:
    """Run the schema and hygiene validators; fail on any error."""
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
    """Parse arguments and dispatch to the selected subcommand."""
    parser = argparse.ArgumentParser(prog="coacus", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="regenerate dist/, .agents/, catalog/ and docs/")
    sub.add_parser("check", help="fail if generated artifacts are stale")
    sub.add_parser("validate", help="run schema and hygiene validators")
    sub.add_parser("completeness", help="verify nothing from the sources was left behind (F8)")
    fresh = sub.add_parser("freshness", help="read-only inventory of version pins (version-freshness)")
    fresh.add_argument("--references", action="store_true", help="also scan references/ assets")
    toon = sub.add_parser("toon", help="validate a TOON handoff payload file")
    toon.add_argument("path", help="path to a file containing a TOON payload")
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "check":
        return cmd_check(args)
    if args.command == "completeness":
        return cmd_completeness(args)
    if args.command == "freshness":
        return cmd_freshness(args)
    if args.command == "toon":
        return cmd_toon(args)
    return cmd_validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
