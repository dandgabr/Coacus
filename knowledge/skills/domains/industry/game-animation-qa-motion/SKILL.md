---
name: game-animation-qa-motion
description: >-
  Provides rigorous quality assurance methodologies for 2D game animations,
  verifying motion continuity, physical arcs, handedness asymmetry preservation,
  stride synchronization, and seam pop elimination. Use when auditing, inspecting,
  or testing 2D character animation loops and gameplay sprite sheets.
tags:
  - game-qa
  - animation-testing
  - motion-continuity
  - quality-assurance
---

# Game Animation QA Motion

Specialized quality assurance and verification authority for 2D game character animations, testing physical motion continuity, trajectory curves, handedness consistency, and seamless locomotion cycles.

## Core Directives

1. **Eliminate Seam Pop**: Test cyclic locomotion loops at operational frame rates, rejecting cycles where head, weapon, or torso trajectories jump visibly at loop wraparound.
2. **Strict Handedness Audit**: Enforce asymmetry rules when flipping characters; verify that one-sided items (watches, patches, scabbards) do not swap sides.
3. **Verify Foot Contact Stance**: Check unintended foot sliding relative to the supporting surface and synchronize stride with movement where appropriate; allow artist-reviewed stylization and other documented exceptions.
4. **Inspect Trajectories**: Compare jumping, falling, and recoil motion with the intended controller and animation timing; investigate unintended discontinuities without rejecting deliberate stylization or holds.

## Reference Modules

- Consult [motion-continuity-checks.md](references/motion-continuity-checks.md) for trajectory tracking, spacing, impact timing, and smear frames.
- Consult [handedness-and-symmetry-audit.md](references/handedness-and-symmetry-audit.md) for asymmetric feature tagging and opposite-facing generation.
- Consult [seam-pop-and-stride-measurement.md](references/seam-pop-and-stride-measurement.md) for loop wraparound tests and stride length measurement.
