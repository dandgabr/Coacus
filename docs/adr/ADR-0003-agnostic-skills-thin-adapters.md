# ADR-0003: Agnostic Skills With Thin Per-Harness Adapters

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D2

## Context

Skills that cite concrete harness tools get locked to one harness. The
`superpowers` model is the only one of the three sources proven multi-harness.

## Decision

Option A: canonical skill bodies prescribe ACTIONS and intentions, never tool
names. Per-harness tool mappings live outside the canonical body in
`references/<harness>-tools.md` and are linked from a "Harness Adaptation"
section when applicable.

## Consequences

A validator enforces a tool-name denylist over canonical content (seeded
built-in list in F1, later derived from `harnesses/*/harness.json`). Porting a
skill to a new harness never edits the body; it adds a reference file.

## Evidence

`superpowers/skills/using-superpowers/references/{antigravity,codex,gemini,hermes,pi}-tools.md`;
`superpowers/docs/porting-to-a-new-harness.md:43-73`.
