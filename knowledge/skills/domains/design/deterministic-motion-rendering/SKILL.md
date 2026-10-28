---
name: deterministic-motion-rendering
description: >-
  Provides offline animation and video export guidance when rendering scenes
  frame by frame, seeking arbitrary frames, or verifying reproducible
  fixed-timeline media. Covers scene readiness, frame evaluation and exported
  media evidence rather than ordinary live UI interaction.
tags:
  - offline-rendering
  - motion-graphics
  - frame-export
  - reproducibility
---

# Deterministic Motion Rendering

Render a declared scene state for a requested frame, independently of capture
speed or the order of previous requests. Keep creative decisions separate from
the machinery used to capture them. These contracts are Coacus conventions
informed by the sources in the references, not guarantees of identical pixels
on arbitrary machines.

## Establish the contract

Record the scene revision, input assets, seed, dimensions, frame rate, frame
count and delivery format. Preserve the requested specification; do not impose
a universal frame rate or silently retime content to match it.

Separate three operations: prepare required resources, evaluate the requested
frame, then capture its completed output. Keep wall clocks, live network data
and uncontrolled randomness outside scene evaluation. For simulations, either
evaluate directly or reconstruct from a known initial state with fixed steps.
Test repeated and shuffled frame requests before committing to a full export.

Load only the reference needed for the current operation:

- For fonts, decoded images, video and asynchronous scene resources, use
  [scene readiness](references/scene-readiness.md).
- For exact frame domains, randomness, seeking, technology adapters and
  subframe sampling, use [timeline and sampling](references/timeline-and-sampling.md).
- For capture records, external encoding recipes, decoded-output inspection
  and acceptance evidence, use [reproducibility and review](references/reproducibility-and-review.md).

## Preserve ownership

Use [interactive motion](../ui-motion-interaction/SKILL.md) for live controls,
gesture interruption and canonical timing tokens. Use
[GPU graphics](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md) for
canvas, shaders and scene implementation. A scroll-controlled player of an
existing image sequence belongs to
[scroll-driven motion](../ui-scroll-driven-motion/SKILL.md), even when this
skill produced its input frames.

Apply the existing [web accessibility](../../../engineering/practices/web-accessibility-wcag/SKILL.md)
requirements to the player and presentation context. An exported video's frame
rate does not establish interactive responsiveness or accessible playback.

## Report evidence honestly

Distinguish scene-state equality, decoded-pixel equality and final-file identity.
Name the environment and comparison method for each claim. Record missing
resources and unexecuted checks; a plausible recipe is not a successful export.
Review narrative continuity and legibility separately from technical validity.
