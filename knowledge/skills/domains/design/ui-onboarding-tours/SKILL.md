---
name: "ui-onboarding-tours"
description: "Provides architecture and UX engineering patterns for product tours, contextual walkthroughs, and UI feature highlights modeled after Driver.js paradigms. Covers SVG cutout spotlight masks, target element alignment and positioning, popover step choreography, keyboard navigation (Esc, Tab, Arrow keys), focus management, progressive disclosure, and everboarding telemetry. Use when implementing interactive onboarding tours, guided product walkthroughs, contextual feature announcements, or help popovers."
tags:
  - onboarding
  - product-tours
  - driver-js
  - highlights
  - walkthrough
  - user-experience
---

# UI Onboarding Tours & Contextual Highlights

User onboarding has evolved from passive, multi-screen modal carousels that users immediately dismiss into **contextual, interactive highlights and guided walkthroughs**. Pioneered by lightweight engines like **Driver.js**, modern onboarding shines a focused spotlight on key interface elements at the exact moment of need, minimizing cognitive load and accelerating Time-to-Value (TTV).

---

## 🧭 When to Activate

- Designing or implementing guided tours, product walkthroughs, or interactive tutorials.
- Highlighting newly released UI features, navigation changes, or hidden tools.
- Building non-intrusive, contextual onboarding flows that guide users through their first real task.
- Implementing spotlight overlays with smooth SVG cutout masks and floating popovers.
- Auditing walkthrough flows for keyboard accessibility, focus trapping, and cognitive load.

---

## 🏗️ The Driver.js Architectural Paradigm

The Driver.js pattern represents the state-of-the-art in lightweight, dependency-free UI highlighting. It isolates three distinct visual layers:

```
+-------------------------------------------------------------+
| Browser Viewport                                            |
|                                                             |
|   +-------------------------------------------------------+ |
|   | Full-Screen Backdrop Overlay (darkened opacity)       | |
|   |                                                       | |
|   |            +-----------------------+                  | |
|   |            | Target Element Cutout |                  | |
|   |            | (Clear SVG hole /     |                  | |
|   |            |  smooth border-radius)|                  | |
|   |            +-----------------------+                  | |
|   |                         |                             | |
|   |                         v                             | |
|   |            +---------------------------+              | |
|   |            | Floating Step Popover     |              | |
|   |            | - Title & Microcopy       |              | |
|   |            | - Step 1 of 4 indicators  |              | |
|   |            | - [Skip]  [Next Step →]   |              | |
|   |            +---------------------------+              | |
|   +-------------------------------------------------------+ |
+-------------------------------------------------------------+
```

### 1. SVG Cutout Spotlight Mask
- **The Technique:** Instead of manipulating the z-index of the target DOM element (which breaks stacking contexts, fixed positioning, and CSS transforms), the engine renders an SVG overlay covering the entire viewport.
- **Path Definition:** Uses an SVG `<path>` with the `fill-rule="evenodd"` attribute. The outer path encloses the screen boundaries, while an inner subpath draws an inverted rectangle or rounded polygon matching the target element's exact bounding box (`getBoundingClientRect()`).
- **Smooth Padding:** The cutout adds configurable padding ($4\text{px}$–$12\text{px}$) and border-radius around the target to prevent visual cramping.

### 2. Autonomous Viewport Alignment & Smooth Scroll
- If the target element is outside the current viewport, the engine automatically issues a smooth scroll command (`element.scrollIntoView({ behavior: 'smooth', block: 'center' })`) prior to opening the popover.
- Recalculates bounding coordinates dynamically on browser window resize or orientation changes.

### 3. Floating Popover Positioning Engine
- Positions the descriptive popover adjacent to the spotlight cutout along eight possible sides: `top`, `bottom`, `left`, `right`, with `start`, `center`, or `end` alignments.
- Includes collision detection: if the popover overflows the viewport edge, it automatically flips to the opposing side.

---

## 🧩 Step Choreography & Interaction Rules

A guided tour is a state machine with strict transition guards:

### 1. The Anatomy of a Tour Step
- **Target Selector:** Unique DOM query selector (e.g., `#main-action-button` or `[data-tour="export-menu"]`).
- **Popover Content:**
  - **Title:** Actionable and concise (3–6 words, e.g., *"Create Your First Document"*).
  - **Description:** Outcome-oriented explanation (1–2 sentences explaining what happens when clicked).
  - **Progress Indicator:** Clear step tracking (*"Step 2 of 4"* or visual dot trail).
  - **Navigation Controls:** *"Previous"*, *"Next"*, and an unambiguous *"Skip / Close"* option.
- **Interactive Cutout:** Allows the user to actually click and interact with the highlighted element while the tour is active, advancing the step upon real action.

### 2. Tour Control Flow
```
[ Trigger: First Login / Feature Announcement ]
                      |
                      v
             [ Step 1 Spotlight ] 
                      |
        +-------------+-------------+
        |                           |
  (User clicks Next)         (User clicks Skip / Esc)
        |                           |
        v                           v
  [ Step 2 Spotlight ]       [ Close Overlay & Save State ]
        |
        v
  [ Step N (Final) ]
        |
        v
  [ Completion Confetti / Dismissal & Telemetry Record ]
```

---

## 🧠 Cognitive UX: From Intrusive Tours to "Everboarding"

1. **The 3-Step Rule:** Limit linear tours to a maximum of 3–4 essential steps. Beyond 4 steps, user drop-off and frustration spike exponentially.
2. **Action-Driven over Passive Reading:** Instead of asking the user to click "Next" repeatedly, instruct them to perform an action on the highlighted element. Real muscle memory builds adoption.
3. **Opt-in & Re-playable:** Never trap the user. Always provide an explicit "Skip Tour" button and allow users to restart the guide anytime from a Help or Quick Start menu.
4. **Contextual Triggering (Everboarding):** Introduce guides progressively as the user visits relevant subpages or unlocks advanced tiers, rather than dumping all documentation on day one.

---

## ♿ Accessibility (WCAG 2.2 APG Conformance)

1. **Focus Trap:** When the tour popover opens, focus must shift into the popover dialog (`role="dialog" aria-modal="true"`). The Tab key cycles strictly within the popover controls until dismissed.
2. **Keyboard Shortcuts:**
   - `Escape`: Instantly cancels and closes the tour overlay.
   - `Right Arrow` / `Enter`: Advances to the next step.
   - `Left Arrow`: Returns to the previous step.
3. **Screen Reader Announcements:** The target element's context and the popover title must be announced via an `aria-live="polite"` region.
4. **Target Restoration:** Upon closing the tour, keyboard focus must gracefully return to the element that triggered the walkthrough or the last active target element.

---

## 📚 References & Standards

- Driver.js Architecture & API Specification, MIT License.
- W3C WAI ARIA Authoring Practices Guide (APG), Dialog (Modal) Pattern.
- Nielsen Norman Group, "Product Tours and Onboarding: 5 Design Guidelines", 2024.
- W3C Web Content Accessibility Guidelines (WCAG) 2.2, Guideline 2.1 (Keyboard Accessible).
