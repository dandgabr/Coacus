#!/usr/bin/env python3
"""Architecture-SI vertical CLI: document ingestion and analysis (F6c).

Unifies the former `pdf2md` / `doc2md` / `doc-analyze` entrypoints over one
dispatcher (knowledge-ingestion):

    coacus_vertical.py ingest  <file|--dir DIR> [output] [--toc-only] [--split-chapters]
    coacus_vertical.py analyze <file|--dir DIR> [--json]
    coacus_vertical.py formats
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import dispatcher  # noqa: E402
from verticals.architecture_si.pipelines.analyze import analyzer  # noqa: E402


def _cmd_formats() -> int:
    dispatcher.load_handlers()
    print("Supported formats:", ", ".join(dispatcher.supported_extensions()))
    return 0


def _cmd_ingest(args: argparse.Namespace) -> int:
    dispatcher.load_handlers()
    options = {"toc_only": args.toc_only, "split_chapters": args.split_chapters}
    if args.dir:
        directory = Path(args.dir)
        if not directory.is_dir():
            print(f"not found: {directory}")
            return 1
        files = sorted(f for f in directory.iterdir() if f.is_file())
        print(f"ingesting {len(files)} file(s) from {directory}")
        seen: dict[str, str] = {}
        for path in files:
            try:
                outputs = dispatcher.convert(str(path), **options)
                print(f"  {path.name} -> {outputs}")
            except (ValueError, FileNotFoundError, RuntimeError) as exc:
                print(f"  {path.name}: skipped ({exc})")
        return 0
    try:
        result = dispatcher.convert(args.input_path, args.output_path, **options)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}")
        return 1
    print(f"converted: {result}")
    return 0


def _cmd_analyze(args: argparse.Namespace) -> int:
    from dataclasses import asdict
    import json

    if args.dir:
        print(analyzer.analyze_dir(args.dir, args.json))
        return 0
    result = analyzer.analyze_markdown(args.input_path)
    print(
        json.dumps(asdict(result), indent=2, ensure_ascii=False)
        if args.json
        else analyzer.human_report(result)
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus-vertical", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="convert a document to Markdown")
    ingest.add_argument("input_path", nargs="?")
    ingest.add_argument("output_path", nargs="?")
    ingest.add_argument("--dir")
    ingest.add_argument("--toc-only", action="store_true")
    ingest.add_argument("--split-chapters", action="store_true")

    analyze = sub.add_parser("analyze", help="analyze a Markdown document")
    analyze.add_argument("input_path", nargs="?")
    analyze.add_argument("--dir")
    analyze.add_argument("--json", action="store_true")

    sub.add_parser("formats", help="list supported input formats")

    args = parser.parse_args(argv)
    if args.command == "formats":
        return _cmd_formats()
    if args.command == "ingest":
        return _cmd_ingest(args)
    return _cmd_analyze(args)


if __name__ == "__main__":
    raise SystemExit(main())
