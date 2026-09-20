"""HTML to Markdown, with a stdlib HTMLParser fallback when BeautifulSoup is absent."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from engine.dispatcher import register_converter

from verticals.architecture_si.pipelines.ingest.handlers import _common as common


class _TextExtractor(HTMLParser):
    """Extract visible text without pulling in a parser dependency.

    Using the stdlib parser (not tag regexes) keeps the fallback correct and
    avoids CodeQL's `bad-tag-filter` finding.
    """

    _SKIP = {"script", "style", "nav", "footer", "head"}

    def __init__(self) -> None:
        """Initialize the extractor with an empty buffer and no skip depth."""
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        """Track skipped subtrees and emit a line break for block-level tags."""
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        """Leave a skipped subtree when its closing tag arrives."""
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        """Buffer visible text, ignoring whitespace-only runs and skipped tags."""
        if not self._skip_depth and data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        """Return the buffered text with runs of blank lines collapsed."""
        return re.sub(r"\n{3,}", "\n\n", "\n".join(self.parts)).strip()


def convert_html_to_md(html_path: str) -> str:
    """Convert an HTML file to Markdown, preferring BeautifulSoup when present."""
    with open(html_path, "r", encoding="utf-8", errors="replace") as handle:
        html = handle.read()
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        parser = _TextExtractor()
        parser.feed(html)
        return parser.text()

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
    """Convert an HTML file to Markdown and return the written path."""
    return common.write_markdown(convert_html_to_md(input_path), output_path, input_path)
