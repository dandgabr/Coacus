"""Harness-manifest validator (F9.1).

Before this validator, ``harness.json`` was only checked for a ``name`` key, so a
misspelled lifecycle capability or an event id absent from the canonical
taxonomy degraded the render silently. This validator makes those errors loud:
it validates the ``bootstrap`` block, the ``plugins[].kind`` values against the
engine's registered kinds, and the ``lifecycle`` block against the canonical
event taxonomy (``methodology/lifecycle/events.json``).

It also validates the authoring template (``harnesses/_template``), which
``discover_harnesses`` deliberately skips.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.generators import plugins as plugin_registry
from engine.guardrail import evaluate as guard_eval

EVENTS_PATH = guard_eval.EVENTS_PATH
SUPPORT_VALUES = {"gate", "observe", "lifecycle", "none"}
REQUIRED_EVENT_KEYS = ("support",)


def _load_events(root: Path) -> set[str]:
    path = root / EVENTS_PATH
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {str(e.get("id")) for e in data.get("events", [])}


def _manifest_paths(root: Path) -> list[Path]:
    harnesses = root / "harnesses"
    if not harnesses.is_dir():
        return []
    return sorted(harnesses.glob("*/harness.json"))


def validate(root: Path) -> list[str]:
    """Return a list of harness-manifest errors (empty = clean)."""
    errors: list[str] = []
    known_events = _load_events(root)
    known_kinds = set(plugin_registry.registered_kinds()) | {"guardrail"}

    for manifest in _manifest_paths(root):
        rel = manifest.relative_to(root).as_posix()
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{rel}: invalid JSON ({exc})")
            continue
        if not isinstance(data, dict) or not str(data.get("name", "")).strip():
            errors.append(f"{rel}: missing 'name'")
            continue

        # A real harness (not the authoring template) must declare a tool_mapping;
        # without it the bootstrap renders an empty tool vocabulary in silence (I3).
        if data["name"] != "_template":
            mapping = data.get("tool_mapping")
            if not isinstance(mapping, dict) or not mapping:
                errors.append(
                    f"{rel}: missing or empty 'tool_mapping' "
                    f"(the bootstrap would render no tool vocabulary)"
                )

        for plugin in data.get("plugins", []) or []:
            kind = str(plugin.get("kind", ""))
            if kind and kind not in known_kinds:
                errors.append(
                    f"{rel}: unknown plugin kind {kind!r} "
                    f"(known: {sorted(known_kinds)})"
                )

        lifecycle = data.get("lifecycle")
        if lifecycle is None:
            continue  # a harness without lifecycle is valid (closed capability)
        if not isinstance(lifecycle, dict):
            errors.append(f"{rel}: 'lifecycle' must be an object")
            continue
        if str(lifecycle.get("schema", 1)) != "1":
            errors.append(f"{rel}: unsupported lifecycle schema {lifecycle.get('schema')!r}")
        events = lifecycle.get("events", {})
        if not isinstance(events, dict):
            errors.append(f"{rel}: lifecycle.events must be an object")
            continue
        for event_id, cap in events.items():
            if known_events and event_id not in known_events:
                errors.append(
                    f"{rel}: lifecycle event {event_id!r} is not in the canonical "
                    f"taxonomy ({EVENTS_PATH})"
                )
            if not isinstance(cap, dict):
                errors.append(f"{rel}: lifecycle.events.{event_id} must be an object")
                continue
            for key in REQUIRED_EVENT_KEYS:
                if key not in cap:
                    errors.append(f"{rel}: lifecycle.events.{event_id} missing {key!r}")
            support = str(cap.get("support", ""))
            if support and support not in SUPPORT_VALUES:
                errors.append(
                    f"{rel}: lifecycle.events.{event_id}.support {support!r} invalid "
                    f"(known: {sorted(SUPPORT_VALUES)})"
                )
            if cap.get("can_ask") and not cap.get("can_block"):
                errors.append(
                    f"{rel}: lifecycle.events.{event_id} declares can_ask without can_block"
                )
            if cap.get("resolved") and not cap.get("source"):
                errors.append(
                    f"{rel}: lifecycle.events.{event_id} has a resolved anchor with no source "
                    f"(version-freshness)"
                )
    return errors
