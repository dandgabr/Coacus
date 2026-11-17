"""Reference helper for the untrusted-data frame (ADR 0009).

Wraps untrusted text between two markers that share a fresh random identifier and
defangs any copy of the marker stem found inside the text. This is defense in depth
only: it never changes the trust class of the text it surrounds. What stops a
forged end marker is the unguessable identifier, not the defanging; defanging only
removes the obvious copies and is known not to catch every look-alike character
(for example letters borrowed from another script).

Adapted from patterns recorded in ADR 0009 (see THIRD-PARTY-NOTICES.md, revision
6337341602be6aa5860b1e83138f03bdd0b78f71, reviewed 2026-11-17).

The module is a pure library. No hook, validator or bootstrap imports it, and nothing
here reads or writes files, the environment or the network. The source file is
ASCII only on purpose: invisible characters are written as numeric codes.
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
MIN_TOKEN = 4

# Invisible or default-ignorable code points, as numbers, so no invisible
# character appears in this source file.
_HIDDEN_CODES = frozenset({
    0x00AD, 0x034F, 0x061C, 0x115F, 0x1160, 0x17B4, 0x17B5, 0x180E,
    0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
    0x2060, 0x2061, 0x2062, 0x2063, 0x2064,
    0x2066, 0x2067, 0x2068, 0x2069,
    0x3164, 0xFEFF, 0xFFA0,
})
_HIDDEN_RANGES = (
    (0x180B, 0x180F), (0xFE00, 0xFE0F), (0xE0000, 0xE007F), (0xE0100, 0xE01EF),
)
_MINUS_SIGN = 0x2212


def _is_hidden(char: str) -> bool:
    """Return True for invisible, format, variation-selector and tag characters."""
    code = ord(char)
    if code in _HIDDEN_CODES or unicodedata.category(char) == "Cf":
        return True
    return any(low <= code <= high for low, high in _HIDDEN_RANGES)


def _strip_hidden(text: str) -> str:
    """Remove every hidden character from text."""
    return "".join(ch for ch in text if not _is_hidden(ch))


def _fold(char: str) -> str:
    """Return the one-character matching key of a character.

    Every dash punctuation character and the minus sign fold to a hyphen, and a
    letter folds to its lowercase form when that stays one character.
    """
    if unicodedata.category(char) == "Pd" or ord(char) == _MINUS_SIGN:
        return "-"
    lowered = char.lower()
    return lowered if len(lowered) == 1 else char


def _default_token() -> str:
    """Return a fresh 128-bit random identifier as lowercase hexadecimal."""
    return secrets.token_hex(16)


def _valid_word(word: str, limit: int) -> bool:
    """Return True for a non-empty ASCII word of letters, digits, dot, dash or underscore."""
    if not word or len(word) > limit:
        return False
    return all(ch.isascii() and (ch.isalnum() or ch in "._-") for ch in word)


def _valid_token(token: str) -> bool:
    """Return True for an identifier that is long enough, alphanumeric and stem-free."""
    return (
        _valid_word(token, MAX_TOKEN)
        and len(token) >= MIN_TOKEN
        and any(ch.isalnum() for ch in token)
        and STEM not in token.lower()
    )


def _normalize(text: str) -> str:
    """Strip hidden characters, then apply NFKC normalization (may lengthen the text)."""
    return unicodedata.normalize("NFKC", _strip_hidden(text))


def sanitize(text: str) -> str:
    """Strip hidden characters and apply NFKC normalization.

    Hidden characters are removed before and after normalization. This changes the
    text: keep the original when exact characters matter.
    """
    return _strip_hidden(_normalize(text))


def neutralize(text: str) -> str:
    """Return sanitized text in which every look-alike of the marker stem is defanged."""
    return _defang(sanitize(text))


def _defang(clean: str) -> str:
    """Replace every look-alike of the marker stem in already sanitized text.

    Matching uses a per-character key (case folded, Unicode dash punctuation and the
    minus sign folded to a hyphen) while the original characters are kept everywhere
    else. Plain string scanning only; no regular expression runs over the untrusted
    text. The replacement starts and ends with brackets, so neighbouring characters
    can never recombine into the stem.
    """
    key = "".join(_fold(ch) for ch in clean)
    width = len(STEM)
    parts: list[str] = []
    index = 0
    while index < len(clean):
        if key[index:index + width] == STEM:
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
        text: the untrusted text. Larger than MAX_CHARS, or larger than twice that
            after normalization, raises ValueError.
        source: a short label of letters, digits, dot, dash or underscore that does
            not contain the marker stem.
        token_source: injectable identifier source, for tests; defaults to a fresh
            random value on every call.

    The framed body is sanitized, so it can differ from the input. The identifier is
    never stored or logged here; a caller must not store, log or echo it either.
    Framing reduces risk; it is not a trust boundary.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > MAX_CHARS:
        raise ValueError("text exceeds MAX_CHARS")
    if not _valid_word(source, MAX_LABEL) or STEM in source.lower():
        raise ValueError("source label is not a short ascii word")
    token = (token_source or _default_token)()
    if not _valid_token(token):
        raise ValueError("identifier is not a usable ascii word")
    normalized = _normalize(text)
    if len(normalized) > 2 * MAX_CHARS:
        raise ValueError("text exceeds the size limit after normalization")
    body = _defang(_strip_hidden(normalized))
    if token.lower() in body.lower():
        raise ValueError("identifier collides with the framed text")
    return (
        f"<<<{STEM} id={token} source={source}>>>\n"
        f"{body}\n"
        f"<<<end-{STEM} id={token}>>>"
    )
