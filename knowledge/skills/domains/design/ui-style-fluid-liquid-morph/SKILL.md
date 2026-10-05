---
name: "ui-style-fluid-liquid-morph"
description: "Provides the fluid liquid and organic metaball UI style: viscous blob physics, SVG goo filters, elastic jelly transitions and morphing boundary surfaces. Use when building experimental branding, creative agencies or playful interactive experiences."
---

# UI Style: Fluid Liquid & Metaball Morph

An interactive, physics-driven aesthetic treating interface elements as viscous fluid or molten mercury. Uses SVG goo filters, spring-tension physics, and morphing blobs to connect elements dynamically.

---

## 🧭 When to Activate

- Creative development studios, experimental marketing landing pages, and interactive art installations.
- Communicating adaptability, fluidity, softness, and modern playful creativity.

---

## 🎨 Visual DNA

- **Palette:** Iridescent mercury chrome, neon pastels, deep bioluminescent liquid gradients (e.g. coral to violet).
- **Physics:** Spring elasticity, cohesive fluid joining (metaball fusion when elements come into close proximity).
- **Textures:** Smooth mirror reflections, chromatic refraction along liquid curves.

---

## 🛠️ Implementation Notes

```css
.goo-filter-container {
  filter: url('#goo');
}
```
```html
<svg style="visibility: hidden; position: absolute;" width="0" height="0">
  <filter id="goo">
    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
    <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="goo" />
    <feComposite in="SourceGraphic" in2="goo" operator="atop" />
  </filter>
</svg>
```

---

## ♿ Accessibility

- Liquid morphs and melting deformations must not compromise text readability; wrap fluid effects around UI wrappers rather than deforming text glyphs directly.
- Must honor `prefers-reduced-motion: reduce`.
