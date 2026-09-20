"""HTML to Markdown, with a regex fallback when BeautifulSoup is unavailable."""

from __future__ import annotations

import html as html_module
import re
from pathlib import Path

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common


def convert_html_to_md(html_path: str) -> str:
    with open(html_path, "r", encoding="utf-8", errors="replace") as handle:
        html = handle.read()
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # Fallback without BeautifulSoup: strip whole elements with a
        # non-backtracking dotall pattern (avoids the bad-tag-filter warning).
        text = re.sub(r"<script\b[^>]*>.*?</script\s*>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style\b[^>]*>.*?</style\s*>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "\n", text)
        text = html_module.unescape(text)
        return re.sub(r"\n{3,}", "\n\n", text)

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title else Path(html_path).stem
    md_lines = [f"# {title}\n"]
    for elem in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "pre", "table"]):
        if elem.name in ("h1", "h2", "h3"):
            level = elem.name[1]
            md_lines.append(f"\n{'#' * int(level)} {elem.get_text().strip()}\n")
        elif elem.name == "p":
            text = elem.get_text().strip()
            if text:
                md_lines.append(f"{text}\n")
        elif elem.name in ("ul", "ol"):
            for li in elem.find_all("li"):
                md_lines.append(f"- {li.get_text().strip()}")
        elif elem.name == "pre":
            md_lines.append(f"```\n{elem.get_text().strip()}\n```\n")
        elif elem.name == "table":
            rows = []
            for tr in elem.find_all("tr"):
                cells = [
                    td.get_text().strip().replace("\n", " ")
                    for td in tr.find_all(["td", "th"])
                ]
                if cells:
                    rows.append(cells)
            if rows:
                md_lines.append("\n" + common.format_markdown_table(rows) + "\n")
    return "\n".join(md_lines)


@register_converter(".html", ".htm")
def handle_html(input_path: str, output_path: str | None = None) -> str:
    return common.write_markdown(convert_html_to_md(input_path), output_path, input_path)
