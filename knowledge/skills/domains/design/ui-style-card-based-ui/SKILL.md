---
name: "ui-style-card-based-ui"
description: "Provides the card-based UI style (2013-present): self-contained content containers in grids and masonry, covering Material's card anatomy, Bootstrap 4 standardization, masonry techniques, container transforms and the density and reading-order pitfalls. Use when designing feeds, commerce grids, dashboards or any card-component system."
---

# UI Style: Card-Based UI

> *"A card is a sheet of material that serves as an entry point to more detailed information. Cards may contain a photo, text, and a link about a single subject."*  
> — Google Material Design Guidelines (2014)

Card-Based UI organizes information into discrete, self-contained interactive surfaces. Originating in physical index cards, Tarot decks, and business cards, the digital card pattern unifies heterogeneous multimedia—imagery, typography, telemetry, and actions—into a modular, easily manipulable physical metaphor ideal for responsive viewports and infinite feed architectures.

---

## 🧭 When to Activate

- Designing e-commerce product catalogs, social media feeds, streaming media directories, and portfolio galleries.
- Building interactive Kanban workflows (Trello, Jira Boards) with drag-and-drop state manipulation.
- Structuring dashboard metric widgets where each card encapsulates one distinct data dimension.
- Creating modular design system component libraries requiring predictable, swappable content units.

---

## 🕰️ Definition, Lineage, and Timeline

- **Physical Heritage:** 19th-century filing systems, library catalog cards, baseball trading cards, and mid-century recipe index files.
- **2010–2011 (The Masonry Pioneers):** Pinterest launches with a multi-column cascading masonry grid designed by Evan Sharp, proving cards could transform visual web discovery. Concurrently, Trello (Fog Creek) introduces draggable lists of cards for project management.
- **June 2014 (Google Material Design Codification):** Matias Duarte unveils Material Design at Google I/O. Cards receive an authoritative mathematical specification: elevation expressed through simulated Z-axis shadows (1dp to 8dp), standard internal paddings (16dp), rounded corners (4dp–8dp), and container-transform motion rules.
- **2018 (Bootstrap 4 Web Standardization):** Bootstrap 4 formally replaces legacy "panels, wells, and thumbnails" with the universal `.card` class, establishing the web standard for card composition.

### Absolute Style Vetos (What Card-Based UI is NOT)
- ❌ **NOT Asymmetric Bento Grid ([ui-style-bento-grid](../ui-style-bento-grid/SKILL.md)):** Card-based UI emphasizes *homogeneous or modularly predictable container rhythm* within uniform grid columns or masonry tracks, rather than deliberate multi-span asymmetric puzzle arrangements.
- ❌ **NOT Pure Flat Text Tables:** A card requires distinct surface elevation, a container boundary, or an explicit encapsulating frame. Raw text rows without containerization do not constitute cards.
- ❌ **NOT Overlapping Broken Grid:** Cards maintain rigorous gutter boundaries and predictable packing order.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                               CARD-BASED UI TAXONOMY                               |
+------------------------------------------------------------------------------------+
| Standard E-Commerce / Catalog Card   | Draggable Kanban / Task Card                |
| - Fixed 16:9 or 1:1 media thumbnail  | - Compact vertical density, no media        |
| - Header & subhead title grouping    | - Drag-handle grip indicator                |
| - Supporting body / price tag        | - Priority chip & assignee avatar           |
| - Dual action button row at bottom   | - Subtle drop shadow on drag elevation      |
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **Container Autonomy:** Every card represents an atomic concept. Extracting a card and rendering it elsewhere preserves its complete contextual meaning.
2. **Standard Internal Anatomy:**
   - **Media Container:** Edge-to-edge header image or video thumbnail.
   - **Header Group:** Primary title and category/date eyebrow.
   - **Supporting Copy:** 2 to 3 lines of contextual text.
   - **Action Bar:** Dedicated footer hosting primary and secondary triggers.
3. **Z-Axis Elevation Hierarchy:** Surfaces exist in simulated physical layers: Resting (Elevation 1), Hover/Focus (Elevation 2), Dragged/Active (Elevation 4).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Card systems leverage ambient occlusion and directional key lighting to communicate interactability:
- **Resting Elevation (Z1):** Soft diffuse contact shadow indicating resting proximity to the background canvas: `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)`.
- **Hover Elevation (Z2):** Upward translation accompanied by an expanded, deeper shadow: `transform: translateY(-2px); box-shadow: 0 6px 16px -2px rgba(0, 0, 0, 0.12), 0 2px 6px -1px rgba(0, 0, 0, 0.06)`.
- **Active / Drag Elevation (Z4):** Dramatic elevation during touch or drag: `box-shadow: 0 16px 32px -4px rgba(0, 0, 0, 0.20), 0 8px 16px -2px rgba(0, 0, 0, 0.10)`.
- **Surface Palette:** Crisp white or dark charcoal surface contrasted against a slightly darker or tinted background canvas (`#F4F5F7` or `oklch(0.14 0.005 270)`).

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Surfaces & Canvas */
  --card-bg-canvas: oklch(0.97 0.005 260);
  --card-bg-surface: oklch(1.00 0 0);
  --card-bg-hover: oklch(0.99 0.002 260);

  /* Borders & Hairlines */
  --card-border: oklch(0.20 0.01 260 / 0.10);
  --card-border-hover: oklch(0.20 0.01 260 / 0.20);
  --card-border-focus: oklch(0.55 0.22 250);

  /* Elevation Shadows */
  --card-shadow-z1: 0 2px 4px oklch(0 0 0 / 0.06), 0 1px 2px oklch(0 0 0 / 0.04);
  --card-shadow-z2: 0 8px 20px -3px oklch(0 0 0 / 0.10), 0 3px 6px -2px oklch(0 0 0 / 0.05);
  --card-shadow-z4: 0 18px 36px -6px oklch(0 0 0 / 0.18), 0 8px 16px -4px oklch(0 0 0 / 0.08);

  /* Radii & Spacing */
  --card-radius: 12px;
  --card-radius-media: 12px 12px 0 0;
  --card-padding: 20px;
  --card-gutter: 24px;

  /* Typography Colors */
  --card-text-title: oklch(0.18 0.01 260);
  --card-text-body: oklch(0.42 0.01 260);
  --card-text-muted: oklch(0.60 0.01 260);

  /* Transitions */
  --card-transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1),
                     box-shadow 180ms cubic-bezier(0.16, 1, 0.3, 1),
                     border-color 180ms ease;
}

[data-theme="dark"] {
  --card-bg-canvas: oklch(0.13 0.005 260);
  --card-bg-surface: oklch(0.18 0.006 260);
  --card-bg-hover: oklch(0.22 0.008 260);
  --card-border: oklch(1 0 0 / 0.08);
  --card-border-hover: oklch(1 0 0 / 0.18);
  --card-text-title: oklch(0.96 0 0);
  --card-text-body: oklch(0.72 0.01 260);
  --card-text-muted: oklch(0.50 0.01 260);
  --card-shadow-z1: 0 2px 6px oklch(0 0 0 / 0.30);
  --card-shadow-z2: 0 10px 24px -4px oklch(0 0 0 / 0.45);
}
```

---

## 🔤 Typography & Lettering Architecture

Card typography enforces tight vertical rhythms:
- **Card Title:** `font-weight: 600`, `16px` to `18px`, `letter-spacing: -0.015em`, line-height `1.3`. Limited to 2 lines via `-webkit-line-clamp: 2`.
- **Card Eyebrow / Category Tag:** `font-weight: 700`, `11px`, `letter-spacing: 0.06em`, uppercase, color `--card-text-muted`.
- **Card Body Text:** `font-weight: 400`, `13px` to `14px`, line-height `1.45`, color `--card-text-body`.
- **Action Links & Buttons:** `font-weight: 600`, `13px`, text-decoration none.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **The Accessible Clickable Card Pattern:** While the entire card surface appears clickable, wrapping the entire card in an `<a>` tag disrupts screen reader accessibility. The canonical implementation embeds the primary link inside the heading and expands its clickable hit area across the whole card via a pseudo-element (`.card-title a::after { position: absolute; inset: 0; content: ""; }`). Secondary action buttons are layered above via `z-index: 2`.
- **Container Transform:** On click, cards expand fluidly to fill the viewport (modal or detail page) via CSS Shared Element Transitions or FLIP technique.

---

## 🧩 Canonical Component Specifications

### 1. E-Commerce Product Card with Media & Actions

```html
<article class="standard-card">
  <div class="card-media-wrapper">
    <img src="product.jpg" alt="Mechanical Keyboard" class="card-media" loading="lazy" />
    <span class="card-badge">In Stock</span>
  </div>
  <div class="card-content">
    <div class="card-eyebrow">Hardware / Peripherals</div>
    <h3 class="card-title">
      <a href="/products/keychron-q1">Keychron Q1 Custom Mechanical Keyboard</a>
    </h3>
    <p class="card-summary">CNC machined 75% layout aluminum chassis with hot-swappable switches and QMK/VIA firmware support.</p>
    <div class="card-footer">
      <span class="card-price">$189.00</span>
      <button class="card-btn-action" aria-label="Add to cart">Add to Cart</button>
    </div>
  </div>
</article>
```

```css
.standard-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--card-bg-surface);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow-z1);
  overflow: hidden;
  transition: var(--card-transition);
}

.standard-card:hover {
  background: var(--card-bg-hover);
  border-color: var(--card-border-hover);
  box-shadow: var(--card-shadow-z2);
  transform: translateY(-2px);
}

.card-media-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: oklch(0.92 0 0);
}

.card-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 300ms ease;
}

.standard-card:hover .card-media {
  transform: scale(1.03);
}

.card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: oklch(0 0 0 / 0.65);
  backdrop-filter: blur(4px);
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 4px;
}

.card-content {
  padding: var(--card-padding);
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-eyebrow {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--card-text-muted);
  margin-bottom: 6px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.card-title a {
  color: var(--card-text-title);
  text-decoration: none;
}

.card-title a::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
}

.card-summary {
  font-size: 13px;
  line-height: 1.45;
  color: var(--card-text-body);
  margin: 0 0 16px 0;
  flex: 1;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--card-border);
  z-index: 2; /* Sits above link overlay */
}

.card-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--card-text-title);
}

.card-btn-action {
  background: var(--card-text-title);
  color: var(--card-bg-surface);
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Target Size & Interactive Regions:** When multiple interactive triggers exist inside one card (e.g. favorite button, category tag, full-card click, and add-to-cart), they must maintain a minimum bounding separation to satisfy **WCAG 2.5.8 (Target Size Minimum, 24x24px)**.
- **Screen Reader Link Redundancy:** Avoid marking both the image, the title, and a "Read More" button as separate redundant links to the same destination. Use the pseudo-element link expansion pattern described above.
- **Focus Rings:** Cards must display an explicit `focus-within` outline (`outline: 2px solid var(--card-border-focus); outline-offset: 2px;`) when keyboard focus lands on any internal element.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Browsable feeds, retail product catalogs, streaming media libraries, real estate listings.
- Modular dashboards where cards can be repositioned or collapsed.
- Responsive mobile views where horizontal rows gracefully collapse into vertical stacks.

### Inappropriate Scenarios
- Dense tabular analysis (accounting spreadsheets, database editors) where high information density without container overhead is critical.
- Linear editorial prose (essays, book chapters) where cards fragment reading flow.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Google Design (2014):** *"Material Design Specification: Surfaces, Elevation & Cards"*, Google I/O.
2. **Bootstrap Documentation (2018):** *"Components: Cards Anatomy and Layout"*, Bootstrap 4 (getbootstrap.com/docs/4.0/).
3. **Pickering, Heydon (2018):** *"Inclusive Components: Cards"*, inclusive-components.design.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct sibling to [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md) (homogeneous grid vs heterogeneous multi-span).
- Integrates with [ui-style-material-you](../ui-style-material-you/SKILL.md) and [ui-style-flat-design](../ui-style-flat-design/SKILL.md).
