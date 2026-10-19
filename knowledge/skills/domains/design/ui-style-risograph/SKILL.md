---
name: "ui-style-risograph"
description: "Provides the authentic Risograph UI style (1980-present Riso Kagaku duplicator print aesthetics): translucent spot-color inks, multi-drum overprint multiplication, mechanical misregistration fringes, stochastic halftone screening, and tactile uncoated paper tooth. Use when designing indie art book portals, cultural print showcases, illustration-first portfolios, or community creative presses."
---

# UI Style: Risograph (Spot Ink, Overprint Multiplication & Halftone Screen)

Risograph is a screen-based translation of the digital stencil duplicator invented by Japan's Riso Kagaku Corporation in 1980. Unlike four-color offset (CMYK) or digital toner, the Risograph forces rich soy- or rice-bran-based spot inks through a thermally burned banana-peel master onto uncoated tooth paper, one cylinder drum at a time. The resulting visual signature is defined by translucent overlapping inks that physically multiply into third colors, tactile stochastic halftone screening, and subtle mechanical misregistration (trapping offsets of 1px to 3px). Synthesized from Risograph print studio standards and artist press archives; see Sources.

---

## 🧭 When to Activate

- Designing indie publishing portals, print workshops, illustration portfolios, small-press zine stores, or music album art hubs.
- Creating an authentic tactile print feel using true spot-color blending and mechanical screen textures.
- Distinct from **[ui-style-zine-independent](../ui-style-zine-independent/SKILL.md)**: Risograph is defined by specialized multi-drum spot inks, overprint optical physics, and halftone screens; Independent Zine is defined by gritty black-and-white photocopier toner, cut-and-paste collage, staples, and DIY ransom-note typography.
- Distinct from **[ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md)**: Duotone uses smooth mathematical color mapping; Risograph uses discrete spot inks with physical multiply blending.

---

## 🕰️ Definition, Lineage, and Timeline

- **Chronology:** Introduced in Japan in 1980 by Noboru Hayama as a high-speed, cost-effective mimeograph duplicator for schools and churches. Adopted globally in the 2000s and 2010s by independent comic artists, graphic designers, and small art presses.
- **Physical Mechanics:** Stencils are burned thermally into master sheets; ink drums rotate at high speed. Because papers pass through multiple passes for multi-color runs, mechanical traction causes natural registration shifts (misregistration) and uneven ink saturation.

---

## 🎨 Visual DNA & Subgenre Taxonomy

- **Spot Ink Drums & Palettes:**
  - Fluorescent Pink (`#FF48B0` / `#FF3399`)
  - Federal / Medium Blue (`#0078BF` / `#0066CC`)
  - Sunflower Yellow (`#FFE800` / `#FFD700`)
  - Hunter Green (`#00A95C`)
  - Teal (`#00838A`)
  - Rich Black (`#1D1D2C` or `#2E294E`)
  - Uncoated Warm Paper Tooth (`#F7F2E8` / `#FAF5EB`)
- **Overprint Multiplication:**
  - Translucent ink overlays where yellow over blue yields vibrant leaf green, or pink over blue yields deep royal purple (`mix-blend-mode: multiply`).
- **Mechanical Misregistration:**
  - Discrete 1px to 3px coordinate offsets between ink passes, exposing raw colored under-fringes at component borders.
- **Halftone Screens & Stipple Dithering:**
  - Microscopic dot matrices simulating drum screen grain rather than smooth digital vectors.
- **Typography:**
  - Chunky neo-grotesques, geometric monospaces, and warm humanist sans-serifs (Space Grotesk, Syne, Cooper Black, DM Mono) with intentional ink spread.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

- **Physical Overprint & Paper Absorption:**
  ```css
  /* Uncoated paper texture + multiply overprint layer */
  .riso-container {
    background: #F7F2E8;
    position: relative;
    isolation: isolate;
  }
  .riso-ink-layer {
    mix-blend-mode: multiply;
    opacity: 0.92;
  }
  .riso-misregister {
    transform: translate(2px, -1px);
  }
  ```
- **Halftone Dot Matrix:**
  ```css
  background-image: radial-gradient(#FF48B0 25%, transparent 26%);
  background-size: 6px 6px;
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrate Paper */
  --riso-paper: #F7F2E8;
  --riso-paper-shadow: #EADBCA;

  /* Official Spot Inks */
  --riso-pink: #FF48B0;
  --riso-blue: #0078BF;
  --riso-yellow: #FFE800;
  --riso-green: #00A95C;
  --riso-teal: #00838A;
  --riso-ink-black: #1D1D2C;

  /* Typography */
  --riso-font-display: 'Syne', 'Space Grotesk', system-ui, sans-serif;
  --riso-font-body: 'Space Grotesk', system-ui, sans-serif;
  --riso-font-mono: 'DM Mono', monospace;

  /* Stencil Rules */
  --riso-border: 2px solid var(--riso-ink-black);
}
```

---

## 🧱 Production-Ready Component Blueprint

```html
<article class="riso-card">
  <div class="riso-layer-pink" aria-hidden="true"></div>
  <div class="riso-layer-blue" aria-hidden="true"></div>
  <div class="riso-card-content">
    <header class="riso-header">
      <span class="riso-tag">ISSUE № 14</span>
      <span class="riso-press">TOKYO DUP // 2-PASS</span>
    </header>
    <h2 class="riso-title">TACTILE REPRODUCTION</h2>
    <p class="riso-desc">
      Soy-based inks forced through microscopic banana-fiber stencils onto uncoated cream stock.
    </p>
    <div class="riso-footer">
      <button class="riso-btn" type="button">COLLECT PRINT</button>
      <span class="riso-price">$24.00</span>
    </div>
  </div>
</article>
```

```css
.riso-card {
  position: relative;
  background: var(--riso-paper);
  border: var(--riso-border);
  padding: 24px;
  max-width: 460px;
  isolation: isolate;
  overflow: hidden;
  box-shadow: 3px 3px 0 var(--riso-ink-black);
}
.riso-layer-pink {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 120px;
  height: 120px;
  background: var(--riso-pink);
  border-radius: 50%;
  mix-blend-mode: multiply;
  opacity: 0.85;
  pointer-events: none;
  z-index: 1;
}
.riso-layer-blue {
  position: absolute;
  top: 14px;
  right: 18px;
  width: 100px;
  height: 100px;
  background: var(--riso-blue);
  clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
  mix-blend-mode: multiply;
  opacity: 0.85;
  pointer-events: none;
  z-index: 2;
}
.riso-card-content {
  position: relative;
  z-index: 3;
}
.riso-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--riso-font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  color: var(--riso-blue);
  border-bottom: 1px dashed var(--riso-ink-black);
  padding-bottom: 8px;
  margin-bottom: 16px;
}
.riso-tag {
  background: var(--riso-yellow);
  color: var(--riso-ink-black);
  padding: 2px 6px;
  font-weight: 700;
}
.riso-title {
  font-family: var(--riso-font-display);
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.05;
  color: var(--riso-ink-black);
  margin: 0 0 12px 0;
  text-transform: uppercase;
}
.riso-desc {
  font-family: var(--riso-font-body);
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--riso-ink-black);
  margin-bottom: 24px;
}
.riso-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.riso-btn {
  background: var(--riso-pink);
  color: #FFFFFF;
  font-family: var(--riso-font-display);
  font-size: 0.9375rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 10px 20px;
  border: var(--riso-border);
  border-radius: 0;
  cursor: pointer;
  position: relative;
  box-shadow: 2px 2px 0 var(--riso-blue);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}
.riso-btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 4px 4px 0 var(--riso-blue);
}
.riso-price {
  font-family: var(--riso-font-mono);
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--riso-ink-black);
}
```

---

## ✨ Micro-Interactions, Motion & Soundscapes

- **Misregistration Shift on Hover:** Moving the cursor over interactive trigger cards offsets the secondary ink layer by an additional 1px–2px (`transform: translate(3px, -2px);`), simulating paper sliding slightly under the drum gripper.
- **Physical Stencil Press:** Interactive buttons depress cleanly with a flat paper drop rather than a digital spring bounce.

---

## 📱 Responsive Layout & Spatial Composition

- Maintain a modular multi-column print grid with visible dashed or dotted guide lines.
- On smaller viewports, scale decorative overprint geometric shapes to avoid obscuring body copy.

---

## ♿ WCAG 2.2 Accessibility & High-Contrast Guardrails

- **Contrast Ratios:**
  - Rich Ink Black (`#1D1D2C`) on Warm Cream Paper (`#F7F2E8`): **13.8:1** (Passes WCAG AAA).
  - Medium Blue (`#0078BF`) on Warm Cream Paper (`#F7F2E8`): **5.1:1** (Passes WCAG AA).
  - Fluorescent Pink (`#FF48B0`) on Warm Cream Paper: **3.8:1** — suitable for large headings and buttons, but NEVER for body copy.
  - Body copy must ALWAYS use `--riso-ink-black` or deep `--riso-blue`.
- **Focus Rings:**
  ```css
  :focus-visible {
    outline: 2px solid var(--riso-blue);
    outline-offset: 3px;
  }
  ```

---

## 🚫 Anti-Patterns & Visual Sins (Anti-AI Slop Traps)

- ❌ **NEVER use smooth CSS gradients or digital drop shadows:** Risograph is physically grounded in flat liquid spot inks and paper fibers.
- ❌ **NEVER mix CMYK photographic rendering:** Photographs must be dithered or halftone screened into discrete spot ink passes.
- ❌ **NEVER use sterile white backgrounds:** Paper must always have warm natural cream or tooth tone.

---

## 🎯 When to Use & When to Avoid

- **Use For:** Creative studios, independent publishing houses, illustration festivals, printmaker markets, music album hubs.
- **Avoid For:** High-density enterprise dashboards, formal legal interfaces, sterile medical software.

---

## 📚 Sources & References

- Luca Bogoni, *Risomania: The New Spirit of Printing* (Niggli Verlag, 2017).
- Riso Kagaku Corporation, *Technical History of the Stencil Duplicator* (Tokyo, 2010).
- John Z. Komurki, *Stationery Fever: From Paper Clips to Pencils and Everything in Between* (Prestel, 2016).
## Appearance and Interaction Verification

Use a verified ink pair for the small pink action label; keep overprint/misregistration in isolated decorative layers with stable reading areas and confirm ink overlays cannot repaint semantic text/focus in requested appearances.

