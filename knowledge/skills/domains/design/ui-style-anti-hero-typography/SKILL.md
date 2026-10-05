---
name: "ui-style-anti-hero-typography"
description: "Provides the monumental type-driven anti-hero UI style: extreme typographic scale, zero decorative images or 3D distractions, radical spatial composition and glyph-led visual gravity. Use when crafting high-end editorial, studio or intellectual brand websites."
---

# UI Style: Type-Driven Minimal & Monumental Anti-Hero

A bold rejection of standard SaaS hero sections (no 3D mockups, no stock photography, no illustrations). Instead, colossal, razor-sharp typography takes up the entire viewport, treating letterforms as monumental architectural sculptures.

---

## 🧭 When to Activate

- Architecture studios, independent typography foundries, literary journals, avant-garde design agencies, and luxury monographs.
- Demanding immediate attention through pure typographic mastery and fearless negative space.

---

## 🎨 Visual DNA

- **Palette:** Restrained and academic: warm charcoal (`#1A1A1A`), off-white plaster (`#F9F9F8`), with singular editorial ink accents (ochre, cobalt, or vermilion).
- **Type:** Massive viewport-relative display type (`font-size: clamp(4rem, 15vw, 18rem)`), extreme weights (hairline paired with black), extended or condensed proportions.
- **Layout:** Asymmetric, edge-to-edge text locking, staggered vertical baselines, and generous editorial white space.

---

## 🛠️ Implementation Notes

```css
.anti-hero-title {
  font-size: clamp(3.5rem, 12vw, 14rem);
  line-height: 0.88;
  letter-spacing: -0.04em;
  font-weight: 800;
  margin: 0;
  text-transform: uppercase;
}
```

---

## ♿ Accessibility

- Monumental text must resize cleanly on mobile viewports without overflowing horizontally or clipping glyph descenders.
- Ensure correct heading hierarchy (`h1` through `h6`) is preserved regardless of visual presentation.
