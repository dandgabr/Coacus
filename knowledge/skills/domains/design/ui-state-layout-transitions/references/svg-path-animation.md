# SVG Path Animation: Morphing and Line Drawing

Two distinct techniques share this file. **Morphing** interpolates a path's geometry from one shape to another. **Line drawing** reveals a stroke along its length. Both repaint the SVG every frame (neither is compositor-only), so keep the animated paths small and few. Durations use the canonical `--motion-*` tokens defined in [motion-timing-engines.md](../../ui-motion-interaction/references/motion-timing-engines.md).

---

## Morphing

### CSS `d: path()`

```css
.icon path {
  d: path("M4 12 L10 18 L20 6");            /* check */
  transition: d var(--motion-state) var(--ease-enter);
}
.icon[data-state="closed"] path {
  d: path("M6 6 L12 12 L18 18");            /* same command count and types */
}
```

- Interpolation works only when both paths have the **identical command structure**: same number of commands, same command letters in the same order, same arc flags. Otherwise the value flips discretely at the midpoint.
- Normalise paths in the design tool or with a script: convert to absolute cubic Béziers (`C`) and pad the shorter path with zero-length segments.
- Support: Chrome 52 and Firefox 97 animate `d`. Safari parses the property but it has no effect (MDN BCD), so Safari shows the initial path and never changes. Base path for Safari: swap two `<path>` elements with an opacity cross-fade, or use a JS morph.

Because Safari parses `d`, `@supports (d: path("M0 0"))` still matches there and cannot detect the gap. Keep the state legible without the morph: both end shapes must be meaningful on their own, and the state change must also be conveyed by the element's accessible name or `aria-pressed`.

### GSAP MorphSVG

MorphSVG morphs between paths with different command structures by subdividing and matching points.

```js
import { gsap } from 'gsap';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
gsap.registerPlugin(MorphSVGPlugin);

MorphSVGPlugin.convertToPath('circle, rect, polygon'); // primitives become <path>
gsap.to('#play', {
  morphSVG: {
    shape: '#pause',
    shapeIndex: 'auto',     // which point on the start shape maps to the end shape's first point
    type: 'rotational',     // interpolates angle and length; avoids kinks on curved shapes
    map: 'complexity',      // how segments pair up: 'size' | 'position' | 'complexity'
  },
  duration: 0.2,            // --motion-state (200 ms); GSAP takes seconds
  ease: 'power2.inOut',
});
```

- When a morph twists inside out, replace `shapeIndex: 'auto'` with an explicit integer found by trial in development, then hard-code it.
- MorphSVG has been free for commercial use since GSAP 3.13.
- **flubber 0.4.2** also interpolates mismatched shapes, but its last npm publish was 2018-03-01; treat it as unmaintained and prefer MorphSVG or pre-normalised paths.

---

## Line Drawing

```html
<svg viewBox="0 0 200 60" role="img" aria-labelledby="sig-title">
  <title id="sig-title">Signature: Ada</title>
  <path class="draw" pathLength="1" d="M10 40 C 40 0, 60 60, 90 30 S 150 10, 190 40"
        fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
</svg>
```

```css
.draw {
  stroke-dasharray: 1;      /* one dash as long as the whole (normalised) path */
  stroke-dashoffset: 0;     /* base state: fully drawn */
}
@media (prefers-reduced-motion: no-preference) {
  /* decorative and non-blocking: the stroke is complete at rest, so the narrative band applies */
  .draw { animation: draw var(--motion-narrative) var(--ease-enter) both; }
  @keyframes draw { from { stroke-dashoffset: 1; } }
}
```

- `pathLength="1"` rescales dash units so `1` equals the full length, whatever the real geometry; no measuring needed.
- Without `pathLength`, measure with `path.getTotalLength()` and set the dash values in user units. Re-measure if the `d` attribute changes.
- The base state is the finished stroke. The animation only runs inside `no-preference`, so reduced-motion users and failed animations both see the complete drawing.
- Draw multiple strokes in sequence with `animation-delay` from a `--i` index, capped so the whole sequence stays inside the `--motion-narrative` band (600–1000 ms).

### `vector-effect: non-scaling-stroke` Caveat

`non-scaling-stroke` keeps stroke width constant when the SVG scales, but it computes the stroke in screen space. Dash lengths then stop matching the `pathLength` normalisation in some engines, and the drawing ends early or overshoots. Test the draw at every rendered size, or drop `non-scaling-stroke` from animated paths and compensate stroke width in the viewBox.

### Scroll-Linked Draw

```css
.draw { stroke-dasharray: 1; stroke-dashoffset: 0; }           /* base: drawn */

@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .draw {
      animation: draw linear both;
      animation-timeline: view();          /* declare after the shorthand */
      animation-range: entry 10% cover 50%;
    }
    @keyframes draw { from { stroke-dashoffset: 1; } }
  }
}
```

- Browser support for scroll-driven timelines is tracked in the support matrix of [ui-scroll-driven-motion](../../ui-scroll-driven-motion/SKILL.md). Outside `@supports`, the stroke is simply drawn.
- A JS fallback with `IntersectionObserver` that plays the timed draw once is acceptable; do not emulate scrubbing with scroll listeners.
- Timeline mechanics, ranges and libraries live in [ui-scroll-driven-motion](../../ui-scroll-driven-motion/SKILL.md).

---

## Accessibility

- Meaningful graphics: `role="img"` on the `<svg>` plus a `<title>` referenced by `aria-labelledby` (add `<desc>` for complex diagrams). The name describes the final drawing, not the animation.
- Decorative graphics: `aria-hidden="true"` and `focusable="false"`.
- Looping morphs or draws that run longer than 5 seconds alongside other content need a visible pause control (2.2.2 Pause, Stop, Hide); pausing on hover does not satisfy it.
- Under reduced motion, show the finished stroke or end shape immediately.
- Full criteria and tests: the "Motion and Animation" section of [web-accessibility-wcag](../../../../engineering/practices/web-accessibility-wcag/SKILL.md).

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **CSS `d` support: Chrome 52, Firefox 97, Safari parses with no effect** (verified) — @mdn/browser-compat-data 8.1.6 `css.properties.d`, https://www.npmjs.com/package/@mdn/browser-compat-data
- **gsap 3.15.0, MorphSVG free since 3.13** (verified) — https://registry.npmjs.org/gsap ; https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
- **flubber 0.4.2** (verified, stale) — last publish 2018-03-01, https://registry.npmjs.org/flubber
- **`non-scaling-stroke` with dash normalisation** (unverified) — BCD does not track the interaction between `vector-effect` and `pathLength` dashing; engine behaviour reported only by secondary sources
