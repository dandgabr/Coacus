# Handedness and Asymmetry Audit

## The Mirroring Pitfall

In 2D games, mirroring a right-facing sprite horizontally to produce the left-facing sprite is standard optimization. However, naive horizontal flipping introduces critical defects:
- An eyepatch switches from the left eye to the right eye.
- A sword sheathed on the left hip teleports to the right hip.
- A watch, scar, or asymmetric emblem flips sides.

## Handedness Verification Protocol

1. **Tag Asymmetric Features**: In the character spec, explicitly enumerate all asymmetric elements:
   ```yaml
   asymmetry:
     - element: "leather holster"
       side: "right thigh"
     - element: "scar"
       side: "across left cheek"
   ```
2. **Explicit Opposite-Facing Generation**: When asymmetric elements are present, generate dedicated left-facing frames rather than relying on automatic canvas mirroring.
3. **Automated Handedness QA**: Run frame-by-frame color-marker tests (`handed-check`) to confirm that asymmetric color clusters reside on the anatomically correct side of the vertical axis.
