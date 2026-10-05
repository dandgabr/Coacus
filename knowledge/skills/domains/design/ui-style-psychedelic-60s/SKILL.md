---
name: "ui-style-psychedelic-60s"
description: "Provides the 1960s psychedelic rock poster UI style: melting liquid typography, vibrant optical vibration palettes, kaleidoscopic symmetry and fluid art-nouveau revival vectors. Use when designing music festival, creative studio or counterculture web interfaces."
---

# UI Style: 1960s Psychedelic & Liquid Light

Visual language born in the mid-1960s San Francisco counterculture (Wes Wilson, Victor Moscoso, Bonnie MacLean). Features melting, curvilinear hand-lettering that fills negative space, vibrating color contrasts, and psychedelic optical illusions.

---

## 🧭 When to Activate

- Designing music festivals, counterculture brands, experimental podcasts, or creative agency portfolios.
- Creating expressive, fluid, and emotive user journeys that break digital rigidity.

---

## 🎨 Visual DNA

- **Palette:** High-chroma complementary pairs creating optical vibration: electric purple (`#7B2CBF`), acid orange (`#FF6B35`), lime green (`#06D6A0`), hot magenta (`#F72585`), and sunshine yellow (`#FFD166`).
- **Type:** Liquid distorted display fonts (Alhambra, Dreamland, Cooper Black with liquid morphs, display type with bulging stems).
- **Shapes:** Concentric waves, undulating contour lines, liquid blobs, paisley motifs, and kaleidoscopic bilateral symmetry.
- **Imagery:** Solarized photography, high-contrast posterized silhouettes, and liquid light projection textures.

---

## 🛠️ Implementation Notes

```css
:root {
  --psy-magenta: #f72585;
  --psy-purple: #7209b7;
  --psy-orange: #ff6b35;
  --psy-yellow: #ffd166;
}

.psychedelic-card {
  background: radial-gradient(circle at center, var(--psy-orange), var(--psy-magenta) 50%, var(--psy-purple) 100%);
  border-radius: 40px 10px 40px 10px;
  box-shadow: 0 10px 30px rgba(114, 9, 183, 0.4);
}
```

---

## ♿ Accessibility

- Optical color vibration (e.g. pure red text directly over pure cyan) can trigger visual discomfort; always ensure solid backing cards and strict contrast verification.
- Provide clean, highly readable geometric grotesques for body copy and navigational links; reserve distorted liquid type strictly for large display headers.
