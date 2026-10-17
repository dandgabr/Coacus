---
name: "ui-style-de-stijl"
description: "Provides the De Stijl / Neoplasticism UI style (1917-1931 lineage, revived for the web): orthogonal black grid lines, flat primary-color planes on white and asymmetric balance, covering Mondrian's neoplastic rules, the 1923 diagonal schism, grid-as-composition CSS, and differences from Bauhaus and Swiss style. Use when designing rigorous grid-based compositions, color-block layouts, portfolios or editorial pages that treat the layout itself as the artwork."
---

# UI Style: De Stijl (Neoplasticism)

> *"Art should not be concerned with reproduction of real objects, but with expressing only the absolutes of life. That is to say, it must express only vertical and horizontal lines and the primary colors."*  
> — Piet Mondrian, *Neoplasticism in Painting* (De Stijl, 1917)

De Stijl (The Style) and **Neoplasticism** (*Nieuwe Beelding*) represent the most unyielding, puritanical reduction in art history. Founded in the Netherlands in 1917 by Piet Mondrian, Theo van Doesburg, and Gerrit Rietveld, De Stijl strips visual reality down to its elemental cosmic grammar: thick continuous orthogonal black lines intersecting at 90-degree right angles, framing flat asymmetrical planes of the three primary colors (red, yellow, blue) and the three non-colors (white, gray, black). In digital design, the layout itself *is* the painting.

---

## 🧭 When to Activate

- Designing art gallery exhibitions, contemporary architecture portfolios, design studio showcases, and avant-garde editorial publications.
- Building asymmetrical color-block CSS Grid layouts where the thickness of the grid lines and spatial distribution form the primary visual identity.
- Creating interactive exhibits or educational retrospectives exploring Dutch modernism and pure geometric abstraction.
- Implementing minimal, high-contrast user interfaces with a hyper-disciplined token footprint.

---

## 🕰️ Definition, Lineage, and Timeline

- **October 1917 (The Foundation):** Theo van Doesburg and Piet Mondrian launch the journal *De Stijl* in Leiden, Netherlands, formulating Neoplasticism as an antidote to the chaotic devastation of World War I. Early members include Bart van der Leck, Vilmos Huszár, and architect J.J.P. Oud.
- **1918–1919 (Rietveld's Three-Dimensional Expansion):** Gerrit Rietveld joins the movement, crafting the canonical *Red and Blue Chair* (1917, lacquered with primary colors in 1919) and later the *Rietveld Schröder House* in Utrecht (1924, designated a UNESCO World Heritage site in 2000).
- **1923–1924 (The Diagonal Schism):** Van Doesburg publishes the *Elementarism* manifesto, introducing 45-degree diagonal lines to express dynamic energy. Mondrian considers diagonals a catastrophic betrayal of spiritual equilibrium and permanently resigns from the movement.
- **1931 (Dissolution & Legacy):** Following van Doesburg's death in 1931, the journal ceases publication, but De Stijl's orthogonal DNA permanently transforms International Style architecture, Bauhaus furniture design, and Yves Saint Laurent's landmark 1965 *Mondrian Collection*.

### Absolute Style Vetos (What De Stijl is NOT)
- ❌ **NOT Bauhaus Elementary Shapes ([ui-style-bauhaus](../ui-style-bauhaus/SKILL.md)):** De Stijl strictly forbids circles, curves, triangles, and expressive diagonal slashes. It admits *only* orthogonal rectangles and straight lines.
- ❌ **NOT Postmodern Memphis ([ui-style-memphis](../ui-style-memphis/SKILL.md)):** No squiggles, no pastel pinks, no terrazzo patterns, no irreverent geometric humor. De Stijl is spiritually austere, serious, and mathematically absolute.
- ❌ **NOT Postwar Swiss Style ([ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md)):** Swiss style subordinates the grid to textual legibility; in De Stijl, the colored spatial plane *is* the primary artwork, and text is nested inside white modular quadrants.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                 DE STIJL TAXONOMY                                  |
+------------------------------------------------------------------------------------+
| Neoplastic Orthodoxy (Mondrian 1917)  | Elementarist Architecture (Rietveld/Doesburg)|
| - Strict horizontal & vertical axes   | - Asymmetric 3D volumetric planes           |
| - Thick black bounding rules (6px-10px)| - Cantilevered structural dividers         |
| - Sparse, isolated primary color hits | - Constructed geometric typography          |
| - Dominant field of pure white/gray   | - High dynamic tension between unequal cells|
+------------------------------------------------------------------------------------+
```

### Visual Hallmarks
1. **The Thick Orthogonal Grid:** Thick black rules (`4px` to `12px`) divide the viewport into interlocking rectangles. Rules run edge-to-edge across the canvas.
2. **The Asymmetric Primary Hierarchy:** White and pale gray occupy 70–80% of the surface area. The primaries are deployed with calculated scarcity: a single massive yellow cell might balance two small red and blue anchor blocks.
3. **Purity of Color:**
   - **Mondrian Red:** `#C8102E` (Deep primary scarlet)
   - **Mondrian Yellow:** `#F7D117` (Vivid solar cadmium)
   - **Mondrian Blue:** `#0B3D91` (Ultramarine royal cobalt)
   - **Base Canvas:** Pure White (`#FFFFFF`) and Light Studio Gray (`#EFEFEF`) framed by Pitch Black (`#111111`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

De Stijl rejects all illusionistic physical depth:
- **Lighting Physics:** Zero real-world lighting. No directional illumination, no sun casting, no ambient occlusion.
- **Surface Elevation:** Completely flat (`box-shadow: none`). Spatial depth is conveyed exclusively through the optical weight and advance/recede properties of primary colors (red advances toward the eye, blue recedes into distance).
- **Corner Radii:** Pure right angles (`border-radius: 0px`).

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* De Stijl Canonical Palette */
  --destijl-white: #FFFFFF;
  --destijl-gray-light: #EFEFEF;
  --destijl-gray-mid: #CCCCCC;
  --destijl-black: #111111;

  /* Primary Triad */
  --destijl-red: #C8102E;
  --destijl-yellow: #F7D117;
  --destijl-blue: #0B3D91;

  /* Grid Line Thickness */
  --destijl-rule-hairline: 2px;
  --destijl-rule-medium: 6px;
  --destijl-rule-heavy: 10px;

  /* Typography Colors */
  --destijl-text-main: #111111;
  --destijl-text-on-blue: #FFFFFF;
  --destijl-text-on-red: #FFFFFF;
  --destijl-text-on-yellow: #111111;

  /* Transitions */
  --destijl-transition: all 160ms linear;
}

[data-theme="dark"] {
  /* Dark Studio Palette */
  --destijl-white: #1A1A1A;
  --destijl-gray-light: #242424;
  --destijl-gray-mid: #444444;
  --destijl-black: #F4F4F4;
  --destijl-text-main: #F4F4F4;
}
```

---

## 🔤 Typography & Lettering Architecture

Typography in De Stijl is constructed, unadorned, and integrated directly into rectangular blocks:
- **Font Stack:** Constructed geometric sans-serifs (`"Space Grotesk"`, `"Syne"`, `"Jost"`, or custom van Doesburg alphabet recreations).
- **Headlines:** `700` or `800` weight, uppercase, stark tracking (`0.08em`), anchored to the top-left or bottom-left of white cells.
- **Body Text:** `400` weight, `14px` to `15px`, line-height `1.4`, set with strict left alignment inside neutral white/gray cells. Text never spills over black grid rules.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Orthogonal Grid Track Animation:** Hovering a primary block triggers a linear redistribution of CSS grid tracks (`grid-template-columns: 2fr 5fr 3fr -> 3fr 4fr 3fr`), smoothly rebalancing the composition in `200ms`.
- **Instantaneous Inversion:** Clicking an interactive cell inverts its fill from white to primary blue or red in a crisp, non-eased transition.
- **Acoustic Feedback:** Crisp wooden block percussion: a dry 12ms marimba strike (`520Hz`) confirming quadrant selection.

---

## 🧩 Canonical Component Specifications

### 1. Neoplastic Grid Composition (Hero / Feature Showcase)

```html
<section class="destijl-composition" aria-label="Neoplastic Composition">
  <!-- Top Left: Red Primary Anchor -->
  <article class="destijl-cell cell-red">
    <span class="destijl-year">1917</span>
  </article>

  <!-- Top Center: Dominant White Canvas -->
  <article class="destijl-cell cell-white cell-lead">
    <h1 class="destijl-title">DE STIJL</h1>
    <p class="destijl-desc">Manifesto of pure neoplastic equilibrium. Vertical meets horizontal in eternal balance.</p>
  </article>

  <!-- Top Right: Light Gray Balance -->
  <article class="destijl-cell cell-gray">
    <div class="destijl-spec">VOL. I</div>
  </article>

  <!-- Bottom Left: White Navigation Block -->
  <article class="destijl-cell cell-white cell-nav">
    <nav class="destijl-links">
      <a href="#mondrian" class="destijl-link">Mondrian</a>
      <a href="#rietveld" class="destijl-link">Rietveld</a>
      <a href="#doesburg" class="destijl-link">Van Doesburg</a>
    </nav>
  </article>

  <!-- Bottom Center: Blue Accent Cell -->
  <article class="destijl-cell cell-blue">
    <span class="destijl-accent-tag">ULTRAMARINE</span>
  </article>

  <!-- Bottom Right: Yellow Primary Base -->
  <article class="destijl-cell cell-yellow">
    <button class="destijl-btn-trigger">EXPLORE ARCHIVE</button>
  </article>
</section>
```

```css
.destijl-composition {
  display: grid;
  grid-template-columns: 180px 1fr 140px;
  grid-template-rows: 240px 180px;
  gap: var(--destijl-rule-medium);
  background-color: var(--destijl-black);
  border: var(--destijl-rule-medium) solid var(--destijl-black);
  max-width: 1000px;
  margin: 0 auto;
}

.destijl-cell {
  padding: 24px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 0;
  transition: var(--destijl-transition);
}

.cell-white { background-color: var(--destijl-white); color: var(--destijl-text-main); }
.cell-gray { background-color: var(--destijl-gray-light); color: var(--destijl-text-main); }
.cell-red { background-color: var(--destijl-red); color: var(--destijl-text-on-red); }
.cell-blue { background-color: var(--destijl-blue); color: var(--destijl-text-on-blue); }
.cell-yellow { background-color: var(--destijl-yellow); color: var(--destijl-text-on-yellow); }

.destijl-title {
  font-family: "Space Grotesk", sans-serif;
  font-size: 48px;
  font-weight: 800;
  letter-spacing: 0.05em;
  line-height: 1;
  margin: 0 0 12px 0;
}

.destijl-desc {
  font-size: 15px;
  line-height: 1.45;
  margin: 0;
  max-width: 480px;
}

.destijl-year {
  font-family: monospace;
  font-size: 24px;
  font-weight: 700;
}

.destijl-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.destijl-link {
  color: var(--destijl-text-main);
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.destijl-link:hover {
  color: var(--destijl-red);
}

.destijl-btn-trigger {
  background-color: var(--destijl-black);
  color: var(--destijl-white);
  border: none;
  font-family: "Space Grotesk", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 10px 14px;
  cursor: pointer;
  width: 100%;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Strict Color Contrast Math:**
  - Ink text (`#111111`) over Mondrian Yellow (`#F7D117`) achieves **11.2:1** (WCAG AAA).
  - White text (`#FFFFFF`) over Mondrian Blue (`#0B3D91`) achieves **9.8:1** (WCAG AAA).
  - White text (`#FFFFFF`) over Mondrian Red (`#C8102E`) achieves **5.2:1** (WCAG AA).
  - **Absolute Rule:** Black text must NEVER be set on Blue or Red; White text must NEVER be set on Yellow.
- **Structural Legibility:** Text is never placed across grid line borders. Every block of text resides securely within a designated rectangular quadrant.
- **Focus Indicators:** Interactive triggers receive a solid 3px outline in high-contrast black or white with an offset of 2px.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Fine art museum digital archives, modernist architecture firms, furniture retrospectives.
- Experimental web design studios and typography showcases.
- High-concept landing pages where bold spatial compartmentalization serves as the primary visualhook.

### Inappropriate Scenarios
- High-density data tables and accounting software.
- Multi-step bureaucratic forms where rigid thick black borders create visual fatigue.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Mondrian, Piet (1917–1918):** *"De Nieuwe Beelding in de schilderkunst" (Neoplasticism in Painting)*, De Stijl, Vol. 1.
2. **Van Doesburg, Theo (1924):** *"Elementarism (The Manifesto of Dynamic Neoplasticism)"*, De Stijl, Vol. 6.
3. **Jaffé, Hans L.C. (1956):** *De Stijl 1917–1931: The Dutch Contribution to Modern Art*, J.M. Meulenhoff.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Orthodox sibling to [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md) and historical parent of [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md).
- Polar opposite to [ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md) and [ui-style-psychedelic-60s](../ui-style-psychedelic-60s/SKILL.md).
