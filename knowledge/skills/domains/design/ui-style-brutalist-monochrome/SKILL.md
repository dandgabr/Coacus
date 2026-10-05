---
name: "ui-style-brutalist-monochrome"
description: "Provides the pure monochrome brutalism UI style: strict black-and-white palette (zero gray), architectural typography hierarchy, razor-sharp hairline borders and uncompromising structural clarity. Use when building severe editorial, architectural or minimalist tech interfaces."
---

# UI Style: Brutalist Monochrome

A disciplined distillation of architectural brutalism and Swiss typography into a zero-gray visual system. Strictly black (`#000000`) and white (`#FFFFFF`), relying purely on scale contrast, line weight, and spatial tension for information hierarchy.

---

## 🧭 When to Activate

- Architectural archives, luxury fashion indexation, intellectual publications, and software tools emphasizing raw clarity.
- When colors are deliberately removed to focus 100% of user attention on structure and typographical nuance.

---

## 🎨 Visual DNA

- **Palette:** Strictly binary: pure `#000000` and pure `#FFFFFF`. No grays, no tinting, no ambient blur.
- **Type:** High-precision sans-serif (Inter, Univers, Helvetica Neue, Söhne) paired with stark monospaced indices.
- **Borders & Dividers:** 1px or 2px solid hairline black/white borders, full-width grid dividing lines.
- **Imagery:** Inverted monochromatic bitmap images, 1-bit dithered portraits, or high-contrast duotone photography.

---

## 🛠️ Implementation Notes

```css
:root {
  --mono-black: #000000;
  --mono-white: #ffffff;
}
.mono-card {
  background: var(--mono-white);
  color: var(--mono-black);
  border: 2px solid var(--mono-black);
}
.mono-card:hover {
  background: var(--mono-black);
  color: var(--mono-white);
}
```

---

## ♿ Accessibility

- Pure black-on-white provides the maximum possible contrast ratio (21:1), easily satisfying WCAG AAA.
- Ensure clear, distinct outline focus rings on interactive elements without relying on color hue changes.
