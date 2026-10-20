---
name: "ui-style-bento-grid"
description: "Provides the bento grid UI style (2022-present): compartmentalized bento-box layouts of asymmetric rounded tiles with hierarchy expressed by span rather than shadow, covering the CSS grid recipe, Apple keynote lineage, motion patterns, DOM-order accessibility risks and appropriate page types. Use when designing feature overviews, marketing pages or portfolio grids in the Apple bento grammar."
---

# UI Style: Bento Grid

> *"Simplicity is not the lack of clutter, that's a consequence of simplicity. Simplicity is somehow essentially describing the purpose and place of an object and product."*  
> — Jony Ive / Apple Industrial Design Ethos

Bento Grid adapts the compartmentalized elegance of Japanese bento lunchboxes (*makunouchi bento*) and Apple keynote presentation modules into a web layout paradigm. Rather than forcing uniform cards into a monotonous feed, Bento Grid organizes heterogeneous content—micro-visualizations, hardware specs, telemetry counters, and high-impact hero shots—into an interlocking, asymmetric mosaic governed by a shared mathematical gutter.

---

## 🧭 When to Activate

- Designing product marketing pages, hardware launch overviews, and SaaS feature summaries where multiple disparate capabilities must be communicated simultaneously.
- Constructing personal portfolio hubs, multi-metric executive dashboards, and interactive changelogs.
- Replacing monotonous bulleted lists with modular visual storytelling.
- Building responsive layouts using modern CSS Grid (`grid-template-areas`, `subgrid`, and container queries).

---

## 🕰️ Definition, Lineage, and Timeline

- **Traditional Precedents:** The centuries-old Japanese *bento* box tradition, wherein wooden lacquered compartments keep distinct culinary flavors physically separated yet harmoniously composed.
- **2010–2014 (Early Precursors):** Windows 8 Metro UI introduced asymmetric tile spans, while Google's Material Design (2014) systematized cards. However, these systems enforced uniform content types.
- **September 2022 (The Apple Hardware Revolution):** Apple's iPhone 14 Pro and M2 MacBook Air keynotes formalize the modern Bento slide format. Instead of bullet points, single slides present dense mosaics: large silicon wafer renders spanning 2x2 cells flanked by battery life counters, camera sensor specs, and iOS lock screen previews.
- **2023–Present (Web Omnipresence):** Bento.me launches, popularizing bento-box personal websites. Web frameworks and landing page builders adopt the bento grid as the default design language for high-converting developer tools (Vercel, Next.js, Raycast).

### Absolute Style Vetos (What Bento Grid is NOT)
- ❌ **NOT Homogeneous Card Feed ([ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md)):** A bento grid is NOT an endless grid of identical e-commerce product cards or social media posts. The defining hallmark is *heterogeneity of cell spans and content modalities*.
- ❌ **NOT Freeform Broken Grid ([ui-style-broken-grid](../ui-style-broken-grid/SKILL.md)):** Bento cells never collide, overlap chaotically, or break orthogonal alignment. Gutters are strictly uniform across all axes.
- ❌ **NOT Skeuomorphic Tactility:** Surfaces are clean, dark or light squircle panels with ultra-subtle border strokes, not thick realistic plastic or wood containers.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                BENTO GRID TAXONOMY                                 |
+------------------------------------------------------------------------------------+
| Hardware / Launch Deck Spec          | Software Feature Mosaic                     |
| - High-contrast black/charcoal base  | - Light/dark neutral surfaces               |
| - High-resolution 3D asset in 2x2    | - Interactive micro-controls in 1x1 cells   |
| - Single metric counter (e.g. 3.2x)  | - Code snippet preview in 2x1 wide cell     |
| - Squircle corner radius (24px-32px) | - Subdued secondary telemetry               |
+------------------------------------------------------------------------------------+
```

### Visual Characteristics
1. **Hierarchy Through Span:** Visual importance is determined by column and row spans (e.g., `span 8` for the flagship capability, `span 4` for supplementary metrics), rather than heavy drop shadows or lurid accent colors.
2. **Squircle Curvature:** Generous, smooth continuous corner radii (typically `20px` to `32px` on desktop) applied universally to all modular cells.
3. **Internal Micro-Compositions:** Each bento cell functions as a miniature autonomous canvas with dedicated typography, internal padding (`24px` to `32px`), and tailored alignment.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Bento Grid relies on industrial surface precision rather than dramatic lighting effects:
- **Surface Geometry:** Rounded squircle tiles with a hairline border: `border: 1px solid oklch(1 0 0 / 0.08)`.
- **Specular Top Edge:** An internal inset shadow simulates high-end anodized aluminum or polished glass: `box-shadow: inset 0 1px 0 0 oklch(1 0 0 / 0.12)`.
- **Subtle Surface Elevation:** Low-frequency ambient shadow: `box-shadow: 0 8px 32px -4px oklch(0 0 0 / 0.25)`.
- **Color Temperature:** Neutral charcoal surfaces (`oklch(0.18 0.005 270)`) contrasted against bright white typography, with occasional single-cell vivid gradients reserved for key metrics.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Bento Container & Gutters */
  --bento-gutter: 20px;
  --bento-radius: 24px;
  --bento-radius-inner: 16px;
  --bento-padding: 28px;

  /* Surfaces (Dark Mode Canonical) */
  --bento-bg-canvas: oklch(0.12 0.005 260);
  --bento-bg-cell: oklch(0.16 0.006 260);
  --bento-bg-cell-elevated: oklch(0.20 0.008 260);
  --bento-bg-cell-hover: oklch(0.22 0.010 260);

  /* Border & Specular */
  --bento-border: oklch(1 0 0 / 0.08);
  --bento-border-hover: oklch(1 0 0 / 0.20);
  --bento-specular: inset 0 1px 0 0 oklch(1 0 0 / 0.15);
  --bento-shadow: 0 12px 30px -10px oklch(0 0 0 / 0.40);

  /* Typography */
  --bento-text-hero: oklch(0.98 0 0);
  --bento-text-body: oklch(0.75 0.01 260);
  --bento-text-muted: oklch(0.52 0.01 260);

  /* Accents */
  --bento-accent-cyan: oklch(0.75 0.16 210);
  --bento-accent-purple: oklch(0.68 0.22 290);
  --bento-accent-amber: oklch(0.80 0.18 75);

  /* Transitions */
  --bento-transition: all 240ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 🔤 Typography & Lettering Architecture

Bento grids utilize geometric sans-serif typography with strong scale differentials:
- **Hero Title (Large Feature Cell):** `font-weight: 700`, `32px` to `44px`, `letter-spacing: -0.03em`, line-height `1.1`.
- **Telemetry Counter / Metric:** `font-weight: 800`, `48px` to `64px`, `font-feature-settings: "tnum" 1`, letter-spacing `-0.04em`.
- **Card Subheadings:** `font-weight: 600`, `18px`, `letter-spacing: -0.015em`.
- **Body & Explanatory Copy:** `font-weight: 400`, `14px`, line-height `1.5`, color `--bento-text-body`.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Independent Cell Hover:** Bento cells respond independently to hover states. On cursor entry, the targeted cell lifts slightly (`transform: translateY(-2px)`), the border brightens, and internal visualizers trigger subtle micro-movements.
- **Staggered Scroll Reveal:** When the bento grid enters the viewport, cells fade and scale in with a `40ms` stagger delay per cell.
- **Audio Profile:** Silent or ultra-minimalist soft haptic clicks for interactive toggle cells (`80Hz` low-frequency thud).

---

## 🧩 Canonical Component Specifications

### 1. Asymmetric 3-Module Bento Grid Section

```html
<section class="bento-container" aria-label="Product Capabilities">
  <!-- Hero Feature Cell (2x2 Span) -->
  <article class="bento-cell bento-hero">
    <div class="bento-header">
      <span class="bento-tag">Flagship Architecture</span>
      <h3 class="bento-title">Zero-Latency Edge Inference</h3>
      <p class="bento-desc">Deploy fine-tuned neural models across 300+ global edge nodes with automatic failover and instantaneous cold starts.</p>
    </div>
    <div class="bento-visual">
      <div class="bento-wireframe-globe"></div>
    </div>
  </article>

  <!-- Metric Cell (1x1 Span) -->
  <article class="bento-cell bento-metric">
    <span class="bento-tag">Throughput</span>
    <div class="bento-stat">12.4x</div>
    <p class="bento-desc">Faster token delivery than standard regional clusters.</p>
  </article>

  <!-- Code / Feature Cell (1x1 Span) -->
  <article class="bento-cell bento-code">
    <span class="bento-tag">Instant Integration</span>
    <pre class="bento-snippet"><code>$ curl -X POST api.coacus.io/v1/run</code></pre>
    <div class="bento-badge-group">
      <span class="bento-badge">HTTP/3</span>
      <span class="bento-badge">mTLS</span>
    </div>
  </article>
</section>
```

```css
.bento-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--bento-gutter);
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.bento-cell {
  background: var(--bento-bg-cell);
  border: 1px solid var(--bento-border);
  border-radius: var(--bento-radius);
  box-shadow: var(--bento-shadow), var(--bento-specular);
  padding: var(--bento-padding);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  transition: var(--bento-transition);
}

.bento-cell:hover {
  background: var(--bento-bg-cell-hover);
  border-color: var(--bento-border-hover);
  transform: translateY(-2px);
}

.bento-hero {
  grid-column: span 8;
  grid-row: span 2;
  min-height: 420px;
}

.bento-metric {
  grid-column: span 4;
}

.bento-code {
  grid-column: span 4;
}

.bento-tag {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--bento-accent-cyan);
  margin-bottom: 8px;
}

.bento-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--bento-text-hero);
  margin: 0 0 12px 0;
}

.bento-desc {
  font-size: 14px;
  line-height: 1.5;
  color: var(--bento-text-body);
  margin: 0;
}

.bento-stat {
  font-size: 54px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--bento-text-hero);
  font-feature-settings: "tnum" 1;
  margin: 8px 0;
}

@media (max-width: 900px) {
  .bento-hero, .bento-metric, .bento-code {
    grid-column: span 12;
    grid-row: auto;
  }
}
```

### 2. Masonry Packing Variant (`display: grid-lanes`)

When tiles have unknown heights (portfolio images, testimonials), CSS Grid Lanes packs them into columns without row gaps. Support is narrow: Safari 26.4 ships it; Chrome and Edge have an older alternative syntax behind a flag; Firefox has the original `grid-template-rows: masonry` syntax behind a preference. Declare `display` twice so other engines keep a regular grid, and scope lane-only rules with `@supports`:

```css
.bento-lanes {
  display: grid;                /* fallback: aligned rows */
  display: grid-lanes;          /* ignored where unsupported */
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: var(--bento-gutter);
}
@supports not (display: grid-lanes) {
  .bento-lanes > * { align-self: start; }
}
```

Masonry packing places items by available space, so visual order drifts from source order; keep the classic span-based bento for curated hierarchy and reserve lanes for homogeneous, order-insensitive collections.

---

## ♿ Accessibility & Environmental Contrast

- **DOM Source Order vs Visual Grid (1.3.2 Meaningful Sequence, 2.4.3 Focus Order):** A primary hazard in asymmetric CSS grid layouts is disconnecting visual reading order from the DOM tab sequence. Bento markup MUST be authored in logical priority order (Hero first, secondary metrics next). Never rely on `grid-row`, `order`, dense auto-placement or masonry packing to rearrange content in ways that disorient screen reader and keyboard users; DOM order is the reading order.
- **`reading-flow` Is Not a Fix Yet:** `reading-flow: grid-rows` (and related values) lets the browser follow visual grid order for focus and reading, but it is experimental and ships only in Chromium 137+. Treat it as progressive enhancement after the DOM order is already correct, never as the remedy.
- **Long-Running Tile Animations (2.2.2, Level A):** Looping visualizers, tickers or auto-rotating tiles that start automatically and run longer than 5 seconds need a visible pause control (hover-only pausing does not count) or must stop within 5 seconds. Scroll-reveal staggers end quickly and need only the reduced-motion treatment. Canonical motion obligations live in [web accessibility](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- **Heading Level Hierarchy:** Each bento cell must provide an explicit semantic heading (`<h2>` or `<h3>`) matching its structural outline, avoiding skipping heading levels.
- **Color Contrast:** All text content inside bento cells meets WCAG 2.2 Level AA requirements (minimum **4.5:1** contrast). Large metric displays (`54px+`) satisfy Level AAA requirements (**7:1+**).

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- High-impact marketing pages, product feature showcases, hardware spec sheets.
- Portfolio sites highlighting diverse mediums (photography, case studies, client logos).
- Executive summary dashboards bringing together telemetry, graphs, and live server health.

### Inappropriate Scenarios
- High-volume data feeds (e.g. social media timelines or e-commerce search results) where uniform predictability is mandatory.
- Tabular data entry tools and enterprise spreadsheet software.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Apple Special Event Keynote Design Archives (2022–2024):** iPhone 14 Pro, Apple Watch Ultra, and M-Series Silicon launch architectures.
2. **Bento.me Visual Grammar (2023):** Modular compartmentalized personal portfolio architecture.
3. **MDN Web Docs:** *"CSS Grid Layout and Accessibility Considerations"*, Mozilla Developer Network.
4. **WebKit Blog:** *"When will CSS Grid Lanes arrive? How long until we can use it?"*, 2026-01-22 (fallback pattern and engine status).

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Differentiated from [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md) through multi-span asymmetry and heterogeneous content modalities.
- Integrates with [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md) for dark-first product landing pages and [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md) for mathematical grid discipline.
## Appearance and Interaction Verification

Bound clipping to visual artwork, keep headings/code and interactive controls reachable, and re-evaluate cell spans/padding/min-height by available cell width and viewport height while retaining uniform gutters and heterogeneous spans.

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **`display: grid-lanes` fallback pattern and engine status, 2026-01-22** (verified) — https://webkit.org/blog/17758/
- **`display: grid-lanes` shipping in Safari 26.4 only** (verified) — MDN browser-compat-data 8.1.6 (2026-10-15)
- **`reading-flow` in Chromium 137+, experimental** (verified) — MDN browser-compat-data 8.1.6 (2026-10-15)
- **WCAG 2.2, W3C Recommendation, 2024-12-12 edition** (verified) — https://www.w3.org/TR/WCAG22/
