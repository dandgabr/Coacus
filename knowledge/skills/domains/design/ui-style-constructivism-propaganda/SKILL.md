---
name: "ui-style-constructivism-propaganda"
description: "Provides the constructivist and agitprop poster UI style: bold 45-degree diagonals, stark black-red-cream palettes, dynamic geometric photomontage, dynamic typography and industrial structural lines. Use when designing high-impact editorial, cultural or statement web interfaces."
---

# UI Style: Constructivism & Agitprop Graphic

Graphic radicalism derived from early 20th-century avant-garde and constructivism (El Lissitzky, Aleksandr Rodchenko, Varvara Stepanova). Characterized by aggressive 45-degree diagonal axes, heavy black and scarlet geometric primitives, photomontage frames, and typography acting as primary architectural structure.

---

## 🧭 When to Activate

- Designing bold editorial features, cultural manifesto pages, exhibition hubs, or statement brand interfaces.
- Replacing conventional symmetrical grids with engineered dynamic tension and industrial rhythm.
- Creating high-contrast activist or avant-garde visual campaigns.

---

## 🎨 Visual DNA

- **Palette:** Stark tri-color base: Soviet red/scarlet (`#E63946` or `#D90429`), pitch black (`#111111`), and warm aged newsprint/cream (`#F4EBD9` or `#EFE6D5`).
- **Type:** Heavy geometric grotesque and industrial sans-serif caps (Bebas Neue, Anton, Oswald, Archivo Black) set along diagonal shear angles and dynamic baseline shifts.
- **Geometry:** Strong 45° and 135° diagonal rules, solid triangles, circular targets, red wedges, and heavy structural dividers.
- **Photomontage:** High-contrast duotone or black-and-white photography with angular geometric cutouts and red tint overlays.

---

## 🛠️ Implementation Notes

```css
:root {
  --constructivist-red: #d90429;
  --constructivist-black: #111111;
  --constructivist-cream: #f4ebd9;
  --angle-dynamic: -12deg;
}

.hero-banner {
  background: var(--constructivist-cream);
  color: var(--constructivist-black);
  border-left: 12px solid var(--constructivist-red);
}

.diagonal-accent {
  transform: rotate(var(--angle-dynamic));
  background: var(--constructivist-red);
  color: #fff;
  font-weight: 900;
  text-transform: uppercase;
}
```

---

## ♿ Accessibility

- Contrast between scarlet (`#D90429`) and pure black must be avoided for text; always pair red against cream/white for WCAG AA compliance (ratio > 4.5:1).
- Rotated headlines must remain accessible to screen readers through standard semantic headings (`h1`–`h6`).
- Support `prefers-reduced-motion: reduce` by disabling dynamic angular hover transitions.
