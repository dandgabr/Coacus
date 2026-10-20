---
name: "ui-style-glassmorphism"
description: "Provides the canonical Glassmorphism & Spatial UI style (2020-present): multi-layered frosted glass surfaces, backdrop-filter optical blur, 1px specular white border highlights, subtle drop shadows, and spatial depth inspired by macOS Big Sur and visionOS. Covers contrast remediation, layered scrim fallbacks, design tokens, and WCAG 2.2 compliance. Use when designing premium fintech dashboards, spatial computing interfaces, or modern operating system shells."
---

# UI Style: Glassmorphism & Spatial UI

**Glassmorphism** is the optical simulation of frosted, translucent glass floating in multi-layered spatial coordinates. Coined in late 2020 by Michał Malewicz following Apple's unveiling of macOS Big Sur (and later crystallized in visionOS), the aesthetic relies on hardware-accelerated background blurring (`backdrop-filter: blur`), multi-layered translucency, a 1px specular white border highlight catching directional light along the top-left rim, and soft diffuse ambient drop shadows.

---

## 🧭 When to Activate

- Designing modern operating system shells, floating navigation overlays, spatial computing windows, or premium consumer fintech dashboards.
- Interfaces with rich, vibrant, or multi-chromatic backgrounds (mesh gradients, 3D scenes, high-res photography) where frosted glass establishes spatial depth without obscuring underlying context.
- Replacing flat, opaque card containers with sophisticated, translucent glass surfaces while strictly enforcing high-contrast text scrims.

---

## 🕰️ Definition, Lineage, and Timeline

- **Precursors & Evolution:** Evolved from Windows Vista/7 *Aero Glass* (2006; heavy gloss, diagonal caustic lines, reflective bevels) and iOS 7 (2013; flat gaussian blur diffusion).
- **Modern Formalization:** Formalized in November 2020 by designer Michał Malewicz to describe the sleek frosted glass interfaces in macOS Big Sur. Elevated to spatial three dimensions with Apple's *visionOS* (2023–2024), where frosted glass dynamically adapts to ambient physical room lighting.
- **Distinctions from Neighboring Styles:**
  - Unlike **Frutiger Aero** (2004–2012: skeuomorphic glossy water bubbles, grass, lens flares, 3D gel buttons), Glassmorphism is minimal, flat, geometric, and relies purely on blur and specular edge refraction.
  - Unlike **Neumorphism** (extruded monochrome clay without borders or distinct backgrounds), Glassmorphism separates foreground from background via optical blur and 1px borders.
  - Unlike **Aura / Mesh Gradient** (the colorful background beneath), Glassmorphism is the refractive lens placed on top of it.
- **Absolute Veto:** Unscrimmed frosted cards with low-contrast gray text on multi-colored moving backgrounds are strictly forbidden. Glass cards must feature an internal dark or light contrast scrim ensuring body text meets WCAG AA (4.5:1).

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                GLASSMORPHISM MATRIX                                    │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. visionOS Spatial Glass  │ 2. macOS Frosted Acrylic   │ 3. Prismatic Specular Glass  │
│ • Adaptive light response  │ • Deep gaussian blur (24px)│ • Subtle chromatic refraction│
│ • Thick translucent slab   │ • 1px solid white hair rim │ • Iridescent edge dispersion │
│ • Soft ambient occlusion   │ • Vibrant gradient backing │ • Directional highlight (45°)│
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Surfaces & Grounds:** Translucent white sheets (`rgba(255, 255, 255, 0.12)` to `0.22`), dark glass variant (`rgba(15, 23, 42, 0.65)`), and vivid multi-stop mesh gradients beneath.
- **Optical Rim Highlights:** 1px directional border gradient (`linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(255, 255, 255, 0.05) 100%)`).
- **Depth & Occlusion:** Deep backdrop blur (12px to 32px), combined with expansive, low-opacity drop shadows (`0 8px 32px rgba(0, 0, 0, 0.18)`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Frosted Optical Diffusion:**
   - Multi-layered CSS backdrop blur paired with semi-transparent background fill.
   ```css
   background: rgba(255, 255, 255, 0.14);
   backdrop-filter: blur(16px) saturate(180%);
   -webkit-backdrop-filter: blur(16px) saturate(180%);
   border: 1px solid rgba(255, 255, 255, 0.25);
   box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.4);
   ```
2. **Dark Smoked Spatial Glass:**
   - Dark mode glass for high-contrast telemetry and video overlays.
   ```css
   background: rgba(15, 23, 42, 0.72);
   backdrop-filter: blur(20px) saturate(160%);
   border: 1px solid rgba(255, 255, 255, 0.12);
   box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2);
   ```

### Refraction Dialect (Liquid Glass)

Apple's **Liquid Glass** (announced 2025-06-09) is a refraction dialect of this style: a translucent material that bends the backdrop at its rim, adapts between light and dark surroundings and carries specular highlights that react to motion. Apple applies it to the floating controls and navigation layer, not to content. NN/g (Raluca Budiu, "Liquid Glass Is Cracked", 2025-10-10) documents the cost: legibility fails over busy content and the motion rarely carries meaning; iOS 26.1 answered with a Clear/Tinted choice. On the web, an SVG `feDisplacementMap` through `backdrop-filter: url(#filter)` renders only in Chromium (unverified), so Firefox and Safari show the plain blur, which must be declared as the fallback. It is not [fluid liquid morph](../ui-style-fluid-liquid-morph/SKILL.md): metaball goo deforms the element's own shape, refraction deforms what lies behind a fixed-shape control.

> **Default: No.**
> **Allowed when:** the surface is the chrome or controls layer only (toolbar, tab bar, floating action), never a reading surface, and its worst-case backdrop has been measured.
> **Evidence required:** text at 4.5:1 and icons or boundaries at 3:1 over the worst backdrop frame; a `forced-colors: active` render; a Firefox or Safari render showing the intended blur.
> **Fallback:** an opaque surface by default, the plain blur where `backdrop-filter` is supported, refraction only as an opt-in enhancement.

Recreation code, engine limits and the verification checklist live in [references/refraction-dialect.md](references/refraction-dialect.md); the shader path (captured background, per-channel dispersion, context-loss fallback) lives in [ui-gpu-graphics-web](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md).

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Translucent Glass Substrates */
  --glass-light-bg: rgba(255, 255, 255, 0.16);
  --glass-light-card: rgba(255, 255, 255, 0.22);
  --glass-dark-bg: rgba(15, 23, 42, 0.72);
  --glass-dark-card: rgba(30, 41, 59, 0.65);

  /* Specular Rim Highlights */
  --glass-rim-highlight: rgba(255, 255, 255, 0.45);
  --glass-rim-subtle: rgba(255, 255, 255, 0.12);
  --glass-border: 1px solid rgba(255, 255, 255, 0.25);

  /* Optical Blurs & Shadows */
  --glass-blur-sm: 8px;
  --glass-blur-md: 16px;
  --glass-blur-lg: 28px;
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  --glass-shadow-dark: 0 16px 48px rgba(0, 0, 0, 0.5);

  /* Typography */
  --glass-font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --glass-font-body: 'Inter', system-ui, sans-serif;
  --glass-text-light: #0F172A;
  --glass-text-dark: #F8FAFC;
  --glass-radius: 16px;
  --glass-reading: rgba(255, 255, 255, 0.94);
  --glass-ink: #0F172A;
  --glass-solid: #FFFFFF;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Modern geometric grotesque (*Inter*, *SF Pro Display*, *Plus Jakarta Sans*) set with tight tracking (-0.02em) and solid contrast.
- **Body & Paragraphs:** High-contrast, neutral system sans (*Inter*, *SF Pro Text*) rendered in deep slate (`#0F172A`) on light glass, or bright snow white (`#F8FAFC`) on dark smoked glass.
- **Scrim Rules:** Never place thin, gray typography directly over translucent panels. Text must sit above an internal contrast scrim (`rgba(255, 255, 255, 0.6)` or `rgba(15, 23, 42, 0.7)`).

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Specular Sweep on Cursor Track:** Glass cards track the pointer dynamically, shifting an internal specular light gradient across the rim (`transform: rotate3d(...)`).
- **Depth Elevation:** On hover, cards elevate along the z-axis (`transform: translateY(-3px) scale(1.01)`), while the backdrop blur intensifies (16px to 24px) and shadow diffuses.
- **Fluid Spring Physics:** Interactive window drags and modal reveals utilize natural spring dynamics (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is detected, 3D tilts and hover elevation are disabled, keeping static frosted glass containers.

---

## 🧩 Canonical Component Specifications

### 1. Frosted Glass Container (`.glass-card`)
A multi-layered spatial card featuring backdrop blur, 1px specular rim, and internal text scrim.
```html
<article class="glass-card">
  <div class="glass-card-header">
    <span class="glass-badge">Spatial Compute</span>
    <h3 class="glass-title">Hardware Telemetry</h3>
  </div>
  <p class="glass-text">Neural engine throughput sustained at 18.4 TFLOPS across optical lanes.</p>
</article>
```
The card uses a dense reading layer over its glass substrate. A host dark appearance maps `--glass-reading` to `rgba(15,23,42,.96)`, `--glass-ink` to `#F8FAFC` and `--glass-solid` to `#0F172A`; verify both over the intended backdrop.
```css
.glass-card {
  background: linear-gradient(var(--glass-reading), var(--glass-reading)), var(--glass-light-bg);
  backdrop-filter: blur(var(--glass-blur-md)) saturate(180%);
  -webkit-backdrop-filter: blur(var(--glass-blur-md)) saturate(180%);
  border: 1px solid var(--glass-rim-subtle);
  border-top-color: var(--glass-rim-highlight);
  border-left-color: var(--glass-rim-highlight);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.35);
  padding: 1.75rem;
  color: var(--glass-ink);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
@supports not (backdrop-filter: blur(1px)) {
  .glass-card { background: var(--glass-solid); }
}
.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
```

### 2. Glass Action Button (`.glass-btn`)
An interactive action button finished in frosted white with crisp specular rim.
```css
.glass-btn {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: var(--glass-ink);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 9999px;
  padding: 0.7rem 1.6rem;
  font-family: var(--glass-font-display);
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.6);
  transition: background 0.15s ease, transform 0.15s ease;
}
.glass-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-1px);
}
```

### 3. Spatial Floating Tab Bar (`.glass-tabs`)
A floating navigation pill centered at the viewport base with deep gaussian blur.

### 4. Prismatic Status Indicator (`.glass-indicator`)
A small glowing orb featuring chromatic dispersion along its specular glass perimeter.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **The Background-Bleed Danger:** In pure glassmorphism, background colors and image patterns bleed through the card, potentially causing contrast to drop below 3:1.
- **Mandatory Scrim Fallback (WCAG 1.4.3):** Every text-bearing glass element must maintain an opaque or high-density fallback scrim layer behind typography ensuring body text meets 4.5:1 at all times.
- **Browser Fallback (`@supports`):** For browsers that do not support `backdrop-filter`, provide an opaque solid fallback (`background: #FFFFFF` in light mode or `#1E293B` in dark mode).
- **Worst-Backdrop Contrast (1.4.3, 1.4.11):** Measure the rendered composite over the brightest, darkest and busiest backdrop the surface can sit or scroll over, not the average. Text needs 4.5:1, icons and control boundaries 3:1.
- **Reduced Transparency:** `prefers-reduced-transparency: reduce` ships in Chrome 118 and Firefox 113 but not in Safari, so the media query can only remove translucency, never add legibility. Make the opaque or high-density surface the default and layer translucency on top:
  ```css
  @media (prefers-reduced-transparency: reduce) {
    .glass-card, .glass-btn { background: var(--glass-solid); backdrop-filter: none; }
  }
  ```
- **Forced Colors:** Under `forced-colors: active` the browser drops backgrounds, gradients and shadows, so the rim highlight and blur disappear. Keep a real `border` (it maps to a system colour) and avoid `forced-color-adjust: none` on text-bearing glass.
- **Focus Rings:** High-visibility solid outline with 2px offset (`outline: 2px solid #0284C7; outline-offset: 3px;`).
- **Motion:** Specular sweeps and tilt are decorative; motion obligations (pause controls, reduced motion as house policy) follow the canonical [web accessibility](../../../engineering/practices/web-accessibility-wcag/SKILL.md) skill.

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Spatial operating system shells, floating overlays, audio/video controls, and HUD window frames.
- Premium consumer applications, modern digital bank cards, and personal portfolio hero banners.
- Controlled environments with rich background imagery that benefits from spatial depth.

### Anti-Patterns & Prohibitions
- Text-heavy documentation wikis, books, or dense administrative spreadsheet tables.
- Mobile sites designed for low-power devices with weak GPU hardware (backdrop-filter causes severe battery drain and frame drops).
- Low-contrast gray text floating directly over vibrant, moving photo backgrounds without a scrim.

---

## 📚 Authoritative Sources & Historical Artifacts

- Michał Malewicz, "Glassmorphism in user interfaces", *UX Collective*, Nov 2020.
- Apple Inc., *macOS Big Sur Human Interface Guidelines*, 2020.
- Apple Inc., *Designing for visionOS*, WWDC 2023.
- Adrian Bece, "CSS Backdrop Filter: A Guide", *CSS-Tricks*, 2021.
- Apple Newsroom, "Apple introduces a delightful and elegant new software design", 2025-06-09 (Liquid Glass).
- Raluca Budiu, "Liquid Glass Is Cracked, and Usability Suffers in iOS 26", *Nielsen Norman Group*, 2025-10-10.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Material Styles:** [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
- **Gradient & Optical Peers:** [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-holographic-foil-iridescent](../ui-style-holographic-foil-iridescent/SKILL.md), [ui-style-frutiger-aero](../ui-style-frutiger-aero/SKILL.md).
- **Refraction Neighbours:** [ui-style-fluid-liquid-morph](../ui-style-fluid-liquid-morph/SKILL.md) (metaball goo, a different technique), [ui-gpu-graphics-web](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md) (refraction and dispersion shaders).
- **Pointer & Timing Mechanics:** cursor-tracked specular sweep and 3D tilt in [pointer-and-gesture.md](../ui-motion-interaction/references/pointer-and-gesture.md); spring presets and duration tokens for elevation and modal reveals in [motion-timing-engines.md](../ui-motion-interaction/references/motion-timing-engines.md).
## Appearance and Interaction Verification

Add an explicit reading scrim to the example and pair its ink with light/dark glass; verify the composite over changing backdrop and the opaque no-backdrop-filter fallback, retaining frosted rim and spatial depth around the reading field.

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **Liquid Glass announcement, 2025-06-09** (verified) — https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/
- **NN/g "Liquid Glass Is Cracked", 2025-10-10** (unverified) — the nngroup.com page could not be fetched this session; citation comes from the coordinating brief
- **iOS 26.1 Clear/Tinted toggle** (unverified) — secondary press coverage only; Apple release notes not re-read
- **backdrop-filter: url() rendering in Chromium only** (unverified) — only secondary sources; MDN browser-compat-data does not track the `url()` value
- **backdrop-filter Baseline 2024; prefers-reduced-transparency Chrome 118, Firefox 113, no Safari** (verified) — web-features 3.43.0 and MDN browser-compat-data 8.1.6 (2026-10-15)
