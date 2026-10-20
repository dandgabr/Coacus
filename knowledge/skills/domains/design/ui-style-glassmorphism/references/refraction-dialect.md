# Refraction Dialect (Liquid Glass): Depth Reference

Companion to the "Refraction Dialect (Liquid Glass)" subsection of [the glassmorphism skill](../SKILL.md). The body carries the gate; this file carries the lineage, the critique and the web recreation limits.

---

## 1. What Apple Liquid Glass Is

- **Announcement:** Apple introduced Liquid Glass on 2025-06-09 (Apple Newsroom, "Apple introduces a delightful and elegant new software design") as a unified material across iOS 26, iPadOS 26, macOS Tahoe 26, watchOS 26 and tvOS 26.
- **Material model:** A translucent material that refracts (bends) what sits behind it instead of only frosting it, adapts its tint between light and dark surroundings, and carries specular highlights that respond to device motion.
- **Placement:** Apple positions it on the floating functional layer (tab bars, toolbars, sidebars, controls and navigation) above content, not on the content itself. The Human Interface Guidelines wording for this layering was not re-read this session; treat the "controls layer, not content" rule as Coacus guidance derived from the announcement, not a quoted HIG requirement.
- **Difference from frosted glass:** Classic glassmorphism blurs the backdrop uniformly. The refraction dialect displaces backdrop pixels near the edge (a lens rim), keeps the centre comparatively clear and adds a moving specular. Clear centres are exactly what makes text over busy backdrops fragile.

## 2. The Usability Critique

- **NN/g:** Raluca Budiu, "Liquid Glass Is Cracked, and Usability Suffers in iOS 26", Nielsen Norman Group, 2025-10-10. The main findings relevant to web adaptations:
  - Legibility collapses when translucent controls sit over busy or high-contrast content; labels and icons change contrast as content scrolls beneath them.
  - Animated refraction and wobbling highlights attract attention without conveying state ("motion for motion's sake").
  - Controls that blend into content lose their affordance and their grouping.
- **Apple's response:** iOS 26.1 added a Liquid Glass appearance choice of **Clear** (the original translucent look) or **Tinted** (higher opacity, more contrast) in Settings. This toggle is reported by secondary press coverage; the Apple release notes were not re-read this session.
- **Design consequence:** Ship the tinted (more opaque) variant as the default and treat the clear variant as an opt-in, the reverse of most marketing demos.

## 3. Web Recreation and Its Limits

The common technique applies an SVG displacement filter to the backdrop:

```html
<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
  <filter id="lens" color-interpolation-filters="sRGB">
    <!-- map.png: red/green channels encode the x/y offset of each pixel -->
    <feImage href="map.png" result="map" preserveAspectRatio="none" />
    <feDisplacementMap in="SourceGraphic" in2="map" scale="40"
                       xChannelSelector="R" yChannelSelector="G" />
  </filter>
</svg>
```

```css
.refraction-bar {
  /* 1. Opaque default: correct with no filter and no media-query support. */
  background: var(--glass-solid);
  color: var(--glass-ink);
}
@supports (backdrop-filter: blur(1px)) {
  .refraction-bar {
    /* 2. Plain blur: what Firefox and Safari actually render. */
    background: color-mix(in oklch, var(--glass-solid) 72%, transparent);
    backdrop-filter: blur(14px) saturate(160%);
  }
}
/* 3. Refraction: progressive enhancement only, never the sole layer. */
.refraction-bar.is-lens {
  backdrop-filter: url(#lens) blur(6px) saturate(160%);
}
@media (prefers-reduced-transparency: reduce), (forced-colors: active) {
  .refraction-bar, .refraction-bar.is-lens {
    background: var(--glass-solid);
    backdrop-filter: none;
  }
}
```

- **Engine support:** `backdrop-filter: url(#filter)` is reported to render only in Chromium; Firefox and Safari do not render the SVG reference, so depending on the engine the lens is skipped or the whole declaration is dropped. This is unverified: MDN browser-compat-data does not track the `url()` value separately, and the claim rests on secondary articles. Feature detection with `@supports` cannot tell whether the SVG reference renders, so the `.is-lens` class must be opt-in per engine you have tested, with the blur declaration as the cascade fallback.
- **Cost:** Displacement runs on every frame the backdrop changes (scroll, video, animation). Measure on low-end hardware before shipping; drop to the blur on long scrolling surfaces.
- **Live DOM:** SVG filters read the real backdrop, so content stays live. A shader recreation instead samples a captured snapshot and goes stale; see [the GPU graphics skill](../../../../engineering/practices/ui-gpu-graphics-web/SKILL.md) for the refraction and chromatic-dispersion shader path and its fallbacks.
- **Specular motion:** Tie the moving highlight to pointer or scroll only when it carries no information, freeze it under `prefers-reduced-motion: reduce`, and never loop it automatically for more than 5 seconds without a pause control. Canonical motion obligations live in [web accessibility](../../../../engineering/practices/web-accessibility-wcag/SKILL.md).

## 4. Not to Be Confused With

- **[Fluid / liquid morph](../../ui-style-fluid-liquid-morph/SKILL.md):** metaball "goo" where shapes merge and split through blur-plus-contrast or SDF blending. It deforms the element's own shape. Liquid Glass deforms what is behind a fixed-shape control.
- **[Holographic foil](../../ui-style-holographic-foil-iridescent/SKILL.md):** angle-dependent hue shift on an opaque surface; no backdrop sampling.

## 5. Verification Checklist

1. Measure text contrast (4.5:1) and icon or boundary contrast (3:1) over the worst backdrop the control can scroll over: the brightest and darkest frame, and the busiest pattern. A token calculation over the average backdrop is not evidence.
2. Render in Chromium, Firefox and Safari; confirm the non-Chromium result is the intended blur, not a transparent bar.
3. Enable `forced-colors: active` and confirm the control keeps a system-colour border and readable text.
4. Enable reduced transparency where supported (Chrome, Firefox) and confirm the opaque state; on Safari confirm the default is already acceptable without it.
5. Enable reduced motion and confirm the specular freezes.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **Liquid Glass announcement, 2025-06-09** (verified) — https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/
- **NN/g "Liquid Glass Is Cracked", Raluca Budiu, 2025-10-10** (unverified) — the nngroup.com page could not be fetched this session; title, author and date come from the coordinating brief
- **iOS 26.1 Clear/Tinted toggle** (unverified) — secondary press coverage only; Apple release notes not re-read
- **backdrop-filter: url() rendering in Chromium only** (unverified) — only secondary sources; MDN browser-compat-data does not track the `url()` value
- **prefers-reduced-transparency: Chrome 118, Firefox 113, no Safari** (verified) — MDN browser-compat-data 8.1.6 (2026-10-15)
