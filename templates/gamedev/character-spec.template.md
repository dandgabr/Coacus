# Character Spec Template

A formal specification contract for 2D game characters to preserve proportional, anatomical, and visual identity across all generated animation frames.

```yaml
character:
  name: "character-id"

  height:
    real_cm: 180
    canonical_px: 128
    heads: 7.5

  body_type: "athletic"

  proportions:
    shoulder_width_heads: 2.2
    torso_height_heads: 2.3
    pelvis_width_heads: 1.4
    upper_arm_heads: 1.4
    forearm_heads: 1.2
    hand_heads: 0.75
    thigh_heads: 2.0
    shin_heads: 1.8
    foot_heads: 1.0

  body_mass:
    shoulders: "broad"
    chest: "defined"
    waist: "narrow"
    hips: "moderate"
    arms: "muscular"
    thighs: "dense"
    calves: "toned"

  appearance:
    skin: "#d8a078"
    hair: "short spiky black"
    eyes: "brown sharp"

  clothing:
    upper: "sleeveless martial gi navy-blue"
    lower: "loose canvas trousers off-white"
    shoes: "wrapped straw sandals"

  accessories:
    - "red cloth headband tied at back"

  asymmetry:
    - "bandaged right forearm and wrist"

  weapons: []

  palette:
    primary: ["#1e293b", "#0f172a"]
    secondary: ["#f1f5f9", "#cbd5e1"]
    accent: ["#ef4444", "#991b1b"]
    skin: ["#fed7aa", "#d8a078", "#9a3412"]

  canonical_orientation: "side-facing-right"
  approved_reference: "references/canonical-neutral.png"
```
