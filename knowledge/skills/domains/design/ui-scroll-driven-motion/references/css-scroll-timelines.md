# CSS Scroll Timelines, ScrollTrigger and Smooth-Scroll Libraries

Mechanics for progress-linked and threshold-triggered scroll motion. Every recipe starts from a complete static page; motion is an enhancement guarded by `@supports`, feature detection and `prefers-reduced-motion: no-preference`.

---

## 1. Scroll progress timelines: `scroll()`

`scroll()` maps the scroll position of a scroll container (0% at the start, 100% at the end) to animation progress. Arguments: scroller (`nearest` default, `root`, `self`) and axis (`block` default, `inline`, `x`, `y`).

```css
/* Base: no progress bar at all. */
.reading-progress { display: none; }

@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: scroll()) {
    .reading-progress {
      display: block;
      position: fixed;
      inset: 0 0 auto 0;
      height: 4px;
      background: var(--color-accent);
      transform-origin: 0 50%;
      animation: grow-progress linear both;
      animation-timeline: scroll(root block);
    }
  }
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

A progress bar is decorative here; if the position matters to the task, expose it as text as well.

## 2. View progress timelines: `view()`

`view()` tracks an element (the subject) as it crosses its scrollport. Optional arguments: axis and an inset (`view(block 10% 0%)`) that shrinks the active area, useful under a sticky header.

### `animation-range` named ranges

| Range | 0% | 100% |
| --- | --- | --- |
| `cover` | Subject's leading edge enters the scrollport | Trailing edge leaves |
| `contain` | Subject fully inside (or fully covering) the scrollport | Starts to leave |
| `entry` | Leading edge enters | Subject fully entered |
| `exit` | Subject starts to leave | Fully left |
| `entry-crossing` / `exit-crossing` | Edge crosses the scrollport edge | Opposite edge crosses it |

Combine a start and an end: `animation-range: entry 10% cover 40%;`. Keyframes can also target ranges directly (`entry 0% { … }`).

### Named timelines and `timeline-scope`

A named view timeline (`view-timeline: --card block`) is visible to the subject and its descendants. A sibling or cousin needs `timeline-scope` on a shared ancestor:

```css
.gallery { timeline-scope: --hero; }
.gallery__hero { view-timeline: --hero block; }
.gallery__caption {
  animation: caption-in linear both;
  animation-timeline: --hero;
  animation-range: contain 0% contain 50%;
}
```

When `timeline-scope` is unavailable, restructure so the timeline source is an ancestor of the animated element.

### The shorthand ordering pitfall

The `animation` shorthand resets `animation-timeline` to `auto`. Declare `animation-timeline` (and `animation-range`) **after** the shorthand, or the element silently falls back to a time-based animation with zero duration. Always use fill mode `both` so the state before and after the range holds.

## 3. Reveal with `@supports` and an IntersectionObserver fallback

```css
/* Base path: content is visible. Nothing below applies without support or a script. */
.reveal { opacity: 1; }

@keyframes reveal {
  from { opacity: 0; transform: translateY(1.5rem); }
}

@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      animation: reveal linear both;
      animation-timeline: view();
      animation-range: entry 0% cover 30%;
    }
  }

  /* Fallback, active only after the script adds .js-reveal. */
  .js-reveal .reveal:not(.is-revealed) {
    opacity: 0;
    transform: translateY(1.5rem);
  }
  /* --reveal-duration: a component-state band token from motion-timing-engines.md */
  .js-reveal .reveal {
    transition: opacity var(--reveal-duration) ease-out,
                transform var(--reveal-duration) ease-out;
  }
}
```

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const timelineSupported = CSS.supports('animation-timeline: view()');

if (!timelineSupported && !reduce.matches && 'IntersectionObserver' in window) {
  document.documentElement.classList.add('js-reveal');

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target); // one-shot: stop paying for it
    }
  }, {
    rootMargin: '0px 0px -10% 0px', // fire slightly after the element enters
    threshold: 0,                   // tall elements may never reach a high ratio
  });

  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  // Focus and find-in-page can land on content that is still transparent.
  document.addEventListener('focusin', (event) => {
    event.target.closest?.('.reveal')?.classList.add('is-revealed');
  });
}
```

Notes:

- `threshold` is the visible fraction of the target, so an element five times taller than the viewport never exceeds 0.2. Use `threshold: 0` plus `rootMargin` for tall targets.
- Disconnect the observer when the owning view unmounts.
- Take reveal durations and curves from [motion timing engines](../../ui-motion-interaction/references/motion-timing-engines.md); scrubbed timelines have no duration.

## 4. GSAP ScrollTrigger essentials

```js
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();
mm.add(
  {
    motion: '(prefers-reduced-motion: no-preference)',
    wide: '(min-width: 48rem)',
  },
  (context) => {
    const { motion, wide } = context.conditions;
    if (!motion) return; // static layout stays in place

    gsap.to('.scene__art', {
      yPercent: -20,
      ease: 'none', // progress-linked: no easing lag
      scrollTrigger: {
        trigger: '.scene',          // measured, never animated
        start: 'top top',           // trigger edge, viewport edge
        end: '+=150%',
        scrub: true,
        pin: wide ? '.scene__stage' : false,
      },
    });
  }
);

document.fonts.ready.then(() => ScrollTrigger.refresh());
window.addEventListener('load', () => ScrollTrigger.refresh());
// On unmount: mm.revert();
```

- **`start` / `end`:** `"<trigger position> <viewport position>"` (`"top 80%"`, `"bottom top"`) or relative (`"+=500"`). Use `markers: true` while developing.
- **`scrub: true` vs a number:** `true` locks progress to the scrollbar. A number (`scrub: 0.5`) is seconds of catch-up smoothing; it decouples the visual from input, so keep it small.
- **`pin`:** fixes an element for the trigger's duration and inserts a pin spacer. Pin a child of the trigger or a dedicated wrapper; pinning inside a transformed ancestor breaks `position: fixed`.
- **Do not animate the trigger or the pinned element itself.** Moving it shifts the measured `start` and `end`. Animate children.
- **`ScrollTrigger.refresh()`:** runs automatically on resize, not on content changes. Call it after fonts, images, accordions, late data and route changes.
- **`gsap.matchMedia()`:** replaces the deprecated `ScrollTrigger.matchMedia()`. Everything created inside a condition reverts when it stops matching, including when the user switches reduced motion on.
- Faux-horizontal tracks with `containerAnimation` are covered in [sticky, snap and overscroll](sticky-snap-overscroll.md).

## 5. Parallax

### Native: named view timeline

Name the timeline on the section, so the layers' own transforms never feed back into the measurement.

```css
.parallax {
  position: relative;
  overflow: clip;              /* clips layers without creating a scroll container */
  view-timeline: --scene block;
}

@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .parallax__layer {
      animation: parallax linear both;
      animation-timeline: --scene;
      animation-range: cover;
    }
    .parallax__layer--far  { --depth: 8vh; }
    .parallax__layer--near { --depth: -4vh; }
  }
}

@keyframes parallax {
  from { translate: 0 calc(var(--depth, 0px) * -1); }
  to   { translate: 0 var(--depth, 0px); }
}
```

### Fallback: transform in one rAF loop

```js
const scene = document.querySelector('.parallax');
const layers = [...scene.querySelectorAll('[data-depth]')];
let visible = false;
let queued = false;

const update = () => {
  queued = false;
  const rect = scene.getBoundingClientRect();                    // read first
  const progress = (innerHeight - rect.top) / (innerHeight + rect.height); // 0..1 over cover
  for (const layer of layers) {                                   // then write
    const depth = Number(layer.dataset.depth);                    // px
    layer.style.transform = `translate3d(0, ${(progress * 2 - 1) * depth}px, 0)`;
  }
};
const request = () => {
  if (visible && !queued) { queued = true; requestAnimationFrame(update); }
};

if (!CSS.supports('animation-timeline: view()') &&
    matchMedia('(prefers-reduced-motion: no-preference)').matches) {
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; request(); })
    .observe(scene);
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);
}
```

Keep depth small (a few viewport percent), never move body text, and drop the effect entirely under reduced motion.

## 6. Smooth-scroll libraries

Gate first: see the "Default: No" box in [the skill](../SKILL.md). For anchor and programmatic jumps, native smoothing is enough and affects nothing else:

```css
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```

### Why hijacking is the exception

A smooth-scroll library intercepts wheel (and optionally touch) input and replays it through its own easing. The interpolation is a low-pass filter: the page lags the input, overrides OS acceleration the user tuned, and turns every scroll into motion the user did not ask for. It runs on the main thread each frame, so a long task stalls scrolling itself instead of one animation.

### Lenis

The package is `lenis`; `@studio-freight/lenis` is the deprecated former name.

| Option | Default | Note |
| --- | --- | --- |
| `lerp` | `0.1` | Interpolation per frame (0..1); when set, `duration` and `easing` are ignored |
| `duration` | `1.2` | Seconds, only without `lerp` |
| `smoothWheel` | `true` | Smooth wheel input |
| `syncTouch` | `false` | Imitate touch inertia; unstable on older iOS |
| `autoRaf` | `false` | Run its own rAF loop; leave off when GSAP drives the ticker |
| `anchors` | `false` | Handle anchor links; otherwise they are blocked while scrolling |
| `prevent` | none | `(node) => boolean`; return `true` to leave a subtree native |
| `allowNestedScroll` | `false` | Let nested scrollers scroll natively; walks the DOM on every event |
| `respectReducedMotion` | `true` | Under `reduce`, forces `lerp: 1` and instant programmatic scrolls |

Sync with GSAP ScrollTrigger and tear down with the owning view:

```js
const lenis = new Lenis({ lerp: 0.1, anchors: true });
const tick = (time) => lenis.raf(time * 1000); // GSAP seconds to ms

lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add(tick);
gsap.ticker.lagSmoothing(0);

// On component unmount, tear both down:
// gsap.ticker.remove(tick); lenis.destroy();
```

Constraints:

- Mark native subtrees with `data-lenis-prevent` (or `-wheel`, `-touch`, `-vertical`, `-horizontal`): modals, code blocks, maps, tables.
- No CSS scroll snap: `scroll-snap-type` fights the interpolation. Use the `lenis/snap` package or drop one of the two.
- Iframes do not forward wheel events, so smoothing stops over embeds.
- Include the library's recommended CSS; test find-in-page, Home and End, Space and Page Down.

### Locomotive Scroll

Version 5 is a thin layer over Lenis plus IntersectionObservers for in-view triggers and parallax attributes. The Lenis gate and constraints apply unchanged; it is not the transform-based scroller of earlier majors.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **lenis 1.3.27** (verified) — https://registry.npmjs.org/lenis ; options and defaults from https://github.com/darkroomengineering/lenis (README, main branch)
- **locomotive-scroll 5.0.1** (verified) — https://registry.npmjs.org/locomotive-scroll (depends on lenis)
- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap ; ScrollTrigger and `gsap.matchMedia()` per https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- **Scroll-driven animations support** (verified) — https://registry.npmjs.org/@mdn/browser-compat-data 8.1.6: `animation-timeline` and `animation-range` Chrome 115, Safari 26, Firefox preview; `timeline-scope` Chrome 116, Safari 26
