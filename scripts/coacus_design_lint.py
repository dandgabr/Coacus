#!/usr/bin/env python3
"""Coacus Design Linter CLI: Detect AI-slop visual anti-patterns in frontend code.

Portable Python 3.10+ standard library script. Zero external dependencies.
Usage:
    python3 scripts/coacus_design_lint.py <file-or-directory> [--strict] [--json]
    python3 scripts/coacus_design_lint.py --test
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add project root to sys.path so engine modules import cleanly
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.validators.design_craft import (
    DesignFinding,
    scan_directory,
    scan_file,
    scan_text,
)


def _run_self_tests() -> int:
    sample_bad = """
    <div className="bg-blue-600 text-slate-400 p-4">
      <div className="rounded-full border px-3 py-1 bg-white/10 text-xs">✨ Introducing v2.0</div>
      <h1>Build the <span className="font-serif italic text-purple-400">Future</span> Today</h1>
      <div className="from-indigo-500 to-purple-600 bg-gradient-to-r p-6">
        <div className="rounded-xl p-3 bg-indigo-50"><svg className="w-6 h-6" /></div>
        <h3>Feature title</h3>
      </div>
      <p>Seamlessly integrate — elevate workflows — supercharge speed — transform results.</p>
    </div>
    """
    findings = scan_text(sample_bad, "sample_bad.tsx")
    rule_ids = {f.rule_id for f in findings}
    expected = {
        "gray-on-color",
        "hero-eyebrow",
        "italic-serif",
        "ai-color-palette",
        "icon-tile",
        "em-dash-overuse",
    }
    missing = expected - rule_ids
    if missing:
        print(f"FAILED self-tests: missing detected rule(s): {missing}", file=sys.stderr)
        return 1

    sample_good = """
    <section className="bg-neutral-900 text-neutral-100 p-8">
      <p className="text-xs font-semibold tracking-wider uppercase text-amber-400">Release Notes</p>
      <h1 className="font-sans text-3xl font-bold tracking-tight">System Architecture Overview</h1>
      <div className="p-6 border border-white/10 rounded-lg">
        <h3 className="text-lg font-medium">Modular Ingestion Pipeline</h3>
        <p className="text-sm text-neutral-400 mt-2">Zero dependencies, portable runtime engine.</p>
      </div>
    </section>
    """
    clean_findings = scan_text(sample_good, "sample_good.tsx")
    if clean_findings:
        print(f"FAILED self-tests: false positive on clean code: {clean_findings}", file=sys.stderr)
        return 1

    print(f"OK: self-tests passed ({len(findings)} anti-patterns correctly detected).")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for scanning frontend code for design anti-patterns."""
    parser = argparse.ArgumentParser(
        description="Scan frontend code for generic AI design anti-patterns."
    )
    parser.add_argument("target", nargs="?", default=".", help="File or directory to scan")
    parser.add_argument("--test", action="store_true", help="Run self-tests and exit")
    parser.add_argument("--strict", action="store_true", help="Fail with non-zero exit code on any finding")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON array")
    args = parser.parse_args(argv)

    if args.test:
        return _run_self_tests()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"Error: target path does not exist: {target_path}", file=sys.stderr)
        return 2

    if target_path.is_file():
        findings = scan_file(target_path)
    else:
        findings = scan_directory(target_path)

    if args.json:
        data = [
            {
                "rule_id": f.rule_id,
                "message": f.message,
                "line": f.line,
                "file": f.file_path,
                "severity": f.severity,
            }
            for f in findings
        ]
        print(json.dumps(data, indent=2))
        return 1 if (findings and args.strict) else 0

    if not findings:
        print(f"No design anti-patterns detected in {args.target}.")
        return 0

    print(f"Found {len(findings)} design craft finding(s) in {args.target}:\n")
    for f in findings:
        print(f"  {f.format_line()}")

    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
