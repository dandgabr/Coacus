---
name: "ui-style-metro-modern-ui"
description: "Provides the Metro / Microsoft Design Language style (2010-2015): typography-first flat design with content-before-chrome, live tiles and motion as a first-class principle, covering the Zune-to-Windows-8 lineage, Segoe type identity, Nielsen's Windows 8 usability verdict and CSS reconstruction. Use when designing typography-led dashboards or studying flat design's true origin."
---

# UI Style: Metro / Modern UI (Microsoft Design Language)

> *"Content before chrome. Be authentically digital. Clean, light, open, fast — celebrate the typography and let the user's data become the interface."*  
> — Microsoft Design Principles, Windows Phone 7 & Windows 8 Design Guidelines (2010)

Metro (later branded Microsoft Design Language / Modern UI) represents the boldest, most influential typography-first revolution in consumer user interfaces since the Xerox Star. Rejecting all skeuomorphic bevels, chrome textures, and artificial drops, Metro pioneered flat, authentically digital design rooted in the Swiss / International Typographic Style, Bauhaus reductionism, and airport wayfinding signage.

---

## 🧭 When to Activate

- Designing typography-led dashboards, telemetry monitors, media hubs, and content-first kiosks where typographic hierarchy and clean planar geometry supersede decorative illustrations.
- Building live tile grids, horizontally panning panoramic canvases, or billboard-scale informational displays.
- Studying or recreating the authentic historical pioneer of flat digital interfaces (predating Apple's iOS 7 and Google's Material Design).
- Modernizing enterprise portals that benefit from high-visibility primary tiles, rapid scanning, and zero gratuitous shadows.

---

## 🕰️ Definition, Lineage, and Timeline

- **1995 (Encarta & MSN):** Early typographic experiments in CD-ROM encyclopedias and web portals prioritize clean headers and content grouping over heavy OS frames.
- **2002–2006 (Windows Media Center & Zune):** The "Zune Desktop" and portable media players introduce the radical "Zegoe" typographic stack, full-bleed album art, and horizontal list scrolling.
- **March 2010 (MIX10 Windows Phone 7 Unveiling):** Joe Belfiore, Albert Shum, and Michael Smuga formally introduce Metro: *"Content is our chrome"*, live updating squares, panorama views, and strict grid alignments.
- **August 2012 (The Renaming):** Following a trademark dispute with German retail conglomerate Metro AG, Microsoft replaces the moniker with "Microsoft Design Language" (MDL) and Modern UI.
- **October 2012 (Windows 8 Launch):** The Start Screen replaces the Start Menu with a full-screen Live Tile grid. While praised for bold typography and tablet touch ergonomics, Jakob Nielsen's landmark usability audit condemns the forced dual-mode desktop paradigm.
- **2017 (Fluent Design System):** Microsoft evolves MDL into Fluent, re-introducing subtle depth, acrylic blur, and directional lighting.

### Absolute Style Vetos (What Metro is NOT)
- ❌ **NOT Post-2017 Fluent Design:** No translucent acrylic frosted glass, no Gaussian blurs, no cursor spotlight reveals, no rounded 8px corners.
- ❌ **NOT iOS 7 Ultra-Thin Skeuomorphism:** No faint hairline dials, no neon gradient washes, no animated 3D gyro parallax.
- ❌ **NOT Playful Neo-Brutalism:** No rough comic-book black outlines, no tilt angles, no decorative stickers. Metro is hyper-disciplined, planar, and Swiss.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                                METRO UI TAXONOMY                                   |
+------------------------------------------------------------------------------------+
| Live Tile Hub (Start Matrix)         | Panorama / Content Pivot (Horizontal)       |
| - Square & double-wide rectangles    | - Huge lowercase page titles (36pt-48pt)    |
| - High-contrast flat color blocks    | - Typography that bleeds off right edge     |
| - Bottom-aligned white labels        | - Monochromatic line iconography (Symbol)   |
| - 3D tile flip animation (flip 180°) | - Semantic Zoom out to high-level index     |
+------------------------------------------------------------------------------------+
```

### Core Design Principles
1. **Fiercely Flat & Authentically Digital:** No drop shadows, no embossed bevels, no glossy gradients. Every pixel exists purely on the 2D plane.
2. **Typography as Information Canvas:** Data *is* the graphic. Numbers and headlines take center stage at monumental scales (48px–72px), contrasted against ultra-clean body text.
3. **Motion is a First-Class Citizen:** Live tiles flip to reveal back-face news, items tilt in 3D perspective upon mouse press, and pages slide horizontally with physical spring decay.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Metro rejects physical real-world lighting simulation:
- **Lighting Model:** Completely ambient, uniform 100% flat luminescence. Zero specular highlights, zero directional shading, zero cast ambient occlusion.
- **Surface Geometry:** Pure 90-degree orthogonal edges (`border-radius: 0px`).
- **Surface Elevation:** Expressed exclusively via **Z-layering** and spatial canvas scale (Semantic Zoom), never via drop shadow blur radii.
- **Tile Chromatic Blocks:**
  - Vibrant Cobalt: `oklch(0.55 0.22 250)` (#0078D7)
  - Windows Crimson: `oklch(0.52 0.23 25)` (#E51400)
  - Emerald Green: `oklch(0.60 0.19 145)` (#00A600)
  - Amber Orange: `oklch(0.68 0.18 55)` (#FF8C00)
  - Cyan: `oklch(0.65 0.16 210)` (#1BA1E2)

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Surface & Base Viewport */
  --metro-bg-canvas: #000000;
  --metro-bg-surface: #1F1F1F;
  --metro-bg-tile-default: #0078D7;

  /* Classic Metro Palette Accents */
  --metro-accent-blue: #0078D7;
  --metro-accent-teal: #00A4A4;
  --metro-accent-green: #339933;
  --metro-accent-orange: #FF8C00;
  --metro-accent-crimson: #E51400;
  --metro-accent-magenta: #D80073;
  --metro-accent-purple: #76608A;

  /* Typographic Contrast */
  --metro-text-title: #FFFFFF;
  --metro-text-body: #CCCCCC;
  --metro-text-muted: #888888;
  --metro-text-inverse: #000000;

  /* Structural Disciplines */
  --metro-radius: 0px;
  --metro-tile-gap: 8px;
  --metro-border-subtle: 2px solid transparent;
  --metro-border-focus: 2px solid #FFFFFF;

  /* Motion & 3D Perspective */
  --metro-perspective: 800px;
  --metro-tilt-transition: transform 120ms cubic-bezier(0.1, 0.9, 0.2, 1);
  --metro-flip-transition: transform 600ms cubic-bezier(0.2, 0.8, 0.2, 1);
}

[data-theme="light"] {
  --metro-bg-canvas: #FFFFFF;
  --metro-bg-surface: #F0F0F0;
  --metro-text-title: #000000;
  --metro-text-body: #333333;
  --metro-text-muted: #777777;
  --metro-border-focus: 2px solid #000000;
}
```

---

## 🔤 Typography & Lettering Architecture

Metro's core soul is **Segoe UI** (authored by Steve Matteson):
- **Hero / Header 1 (Panorama):** `Segoe UI Light`, `300` weight, font-size `42px` to `56px`, letter-spacing `-0.02em`, lowercase default for subheadings (`recent items`, `all apps`).
- **Tile Header:** `Segoe UI Semibold`, `600` weight, font-size `14px`, uppercase or sentence case, bottom-left anchored.
- **Live Tile Metric / Big Stat:** `Segoe UI`, `300` weight, font-size `36px` to `48px`, tabular numerals.
- **Body & Paragraphs:** `Segoe UI`, `400` weight, font-size `14px`, line-height `1.4`.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **The Metro 3D Press Tilt:** When the user clicks or presses a tile, the tile recedes slightly on a 3D Z-plane pivoted from the cursor contact point (`transform: perspective(600px) rotateX(4deg) scale(0.98)`).
- **Live Tile Flip:** Background tiles cycle information by performing a continuous 180-degree vertical flip on the X-axis every 5 to 10 seconds.
- **Audio Feedback:** Sharp, crisp, high-frequency single-click acoustic feedback: a clean 5ms glass-click sound upon tile activation.

---

## 🧩 Canonical Component Specifications

### 1. Live Tile (Standard Square & Wide Format)

```html
<div class="metro-tile-grid">
  <div class="metro-tile metro-tile-square tile-blue" tabindex="0">
    <div class="metro-tile-inner">
      <div class="metro-tile-front">
        <svg class="metro-tile-icon" width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
        <span class="metro-tile-label">Music</span>
      </div>
      <div class="metro-tile-back">
        <span class="metro-tile-stat">4,812</span>
        <span class="metro-tile-label">Tracks Synced</span>
      </div>
    </div>
  </div>

  <div class="metro-tile metro-tile-wide tile-orange" tabindex="0">
    <div class="metro-tile-content">
      <div class="metro-tile-headline">System Alert</div>
      <div class="metro-tile-body">All cluster nodes running at 99.98% operational uptime.</div>
      <span class="metro-tile-label">Telemetry</span>
    </div>
  </div>
</div>
```

```css
.metro-tile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 140px);
  grid-auto-rows: 140px;
  gap: var(--metro-tile-gap);
  perspective: var(--metro-perspective);
}

.metro-tile {
  position: relative;
  border-radius: 0;
  outline: none;
  cursor: pointer;
  user-select: none;
  transition: var(--metro-tilt-transition);
}

.metro-tile:active {
  transform: perspective(600px) scale(0.96) rotateX(3deg);
}

.metro-tile:focus-visible {
  outline: var(--metro-border-focus);
}

.metro-tile-square {
  grid-column: span 1;
}

.metro-tile-wide {
  grid-column: span 2;
}

.tile-blue { background-color: var(--metro-accent-blue); }
.tile-orange { background-color: var(--metro-accent-orange); }

.metro-tile-inner {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

.metro-tile-label {
  position: absolute;
  bottom: 8px;
  left: 10px;
  font-family: "Segoe UI", sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #FFFFFF;
}

.metro-tile-stat {
  font-family: "Segoe UI", sans-serif;
  font-size: 32px;
  font-weight: 300;
  color: #FFFFFF;
  margin-top: 10px;
}
```

### 2. Panorama Pivot Header with Content Stream

```html
<section class="metro-pivot-container">
  <header class="metro-pivot-header">
    <h1 class="metro-pivot-appname">PROJECT TELEMETRY</h1>
    <div class="metro-pivot-tabs" role="tablist">
      <button class="metro-tab active" role="tab" aria-selected="true">overview</button>
      <button class="metro-tab" role="tab" aria-selected="false">live nodes</button>
      <button class="metro-tab" role="tab" aria-selected="false">audit log</button>
    </div>
  </header>
  <div class="metro-pivot-body" role="tabpanel">
    <!-- Panel Content -->
  </div>
</section>
```

```css
.metro-pivot-container {
  padding: 24px;
  background: var(--metro-bg-canvas);
  color: var(--metro-text-title);
  overflow-x: hidden;
}

.metro-pivot-appname {
  font-family: "Segoe UI", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--metro-text-muted);
  margin: 0 0 8px 0;
}

.metro-pivot-tabs {
  display: flex;
  gap: 28px;
  margin-bottom: 24px;
}

.metro-tab {
  background: transparent;
  border: none;
  font-family: "Segoe UI Light", "Segoe UI", sans-serif;
  font-size: 36px;
  font-weight: 300;
  color: var(--metro-text-muted);
  cursor: pointer;
  padding: 0;
  transition: color 150ms ease;
}

.metro-tab.active {
  color: var(--metro-text-title);
}

.metro-tab:hover {
  color: var(--metro-accent-blue);
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Level AA Compliance:**
  - High-contrast pure white text (#FFFFFF) over Metro accent tiles (`#0078D7`, `#E51400`, `#00A4A4`) delivers between **4.8:1** and **6.2:1** contrast.
  - Light mode requires dark text (#000000) over light accents (yellow/cyan) to prevent contrast failure.
- **Focus Indicators:** Pure flat styles often omit hover borders. Metro mandates a high-visibility 2px white outline (`outline: 2px solid #FFFFFF`) with an `outline-offset: -2px` on all focused tiles.
- **Affordance Signifiers:** To mitigate Jakob Nielsen's usability critique (lack of clear affordance for clickable elements), interactive tiles must include explicit glyph cues or typographic action labels.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Information dashboards, big-screen control room monitors, and transit signage displays.
- Digital kiosks requiring high-contrast, finger-friendly hit targets without visual distraction.
- Applications celebrating typographic craft and pure geometric minimalism.

### Inappropriate Scenarios
- Dense spreadsheet tooling where high data granularity requires thin 1px row dividers.
- Rich luxury e-commerce brands where photographic depth, tactile textures, and organic shadows are essential.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Microsoft Design Guidelines (2010):** *"Windows Phone Design System: Metro Principles"*, Microsoft MIX10.
2. **Kruzeniski, Mike (2011):** *"How Print Design is the Future of Interaction"*, Windows Design Team.
3. **Nielsen, Jakob (November 2012):** *"Windows 8 — Disappointing Usability for Both Novice and Power Users"*, Nielsen Norman Group.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct ancestor of [ui-style-flat-design](../ui-style-flat-design/SKILL.md) and contemporary foil to [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
- Contrasts with [ui-style-windows-xp](../ui-style-windows-xp/SKILL.md) by eliminating all bevels, drop shadows, and glossy plastic gradients.
## Appearance and Interaction Verification

Use accent-specific on-colors in tile examples, especially orange; allow tile grids and panorama tabs to reflow or remain reachable in narrow/short owners, and preserve exactly one semantic active panel while flipping decorative tile faces.

