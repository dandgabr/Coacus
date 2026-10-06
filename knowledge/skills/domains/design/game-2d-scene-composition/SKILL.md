---
name: game-2d-scene-composition
description: >-
  Provides patterns and mathematical models for 2D game scene composition,
  multi-plane parallax layering, directional projected shadows, contact anchors,
  and repeating background tile quilting. Use when composing, laying out, or
  lighting 2D game levels and cinematic scene environments.
tags:
  - game-art
  - scene-composition
  - parallax
  - 2d-lighting
---

# Game 2D Scene Composition

Guides the architectural layout and composition of 2D game environments, coordinating multiple visual planes, parallax scroll velocities, foot-anchored projected shadows, and seamless texture loops.

## Core Directives

1. **Strict Plane Separation**: Organize visual assets into distinct velocity layers (`sky`, `midground`, `gameplay`, `foreground`) to preserve spatial depth.
2. **Foot-Anchored Shadow Projection**: Transform cast shadows using light-source squash and shear matrices with fixed ground contact points.
3. **Y-Depth Sorting**: Order overlapping characters and environmental props on the gameplay plane strictly by their ground anchor coordinates.
4. **Seamless Texture Quilting**: Ensure repeating background tiles are joined along minimum-error seam paths without visible repetition seams.

## Reference Modules

- Consult [planes-and-parallax.md](references/planes-and-parallax.md) for velocity factors, coordinate transforms, and plane hierarchy.
- Consult [projected-shadows-and-lighting.md](references/projected-shadows-and-lighting.md) for affine shadow matrices, shear angles, and ambient occlusion rules.
- Consult [repeating-tiles-quilting.md](references/repeating-tiles-quilting.md) for seamless tile generation and overlap seam minimization.
