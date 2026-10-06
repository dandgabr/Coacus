---
name: game-sprite-design
description: >-
  Provides end-to-end design patterns, anatomical mannequin modeling, head-count
  proportions, multi-genre pose libraries, and hitbox alignment for consistent
  2D game sprites and animation frames. Use when generating, illustrating, or
  refining 2D game characters and visual gameplay assets.
tags:
  - game-art
  - 2d-sprites
  - character-design
  - animation
---

# Game Sprite Design

Acts as a specialized 2D Game Art and Sprite Design authority, enforcing absolute anatomical, proportional, and stylistic consistency across sequential animation frames and multi-character rosters.

## Core Directives

1. **Preserve Skeletal Proportions**: Bone lengths and cranial ratios defined in the character specification remain constant across all poses.
2. **Preserve Anatomical Mass**: Muscle mass and body volume must not unintentionally shrink or expand between frames.
3. **Geometric Mannequin First**: Construct poses using primitive volumes (spheres, boxes, cylinders) before rendering surface details or costume contours.
4. **World Scale Grounding**: All assets adhere to the project's global metric scale (`pixels_per_meter`), not arbitrary canvas boundaries.
5. **Enforce Negative Space**: Maintain readable silhouettes with clear separation between limbs and torso, ensuring readability at game viewport resolutions.

## Production Workflow

```text
1. SPECIFICATION LOAD
   ↓ Load character head-count, body mass, and palette rules.
2. MANNEQUIN BLOCKING
   ↓ Establish line of action, joint hinges, and silhouette balance.
3. GENRE POSE SELECTION
   ↓ Reference startup, active, and recovery frames from the genre library.
4. SURFACE RENDERING
   ↓ Apply costume layers, secondary motion (hair/cloth), and fixed palette.
5. COLLISION & HITBOX RIGGING
   ↓ Map sprite boundaries against hurtboxes, hitboxes, and pushboxes.
```

## Detailed Reference Modules

- Consult [anatomy-and-mannequin.md](references/anatomy-and-mannequin.md) for joint hinge limits, geometric volumes, and mass conservation.
- Consult [proportions-and-scale.md](references/proportions-and-scale.md) for head-count proportional scaling, world scale anchoring, and roster lineups.
- Consult [genre-pose-libraries.md](references/genre-pose-libraries.md) for fighting games, platformers, beat 'em ups, and side-view shooters.
- Consult [hitbox-hurtbox-alignment.md](references/hitbox-hurtbox-alignment.md) for collision box taxonomy and gameplay hit registration rules.
