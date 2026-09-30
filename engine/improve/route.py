"""Route a candidate to improve / create / merge / skip (F10 step 3).

There is no canonical algorithm for improve-vs-create, so this is an explicit,
deterministic, auditable procedure modeled on ``engine/router``: lexical
features, fixed thresholds, a documented tie-break. Retrieval-first, default
IMPROVE (creation is the expensive, overfitting-prone branch).
"""

from __future__ import annotations

import json
from pathlib import Path

CATALOG = "catalog/catalog.json"


def _fold(text: str) -> set[str]:
    """Normalized token set (lowercase, alphanumeric)."""
    return {t for t in "".join(c if c.isalnum() else " " for c in text.lower()).split() if len(t) > 2}


def _load_catalog(root: Path) -> list[dict]:
    path = root / CATALOG
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    targets: list[dict] = []
    for skill in data.get("skills", []):
        targets.append({"name": skill.get("name"), "path": skill.get("path"), "text": str(skill.get("name", ""))})
    for agent in data.get("agents", []):
        targets.append({"name": agent.get("name"), "path": agent.get("source"), "text": agent.get("description", "")})
    return targets


def _overlap(a: set[str], b: set[str]) -> float:
    if not a:
        return 0.0
    return len(a & b) / len(a)


T_LEX = 0.34
T_COVER = 0.6


def route(root: Path, candidate: dict) -> dict:
    """Return a routing decision with the features that produced it."""
    statement = _fold(candidate.get("statement", ""))
    best_name, best_score, best_cover = None, 0.0, 0.0
    for target in _load_catalog(root):
        score = _overlap(statement, _fold(str(target.get("text", ""))))
        cover = score
        if score > best_score:
            best_name, best_score, best_cover = target.get("name"), score, cover

    if best_score >= T_LEX and best_cover >= T_COVER:
        decision, reason = "skip", "already covered by the closest target"
    elif best_score >= T_LEX:
        decision, reason = "improve", "closest target exists but does not cover it"
    elif candidate.get("support", 0) >= 2 and candidate.get("trusted"):
        decision, reason = "create", "no close target and the evidence generalizes"
    else:
        decision, reason = "skip", "no close target and the evidence is single-session or tainted"
    return {
        "decision": decision,
        "target": best_name,
        "features": {"lex": round(best_score, 3), "cover": round(best_cover, 3), "support": candidate.get("support", 0)},
        "thresholds": {"T_lex": T_LEX, "T_cover": T_COVER},
        "reason": reason,
    }
