---
name: "ui-style-bauhaus"
description: "Provides the Bauhaus UI style (1919-1933 lineage, revived for the web): form follows function, circle-square-triangle geometry, primary color with black, geometric sans typography and functional asymmetric layout, covering the school's timeline, tokens, grid and type rules, and how it differs from De Stijl and Swiss style. Use when designing geometric, educational, cultural or design-led brands that want modernist clarity with warmth."
---

# UI Style: Bauhaus

> *"Architects, sculptors, painters—we all must return to the crafts! For there is no such thing as 'professional art'. The artist is an exalted craftsman."*  
> — Walter Gropius, *Bauhaus Manifesto* (Weimar, April 1919)

Originating at the Staatliches Bauhaus in Germany (1919–1933), Bauhaus synthesizes fine art, craft, and industrial production under the radical principle that **form follows function**. Rejecting ornamental bourgeois excess, Bauhaus constructs visual language from pure geometric primitives—the circle, the square, and the equilateral triangle—anchored by primary pigment colors, dynamic asymmetric balance, heavy structural rules, and functional geometric typography.

---

## 🧭 When to Activate

- Designing cultural institutions, architecture and industrial design studios, modern art foundations, and forward-looking educational platforms.
- Building posters, product landing pages, and editorial layouts that celebrate primary geometry and expressive asymmetry.
- Transforming cluttered layouts into bold, elemental compositions governed by functional hierarchy and mathematical purity.
- Articulating a distinct European modernist identity that bridges artisanal craft with industrial reproducibility.

---

## 🕰️ Definition, Lineage, and Timeline

- **1919–1925 (Weimar Phase — Craft & Expressionism):** Walter Gropius founds the school in Weimar, uniting fine art with workshop craft. Johannes Itten establishes the *Vorkurs* (preliminary course), exploring color theory and elementary forms.
- **1925–1932 (Dessau Phase — High Industrial Constructivism):** The school moves to the iconic Gropius-designed Dessau campus. Herbert Bayer leads the printing and advertising workshop, designing the radical single-case *"Universal"* typeface (1925). László Moholy-Nagy champions the *Typofoto* (dynamic integration of typography and photography).
- **1932–1933 (Berlin Phase & Dissolution):** Mies van der Rohe directs the school through intense political pressure until forced closure by the Nazi regime in April 1933. Emigrating faculty disseminate Bauhaus ideals globally ("The New Bauhaus" in Chicago, Black Mountain College, and Harvard GSD).

### Absolute Style Vetos (What Bauhaus is NOT)
- ❌ **NOT De Stijl Purity ([ui-style-de-stijl](../ui-style-de-stijl/SKILL.md)):** De Stijl strictly forbids diagonal lines, circles, and curves, admitting only 90-degree orthogonal black lines and primary rectangles. Bauhaus actively celebrates circles, 45-degree diagonals, triangles, and photomontage.
- ❌ **NOT Postwar Swiss Minimalism ([ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md)):** Swiss style is austere, objective, and neutral (black/white with minimal red, rigid grid). Bauhaus is expressive, painterly, and playfully geometric.
- ❌ **NOT Playful Neo-Brutalism ([ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md)):** Bauhaus is mathematically disciplined and functional, never ironic, intentionally ugly, or decorated with cartoon stickers.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                 BAUHAUS TAXONOMY                                   |
+------------------------------------------------------------------------------------+
| Weimar Experimental Craft (1919-1925) | Dessau Industrial Typography (1925-1932)   |
| - Textured warm oatmeal paper base    | - Crisp white/cream functional backgrounds |
| - Expressive primary color contrasts  | - Heavy geometric sans in lowercase (Bayer)|
| - Elementary shapes (circle/triangle) | - High-contrast photographic cutouts       |
| - Diagonal asymmetric kinetic balance | - Structural black rules and grid anchors  |
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **The Elementary Geometric Trinity:**
   - **Circle:** Dynamic, rotating, focal point; traditionally associated with Blue or Red.
   - **Square:** Grounded, stable, foundational container; traditionally associated with Red or Black.
   - **Triangle:** Directional, active, kinetic wedge; traditionally associated with Yellow.
2. **Primary Triad Palette:** Pure unmixed pigments: Bauhaus Vermilion (`#D7261E`), Bauhaus Cadmium Yellow (`#F7B500`), and Bauhaus Cobalt Blue (`#17489E`), anchored by Carbon Ink (`#111111`) on warm Unbleached Paper (`#F4EEDB`).
3. **Asymmetric Kinetic Equilibrium:** Centered symmetrical layouts are rejected. Visual balance is achieved by counterbalancing a heavy black typography block on the left with a vivid yellow triangle and blue circle on the right.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Bauhaus exists strictly on the graphic printing plane:
- **Surface Rendering:** 100% matte, flat pigment fills. Zero gradients, zero ambient occlusion, zero glassy specular glare.
- **Elevation Model:** Expressed through physical paper layering and overlapping geometric collages (`z-index: 1 -> 2 -> 3`), rather than blurred drop shadows.
- **Borders & Dividers:** Bold, solid black rules (`2px` to `4px solid #111111`) that serve as structural girders anchoring typography to the page.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Canvas & Paper Surfaces */
  --bauhaus-bg-paper: #F4EEDB;        /* Warm Unbleached Parchment */
  --bauhaus-bg-surface: #EAE3CF;      /* Stepped Neutral Layer */
  --bauhaus-ink: #121212;             /* Deep Carbon Ink */

  /* The Pure Primary Triad */
  --bauhaus-red: #D7261E;             /* Weimar Vermilion */
  --bauhaus-yellow: #F7B500;          /* Cadmium Primary Yellow */
  --bauhaus-blue: #17489E;            /* Cobalt Ultramarine */

  /* Neutral Supports */
  --bauhaus-white: #FFFFFF;
  --bauhaus-muted: #666052;

  /* Structural Structural Lines */
  --bauhaus-rule-thin: 1px solid var(--bauhaus-ink);
  --bauhaus-rule-thick: 3px solid var(--bauhaus-ink);
  --bauhaus-rule-heavy: 6px solid var(--bauhaus-ink);

  /* Geometry & Corners */
  --bauhaus-radius-none: 0px;
  --bauhaus-radius-circle: 50%;

  /* Motion & Mechanical Physics */
  --bauhaus-ease: cubic-bezier(0.2, 0.0, 0.2, 1.0);
  --bauhaus-duration: 220ms;
}

[data-theme="dark"] {
  /* Historical Inversion (Dessau Night Exhibition) */
  --bauhaus-bg-paper: #121212;
  --bauhaus-bg-surface: #1E1E1E;
  --bauhaus-ink: #F4EEDB;
  --bauhaus-white: #FFFFFF;
  --bauhaus-muted: #888070;
  --bauhaus-rule-thick: 3px solid #F4EEDB;
}
```

---

## 🔤 Typography & Lettering Architecture

Typography reflects the geometric revolution led by Herbert Bayer and Jan Tschichold:
- **Font Stack:** `"Futura"`, `"Jost"`, `"Josefin Sans"`, or `"Inter"`.
- **Display & Section Titles:** `800` or `900` weight (Heavy/Black), geometric sans, tight tracking (`-0.03em`), frequently set in **all-lowercase** (`text-transform: lowercase`) in homage to Bayer's Universal Alphabet.
- **Body Text:** `400` or `500` weight, `15px` to `17px`, line-height `1.5`, flush-left ragged-right.
- **Rotated Margin Annotations:** Vertical text set along layout edges (`writing-mode: vertical-rl; transform: rotate(180deg)`), uppercase, `letter-spacing: 0.15em`.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Mechanical Step Animation:** Transitions operate like industrial machinery: precise 90-degree rotations, orthogonal slides, and instant color swaps.
- **Primary Color Swap on Hover:** Hovering a neutral button instantaneously fills its background with Bauhaus Red (`#D7261E`) and inverts text to white in `120ms`.
- **Acoustic Profile:** Heavy, solid mechanical click: a crisp 15ms typewriter-bar strike (`440Hz` clack) upon trigger execution.

---

## 🧩 Canonical Component Specifications

### 1. Asymmetric Geometric Hero Section

```html
<section class="bauhaus-hero">
  <div class="bauhaus-shape-composition" aria-hidden="true">
    <div class="bauhaus-shape shape-circle"></div>
    <div class="bauhaus-shape shape-triangle"></div>
    <div class="bauhaus-shape shape-square"></div>
  </div>
  <div class="bauhaus-hero-text">
    <span class="bauhaus-eyebrow">staatliches bauhaus dessau</span>
    <h1 class="bauhaus-title">kunst und technik —<br>eine neue einheit</h1>
    <p class="bauhaus-lead">form follows function. we reject the historicist ornamentation of the 19th century in favor of industrial clarity and mathematical harmony.</p>
    <div class="bauhaus-actions">
      <a href="#workshops" class="bauhaus-btn">view workshops</a>
      <span class="bauhaus-badge">1919–1933</span>
    </div>
  </div>
</section>
```

```css
.bauhaus-hero {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;
  padding: 60px 40px;
  background-color: var(--bauhaus-bg-paper);
  color: var(--bauhaus-ink);
  border-bottom: var(--bauhaus-rule-heavy);
  position: relative;
  align-items: center;
}

.bauhaus-shape-composition {
  position: relative;
  width: 240px;
  height: 240px;
}

.shape-circle {
  width: 140px;
  height: 140px;
  border-radius: var(--bauhaus-radius-circle);
  background-color: var(--bauhaus-blue);
  position: absolute;
  top: 0;
  left: 20px;
  z-index: 2;
}

.shape-triangle {
  width: 140px;
  height: 140px;
  background-color: var(--bauhaus-yellow);
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  position: absolute;
  bottom: 0;
  right: 10px;
  z-index: 1;
}

.shape-square {
  width: 90px;
  height: 90px;
  background-color: var(--bauhaus-red);
  position: absolute;
  bottom: 20px;
  left: 0;
  z-index: 3;
}

.bauhaus-eyebrow {
  font-family: "Jost", "Futura", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--bauhaus-red);
  display: block;
  margin-bottom: 8px;
}

.bauhaus-title {
  font-family: "Jost", "Futura", sans-serif;
  font-size: 42px;
  font-weight: 800;
  text-transform: lowercase;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin: 0 0 16px 0;
}

.bauhaus-lead {
  font-size: 16px;
  line-height: 1.5;
  color: var(--bauhaus-ink);
  max-width: 560px;
  margin: 0 0 24px 0;
}

.bauhaus-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.bauhaus-btn {
  background-color: var(--bauhaus-ink);
  color: var(--bauhaus-bg-paper);
  font-family: "Jost", "Futura", sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: lowercase;
  padding: 10px 22px;
  text-decoration: none;
  border-radius: var(--bauhaus-radius-none);
  transition: background-color var(--bauhaus-duration) var(--bauhaus-ease);
}

.bauhaus-btn:hover {
  background-color: var(--bauhaus-red);
}

.bauhaus-badge {
  font-family: monospace;
  font-size: 11px;
  font-weight: 700;
  border: var(--bauhaus-rule-thin);
  padding: 4px 8px;
}
```

### 2. Primary Color-Coded Modular Workshop Card

```html
<article class="bauhaus-card card-blue">
  <div class="bauhaus-card-stripe"></div>
  <div class="bauhaus-card-body">
    <div class="bauhaus-card-num">02</div>
    <h3 class="bauhaus-card-title">metal workshop</h3>
    <p class="bauhaus-card-desc">prototyping tubular steel furniture, lighting fixtures, and tea infusers with Marianne Brandt and Marcel Breuer.</p>
  </div>
</article>
```

```css
.bauhaus-card {
  background-color: var(--bauhaus-white);
  border: var(--bauhaus-rule-thick);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.bauhaus-card-stripe {
  height: 8px;
  width: 100%;
}

.card-blue .bauhaus-card-stripe { background-color: var(--bauhaus-blue); }
.card-red .bauhaus-card-stripe { background-color: var(--bauhaus-red); }
.card-yellow .bauhaus-card-stripe { background-color: var(--bauhaus-yellow); }

.bauhaus-card-body {
  padding: 24px;
}

.bauhaus-card-num {
  font-family: "Jost", "Futura", sans-serif;
  font-size: 32px;
  font-weight: 800;
  color: var(--bauhaus-ink);
  line-height: 1;
  margin-bottom: 8px;
}

.bauhaus-card-title {
  font-family: "Jost", "Futura", sans-serif;
  font-size: 20px;
  font-weight: 800;
  text-transform: lowercase;
  margin: 0 0 10px 0;
  color: var(--bauhaus-ink);
}

.bauhaus-card-desc {
  font-size: 14px;
  line-height: 1.5;
  color: var(--bauhaus-muted);
  margin: 0;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Contrast Validation on Primary Yellow:** Pure yellow (`#F7B500`) on white or cream paper yields only **1.4:1** contrast and **FAILS** for text. Yellow is strictly reserved for *large graphical shapes, backgrounds with black text, or borders*. Text placed on a yellow background must be ink black (`#121212`), which yields **11.8:1** (WCAG AAA).
- **Red & Blue Contrast Math:**
  - Bauhaus Red (`#D7261E`) on warm paper (`#F4EEDB`) yields **4.6:1** (conforming to WCAG AA for normal text).
  - Bauhaus Blue (`#17489E`) on warm paper yields **8.4:1** (conforming to WCAG AAA).
- **Focus Rings:** Interactive elements must display a distinct focus outline: `outline: 3px solid var(--bauhaus-blue); outline-offset: 3px;`.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Architecture firms, design academies, cultural festivals, typography showcases.
- Modernist furniture stores, publishing houses, and craft-centered digital tools.
- Educational content where primary shapes and color grouping aid cognitive comprehension.

### Inappropriate Scenarios
- Conservative financial institutions and regulatory legal compliance portals.
- Dense enterprise data software where bright primary shapes distract operator concentration.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Gropius, Walter (1919):** *Programm des Staatlichen Bauhauses in Weimar (The Bauhaus Manifesto)*.
2. **Bayer, Herbert, Gropius, Walter & Gropius, Ise (1938):** *Bauhaus 1919–1928*, Museum of Modern Art, New York.
3. **Droste, Magdalena (2002):** *Bauhaus: 1919–1933*, Taschen / Bauhaus-Archiv.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct sibling to [ui-style-de-stijl](../ui-style-de-stijl/SKILL.md) and ancestor of [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md).
- Contrasts with [ui-style-art-nouveau](../ui-style-art-nouveau/SKILL.md) (which Bauhaus rejected as bourgeois ornament) and [ui-style-memphis](../ui-style-memphis/SKILL.md) (which later subverted Bauhaus functionalism with postmodern irony).
