---
name: "ui-style-fluid-liquid-morph"
description: "Provides the fluid liquid and organic metaball UI style: viscous blob physics, SVG goo filters, elastic jelly transitions, cohesive fluid joining and morphing boundary surfaces. Use when building experimental branding, creative agencies or playful interactive experiences."
---

# UI Style: Fluid Liquid & Metaball Morph

An interactive, physics-driven aesthetic treating interface elements as viscous fluid or molten mercury. Uses SVG goo filters, spring-tension physics, and morphing blobs to connect elements dynamically. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Creative development studios, experimental marketing landing pages, and interactive art installations.
- Communicating adaptability, fluidity, softness, and modern playful creativity.
- Crafting hero interactions where cards or buttons merge like liquid droplets.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in computer graphics metaball modeling (Jim Blinn, 1982), popularized on the web through SVG filter techniques (Lucas Bebber, 2015) and modern spring animation engines (Framer Motion).
- **Philosophy:** Breaking digital box rigidity. Transforming rigid geometric UI components into organic, fluid substances with surface tension and cohesive bonding.
- **Difference from neighbors:** Unlike [ui-style-psychedelic-60s](../ui-style-psychedelic-60s/SKILL.md), which is retro-illustrative and typography-focused, Fluid Liquid Morph is algorithmic, physics-based, interactive, and modern. Unlike [ui-style-solarpunk-biomorphic](../ui-style-solarpunk-biomorphic/SKILL.md), which uses Voronoi tessellations, Fluid Liquid uses continuous viscous merging.

---

## 🎨 Visual DNA

- **Palette:** Iridescent mercury chrome, neon pastels, deep bioluminescent liquid gradients (coral `#FF5E7E` to violet `#845EC2`), and deep dark background canvases (`#0F0A1C`).
- **Physics & Shapes:** Viscous metaballs, spring elasticity, morphing rounded corners (`border-radius: 32px`), and cohesive fluid bridges when elements approach each other.
- **Textures:** Smooth specular mirror reflections and chromatic refraction along fluid curves.
- **Depth:** Luminous layered glows (`box-shadow: 0 12px 30px rgba(132, 94, 194, 0.25)`).

---

## 🖱️ Interaction and Motion

- Elastic spring hover: buttons squish and stretch along movement vectors (`transform: scale(1.08, 0.94)`).
- Liquid merging: nearby interactive chips join together via SVG Gaussian blur and color-matrix threshold filters.
- Under `prefers-reduced-motion: reduce`, disable all goo filters and elastic stretching, rendering stable rounded buttons.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="fluid-liquid-morph"] {
  --bg: #0f0a1c;
  --surface: rgba(132, 94, 194, 0.12);
  --fg: #f0e6ff;
  --muted: #a393bf;
  --accent: #ff5e7e;
  --accent-fg: #ffffff;
  --border: rgba(255, 94, 126, 0.3);
  --radius: 28px;
  --font-body: 'Cabinet Grotesk', sans-serif;
  --font-display: 'Cabinet Grotesk', sans-serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Legibility protection:** Liquid morphing filters must wrap UI containers, never applying directly across text glyphs to prevent text blurring.
- **Motion sensitivity:** Always honor `prefers-reduced-motion: reduce` to protect users with vestibular disorders.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Creative agency portfolios, innovative beverage or beauty marketing, and experimental web showcases.
- **Avoid:** Data-heavy spreadsheets, document readers, and administrative dashboards.

---

## 📚 Sources

- Jim Blinn, "A Generalization of Algebraic Surface Drawing", *ACM Transactions on Graphics*, 1982.
- Lucas Bebber, "Creative Gooey Effects with SVG Filters", *Codrops*, 2015.
- W3C, *SVG Filter Effects Module Level 1*, 2023.

---

## 🔗 Integration with Other Skills

- Sibling interactive styles: [ui-style-micro-interactions](../ui-style-micro-interactions/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
