---
name: "ui-scroll-driven-motion"
description: "Provides implementation mechanics for scroll-triggered and scroll-linked web motion: IntersectionObserver reveals, CSS scroll and view timelines (animation-timeline, animation-range, timeline-scope), GSAP ScrollTrigger, smooth-scroll libraries such as Lenis, parallax, sticky positioning, faux-horizontal sections, scroll snapping, overscroll control and canvas image sequences. Use when building scroll animations, scrubbed or pinned scenes, snap carousels, pull-to-refresh or scroll-driven image sequences, when sticky positioning does not stick, or when reviewing scroll motion for browser support, reduced motion or performance."
tags:
  - scroll-driven-animation
  - scroll-timeline
  - intersection-observer
  - scrolltrigger
  - smooth-scroll
  - sticky-positioning
  - scroll-snap
  - web-animation
---

# UI Scroll-Driven Motion

Scroll is the user's own input. Motion attached to it follows the input, never replaces it, and leaves a complete page when motion is unavailable or unwanted. This skill owns the mechanics; narrative and depth styles live in the style skills linked below.

---

## 🧭 When to Activate

- Revealing content when it enters the viewport, or scrubbing a visual state with scroll progress.
- Choosing between IntersectionObserver, CSS scroll/view timelines, GSAP ScrollTrigger and a smooth-scroll library.
- Building parallax layers, sticky headers or pinned scenes, faux-horizontal sections, snap carousels or pull-to-refresh.
- Playing an image or video sequence keyed to scroll.
- Reviewing scroll motion for support gaps, reduced motion, keyboard reachability or main-thread cost.

---

## 🗺️ Narrative Mode Before Mechanism

Decide what scroll controls before choosing an implementation.

| Mode | What scroll controls | Native expectation |
| --- | --- | --- |
| Continuous reading | Position in a normal document | Content remains directly scrollable |
| Threshold reveal | Appearance or annotation at a boundary | Scrolling remains continuous |
| Pin and scrub | A scene's visual state through an interval | Input continues through the interval |
| Stepped presentation | Movement between discrete scenes | Each scene has a reachable destination |

A long page is not a deck, and a scene class changing does not prove a transition is visible. Prefer native scrolling, anchors and snap. Stepped presentations need extra contracts; see [sticky, snap and overscroll](references/sticky-snap-overscroll.md).

---

## 🌳 Decision Tree

1. **Fires once when an element arrives?** IntersectionObserver: toggle a class, then `unobserve`.
2. **Tied continuously to progress (scrub, parallax, progress bar)?**
   - Only `transform`, `opacity` or `filter`, and a static result is acceptable where unsupported: CSS `scroll()` / `view()` timelines behind `@supports`.
   - Needs sequencing, pinning, callbacks or identical behavior in every engine: GSAP ScrollTrigger.
3. **Inertial, eased wheel scrolling explicitly required?** Only then a smooth-scroll library, through the gate below. Native `scroll-behavior: smooth` covers anchor jumps.
4. **Frame sequence?** Follow [canvas image sequence](references/canvas-image-sequence.md); hand WebGL scenes to [ui-gpu-graphics-web](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md).

| Criterion | IntersectionObserver | CSS scroll/view timeline | GSAP ScrollTrigger | Smooth-scroll library |
| --- | --- | --- | --- | --- |
| Output | One-shot state change | Progress-linked keyframes | Progress-linked timelines, pins, callbacks | Replaces wheel scrolling |
| Thread | Main (callback only) | Compositor for transform/opacity/filter | Main | Main, every frame |
| Support | Universal | Limited | Universal (library) | Universal (library) |
| Cost of failure | Content must still be visible | Static fallback | Content must still be visible | Breaks scrolling itself |

Recipes for all four live in [CSS scroll timelines](references/css-scroll-timelines.md).

---

## 📊 Support Matrix

| Feature | Status | Browsers | Fallback |
| --- | --- | --- | --- |
| IntersectionObserver | Baseline widely available | All current | None needed (base path) |
| `animation-timeline` with `scroll()` / `view()`, `animation-range` | Limited | Chrome 115, Safari 26; Firefox preview only | IntersectionObserver class toggle or static layout |
| `timeline-scope` | Limited | Chrome 116, Safari 26 | Make the timeline source an ancestor |
| Scroll-triggered animations (`animation-trigger`) | Limited | Chrome 146 only | IntersectionObserver |
| `position: sticky` | Baseline widely available | All current | Static flow |
| `overflow: clip` | Baseline widely available (2025-03-12) | All current | Move clipping off the sticky ancestor chain |
| Scroll-state container queries | Limited | Chrome 133 (`scrolled` 144) | No stuck styling, or a sentinel observer |
| Scroll snap | Baseline widely available | All current | Free scrolling |
| `scroll-snap-stop` | Broad | Chrome 75, Firefox 103, Safari 15 | Normal snap |
| `scrollsnapchange` / `scrollsnapchanging` | Limited | Chrome 129 only | `scrollend` plus nearest-item calculation |
| `::scroll-button()`, `::scroll-marker`, `scroll-marker-group` | Limited | Chrome 135 only | Real buttons and anchor links |
| `scrollend` | Baseline newly available (2025-12-12) | Chrome 114, Firefox 109, Safari 26.2 | Debounced `scroll` |
| `scroll-behavior` | Baseline widely available (2024-09-14) | All current | Instant jump |
| `overscroll-behavior` | Limited (full spec); older partial behaviour works in all engines | Chrome 63, Firefox 59, Safari 16 (non-overflowing containers: Chrome 144, Firefox 150) | Scroll lock on the document |

---

## 📏 Core Rules

1. **Content is visible without JavaScript.** Never ship `opacity: 0` that only a script or timeline can undo. Hide pre-reveal state only under a script-added class or inside `@supports`, so a failed script or unsupported engine shows the finished page.
2. **Base path first.** Write the static layout, then layer motion inside `@supports (animation-timeline: scroll())` or after feature detection. Chrome-only features never carry content or controls alone.
3. **Off-main-thread only for `transform`, `opacity` and `filter`.** Timelines driving layout or paint properties (`height`, `clip-path`, `mask`) run on the main thread each frame; measure first.
4. **Refresh after layout changes.** Trigger positions are cached; recalculate (`ScrollTrigger.refresh()`) after `document.fonts.ready`, image loads, accordions and route changes.
5. **Reduced motion means a static layout.** Under `prefers-reduced-motion: reduce`, unpin, drop scrub and parallax, show every step in normal flow. (house policy; see the canonical accessibility section).
6. **Progress-driven motion has no duration** and no easing lag. Triggered reveals take durations from [motion timing engines](../ui-motion-interaction/references/motion-timing-engines.md).
7. **Own and release resources.** Observers, triggers, smooth-scroll instances and rAF loops die with their mounting context; see the lifecycle contract in [frontend-developer](../../../roles/frontend-developer/SKILL.md).

---

## 🚫 Default: No

> **Smooth-scroll hijacking libraries on wheel input** (Lenis, Locomotive Scroll)
> - **Allowed when:** the brief explicitly requires synchronized scroll for a WebGL or pinned scene, and reduced motion disables smoothing.
> - **Evidence required:** wheel, trackpad, keyboard, find-in-page, anchors, nested scrollers and iframes tested; frame timing measured on a low-end device.
> - **Fallback:** native scrolling with `scroll-behavior: smooth` inside `@media (prefers-reduced-motion: no-preference)`.

> **Faux-horizontal sections** (vertical scroll translated into horizontal travel)
> - **Allowed when:** the content is a short visual sequence, not reading material, and every item is reachable by keyboard.
> - **Evidence required:** `focusin` scrolls to the focused item; narrow-viewport and reduced-motion layouts tested at 320 CSS px (1.4.10).
> - **Fallback:** a vertical stack or a native horizontal scroller with snap and buttons.

> **`scroll-snap-type: mandatory` with tall items**
> - **Allowed when:** every snap item is guaranteed shorter than the scrollport at all supported sizes and zoom levels.
> - **Evidence required:** tested at 200% zoom and short landscape viewports; no item's end becomes unreachable.
> - **Fallback:** `proximity`.

> **Scroll-driven image sequences**
> - **Allowed when:** the sequence carries information a video or still cannot, and a memory budget is set.
> - **Evidence required:** decoded-memory math, mid-range mobile test without tab reload, text alternative present.
> - **Fallback:** a poster image plus optional user-started video.

---

## 🏔️ Parallax

Layers translated by a named `view()` timeline, with a one-loop rAF `transform` fallback. Keep depth small; never move body text. Recipes in [CSS scroll timelines](references/css-scroll-timelines.md); history in [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md).

## 📌 Sticky

Sticky fails silently when an ancestor creates a scroll container; use `overflow: clip`. Keep sticky bars off focused elements (2.4.11). See [sticky, snap and overscroll](references/sticky-snap-overscroll.md).

## 🧲 Snapping

Prefer `proximity`, add `scroll-padding` for fixed headers, and give carousels previous/next buttons (2.5.7). See [sticky, snap and overscroll](references/sticky-snap-overscroll.md).

## 🌊 Overscroll

`overscroll-behavior: contain` stops scroll chaining from panels and dialogs; custom pull-to-refresh needs a refresh button. See [sticky, snap and overscroll](references/sticky-snap-overscroll.md).

---

## ♿ Accessibility

Canonical obligations live in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md). Scroll-specific checks:

- **2.2.2:** loops started by scrolling into view get a visible pause control.
- **2.3.3:** scrub, parallax and pinning disappear on the static path.
- **2.4.11:** sticky headers and pinned scenes never entirely hide the focused element; reserve space with `scroll-padding-top`.
- **2.5.7:** carousels, horizontal tracks and pull-to-refresh offer buttons.
- **1.4.10:** horizontal travel collapses to vertical flow at narrow widths.

Nothing may depend on a wheel event.

---

## ✅ Acceptance

Exercise forward and back gestures, keyboard, a scene taller than the screen, focus in a field, resize mid-scrub and leaving the narrative. Assert visible output at fixed scroll positions, endpoints, cleanup, the unsupported-engine fallback and the reduced-motion layout. Keep a continuous-reading control case so a rule does not turn every article into slides.

---

## 🔗 Cross-Skill Integration

- Motion hub and tokens: [ui-motion-interaction](../ui-motion-interaction/SKILL.md).
- Narrative style: [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md).
- Depth style: [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md).
- WebGL and GPU scenes: [ui-gpu-graphics-web](../../../engineering/practices/ui-gpu-graphics-web/SKILL.md).
- Lifecycle and cleanup contract: [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- State changes, clip reveals and scroll-linked SVG line drawing: [ui-state-layout-transitions](../ui-state-layout-transitions/SKILL.md).
- Drag, swipe and fling on carousels and horizontal tracks: [pointer-and-gesture](../ui-motion-interaction/references/pointer-and-gesture.md).

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **web-features 3.43.0** (verified) — https://registry.npmjs.org/web-features (Baseline statuses and dates in the support matrix)
- **@mdn/browser-compat-data 8.1.6** (verified) — https://registry.npmjs.org/@mdn/browser-compat-data (browser versions in the support matrix)
- **lenis 1.3.27** (verified) — https://registry.npmjs.org/lenis
- **locomotive-scroll 5.0.1** (verified) — https://registry.npmjs.org/locomotive-scroll
- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap
