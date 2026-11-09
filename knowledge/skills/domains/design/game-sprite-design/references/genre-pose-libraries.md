# Genre Pose Libraries

## 1. Fighting Games

### Neutral Stance
- **Weight**: 60/40 or 50/50 distribution between back and lead foot.
- **Silhouette**: Clear negative space between limbs; 3/4 torso angle showing both arms.
- **Center of Mass**: Low and balanced, knees slightly bent.

### Attack Phases
```text
STARTUP / ANTICIPATION → ACTIVE FRAMES → RECOVERY
(Coil back, windup)       (Max extension)  (Weight resets)
```
- **Light Attacks**: 2-3 startup frames, 2 active, 3-4 recovery.
- **Heavy Attacks**: 6-10 startup frames, 3-5 active, 12-16 recovery.

### Hit Reactions
- **Standing Hitstun**: Head snaps back, spine curves inward, guard breaks.
- **Knockdown / Juggle**: Parabolic airborne arc with tumbling rotation; hard ground impact frame followed by settle.

---

## 2. Platformers

- **Run Cycle**: Clear squash on ground strike, extension on push-off, distinct airborne transition.
- **Jump Rising**: Streamlined upward silhouette, limbs tucked or driving upward.
- **Jump Apex**: Neutral hang frame signaling direction change.
- **Jump Falling**: Flared clothing/hair, arms raised, feet pointing downward toward anticipated impact.
- **Wall Interaction**: Hand and lead foot planted firmly against vertical surface without clipping.

---

## 3. Beat 'em Ups (2.5D Belt Scrollers)

- **Depth Planes**: Characters move on X and Z axes. The sprite baseline anchors the contact point on the ground plane.
- **Grapple & Throw**: Distinct holds (front grab, back grab), lifting anticipation, overhead toss, slam frame with shockwave dust.
- **Crowd Readability**: Exaggerated primary weapon/fist silhouette so the action reads even when surrounded by 4+ enemy sprites.

---

## 4. Side-View Shooters

- **Aim Angles**: Orthogonal (horizontal, vertical) and 45° diagonal aim poses with locked shoulder pivots.
- **Weapon Invariance**: Barrel, receiver, magazine, and stock retain identical pixel dimensions across all aim directions.
- **Recoil Dynamics**: Upper torso and arms absorb kickback without displacing hip or foot anchors.
