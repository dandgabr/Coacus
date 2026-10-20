---
name: "ui-style-linear-saas"
description: "Provides the Linear-style SaaS UI style (2019-present): dark-first, low-chroma neutrals, perceptually uniform theming, tight Inter typography, subtle borders and keyboard-driven density, covering LCH-based theme generation, three-variable theming, soft glow accents and speed as aesthetic. Use when designing modern B2B SaaS product UI and marketing pages that signal craft, focus and performance."
---

# UI Style: Linear SaaS

> *"Speed is not just a feature; it is an aesthetic and a promise of respect for the operator's attention."*  
> — Karri Saarinen, Linear Co-Founder & Head of Design

Linear SaaS defines the high-craft product aesthetic of the 2020s: dark-first, low-chroma neutrals, perceptually uniform color spaces (LCH/OKLCH), tight Inter typography, hairline borders, structural radial glows, and hyper-responsive keyboard workflows.

---

## 🧭 When to Activate

- Designing developer tools, issue trackers, workflow automation engines, and data consoles where density and operational velocity dominate.
- Building unified dark/light themes derived algorithmically from minimal seed inputs (base hue, accent chroma, contrast multiplier).
- Architecting keyboard-first web applications featuring universal command palettes (`Cmd/Ctrl+K`), instant single-key actions, and zero-latency visual feedback.
- Auditing SaaS applications suffering from "cargo-cult dark mode" that fail WCAG contrast ratios or exhibit sluggish, over-animated micro-interactions.

---

## 🕰️ Definition, Lineage, and Timeline

- **2019–2020 (The Genesis):** Karri Saarinen and Tuomas Artman found Linear after leading design and engineering at Airbnb and Uber. They react against bloated enterprise software (Jira, Salesforce), establishing a bespoke Electron/web stack with sub-50ms UI responses, near-black canvases, and purple/indigo focus accents.
- **March 28, 2024 (UI Redesign Part II):** Linear publishes its landmark redesign monograph. The system transitions to perceptually uniform LCH color science, shrinking theme variables from 98 bespoke definitions down to 3 algorithmic anchors: `base`, `accent`, and `contrast`. Headings adopt `Inter Display` with tight negative tracking, while surface borders are standardized to 1px low-alpha hairlines.
- **Aesthetic Proliferation (2021–Present):** The "Linear Look" becomes the visual lingua franca of Silicon Valley devtools (Vercel, Supabase, Raycast, Clerk).

### Absolute Style Vetos (What Linear SaaS is NOT)
- ❌ **NOT Aurora / Glassmorphism Spectacle:** Glowing gradients are structural and localized (soft 5-10% opacity backdrop behind primary heroes), never decorative neon washes or heavily frosted glass surfaces.
- ❌ **NOT Playful Neo-Brutalism:** Zero heavy 2px-3px black borders, zero 100% hard offset drop shadows, zero novelty stickers or tilted badges.
- ❌ **NOT Generic AI Template:** No pastel gradient cards with floating sparkle icons, no ungrounded float cards, no arbitrary spring bounces.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
+------------------------------------------------------------------------------------+
|                               LINEAR SAAS TAXONOMY                                 |
+------------------------------------------------------------------------------------+
| Product Workspace (Dense)            | Marketing & Launch (Atmospheric)            |
| - 12px-14px tabular data rows         | - Large product canvas with inner glow      |
| - Monochromatic semantic badges       | - Subtle radial background spotlight (10%)  |
| - Hairline 1px borders (8% white)     | - Bento feature grid with squircle bounds   |
| - Universal Cmd+K command palette     | - Hero typography in Inter Display (-0.03em)|
+------------------------------------------------------------------------------------+
```

### Aesthetic Pillars
1. **Speed as Aesthetic:** Instantaneous state transitions (<150ms ease-out). No sluggish spring physics; optimistic UI updates ensure the interface never makes the user wait.
2. **Perceptually Uniform Lightness:** Surfaces are stepped strictly by luminance delta (OKLCH lightness: 0.14 -> 0.18 -> 0.22), ensuring consistent contrast irrespective of monitor gamma.
3. **Hairline Precision:** Structural panels are demarcated by 1px borders rendered at `rgba(255, 255, 255, 0.08)` on dark modes, reinforced by 1px subtle top highlights simulating directional light.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

Linear SaaS constructs depth through an architectural dark room model rather than ambient drop shadows:
- **Light Source:** High zenith, low diffusion. Key light hits the top edge of cards, generating a 1px pseudo-inset border (`inset 0 1px 0 rgba(255, 255, 255, 0.12)`).
- **Surface Step:**
  - Base Viewport: `oklch(0.14 0.005 270)`
  - Elevated Container / Sidebar: `oklch(0.17 0.006 270)`
  - Active Card / Popover: `oklch(0.21 0.008 270)`
  - Hover Surface: `oklch(0.24 0.010 270)`
- **Atmospheric Glow:** Linear marketing sections apply a single radial light pool positioned behind the primary artifact: `radial-gradient(ellipse 60% 40% at 50% -20%, oklch(0.55 0.18 275 / 0.15), transparent 70%)`.

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Light Theme Archetype */
  --linear-bg-canvas: oklch(0.99 0.002 270);
  --linear-bg-subtle: oklch(0.96 0.004 270);
  --linear-bg-surface: oklch(0.98 0.003 270);
  --linear-bg-hover: oklch(0.93 0.006 270);
  --linear-bg-active: oklch(0.90 0.008 270);

  --linear-border-hairline: oklch(0.20 0.01 270 / 0.08);
  --linear-border-strong: oklch(0.20 0.01 270 / 0.18);
  --linear-border-focus: oklch(0.58 0.22 275);

  --linear-text-primary: oklch(0.18 0.01 270);
  --linear-text-secondary: oklch(0.46 0.02 270);
  --linear-text-muted: oklch(0.60 0.01 270);

  --linear-accent: oklch(0.56 0.22 275);
  --linear-accent-hover: oklch(0.50 0.24 275);
  --linear-accent-subtle: oklch(0.56 0.22 275 / 0.12);

  /* Status Tones (Restrained Chroma) */
  --linear-status-todo: oklch(0.55 0.02 270);
  --linear-status-progress: oklch(0.68 0.16 60);
  --linear-status-done: oklch(0.60 0.18 150);
  --linear-status-canceled: oklch(0.55 0.02 270);

  /* Geometry & Timing */
  --linear-radius-sm: 4px;
  --linear-radius-md: 6px;
  --linear-radius-lg: 10px;
  --linear-radius-xl: 14px;
  --linear-transition-fast: 120ms cubic-bezier(0.16, 1, 0.3, 1);
  --linear-transition-normal: 180ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="dark"] {
  /* Dark Theme Archetype (Canonical) */
  --linear-bg-canvas: oklch(0.14 0.005 270);
  --linear-bg-subtle: oklch(0.16 0.006 270);
  --linear-bg-surface: oklch(0.19 0.007 270);
  --linear-bg-hover: oklch(0.23 0.009 270);
  --linear-bg-active: oklch(0.27 0.012 270);

  --linear-border-hairline: oklch(0.98 0 0 / 0.08);
  --linear-border-strong: oklch(0.98 0 0 / 0.16);
  --linear-border-focus: oklch(0.68 0.20 275);

  --linear-text-primary: oklch(0.96 0.003 270);
  --linear-text-secondary: oklch(0.70 0.010 270);
  --linear-text-muted: oklch(0.50 0.010 270);

  --linear-accent: oklch(0.66 0.20 275);
  --linear-accent-hover: oklch(0.72 0.18 275);
  --linear-accent-subtle: oklch(0.66 0.20 275 / 0.15);

  --linear-card-highlight: inset 0 1px 0 0 oklch(1 0 0 / 0.10);
  --linear-card-shadow: 0 4px 20px -2px oklch(0 0 0 / 0.50);
}
```

---

## 🔤 Typography & Lettering Architecture

Linear uses the **Inter** family exclusively, leveraging OpenType variable features:
- **Heading 1 / Display:** Inter Display or Inter tight, `700` weight, letter-spacing `-0.035em`, line-height `1.1`.
- **Heading 2 / Section Titles:** Inter, `600` weight, letter-spacing `-0.02em`, line-height `1.25`.
- **UI Body & Row Data:** Inter, `450` or `500` weight, font-size `13px`, letter-spacing `-0.008em`, line-height `1.4`.
- **Keybindings & Numeric Telemetry:** Inter with `font-feature-settings: "cv05" 1, "tnum" 1, "calt" 1`, font-size `11px`, `600` weight.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Action Latency:** Keypress or click triggers an immediate state update. Network calls resolve in the background (optimistic replication).
- **Row Hover Action:** Hovering an issue row exposes subtle contextual action buttons (assignee picker, priority toggle) that are hidden by default to keep visual clutter at near-zero.
- **Micro-Animations:** Height collapses and drawer slides adhere strictly to `cubic-bezier(0.16, 1, 0.3, 1)` within a 150ms-200ms window.
- **Sound:** Near-silent tactile feedback. If audio feedback is enabled, it uses sub-30ms muffled wooden percussive clicks for task completions (`320Hz` sine blip).

---

## 🧩 Canonical Component Specifications

### 1. Issue List Item with Status & Shortcut Key

```html
<div class="linear-issue-row">
  <div class="linear-issue-status done" aria-label="Status: Done">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M4.5 7L6 8.5L9.5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
  </div>
  <span class="linear-issue-id">ENG-4209</span>
  <span class="linear-issue-title">Refactor LCH color palette generator to OKLCH tokens</span>
  <div class="linear-issue-metadata">
    <span class="linear-badge">Optimization</span>
    <kbd class="linear-kbd">C</kbd>
  </div>
</div>
```

```css
.linear-issue-row {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 36px;
  padding: 0 12px;
  background: var(--linear-bg-surface);
  border-bottom: 1px solid var(--linear-border-hairline);
  color: var(--linear-text-primary);
  font-size: 13px;
  cursor: pointer;
  transition: background var(--linear-transition-fast);
}

.linear-issue-row:hover {
  background: var(--linear-bg-hover);
}

.linear-issue-id {
  font-size: 12px;
  color: var(--linear-text-muted);
  font-feature-settings: "tnum" 1;
  font-weight: 500;
}

.linear-issue-title {
  flex: 1;
  font-weight: 450;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.linear-kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  font-family: inherit;
  font-size: 10px;
  font-weight: 600;
  color: var(--linear-text-muted);
  background: var(--linear-bg-subtle);
  border: 1px solid var(--linear-border-hairline);
  border-radius: var(--linear-radius-sm);
}
```

### 2. Universal Command Palette (`Cmd+K`) Container

```html
<div class="linear-modal-backdrop">
  <div class="linear-palette" role="dialog" aria-modal="true" aria-label="Command Menu">
    <div class="linear-palette-input-wrap">
      <svg class="linear-palette-search-icon" width="16" height="16" viewBox="0 0 16 16"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M11 11L14.5 14.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      <input type="text" class="linear-palette-input" placeholder="Type a command or search..." autofocus />
      <span class="linear-kbd">ESC</span>
    </div>
    <ul class="linear-palette-list" role="listbox">
      <li class="linear-palette-item active" role="option" aria-selected="true">
        <span>Change status...</span>
        <span class="linear-palette-hint">S</span>
      </li>
      <li class="linear-palette-item" role="option" aria-selected="false">
        <span>Assign to me</span>
        <span class="linear-palette-hint">I</span>
      </li>
    </ul>
  </div>
</div>
```

```css
.linear-modal-backdrop {
  position: fixed;
  inset: 0;
  background: oklch(0 0 0 / 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 15vh;
  z-index: 1000;
}

.linear-palette {
  width: 100%;
  max-width: 580px;
  background: var(--linear-bg-surface);
  border: 1px solid var(--linear-border-strong);
  border-radius: var(--linear-radius-lg);
  box-shadow: var(--linear-card-shadow), var(--linear-card-highlight);
  overflow: hidden;
}

.linear-palette-input-wrap {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  gap: 10px;
  border-bottom: 1px solid var(--linear-border-hairline);
}

.linear-palette-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--linear-text-primary);
  font-size: 14px;
}
```

---

## ♿ Accessibility & Environmental Contrast

- **WCAG 2.2 Level AA / AAA Conformance:**
  - `var(--linear-text-primary)` over `var(--linear-bg-canvas)` delivers an **11.2:1** contrast ratio.
  - Secondary text (`--linear-text-secondary`) maintains **4.8:1** (exceeding 4.5:1 required for 13px UI typography).
  - Placeholder / muted labels must not drop below **3.2:1** for large labels or **4.5:1** for critical informational text.
- **Keyboard Trapping & Single-Key Remapping:** Universal shortcuts (`C`, `S`, `I`) must be automatically disabled when focus lands on input fields and must offer user remapping to conform to **WCAG 2.1.4**.
- **Reduced Motion:** When `prefers-reduced-motion: reduce` is detected, all command palette drop-downs and list item state changes resolve in `0ms`.

---

## ✅ When to Use / ❌ When to Avoid

### Appropriate Scenarios
- High-frequency operator interfaces, engineering task managers, incident management platforms, code review engines.
- Desktop-first web apps that demand high screen efficiency, rich keyboard accelerators, and minimal cognitive strain during prolonged 8-hour sessions.

### Inappropriate Scenarios
- Youth-oriented consumer social apps, playful educational platforms, or brands requiring high emotional warmth.
- Public e-commerce stores requiring maximal visual excitement and broad retail accessibility across variable budget mobile screens.

---

## 📚 Authoritative Sources & Historical Artifacts

1. **Linear Design Team Monograph (March 2024):** *"Re-designing the Linear UI: Part II — Color System, LCH, and Speed as Philosophy"*, linear.app/blog.
2. **Saarinen, Karri:** *"Building Software with Taste and Speed"*, Config 2023 Keynote.
3. **Matteson, Steve & Inter Authors (Rasmus Andersson):** *"Inter Font Family Variable Design Specification"*, rsms.me/inter.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- Complements [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md) by providing the concrete high-craft execution framework.
- Contrasts with [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md) and [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md) by prioritizing surgical restraint and zero-lag performance over physical hyperbole.
- Takes its duration bands, easing curves and zero-bounce spring presets from [motion-timing-engines.md](../ui-motion-interaction/references/motion-timing-engines.md).
## Appearance and Interaction Verification

Retain compact issue rows but expose complete ellipsized titles and keyboard actions; bound the palette to usable height with scrollable results and verify light/dark muted labels and focus in the actual surface stack.
