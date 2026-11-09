# Animation Spec Template

Specification contract for 2D character animation loops, contact timings, and collision logic.

```yaml
animation:
  character: "character-id"
  state: "walk"
  fps: 12
  loop: true
  cell_dimensions:
    width: 256
    height: 256

  timing:
    total_frames: 8
    keyframe_indices: [0, 2, 4, 6]
    contact_frames:
      left_foot_strike: 0
      right_foot_strike: 4

  dynamics:
    squash_and_stretch: false
    ground_anchor: "foot-centroid"
    vertical_bounce_px: 4

  hitboxes:
    hurtbox_default:
      x: 104
      y: 40
      width: 48
      height: 180
    hitbox_active_frames: []
    pushbox:
      width: 40
      height: 160

  directional_rules:
    facing: "right"
    mirror_allowed: false
    asymmetry_notes: "Forearm bandage must remain on right arm; do not mirror naively."
```
