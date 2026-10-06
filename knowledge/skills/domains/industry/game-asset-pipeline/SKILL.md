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

1. **Deterministic Soft-Alpha Unmix**: Decompose edge color blends into despilled RGB and partial alpha instead of destructive edge peeling.
2. **Backbone Lattice Alignment**: Recover true pixel-art grids using fractional pitch detection and phase synchronization; never perform naive raster resampling.
3. **Loop Seam Healing**: Eliminate cycle jumps ("seam pop") in walk and run cycles using optical-flow frame interpolation and foot-anchor locking.
4. **Runtime Manifest as Single Source of Truth**: Emit explicit absolute bounding boxes (`frame_layout`) to prevent engine-side alpha guessing.

## Reference Modules

- Consult [chroma-soft-alpha-unmix.md](references/chroma-soft-alpha-unmix.md) for color-distance bounds, key selection, and despill equations.
- Consult [pixel-unfake-lattice.md](references/pixel-unfake-lattice.md) for pitch detection, median-cut palettes, and integer upscaling.
- Consult [loop-repair-and-interpolation.md](references/loop-repair-and-interpolation.md) for RIFE neural interpolation and stride synchronization.
- Consult [runtime-manifest-contracts.md](references/runtime-manifest-contracts.md) for Phaser, Flame, Godot, and Aseprite JSON schemas.
