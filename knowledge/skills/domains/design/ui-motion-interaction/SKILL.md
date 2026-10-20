---
name: "ui-motion-interaction"
description: "Provides the motion hub for UI design engineering: tactile state transitions (hover, active, focus-visible, drag, disabled), pointer physics (spotlight gradients, magnetic pull, 3D tilt), the Accot-Zhai steering law for hover corridors, Dan Saffer's micro-interaction lifecycle, canonical duration bands and spring tokens (stiffness, damping, damping ratio, overshoot), interruption and retargeting behaviour, rendering performance for animation (compositor-friendly properties, forced layout, will-change, INP) and reduced-motion handling. Use when crafting interactive components, defining design system motion tokens, choosing between easing and springs, or auditing animation smoothness and motion accessibility."
tags:
  - motion-design
  - micro-interactions
  - hover-effects
  - spring-physics
  - interaction-design
  - web-animation
---

# UI Motion & Tactile Interaction Engineering

Motion is not visual ornament; it is a spatial and temporal feedback system that communicates state, causality, and intent. Static changes are appropriate when clarity, accessibility or the visual language calls for them. Use tactile motion when it improves feedback rather than treating animation as evidence of quality.

---

## 🧭 When to Activate

- Implementing or specifying hover, active, focus, drag, or loading states on interactive elements.
- Designing magnetic cursor attractions, spotlight radial borders, or 3D tilt effects on cards.
- Configuring design system motion tokens (duration tiers, easing curves, spring physics parameters).
- Preventing menu closing errors using the Accot-Zhai steering law for dropdowns and hover corridors.
- Auditing UI animations for 60fps/120fps compositor execution and WCAG motion accessibility.

### Motion hub routing

- Durations, easing, spring tokens, interruption, Web Animations API, motion tokens: [motion-timing-engines](references/motion-timing-engines.md) (single source; do not restate values elsewhere).
- Overlay coverage, active scenes and teardown: [effect-coverage-lifecycle](references/effect-coverage-lifecycle.md).
- Scroll-linked and scroll-triggered motion: the ui-scroll-driven-motion skill (planned).
- View Transitions, FLIP, shared-element and accordion/layout transitions: the ui-state-layout-transitions skill (planned).
- Pointer and gesture recipes, text-effect recipes: the hub references pointer-and-gesture.md and text-effect-recipes.md (planned).

---

## 🏎️ Physics-Based Motion vs. Easing Curves

Choose motion by purpose and interruption needs; neither springs nor short fixed durations are universal requirements. For overlays, active scenes and teardown, use [effect coverage and lifecycle](references/effect-coverage-lifecycle.md). For continuous, revealed, scrubbed or stepped stories, use [scroll narrative modes](references/scroll-narrative-modes.md). These references distinguish visible output from state markers and frame processing from callback cadence.

| Dimension | Cubic-Bezier (Duration-based) | Spring Physics (Physics-based) |
| :--- | :--- | :--- |
| **Parameters** | `duration`, `cubic-bezier(x1, y1, x2, y2)` | `stiffness` ($k$), `damping` ($c$), `mass` ($m$) |
| **Interruption** | Retargeting continuity depends on the transition implementation | Can preserve velocity when the solver carries current state |
| **Best For** | Background fades, page opacities, color shifts | Component scaling, modals, drag-and-drop, cursor pull |

### Canonical Spring Tokens

Values (k, c, ζ, overshoot, settle time, Motion mapping) live only in [motion-timing-engines](references/motion-timing-engines.md#3-spring-model-and-canonical-presets).

| Token | Use |
| :--- | :--- |
| `spring.snap` | Press feedback, toggles, small controls (no overshoot) |
| `spring.smooth` | Menus, drawers, modals, layout moves |
| `spring.playful` | Celebratory badges, rare delight (visible bounce) |

Damping ratio ζ, not stiffness, decides bounce. Effects (opacity, colour) never overshoot.

---

## 🎯 State Dynamics & Hover Craft

### 1. The Multi-State Component Continuum
Every interactive component must define a coherent continuum across all physiological states:
1. **Rest / Default:** Semantic baseline color, elevation, and opacity.
2. **Hover:** An appropriate visible cue; optional lift, luminance change or glow must preserve hit areas and reading ink.
3. **Active / Pressed:** An appropriate pressed cue; physical compression is optional and must not displace essential content.
4. **Focus-Visible:** High-contrast outline offset (`outline: 2px solid var(--accent); outline-offset: 2px;`), never suppressed without replacement.
5. **Disabled:** Expose the correct disabled semantics and recognizable state. Visual attenuation depends on the surrounding surface; pointer suppression alone does not disable keyboard activation or communicate state.

### 2. Spotlight & Cursor-Tracking Borders
- **Mechanism:** Mouse position is tracked locally via pointer events and mirrored into CSS custom properties (`--mouse-x`, `--mouse-y`) on the target element.
- **Rendering:** A radial gradient layer masked behind the border renders a luminous spotlight that follows the cursor:
  ```css
  .spotlight-card {
    position: relative;
    background: radial-gradient(
      400px circle at var(--mouse-x, 0px) var(--mouse-y, 0px),
      rgba(255, 255, 255, 0.08),
      transparent 80%
    );
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: border-color 0.25s ease;
  }
  ```

### 3. Magnetic Pointer Attraction
- **Mechanism:** When the pointer enters the proximity bounding box of an element (e.g., within 30px of a circular action button), the button translates toward the cursor at a fractional ratio (e.g., $0.2 \times \Delta x, 0.2 \times \Delta y$).
- **Settling:** On pointer exit, a snappy spring restores the element to its origin with zero residual offset.

### 4. 3D Card Tilt with Specular Sheen
- **Mechanism:** Rotates cards in 3D perspective (`perspective(1000px) rotateX(...) rotateY(...)`) proportional to cursor distance from the card center.
- **Restraint:** Maximum tilt angle should not exceed $4^\circ$ to $8^\circ$ to prevent text distortion and eye strain.

---

## 🧠 Motor Ergonomics: Accot-Zhai Steering Law & Hover Corridors

The **Accot-Zhai Steering Law** models the time required to navigate a pointer through a constrained tunnel:

$$T = a + b \int_C \frac{ds}{W(s)}$$

Where $C$ is the straight or curved path and $W(s)$ is the tunnel width.

### Practical Application for Menus and Tooltips:
- **The Triangle Safety Corridor:** When hovering from a top-level menu item to a submenu located to the right or below, human users move in diagonal arcs rather than perpendicular paths.
- **The Problem:** Moving diagonally causes the pointer to temporarily exit the parent item's bounding box, collapsing the submenu prematurely.
- **The Solution:** Establish an invisible triangular hit-testing corridor between the cursor and the submenu boundaries, or introduce an intentional **debounce buffer** (100ms–200ms) before triggering exit transitions.

---

## 🔄 Dan Saffer's Micro-Interaction Architecture

Every micro-interaction consists of four discrete stages:
1. **Trigger:** User-initiated (click, hover, swipe) or system-initiated (threshold exceeded, message arrived).
2. **Rules:** Logic governing behavior (e.g., "if button is disabled, reject click; if active, trigger spring compression").
3. **Feedback:** Instant visual, auditory, or haptic verification (e.g., button scale change, checkmark morphing).
4. **Loops & Modes:** Meta-rules controlling duration, repetitions, or context shifts (e.g., toggled into dark mode).

---

## ♿ Accessibility, Motion Sickness & Performance

Canonical obligations live in [web-accessibility-wcag, Motion and Animation](../../../engineering/practices/web-accessibility-wcag/SKILL.md). Honour reduced motion everywhere: it is WCAG technique C39 and Coacus house policy, not an AA requirement.

Author no-motion first: opt into spatial motion only when the user has no preference, and keep a reduce fallback for motion that is set elsewhere.

```css
.revealed-content { opacity: 1; transform: none; }   /* static result is the default */

@media (prefers-reduced-motion: no-preference) {
  .revealed-content:not(.is-visible) { opacity: 0; transform: translateY(12px); }
  .revealed-content { transition: opacity 220ms ease-out, transform 220ms ease-out; }
}

@media (prefers-reduced-motion: reduce) {
  .motion-decoration { animation: none; transition: none; }
  .narrative-owner { scroll-behavior: auto; }
  .state-change { transition: opacity 120ms linear; }  /* fade replaces travel */
}
```

When motion is reduced, expose a complete static result or direct navigation. Do not rely on a near-zero global duration reset to reveal content or initialise state. Avoid full-screen parallax, flashing, and rotational or zooming vortex effects.

### Rendering performance for animation

- **Compositor-friendly:** `transform` and `opacity`; `filter` sometimes (cheap blurs, browser-dependent). Width, height, top/left, margin, padding and font metrics trigger layout; colour, shadow, border-radius, `clip-path` and masks trigger paint. Neither a property name nor `will-change` proves acceleration: measure.
- **Read, then write:** batch all layout reads (`getBoundingClientRect`, `offsetWidth`) before any style writes in a frame. Interleaving forces synchronous layout (layout thrashing). Depth: [javascript-high-performance](../../../languages/javascript-high-performance/SKILL.md).
- **`will-change` lifecycle:** add it just before the motion (e.g. on `pointerenter`), remove it on `transitionend`/`finished`. Permanent or blanket use creates a layer explosion and wastes GPU memory; treat it as a last resort.
- **INP:** good ≤ 200 ms, poor > 500 ms at p75. Start visual feedback in the same frame as the input; defer heavy work. Core Web Vitals context: [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- **Long Animation Frames (Chrome/Edge only):** `PerformanceObserver` type `long-animation-frame` exposes `blockingDuration` and `scripts[].forcedStyleAndLayoutDuration` to attribute forced layout to the script that caused it.
- **Offscreen work:** `content-visibility: auto` with `contain-intrinsic-size` skips rendering for offscreen sections; pause animations there too.
- **Frame budget:** 16.6 ms at 60 Hz, 8.3 ms at 120 Hz; distinguish callback cadence from frame processing.

---

## 📚 References & Standards

- Dan Saffer, *Microinteractions: Designing with Details*, O'Reilly Media, 2013.
- J. Accot and S. Zhai, "Beyond Fitts' Law: Models for Trajectory-Based HCI Tasks", *ACM CHI Proceedings*, 1997.
- Paul M. Fitts, "The information capacity of the human motor system in controlling the amplitude of movement", *Journal of Experimental Psychology*, 1954.
- W3C WAI, "Understanding SC 2.3.3: Animation from Interactions", WCAG 2.2.
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, 12 December 2024 edition; technique C39.

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **WCAG 2.2** (verified) — W3C Recommendation, 12 December 2024 edition, https://www.w3.org/TR/WCAG22/
- **INP thresholds** (verified) — good ≤ 200 ms, poor > 500 ms at p75, https://web.dev/articles/inp
- **Long Animation Frames API** (verified) — Chrome/Edge 123 only, MDN BCD 8.1.6, https://developer.mozilla.org/en-US/docs/Web/API/PerformanceLongAnimationFrameTiming
- **`content-visibility`** (verified) — Baseline 2024 (Chrome 85, Firefox 125, Safari 18), web-features 3.43.0, https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility
