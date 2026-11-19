"""The surfaces the improvement loop may not propose to change (rung 0).

The loop proposes and a person disposes, so this is a second lock, not the only one:
a candidate that routes to one of these files, or whose statement names one, is
rejected before it is staged. The list is the single source; the standard
``docs/standards/self-improvement-loop.md`` quotes it and a test keeps the two equal.

Matching is on text, not on the file system: a statement is untrusted prose, so it is
folded first (NFKC, no format characters, case-insensitive, one path separator) and a
path that only reaches a protected file through ``..`` is normalised before the test.
A name written with spaces or through an encoding the fold does not undo can still slip
past a text match, which is why the human gate and the repository checks stay in place.
"""

from __future__ import annotations

import posixpath
import re
import unicodedata

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


def _fold(text: str) -> str:
    """Normalise prose or a path so equal files compare equal."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    return text.replace("\\", "/").casefold()


def _regex(pattern: str) -> re.Pattern[str]:
    body = re.escape(_fold(pattern)).replace(r"\*", r"[^/\s]*")
    tail = "" if pattern.endswith("/") else r"(?![\w.-])"
    return re.compile(r"(?<![\w.-])" + body + tail)


_PATTERNS = tuple((pattern, _regex(pattern)) for pattern in PROTECTED)


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
    folded = _fold(text)
    # ``a/../b`` is a path that reaches ``b``: resolve each path-like token first.
    folded += " " + " ".join(posixpath.normpath(tok) for tok in folded.split() if ".." in tok)
    for pattern, rx in _PATTERNS:
        if rx.search(folded):
            return pattern
    return None
