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

Motion is not visual ornament; it is a spatial and temporal feedback system that communicates state, causality, and intent. In modern digital interfaces, static state changes feel artificial. Tactile motion grounded in physical spring dynamics transforms flat digital surfaces into responsive, tangible tools.

---

## 🧭 When to Activate

- Implementing or specifying hover, active, focus, drag, or loading states on interactive elements.
- Designing magnetic cursor attractions, spotlight radial borders, or 3D tilt effects on cards.
- Configuring design system motion tokens (duration tiers, easing curves, spring physics parameters).
- Preventing menu closing errors using the Accot-Zhai steering law for dropdowns and hover corridors.
- Auditing UI animations for 60fps/120fps compositor execution and WCAG motion accessibility.

---

## 🏎️ Physics-Based Motion vs. Easing Curves

Traditional UI animation relied on fixed-duration cubic-bezier curves. Modern high-craft interfaces prioritize **spring physics** because springs preserve momentum, adapt fluidly to user interruption, and eliminate artificial deceleration halts.

| Dimension | Cubic-Bezier (Duration-based) | Spring Physics (Physics-based) |
| :--- | :--- | :--- |
| **Parameters** | `duration`, `cubic-bezier(x1, y1, x2, y2)` | `stiffness` ($k$), `damping` ($c$), `mass` ($m$) |
| **Interruption** | Resets or snaps awkwardly mid-flight | Preserves velocity and redirects naturally |
| **Tactile Feel** | Mechanical and scripted | Organic, elastic, and physical |
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
2. **Hover:** Immediate micro-lift (`translateY(-1px to -2px)`), subtle surface luminosity gain, or border glow.
3. **Active / Pressed:** Physical compression (`scale(0.97–0.98)` or `translateY(1px)`), increased shadow compactness.
4. **Focus-Visible:** High-contrast outline offset (`outline: 2px solid var(--accent); outline-offset: 2px;`), never suppressed without replacement.
5. **Disabled:** Desaturated, reduced opacity (`0.4–0.5`), `pointer-events: none;`, `cursor: not-allowed;`.

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

1. **Hardware-Accelerated Properties Only:** Animate strictly `transform` and `opacity`. Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`), which cause browser reflow and frame drops.
2. **The 60/120fps Frame Budget:** Each frame must render in under $16.6\text{ms}$ ($8.3\text{ms}$ on 120Hz displays). Use `will-change: transform` conservatively on frequently animated layers.
3. **WCAG 2.2 Criterion 2.2.2 & 2.3.3 (Motion Conformance):**
   - Strictly honor `@media (prefers-reduced-motion: reduce)`:
     ```css
     @media (prefers-reduced-motion: reduce) {
       *, *::before, *::after {
         animation-duration: 0.01ms !important;
         animation-iteration-count: 1 !important;
         transition-duration: 0.01ms !important;
         scroll-behavior: auto !important;
       }
     }
     ```
   - When motion is reduced, replace spatial movement and camera zooms with immediate opacity fades.
4. **Vestibular Safety:** Avoid full-screen parallax, high-frequency pulsing flashes, or rotational vortex effects that trigger vestibular disorientation in sensitive users.

---

## 📚 References & Standards

- Dan Saffer, *Microinteractions: Designing with Details*, O'Reilly Media, 2013.
- J. Accot and S. Zhai, "Beyond Fitts' Law: Models for Trajectory-Based HCI Tasks", *ACM CHI Proceedings*, 1997.
- Paul M. Fitts, "The information capacity of the human motor system in controlling the amplitude of movement", *Journal of Experimental Psychology*, 1954.
- W3C WAI, "Understanding SC 2.3.3: Animation from Interactions", WCAG 2.2.
