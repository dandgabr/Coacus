# Anatomy and Mannequin Principles

## Core Principle

Poses change, but a character's underlying skeletal structure and mass remain invariant unless a deliberate transformation (e.g., metamorphosis, lycanthropy) is requested.

## Geometric Mannequin

Before adding facial details, cloth folds, or weapons, build the figure from solid primitive volumes:

- **Head**: Sphere or tapered egg.
- **Neck**: Short cylinder angled slightly forward.
- **Thorax / Rib Cage**: Rounded box or tapered cylinder.
- **Pelvis**: Rigid basin box tilted forward or back depending on posture.
- **Limbs**: Two-stage cylinders (upper arm, forearm; thigh, shin) hinged on joint spheres (shoulders, elbows, knees).
- **Extremities**: Wedge-shaped feet planted on the contact plane; boxy or mitten-blocked hands.

Recommended construction order:
```text
SKELETON (line of action & bone lengths)
  ↓
MANNEQUIN (primitive 3D volumes)
  ↓
ANATOMY (muscle groups & flesh contours)
  ↓
COSTUME & GEAR (surfaces attached to bone anchors)
```

## Anatomical Anchors and Invariants

1. **Joint Hinge Planes**: Elbows and knees bend along a single plane. Never allow hyper-extended or rubbery limbs that break anatomical joint limits.
2. **Torso Twist Limits**: The thorax can rotate relative to the pelvis by up to 45° without moving the hips. Avoid unnatural 180° abdominal twists.
3. **Mass Conservation**: In extreme attack extension or impact compression, mass squashes and stretches while total volume remains visually constant.
