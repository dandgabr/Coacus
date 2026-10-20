# Reveal, Collapse and Loading Transitions

Recipes for elements that appear, disappear, expand, reveal or wait for data. Every recipe starts from a state that is correct with no animation; the transition is layered on top. Durations and easings use the canonical `--motion-*` and `--ease-*` tokens defined in [motion-timing-engines.md](../../ui-motion-interaction/references/motion-timing-engines.md); under reduced motion the spatial tokens collapse to `0ms`.

---

## Entry and Exit Primitives

### `@starting-style` and `transition-behavior: allow-discrete`

Transitions never run on the first style of a freshly inserted or newly displayed element, and `display` normally flips instantly. Two primitives fix that:

- `@starting-style` defines the "before" style used for the first transition after insertion or after `display: none` is removed (Baseline newly available 2024-08-06).
- `transition-behavior: allow-discrete` (or the `allow-discrete` keyword in the shorthand) lets discrete properties such as `display` and `content-visibility` take part in a transition. On exit, `display` stays visible until the end of the transition, then flips to `none` (Baseline newly 2024-08-06 for the property).

```css
.toast {
  opacity: 1;
  translate: 0 0;
  transition:
    opacity var(--motion-state) var(--ease-enter),
    translate var(--motion-state) var(--ease-enter),
    display var(--motion-state) allow-discrete;
}
.toast[hidden] {               /* exit target; also the no-transition base */
  display: none;
  opacity: 0;
  translate: 0 0.5rem;
}
@starting-style {              /* entry origin */
  .toast { opacity: 0; translate: 0 0.5rem; }
}
@media (prefers-reduced-motion: reduce) {
  .toast { translate: none; }  /* keep the fade, drop the travel */
}
```

Support caveat: transitioning `display` works in Chrome 117 and Safari 18, not in Firefox (MDN BCD), so the **exit** is instant in Firefox while the entry still animates. That is an acceptable degradation; do not add JS timers to fake it.

### Popover

```css
[popover] {
  opacity: 0;
  scale: 0.96;
  transition:
    opacity var(--motion-state) var(--ease-enter),
    scale var(--motion-state) var(--ease-enter),
    overlay var(--motion-state) allow-discrete,
    display var(--motion-state) allow-discrete;
}
[popover]:popover-open {
  opacity: 1;
  scale: 1;
}
@starting-style {
  [popover]:popover-open { opacity: 0; scale: 0.96; }
}
```

- `overlay` keeps the element in the top layer until the exit finishes. It ships only in Chromium (Chrome 117) and is not Baseline. Without it (Safari, Firefox), the element leaves the top layer the moment it closes, so its exit can render beneath other content or be skipped. Keep exits short so the difference is not noticeable.
- Popover API is Baseline newly available since 2025-01-27; light dismiss and focus return come with it, so prefer it over a custom overlay.

### `<dialog>`

```css
dialog {
  --exit: calc(var(--motion-layout) * var(--motion-exit-ratio));
  opacity: 0;
  translate: 0 1rem;
  transition:                  /* closed state = exit target, so these are exit timings */
    opacity var(--exit) var(--ease-exit),
    translate var(--exit) var(--ease-exit),
    overlay var(--exit) allow-discrete,
    display var(--exit) allow-discrete;
}
dialog[open] {
  opacity: 1;
  translate: 0 0;
  transition-duration: var(--motion-layout);   /* enter timing */
  transition-timing-function: var(--ease-enter);
}
@starting-style { dialog[open] { opacity: 0; translate: 0 1rem; } }

dialog::backdrop {
  background: rgb(0 0 0 / 0);
  transition:
    background-color var(--motion-layout),
    overlay var(--motion-layout) allow-discrete,
    display var(--motion-layout) allow-discrete;
}
dialog[open]::backdrop { background: rgb(0 0 0 / 0.5); }
@starting-style { dialog[open]::backdrop { background: rgb(0 0 0 / 0); } }
```

- Open with `showModal()` so focus moves into the dialog and the rest of the page becomes inert natively; closing returns focus to the opener.
- Exits use the house "exit is about 70 to 80 percent of the enter" rule through `--motion-exit-ratio`: the closed-state rule carries the exit timing and `[open]` overrides it with the enter timing.

---

## Accordion and Auto Height

### Base: Grid `0fr ↔ 1fr`

Grid track sizes interpolate (widely available), so a single-row grid animates to the content's intrinsic height without measuring.

```html
<h3>
  <button type="button" aria-expanded="false" aria-controls="ship-panel" id="ship-btn">Shipping</button>
</h3>
<div class="panel" id="ship-panel" role="region" aria-labelledby="ship-btn" inert>
  <div class="panel__inner">…</div>
</div>
```

```css
.panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--motion-layout) var(--ease-enter);
}
.panel__inner { min-height: 0; overflow: hidden; }
.panel[data-open] { grid-template-rows: 1fr; }
@media (prefers-reduced-motion: reduce) { .panel { transition: none; } }
```

```js
button.addEventListener('click', () => {
  const open = button.getAttribute('aria-expanded') !== 'true';
  button.setAttribute('aria-expanded', String(open));
  panel.toggleAttribute('data-open', open);
  panel.inert = !open;   // collapsed content leaves the tab order and the accessibility tree
});
```

- `inert` toggles immediately on both open and close; a collapsing panel must not keep focusable children reachable during its exit.
- Use a real `<button>` with `aria-expanded` and `aria-controls`; the heading wrapper keeps the outline navigable.

### Enhancement: `interpolate-size` and `calc-size()`

```css
@supports (interpolate-size: allow-keywords) {
  :root { interpolate-size: allow-keywords; }   /* lets height: 0 ↔ auto interpolate */
}
/* or per property: block-size: calc-size(auto, size); */
```

Both ship only in Chrome 129. Elsewhere the keyword change is discrete, so the grid recipe stays the base path.

### Native `<details>`

```html
<details name="faq"><summary>Returns</summary><p>…</p></details>
<details name="faq"><summary>Warranty</summary><p>…</p></details>
```

```css
details::details-content {
  block-size: 0;
  overflow: clip;
  transition:
    block-size var(--motion-layout) var(--ease-enter),
    content-visibility var(--motion-layout) allow-discrete;
}
details[open]::details-content { block-size: auto; }   /* animates where interpolate-size applies */
```

- `name` makes a group exclusive: opening one closes the others (Baseline newly 2024-09-03).
- `::details-content` is Baseline newly available since 2025-09-16 (Chrome 131, Firefox 143, Safari 18.4). The height animation needs `interpolate-size` (Chrome only); `content-visibility` with `allow-discrete` is not transitionable in Firefox. Other engines toggle instantly, which is correct behaviour.
- Collapsed `<details>` content is already hidden from assistive technology and the tab order; no `inert` is needed. Expanded state is exposed natively.

---

## Clip-Path and Mask Reveals

```css
.reveal { clip-path: inset(0 0 0 0); }            /* base: fully visible */

@media (prefers-reduced-motion: no-preference) {
  .js .reveal:not(.is-revealed) { clip-path: inset(0 100% 0 0); }
  .js .reveal { transition: clip-path var(--motion-layout) var(--ease-enter); }
}
```

- Arm the hidden state only when script runs (`.js` on `<html>`), so content is never stuck clipped.
- Circle from the pointer: `clip-path: circle(0 at var(--x) var(--y))` to `circle(150% at var(--x) var(--y))`. `inset()`, `circle()`, `ellipse()` and `polygon()` animate everywhere (clip-path animation is widely available). `polygon()` needs the same vertex count at both ends.
- `shape()` (Baseline newly available 2026-02-24; Chrome 135, Firefox 148, Safari 18.4) allows curved, responsive clip shapes; supply an `inset()` or `polygon()` fallback before it.
- Mask wipe with a registered custom property, since gradients do not interpolate directly:

```css
@property --reveal { syntax: '<percentage>'; inherits: false; initial-value: 110%; }
.mask-reveal {
  mask-image: linear-gradient(to right, #000 var(--reveal), transparent calc(var(--reveal) + 10%));
  transition: --reveal var(--motion-layout) var(--ease-enter);
}
.js .mask-reveal:not(.is-revealed) { --reveal: -10%; }
```

- Cost: `clip-path` and `mask-image` animations repaint the element every frame; compositor acceleration of clip-path is not guaranteed across engines. Profile large or full-viewport reveals on a mid-range device.
- `inert`: when the reveal is **user-triggered** ("show more", a toggle), keep the clipped content `inert` until it is revealed. For **scroll-triggered** reveals, do not use `inert` (keyboard users could never reach the content); reveal on `focusin` of the container as well as on intersection.

---

## Skeletons and Shimmer

```html
<section aria-busy="true" aria-labelledby="orders-h">
  <h2 id="orders-h">Orders</h2>
  <div class="skeleton-row" aria-hidden="true">
    <span class="skeleton" style="inline-size: 40%"></span>
    <span class="skeleton" style="inline-size: 25%"></span>
  </div>
</section>
<p role="status" class="visually-hidden" id="orders-status">Loading orders</p>
```

```css
.skeleton {
  display: block;
  block-size: 1lh;                        /* match the final line box */
  background: var(--skeleton-base);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}
.skeleton::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, var(--skeleton-shine), transparent);
  translate: -100% 0;
  animation: shimmer 1.4s linear 3;        /* loop period, not a transition token; finite: stops after ~4 s */
}
@keyframes shimmer { to { translate: 100% 0; } }
@media (prefers-reduced-motion: reduce) {
  .skeleton::after { animation: none; display: none; }
}
```

- **Layout stability (CLS):** the skeleton must occupy the final content's exact box: same line height, same row count where known, `aspect-ratio` for media. Swapping a short skeleton for taller content is a layout shift.
- **Shimmer via `transform`** on a pseudo-element runs on the compositor; animating `background-position` repaints every frame.
- **`aria-busy="true"`** on the region while loading; set it to `false` when content lands. Mark skeleton shapes `aria-hidden="true"`.
- **Completion (4.1.3 Status Messages):** update the `role="status"` text ("12 orders loaded") when data arrives; do not rely on the visual swap.
- **Indefinite loaders (2.2.2):** a shimmer or spinner that can run longer than 5 seconds alongside other content needs to stop or offer a pause; the finite iteration count above stops it. A loader is exempt only when it is essential (interaction cannot happen during the phase).
- **Reduced motion:** a static skeleton, no shimmer.
- Table-specific loading states: [ui-data-tables-dashboards](../../ui-data-tables-dashboards/SKILL.md). Full criteria: the "Motion and Animation" section of [web-accessibility-wcag](../../../../engineering/practices/web-accessibility-wcag/SKILL.md).

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **Baseline statuses (`@starting-style`, `transition-behavior`, popover, `<details name>`, `::details-content`, `shape()`, clip-path animation)** (verified) — web-features 3.43.0, https://www.npmjs.com/package/web-features
- **Browser versions (`display` and `content-visibility` transitionable, `overlay`, `interpolate-size`, `calc-size()`)** (verified) — @mdn/browser-compat-data 8.1.6, https://www.npmjs.com/package/@mdn/browser-compat-data
- **Compositor-accelerated `clip-path` animation** (unverified) — not tracked by BCD or web-features; engine behaviour reported only by secondary sources, so assume repaint
