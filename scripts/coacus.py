#!/usr/bin/env python3
"""Coacus thin CLI: generate | check | validate.

Deterministic build tooling for the framework (ADR-0004, ADR-0013, ADR-0014).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.generators import agent_manifests, catalog  # noqa: E402
from engine.validators import agents as agent_validator  # noqa: E402
from engine.validators import hygiene  # noqa: E402


def cmd_generate(_args: argparse.Namespace) -> int:
    errors = agent_validator.validate(ROOT) + hygiene.validate(ROOT)
    if errors:
        print("cannot generate: validation failed")
        for item in errors:
            print(f"  {item}")
        return 1
    written = agent_manifests.write_all(ROOT)
    catalog_path = catalog.write(ROOT)
    print(f"generated {len(written)} manifest file(s)")
    print(f"generated {catalog_path.relative_to(ROOT)}")
    return 0


def cmd_check(_args: argparse.Namespace) -> int:
    drift = agent_manifests.check(ROOT) + catalog.check(ROOT)
    if drift:
        print("DRIFT detected — run: python3 scripts/coacus.py generate")
        for item in drift:
            print(f"  {item}")
        return 1
    print("no drift: generated artifacts are up to date")
    return 0


def cmd_validate(_args: argparse.Namespace) -> int:
    errors = agent_validator.validate(ROOT) + hygiene.validate(ROOT)
    if errors:
        print(f"{len(errors)} validation error(s):")
        for item in errors:
            print(f"  {item}")
        return 1
    print("validation OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="regenerate dist/, .agents/ and catalog/")
    sub.add_parser("check", help="fail if generated artifacts are stale")
    sub.add_parser("validate", help="run schema and hygiene validators")
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "check":
        return cmd_check(args)
    return cmd_validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
