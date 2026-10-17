---
name: "ui-style-broken-grid"
description: "Provides the canonical Broken Grid & Controlled Asymmetry UI style (1980s print lineage, web 2010s-present): deliberate disruption of an underlying 12-column grid through intentional overlap, offset layering, scale contrasts, and bleed margins. Covers CSS Grid line-based overlapping techniques, DOM reading-order safety, responsive reflow collapsing, and WCAG 2.2 accessibility. Use when designing high-fashion editorial layouts, creative agency portfolios, or architectural monographs."
---

# UI Style: Broken Grid & Controlled Asymmetry

**Broken Grid** (also known as **Controlled Asymmetry**) is an architectural layout methodology that establishes a rigorous underlying structural grid (typically 12 or 16 columns) and then deliberately and systematically violates it in controlled focal locations. By allowing oversized display headlines to bleed across column boundaries, tucking captions under overlapping imagery, and offsetting containers across grid rows, Broken Grid introduces kinetic tension, depth, and editorial movement while preserving mathematical structural integrity.

---

## 🧭 When to Activate

- High-end creative agency portfolios, architecture firms, and independent design studio showcases.
- Editorial magazines, cultural essays, luxury fashion campaigns, and artistic monographs where standard uniform card grids feel generic and predictable.
- Translating sophisticated print publication spreads into responsive, accessible web layouts.

---

## 🕰️ Definition, Lineage, and Timeline

- **Historical Foundations:** Emerged as a postmodern reaction against post-war Swiss / International Typographic Style (Josef Müller-Brockmann's *Grid Systems in Graphic Design*, 1981). Pioneered in print by David Carson (*Ray Gun* magazine, 1992–1995) and Wolfgang Weingart's New Wave typography.
- **The Modern Web Evolution (2017–Present):** Prior to native CSS Grid, web layouts relied on fragile negative margins and absolute positioning hacks. The W3C CSS Grid Level 1 specification (shipping across major browsers in 2017) enabled line-based placement (`grid-column: 3 / span 6; grid-row: 1 / span 2;`), making deliberate overlapping layouts robust, maintainable, and responsive.
- **Distinctions from Neighboring Styles:**
  - Unlike **Swiss Web Minimalism** (which strictly obeys the grid with neutral alignment), Broken Grid deliberately breaks the grid to create dynamic visual friction.
  - Unlike **Web Brutalism** (raw, unstyled, crude), Broken Grid is elegant, editorial, refined, and typographically surgical.
  - Unlike **Collage / Scrapbook** (hand-cut scissors, tape, irregular paper scraps), Broken Grid maintains straight, razor-sharp geometric alignment lines.
- **Absolute Veto:** Breaking the grid randomly everywhere without establishing the underlying structure first. A broken grid only works when 70% of the page adheres to an orderly baseline; if 100% of elements are offset, it collapses into unreadable chaos.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 BROKEN GRID MATRIX                                     │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Editorial Magazine      │ 2. Architectural Bleed     │ 3. Layered Portfolio Spread  │
│ • Headline overlaps image  │ • Container bleeds past rim│ • Off-axis thumbnail cards   │
│ • Caption tucked in margin │ • Hairline coordinate axes │ • Staggered vertical rhythm  │
│ • Deep scale contrast      │ • Generous negative space  │ • High-contrast serifs       │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Restraint:** Minimalist and high-contrast—crisp linen white (`#FBFBF9`), ink black (`#111111`), architectural slate (`#4A4A4A`), with a single vibrant editorial accent (e.g. vermilion `#E63946` or cobalt `#1D4ED8`).
- **Scale Contrast:** Extreme contrast between massive display type (clamp 4rem to 10rem) and delicate 12px monospaced captions.
- **Controlled Layering:** Images spanning columns 5 to 12 overlapping headlines anchored to columns 2 to 8, with intentional z-index planes.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **CSS Grid Line-Based Overlap:**
   - Elements occupying identical grid coordinates create spatial layering without breaking document flow.
   ```css
   .grid-stage {
     display: grid;
     grid-template-columns: repeat(12, 1fr);
     column-gap: 1.5rem;
     row-gap: 2rem;
   }
   .grid-title {
     grid-column: 2 / span 7;
     grid-row: 1;
     z-index: 2;
     font-size: clamp(3rem, 7vw, 7rem);
   }
   .grid-hero-img {
     grid-column: 6 / 13;
     grid-row: 1 / span 2;
     z-index: 1;
   }
   ```
2. **Controlled Negative Margin Offset:**
   - Pushing small caption cards 2rem upward into the image frame while retaining document accessibility.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Substrates & Ink */
  --bg-grid-linen: #FBFBF9;
  --bg-grid-surface: #FFFFFF;
  --ink-grid-primary: #111111;
  --ink-grid-secondary: #555555;
  --accent-grid-red: #E63946;

  /* Grid Metrics */
  --grid-columns: 12;
  --grid-gap: 1.5rem;
  --grid-max-width: 1440px;

  /* Typography */
  --font-grid-display: 'Ogg', 'Playfair Display', 'Cinzel', serif;
  --font-grid-sans: 'Inter', system-ui, sans-serif;
  --font-grid-mono: 'Space Mono', 'JetBrains Mono', monospace;

  /* Borders & Radius */
  --grid-border: 1px solid rgba(17, 17, 17, 0.15);
  --grid-radius: 0px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Expressive editorial serifs (*Playfair Display*, *Ogg*, *Baskerville*) or high-contrast modern grotesques (*Clash Display*, *Syne*) scaled massively to bleed across columns.
- **Body Text:** Neutral, highly readable grotesque (*Inter*, *Neue Haas Grotesk*) set in restrained, narrow column widths (columns 2 to 6, or 8 to 12) with 1.65 line-height.
- **Annotations & Footnotes:** Small monospaced callouts (*Space Mono*) tucked into the margin gutters with leader rules.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Staggered Parallax Layering:** As the user scrolls, overlapping text and image planes translate vertically at differential speeds (e.g. image at 0.1x, title at 0.04x).
- **Z-Index Layer Elevation on Hover:** Hovering an overlapping text card brings it to the forefront of the z-stack (`z-index: 10`).
- **Smooth Image Scale on Pointer Focus:** Hero photographs scale gently (`transform: scale(1.02); transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)`).
- **Motion Gating:** When `prefers-reduced-motion: reduce` is enabled, all differential scroll parallax and zoom transitions are disabled.

---

## 🧩 Canonical Component Specifications

### 1. Overlapping Editorial Hero (`.bg-hero`)
A multi-layered layout where a massive serif headline overlaps a full-bleed architectural image.
```html
<section class="bg-hero">
  <h1 class="bg-hero-title">Structural Tensions</h1>
  <div class="bg-hero-media">
    <img src="architectural-facade.jpg" alt="Brutalist concrete cantilever" />
    <span class="bg-hero-caption">FIGURE 01 // ROTTERDAM 1968</span>
  </div>
  <div class="bg-hero-body">
    <p>Exploring the boundary where mathematical grid discipline yields to deliberate compositional asymmetry.</p>
  </div>
</section>
```
```css
.bg-hero {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  column-gap: 1.5rem;
  padding: 4rem 2rem;
  max-width: var(--grid-max-width);
  margin: 0 auto;
}
.bg-hero-title {
  grid-column: 1 / span 8;
  grid-row: 1;
  z-index: 2;
  font-family: var(--font-grid-display);
  font-size: clamp(3rem, 8vw, 7rem);
  line-height: 0.95;
  color: var(--ink-grid-primary);
  margin: 0;
}
.bg-hero-media {
  grid-column: 5 / 13;
  grid-row: 1 / span 2;
  z-index: 1;
  position: relative;
}
.bg-hero-media img {
  width: 100%;
  height: auto;
  display: block;
}
.bg-hero-body {
  grid-column: 2 / span 4;
  grid-row: 2;
  z-index: 3;
  font-family: var(--font-grid-sans);
  margin-top: -3rem;
  background: var(--bg-grid-linen);
  padding: 1.5rem;
}
```

### 2. Off-Axis Editorial Button (`.bg-btn`)
An asymmetric action trigger offset from its container bounding box.
```css
.bg-btn {
  display: inline-block;
  background: var(--ink-grid-primary);
  color: #FFFFFF;
  font-family: var(--font-grid-sans);
  font-size: 0.95rem;
  font-weight: 600;
  padding: 0.8rem 2rem;
  border: none;
  cursor: pointer;
  margin-left: 2rem;
  margin-top: -1rem;
  position: relative;
  z-index: 4;
  transition: transform 0.2s ease, background-color 0.2s ease;
}
.bg-btn:hover {
  background: var(--accent-grid-red);
  transform: translate(-3px, -3px);
}
```

### 3. Asymmetric Section Card (`.bg-card`)
A content card deliberately offset by 1 column from standard alignment.

### 4. Responsive Mobile Reflow System (`@media max-width: 48rem`)
A clean collapse rule resetting overlapping layers into an orderly single-column flow on mobile viewports.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **DOM Sequence vs Visual Position (WCAG 1.3.2 & 2.4.3):** When CSS Grid repositions elements visually across columns and rows, the underlying HTML source code must strictly follow the natural reading order: Heading first, Image second, Body copy third. Screen readers and keyboard navigation must never jump erratically across the layout.
- **Text-Over-Image Contrast (WCAG 1.4.3):** When headlines overlap photography, the text must maintain at least 4.5:1 contrast against every pixel it crosses. If photography varies in brightness, place an opaque backing plate (`background: var(--bg-grid-linen)`) behind the overlapping text block.
- **Responsive Reflow (WCAG 1.4.10):** Overlapping CSS Grid configurations rarely survive viewports under 48rem (768px). Use media queries to gracefully collapse overlapping layers into a single clean column, preventing horizontal scrolling or text clipping at 320 CSS pixels.
- **Focus Rings:** Unobscured focus outline with 2px offset (`outline: 2px solid var(--accent-grid-red); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Architectural monographs, design agency portfolios, and fashion lookbooks.
- Cultural journalism, literary essays, and art exhibition landing pages.
- High-concept brand showcases looking to subvert generic card-based templates.

### Anti-Patterns & Prohibitions
- Form-heavy applications, multi-step checkout flows, or medical patient records where unexpected layout shifts create errors.
- Financial trading dashboards where instant spatial predictability is critical.
- Overlapping interactive buttons on top of other interactive links, which causes accidental clicks.

---

## 📚 Authoritative Sources & Historical Artifacts

- Josef Müller-Brockmann, *Grid Systems in Graphic Design*, Niggli, 1981.
- David Carson, *The End of Print: The Graphic Design of David Carson*, Chronicle Books, 1995.
- Rachel Andrew, *The New CSS Layout*, A Book Apart, 2017.
- W3C, *CSS Grid Layout Module Level 1*, W3C Recommendation.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Layout Styles:** [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md).
- **Postmodern & Editorial Peers:** [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-maximalism](../ui-style-maximalism/SKILL.md).
