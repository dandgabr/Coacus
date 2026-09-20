"""Version-freshness check (version-freshness).

Canonical artifacts pin versions of standards, frameworks, libraries and
regulations in their instruction bodies. A training-memory pin is a claim about
an unknown instant, so every such pin must sit near evidence that it was
resolved: a source anchor (a URL, an RFC identifier, a publisher or vendor name)
or an explicit resolution marker (``resolved YYYY-MM-DD``).

This validator reports WARNINGS, not errors. It keeps a machine surface on the
pin list so the corpus can be reconciled; the standard promotes it to a hard gate
once the list is clean.

Prose only. The scan excludes the YAML frontmatter, fenced code blocks and inline
code spans: those are samples and identifiers, not behavioural claims, and flagging
them buries the real pins.

Only MOVING targets are flagged: a release line that a publisher supersedes — a
``vX.Y[.Z]`` framework version, an ``OWASP ... YYYY`` release, a ``MASVS``/``CSF``/
``CIS Controls``/``SLSA``/``SBOM``/``PCI DSS`` release, or a ``NIST SP`` WITH a
revision suffix (``800-61r3``, ``Rev. 5``). A bare document identifier — ``RFC 9110``,
``ISO/IEC 9899``, ``FIPS 203``, ``NIST SP 800-53`` without a revision — names a
fixed document, not a current-version claim, and is not flagged.
"""

from __future__ import annotations

import re
from pathlib import Path

SCAN_GLOBS = (
    "knowledge/agents/**/agent.source.md",
    "knowledge/skills/**/SKILL.md",
    "methodology/workflows/**/SKILL.md",
)

# A MOVING pin: a release line the publisher supersedes over time. A bare fixed
# document identifier (RFC 9110, ISO/IEC 9899, FIPS 203, NIST SP 800-53) is not
# a current-version claim and is deliberately absent.
PIN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("nist", re.compile(r"\bNIST\s+SP\s+\d{3}-\d+[A-Za-z]*(?:r\d+|[\s,]*Rev\.?\s*\d+)")),
    ("owasp", re.compile(r"\bOWASP\s+[A-Za-z0-9][A-Za-z0-9 /-]*?\s+\d{4}\b")),
    ("masvs", re.compile(r"\bMASVS\s+v?\d+(?:\.\d+)+")),
    ("semver", re.compile(r"\bv\d+\.\d+(?:\.\d+)?\b")),
    ("csf", re.compile(r"\bCSF\s+\d+\.\d+")),
    ("controls", re.compile(r"\bCIS\s+Controls\s+v?\d+(?:\.\d+)?")),
    ("slsa", re.compile(r"\bSLSA\s+v?\d+(?:\.\d+)?")),
    ("sbom", re.compile(r"\b(?:CycloneDX|SPDX)\s+v?\d+(?:\.\d+)?")),
    ("pci", re.compile(r"\bPCI\s+DSS\s+v?\d+(?:\.\d+)?")),
)

# Evidence that the pin was resolved in this corpus: a source anchor or an
# explicit resolution date. A window catches the common case (identifier,
# edition and URL on adjacent lines).
ANCHOR = re.compile(
    r"(https?://|resolved\s+\d{4}-\d{2}-\d{2}|rfc-editor|nist\.gov|iso\.org"
    r"|owasp\.org|context7|pcisecuritystandards\.org|github\.com)",
    re.IGNORECASE,
)
CONTEXT_LINES = 3

# A per-artifact resolution declaration anchors every pin in that artifact. The
# accepted form is the standard's "resolved YYYY-MM-DD": a skill that documents
# its sources once (a "Version Sources" section) does not repeat the date on each
# citation line.
FILE_RESOLUTION = re.compile(r"resolved\s+\d{4}-\d{2}-\d{2}")

# The standard's other honest terminal state: a pin that could NOT be resolved is
# marked `unverified` with a reason (version-freshness rule 5). Rejecting this
# would force the author to write a false "resolved" date, so the gate accepts it
# too — but the report surfaces it, and it requires a reason, not a bare marker.
FILE_UNVERIFIED = re.compile(r"\(unverified\)\s*[—:-]\s*\S")

# The standards themselves name editions as their subject rather than as a
# behavioural claim; the validator does not scan docs/.
_SKIP_PARTS = ("dist/", "references/", "examples/", "scripts/")


def discover_sources(root: Path) -> list[Path]:
    """Every canonical artifact subject to the freshness rule."""
    found: list[Path] = []
    for pattern in SCAN_GLOBS:
        for path in root.glob(pattern):
            rel = path.relative_to(root).as_posix()
            if any(part in rel for part in _SKIP_PARTS):
                continue
            found.append(path)
    return sorted(found)


def _clean(text: str) -> str:
    """Blank non-prose regions, keeping every newline so line numbers stay true.

    Removes the YAML frontmatter, fenced code blocks and inline code spans. A
    blanked line becomes empty rather than deleted, so a reported line number is
    the file line the pin sits on.
    """
    lines = text.splitlines()
    cleaned: list[str] = []
    in_fence = False
    in_front = False
    for index, line in enumerate(lines):
        bare = line.strip()
        if index == 0 and bare == "---":
            in_front = True
            cleaned.append("")
            continue
        if in_front:
            cleaned.append("")
            if bare == "---":
                in_front = False
            continue
        if bare.startswith("```"):
            in_fence = not in_fence
            cleaned.append("")
            continue
        if in_fence:
            cleaned.append("")
            continue
        cleaned.append(re.sub(r"`[^`]*`", " ", line))
    return "\n".join(cleaned)


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _window(lines: list[str], pin_line: int) -> str:
    lo = max(0, pin_line - 1 - CONTEXT_LINES)
    hi = min(len(lines), pin_line + CONTEXT_LINES)
    return "\n".join(lines[lo:hi])


def _anchored(lines: list[str], pin_line: int) -> bool:
    window = _window(lines, pin_line)
    return bool(ANCHOR.search(window)) or bool(FILE_UNVERIFIED.search(window))


def _is_unverified(lines: list[str], pin_line: int) -> bool:
    """A nearby explicit ``(unverified) — reason`` marker for this pin."""
    return bool(FILE_UNVERIFIED.search(_window(lines, pin_line)))


def warnings(root: Path) -> list[str]:
    """Return a list of warning strings (empty = no unanchored pins)."""
    notes: list[str] = []
    for source in discover_sources(root):
        rel = source.relative_to(root).as_posix()
        try:
            text = _clean(source.read_text(encoding="utf-8"))
        except OSError:
            continue
        # An artifact-level resolution declaration ("resolved YYYY-MM-DD")
        # anchors every pin in it. Without one, each pin needs its own anchor or
        # a nearby "(unverified) — reason" marker.
        declared = bool(FILE_RESOLUTION.search(text))
        if declared:
            continue
        lines = text.splitlines()
        for kind, pattern in PIN_PATTERNS:
            for match in pattern.finditer(text):
                line = _line_of(text, match.start())
                if _anchored(lines, line):
                    continue
                notes.append(
                    f"{rel}:{line}: unanchored version pin "
                    f"({kind}: {match.group(0).strip()!r}) — resolve it and record the "
                    "source/date, or mark it '(unverified) — reason' (version-freshness)"
                )
    return notes


def validate(root: Path) -> list[str]:
    """Alias of :func:`warnings` for callers that expect ``validate``."""
    return warnings(root)


def report(root: Path, include_references: bool = False) -> list[str]:
    """Read-only pin inventory (offline; no network).

    Lists every moving release pin with its artifact and line and one of three
    statuses: ``resolved`` (has a resolution declaration), ``unverified`` (the
    standard's explicit "could not resolve" state, with a reason) or
    ``UNRESOLVED`` (a gate error). Never fails: it is the audit surface for "how
    old is the corpus", not a gate.
    """
    roots = list(SCAN_GLOBS)
    if include_references:
        roots += (
            "knowledge/skills/**/references/**/*.md",
            "knowledge/agents/**/references/**/*.md",
        )
    rows: list[str] = []
    for pattern in roots:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if not include_references and any(p in rel for p in _SKIP_PARTS):
                continue
            try:
                text = _clean(path.read_text(encoding="utf-8"))
            except OSError:
                continue
            declared = bool(FILE_RESOLUTION.search(text))
            lines = text.splitlines()
            for kind, pattern_ in PIN_PATTERNS:
                for match in pattern_.finditer(text):
                    line = _line_of(text, match.start())
                    if _is_unverified(lines, line):
                        status = "unverified"
                    elif declared or _anchored(lines, line):
                        status = "resolved"
                    else:
                        status = "UNRESOLVED"
                    rows.append(
                        f"{status:10s} {rel}:{line}: [{kind}] {match.group(0).strip()!r}"
                    )
    return rows
