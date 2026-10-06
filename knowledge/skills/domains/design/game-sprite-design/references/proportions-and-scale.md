# Proportions, Scale, and Canonical Lineup

## Head-Count Proportions

To prevent character drift during multi-frame generation, declare canonical proportions relative to the character's own cranial height (cranial crown to chin):

```yaml
proportions_standard_hero:
  total_height: 7.5 heads
  shoulder_width: 2.2 heads
  torso_height: 2.3 heads
  pelvis_width: 1.4 heads
  upper_arm: 1.4 heads
  forearm: 1.2 heads
  hand: 0.75 heads
  thigh: 2.0 heads
  shin: 1.8 heads
  foot: 1.0 heads
```

- **Chibi / SD Style**: 2.0 to 3.5 heads.
- **Classic 16-bit Action**: 4.0 to 5.5 heads.
- **Heroic / Anime Realistic**: 7.0 to 8.5 heads.

## World Scale Invariance

Scale is an absolute property of the game universe, not of the generation cell:
- Establish a global constant: `WORLD_SCALE = pixels_per_meter` (e.g., 100 px = 1.0 m).
- A 1.80m swordsman measures 180 px; a 2.10m brawler measures 210 px.
- Never resize characters to fit arbitrary cell boxes. Increase the frame margin instead.

## Master Lineup Verification

Before finalizing any character sprite set, arrange all game characters side by side along a single ground line:
1. Verify relative eye levels and shoulder heights.
2. Confirm head sizes are mutually coherent unless stylization explicitly dictates otherwise.
3. Validate silhouette uniqueness across the roster.
