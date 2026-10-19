---
name: "ui-style-material-you"
description: "Provides Material Design 3 / Material You (2021-present): Google's dynamic-color design system with HCT tonal palettes, shape and type tokens, tonal elevation and expressive motion, covering the token architecture, material-color-utilities engine, web theming strategy and the dynamic-color trade-offs. Use when implementing M3 theming on the web or in Flutter, or evaluating dynamic color for a product."
---

# UI Style: Material Design 3 (Material You)

> *"Material You rethinks the entire relationship between people and their devices. We are creating an experience that is personal for every style, accessible for every need, alive and adaptive for every screen."*  
> — Matías Duarte, VP of Material Design, Google I/O (May 2021)

Material Design 3 (branded as **Material You**) represents Google's third-generation design language. Radically pivoting from the sterile, rigid white cards of Material 2, Material You introduces personal algorithmic computing: dynamic color extraction from user wallpapers into perceptually uniform **HCT** (Hue-Chroma-Tone) tonal palettes, oversized squircle pill geometry, tonal surface elevation (surface tinting replacing drop shadow stacking), and fluid spring physics.

---

## 🧭 When to Activate

- Designing modern multi-platform web or mobile applications (Flutter, Jetpack Compose, Web Components) aligned with Android 12–15+ design conventions.
- Implementing wallpaper-reactive personalization engines or user-customizable theme palettes derived from a single seed color.
- Upgrading legacy Material Design (M1/M2) web applications to modern CSS custom properties and tokenized design systems.
- Designing touch-friendly, organic interfaces with generous hit targets, fluid pill containers, and state-layer interactions.

---

## 🕰️ Definition, Lineage, and Timeline

- **June 2014 (Material Design 1.0 - "Quantum Paper"):** Matías Duarte unveils Material Design at Google I/O. The system establishes digital paper sheets, Z-axis dp elevation shadows, and floating action buttons (FAB).
- **2018 (Material Design 2.0 - "Google Material"):** A visual refresh standardizes Google Sans, rounded 4dp–8dp corners, and pure white cards with subtle grey strokes.
- **May 18, 2021 (Material You / M3 Announcement):** Unveiled at Google I/O with Android 12 and Pixel 6. Google replaces RGB/HSL theming with the **Monet engine** and HCT color science. The specification officially ships October 27, 2021.
- **May 2024–2025 (Material 3 Expressive):** Google expands M3 with bouncier spring easing curves, asymmetrical card shapes, pill-in-pill nesting, and adaptive layout window classes.

### Absolute Style Vetos (What Material You is NOT)
- ❌ **NOT Material 1 / Flat 2.0 ([ui-style-flat-design](../ui-style-flat-design/SKILL.md)):** No pure white cards floating with multi-tiered black drop shadows. Surfaces must use *tonal surface elevation tinting*.
- ❌ **NOT iOS 7 Thin Minimalism:** No hairline ghost buttons, no ultra-thin 100-weight typography, no rigid rectangular panes. M3 celebrates organic, rounded pill shapes.
- ❌ **NOT Unregulated Rainbow Palettes:** Colors must not be randomly handpicked. They must be generated via algorithmic tonal steps (Tones 10 to 90) ensuring mathematical WCAG contrast pairs.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                               MATERIAL YOU TAXONOMY                                |
+------------------------------------------------------------------------------------+
| M3 Standard (Android 12-14)          | M3 Expressive (2024-2025)                   |
| - Symmetrical squircle containers    | - Asymmetrical corner radii on cards        |
| - Pill Floating Action Button (FAB)  | - Bouncier spring physics on interaction   |
| - Tonal surface tint elevation (1-5) | - Fluid container morphs & expanded badges  |
| - Roboto / Google Sans type scales   | - High-contrast accessible color options    |
+------------------------------------------------------------------------------------+
```

### Visual Pillars
1. **The HCT Color Space:** Blends CAM16 (color appearance model for human color perception) with CIELAB L* (perceptual lightness). Tone directly correlates with luminance regardless of hue, guaranteeing deterministic contrast math.
2. **Tonal Elevation over Drop Shadows:** In dark mode, higher elevation is communicated by blending an increasing percentage of `--md-sys-color-primary` into the surface background, rather than inflating black drop shadows.
3. **Pill & Squircle Geometry:** Corner radii scale generously: XS (`4px`), S (`8px`), M (`12px`), L (`16px`), XL (`28px`), and Full (`9999px` for pill buttons and chips).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Material You replaces physical sun-casting with ambient surface illumination and tonal layers:
- **Tonal Elevation Levels:**
  - Level 0 (Surface Base): Surface tone with 0% tint.
  - Level 1 (Resting Card): Surface + 5% primary color tint (`--md-sys-color-surface-container-low`).
  - Level 2 (Hover Card / FAB): Surface + 8% primary tint (`--md-sys-color-surface-container`).
  - Level 3 (Active Dialog / Drawer): Surface + 11% primary tint (`--md-sys-color-surface-container-high`).
  - Level 4 / 5 (Modal Sheets): Surface + 14% tint (`--md-sys-color-surface-container-highest`).
- **State Layer Opacities:**
  - Hover: `8%` overlay of on-surface token.
  - Focus: `12%` overlay.
  - Press / Ripple: `12%` expanding radial ripple.

---

## 🏷️ Illustrative Design Tokens

These hand-picked OKLCH values illustrate role wiring; they are not an HCT-generated scheme or a contrast guarantee. Generate production roles with the selected engine and verify rendered pairs including state layers.

```css
:root {
  /* Seed Color Anchor: Electric Cobalt (Hue 250, Chroma 48) */
  --md-sys-color-primary: oklch(0.55 0.22 250);
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: oklch(0.88 0.08 250);
  --md-sys-color-on-primary-container: oklch(0.25 0.16 250);

  --md-sys-color-secondary: oklch(0.60 0.08 250);
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: oklch(0.90 0.04 250);
  --md-sys-color-on-secondary-container: oklch(0.28 0.06 250);

  --md-sys-color-tertiary: oklch(0.62 0.15 320);
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: oklch(0.90 0.07 320);
  --md-sys-color-on-tertiary-container: oklch(0.26 0.12 320);

  /* Surface Hierarchy (Light Mode) */
  --md-sys-color-surface: oklch(0.98 0.005 250);
  --md-sys-color-on-surface: oklch(0.18 0.01 250);
  --md-sys-color-surface-container-low: oklch(0.96 0.008 250);
  --md-sys-color-surface-container: oklch(0.94 0.010 250);
  --md-sys-color-surface-container-high: oklch(0.92 0.012 250);

  /* Outline & Shape */
  --md-sys-color-outline: oklch(0.70 0.01 250);
  --md-sys-color-outline-variant: oklch(0.85 0.01 250);

  --md-sys-shape-corner-xs: 4px;
  --md-sys-shape-corner-sm: 8px;
  --md-sys-shape-corner-md: 12px;
  --md-sys-shape-corner-lg: 16px;
  --md-sys-shape-corner-xl: 28px;
  --md-sys-shape-corner-full: 9999px;

  /* Motion Curves */
  --md-sys-motion-easing-emphasized: cubic-bezier(0.2, 0.0, 0.0, 1.0);
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0.0, 0.2, 1.0);
  --md-sys-motion-duration-short: 200ms;
  --md-sys-motion-duration-medium: 350ms;
}

[data-theme="dark"] {
  /* Dark Mode Inversions */
  --md-sys-color-secondary: oklch(0.82 0.06 250);
  --md-sys-color-on-secondary: oklch(0.20 0.04 250);
  --md-sys-color-secondary-container: oklch(0.32 0.06 250);
  --md-sys-color-on-secondary-container: oklch(0.92 0.03 250);
  --md-sys-color-tertiary: oklch(0.82 0.10 320);
  --md-sys-color-on-tertiary: oklch(0.20 0.06 320);
  --md-sys-color-tertiary-container: oklch(0.32 0.10 320);
  --md-sys-color-on-tertiary-container: oklch(0.92 0.04 320);
  --md-sys-color-primary: oklch(0.80 0.12 250);
  --md-sys-color-on-primary: oklch(0.20 0.15 250);
  --md-sys-color-primary-container: oklch(0.35 0.18 250);
  --md-sys-color-on-primary-container: oklch(0.90 0.06 250);

  --md-sys-color-surface: oklch(0.14 0.008 250);
  --md-sys-color-on-surface: oklch(0.92 0.005 250);
  --md-sys-color-surface-container-low: oklch(0.17 0.010 250);
  --md-sys-color-surface-container: oklch(0.20 0.012 250);
  --md-sys-color-surface-container-high: oklch(0.24 0.014 250);

  --md-sys-color-outline: oklch(0.55 0.01 250);
  --md-sys-color-outline-variant: oklch(0.30 0.01 250);
}
```

---

## 🔤 Typography & Lettering Architecture

M3 specifies a rigorous 15-role typographic system:
- **Display (Large / Medium / Small):** `Roboto` or `Google Sans`, `400` weight, `45px` to `64px`, `letter-spacing: -0.02em`.
- **Headline (Large / Medium / Small):** `Roboto`, `400` weight, `24px` to `32px`.
- **Title (Large / Medium / Small):** `Roboto`, `500` weight (Medium), `14px` to `22px`.
- **Body (Large / Medium / Small):** `Roboto`, `400` weight, `12px` to `16px`, line-height `1.5`.
- **Label (Large / Medium / Small):** `Roboto`, `500` weight (Medium), `11px` to `14px`, uppercase or tight for buttons and chips.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **State Layer Architecture:** Every interactive surface renders a dedicated CSS `::before` state overlay layer that shifts from `opacity: 0` to `0.08` (hover), `0.12` (focus), and triggers a radial CSS ripple on press.
- **Container Morphing:** Modal dialogs and detail screens morph outwards directly from the clicked card or FAB using `clip-path` and `--md-sys-motion-easing-emphasized`.
- **Audio Feedback:** Soft organic water-drop acoustic feedback: a warm 12ms pop (`240Hz`) for FAB activations.

---

## 🧩 Canonical Component Specifications

### 1. Extended Floating Action Button (Extended FAB)

```html
<button class="m3-fab-extended">
  <svg class="m3-fab-icon" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
  </svg>
  <span class="m3-fab-label">Create Workflow</span>
</button>
```

```css
.m3-fab-extended {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  height: 56px;
  padding: 0 20px;
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  border: none;
  border-radius: var(--md-sys-shape-corner-lg);
  font-family: Roboto, sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 4px 8px oklch(0 0 0 / 0.15);
  transition: transform var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard),
              box-shadow var(--md-sys-motion-duration-short) var(--md-sys-motion-easing-standard);
  overflow: hidden;
}

.m3-fab-extended::before {
  content: "";
  position: absolute;
  inset: 0;
  background-color: currentColor;
  opacity: 0;
  transition: opacity var(--md-sys-motion-duration-short) ease;
}

.m3-fab-extended:hover::before {
  opacity: 0.08;
}

.m3-fab-extended:hover {
  box-shadow: 0 6px 12px oklch(0 0 0 / 0.20);
  transform: translateY(-1px);
}

.m3-fab-extended:active::before {
  opacity: 0.12;
}

.m3-fab-extended:focus-visible {
  outline: 3px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
```

### 2. Tonal Elevated Card with Pill Action Chip

```html
<article class="m3-card">
  <div class="m3-card-header">
    <span class="m3-chip">Automated Rule</span>
    <h3 class="m3-card-title">Realtime Telemetry Ingestion</h3>
  </div>
  <p class="m3-card-body">Edge sensors stream metrics to regional Kafka clusters with automatic partition rebalancing.</p>
  <div class="m3-card-actions">
    <button class="m3-btn-filled">Configure</button>
    <button class="m3-btn-tonal">View Logs</button>
  </div>
</article>
```

```css
.m3-card {
  background-color: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-xl);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  border: 1px solid var(--md-sys-color-outline-variant);
  transition: background-color var(--md-sys-motion-duration-short) ease;
}

.m3-card:hover {
  background-color: var(--md-sys-color-surface-container-high);
}

.m3-chip {
  display: inline-block;
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--md-sys-shape-corner-sm);
  margin-bottom: 8px;
}

.m3-card-title {
  font-family: Roboto, sans-serif;
  font-size: 20px;
  font-weight: 500;
  margin: 0;
}

.m3-card-body {
  font-family: Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: oklch(from var(--md-sys-color-on-surface) l c h / 0.80);
  margin: 0;
}

.m3-card-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.m3-btn-filled {
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  height: 38px;
  padding: 0 16px;
  border-radius: var(--md-sys-shape-corner-full);
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
}

.m3-btn-tonal {
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  border: none;
  height: 38px;
  padding: 0 16px;
  border-radius: var(--md-sys-shape-corner-full);
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **Generated Tone Pairs:** HCT tone supports contrast reasoning for generated colors. Do not transfer numerical guarantees to unrelated OKLCH samples or translucent state composites; calculate the delivered foreground/background pairs.
- **Dynamic Palette Safeguards:** When extracting colors from arbitrary wallpapers, low-chroma images (grey gravel or beige wood) can produce washed-out palettes. The Monet algorithm injects a minimum chroma floor (Chroma ≥ 48 for Primary) to prevent contrast collapse.
- **Focus Indicators:** Interactive components must display an explicit high-contrast focus ring (`outline: 3px solid var(--md-sys-color-primary); outline-offset: 2px`).

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- Consumer web applications, Android ecosystem tools, Flutter-powered mobile interfaces.
- Personalized apps that let users customize accent hues without breaking accessibility.
- Touch-first responsive designs demanding tactile pill buttons and generous hit boundaries.

### Inappropriate Scenarios
- Strict enterprise B2B apps where fixed corporate brand guidelines prohibit algorithmic color shifting.
- High-density data tables where generous pill radii and 56px FABs waste critical screen real estate.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Google Material Design Team (October 2021):** *"Material Design 3 Official Specification"*, m3.material.io.
2. **Google Open Source:** *"material-color-utilities Library (HCT Color Science and Quantization)"*, github.com/material-foundation/material-color-utilities.
3. **Duarte, Matías & Google Design:** *"Designing Material You"*, Google I/O 2021 Keynote.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Direct successor to [ui-style-flat-design](../ui-style-flat-design/SKILL.md) (Flat 2.0).
- Contrasts with [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md) and [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md) by trading monochrome discipline for organic, playful personalization.
## Appearance and Interaction Verification

Label hand-picked OKLCH values as illustrative rather than HCT-generated guarantees; complete secondary/tertiary/on-state role pairs in requested appearances and verify tinted/ripple layers and chips in rendered states.

