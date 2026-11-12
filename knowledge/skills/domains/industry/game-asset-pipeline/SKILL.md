---
name: game-asset-pipeline
description: >-
  Provides automated 2D sprite processing, soft-alpha unmixing, pixel art lattice
  recovery, RIFE frame interpolation, atlas packing, and engine manifest exports.
  Use when automating, extracting, assembling, or integrating 2D game sprite sheets
  with engines such as Phaser, Flame, Godot, or Unity.
tags:
  - game-dev
  - asset-pipeline
  - sprite-sheets
  - image-processing
---

# Game Asset Pipeline

Governs the technical automation, image-processing mathematics, and engine integration pipelines for 2D game sprites, sheets, and animation loops.

## Core Directives

1. **Soft-Alpha Estimation**: Preserve the source; estimate alpha and despill under explicit compositing assumptions. Unknown foreground and alpha cannot generally be recovered uniquely.
2. **Backbone Lattice Alignment**: Recover true pixel-art grids using fractional pitch detection and phase synchronization; avoid naive raster resampling.
3. **Optional Loop Repair**: Inspect playback first; use hand editing or interpolation only when needed, preserving timing and reviewing artifacts and contact points.
4. **Runtime Manifest**: Record explicit atlas rectangles, trim offsets, source-space pivots and frame durations. Preserve the legacy `frame_layout` contract where applicable and follow the migration guidance.

## Reference Modules

- Consult [chroma-soft-alpha-unmix.md](references/chroma-soft-alpha-unmix.md) for the compositing model, ambiguity, assumptions and key selection.
- Consult [pixel-unfake-lattice.md](references/pixel-unfake-lattice.md) for pitch detection, median-cut palettes, and integer upscaling.
- Consult [loop-repair-and-interpolation.md](references/loop-repair-and-interpolation.md) for optional interpolation, timing preservation and contact-point review.
- Consult [runtime-manifest-contracts.md](references/runtime-manifest-contracts.md) for the custom manifest, legacy layout and engine adapter requirements.
