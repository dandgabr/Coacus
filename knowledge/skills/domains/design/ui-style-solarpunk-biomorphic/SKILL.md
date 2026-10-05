---
name: "ui-style-solarpunk-biomorphic"
description: "Provides the biomorphic and generative growth UI style: Voronoi cells, algorithmic leaf veining, chlorophyll and solar gradients, fluid organic contours and living responsive curves. Use when building biotech, ecological science or regenerative technology interfaces."
---

# UI Style: Biomorphic & Generative Growth

A scientific-artistic design paradigm rooted in biomimicry and generative biological patterns. Utilizes Voronoi cell partitions, Fibonacci spiral distributions, leaf xylem venation, and bioluminescent gradients to create UI systems that feel dynamically alive.

---

## 🧭 When to Activate

- Biotech platforms, environmental data visualizations, ecological research institutes, and regenerative energy products.
- Presenting complex scientific and ecological data through organic, nature-engineered structures.

---

## 🎨 Visual DNA

- **Palette:** Photosynthetic green (`#2EC4B6`), bioluminescent cyan (`#00F5D4`), warm solar amber (`#F77F00`), deep fertile loam (`#0E2A24`), and pollen yellow (`#FFE45E`).
- **Shapes:** Voronoi modular tessellations, smooth organic bezier cards without sharp edges, and branching node dendrites.
- **Motion:** Gentle pulse breathing animations, smooth morphing blobs, and organic growth loading indicators.

---

## 🛠️ Implementation Notes

```css
.biomorphic-card {
  background: radial-gradient(circle at 80% 20%, rgba(0, 245, 212, 0.12), transparent), #0e2a24;
  border: 1px solid rgba(46, 196, 182, 0.3);
  border-radius: 40px 18px 36px 20px;
  color: #e8f5f1;
}
```

---

## ♿ Accessibility

- Dynamic biological morphs must honor `prefers-reduced-motion: reduce`.
- Maintain crisp, high-contrast typography inside organic containers.
