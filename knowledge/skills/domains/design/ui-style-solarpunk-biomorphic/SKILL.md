---
name: "ui-style-solarpunk-biomorphic"
description: "Provides the biomorphic and generative growth UI style: Voronoi cells, algorithmic leaf venation, chlorophyll and solar gradients, fluid organic contours and living responsive curves. Use when building biotech, ecological science or regenerative technology interfaces."
---

# UI Style: Biomorphic & Generative Growth

A scientific-artistic design paradigm rooted in biomimicry, generative biological patterns, and living systems. Utilizes Voronoi cell partitions, Fibonacci spiral distributions, leaf xylem venation, and bioluminescent gradients to create UI systems that feel dynamically alive. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Biotech platforms, environmental data visualizations, ecological research institutes, and regenerative energy products.
- Presenting complex scientific and ecological data through organic, nature-engineered structures.
- Modern sustainability products seeking an advanced, high-tech biological aesthetic.

---

## 🕰️ Definition and Timeline

- **Origins:** Emerged at the intersection of parametric architecture (Neri Oxman, Frei Otto) and algorithmic generative design in the late 2010s and early 2020s.
- **Philosophy:** Nature as the ultimate engineer. Interfaces adopt structural patterns evolved by biology over billions of years (cellular tessellation, minimal surface tension, branching networks).
- **Difference from neighbors:** Unlike [ui-style-solarpunk-naturecore](../ui-style-solarpunk-naturecore/SKILL.md), which is rustic, pastoral, and linen-textured, Biomorphic is high-tech, parametric, algorithmic, and computational. Unlike [ui-style-biopunk](../ui-style-biopunk/SKILL.md), which is dark, gritty, and mutational, Biomorphic is luminous, clean, and regenerative.

---

## 🎨 Visual DNA

- **Palette:** Photosynthetic green (`#2EC4B6`), bioluminescent cyan (`#00F5D4`), warm solar amber (`#F77F00`), deep fertile loam (`#0B1D19`), and pollen yellow (`#FFE45E`).
- **Shapes & Partitions:** Voronoi modular tessellations, smooth organic bezier cards without sharp corners (`border-radius: 36px 14px 32px 18px`), and branching node dendrites.
- **Gradients:** Radial bioluminescent blooms, subtle organic pulse breathing animations, and photosynthetic translucency.
- **Depth:** Soft luminous backdrops combined with thin organic membrane borders (`border: 1px solid rgba(46, 196, 182, 0.35)`).

---

## 🖱️ Interaction and Motion

- Organic cell swelling: hovering a card causes its asymmetric border-radius to shift gently, mimicking cellular mitosis or fluid membrane elasticity.
- Pulse breathing: ambient status badges pulse slowly like living chloroplasts (4s breathing cycle).
- Under `prefers-reduced-motion: reduce`, disable continuous breathing pulses and morphing radius transitions.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="solarpunk-biomorphic"] {
  --bg: #0b1d19;
  --surface: #102923;
  --fg: #e8f5f1;
  --muted: #6a9b8f;
  --accent: #2ec4b6;
  --accent-fg: #0b1d19;
  --border: rgba(46, 196, 182, 0.35);
  --radius: 32px;
  --font-body: 'Plus Jakarta Sans', sans-serif;
  --font-display: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Text contrast:** Ensure neon cyan and green accents are paired against deep loam green (`#0B1D19`) to exceed the 4.5:1 ratio requirement.
- **Focus visibility:** Provide distinct, high-contrast cyan focus outlines (`#00F5D4`) on all interactive controls.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Climate tech dashboards, synthetic biology tools, regenerative agriculture portals, and advanced healthcare platforms.
- **Avoid:** Traditional banking, tax accounting, and retro gaming sites.

---

## 📚 Sources

- Neri Oxman, *Age of Entanglement*, MIT Media Lab, 2016.
- D'Arcy Wentworth Thompson, *On Growth and Form*, Cambridge University Press, 1917/1992.
- Biomimicry Institute, *Nature's Design Principles for Technology*, 2022.

---

## 🔗 Integration with Other Skills

- Sibling living styles: [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md).
