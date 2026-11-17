"""Reference helper for the untrusted-data frame (ADR 0009).

Wraps untrusted text between two markers that share a fresh random identifier and
defangs any copy of the marker stem found inside the text. This is defense in depth
only: it never changes the trust class of the text it surrounds.

The module is a pure library. No hook, validator or bootstrap imports it, and nothing
here reads or writes files, the environment or the network.
"""

from __future__ import annotations

import secrets
import unicodedata
from typing import Callable, Optional

STEM = "untrusted-data"
DEFANGED = "[marker-removed]"
MAX_CHARS = 200_000
MAX_LABEL = 64
MAX_TOKEN = 64

_HIDDEN = frozenset(
    ord(ch)
    for ch in "​‌‍⁠﻿"
    "‪‫‬‭‮⁦⁧⁨⁩"
)
_TAG_FIRST = 0xE0000
_TAG_LAST = 0xE007F


def _is_hidden(char: str) -> bool:
    """Return True for zero-width, bidirectional-control and Unicode tag characters."""
    code = ord(char)
    return code in _HIDDEN or _TAG_FIRST <= code <= _TAG_LAST


def _strip_hidden(text: str) -> str:
    """Remove every hidden character from text."""
    return "".join(ch for ch in text if not _is_hidden(ch))


def _default_token() -> str:
    """Return a fresh 128-bit random identifier as lowercase hexadecimal."""
    return secrets.token_hex(16)


def _valid_word(word: str, limit: int) -> bool:
    """Return True for a non-empty ASCII word of letters, digits, dot, dash or underscore."""
    if not word or len(word) > limit:
        return False
    return all(ch.isascii() and (ch.isalnum() or ch in "._-") for ch in word)


def sanitize(text: str) -> str:
    """Strip hidden characters and apply NFKC normalization.

    Hidden characters are removed before and after normalization so that a marker
    split by a zero-width character, a Unicode tag or a bidirectional control cannot
    survive. Normalization folds full-width and compatibility forms back to ASCII.
    """
    return _strip_hidden(unicodedata.normalize("NFKC", _strip_hidden(text)))


def neutralize(text: str) -> str:
    """Return sanitized text in which every case variant of the marker stem is defanged.

    Plain string scanning only; no regular expression runs over the untrusted text.
    The replacement starts and ends with brackets, so neighbouring characters can
    never recombine into the stem.
    """
    clean = sanitize(text)
    width = len(STEM)
    parts: list[str] = []
    index = 0
    while index < len(clean):
        if clean[index:index + width].lower() == STEM:
            parts.append(DEFANGED)
            index += width
        else:
            parts.append(clean[index])
            index += 1
    return "".join(parts)


def frame(
    text: str,
    source: str,
    *,
    token_source: Optional[Callable[[], str]] = None,
) -> str:
    """Return text wrapped in a start and an end marker that share one fresh identifier.

    Args:
        text: the untrusted text. Larger than MAX_CHARS raises ValueError.
        source: a short label of letters, digits, dot, dash or underscore.
        token_source: injectable identifier source, for tests; defaults to a fresh
            random value on every call.

    The identifier is never stored or logged here. A caller must not store, log or
    echo it either. Framing reduces risk; it is not a trust boundary.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > MAX_CHARS:
        raise ValueError("text exceeds MAX_CHARS")
    if not _valid_word(source, MAX_LABEL):
        raise ValueError("source label is not a short ascii word")
    token = (token_source or _default_token)()
    if not _valid_word(token, MAX_TOKEN):
        raise ValueError("identifier is not a short ascii word")
    body = neutralize(text)
    if token in body:
        raise ValueError("identifier collides with the framed text")
    return (
        f"<<<{STEM} id={token} source={source}>>>\n"
        f"{body}\n"
        f"<<<end-{STEM} id={token}>>>"
    )
