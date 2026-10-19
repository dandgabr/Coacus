---
name: "ui-motion-interaction"
description: "Provides design engineering patterns for tactile UI motion, micro-interactions, and pointer physics. Covers state transitions (hover, active, focus-visible, drag, disabled), spring physics calibration (stiffness, damping, mass), dynamic pointer tracking (spotlight radial gradients, magnetic cursor pull, 3D card tilt), Dan Saffer's micro-interaction lifecycle, the Accot-Zhai steering law for hover corridors, and strict 60/120fps hardware-composited performance with WCAG prefers-reduced-motion compliance. Use when crafting interactive components, design system motion tokens, or tactile web interfaces."
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

---

## 🏎️ Physics-Based Motion vs. Easing Curves

Choose motion by purpose and interruption needs; neither springs nor short fixed durations are universal requirements. For overlays, active scenes and teardown, use [effect coverage and lifecycle](references/effect-coverage-lifecycle.md). For continuous, revealed, scrubbed or stepped stories, use [scroll narrative modes](references/scroll-narrative-modes.md). These references distinguish visible output from state markers and frame processing from callback cadence.

Duration-based easing suits many transitions. Springs can preserve momentum during interruptible movement; use the approach appropriate to the task and the actual implementation rather than assigning quality by technique alone.

| Dimension | Cubic-Bezier (Duration-based) | Spring Physics (Physics-based) |
| :--- | :--- | :--- |
| **Parameters** | `duration`, `cubic-bezier(x1, y1, x2, y2)` | `stiffness` ($k$), `damping` ($c$), `mass` ($m$) |
| **Interruption** | Retargeting continuity depends on the transition implementation | Can preserve velocity when the solver carries current state |
| **Tactile Feel** | Determined by curve, duration, distance and context | Determined by solver parameters, distance and context |
| **Best For** | Background fades, page opacities, color shifts | Component scaling, modals, drag-and-drop, cursor pull |

### Standard Spring Presets for Design Systems
- **Snappy / Tight (Buttons, Toggles, Micro-actions):**
  - Stiffness: `400`–`500`, Damping: `30`–`35`, Mass: `1.0`
  - Zero visible bounce; instantaneous response (<150ms perceived settling).
- **Smooth / Gentle (Modals, Drawers, Floating Panels):**
  - Stiffness: `250`–`300`, Damping: `25`–`28`, Mass: `1.0`
  - Elegant deceleration with imperceptible overshoot.
- **Bouncy / Playful (Badges, Gamified Toast Alerts, Drop Pins):**
  - Stiffness: `200`–`300`, Damping: `12`–`18`, Mass: `1.0`
  - Explicit elastic rebound for celebratory moments (use sparingly).

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

1. **Control rendering cost:** Prefer compositor-friendly properties when they achieve the effect. Layout-affecting movement needs measurement and a reason; neither a property name nor `will-change` proves hardware acceleration or acceptable cost.
2. **Frame budget evidence:** Derive the budget from the target display and product. Distinguish callback cadence, frame processing, aggregated work and software versus hardware rendering. Use `will-change` conservatively and verify the measured workload.
3. **WCAG 2.2 Criterion 2.2.2 & 2.3.3 (Motion Conformance):**
   - Strictly honor `@media (prefers-reduced-motion: reduce)`:
     ```css
     @media (prefers-reduced-motion: reduce) {
       .motion-decoration { animation: none; transition: none; }
       .revealed-content { opacity: 1; transform: none; clip-path: none; }
       .narrative-owner { scroll-behavior: auto; }
     }
     ```
   - When motion is reduced, expose a complete static result or direct navigation appropriate to the product. Do not rely on a near-zero global duration reset to reveal content or initialize state.
4. **Vestibular Safety:** Avoid full-screen parallax, high-frequency pulsing flashes, or rotational vortex effects that trigger vestibular disorientation in sensitive users.

---

## 📚 References & Standards

- Dan Saffer, *Microinteractions: Designing with Details*, O'Reilly Media, 2013.
- J. Accot and S. Zhai, "Beyond Fitts' Law: Models for Trajectory-Based HCI Tasks", *ACM CHI Proceedings*, 1997.
- Paul M. Fitts, "The information capacity of the human motor system in controlling the amplitude of movement", *Journal of Experimental Psychology*, 1954.
- W3C WAI, "Understanding SC 2.3.3: Animation from Interactions", WCAG 2.2.
