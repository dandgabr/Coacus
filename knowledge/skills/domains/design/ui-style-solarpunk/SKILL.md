---
name: "ui-style-solarpunk"
description: "Provides the complete solarpunk UI and UX style (2008-present): optimistic ecological futures, sunlit aesthetics, botanical linen and watercolor textures, Voronoi biomorphic algorithms, garden-like navigation, low-energy budgets and hopeful microcopy. Use when designing climate, renewable energy, cooperative, sustainable lifestyle or biotech interfaces."
---

# UI Style: Solarpunk (Ecological, Pastoral & Biomorphic)

The definitive ecological "-punk" genre answering cyberpunk with tangible hope: renewable energy, community resilience, biomimetic engineering, and nature deeply woven into technology. Expressed in UI through three unified expressions: sunlit civic infrastructure, tactile botanical warmth (naturecore/pastoral), and computational biomorphic growth (cellular Voronoi/venation). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Climate and renewable energy platforms, ecological research, urban farming, mutual-aid collectives, and civic-tech tools.
- Sustainable fashion, organic food brands, and slow-living portals seeking artisanal botanical warmth.
- Modern biotech, environmental telemetry, and synthetic biology applications using algorithmic biological models.
- Reviewing sustainability claims to ensure the interface reflects honest performance budgets rather than greenwashing.

---

## 🕰️ Definition and Timeline

- **Origins:** Term coined in 2008 in the essay "From Steampunk to Solarpunk". Solidified by Adam Flynn's "Solarpunk: Notes toward a manifesto" (Project Hieroglyph, 2014) and the 2019 "A Solarpunk Manifesto". Considers technology as a partner of natural ecosystems rather than an extractive instrument.
- **The Pastoral/Naturecore Strand:** Draws from the 19th-century Arts and Crafts movement (William Morris) and the digital Cottagecore culture: woven linen textures, natural earth pigments, pressed botanical accents, and slow-paced design.
- **The Computational Biomorphic Strand:** Informed by parametric architecture (Neri Oxman, Frei Otto) and biomimicry: interfaces adopt structural laws evolved by biological systems (Voronoi tessellation, Fibonacci distributions, minimal surface tension, leaf xylem networks).
- **Difference from neighbors:** Unlike [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), which is neutral corporate wellness without sociopolitical ambition, Solarpunk celebrates visible community agency, renewable technology, and ecological optimism. Unlike dystopian [ui-style-biopunk](../ui-style-biopunk/SKILL.md), Solarpunk is radiant, clean, and regenerative.

---

## 🎨 Visual DNA

- **Color Palette:**
  - *Solar & Floral Accents:* Sun gold (`#F2B632`), terracotta clay (`#C8643B`), warm amber (`#F77F00`).
  - *Living Foliage:* Leaf and moss greens (`#2F7D4F`, `#8CC084`), photosynthetic cyan (`#00F5D4`), sage green (`#7D9D8B`).
  - *Natural Grounds:* Oatmeal linen (`#F7F4EE`), warm cream (`#FBF6E9`), and deep fertile loam (`#0B1D19`) for dark modes.
- **Typography:** Warm humanist serifs with calligraphic heritage (Fraunces, Cormorant Garamond, Recoleta) paired with organic sans-serifs (Plus Jakarta Sans, Nunito, Bricolage Grotesque).
- **Shapes & Partitions:** Asymmetric organic contours (`border-radius: 28px 12px 32px 14px`), Voronoi cell partitions, hexagon mesh structures, and soft deckle paper borders.
- **Texture & Lighting:** Sunlight radial gradients, delicate paper/linen grain, and thin organic membrane outlines (`border: 1px solid rgba(46, 196, 182, 0.35)`).

---

## 🖱️ Interaction and Motion

- **Growth Transitions:** Sections unfold like sprouting leaves (`scale: 0.96 -> 1.0`, 300–500ms ease-out); SVG vines draw gracefully with `stroke-dashoffset`.
- **Living Rhythms:** Ambient status indicators pulse gently with slow 4s biological breathing rhythms.
- **Tactile Softness:** Buttons settle with smooth organic deceleration rather than harsh mechanical snapping.
- Under `prefers-reduced-motion: reduce`, disable all pulsing animations and dynamic SVG drawing, showing immediate static layouts.

---

## 🧩 UX Patterns

- **Garden Navigation:** Information architecture structured around garden metaphors (Plots, Harvest, Community, Energy), while preserving standard locations and labels for search, cart, and account settings (NN/g Heuristic 4).
- **Low-Data / Eco-Mode:** Native toggle allowing users to disable heavy assets, video, and webfonts, reducing kilowatt-hour consumption per page visit.
- **Microcopy:** Warm, empowering, collective voice ("Our shared harvest", "Locally generated"); avoids doom counters in favor of concrete actionable impact figures.
- **Verification over Greenwashing:** Every ecological badge or sustainability claim is backed by transparent, verifiable metrics.

---

## 🛠️ Implementation Notes

```css
:root {
  --sun: #F2B632;
  --leaf: #2F7D4F;
  --moss: #8CC084;
  --clay: #C8643B;
  --paper: #FBF6E9;
  --ink: #1B3A2A;
  --bio-neon: #00F5D4;
}
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'Nunito', system-ui, sans-serif;
}
.solar-card {
  background: #ffffff;
  border: 1.5px solid var(--moss);
  border-radius: 28px 14px 32px 16px;
  box-shadow: 0 8px 24px rgba(27, 58, 42, 0.08);
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
}
.solar-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 30px rgba(27, 58, 42, 0.12);
}
.vine-path {
  stroke: var(--leaf);
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: grow 1.4s ease-out forwards;
}
@keyframes grow { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) {
  .vine-path { animation: none; stroke-dashoffset: 0; }
  .solar-card { transition: none; }
}
```

---

## ♿ Accessibility

- **Contrast Ratios:** Pale greens and golds on cream fail WCAG 1.4.3; strictly anchor body text in deep forest loam (`#1B3A2A`), reserving light greens and golds for fills and borders.
- **Non-Text Indicators:** Do not rely on green versus red alone to signify status (WCAG 1.4.1); always accompany status markers with accessible icons and text labels.
- **Performance Budget:** Respect low-bandwidth connections: compress vector assets, lazy-load media, and budget total page weight under 500KB.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Renewable energy grids, climate-action portals, organic farming cooperatives, environmental storytelling, sustainable e-commerce, and biotech research.
- **Caution:** High-density financial data terminals (apply color tokens without ornamental illustrations).
- **Avoid:** Organizations whose business models directly contradict ecological restoration (greenwashing hazard).

---

## ⚠️ Pitfalls

- Superficially pasting leaf clipart onto a generic corporate template without structural warmth or ecological performance consideration.
- Unreadable pastel text on light linen backgrounds.
- Heavy autoplay hero videos that consume excess bandwidth and contradict the low-carbon ethos.

---

## 📚 Sources

- Adam Flynn, "Solarpunk: Notes toward a manifesto", *Project Hieroglyph*, 2014.
- Neri Oxman, *Age of Entanglement*, MIT Media Lab, 2016.
- William Morris, *News from Nowhere*, 1890.
- Sustainable Web Design, *Web Sustainability Guidelines*, 2023 — https://sustainablewebdesign.org/
- W3C, *Web Content Accessibility Guidelines 2.2* — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling organic styles: [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md).
- Night counterpart: [ui-style-lunarpunk](../ui-style-lunarpunk/SKILL.md).
