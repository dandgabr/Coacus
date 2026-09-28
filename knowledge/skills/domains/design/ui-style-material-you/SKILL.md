---
name: "ui-style-material-you"
description: "Provides Material Design 3 / Material You (2021-present): Google's dynamic-color design system with HCT tonal palettes, shape and type tokens, tonal elevation and expressive motion, covering the token architecture, material-color-utilities engine, web theming strategy and the dynamic-color trade-offs. Use when implementing M3 theming on the web or in Flutter, or evaluating dynamic color for a product."
---

# UI Style: Material Design 3 (Material You)

Google's third-generation design system: dynamic color extracted from the user's wallpaper into HCT tonal palettes, token-driven type/shape scales, tonal elevation and expressive spring motion. Unveiled at Google I/O (May 18, 2021) with Android 12; spec released October 27, 2021; "Material 3 Expressive" announced May 2025. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Implementing M3 theming on the web (CSS tokens) or in Flutter/Android.
- Building wallpaper-reactive personalization or tonal palette systems.
- Migrating a Material 2 app to M3 tokens and shape/motion scales.

---

## 🕰️ Definition and Timeline

- Material 1: I/O, June 25, 2014 (Quantum Paper; Matías Duarte). Material 2 refresh 2018. **M3/Material You:** Android 12 preview May 18, 2021; Pixel 6 flagship; Google apps retrofitted 2021. M3 Expressive (May 2025) adds bouncier springs; rollout to Pixel 6+ from September 2025.
- Web note: the MDC-Web component library froze around v14 (April 2022); Flutter and Jetpack Compose carry the system forward.

---

## 🎨 Visual DNA

- **Color:** wallpaper quantization (Celebi algorithm) → core palettes → **tonal palettes** (tones 0–100, constant hue/chroma) → light/dark/high-contrast schemes, in the **HCT space** (hue-chroma-tone, CAM16 × CIELAB L\*) for perceptual consistency.
- **Type:** 15-role type scale (display/headline/title/body/label); Roboto default; Google Sans for Google products.
- **Shape:** shape-scale tokens (extra-small → extra-large, large ≈ 28px radius; pill buttons/cards/sheets/FAB).
- **Depth:** tonal elevation replaces shadow stacking in dark mode (surface-tint blend); fewer drop shadows than M2.
- **Icons:** Material Symbols with variable axes (weight/fill/grade/optical size); **layout:** 4/8dp grid, compact/medium/expanded window classes, large top-app bars.

---

## 🖱️ Interaction and Motion

- State-layer ripples, container morph/shape transitions, icon morphing; M3 Expressive adds springy emphasized easing and bouncier curves; predictive back and swipe dismissal.

---

## 🛠️ Implementation Notes

- Reference engine: `material-color-utilities` (Apache-2.0) — `hct`, `TonalPalette`/`CorePalette`, `dynamiccolor`, `quantize` (Celebi = Wu + WSMeans), `score`, `contrast`, `dislike` modules.
- Web theming: CSS custom properties for scheme roles (`--md-sys-color-primary` etc.); swappable `[data-theme]` maps; `color-scheme: light dark`; Material Theme Builder (Figma plugin + web) exports tokens.
- Android: `dynamicLightColorScheme(context)`; Flutter: `dynamic_color` package. Use `contrast` utilities to enforce ≥3:1 / ≥4.5:1 tone pairings; `harmonize` to blend brand hues with dynamic sources.

---

## ♿ Accessibility

- Low-contrast pastel primary variants are a known risk — mitigate via contrast tokens; dynamic color can wash out palettes at low chroma; verify text roles against the *generated* scheme, not the brand source palette.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** consumer Android/Flutter apps, products wanting personalization, design-system-driven web apps.
- **Avoid:** brands needing strict fixed identity (dynamic color overrides brand hue — mitigate with `harmonize`/fixed tonal sources); data-dense enterprise tools where expressive motion costs focus.

---

## ⚠️ Pitfalls

- Non-reproducible screenshots for brand review; perceived wash-out at low chroma; OEM fragmentation (M2/M3 mixed); web support second-class after MDC-Web froze.

---

## 📚 Sources

- Material Design 3 specification (color system, dynamic color), Google, 2021–present — https://m3.material.io
- Dave Burke, "A dozen things to love in Android 12", The Keyword, Oct 19, 2021 — https://blog.google/products/android/android-12/
- "Material Design", Wikipedia — https://en.wikipedia.org/wiki/Material_Design
- Material Color Utilities, material-foundation, GitHub — https://github.com/material-foundation/material-color-utilities
- "The Science of Color & Design", Material Design blog — https://m3.material.io/blog/science-of-color-design
- Dieter Bohn, "Android 12 preview", The Verge, May 18, 2021 — https://www.theverge.com/22439777/android-12-design-features-widgets-first-look-google
- Google, "Material 3 Expressive" announcement, May 13, 2025 — https://blog.google/products/android/material-3-expressive-android-wearos-launch/

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md).
- For design-system architecture, see [ui-ux-principles](../../../engineering/practices/ui-ux-principles/SKILL.md).
