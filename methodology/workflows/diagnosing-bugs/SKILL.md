---
name: diagnosing-bugs
description: Use when a bug or performance regression is hard to find, to build a tight pass/fail feedback loop before forming any hypothesis, then fix and lock it down.
---

# Diagnosing bugs

A disciplined diagnosis loop for hard bugs and regressions. Work the phases in
order; do not skip Phase 1.

## Phase 1 — Build the loop (this is the skill)

A **tight loop** is a signal that goes red on *this* bug and green when it is
fixed. If you have one, you will find the cause. If you do not, no amount of
staring at code will save you. Spend disproportionate effort here.

Ranked techniques to build one, roughly cheapest first:

1. A failing test at the right seam.
2. A direct HTTP request that reproduces it.
3. A CLI invocation diffed against a known-good snapshot.
4. A headless browser run for a UI bug.
5. Replay a captured trace.
6. A throwaway harness around the suspect unit.
7. Property-based or fuzz testing when inputs are broad.
8. A bisection harness over commits.
9. A differential run: old versus new.
10. A human-in-the-loop script that walks the manual steps, as a last resort.

**Treat the loop as a product.** Make it faster, sharpen the assertion to the
specific symptom (not "did not crash"), and make it deterministic by pinning time,
seeding randomness, isolating the filesystem and freezing the network. A flaky
30-second loop is barely better than none; a deterministic 2-second loop is a
superpower.

For a non-deterministic bug the goal is not a clean reproduction but a **higher
reproduction rate**: a 50% flake is debuggable, a 1% flake is not.

**Hard stop:** do not hypothesise without a loop. Reading code to build a theory
before the loop exists is the exact failure this skill prevents.

Completion criterion — the loop is red-capable, deterministic, fast and runnable
by the agent, unattended.

## Phase 2 — Minimise

Reduce the reproduction to the smallest input and the fewest moving parts before
changing anything.

## Phase 3 — Hypotheses

Write three to five **falsifiable** hypotheses before testing any. Each carries a
prediction: if X is the cause, then changing Y will make the bug disappear. If you
cannot state the prediction, it is a vibe, not a hypothesis.

## Phase 4 — Instrument

Change one variable at a time. One breakpoint beats ten logs. Never log everything
and grep. Tag every temporary log with a unique marker so cleanup is a single
search.

## Phase 5 — Fix and lock it down

Write the regression test at the seam **before** the fix. If no correct seam
exists, that itself is the finding: the architecture is preventing the bug from
being locked down — report it.

## Phase 6 — Clean up

Remove the tagged instrumentation, confirm the loop is green, and state the
hypothesis that proved correct in the commit or PR message so the next debugger
learns.

## Secrets

Before building a loop, redact every secret: keep credentials in the environment,
and quote only the signal-carrying lines.
