# FLIP and Layout Animation

Layout properties (`top`, `width`, grid placement) cannot be animated cheaply: each frame would relayout. FLIP moves the element to its final layout instantly, then animates a `transform` that makes it look as if it started from the old position. The browser does one layout; the compositor does the motion.

---

## First, Last, Invert, Play

1. **First**: read the element's box before the change (`getBoundingClientRect()`).
2. **Last**: apply the change (reorder, class toggle, reparent) and read the new box.
3. **Invert**: compute the delta and apply a transform that puts the element back where it was.
4. **Play**: animate the transform to `none`.

```js
// Read the canonical tokens (--motion-layout, --ease-enter) from CSS so JS and CSS share one source.
const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

function flip(elements, mutate, {
  duration = parseFloat(token('--motion-layout')) || 320,  // "320ms" → 320; fallback if unset
  easing = token('--ease-enter') || 'ease-out',
} = {}) {
  // FIRST: batch every read before any write. Reading while a previous flip is
  // still running captures the in-flight visual box, so a retarget starts there.
  const first = new Map(elements.map((el) => [el, el.getBoundingClientRect()]));

  // Drop running flips so the Last read sees the untransformed final layout.
  elements.forEach((el) => el.getAnimations().forEach((anim) => anim.cancel()));

  mutate(); // apply the DOM or class change

  // LAST: one layout flush for all reads.
  const last = new Map(elements.map((el) => [el, el.getBoundingClientRect()]));

  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  for (const el of elements) {
    const a = first.get(el);
    const b = last.get(el);
    const dx = a.left - b.left;
    const dy = a.top - b.top;
    const sx = a.width / b.width;
    const sy = a.height / b.height;
    if (!dx && !dy && sx === 1 && sy === 1) continue;

    // INVERT + PLAY
    el.animate(
      [
        { transformOrigin: 'top left', transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy})` },
        { transformOrigin: 'top left', transform: 'none' },
      ],
      { duration, easing }
    );
  }
}
```

Interruption: the order above matters. Cancelling before the First read makes the element snap to its previous final layout, a visible jump; cancelling after the Last read pollutes Last with the old transform. Read First with the in-flight transform applied, cancel, mutate, read Last. Velocity is not carried over (the new animation starts at rest), which is acceptable for short layout moves; use a spring engine when it is not. GSAP Flip and Motion handle this ordering for you. Retargeting rules for each engine: [motion-timing-engines.md](../../ui-motion-interaction/references/motion-timing-engines.md).

---

## Read/Write Batching

- Group all `getBoundingClientRect()` calls, then all style writes. Interleaving read, write, read in a loop forces a synchronous layout per element (layout thrashing).
- Run measurements in the same task as the mutation; do not defer the Last read to `requestAnimationFrame` or the user sees one frame at the final position.
- For dozens of items, animate only the elements whose delta exceeds a pixel threshold and that intersect the viewport.

See [javascript-high-performance](../../../../languages/javascript-high-performance/SKILL.md) for forced-reflow diagnosis.

---

## Counter-Scaling Children and Border Radius

Scaling a parent from 100 px to 400 px wide also stretches its text, icons and corners.

- **Counter-scale children**: animate each child with the inverse scale (`scale(1/sx, 1/sy)`) on the same timeline. With linear interpolation the inverse is not exact mid-flight; sample keyframes (8 to 12 steps of `1 / currentScale`) so the inverse tracks the parent frame by frame.
- **Correct `border-radius`**: a radius of 16 px under `scaleX(4)` renders 64 px wide. Animate `border-radius` per frame as `r / sx` horizontally and `r / sy` vertically (`border-radius: calc(16px / var(--sx)) / calc(16px / var(--sy))` with registered `@property` numbers), or clip the corners with an unscaled wrapper.
- **Prefer position-only FLIP** when sizes change a lot: translate the element and cross-fade the content instead of scaling it.

---

## Scroll Anchoring

`overflow-anchor` (Baseline newly available 2026-09-14; Chrome 56, Firefox 66, Safari 27) lets the browser shift the scroll position so visible content stays put when content above it changes size. During a FLIP sequence, the browser can apply an anchoring adjustment between the First and Last reads, so items appear to jump by the anchored amount.

- Set `overflow-anchor: none` on the animating list (or its scroller) for the duration, or include `scrollY` in both reads and subtract the difference.
- Re-enable anchoring after the animation so later lazy-loaded content does not push the reader.

---

## GSAP Flip

```js
import { gsap } from 'gsap';
import { Flip } from 'gsap/Flip';
gsap.registerPlugin(Flip);

const state = Flip.getState('.card, .card-title');   // First
grid.classList.toggle('is-list');                     // mutate
Flip.from(state, {                                    // Last, Invert, Play
  duration: 0.32,     // --motion-layout (320 ms); GSAP takes seconds
  ease: 'power2.inOut',
  absolute: true,     // position: absolute during the flip so flex/grid reflow does not fight it
  nested: true,       // compensate children whose parent also moves
  scale: true,        // animate scaleX/scaleY instead of width/height (cheaper; distorts content)
  prune: true,        // skip elements that did not move
  onEnter: (els) => gsap.fromTo(els, { opacity: 0 }, { opacity: 1 }),
  onLeave: (els) => gsap.to(els, { opacity: 0 }),
});
```

- `Flip.getState()` records position, size, rotation and optional `props` ('backgroundColor,color').
- Shared elements: give the outgoing and incoming nodes the same `data-flip-id` and pass both to `getState()` / `from()` with `targets`.
- Calling `Flip.from()` while a previous flip runs starts from the current visual state when `getState()` is captured mid-flight.
- GSAP and all its plugins, Flip included, have been free for commercial use since 3.13 under the Webflow standard no-charge license.

---

## Motion (React)

```jsx
import { motion, AnimatePresence, LayoutGroup } from 'motion/react';

<LayoutGroup id="inbox">
  <ul>
    <AnimatePresence initial={false}>
      {items.map((item) => (
        <motion.li
          key={item.id}
          layout                              // animate its own layout changes
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          style={{ borderRadius: 12 }}        // set via style so Motion corrects distortion
        >
          {item.title}
          {item.id === selected && <motion.span layoutId="selection" className="pill" />}
        </motion.li>
      ))}
    </AnimatePresence>
  </ul>
</LayoutGroup>
```

| API | Role |
|---|---|
| `layout` (`true`, `"position"`, `"size"`) | Animate this element's layout changes; `"position"` avoids scale distortion of content |
| `layoutId` | Shared element: a new element with the same id animates from the old one's box |
| `AnimatePresence` | Keeps removed children mounted until their `exit` animation finishes |
| `LayoutGroup` | Synchronises layout animations across components that do not re-render together; `id` namespaces `layoutId` |
| `layoutScroll` | On a scrollable ancestor, so measurements account for its scroll offset |
| `layoutRoot` | On a `position: fixed` ancestor, so page scroll is accounted for |
| `layoutDependency` | Measure only when this value changes |

- Motion corrects scale distortion of `borderRadius` and `boxShadow` only when they are set through `style` or animation props, not through CSS classes.
- Children of a scaling `layout` element distort unless they also receive `layout`.
- Do not combine `layoutId` with a View Transition on the same element; see the SKILL.md framework notes.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **gsap 3.15.0, plugins free since 3.13** (verified) — https://registry.npmjs.org/gsap ; https://gsap.com/standard-license ; Flip docs https://gsap.com/docs/v3/Plugins/Flip/
- **motion 14.4.0, `motion/react` layout props** (verified) — https://registry.npmjs.org/motion ; https://motion.dev/docs/react-layout-animations
- **`overflow-anchor` Baseline 2026-09-14** (verified) — web-features 3.43.0 and @mdn/browser-compat-data 8.1.6, https://www.npmjs.com/package/web-features
