---
name: "color-ui-systems"
description: "Provides color architecture for UI design systems: primitive/semantic/component token layers, role-based naming (M3's 26 roles, on/container/variant grammar), theming (light/dark/brand from one role set), dynamic color and HCT tonal palettes, text/background/border/focus role conventions, status colors, palette generation tooling and how major systems (Material, Apple, Atlassian, Polaris, Primer, Radix, GOV.UK) document color. Use when designing color tokens, theming or a brand-adaptable token layer."
---

# AI Skill: Color in UI Systems

How color becomes architecture: tokens, roles, themes and the conventions that make a palette operable at scale. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing a color token layer or migrating a palette into tokens.
- Building light/dark/brand/high-contrast themes.
- Defining text, surface, border, focus and status role conventions.
- Auditing a design system's color architecture.

---

## 🧱 Token Layers

- **Three layers, universally:** **primitive/base** tokens hold raw values (`color-pink-5`) and exist only to be referenced; **semantic/functional** tokens express UI meaning (`borderColor-accent-emphasis`) and are what components consume; **component** tokens cover component-specific values. Primer forbids using base tokens directly in code.
- **Naming grammar:** Atlassian's `foundation.property.modifier` (`color.icon.success`); Style Dictionary's CTI path (`color.background.button.error`); Primer's `fgColor-*`/`bgColor-*`/`borderColor-*` × roles × intensity (`-muted`, `-emphasis`, `-onEmphasis`, `-inverse`).
- **Rule:** choose tokens by *meaning*, never because a value happens to match — matching by eye breaks other themes.
- **DTCG format** ("Design Tokens Format Module 2025.10", Draft CG Report Sep 2026): JSON with required `$value`, optional `$type` (`color` is defined), `$description`, `$deprecated`, `$extensions`; aliases reference `{color.brand}`; the 2025.10 draft adds mandatory JSON Pointer `$ref` and group `$extends` deep-merge; color values are structured objects (`colorSpace`, `components`, `hex`, `alpha`). Reference translators: Style Dictionary, Terrazzo.

---

## 🎭 Role Grammar (Material 3)

- **26 standard roles in six groups** — primary, secondary, tertiary, error, surface, outline — plus optional add-ons (fixed/fixed-dim, inverse, scrim, shadow) for 45 total.
- **Vocabulary:** **Surface** = low-emphasis backgrounds; **Container** = fills for foreground elements (never text/icons); **On-X** = the color for text/icons on top of X; **-Variant** = lower-emphasis sibling.
- **Emphasis hierarchy:** primary for high-emphasis (key buttons, FAB), secondary for less prominent (filter chips, selected nav), tertiary for small contrasting accents (badges).
- **Contrast is contractual:** role pairs guarantee a minimum **3:1**; M3 supports three user contrast levels. "Paint by number": use published pairings; mixing `primary` with `primary container` text is an explicit don't.

---

## 🌗 Theming

- **One role set, N themes.** A theme is a collection of token *values* (light, dark, high-contrast, brand) bound over the same semantic layer (Atlassian's definition).
- **Light/dark mechanics:** swap custom properties under `prefers-color-scheme`; `color-scheme: light dark` fixes UA controls and scrollbars; `light-dark()` gives compact two-value form (Baseline May 2024). Primer inverts neutral scales between modes so one functional token serves both.
- **Brand theming** = alias re-binding: keep components pointed at semantic tokens and swap the value layer (`$extends` per-brand packs; Tailwind v4 `@theme inline` over `[data-theme]`; Radix mutable aliases). Polaris narrows brand expression to token-driven props (`tone`, `color`, `variant`) and locks custom CSS out — theming authority moved into the platform.
- **Dynamic color (Material You):** source color (wallpaper quantized via Celebi, in-app content, or hand-picked) → five key colors → tonal palettes (tones 0–100) → tone-to-role assignment; error roles stay static. Implement with Material Color Utilities (HCT = CAM16 hue/chroma + CIELAB L\*); theme with Material Theme Builder.
- **Performance:** split per-mode stylesheets behind `<link media>`; use client hints to avoid a flash of the wrong theme.

---

## 🎯 Role Conventions in Practice

- **Text ladder:** default → muted/secondary → disabled → placeholder, plus link (Apple's semantic label ladder; Primer's `fgColor-default/muted/disabled/link`). Contrast banding on scales: Primer text on neutral steps 9–10, high-contrast themes target ≥7:1.
- **Surfaces/elevation:** M3's five surface-container levels for nesting; elevation as color + shadow together; dark mode elevates via lighter overlays.
- **Borders/dividers:** M3's `outline` (important boundaries, 3:1) vs `outline variant` (decorative dividers); Radix steps 6–8 (subtle border, interactive border, stronger hover/focus); Primer steps 7–8.
- **Focus rings:** a dedicated token (GOV.UK's focus yellow reserved exclusively for focus; Primer's `--focus-outlineColor`); Radix focus rings at steps 7–8.
- **Status colors:** error=red, success=green, warning=amber, info=blue across GOV.UK, Primer and Polaris; each needs foreground + background + border variants, and subtle (`muted`) vs solid (`emphasis`) forms for light/dark. Cultural caveat: red/green polarity flips by locale (Apple flips Stocks colors for Chinese).
- **Apple's universal rule:** every color needs light, dark and increased-contrast variants — custom colors must ship all three.

---

## 🛠️ Palette Engineering Toolchain

- Generate, don't hand-pick: perceptual spaces (OKLCH/Oklab; HCT for M3) + tone targets + contrast solvers.
- **Material Theme Builder** (Figma plugin + web) for M3 schemes; **Style Dictionary** for multi-platform token builds; **Tailwind v4 `@theme`** where the `--color-*` namespace *is* the token layer.
- **Escape hatches matter:** keep static schemes available (M3's error-as-static-role) so a broken extraction cannot make a semantic color unusable.
- **Data is not UI:** chart palettes are a separate token family (Primer ships 16 data-viz hues with emphasis/muted variants).

---

## ⚠️ Pitfalls

- Components consuming primitive tokens; value-matching instead of role matching.
- One token set per theme instead of one role set with re-bound values.
- Reassigning semantic status colors mid-flight; custom colors shipped without dark/contrast variants.
- Treating `outline` and `outline variant` as interchangeable.

---

## 📚 Sources

- Material 3, "Color roles" — https://m3.material.io/styles/color/roles
- Material 3, "How the color system works" — https://m3.material.io/styles/color/system/how-the-system-works
- Material 3, "Dynamic color" — https://m3.material.io/styles/color/dynamic-color/overview
- DTCG, "Design Tokens Format Module 2025.10" — https://www.designtokens.org/TR/2025.10/format/
- Atlassian Design System, "Design tokens explained" — https://atlassian.design/foundations/tokens/design-tokens
- Primer, "Color usage" — https://primer.style/product/getting-started/foundations/color-usage/
- Primer, "Color primitives" — https://primer.style/product/primitives/color/
- Radix Colors, "Understanding the scale" — https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
- Apple HIG, "Color" — https://developer.apple.com/design/human-interface-guidelines/color
- Shopify Polaris, "Using web components" — https://shopify.dev/docs/api/polaris/using-polaris-web-components
- GOV.UK Design System, "Colour" — https://design-system.service.gov.uk/styles/colour/
- Thomas Steiner, "prefers-color-scheme", web.dev, 2019 — https://web.dev/articles/prefers-color-scheme
- Thomas Steiner, "Improve dark mode default with color-scheme", web.dev, 2020 — https://web.dev/articles/color-scheme
- Bramus, "CSS color-scheme-dependent colors with light-dark()", web.dev, 2024 — https://web.dev/articles/light-dark
- Material Foundation, "Material Color Utilities" — https://github.com/material-foundation/material-color-utilities

---

## 🔗 Integration with Other Skills

- For the spaces behind the tokens, see [color-theory-foundations](../color-theory-foundations/SKILL.md).
- For contrast guarantees, see [color-contrast-accessibility](../color-contrast-accessibility/SKILL.md).
- For chart palettes, see [color-data-visualization](../color-data-visualization/SKILL.md).
- For token-driven implementation, see [ui-designer](../../../roles/ui-designer/SKILL.md) and [frontend-developer](../../../roles/frontend-developer/SKILL.md).
