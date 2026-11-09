---
name: "ui-style-isometric"
description: "Provides the isometric illustration and UI technique (engineering drawing origins, video games from 1981, web revival 2010s-present): equal-foreshortening 30-degree axes, 2:1 dimetric pixel art, CSS transform and SVG construction, covering geometry, shading, layout, motion and WCAG handling. Use when designing explainer illustrations, product diagrams, isometric dashboards or game-like scenes without needing a WebGL renderer."
---

# UI Style: Isometric Projection & Axonometric Engineering

> "In axonometric projection, parallel lines in three-dimensional space remain parallel in the projection, preserving dimensional measurement and structural relationships without the visual convergence of perspective."  
> — Carl Farish, *On Isometrical Perspective* (1820)

Isometric projection is an exact spatial representation and technical illustration system, not an emotional mood. By equal foreshortening of all three principal axes ($120^\circ$ separation), isometric scenes deliver tangible depth, mechanical clarity, and direct dimensional measurement without the runtime overhead or perspective distortion of a 3D graphics pipeline. For real-time 3D camera scenes, use [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).

---

## 🧭 When to Activate

- Authoring architectural cutaways, infrastructure topologies, data pipelines, hardware apparatus, and mechanical flowcharts.
- Building interactive 2.5D game worlds, tactical RPG maps, or simulation consoles using lightweight 2D vectors or canvas sprites.
- Delivering spatial depth and physical tangibility without WebGL dependencies, GPU context loss risks, or heavy 3D asset bundles.
- Explaining multi-layered software stacks, request lifecycles, and component hierarchies through stacked spatial planes.

---

## 🕰️ Definition, Lineage, and Timeline

- **Mathematical Foundations (1820):** Formalized by Professor William Farish at Cambridge University for engineering drawings. The object is rotated $45^\circ$ about the vertical axis and tilted $\arcsin(1/\sqrt{3}) \approx 35.264^\circ$ horizontally, causing all three principal axes to foreshorten equally by a factor of $\sqrt{2/3} \approx 0.816$.
- **Video Game Evolution (1981–1990s):** Early hardware lacked hardware division; true $30^\circ$ lines created jagged, stepped aliasing on raster screens. Video games adopted *dimetric projection* with a 2:1 pixel ratio ($\arctan(0.5) \approx 26.565^\circ$): *Treasure Island* (1981), *Zaxxon* (1982), *Q*bert* (1982), and *Knight Lore* (1984).
- **Web & Interface Revival (2010s–present):** Vector SVG, CSS 3D matrix transforms, and high-DPI displays enabled high-precision $30^\circ$ isometric vector diagrams for developer tooling, cloud architectures, and SaaS landing pages.
- **Absolute Style Vetos:**
  - **No perspective convergence:** Lines parallel in world space MUST remain parallel; vanishing points violate axonometric discipline.
  - **No skewed viewport text:** Typography and annotations MUST remain upright in screen space; skewing text into 3D planes degrades legibility and WCAG compliance.
  - **No unanchored floating geometry:** Every mechanical or architectural element must connect to a visible foundation, baseplate, or mounting bracket.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AXONOMETRIC SUBGENRE COMPARISON MATRIX                          │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ Dimension                  │ True Isometric (30°)        │ Dimetric Pixel Art (2:1)    │
├────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Axis Angles                │ 30° / 90° / 150°            │ 26.565° / 90° / 153.435°    │
│ Primary Medium             │ SVG, Canvas 2D, CSS 3D      │ Indexed Pixel Sprites       │
│ Coordinate Ratios          │ [cos 30°, sin 30°] ≈ [0.866, 0.5] │ [2px horizontal, 1px vertical]│
│ Typical Application        │ Technical Architecture, SaaS│ Retro Games, Indie Consoles │
│ Shading Technique          │ 3-Tone + Hermite Lathe      │ Flat Dithered Pixel Steps   │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

- **Axonometric Integrity:** Verticals stay strictly vertical ($90^\circ$); diagonal grid lines run precisely at $30^\circ$ (or $26.565^\circ$ for pixel art).
- **Four-Tone Illumination:** Light emanates from an infinite directional source positioned top-left-front. Top face receives direct light (1.15×), left face diffuse light (1.00×), right face shadow (0.80×), and internal cutaway cavities receive occlusion tone (0.60×).
- **Mechanical Cutaway Craft:** Complex apparatus uses cutaway cross-sections, segmented conduit routing, and exploded-view offsets along principal axes. See [Isometric Mechanical Craft](references/isometric-mechanical-craft.md).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Directional Planar Facets:**
   - Surfaces reflect light according to the surface normal relative to the standard isometric illumination vector $\mathbf{L} = [-1, 1, 1] / \sqrt{3}$.
   - Planar facets use uniform flat fills; avoid soft radial gradients that contradict the parallel projection.
2. **Curved Solids of Revolution (Hermite Shading):**
   - For cylinders, shafts, and collars, compute surface luminance continuously via monotone cubic Hermite interpolation along the longitudinal axis ($dr/ds$), maintaining crisp specular creases at shoulders and fillets.
3. **Cast Shadows:**
   - Cast shadows project onto the base plane as flat, skewed 30-degree polygons with deep neutral opacity (`rgba(15, 23, 42, 0.25)` to `0.40`).

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Isometric Grid & Geometry Tokens */
  --iso-angle: 30deg;
  --iso-sin: 0.5;
  --iso-cos: 0.866025;
  --iso-ratio: 0.57735; /* tan(30deg) */

  /* Surface Luminance Multipliers */
  --iso-face-top: hsl(215, 25%, 95%);
  --iso-face-left: hsl(215, 20%, 82%);
  --iso-face-right: hsl(215, 22%, 68%);
  --iso-face-cavity: hsl(215, 25%, 45%);

  /* Line Work & Boundaries */
  --iso-stroke-outer: #0f172a;
  --iso-stroke-inner: #334155;
  --iso-stroke-seam: rgba(51, 65, 85, 0.4);
  --iso-stroke-width: 1.5px;

  /* Accent & Interactive States */
  --iso-accent-core: #2563eb;
  --iso-accent-glow: rgba(37, 99, 235, 0.35);
  --iso-hover-lift: -6px;
  --iso-shadow-cast: rgba(15, 23, 42, 0.2);
}
```

---

## 🔤 Typography & Lettering Architecture

- **Unskewed Screen Orthogonality:** Labels, metric values, and textual annotations MUST remain upright in screen space. Never project text onto 30-degree planes; skewing typography impairs reading speed and legibility.
- **Leader Lines:** Connect upright callout text to target components using crisp $30^\circ$ or $90^\circ$ angled leader lines terminating in a solid $4\text{px}$ circular anchor dot.
- **Typographic Hierarchy:**
  - Display / Architecture Titles: High-contrast geometric sans (`Inter`, `Space Grotesk`, `Plus Jakarta Sans`), semi-bold.
  - Component Callouts & Metrics: Monospaced technical sans (`JetBrains Mono`, `Fira Code`), $11\text{px}$–$13\text{px}$, tabular figures (`font-variant-numeric: tabular-nums`).

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Axis-Locked Motion:** When an element hovers or activates, motion must occur strictly along the vertical axis (`translateY(-6px)`) or along the $30^\circ$ projection vectors.
- **Exploded Assembly Inspection:** On click or step trigger, complex apparatus separates into sub-components expanding along their mounting shafts. Springs use critically damped physics ($\zeta = 1.0$, stiffness $180\text{ N/m}$) without oscillation.
- **Depth Sorting During Motion:** Interactive tiles must dynamically update their `z-index` or SVG DOM position based on centroid depth coordinates ($D = x + y + z$) so raised elements properly occlude background tiles without clipping.
- **Reduced Motion:** When `prefers-reduced-motion: reduce` is detected, animations collapse to instant state switches; hover elevation transitions are disabled.

---

## 🧩 Canonical Component Specifications

### 1. Isometric Interactive Tile (CSS / SVG Hybrid)

```html
<div class="iso-tile" role="button" tabindex="0" aria-label="Database Storage Cluster">
  <svg class="iso-svg" viewBox="0 0 120 100" width="120" height="100" aria-hidden="true">
    <!-- Base Cast Shadow -->
    <polygon points="60,90 110,65 60,40 10,65" class="iso-shadow" />
    <!-- 3D Solid Extrusion -->
    <g class="iso-solid">
      <!-- Left surface with diffuse light -->
      <polygon points="10,55 60,80 60,50 10,25" class="iso-face-left" />
      <!-- Right surface in shadow -->
      <polygon points="60,80 110,55 110,25 60,50" class="iso-face-right" />
      <!-- Top surface with direct illumination -->
      <polygon points="60,20 110,45 60,70 10,45" class="iso-face-top" />
    </g>
  </svg>
  <div class="iso-label">
    <span class="iso-label-title">Storage Tier</span>
    <span class="iso-label-stat">99.99%</span>
  </div>
</div>
```

```css
.iso-tile {
  position: relative;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  outline: none;
}
.iso-solid {
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
  transform-origin: 60px 80px;
}
.iso-tile:hover .iso-solid,
.iso-tile:focus-visible .iso-solid {
  transform: translateY(var(--iso-hover-lift));
}
.iso-tile:focus-visible {
  outline: 2px solid var(--iso-accent-core);
  outline-offset: 4px;
}
.iso-face-top { fill: var(--iso-face-top); stroke: var(--iso-stroke-outer); stroke-width: var(--iso-stroke-width); }
.iso-face-left { fill: var(--iso-face-left); stroke: var(--iso-stroke-outer); stroke-width: var(--iso-stroke-width); }
.iso-face-right { fill: var(--iso-face-right); stroke: var(--iso-stroke-outer); stroke-width: var(--iso-stroke-width); }
.iso-shadow { fill: var(--iso-shadow-cast); }

.iso-label {
  margin-top: 8px;
  text-align: center;
  font-family: var(--font-sans, system-ui);
}
.iso-label-title { display: block; font-size: 12px; font-weight: 600; color: #0f172a; }
.iso-label-stat { font-family: var(--font-mono, monospace); font-size: 11px; color: #64748b; }

@media (prefers-reduced-motion: reduce) {
  .iso-solid { transition: none; }
}
```

---

## ♿ Accessibility & Environmental Contrast

- **Non-Text Contrast (WCAG 2.2 SC 1.4.11):** All structural edges, component boundaries, and interactive outlines must maintain at least $3:1$ contrast against adjacent background surfaces.
- **Text Alternatives (WCAG 2.2 SC 1.1.1):** Complex architectural diagrams must include a comprehensive structured text alternative (HTML table or hierarchical description list) disclosing the node connections and data flows.
- **Focus Order & Visual Story (WCAG 2.2 SC 2.4.3):** Interactive nodes must be sequenced in DOM order according to logical data flow, not raw painter's-algorithm z-stacking order.
- **Touch Target Sizing (WCAG 2.2 SC 2.5.8):** Interactive isometric bounding hitboxes must measure at least $24\times24\text{px}$ (preferably $44\times44\text{px}$ for mobile interfaces).

---

## ✅ When to Use / ❌ When to Avoid

### When to Use
- Infrastructure, deployment, and cloud network architecture maps.
- System cutaways explaining data flows, caching layers, and security barriers.
- Onboarding feature heroes where physical machinery serves as an intuitive metaphor for digital services.
- 2.5D game viewports and tactical battlemaps.

### When to Avoid
- Quantitative data charts and comparative bar graphs (foreshortening distorts heights and values).
- High-density data tables and small-screen primary navigation.
- Interfaces requiring dynamic, omnidirectional 3D camera rotation (use WebGL instead).

---

## 📚 Authoritative Sources & Historical Artifacts

- Farish, William. *On Isometrical Perspective*. Transactions of the Cambridge Philosophical Society, Vol. 1, 1820.
- Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F. *Computer Graphics: Principles and Practice*. Addison-Wesley, 1990 (Axonometric Projections and Painter's Algorithm).
- Fritsch, F. N., & Carlson, R. E. *Monotone Piecewise Cubic Interpolation*. SIAM Journal on Numerical Analysis, 1980 (Hermite Lathe Shading).
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. W3C Recommendation, 2023.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **[Isometric Mechanical Craft](references/isometric-mechanical-craft.md):** In-depth authoring guide for solids of revolution, cutaway chambers, and depth sorting.
- **[ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md):** For true real-time 3D camera control, lighting shaders, and WebGPU/WebGL scenes.
- **[ui-style-pixel-art](../ui-style-pixel-art/SKILL.md):** For 2:1 dimetric pixel art sprites and indexed color constraints.
- **[ui-gpu-graphics-web](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md):** For GPU-accelerated 2D/3D canvas rendering and SVG/WebGL hybrid layering.
- **[web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md):** For complete WCAG 2.2 verification methodology.
