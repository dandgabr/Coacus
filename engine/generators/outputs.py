"""Cross-generator output uniqueness (single-source, generated-artifacts).

Every generated repo-relative path has exactly ONE producer. Before this module,
each generator merged its own outputs with ``dict.update`` and the facade
concatenated the generators, so two generators writing the same path silently
clobbered each other (last-wins) and ``check`` compared against the wrong bytes.

``union`` turns that silent overwrite into a build error. It is called by
``scripts/coacus.py`` across ALL generators, because a module cannot see a
sibling module's paths (D3: disk is the truth; generation is the contract).
"""

from __future__ import annotations


class OutputCollision(ValueError):
    """Two producers emitted the same repo-relative path."""


def union(named_outputs: list[tuple[str, dict[str, str]]]) -> dict[str, str]:
    """Merge ``[(producer, {path: content})]`` rejecting any duplicate path.

    Raises ``OutputCollision`` naming both producers so the fix is obvious:
    the two generators must agree on one owner, or write disjoint paths.
    """
    seen: dict[str, str] = {}
    owner: dict[str, str] = {}
    for producer, mapping in named_outputs:
        for rel, content in mapping.items():
            if rel in seen:
                raise OutputCollision(
                    f"{rel}: rendered by {owner[rel]!r} and {producer!r}"
                )
            seen[rel] = content
            owner[rel] = producer
    return seen
