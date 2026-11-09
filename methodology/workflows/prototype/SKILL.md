---
name: prototype
description: Use when validating uncertain interaction physics or state transitions, to build disposable logic or UI prototypes before writing production code.
---

# Prototype

Build disposable, focused prototypes to de-risk unknown state transitions,
performance bottlenecks, or visual interactions before committing to a production
specification.

## Two-branch prototyping

Bifurcate exploration into logic versus presentation:

### 1. Logic prototype (State machines & protocols)
- **Goal:** Verify whether the state model, concurrency invariants, and transition
  rules hold under stress.
- **Form:** A self-contained script or minimal test harness that exercises transitions
  without UI overhead.
- **Scenario matrices:** Exercise the happy path, out-of-order events, network drops,
  and rapid repeated submissions.
- **Assertion:** When the logic state settles, all internal invariants match the
  mathematical model.

### 2. UI prototype (Visual & tactile exploration)
- **Goal:** Evaluate how layout, typography, and motion feel to a human operator.
- **Form:** A throwaway view or sandbox route supporting quick directional switching
  (e.g., query parameter variants `?variant=a|b|c`).
- **Fixture states:** Every UI variant must be evaluated against four standard
  fixtures:
  1. *Empty state:* Zero records, zero notifications, onboarding prompts.
  2. *Typical state:* Standard volume, expected string lengths, average telemetry.
  3. *Dense state:* High data volume, narrow viewport bounds, tabular stress.
  4. *Edge state:* Very long strings, missing metadata, slow asset loads.

## The disposable contract

- **Prototypes are throwaway artifacts:** They exist solely to generate evidence,
  resolve architectural ambiguity, and confirm user preferences.
- **No production grafting:** Never merge throwaway prototype code directly into
  production without building the proper test seams and following strict
  test-driven development.
- **Extract decisions, not code:** Once the prototype answers the core question,
  capture the resolved decisions in an architecture decision record (ADR) or spec,
  then delete or archive the prototype.
