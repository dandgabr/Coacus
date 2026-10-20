---
name: "ui-state-layout-transitions"
description: "Provides the mechanics for animating UI state and layout changes on the web: same-document and cross-document View Transitions, FLIP and shared-element layout animation (vanilla WAAPI, GSAP Flip, Motion layout and layoutId), entry and exit primitives (@starting-style, transition-behavior: allow-discrete, popover and dialog), auto-height accordions, clip-path and mask reveals, skeleton and shimmer loaders, and SVG morphing and line drawing. Use when building a page transition or shared element transition, when a list reorders, a card expands into a detail view, a route or tab changes, an overlay opens or closes, a panel collapses, content loads behind a skeleton loader, or an SVG path must morph or draw itself."
tags:
  - view-transitions
  - flip-animation
  - layout-animation
  - entry-exit-transitions
  - accordion
  - skeleton-loading
  - svg-animation
---

# UI State & Layout Transitions

A state transition explains a change: where an element went, what replaced it, what is still loading. Build the state change first so it works without animation, then layer the transition on top as an enhancement that can be skipped, interrupted or reduced without losing information.

---

## 🧭 When to Activate

- A list filters, sorts or reorders and items must glide to their new slots.
- A thumbnail expands into a detail view, or a route or tab change needs continuity.
- A popover, dialog, menu or toast needs an entry and an exit animation.
- An accordion or disclosure must animate to and from `height: auto`.
- Content loads behind a skeleton, or a section reveals with a clip or mask.
- An SVG icon morphs between shapes, or an outline draws itself.

---

## 🗺️ Decision Table: State Change to Technique

| State change | Technique | Reference |
|---|---|---|
| Whole view or region swaps (tab, filter result, SPA route) | Same-document View Transition (`document.startViewTransition`) | [view-transitions.md](references/view-transitions.md) |
| Multi-page site navigation, same origin | Cross-document View Transition (`@view-transition { navigation: auto; }`) | [view-transitions.md](references/view-transitions.md) |
| Items move inside a live, interactive layout (reorder, grid reflow, expand in place) | FLIP / layout animation (WAAPI, GSAP Flip, Motion `layout`) | [flip-layout-animation.md](references/flip-layout-animation.md) |
| Element is inserted or shown for the first time | `@starting-style` entry transition | [reveal-collapse-loading.md](references/reveal-collapse-loading.md) |
| Element leaves via `display: none`, popover or `<dialog>` close | Discrete exit with `transition-behavior: allow-discrete` (+ `overlay` in Chromium) | [reveal-collapse-loading.md](references/reveal-collapse-loading.md) |
| Panel opens to intrinsic height | Grid `0fr ↔ 1fr` accordion; `<details>` with `::details-content` | [reveal-collapse-loading.md](references/reveal-collapse-loading.md) |
| Section or media reveals | `clip-path` / `mask-image` reveal | [reveal-collapse-loading.md](references/reveal-collapse-loading.md) |
| Data is in flight | Skeleton matching the final layout, optional shimmer | [reveal-collapse-loading.md](references/reveal-collapse-loading.md) |
| Icon or shape changes form, outline traces itself | SVG `d` morph / MorphSVG; `stroke-dashoffset` line drawing | [svg-path-animation.md](references/svg-path-animation.md) |

Rule of thumb: a View Transition animates **snapshots** while the live DOM is already final; FLIP animates the **live elements**. Choose FLIP when the user may keep interacting during the motion; choose a View Transition when the swap is atomic.

---

## 🌐 Support Matrix

Resolved against web-features and MDN browser-compat-data (see Version Sources).

| Feature | Baseline / browsers | Fallback |
|---|---|---|
| Same-document View Transitions | Baseline newly available 2025-10-14 (Chrome 111, Firefox 144, Safari 18) | Call the update directly; the DOM changes instantly |
| `view-transition-class`, transition types | Baseline newly 2025-10-14 / 2026-01-13 | Style by `view-transition-name` only |
| Cross-document View Transitions | Not Baseline: Chrome 126, Safari 18.2, no Firefox | Normal navigation |
| Nested groups, element-scoped transitions, `waitUntil()` | Chromium only (140 / 147 / 144) | Document-scoped flat transition |
| `@starting-style`, `transition-behavior` | Baseline newly 2024-08-06 | Element appears without transition |
| Transitioning `display` | Chrome 117, Safari 18; not Firefox | Exit is instant in Firefox |
| `overlay` property | Chrome 117 only | Top-layer exit snaps closed |
| `interpolate-size`, `calc-size()` | Chrome 129 only | Grid `0fr ↔ 1fr` |
| `::details-content` / `<details name>` | Baseline newly 2025-09-16 / 2024-09-03 | Instant disclosure |
| `clip-path` animation; `shape()` | Widely available; `shape()` Baseline newly 2026-02-24 | `inset()` / `polygon()` |
| CSS `d: path()` | Chrome 52, Firefox 97; Safari parses it with no effect | JS morph or crossfade two paths |
| Web Animations API (FLIP) | Widely available | Instant reflow |

---

## 📏 Core Rules

1. **Base path first, enhancement second.** Write the instant state change, then add the transition behind `@supports` or a feature check (`if (!document.startViewTransition) return update()`). Never hide content at rest waiting for an animation to reveal it.
2. **Restore focus after every DOM swap (2.4.3 Focus Order).** When the focused element is replaced, move focus to the equivalent element in the new state, or to the new region's heading (`tabindex="-1"`). Do it in the update callback, not after the animation ends, so keyboard users never sit on a detached node.
3. **Collapsed and clipped content is `inert`.** Anything visually hidden by `0fr`, `clip-path`, a mask or an exit animation must be removed from the tab order and the accessibility tree until it is revealed.
4. **Reduced motion means cross-fade or instant.** Under `prefers-reduced-motion: reduce`, drop positional and scale movement; keep a short opacity cross-fade or swap instantly. Honouring the query is a Coacus house policy (WCAG technique C39), not an AA requirement.
5. **Define interruption per technique.** A CSS transition reverses from its current value; a View Transition is skipped or replaced when a new one starts (the old snapshot jumps to final); FLIP must read the element's current transformed box before computing the next inversion; GSAP Flip and Motion retarget from the in-flight state. Follow the retargeting rules in [motion-timing-engines.md](../ui-motion-interaction/references/motion-timing-engines.md).
6. **Use the house timing tokens.** Write durations as `var(--motion-state)`, `var(--motion-layout)`, `var(--motion-route)` (and `var(--motion-narrative)` only for decorative, non-blocking draws), with `--ease-enter` / `--ease-exit`, as defined in [motion-timing-engines.md](../ui-motion-interaction/references/motion-timing-engines.md); never invent values per component.
7. **Measure what repaints.** `clip-path`, `mask-image`, SVG `d` and `stroke-dashoffset` repaint every frame; profile on a mid-range device before shipping a large or long-running one.

---

## ⚛️ Framework Notes

- **React.** `<ViewTransition>` and `addTransitionType` are stable since React 19.3 (React blog, 2026-09-09). React calls `startViewTransition` itself: never call it manually around React updates, because React interrupts competing transitions. Only Transitions, `<Suspense>` reveals and `useDeferredValue` activate it; a plain `setState` does not, and a `flushSync` inside the sequence skips the animation. On older React lines, use the `flushSync` fallback in [view-transitions.md](references/view-transitions.md#framework-integration-snippets). Names must be unique among mounted boundaries, or React throws. React does not apply reduced motion for you.
- **Next.js.** In the App Router, route navigations are Transitions, so `<ViewTransition>` animates them with no configuration on current releases. Older releases gated this behind `experimental.viewTransition`; the flag was inert and has been removed. Tag direction with the `transitionTypes` prop on `<Link>` or in `router.push()`.
- **Vue.** `<Transition>` (enter/leave classes, `mode="out-in"`) and `<TransitionGroup>` (FLIP-based `move-class`) are the stable path. For route-level View Transitions, use the `viewTransition` prop on `<RouterLink>` for link clicks, or start the transition in a `router.beforeResolve` guard and finish it after `nextTick()` in `afterEach` so back and forward navigations are covered too ([view-transitions.md](references/view-transitions.md) has the guard).
- **Motion `layoutId` and View Transitions do not mix on one element.** A View Transition snapshots the old and new DOM and animates pseudo-elements over a live DOM that is already final, so Motion measures and animates elements hidden beneath the snapshot overlay. Shared-element continuity from `layoutId` does not survive the snapshot swap. Pick one system per element.
- Cleanup, SSR and hydration rules for animation code live in the "Motion in Component Lifecycles" section of the [frontend-developer role skill](../../../roles/frontend-developer/SKILL.md); framework idioms in [framework-react](../../../frameworks/framework-react/SKILL.md) and [framework-vue](../../../frameworks/framework-vue/SKILL.md).

---

## ♿ Accessibility

The canonical success criteria, levels and tests are in the "Motion and Animation" section of [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md). Specific to this skill:

- Pointer input during the snapshot overlay: see [Interaction During the Snapshot](references/view-transitions.md#interaction-during-the-snapshot).
- Looping shimmers, indefinite loaders and looping SVG draws need a stop mechanism under 2.2.2 Pause, Stop, Hide.
- Announce load completion with a status message (4.1.3), not by animation alone.
- Expanded state is exposed with native `<details>` or `aria-expanded` and `aria-controls` on a real `<button>`.

---

## 🔗 Integration with Other Skills

- Motion hub, tokens and engine choice: [ui-motion-interaction](../ui-motion-interaction/SKILL.md).
- Single-action feedback style: [ui-style-micro-interactions](../ui-style-micro-interactions/SKILL.md).
- Draw-on strokes in a sketch voice: [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md).
- Table and dashboard loading states: [ui-data-tables-dashboards](../ui-data-tables-dashboards/SKILL.md).
- Forced reflow and main-thread budgets: [javascript-high-performance](../../../languages/javascript-high-performance/SKILL.md).
- Scroll-linked variants (a path drawn by scroll position) belong to [ui-scroll-driven-motion](../ui-scroll-driven-motion/SKILL.md).

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **Baseline statuses** (verified) — web-features 3.43.0, https://www.npmjs.com/package/web-features
- **Browser versions** (verified) — @mdn/browser-compat-data 8.1.6 (2026-10-15), https://www.npmjs.com/package/@mdn/browser-compat-data
- **React 19.3, `<ViewTransition>` stable** (verified) — https://react.dev/blog/2026/09/09/react-19-3 ; npm `react` 19.3.1 (2026-10-14) exports `ViewTransition`. Divergence: the Context7 index of react.dev still labels it Canary/Experimental; the newer publisher post wins.
- **Next.js, no config flag** (verified) — https://nextjs.org/docs/app/guides/view-transitions (updated 2026-10-15; npm `next` 16.4.2); Context7 `/vercel/next.js` notes `experimental.viewTransition` was inert and removed (vercel/next.js PR 96098).
- **Vue 3.5.44, vue-router 5.4.0 `viewTransition` prop** (verified) — https://router.vuejs.org/api/interfaces/RouterLinkProps.html ; npm registry.
