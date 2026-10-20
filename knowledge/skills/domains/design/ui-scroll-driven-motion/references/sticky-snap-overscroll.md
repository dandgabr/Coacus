# Sticky, Faux-Horizontal, Snap and Overscroll

Native scroll primitives first. Each recipe keeps a complete static layout and adds motion or Chrome-only features as enhancements.

---

## 1. Sticky positioning

`position: sticky` needs an inset (`top`, `inset-block-start`), room inside its containing block, and the right scroll container.

### Why sticky silently does nothing

- **An ancestor became the scroll container.** Any ancestor between the sticky element and the intended scroller with `overflow: hidden`, `auto` or `scroll` (on either axis) becomes the element's scrollport. If that ancestor does not scroll, the element never sticks.
- **Fix:** use `overflow: clip` on that ancestor. It clips painting like `hidden` but does not create a scroll container. Otherwise move the clipping to an element outside the sticky chain.
- **Flex and grid stretch.** An item stretched to the full row height has no room to travel. Add `align-self: start` (or `align-items: start` on the container).
- **The containing block ends.** Sticky stops at the end of its parent; a parent exactly as tall as the sticky element never shows the effect.

Find the culprit:

```js
for (let el = sticky.parentElement; el; el = el.parentElement) {
  const { overflowX, overflowY } = getComputedStyle(el);
  if (/auto|scroll|hidden/.test(overflowX + overflowY)) console.log(el, overflowX, overflowY);
}
```

### Stuck styling with scroll-state queries (Chrome-only enhancement)

```css
.site-header {
  position: sticky;
  top: 0;
  container-type: scroll-state;
}

@supports (container-type: scroll-state) {
  @container scroll-state(stuck: top) {
    .site-header__inner { box-shadow: 0 1px 0 var(--color-border); }
  }
}
```

The query styles descendants of the container, not the container itself. Without support the header simply has no stuck styling; do not rebuild it with scroll listeners unless the state carries meaning. `scroll-state(scrolled: …)` is newer still.

### Sticky headers and Focus Not Obscured (2.4.11)

A sticky header can cover the element that receives focus when tabbing backward or following an anchor.

```css
html { scroll-padding-top: calc(var(--header-height, 4rem) + 0.5rem); }

/* Short viewports and high zoom: stop sticking rather than covering content. */
@media (max-height: 30rem) {
  .site-header { position: static; }
}
```

Measure the real header height with a `ResizeObserver` into `--header-height` when it varies. `scroll-padding` applies to the scroll container (the root here); `scroll-margin-top` adjusts individual targets.

---

## 2. Faux-horizontal section

Vertical scrolling drives horizontal travel of a track. Gate it first (see the "Default: No" box in [the skill](../SKILL.md)). The base layout is a vertical list; the enhancement only applies on wide viewports without a reduced-motion preference.

```html
<section class="hscroll" aria-labelledby="hscroll-title" style="--items: 5">
  <div class="hscroll__sticky">
    <h2 id="hscroll-title">Release timeline</h2>
    <ol class="hscroll__track">
      <li class="hscroll__item"><a href="/releases/1">…</a></li>
      <!-- … -->
    </ol>
  </div>
</section>
```

### CSS: `view()` timeline on the section

```css
.hscroll__track {
  display: grid;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

@media (min-width: 48rem) and (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .hscroll {
      height: calc(var(--items) * 100vh);  /* vertical distance that pays for the travel */
      view-timeline: --hscroll block;
    }
    .hscroll__sticky {
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: clip;                      /* clips the track, no scroll container */
      display: flex;
      align-items: center;
    }
    .hscroll__track {
      grid-auto-flow: column;
      grid-auto-columns: min(80vw, 40rem);
      width: max-content;
      animation: hscroll-travel linear both;
      animation-timeline: --hscroll;
      animation-range: contain;            /* the interval while the stage is stuck */
    }
  }
}

@keyframes hscroll-travel {
  to { transform: translateX(calc(-100% + 100vw)); }
}
```

`contain` runs from the section's top reaching the viewport top to its bottom reaching the viewport bottom, exactly the sticky interval. A `scroll()` timeline works too when the section is the only content of its scroller.

### GSAP alternative with `containerAnimation`

Use this when engines without scroll timelines need the same behavior. GSAP pins the stage, so drop the `N × 100vh` height and the CSS sticky rules.

```js
const mm = gsap.matchMedia();
mm.add('(min-width: 48rem) and (prefers-reduced-motion: no-preference)', () => {
  const track = document.querySelector('.hscroll__track');
  const travel = () => track.scrollWidth - document.documentElement.clientWidth;

  const tween = gsap.to(track, {
    x: () => -travel(),
    ease: 'none',                       // required by containerAnimation
    scrollTrigger: {
      trigger: '.hscroll',
      start: 'top top',
      end: () => `+=${travel()}`,
      pin: '.hscroll__sticky',
      scrub: true,
      invalidateOnRefresh: true,
    },
  });

  // Triggers inside the moving track: no pin, no snap on these.
  gsap.utils.toArray('.hscroll__item').forEach((item) => {
    gsap.from(item, {
      opacity: 0.4,
      ease: 'none',
      scrollTrigger: {
        trigger: item,
        containerAnimation: tween,
        start: 'left 80%',
        end: 'left 40%',
        scrub: true,
      },
    });
  });
});
```

### Keyboard: follow focus

The clipped track cannot scroll, so a focused link off to the side stays invisible. Scroll the page to the progress that brings it into view:

```js
const section = document.querySelector('.hscroll');
const track = section.querySelector('.hscroll__track');

section.addEventListener('focusin', (event) => {
  const item = event.target.closest('.hscroll__item');
  if (!item || getComputedStyle(track).gridAutoFlow !== 'column') return; // vertical layout: native
  const maxTravel = track.scrollWidth - track.parentElement.clientWidth;
  const progress = Math.min(1, Math.max(0, item.offsetLeft / maxTravel)); // layout offset, ignores transform
  const start = section.getBoundingClientRect().top + scrollY;
  const distance = section.offsetHeight - innerHeight;
  window.scrollTo({ top: start + progress * distance, behavior: 'auto' });
});
```

`offsetLeft` is relative to the sticky stage (a positioned ancestor) and unaffected by transforms. With the GSAP variant, `distance` is the pin duration instead (`tween.scrollTrigger.end - tween.scrollTrigger.start`).

### Narrow screens and reduced motion

Below the breakpoint, or with reduced motion, the media query fails and the base vertical list renders, satisfying 1.4.10 Reflow at 320 CSS px. Verify that the section height resets (no empty `N × 100vh` gap) and that `gsap.matchMedia()` reverts the pin when the preference changes mid-session.

---

## 3. Scroll snapping

```css
.carousel {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 80%;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x proximity;
  scroll-padding-inline: 1rem;
  overscroll-behavior-x: contain;
}
.carousel > * { scroll-snap-align: start; }
.carousel > .chapter-end { scroll-snap-stop: always; }
```

- **`mandatory` vs `proximity`:** `mandatory` always comes to rest on a snap position; when an item is larger than the scrollport, its far end can become unreachable or jumpy across engines. `proximity` snaps only near a position. Use `mandatory` only when every item is guaranteed smaller than the scrollport at every size and zoom level.
- **`scroll-snap-stop: always`:** prevents a fling from skipping the item. Use for chapter boundaries, not every slide.
- **`scroll-padding`:** offsets snap positions for fixed headers and gutters; on the root it also keeps anchors clear of sticky bars.
- Re-snapping after resize and content changes is automatic; your own "current slide" state is not.

### Tracking the current item

```js
const setCurrent = (el) => { /* update aria-current, dots, buttons */ };

if ('onscrollsnapchange' in window) {
  carousel.addEventListener('scrollsnapchange', (event) => setCurrent(event.snapTargetInline));
} else if ('onscrollend' in window) {
  carousel.addEventListener('scrollend', () => setCurrent(nearestItem(carousel)));
} else {
  let timer;
  carousel.addEventListener('scroll', () => {
    clearTimeout(timer);
    timer = setTimeout(() => setCurrent(nearestItem(carousel)), 120);
  }, { passive: true });
}
```

`scrollsnapchanging` fires during the gesture with the pending target, useful for previews.

### Buttons are the base path (2.5.7)

Swiping is a dragging movement; every carousel needs single-pointer controls.

```html
<div class="carousel-controls">
  <button type="button" data-dir="-1" aria-controls="gallery">Previous slide</button>
  <button type="button" data-dir="1" aria-controls="gallery">Next slide</button>
</div>
```

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
controls.addEventListener('click', (event) => {
  const dir = Number(event.target.closest('button')?.dataset.dir);
  if (!dir) return;
  carousel.scrollBy({ left: dir * carousel.clientWidth * 0.8, behavior: reduce.matches ? 'auto' : 'smooth' });
});
```

Disable the button at each end, and keep targets at least 24 × 24 CSS px (2.5.8).

### Native scroll buttons and markers (Chrome-only enhancement)

```css
@supports selector(::scroll-button(*)) {
  .carousel-controls { display: none; } /* avoid duplicate controls */

  .carousel::scroll-button(inline-start) { content: "‹" / "Previous slide"; }
  .carousel::scroll-button(inline-end)   { content: "›" / "Next slide"; }

  .carousel { scroll-marker-group: after; }
  .carousel > *::scroll-marker { content: "" / attr(data-label); }
  .carousel > *::scroll-marker:target-current { background: var(--color-accent); }
}
```

Give every generated button and marker an accessible name through the alternative text after the slash, and confirm the names in the accessibility tree. Engines without support keep the HTML buttons.

---

## 4. Overscroll

`overscroll-behavior` controls what happens when a scroll container reaches its edge.

| Value | Scroll chaining to the parent | Local bounce or glow, browser gestures |
| --- | --- | --- |
| `auto` | Yes | Yes |
| `contain` | No | Kept locally |
| `none` | No | Removed |

- **Axes:** use the per-axis longhands `overscroll-behavior-x` and `overscroll-behavior-y` (or the logical `-inline` and `-block` forms). A horizontal carousel with `overscroll-behavior-x: contain` stops edge swipes from chaining into history navigation in engines that support it.
- **Root:** `html { overscroll-behavior-y: none; }` removes the browser's own pull-to-refresh. Do this only when the product supplies its own refresh control.

### Scroll lock behind `<dialog>`

`overscroll-behavior` applies to scroll containers; in older engines a container that does not currently overflow still chains to the page. Make the dialog body the scroll container and lock the page while a modal is open:

```css
dialog { max-height: 90vh; overflow-y: auto; overscroll-behavior: contain; }
html:has(dialog:modal) { overflow: hidden; scrollbar-gutter: stable; }
```

`scrollbar-gutter: stable` prevents the layout shift when the page scrollbar disappears.

### Custom pull-to-refresh

- Provide a visible Refresh button; the pull gesture is a dragging movement and cannot be the only path (2.5.7).
- Announce the result through a status message (4.1.3), not by moving focus.
- Contain overscroll on the element that implements the gesture, and drop rubber-band motion under reduced motion.
- Pointer capture, velocity tracking and release momentum for the pull follow the drag recipe in [pointer-and-gesture](../../ui-motion-interaction/references/pointer-and-gesture.md).

---

## 5. Stepped presentations (only when explicitly requested)

A stepped presentation moves between discrete scenes instead of continuous reading. Start from native snap; add input handling only when snap alone cannot deliver the specified gesture.

- **Alignment:** define scene alignment against the usable area below fixed controls (`scroll-padding`). Keep the selected scene and progress coherent after resize, interruption and orientation changes; check progress endpoints and visible stacking over menus in every appearance.
- **Scoped input:** keep any wheel or key handling local to the active narrative. Normalize delta units (`deltaMode` pixels, lines or pages), absorb momentum without trapping the user, and never swallow a new gesture after resize.
- **Preserve defaults:** zoom gestures, horizontal input, editable fields, range controls, nested scrolling tables and everything outside the narrative keep native behavior.
- **Oversized scenes:** a scene taller than the usable viewport stays scrollable to its last control before advancing.
- **Access:** every scene is reachable by keyboard and touch; no information depends on a wheel event.
- **Static path:** expose the full information without scrubbed animation, forced timing or a transition that must finish. Use a static sequence or immediate navigation. Leaving a snap rule in place is not by itself proof of an accessible static path; verify that actions below the fold remain reachable.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20 against web-features 3.43.0 (https://registry.npmjs.org/web-features) and MDN browser-compat-data 8.1.6 (https://registry.npmjs.org/@mdn/browser-compat-data):

- **`overflow: clip`** (verified) — Baseline widely available 2025-03-12
- **Scroll-state container queries** (verified) — Chrome 133 only; `scrolled` state Chrome 144
- **`scroll-snap-stop`** (verified) — Chrome 75, Firefox 103, Safari 15
- **`scrollsnapchange` / `scrollsnapchanging`** (verified) — Chrome 129 only
- **`::scroll-button()` / `::scroll-marker` / `scroll-marker-group`** (verified) — Chrome 135 only
- **`scrollend`** (verified) — Baseline newly available 2025-12-12
- **`overscroll-behavior`** (verified) — partial behavior Chrome 63, Firefox 59, Safari 16; non-overflowing scroll containers Chrome 144, Firefox 150
- **`scrollbar-gutter`** (verified) — Baseline newly available 2024-12-11
- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap ; `containerAnimation` requires `ease: "none"` and cannot pin or snap per https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- **Alternative text in `content` with `attr()` for `::scroll-marker` names** (unverified) — not covered by BCD at this granularity; confirm in the accessibility tree
