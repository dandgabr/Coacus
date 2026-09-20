"""Deterministic agent router (routing).

Given a user prompt, rank the agents in the routing index and return the best
candidates. This is the lexical, offline scorer:

- **Mode A (automated curation)**: ``rank(prompt)`` scores each agent against the
  prompt and returns the top-N above a minimum threshold.
- **Mode M (manual selection)**: ``resolve(names)`` validates a user's explicit
  list of agent names, returning the matched entries and an error per unknown
  name with close suggestions.

Scoring is a weighted token/phrase overlap without external dependencies:

- a curated trigger phrase (``knowledge/routing/lexicon.json``) weighs most, so
  the bilingual vocabulary is authoritative;
- a term in the agent's name weighs next;
- a term in the description or a skill slug weighs least.

The router never runs the agents and never spawns anything; it only proposes.
Concurrency is the governor's job (orchestration-governance), and ``rank`` accepts
a ``limit`` so a caller can cap the proposal at the free slots.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path

from engine.generators.routing import ROUTING_PATH

# Common PT-BR and EN stopwords: never discriminative for agent choice.
STOPWORDS = frozenset(
    """
    a o e de da do das dos em no na nos nas um uma uns umas para por com sem
    que qual quais como onde quando sobre entre até ate ao aos à às se sim não
    nao the a an and or of to in on for with without that which how where when
    about between until if yes no my your our their this these those it its is
    are be been being was were will would can could should may might do does did
    me you we they he she them us i
    """.split()
)

_TOKEN = re.compile(r"[a-z0-9][a-z0-9+#./-]*")
MIN_TOKEN_LEN = 2

# Weights: curated triggers dominate, then the name, then description/skills.
W_TRIGGER = 5.0
W_NAME = 3.0
W_TEXT = 1.0
# A single match is rarely enough; the default floor keeps noise out.
DEFAULT_MIN_SCORE = 1.0


@dataclass
class Candidate:
    """One ranked agent proposal."""

    name: str
    category: str
    score: float
    matched: list[str]
    description: str


def _load_index(root: Path) -> list[dict]:
    path = root / ROUTING_PATH
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    entries = data.get("entries", []) if isinstance(data, dict) else []
    return [e for e in entries if isinstance(e, dict)]


def _strip_accents(text: str) -> str:
    """Fold diacritics to ASCII so ``latência`` and ``latencia`` match.

    PT-BR and EN prompts carry accents; the curated lexicon may or may not, and
    the user may type either. Folding both sides to a common form makes the match
    accent-insensitive instead of splitting ``latência`` into ``lat`` + ``ncia``.
    """
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )


def _tokens(text: str) -> list[str]:
    """Lowercase, accent-folded word tokens, minus stopwords and single chars."""
    folded = _strip_accents(text.lower())
    return [
        tok
        for tok in _TOKEN.findall(folded)
        if len(tok) >= MIN_TOKEN_LEN and tok not in STOPWORDS
    ]


def _fold_phrase(text: str) -> str:
    """Accent-folded, whitespace-collapsed lowercase text for phrase matching."""
    return re.sub(r"\s+", " ", _strip_accents(text.lower())).strip()


def _agent_terms(entry: dict) -> tuple[set[str], set[str], set[str], list[str]]:
    """Term sets for one agent: (trigger tokens, name, text, trigger phrases).

    A single-word trigger contributes a token; a multi-word trigger contributes a
    PHRASE that must appear in the prompt, so ``sistema digital`` no longer matches
    a prompt that merely contains ``sistema``.
    """
    trigger_tokens: set[str] = set()
    trigger_phrases: list[str] = []
    for term in entry.get("triggers", []) or []:
        raw = str(term).strip()
        if not raw:
            continue
        if " " in raw.strip():
            trigger_phrases.append(_fold_phrase(raw))
        else:
            trigger_tokens.update(_tokens(raw))
    name = set(_tokens(str(entry.get("name", "")).replace("-", " ")))
    text: set[str] = set(_tokens(str(entry.get("description", ""))))
    for skill in entry.get("skills", []) or []:
        text.update(_tokens(Path(str(skill)).parent.name.replace("-", " ")))
    return trigger_tokens, name, text, trigger_phrases


def rank(
    root: Path,
    prompt: str,
    limit: int | None = None,
    min_score: float = DEFAULT_MIN_SCORE,
) -> list[Candidate]:
    """Rank agents for ``prompt`` (Mode A); best first, above ``min_score``."""
    prompt_tokens = set(_tokens(prompt))
    prompt_folded = _fold_phrase(prompt)
    if not prompt_tokens:
        return []
    candidates: list[Candidate] = []
    for entry in _load_index(root):
        triggers, name, text, phrases = _agent_terms(entry)
        matched_triggers = prompt_tokens & triggers
        matched_phrases = [p for p in phrases if p and p in prompt_folded]
        matched_name = prompt_tokens & name
        matched_text = prompt_tokens & text
        score = (
            W_TRIGGER * (len(matched_triggers) + len(matched_phrases))
            + W_NAME * len(matched_name)
            + W_TEXT * len(matched_text)
        )
        if score < min_score:
            continue
        matched = sorted(matched_triggers | matched_name | matched_text) + matched_phrases
        candidates.append(
            Candidate(
                name=str(entry.get("name", "")),
                category=str(entry.get("category", "")),
                score=score,
                matched=matched,
                description=str(entry.get("description", "")),
            )
        )
    candidates.sort(key=lambda c: (-c.score, c.name))
    if limit is not None and limit >= 0:
        candidates = candidates[:limit]
    return candidates


def resolve(root: Path, names: list[str]) -> tuple[list[dict], list[str]]:
    """Validate an explicit list of agent names (Mode M).

    Returns ``(matched_entries, errors)``. A name that does not exist yields an
    error carrying close suggestions; matching is exact on the canonical name or
    a case-insensitive trigger alias.
    """
    index = _load_index(root)
    by_name = {str(e.get("name")): e for e in index}
    alias: dict[str, str] = {}
    for entry in index:
        for term in entry.get("triggers", []) or []:
            alias.setdefault(str(term).strip().lower(), str(entry.get("name")))

    matched: list[dict] = []
    errors: list[str] = []
    for raw in names:
        query = raw.strip()
        if not query:
            continue
        canonical = query if query in by_name else alias.get(query.lower())
        if canonical and canonical in by_name:
            matched.append(by_name[canonical])
            continue
        suggestions = get_close_matches(query, list(by_name), n=3, cutoff=0.6)
        hint = f" (did you mean: {', '.join(suggestions)}?)" if suggestions else ""
        errors.append(f"unknown agent {query!r}{hint}")
    return matched, errors


def list_agents(root: Path, category: str | None = None, grep: str | None = None) -> list[dict]:
    """Enumerate the agents for manual browsing (Mode M)."""
    index = _load_index(root)
    needle = (grep or "").lower()
    out: list[dict] = []
    for entry in index:
        if category and str(entry.get("category")) != category:
            continue
        if needle:
            haystack = f"{entry.get('name','')} {entry.get('description','')}".lower()
            if needle not in haystack:
                continue
        out.append(entry)
    return out


def rerank(
    candidates: list[Candidate],
    prompt: str,
    command: str,
) -> list[Candidate]:
    """Re-rank lexical candidates with an external command (Mode A, opt-in).

    The lexical scorer is the offline default; a semantic reranker (embeddings, a
    local model, an LLM) plugs in here without becoming a dependency. The command
    mirrors the eval judge: it reads JSON on stdin
    ``{"prompt": ..., "candidates": [{name, score, matched}, ...]}`` and prints an
    ordered list of agent names, one per line.

    Fails open: an absent or failing command returns the lexical ranking unchanged,
    so routing never breaks because the optional reranker is missing.
    """
    import json
    import shlex
    import subprocess

    payload = json.dumps(
        {
            "prompt": prompt,
            "candidates": [
                {"name": c.name, "score": c.score, "matched": c.matched}
                for c in candidates
            ],
        }
    )
    try:
        proc = subprocess.run(
            shlex.split(command),
            input=payload,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return candidates
    if proc.returncode != 0:
        return candidates
    order = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not order:
        return candidates
    by_name = {c.name: c for c in candidates}
    ranked = [by_name[name] for name in order if name in by_name]
    # Keep any candidate the reranker did not mention, after the ranked ones.
    ranked.extend(c for c in candidates if c.name not in order)
    return ranked

