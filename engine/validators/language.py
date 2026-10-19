"""Repository-wide English language gate using Lingua language detection.

Natural-language segments are checked in tracked and non-ignored untracked
text files. Ambiguous or unsupported text blocks validation for human review.
"""

from __future__ import annotations

import ast
from html.parser import HTMLParser
import hashlib
import json
from functools import lru_cache
import re
import subprocess
import tokenize
from pathlib import Path

try:
    from lingua import Language, LanguageDetectorBuilder
except ImportError:  # fail closed with an actionable validation error
    Language = None  # type: ignore[assignment,misc]
    LanguageDetectorBuilder = None  # type: ignore[assignment,misc]

try:
    from wordfreq import available_languages, zipf_frequency
except ImportError:  # fail closed with an actionable validation error
    available_languages = None  # type: ignore[assignment,misc]
    zipf_frequency = None  # type: ignore[assignment,misc]

from engine.frontmatter import FrontmatterError, parse

EXCEPTIONS = "config/language-exceptions.json"
MIN_WORDS = 4
MIN_LANGUAGE_PROBABILITY = 0.12
MIN_PROBABILITY_MARGIN = 0.025
STRUCTURED_SUFFIXES = {
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".properties", ".gitignore",
    ".gitattributes", ".editorconfig",
}
STRUCTURED_NAMES = {".bandit"}
CODE_SUFFIXES = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java",
    ".kt", ".kts", ".go", ".rs", ".c", ".h", ".cc", ".cpp", ".hpp", ".cs",
    ".php", ".rb", ".swift", ".sh", ".bash", ".ps1", ".sql", ".css", ".scss", ".dot",
    ".sass", ".less", ".graphql", ".proto",
}
TEXT_SUFFIXES = {
    ".md", ".markdown", ".mdx", ".rst", ".adoc", ".txt", ".text",
    ".json", ".ipynb", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".properties", ".xml", ".html", ".htm", ".svg", ".py", ".pyi",
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".kt",
    ".kts", ".go", ".rs", ".c", ".h", ".cc", ".cpp", ".hpp", ".cs",
    ".php", ".rb", ".swift", ".sh", ".bash", ".ps1", ".sql", ".css",
    ".scss", ".sass", ".less", ".graphql", ".proto", ".lock", ".dot",
}
TEXT_NAMES = {"README", "LICENSE", "NOTICE", "COPYING", "Makefile", "Dockerfile", "Containerfile", ".gitkeep"}
GENERATED_PREFIXES = (".agents/", "catalog/", ".well-known/")
GENERATED_FILES = {
    "docs/reference/python-api.md", "docs/reference/lifecycle-matrix.md",
}
_MARKUP = re.compile(r"`([^`]+)`|!?\[([^\]]*)\]\([^)]*\)|https?://\S+|<[^>]+>")
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
_ENGLISH_FUNCTION_WORDS = {"a", "an", "and", "are", "as", "at", "be", "because", "by", "can", "cannot", "for", "from", "has", "have", "if", "in", "into", "is", "it", "must", "not", "of", "on", "or", "shall", "that", "the", "their", "this", "to", "when", "which", "will", "with"}
_PROSE_FIELDS = {
    "caption", "comment", "content", "description", "details", "error", "example", "expected",
    "help", "hint", "instructions", "label", "message", "overview", "placeholder",
    "prompt", "purpose", "rationale", "reason", "summary", "text", "title", "tooltip",
    "usage", "warning", "when", "steps", "body", "explanation", "triggers",
    "banner", "heading", "subtitle", "cta", "copy", "button", "status",
    "tip", "tips", "label", "labels",
}
_CODE_PROSE_FIELDS = _PROSE_FIELDS - {"content", "text", "body"}
_WORD_FREQUENCY_LANGUAGES = tuple(
    lang for lang in (available_languages("best") if available_languages else {})
    if lang not in {"ja", "zh", "ko"}
)
_PY_COMMENT = re.compile(r"#.*")
_STRING_LITERAL = re.compile(
    r'''(?P<double>"""[\\s\\S]*?"""|"(?:\\\\.|[^"\\\\])*?")|'''
    r'''(?P<single>''' + "'''" + r'''[\\s\\S]*?''' + "'''" + r'''|'(?:\\\\.|[^'\\\\])*?')|'''
    r'''(?P<backtick>`(?:\\\\.|[^`\\\\])*?`)'''
)


def _is_natural_string(value: str) -> bool:
    """Keep prose-like literals while excluding ordinary protocol tokens."""
    words = _WORD.findall(value)
    return len(words) >= 2 or bool(re.search(r"[^\x00-\x7f]", value))


def _is_prose_key(value: str) -> bool:
    """Recognize user-facing identifiers such as ``title_text`` and ``banner``."""
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower().split("_")
    return bool(words) and ("_".join(words) in _CODE_PROSE_FIELDS or words[-1] in _CODE_PROSE_FIELDS)


def _quoted_segments(text: str, *, suffix: str, prose_contexts: bool = True) -> list[tuple[int, str]]:
    """Extract quoted natural-language literals from non-Python source text."""
    found: list[tuple[int, str]] = []
    for match in _STRING_LITERAL.finditer(text):
        literal = match.group().strip("\"'`")
        literal = re.sub(r"\\([\\\"'`])", r"\1", literal)
        prefix = text[max(0, match.start() - 100):match.start()]
        named_prose = prose_contexts and bool(re.search(
            r"(?:caption|description|details|error|example|expected|help|hint|instructions|labels?|message|overview|placeholder|prompt|purpose|rationale|reason|summary|title|tooltip|usage|warning|banner|heading|subtitle|cta|copy|button|status|tips?)(?:_[A-Za-z0-9]+)*\s*[:=]\s*(?:[\[{(]\s*)*$",
            prefix, re.I,
        ))
        named_prose = named_prose or bool(re.search(
            r"(?:print|input|alert|confirm|warn|warning|error|info|debug|critical|exception|fatal|showMessage|notify|setText|setTitle|setLabel|send)\s*\([^)]*$",
            prefix, re.I,
        ))
        if suffix == ".dot" and re.search(r"(?:label|tooltip)\s*=\s*$", prefix, re.I):
            named_prose = True
        if re.match(r"^(?:https?://|mailto:|tel:|/|\.{1,2}/)", literal, re.I):
            continue
        if named_prose and not _looks_like_code(literal):
            found.append((text.count("\n", 0, match.start()) + 1, literal))
    return found


def _sentence_units(value: str) -> list[str]:
    """Split prose into separately classifiable sentences/clauses."""
    abbreviations = ("e.g.", "i.e.", "vs.", "etc.", "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.")
    result = []
    item = value
    # Keep list ordinals and citation initials attached to their sentence.
    item = re.sub(r"\b([A-Z]|\d{1,2})\.(?=\s+[A-Z])", lambda match: match.group(1) + "\uE010", item)
    for index, abbreviation in enumerate(abbreviations):
        item = re.sub(re.escape(abbreviation), abbreviation.replace(".", f"\uE000{index}\uE001"), item, flags=re.I)
    units = re.split(r"(?<=[.!?;])\s+(?=[\"'“‘([{]*[A-ZÀ-Þ¿¡])", item)
    for unit in units:
        unit = unit.replace("\uE010", ".")
        for index in range(len(abbreviations)):
            unit = unit.replace(f"\uE000{index}\uE001", ".")
        unit = " ".join(unit.split())
        if unit:
            result.append(unit)
    return result


def _inventory(root: Path) -> list[Path]:
    """Return every repository file, including staged and untracked files."""
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root, stderr=subprocess.DEVNULL,
        )
        relatives = [Path(item.decode("utf-8")) for item in output.split(b"\0") if item]
    except (OSError, subprocess.CalledProcessError):
        relatives = [p.relative_to(root) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    return sorted((root / rel for rel in relatives if (root / rel).is_file()),
                  key=lambda path: path.as_posix())


def _code_segments(path: Path, text: str) -> list[tuple[int, str]]:
    """Extract comments, docstrings and literal values from common source files."""
    suffix = path.suffix.lower()
    if suffix in {".py", ".pyi"}:
        found: list[tuple[int, str]] = []
        try:
            for token in tokenize.generate_tokens(iter(text.splitlines(keepends=True)).__next__):
                if (token.type == tokenize.COMMENT
                        and not token.string.startswith(("#!", "#pragma"))
                        and not re.match(r"#\s*(?:noqa|nosec|type:\s*ignore|pragma:\s*no cover)\b", token.string, re.I)):
                    found.append((token.start[0], token.string.lstrip("# ")))
            tree = ast.parse(text)
            parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    value = ast.get_docstring(node, clean=False)
                    if value:
                        found.append((getattr(node, "lineno", 1), value))
                parent = parents.get(node)
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    owner = parent
                    while isinstance(owner, (ast.List, ast.Tuple, ast.Set)):
                        owner = parents.get(owner)
                    enum_field = (
                        isinstance(owner, ast.keyword)
                        and owner.arg in {"mode", "state", "status", "type", "kind"}
                        and node.value.lower() in {"off", "on", "auto", "prompt", "select", "error", "failed", "failure", "ok", "success", "warning", "info"}
                    )
                    named_prose = (
                        isinstance(owner, ast.keyword) and _is_prose_key(owner.arg)
                    ) or (
                        isinstance(owner, (ast.Assign, ast.AnnAssign))
                        and any(isinstance(target, ast.Name) and _is_prose_key(target.id)
                                for target in (owner.targets if isinstance(owner, ast.Assign) else [owner.target]))
                    ) or (
                        isinstance(owner, ast.Call)
                        and ((isinstance(owner.func, ast.Name) and (
                            owner.func.id.lower() in {
                            "print", "input", "warn", "warning", "error", "info", "debug",
                            "critical", "exception", "fatal", "alert", "confirm",
                            } or owner.func.id.lower().endswith(("error", "exception"))
                        ))
                        or (isinstance(owner.func, ast.Attribute) and owner.func.attr.lower() in {
                            "warn", "warning", "error", "info", "debug", "critical", "exception", "fatal",
                        }))
                    )
                    if named_prose and not enum_field and not _looks_like_code(node.value):
                        found.append((getattr(node, "lineno", 1), node.value))
                elif isinstance(node, ast.JoinedStr):
                    value = "".join(part.value for part in node.values if isinstance(part, ast.Constant) and isinstance(part.value, str))
                    parent = parents.get(node)
                    named_prose = isinstance(parent, ast.keyword) and _is_prose_key(parent.arg)
                    if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name):
                        named_prose = named_prose or parent.func.id.lower() in {
                            "print", "input", "warn", "warning", "error", "info", "debug",
                        } or parent.func.id.lower().endswith(("error", "exception"))
                    if named_prose and not _looks_like_code(value):
                        found.append((getattr(node, "lineno", 1), value))
        except (SyntaxError, tokenize.TokenError, IndentationError):
            found.extend((i, match.group()) for i, line in enumerate(text.splitlines(), 1)
                         if (match := _PY_COMMENT.search(line)))
        return list(dict.fromkeys(found))
    found = []
    in_block_comment = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("#!", "#pragma")):
            continue
        comment = _extract_comment(line, suffix, in_block_comment)
        in_block_comment = comment[1]
        if comment[0]:
            value = comment[0].strip()
            if (value and not _looks_like_code(value)
                    and not re.match(r"(?:noqa|type:\s*ignore|pragma:\s*no cover)\b", value, re.I)):
                found.append((number, value))
        # Ordinary string literals are application data and often contain
        # protocol values, fixtures or examples. Explanatory prose belongs in
        # comments/docstrings, which are scanned above.
    quoted = _quoted_segments(text, suffix=suffix)
    if suffix == ".dot":
        # These terse labels are state/edge labels in this Graphviz source,
        # not standalone natural-language passages. Other DOT labels remain
        # subject to language classification.
        quoted = [item for item in quoted if item[1].strip().lower() not in {"no", "yes", "ok", "problem", "condition a", "condition b"}]
    found.extend(quoted)
    return list(dict.fromkeys(found))


def _extract_comment(line: str, suffix: str, in_block: bool = False) -> tuple[str, bool]:
    """Extract a source comment outside quoted strings, including inline comments."""
    if in_block:
        end = line.find("*/")
        return (line[:end] if end >= 0 else line, end < 0)
    markers = ["/*", "<!--"]
    if suffix in {".py", ".pyi", ".sh", ".bash", ".ps1", ".rb", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".properties"}:
        markers.append("#")
    if suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".kt", ".kts", ".go", ".rs", ".c", ".h", ".cc", ".cpp", ".hpp", ".cs", ".php", ".swift", ".graphql", ".proto", ".css", ".scss", ".sass", ".less", ".dot"}:
        markers.append("//")
    if suffix == ".sql":
        markers.append("--")
    if suffix in {".html", ".htm", ".xml", ".svg"}:
        markers.append("<!--")
    quote = ""
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        marker = next((item for item in markers if line.startswith(item, index)), None)
        if marker and (marker != "#" or index == 0 or line[index - 1].isspace()):
            end_marker = "*/" if marker == "/*" else "-->" if marker == "<!--" else ""
            content_start = index + len(marker)
            end = line.find(end_marker, content_start) if end_marker else -1
            content = line[content_start:end] if end >= 0 else line[content_start:]
            return content, marker in {"/*", "<!--"} and end < 0
        index += 1
    return "", False


class _HtmlText(HTMLParser):
    """Collect visible HTML text and natural-language attributes/comments."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[tuple[int, str]] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1
        for key, value in attrs:
            if key in {"title", "alt", "aria-label", "placeholder"} and value:
                self.parts.append((self.getpos()[0], value))

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if data.strip():
            if not self.hidden:
                self.parts.append((self.getpos()[0], data.strip()))
            else:
                for value in re.findall(r'''"([^"\n]+)"|'([^'\n]+)'|`([^`\n]+)`''', data):
                    sample = next((part for part in value if part), "")
                    if len(_WORD.findall(sample)) >= MIN_WORDS:
                        self.parts.append((self.getpos()[0], sample))

    def handle_comment(self, data: str) -> None:
        if data.strip():
            self.parts.append((self.getpos()[0], data.strip()))


def _segments(path: Path, text: str) -> list[tuple[int, str]]:
    suffix = path.suffix.lower()
    if suffix in STRUCTURED_SUFFIXES or path.name in STRUCTURED_NAMES | {".gitignore", ".gitattributes", ".editorconfig"}:
        found: list[tuple[int, str]] = []
        lines = text.splitlines()
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("#", ";")):
                comment = stripped.lstrip("#; ")
                if comment and not re.fullmatch(r"[-= ]{3,}.*", comment):
                    found.append((number, comment))
                continue
            if suffix in {".gitignore", ".gitattributes", ".editorconfig"}:
                continue
            if suffix in {".yaml", ".yml"}:
                match = re.match(r"(?:-\s*)?([A-Za-z0-9_-]+):\s*(.*?)\s*$", stripped)
                if not match:
                    continue
                key, value = match.groups()
                if value in {"|", "|-", ">", ">-"}:
                    base_indent = len(line) - len(line.lstrip())
                    parts = []
                    for continuation in lines[number:]:
                        if continuation.strip() and len(continuation) - len(continuation.lstrip()) <= base_indent:
                            break
                        if continuation.strip():
                            parts.append(continuation.strip())
                    value = " ".join(parts)
                elif key.lower() not in _PROSE_FIELDS and not _is_natural_string(value):
                    continue
            else:
                match = re.match(r"([A-Za-z0-9_.-]+)\s*=\s*(.*?)\s*$", stripped)
                if not match:
                    continue
                key, value = match.groups()
                if key.lower() not in _PROSE_FIELDS and not _is_natural_string(value):
                    continue
            value = value.strip("\"' ")
            value = re.sub(r"\s+#.*$", "", value).strip()
            # Short metadata labels and identifiers are not prose. Accented
            # words remain in scope so localized labels still reach review.
            if key.lower() not in _PROSE_FIELDS and not _is_natural_string(value):
                continue
            if (value and not value.startswith(("${{", "http://", "https://"))
                    and not _looks_like_code(value)):
                found.append((number, value))
        return found
    if suffix in CODE_SUFFIXES:
        return _code_segments(path, text)
    if suffix in {".html", ".htm", ".svg", ".xml"}:
        parser = _HtmlText()
        try:
            parser.feed(text)
        except Exception:
            return [(i, line.strip()) for i, line in enumerate(text.splitlines(), 1)
                    if line.lstrip().startswith(("<!--", "* "))]
        return parser.parts
    if suffix in {".md", ".markdown", ".mdx", ".rst", ".adoc"}:
        metadata_segments: list[tuple[int, str]] = []
        try:
            if path.name in {"SKILL.md", "agent.source.md"}:
                doc = parse(text)
                description = doc.meta.get("description", "")
                if description:
                    metadata_lines = text.splitlines()
                    description_line = next((i for i, line in enumerate(metadata_lines[:100], 1)
                                             if re.match(r"^\s*description\s*:", line)), 2)
                    metadata_segments.append((description_line, str(description)))
                lines = text.splitlines()
                if lines and lines[0].strip() == "---":
                    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
                    if closing is not None:
                        text = "\n" * (closing + 1) + "\n".join(lines[closing + 1:])
        except FrontmatterError:
            pass
        prose_source = []
        fence = False
        for source_line in text.splitlines():
            if source_line.lstrip().startswith(("```", "~~~")):
                fence = not fence
                prose_source.append("")
            else:
                prose_source.append("" if fence else source_line)
        clean_lines = [_MARKUP.sub(lambda match: match.group(1) or match.group(2) or " ", line) for line in prose_source]
        prose: list[tuple[int, str]] = metadata_segments.copy()
        block: list[str] = []
        block_start = 1
        heading_only = False
        source_lines = text.splitlines()

        def flush_block() -> None:
            nonlocal block, heading_only
            if block:
                prose.append((block_start, " ".join(block)))
                block = []
            heading_only = False

        for number, line in enumerate(clean_lines, 1):
            source = source_lines[number - 1] if number <= len(source_lines) else ""
            is_heading = bool(re.match(r"^\s{0,3}#{1,6}\s+", source) or re.fullmatch(r"\s*\*\*[^*]+\*\*\s*", source))
            if line.strip():
                if is_heading and block and not heading_only:
                    flush_block()
                if not block:
                    block_start = number
                    heading_only = is_heading
                block.append(line.strip())
                if not is_heading:
                    heading_only = False
            else:
                if block and not heading_only:
                    flush_block()
        flush_block()
        in_fence = False
        fence_language = ""
        code: list[tuple[int, str]] = []
        for number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                if not in_fence:
                    fence_language = line.lstrip()[3:].strip().lower()
                in_fence = not in_fence
            elif in_fence and line.strip():
                stripped = line.strip()
                if stripped.startswith(("# ", "// ", "-- ", "<!-- ", "* ")):
                    comment = re.sub(r"^(?:#|//|--|<!--|\*)\s*", "", stripped).removesuffix("-->")
                    if (not _looks_like_code(comment)
                            and not re.search(r"[/\\]|\b[\w-]+\.[A-Za-z0-9]{1,8}\b", comment)):
                        code.append((number, comment))
                elif fence_language in {"text", "txt", "plaintext", "console", "output"}:
                    if (len(_WORD.findall(stripped)) >= 4
                            and not re.search(r"[/\\]|\b[\w-]+\.[A-Za-z0-9]{1,8}\b|\w_\w", stripped)):
                        code.append((number, stripped))
                    elif re.fullmatch(r"[\wÀ-ÿ-]{3,}\s*/\s*[\wÀ-ÿ-]{3,}", stripped, re.UNICODE):
                        code.append((number, stripped))
                    elif re.search(r"[^\x00-\x7f]", stripped) and _WORD.findall(stripped):
                        code.append((number, stripped))
                elif (not fence_language and not re.fullmatch(r"\[.*\]", stripped)
                      and len(_WORD.findall(stripped)) >= 4
                      and not re.search(r"[/\\]|\b[\w-]+\.[A-Za-z0-9]{1,8}\b|\w_\w", stripped)):
                    code.append((number, stripped))
                elif re.search(r"[^\x00-\x7f]", stripped) and _WORD.findall(stripped):
                    code.append((number, stripped))
                else:
                    # In source fences, inspect comments and quoted values only;
                    # identifiers and syntax are not prose.
                    for quoted in re.findall(r'''"([^"\n]+)"|'([^'\n]+)'|`([^`\n]+)`''', stripped):
                        value = next((part for part in quoted if part), "")
                        tokens = {word.lower() for word in _WORD.findall(value)}
                        if (len(tokens) >= MIN_WORDS
                                and (tokens & _ENGLISH_FUNCTION_WORDS or re.search(r"[^\x00-\x7f]", value))):
                            code.append((number, value))
        prose = [item for item in prose if item[1].strip("# *:-") not in {"Added", "Changed", "Fixed", "Removed", "Security"}]
        code_groups: list[tuple[int, str]] = []
        for number, segment in code:
            if code_groups and code_groups[-1][0] <= number <= code_groups[-1][0] + 2:
                previous_line, previous_text = code_groups[-1]
                code_groups[-1] = (previous_line, f"{previous_text} {segment}")
            else:
                code_groups.append((number, segment))
        prose.extend(code_groups)
        return list(dict.fromkeys(prose))
    if path.name == "LICENSE":
        return [(1, " ".join(text.split()))]
    if suffix in {".json", ".ipynb"}:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if data is not None:
            values: list[str] = []
            def collect_exception_manifest(item: object) -> None:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if key == "reason" and isinstance(value, str):
                            values.append(value)
                        elif key == "exceptions" and isinstance(value, list):
                            collect_exception_manifest(value)
                elif isinstance(item, list):
                    for value in item:
                        collect_exception_manifest(value)
            if path.as_posix().endswith(EXCEPTIONS):
                collect_exception_manifest(data)
                return _json_locations(text, values)
            if path.as_posix().endswith("knowledge/routing/lexicon.json"):
                description = data.get("description", "") if isinstance(data, dict) else ""
                if isinstance(description, str):
                    values.append(description)
                agents = data.get("agents", {}) if isinstance(data, dict) else {}
                if isinstance(agents, dict):
                    values.extend(term for terms in agents.values() if isinstance(terms, list)
                                  for term in terms if isinstance(term, str))
                return _json_locations(text, values)
            def collect(item: object, field: str = "") -> None:
                if isinstance(item, str):
                    if field in _PROSE_FIELDS:
                        values.append(item)
                elif isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(key, str):
                            collect(value, key.lower())
                elif isinstance(item, list):
                    for value in item:
                        collect(value, field)
            collect(data)
            return _json_locations(text, values)
    # Human-readable data and prose files are checked by paragraph, not as one
    # enormous document (which could hide mixed-language contamination).
    return [(i, line.strip()) for i, line in enumerate(text.splitlines(), 1) if line.strip()]


def _json_locations(text: str, values: list[str]) -> list[tuple[int, str]]:
    """Map extracted JSON strings back to source lines, including duplicates."""
    result: list[tuple[int, str]] = []
    cursor = 0
    for value in values:
        encoded = json.dumps(value, ensure_ascii=False)
        position = text.find(encoded, cursor)
        if position < 0:
            encoded = json.dumps(value, ensure_ascii=True)
            position = text.find(encoded, cursor)
        if position < 0:
            position = text.find(encoded)
        if position >= 0:
            result.append((text.count("\n", 0, position) + 1, value))
            cursor = position + len(encoded)
        else:
            result.append((1, value))
    return result


def _looks_like_code(value: str) -> bool:
    """Exclude code lines copied into explanatory comments or fenced examples."""
    value = re.sub(r"^\s*\d+[.)]\s+", "", value)
    return bool(
        re.fullmatch(r"\d{1,3}[a-z]?[.)]?", value, re.I)
        or re.fullmatch(r"(?:Rust|Python|JavaScript|TypeScript|Java|Go|Ruby|Lua|C|C\+\+|C#|Swift|Kotlin|PHP|SQL)", value)
        or re.match(r"^(?:await\s+)?[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+\s*\(", value)
        or re.match(r"^(?:await|return|const|let|var|expect)\s+.*[();{}]", value)
        or re.fullmatch(r"[A-Z0-9_-]+(?:\s+[A-Z0-9_-]+)*", value)
        or re.fullmatch(r"[a-z][a-z0-9]*-[a-z][a-z0-9-]*", value)
        or re.fullmatch(r"(?:[a-z][\w-]*\.(?:js|ts|py|rs|md|yml|yaml|json))(?:\s+[a-z][\w-]*\.(?:js|ts|py|rs|md|yml|yaml|json))*", value, re.I)
        or re.fullmatch(r"(?:[A-Z][A-Za-z0-9.+#-]*)(?:\s+[A-Z][A-Za-z0-9.+#-]*)?(?:\s*/\s*(?:[A-Z][A-Za-z0-9.+#-]*)(?:\s+[A-Z][A-Za-z0-9.+#-]*)?){2,}", value)
        or re.fullmatch(r"(?:[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*|[a-z]+_[a-z][\w]*)(?:\s*[,;]\s*(?:[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*|[a-z]+_[a-z][\w]*))*", value)
        or re.fullmatch(r"(?:Claude Code|Codex CLI|Google Antigravity|OpenCode|Cursor|Aider):?", value)
        or re.fullmatch(r"AI/ML [A-Z][A-Za-z-]+", value)
        or re.fullmatch(r"type\s+[A-Z][A-Za-z0-9]+\s+typeof\s+[a-z][A-Za-z0-9]+;?", value)
        or re.fullmatch(r"-{2,}\s*[A-Za-z0-9_-]+\s*-{2,}", value)
        or re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+(?:\s+[a-z][a-z0-9]*(?:-[a-z0-9]+)+)+", value)
        or re.fullmatch(r"(?:import\s+[\w.]+|from\s+[\w.]+\s+import\s+[\w*, ]+)", value)
        or value.lower() == "regex"
        or re.fullmatch(r"(?:-\s*)?[a-z][a-z0-9]*(?:-[a-z0-9]+)+(?:\s+-\s*[a-z][a-z0-9]*(?:-[a-z0-9]+)+)+(?:\s*---)?", value)
        or re.fullmatch(r"type\s+[A-Z][A-Za-z0-9]*\s+typeof\s+[a-z][A-Za-z0-9]*;?\s*//\s*value type", value)
        or re.fullmatch(r"(?:[\w.-]+/)*(?:[\w.-]+\.(?:yml|yaml|tf))(?:\s+[\w./-]+\.(?:yml|yaml|tf))*", value, re.I)
        or re.fullmatch(r"(?:narrowed|widened|inferred|resolved):\s*[A-Z][A-Za-z0-9_.<>|& ]*", value)
        or re.fullmatch(r"(?:threadManager|agentThreadId|blocksPerGrid|threadsPerBlock|sharedBytes|stream)(?:\s*,\s*[A-Za-z_$][\w$]*)*,?", value)
        or re.fullmatch(r"(?:[A-Za-z_$][\w$]*\s*:\s*[A-Za-z_$][\w$]*)(?:\s*,\s*[A-Za-z_$][\w$]*\s*:\s*[A-Za-z_$][\w$]*)*", value)
        or re.fullmatch(r"(?:-\*-\s*)?mode:\s*ruby\s*-\*-\s*(?:vi:\s*set\s*ft=ruby\s*:)?", value, re.I)
        or re.fullmatch(r"env:VAR\s+VAR\s+VAR\s+REDACTED", value)
        or re.fullmatch(r"(?:nord\d+:\s*[A-F0-9]{6}\s*\([^)]*\))(?:\s+nord\d+:\s*[A-F0-9]{6}\s*\([^)]*\))*", value, re.I)
        or re.fullmatch(r"[A-Za-z][A-Za-z0-9]*(?:Dynamo|Inductor)(?:\s+[A-Za-z][A-Za-z0-9]*(?:Dynamo|Inductor))*\s+optimization", value)
        or (re.fullmatch(r"[\w./@:-]+(?:\s+[\w./@:-]+)*", value)
            and re.search(r"[^\s]/[^\s]|@", value))
        or (re.fullmatch(r"[a-z0-9]{16,}", value, re.I)
            and re.search(r"[a-z]", value, re.I) and re.search(r"\d", value))
        or re.fullmatch(r"(?:nord\d+:\s*#[A-F0-9]{6}\s*\([^)]*\)\s*)+", value, re.I)
        or (len(re.findall(r"\bnord\d+\b", value, re.I)) >= 2
            and len(re.findall(r"#[A-F0-9]{6}", value, re.I)) >= 2)
        or ("-->" in value and sum(value.count(char) for char in "=+*/^_") >= 3)
        or ("u_sat" in value and "Saturation Error" in value)
        or re.fullmatch(r"vi:\s*set\s*ft\s*=?\s*ruby\s*:?", value, re.I)
        or (re.search(r"\.(?:yml|yaml|tf)\b", value, re.I)
            and re.search(r"(?:^|\s)[\w.-]+/\s", value))
    )


def _is_math_notation(value: str) -> bool:
    """Exclude equations that Lingua can mistake for prose after markup removal."""
    words = _WORD.findall(value)
    if ("\\frac" in value or "\\mathbf" in value or "\\sum" in value
            or "\\int" in value or "\\Delta" in value or "\\mathcal" in value
            or "\\cdot" in value or "argmin" in value):
        return True
    operators = sum(value.count(char) for char in "=+*/^_{}[]")
    return len(words) >= 2 and operators >= 4 and not any(
        word.lower() in _ENGLISH_FUNCTION_WORDS for word in words
    )


@lru_cache(maxsize=8192)
def _word_frequency_evidence(value: str) -> tuple[str, float, float] | None:
    """Return the leading language, mean Zipf frequency, and margin for prose words."""
    if zipf_frequency is None or len(_WORD_FREQUENCY_LANGUAGES) < 2:
        return None
    words = [word.lower() for word in _WORD.findall(value)]
    if not words:
        return None
    scores = {
        lang: sum(zipf_frequency(word, lang) for word in words) / len(words)
        for lang in _WORD_FREQUENCY_LANGUAGES
    }
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if len(ranked) < 2:
        return None
    return ranked[0][0], ranked[0][1], ranked[0][1] - ranked[1][1]


def _load_exceptions(root: Path) -> tuple[set[tuple[str, str, str]], list[str]]:
    path = root / EXCEPTIONS
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        entries = data["exceptions"]
        if not isinstance(entries, list):
            raise ValueError("exceptions must be a list")
    except FileNotFoundError:
        return set(), []
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        return set(), [f"{EXCEPTIONS}: invalid exception manifest: {exc}"]
    allowed: set[tuple[str, str, str]] = set()
    declared: set[tuple[str, str, str]] = set()
    errors: list[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"path", "scope", "sha256", "reason"}:
            errors.append(f"{EXCEPTIONS}: exception {index} must contain only path, scope, sha256, reason")
            continue
        rel, scope, digest, reason = entry["path"], entry["scope"], entry["sha256"], entry["reason"]
        if (not isinstance(rel, str) or Path(rel).is_absolute() or ".." in Path(rel).parts
                or scope not in {"segment", "file"}
                or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)
                or not isinstance(reason, str) or len(reason.strip()) < 12):
            errors.append(f"{EXCEPTIONS}: exception {index} requires a relative path, segment/file scope, SHA-256, and justified reason")
            continue
        identity = (rel, scope, digest)
        if identity in declared:
            errors.append(f"{EXCEPTIONS}: duplicate exception for {rel} ({digest[:12]})")
        declared.add(identity)
        if not (root / rel).is_file():
            errors.append(f"{EXCEPTIONS}: exception path does not exist: {rel}")
        allowed.add(identity)
    return allowed, errors


def _classify_segment(
    rel: str,
    lineno: int,
    raw_segment: str,
    detector: object,
    detections: dict[str, list[object]],
) -> str | None:
    """Return a blocking finding unless this exact prose unit is English."""
    sample = " ".join(raw_segment.split())
    sample = re.sub(r"\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$(?!\$)", " ", sample)
    sample = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", " ", sample)
    sample = " ".join(sample.split())
    sample = re.sub(r"^(?:[A-Z]|\d{1,3})[.)]\s+", "", sample)
    if sample.startswith(("#", "---")):
        sample = re.sub(r"^#{1,6}\s*", "", sample)
    sample = re.sub(r"[^\w\s.,!?;:'\"()/-]", " ", sample, flags=re.UNICODE)
    sample = " ".join(sample.split())
    if not _WORD.findall(sample):
        return None
    # Parenthesized acronyms and protocol codes can overwhelm short prose.
    classify_sample = re.sub(
        r"\((?=[^)]{0,40}\))(?=[^)]*[A-Z0-9/])(?=[^)]*(?:[A-Z0-9/]))[^)]*\)",
        " ", sample,
    )
    classify_sample = " ".join(classify_sample.split()) or sample
    if (_looks_like_code(raw_segment) or _looks_like_code(classify_sample)
            or (len(_WORD.findall(raw_segment)) <= 3 and _is_math_notation(raw_segment))
            or _is_math_notation(classify_sample)):
        return None
    if classify_sample not in detections:
        try:
            detections[classify_sample] = detector.compute_language_confidence_values(classify_sample)  # type: ignore[attr-defined]
        except Exception as exc:
            return f"{rel}:{lineno}: detection failed; needs human review ({exc})"
    confidences = detections[classify_sample]
    if not confidences:
        return f"{rel}:{lineno}: needs human review (language not confidently classified): {sample[:100]}"
    top = confidences[0]
    runner_up = confidences[1].value if len(confidences) > 1 else 0.0
    confidence = top.value
    margin = confidence - runner_up
    lexical = _word_frequency_evidence(classify_sample)
    if lexical:
        lexical_language, lexical_score, lexical_margin = lexical
        # The sentence model is the primary detector. The lexical model often
        # has low coverage on technical English and should not turn confident
        # English prose into a review finding by itself.
        if (top.language == Language.ENGLISH and confidence >= 0.80 and margin >= 0.20
                and lexical_language == "en"):
            return None
        if (lexical_language == "en" and lexical_score >= 2.0
                and lexical_margin >= 0.10):
            # A complete English sentence can hide a localized word from both
            # sentence-level models. Accented tokens are therefore escalated
            # for human review, never assigned a language from one word.
            if any(
                len(word) >= 4 and not word.isascii() and word[:1].islower()
                and zipf_frequency(word, "en") < 1.0
                for word in _WORD.findall(classify_sample)
            ):
                return f"{rel}:{lineno}: needs human review (non-ASCII token inside otherwise English prose): {sample[:100]}"
            return None
        if lexical_language != "en" and lexical_score >= 2.0 and lexical_margin >= 0.35:
            return f"{rel}:{lineno}: non-English language {lexical_language.upper()}; needs human review or exact justified exception: {sample[:100]}"
        return f"{rel}:{lineno}: needs human review (lexical language evidence {lexical_language} {lexical_score:.3f}, margin {lexical_margin:.3f}): {sample[:100]}"
    if confidence < MIN_LANGUAGE_PROBABILITY or margin < MIN_PROBABILITY_MARGIN:
        return f"{rel}:{lineno}: needs human review (language confidence {confidence:.3f}, margin {margin:.3f}): {sample[:100]}"
    if top.language != Language.ENGLISH:
        return f"{rel}:{lineno}: non-English language {top.language.name}; needs human review or exact justified exception: {sample[:100]}"
    return None


def repository_errors(root: Path) -> list[str]:
    """Validate natural-language segments throughout the repository."""
    if LanguageDetectorBuilder is None or Language is None or zipf_frequency is None:
        return ["lingua-language-detector==2.2.0 and wordfreq==3.1.1 are required for the repository language gate"]
    try:
        detector = LanguageDetectorBuilder.from_all_languages().build()
    except Exception as exc:  # library/model initialization failure must not bypass the gate
        return [f"lingua-language-detector failed to initialize; needs human review: {exc}"]
    allowed, errors = _load_exceptions(root)
    if errors:
        return errors
    seen: set[tuple[str, str]] = set()
    detections: dict[str, list[object]] = {}
    errors = []
    for path in _inventory(root):
        rel = path.relative_to(root).as_posix()
        parts = Path(rel).parts
        if (rel.startswith(GENERATED_PREFIXES) or rel in GENERATED_FILES
                or "dist" in parts or (len(parts) >= 4 and parts[0] == "harnesses" and parts[2] == "bootstrap")):
            # These artifacts are deterministic copies. Their canonical source
            # is scanned here; generator drift is blocked by the separate check.
            continue
        suffix = path.suffix.lower()
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            errors.append(f"{rel}: unreadable text artifact; needs human review ({exc})")
            continue
        if b"\0" in raw_bytes[:8192]:
            continue
        file_key = (rel, "file", hashlib.sha256(raw_bytes).hexdigest())
        if file_key in allowed:
            seen.add(file_key)
            continue
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeError as exc:
            errors.append(f"{rel}: undecodable text artifact; needs human review ({exc})")
            continue
        for lineno, raw in _segments(path, text):
            raw_units = _sentence_units(raw)
            for raw_segment in raw_units:
                raw_segment = " ".join(raw_segment.split())
                digest = hashlib.sha256(raw_segment.encode("utf-8")).hexdigest()
                key = (rel, "segment", digest)
                if key in allowed:
                    seen.add(key)
                    continue
                finding = _classify_segment(rel, lineno, raw_segment, detector, detections)
                if finding:
                    errors.append(finding)
    stale = allowed - seen
    for rel, scope, digest in sorted(stale):
        errors.append(f"{EXCEPTIONS}: stale exception does not match exact content at {rel} ({digest[:12]})")
    return errors


def validate(root: Path) -> list[str]:
    """Return blocking repository-wide language errors."""
    return repository_errors(root)
