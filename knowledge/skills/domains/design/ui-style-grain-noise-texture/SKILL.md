---
name: "ui-style-grain-noise-texture"
description: "Provides the grain / noise texture UI style (2020s revival of a film-era look): a fine stochastic overlay that breaks digital flatness, covering SVG feTurbulence noise, grainy gradients, blend-mode layering, performance budgets and contrast safety. Use when adding tactile, analog warmth to flat or gradient surfaces without hurting legibility or rendering cost."
---

# UI Style: Grain and Noise Texture

A fine, random speckle laid over color, gradients and imagery so surfaces read as printed, photographed or analog rather than perfectly smooth. The look borrows from photographic film grain and Perlin-style procedural noise; on the web it is almost always generated, not shipped as a large bitmap. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Flat or gradient UI feels sterile and needs tactile warmth ("anti-AI-slop" texture pass).
- Gradients show banding and need dithering that disappears gracefully.
- Building hero backdrops, cards or posters with analog, risograph or film-stock character.

---

## 🕰️ Definition and Timeline

- Film grain is "the random optical texture of processed photographic film", caused by silver particles or dye clouds; larger crystals mean higher sensitivity and more visible grain (Wikipedia).
- Procedural noise: Ken Perlin created Perlin noise in 1982 to escape the machine-like look of CGI. SVG's `feTurbulence` (Baseline since July 2015) exposes Perlin turbulence to CSS authors.
- Web trend: Jimmy Chion's CSS-Tricks "Grainy Gradients" (13 Sep 2021) popularized noise under a gradient plus brightness/contrast boost.
- Distinct from [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md): grain is a global surface treatment on any palette; risograph is a spot-color print simulation with misregistration. Distinct from [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md): texture here is stochastic, not sculpted soft shadow.

---

## 🎨 Visual DNA

- **Noise:** monochrome fractal noise at 0.6-0.9 base frequency for fine grain; 3-4 octaves; low opacity (4-12%).
- **Color:** muted or warm bases (cream, ink, dusty hue) so grain reads as paper or film, not static.
- **Gradients:** wide soft gradients with dithered edges; grain hides banding.
- **Imagery:** photos with matching grain so UI and photography share one material.
- **Type:** high-contrast, confident display faces; grain is applied beneath text, never to it.

---

## 🖱️ Interaction and Motion

- Default state is static. A slow "film flicker" (step-timed seed or 2-4px background-position jumps at 8-12 fps) is optional flavor for hero areas only.
- Never animate grain over text or controls; never tie grain to scroll or pointer movement at 60fps.
- Under `prefers-reduced-motion: reduce`, freeze the grain completely.

---

## 🛠️ Implementation Notes

```html
<svg width="0" height="0" aria-hidden="true" focusable="false">
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch" seed="7"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</svg>
```

```css
.grain { position: relative; isolation: isolate; }
.grain::after {
  content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  filter: url(#grain); opacity: .08; mix-blend-mode: multiply;
}
@media (prefers-reduced-motion: reduce) { .grain::after { animation: none; } }
```

- Prefer one fixed overlay for the page or per section; avoid a filter on every card.
- Pre-render the noise to a small tiling PNG/WebP (128-256px) when filter cost is measured too high on low-end devices.
- Keep text above the overlay in stacking order; use `isolation: isolate` to contain blend modes.

---

## ♿ Accessibility

- 1.4.3 Contrast (Minimum) and 1.4.11 Non-text Contrast: measure text and control contrast against the darkest and lightest grain speckles, not the base color.
- 1.4.12 Text Spacing and 1.4.4 Resize Text: heavy grain under small or light weights hurts legibility; keep body text on a flat, grain-free plate.
- Grain overlay must not intercept input (`pointer-events: none`) and must not cover focus rings (2.4.11 Focus Not Obscured).
- Flicker animation: honor `prefers-reduced-motion`; avoid any flashing above three times per second.
- High-contrast / forced-colors modes: disable the overlay (`@media (forced-colors: active)`).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** editorial, portfolio, music, food, craft and brand pages; hero backdrops; poster-like cards.
- **Caution:** data dashboards and long-form reading (restrict to chrome and headers).
- **Avoid:** dense tables, low-power devices without a pre-rendered fallback, medical or financial detail views.

---

## ⚠️ Pitfalls

- Grain opacity too high turns into visible dirt and fails contrast.
- Full-viewport SVG filters repainted on scroll cause jank and battery drain.
- Blend modes create stacking contexts and unexpected clipping.
- Compression: JPEG/WebP smooth grain away or bloat file size; test the delivered asset.
- Applying the same grain to everything flattens hierarchy; vary it by surface.

---

## 📚 Sources

- Jimmy Chion, "Grainy Gradients" (CSS-Tricks), 13 Sep 2021 — https://css-tricks.com/grainy-gradients/
- MDN Web Docs, "<feTurbulence> SVG filter primitive" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence
- MDN Web Docs, "mix-blend-mode" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode
- Wikipedia, "Film grain" (Wikimedia) — https://en.wikipedia.org/wiki/Film_grain
- Wikipedia, "Perlin noise" (Wikimedia) — https://en.wikipedia.org/wiki/Perlin_noise
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", Recommendation 12 Dec 2024 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-risograph-zine](../ui-style-risograph-zine/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
