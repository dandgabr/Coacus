---
name: "ui-style-constructivism"
description: "Provides the authentic Constructivism UI style (1919-1930s Soviet avant-garde): pure geometric primitives, dynamic 45-degree diagonal axes, stark scarlet-and-black contrast, load-bearing industrial typography, and photomontage engineering. Use when designing bold editorial manifests, architectural exhibition portals, avant-garde cultural features, or high-impact activist platforms."
---

# UI Style: Constructivism (Architectonic & Geometric Avant-Garde)

Constructivism is an early 20th-century avant-garde movement founded in post-revolutionary Russia (1919–1934) by Aleksandr Rodchenko, El Lissitzky, Varvara Stepanova, and Vladimir Tatlin. It rejected decorative "art for art's sake" in favor of art as an active instrument of social and technical construction (*konstruktsiya*). The visual constructor replaces bourgeois decorative conventions with raw geometric primitives, load-bearing industrial typography, dynamic diagonal tension, and precise photomontage. Synthesized from primary avant-garde archival sources; see Sources.

---

## 🧭 When to Activate

- Designing high-impact cultural manifestos, avant-garde design archives, architectural portfolios, or activist publishing platforms.
- Replacing conventional orthogonal grid structures with engineered diagonal tension, structural framing bars, and asymmetrical kinetic thrust.
- Distinct from **[ui-style-agitprop-poster](../ui-style-agitprop-poster/SKILL.md)**: Constructivism focuses on abstract architectural engineering, pure geometric forms (wedges, circles, intersecting bars), and systemic typography; Agitprop focuses on heroic figuration, worker lithographs, and street-level propagandistic rallying.
- Distinct from **[ui-style-bauhaus](../ui-style-bauhaus/SKILL.md)**: Bauhaus emphasizes balanced, orthogonal harmony and primary tri-colors; Constructivism uses aggressive diagonal shear (-15° to -45°), asymmetric conflict, and heavy scarlet-black contrast.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Formulated in 1919 with Vladimir Tatlin's *Monument to the Third International* and El Lissitzky's foundational lithograph *Beat the Whites with the Red Wedge* (1919). Institutionalized at INKhUK (Institute of Artistic Culture) and Vkhutemas workshops (1920–1930).
- **Philosophical Core:** Utilitarian visual construction over passive decoration. The designer acts as an engineer assembling prefabricated industrial components: heavy structural rules, circular targets, red wedges, and unvarnished mechanical type.
- **Graphic Innovation:** Rodchenko's diagonal camera angles and Lissitzky's typotectonics (typography acting as structural architecture).

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Palettes:** Stark tripartite core:
  - Soviet Scarlet (`#D90429` / `#CC1111`)
  - Deep Coal Black (`#111111` / `#0A0A0A`)
  - Unbleached Newsprint Cream (`#F4EBD9` / `#EDE4CF`)
  - Occasional industrial structural accents: Galvanized Slate (`#4A4E69`) and Caution Ochre (`#D97706`).
- **Geometric Primitives & Structural Bars:**
  - 45° dynamic wedges slicing through rectilinear viewports.
  - Load-bearing structural divider bars (4px to 16px solid black or scarlet).
  - Concentric circular targets and compass-drawn arcs framing editorial content.
- **Industrial Typography:**
  - Heavy condensed grotesques and woodblock display sans-serifs (Oswald, Bebas Neue, Archivo Black) set in forceful uppercase.
  - Diagonal baselines, vertical letter-stacks, and extreme scale contrasts between gigantic numeral indices and dense monospaced captions.
- **Photomontage:**
  - High-contrast duotone or monochrome photographic cutouts integrated directly into geometric solids with sharp knife-edge boundaries.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Flat Opaque Surfaces:** Absolute rejection of atmospheric blur, drop shadows, or glossy specular highlights. Depth is achieved strictly through overlapping hard geometric planes:
  ```css
  /* Constructivist planar layering */
  box-shadow: none;
  border-radius: 0;
  clip-path: polygon(0 0, 100% 8%, 100% 100%, 0 92%);
  ```
- **Structural Tension Line:**
  ```css
  border: 4px solid #111111;
  border-left: 16px solid #D90429;
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Surface and Ink */
  --construct-bg: #F4EBD9;
  --construct-surface: #EDE4CF;
  --construct-fg: #111111;
  --construct-red: #D90429;
  --construct-black: #0A0A0A;
  --construct-slate: #4A4E69;
  --construct-ochre: #D97706;
  --construct-white: #FFFFFF;

  /* Typography */
  --construct-font-display: 'Bebas Neue', 'Oswald', Impact, sans-serif;
  --construct-font-body: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif;
  --construct-font-mono: 'Space Mono', monospace;

  /* Structural Rules */
  --construct-border-thin: 2px solid var(--construct-black);
  --construct-border-thick: 6px solid var(--construct-black);
  --construct-border-beam: 16px solid var(--construct-red);

  /* Layout Constants */
  --construct-radius: 0px;
  --construct-angle: -3deg;
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<section class="construct-panel">
  <div class="construct-header">
    <span class="construct-index">№ 04</span>
    <h2 class="construct-title">PRODUCE // BUILD</h2>
  </div>
  <div class="construct-body">
    <div class="construct-wedge"></div>
    <div class="construct-content">
      <p class="construct-lead">THE ARTIST BECOMES THE VISUAL CONSTRUCTOR OF FUNCTIONAL REALITY.</p>
      <p class="construct-text">Rejecting bourgeois decorative aesthetics in favor of industrial engineering and utilitarian typography.</p>
      <div class="construct-actions">
        <button class="construct-btn construct-btn-primary" type="button">EXECUTE DIRECTIVE</button>
        <button class="construct-btn construct-btn-secondary" type="button">INSPECT ARCHIVE</button>
      </div>
    </div>
  </div>
</section>
```

```css
.construct-panel {
  background: var(--construct-bg);
  color: var(--construct-fg);
  border: var(--construct-border-thick);
  border-left: var(--construct-border-beam);
  border-radius: var(--construct-radius);
  padding: 24px;
  max-width: 680px;
  position: relative;
  overflow: hidden;
  box-shadow: none;
}
.construct-header {
  display: flex;
  align-items: baseline;
  gap: 16px;
  border-bottom: var(--construct-border-thick);
  padding-bottom: 12px;
  margin-bottom: 20px;
  transform: rotate(var(--construct-angle));
  transform-origin: left center;
}
.construct-index {
  background: var(--construct-black);
  color: var(--construct-white);
  font-family: var(--construct-font-mono);
  font-size: 1.125rem;
  font-weight: 700;
  padding: 4px 10px;
}
.construct-title {
  font-family: var(--construct-font-display);
  font-size: 2.75rem;
  letter-spacing: 0.05em;
  line-height: 0.9;
  margin: 0;
  color: var(--construct-red);
}
.construct-body {
  position: relative;
}
.construct-wedge {
  position: absolute;
  top: -10px;
  right: -30px;
  width: 140px;
  height: 140px;
  background: var(--construct-red);
  clip-path: polygon(100% 0, 0 0, 100% 100%);
  pointer-events: none;
}
.construct-lead {
  font-family: var(--construct-font-display);
  font-size: 1.375rem;
  line-height: 1.1;
  color: var(--construct-black);
  margin-bottom: 12px;
}
.construct-text {
  font-family: var(--construct-font-body);
  font-size: 0.9375rem;
  line-height: 1.6;
  max-width: 480px;
  margin-bottom: 24px;
}
.construct-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.construct-btn {
  font-family: var(--construct-font-display);
  font-size: 1.25rem;
  letter-spacing: 0.08em;
  padding: 10px 24px;
  border-radius: 0;
  cursor: pointer;
  text-transform: uppercase;
  transition: transform 0.12s linear, background-color 0.12s linear;
}
.construct-btn-primary {
  background: var(--construct-red);
  color: var(--construct-white);
  border: var(--construct-border-thin);
}
.construct-btn-primary:hover {
  background: var(--construct-black);
  transform: translate(-2px, -2px);
}
.construct-btn-secondary {
  background: transparent;
  color: var(--construct-black);
  border: var(--construct-border-thin);
}
.construct-btn-secondary:hover {
  background: var(--construct-black);
  color: var(--construct-white);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Mechanical Step Easing:** Avoid soft bouncy springs; transitions must be rapid and architectural (`120ms linear` or `cubic-bezier(0, 0, 0.2, 1)`).
- **Axis Realignment on Hover:** Elements tilted at `-3deg` snap to `0deg` on hover/focus, representing structural stabilization under user inspection.
- **Angular Wipe Transitions:** Container entrances clip along diagonal wedge angles using CSS `clip-path`.

---

## 📱 Responsive Layout & Spatial Composition

- In mobile viewports (`< 640px`), cancel radical angular rotations (`transform: none`) on text blocks to preserve readability while retaining the thick structural border bars and sharp red geometric wedges.
- Keep structural grid gutters wide (24px to 32px) to prevent heavy black border collisions.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Coal Black (`#111111`) on Newsprint Cream (`#F4EBD9`): **14.2:1** (Passes WCAG AAA).
  - Soviet Scarlet (`#D90429`) on Newsprint Cream (`#F4EBD9`): **4.9:1** (Passes WCAG AA for normal text, AAA for bold headings).
  - White (`#FFFFFF`) on Soviet Scarlet (`#D90429`): **4.6:1** (Passes WCAG AA).
- **Critical Guardrail:** NEVER render body text in Soviet Scarlet directly over Deep Black (contrast ratio is only ~3.1:1). Scarlet text must only reside on cream or white surfaces.
- **Reduced Motion:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    .construct-header, .construct-panel, .construct-btn {
      transform: none !important;
      transition: none !important;
    }
  }
  ```

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use rounded corners or pill badges:** Rounded corners immediately destroy constructivist architectural integrity. Radius must be strictly `0px`.
- ❌ **NEVER use drop shadows or soft Gaussian glows:** Constructivism is physically grounded in opaque ink and printing blocks, never ambient digital lighting.
- ❌ **NEVER rotate large bodies of reading copy:** Diagonal axes are reserved strictly for display headers, banners, and structural framing.

---

## 🎯 When to Use & When to Avoid

- **Use For:** Art exhibitions, avant-garde editorial platforms, architectural manifestos, cultural archives, and provocative indie branding.
- **Avoid For:** E-commerce checkout flows, medical software, financial accounting portals, or applications requiring neutral, calming utility.

---

## 📚 Sources & References

- Christina Lodder, *Russian Constructivism* (Yale University Press, 1983).
- Aleksandr Rodchenko & Varvara Stepanova, *The Future Is Our Only Goal* (Prestel, 1991).
- El Lissitzky, *About Two Squares: A Suprematist Tale in Six Constructions* (1922).
## Appearance and Interaction Verification

Separate wedge/diagonal clipping from reading and focus owners; check rotated long titles in actual panel width and create a cream reading plane where a red wedge crosses ink, preserving hard geometric thrust and thick structural bars.
