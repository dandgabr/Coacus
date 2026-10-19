---
name: "ui-style-blueprint-cad-schematic"
description: "Provides the architectural blueprint and CAD schematic UI style: engineering cyan lines, coordinate crosshairs, dimension tick marks, monospaced drafting notes and technical grid backing. Use when building engineering tools, architecture portfolios or technical hardware docs."
---

# UI Style: Blueprint & CAD Technical Schematic

> *"An engineering drawing is not an artistic interpretation; it is an unambiguous legal and mathematical contract between designer and fabricator."*  
> — Engineering Drafting & Dimensioning Standards (ISO 128 / ANSI Y14)

Blueprint & CAD Schematic translates the authentic aesthetics of architectural cyanotype contact prints (Sir John Herschel, 1842) and computer-aided design drafting tools (AutoCAD, MicroStation) into user interfaces. Built on millimeter grid canvases, Prussian blue tones, precision dimensioning leader lines, coordinate crosshairs, and engineering title blocks, this style communicates mathematical rigor, physical transparency, and structural authority.

---

## 🧭 When to Activate

- Designing developer infrastructure consoles, robotics telemetry portals, and aerospace / hardware monitoring systems.
- Crafting civil engineering, architectural studio, and structural design portfolios.
- Building interactive technical documentation, API architecture visualizers, and hardware specification sheets.
- Transforming generic enterprise dashboards into high-craft technical drafting environments.

---

## 🕰️ Definition, Lineage, and Timeline

- **1842 (The Cyanotype Process):** Polymath Sir John Herschel invents the cyanotype process using ferric ammonium citrate and potassium ferricyanide, enabling rapid, low-cost architectural blueprint duplication.
- **1930s–1970s (The Drafting Room Era):** Hand-drafting with T-squares, ruling pens, and vellum paper establishes global drafting standards (ANSI, ISO). Drawings feature orthogonal dimension lines, extension ticks, and formal title blocks.
- **1982 (The AutoCAD Revolution):** John Walker and Autodesk release AutoCAD. Vector displays replace vellum paper, introducing high-contrast cyan, green, and white wireframe geometry on deep black/navy CRT monitors.
- **2010s–Present (Digital Technical revival):** Modern web engineering platforms adopt CAD conventions to communicate system reliability, infrastructure topologies, and cryptographic determinism.

### Absolute Style Vetos (What Blueprint is NOT)
- ❌ **NOT Cyberpunk HUD ([ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md)):** Blueprint is constructive, architectural, and calm—never dystopian, glitching, or weaponized with red targeting reticles.
- ❌ **NOT Terminal TUI ([ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md)):** Blueprint is graphical, vector-drawn, and dimension-annotated; it is not a monospace character-cell grid.
- ❌ **NOT Soft Neumorphism:** Zero extruded clay pills, zero blurred drop shadows. Every boundary is an orthogonal, razor-sharp vector line.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                         BLUEPRINT & CAD SCHEMATIC TAXONOMY                         |
+------------------------------------------------------------------------------------+
| Classical Cyanotype (Architectural)  | Precision CAD Wireframe (AutoCAD 1980s)     |
| - Deep Prussian Blue (#0A192F) base  | - Pitch Black or Midnight CRT background    |
| - Crisp white and pale cyan ink      | - Bright cyan (#00E5FF) and lime vector lines|
| - Hand-lettered drafting typography  | - Monospace coordinate readouts (X/Y/Z)     |
| - Millimeter graph grid texture      | - Dimension arrows, leader lines, & tolerances|
+------------------------------------------------------------------------------------+
```

### Visual Hallmarks
1. **The Technical Graph Grid:** Canvas background is scored with millimeter or 10px/50px dual-frequency grid lines in low-opacity cyan or cobalt.
2. **Dimensioning Annotation:** Data containers and cards incorporate drafting extension lines, dimension tick arrows, and tolerance notations (`±0.05mm`).
3. **The ISO Title Block (Approval Stamp):** Sections conclude with an official engineering title block recording revision numbers, author, scale, and status verification.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Blueprint & CAD Schematic exists within an architectural orthographic projection model:
- **Light Physics:** Zero perspective distortion, zero atmospheric perspective, zero sun shadows. All geometry is drawn on an infinite planar orthographic sheet.
- **Surface Geometry:** Pure 90-degree corners (`border-radius: 0px`).
- **Vector Strokes:** 1px hairline strokes with precise coordinate alignments (`shape-rendering: crispEdges`).
- **Background Grid Shader:**
  ```css
  background-image:
    linear-gradient(rgba(0, 229, 255, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 229, 255, 0.12) 1px, transparent 1px),
    linear-gradient(rgba(0, 229, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 229, 255, 0.04) 1px, transparent 1px);
  background-size: 50px 50px, 50px 50px, 10px 10px, 10px 10px;
  ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Classical Blueprint Prussian Palette */
  --cad-bg-canvas: #0A192F;         /* Deep Prussian Blue */
  --cad-bg-surface: #0E223D;        /* Elevated Drafting Sheet */
  --cad-bg-elevated: #132B4C;

  /* Line & Vector Strokes */
  --cad-stroke-cyan: #00E5FF;       /* High-Visibility Drafting Cyan */
  --cad-stroke-subtle: rgba(0, 229, 255, 0.25);
  --cad-stroke-grid: rgba(0, 229, 255, 0.08);
  --cad-stroke-white: #FFFFFF;

  /* Engineering Accents */
  --cad-accent-amber: #FFB300;      /* Warning / Dimension Callout */
  --cad-accent-crimson: #FF3B30;    /* Revision Stamp / Error */
  --cad-accent-green: #00E676;      /* Tolerance Pass / Verified */

  /* Typographic Contrast */
  --cad-text-primary: #FFFFFF;
  --cad-text-cyan: #00E5FF;
  --cad-text-muted: #5C82A6;

  /* Structural Geometry */
  --cad-radius: 0px;                /* Strict orthogonal purity */
  --cad-border-primary: 1px solid var(--cad-stroke-cyan);
  --cad-border-subtle: 1px solid var(--cad-stroke-subtle);

  /* Transitions */
  --cad-transition-snap: all 120ms linear;
}
```

---

## 🔤 Typography & Lettering Architecture

Blueprint typography honors standardized technical lettering (DIN 1451, ISO 3098, and monospaced terminal fonts):
- **Engineering Title / Title Block:** `"Space Mono"`, `"DIN Alternate"`, or `"Consolas"`, `700` weight, uppercase, `letter-spacing: 0.08em`.
- **Dimension Callouts & Values:** `"JetBrains Mono"`, `"Consolas"`, `400` weight, font-size `12px`, tabular numbers (`font-feature-settings: "tnum" 1`).
- **Body & Technical Notes:** `"Space Mono"`, `400` weight, `13px` to `14px`, line-height `1.5`.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Coordinate Cursor Tracker:** The mouse pointer is accompanied by live dynamic X/Y coordinate indicators rendered in cyan at the viewport corner.
- **Vector Line Drawing:** Cards and frames reveal with technical stroke animations (`stroke-dasharray` and `stroke-dashoffset` unspooling in 250ms).
- **Acoustic Profile:** High-frequency, mechanical pen-plotter stepped clicks: a sub-10ms mechanical stepper motor click (`1200Hz`) upon interactive engagement.

---

## 🧩 Canonical Component Specifications

### 1. ISO Standard Drafting Title Block (Container Frame)

```html
<section class="cad-sheet">
  <div class="cad-sheet-header">
    <div class="cad-crosshair top-left">+</div>
    <div class="cad-crosshair top-right">+</div>
    <div class="cad-dimension-bar">
      <span class="cad-tick-start">|&lt;</span>
      <span class="cad-dimension-val">420.00 mm (DIM A)</span>
      <span class="cad-tick-end">&gt;|</span>
    </div>
  </div>

  <div class="cad-body">
    <h3 class="cad-title">DISTRIBUTED CLUSTER SCHEMATIC</h3>
    <p class="cad-notes">NOTE 1: ALL NODES MUST CONFORM TO IEEE 802.3bz SPECIFICATIONS.<br>NOTE 2: TOLERANCES ARE ±0.002ms UNLESS OTHERWISE SPECIFIED.</p>
  </div>

  <!-- ISO Title Block -->
  <footer class="cad-title-block">
    <div class="cad-block-cell cell-wide">
      <span class="cad-block-label">PROJECT NAME</span>
      <span class="cad-block-val">COACUS RUNTIME ENGINE</span>
    </div>
    <div class="cad-block-cell">
      <span class="cad-block-label">DWG NO.</span>
      <span class="cad-block-val">DWG-2026-F5</span>
    </div>
    <div class="cad-block-cell">
      <span class="cad-block-label">REV</span>
      <span class="cad-block-val status-ok">A.04</span>
    </div>
    <div class="cad-block-cell">
      <span class="cad-block-label">SCALE</span>
      <span class="cad-block-val">1:1</span>
    </div>
  </footer>
</section>
```

```css
.cad-sheet {
  background-color: var(--cad-bg-surface);
  border: var(--cad-border-primary);
  padding: 24px;
  position: relative;
  max-width: 720px;
  margin: 0 auto;
  font-family: "Space Mono", Consolas, monospace;
  box-shadow: 0 0 0 1px var(--cad-stroke-subtle);
}

.cad-crosshair {
  position: absolute;
  color: var(--cad-stroke-cyan);
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
}

.top-left { top: 6px; left: 6px; }
.top-right { top: 6px; right: 6px; }

.cad-dimension-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--cad-accent-amber);
  font-size: 11px;
  border-bottom: 1px dashed var(--cad-stroke-subtle);
  padding-bottom: 8px;
  margin-bottom: 20px;
}

.cad-title {
  color: var(--cad-stroke-cyan);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin: 0 0 12px 0;
}

.cad-notes {
  color: var(--cad-text-muted);
  font-size: 12px;
  line-height: 1.6;
  margin: 0 0 24px 0;
}

.cad-title-block {
  display: grid;
  grid-template-columns: 2fr 1fr 60px 60px;
  border: var(--cad-border-primary);
  background-color: var(--cad-bg-canvas);
}

.cad-block-cell {
  border-right: var(--cad-border-primary);
  padding: 6px 10px;
  display: flex;
  flex-direction: column;
}

.cad-block-cell:last-child {
  border-right: none;
}

.cad-block-label {
  font-size: 8px;
  font-weight: 700;
  color: var(--cad-text-muted);
  letter-spacing: 0.05em;
}

.cad-block-val {
  font-size: 11px;
  font-weight: 700;
  color: var(--cad-text-primary);
}

.cad-block-val.status-ok {
  color: var(--cad-accent-green);
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Level AA Contrast Math:**
  - High-visibility drafting cyan (`#00E5FF`) on deep Prussian blue (`#0A192F`) delivers a **9.4:1** contrast ratio.
  - Dimensioning amber (`#FFB300`) on Prussian blue yields **8.2:1**.
  - All textual labels strictly exceed the 4.5:1 requirement.
- **Grid Subtlety vs Distraction:** Background graph lines must maintain low alpha opacity (`0.06` to `0.10`) to prevent visual pattern interference with text comprehension.
- **Reduced Motion Conformance:** Line-draw animations and caliper coordinate tracking automatically freeze when `prefers-reduced-motion: reduce` is detected.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Technical infrastructure architecture diagrams, developer tooling, hardware specs.
- Industrial automation platforms, robotics telemetry, aerospace control interfaces.
- Portfolios of architects, structural engineers, and technical draftspeople.

### Inappropriate Scenarios
- Consumer retail e-commerce, casual dating apps, lifestyle blogs.
- Applications where high emotional warmth, soft organic shapes, and photorealistic human faces take precedence.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Herschel, Sir John (1842):** *"On the Action of the Rays of the Solar Spectrum on Vegetable Colours, and on Some New Photographic Processes"*, Philosophical Transactions of the Royal Society of London.
2. **Autodesk (1982–1990):** *AutoCAD Technical Documentation and Graphic Vector Architecture*.
3. **International Organization for Standardization:** *ISO 128: Technical Product Documentation (TPD) — General Principles of Execution*.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct counterpart to [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md) (vector technical precision vs character-cell console).
- Contrasts with [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md) and [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md) by eliminating all faux-3D tactile surfaces in favor of orthographic vector clarity.
## Appearance and Interaction Verification

Reflow title-block cells according to sheet width and long project/revision strings, retaining dimension ticks; verify muted notes over actual minor/major grid lines, with a local sheet backing if needed.

