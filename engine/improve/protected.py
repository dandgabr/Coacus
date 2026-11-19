"""The surfaces the improvement loop may not propose to change (rung 0).

The loop proposes and a person disposes, so this is a second lock, not the only one:
a candidate that routes to one of these files, or whose statement names one, is
rejected before it is staged. The list is the single source; the standard
``docs/standards/self-improvement-loop.md`` quotes it and a test keeps the two equal.

Matching is on text, not on the file system: a statement is untrusted prose, so it is
folded first (NFKC, no format characters, case-insensitive, one path separator) and a
path that only reaches a protected file through ``..`` is normalised before the test.
What the fold does not undo stays a residual (confusable letters from another script, a
glob or brace form, a bare file name, a paraphrase), which is why the human gate and the
repository checks stay in place. A bare ``AGENTS.md`` also matches inside another path,
on purpose: the cost is a dropped proposal, which the loop now reports.
"""

from __future__ import annotations

import html
import posixpath
import re
import unicodedata
from urllib.parse import unquote

# A trailing slash means "everything below"; ``*`` stays inside one path segment.
PROTECTED: tuple[str, ...] = (
    "docs/standards/self-improvement-loop.md",
    "docs/standards/evidence.md",
    "docs/standards/untrusted-content.md",
    "docs/standards/lifecycle-guardrails.md",
    "engine/improve/",
    "engine/guardrail/",
    "engine/verify/",
    "scripts/coacus_eval.py",
    "evals/scenarios/",
    "harnesses/*/bootstrap/guardrail-hooks.json",
    "AGENTS.md",
)

# The same code reached by its Python name, derived so the list stays the only source.
MODULES: tuple[tuple[str, str], ...] = tuple(
    (pattern.removesuffix(".py").rstrip("/").replace("/", "."), pattern)
    for pattern in PROTECTED
    if pattern.startswith(("engine/", "scripts/"))
)

MAX_STATEMENT_CHARS = 64_000

_SLASHES = str.maketrans({"\\": "/", "\u2215": "/", "\u2044": "/", "\u29f8": "/", "\u2571": "/"})
_IGNORABLE = set("\u115f\u1160\u3164\uffa0\u180b\u180c\u180d\u180e\u180f\u034f")


def _fold(text: str) -> str:
    """Normalise prose or a path so equal files compare equal."""
    text = unicodedata.normalize("NFKD", unicodedata.normalize("NFKC", text))
    text = "".join(ch for ch in text if ch not in _IGNORABLE and unicodedata.category(ch) not in ("Cf", "Mn", "Me"))
    return unicodedata.normalize("NFKC", text).translate(_SLASHES).casefold()


def _views(text: str) -> list[str]:
    """The text as written and as a decoder would read it (HTML entities, percent escapes)."""
    views = [text]
    decoded = unquote(html.unescape(text))
    if decoded != text:
        views.append(decoded)
    return views


def _prose(text: str) -> str:
    """Fold prose and take out the markup and spacing that split a path in a document."""
    folded = _fold(text).replace("`", "")
    folded = re.sub(r"\*{2,}", "", folded)
    return re.sub(r"\s*/\s*", "/", folded)


def _regex(pattern: str) -> re.Pattern[str]:
    body = re.escape(_fold(pattern)).replace(r"\*", r"[^/\s]*")
    # A directory may be written without its closing slash; a file must stand alone.
    tail = r"(?=/|[^\w.-]|$)" if pattern.endswith("/") else r"(?![\w.-])"
    if pattern.endswith("/"):
        body = body[:-2] if body.endswith("\\/") else body.rstrip("/")
    return re.compile(r"(?<![\w.-])" + body + tail)


_PATTERNS = tuple((pattern, _regex(pattern)) for pattern in PROTECTED)
_MODULE_PATTERNS = tuple(
    (target, re.compile(r"(?<![\w.-])" + re.escape(name) + r"(?![\w-])")) for name, target in MODULES
)


def is_protected(path: str) -> str | None:
    """Return the protected pattern a repository-relative ``path`` falls under, or None."""
    if not isinstance(path, str) or not path.strip():
        return None
    clean = posixpath.normpath(_fold(path).strip().lstrip("/"))
    for pattern, rx in _PATTERNS:
        if rx.fullmatch(clean) or (pattern.endswith("/") and clean.startswith(_fold(pattern))):
            return pattern
    return None


def mentions(text: str) -> str | None:
    """Return the first protected pattern a statement names, or None."""
    if not isinstance(text, str):
        return None
    for view in _views(text):
        folded = _prose(view)
        # ``a/../b`` and ``a/./b`` are paths that reach ``b``: resolve each path-like token.
        folded += " " + " ".join(
            posixpath.normpath(tok) for tok in folded.split()
            if "/" in tok and (".." in tok or "/./" in tok or "//" in tok)
        )
        for pattern, rx in _PATTERNS:
            if rx.search(folded):
                return pattern
        for target, rx in _MODULE_PATTERNS:
            if rx.search(folded):
                return target
    return None
