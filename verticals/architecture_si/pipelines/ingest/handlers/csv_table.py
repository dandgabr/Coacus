"""CSV / TSV to a Markdown table."""

from __future__ import annotations

import csv
from pathlib import Path

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common


@register_converter(".csv", ".tsv")
def handle_csv(input_path: str, output_path: str | None = None) -> str:
    """Convert a CSV/TSV file to a Markdown table and return the written path."""
    with open(input_path, "r", encoding="utf-8", errors="replace") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        delimiter = ";" if sample.count(";") > sample.count(",") else ","
        rows = list(csv.reader(handle, delimiter=delimiter))
    if not rows:
        return common.write_markdown(
            f"# {Path(input_path).stem}\n\n_Empty file._", output_path, input_path
        )
    md = f"# {Path(input_path).stem}\n\n" + common.format_markdown_table(rows)
    return common.write_markdown(md, output_path, input_path)
