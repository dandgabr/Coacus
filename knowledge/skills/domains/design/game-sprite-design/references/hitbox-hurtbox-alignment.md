# Hitbox and Hurtbox Alignment

## Collision Box Taxonomy

Gameplay systems operate on abstract geometric bounding boxes rather than raw pixel contours:

1. **Sprite Boundary**: The visual envelope containing RGB pixels.
2. **Hurtbox**: Vulnerable region where receiving an attack triggers damage and hitstun.
3. **Hitbox**: Damaging region active during specific frames that inflicts damage on opponent hurtboxes.
4. **Pushbox**: Physical exclusion zone preventing characters from walking through each other.

```text
+-------------------+
|      [HEAD]       |  <-- High Hurtbox
|    +--------+     |
|    | PUSH-  | ===>|  <-- Attack Hitbox (Extended Fist)
|    |  BOX   |     |
|    +--------+     |  <-- Mid Hurtbox (Torso)
|     /      \      |
|    /        \     |  <-- Low Hurtbox (Legs)
+-------------------+
```

## Design and Alignment Rules

- **Lag Behind Visuals on Recovery**: Never let a damaging hitbox persist when the character enters the recovery wind-down phase.
- **Vulnerability Extension**: When a character extends a heavy attack, their hurtbox must extend along the limb (risk vs. reward).
- **Floor Pinning**: Pushbox bases must align directly with the ground plane anchor to prevent jittering during stance changes.
- **Disjointed Hitboxes**: Weapons (swords, bullets, energy beams) should feature hitboxes that extend beyond their hurtboxes, granting defensive advantage.
