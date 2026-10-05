---
name: "ui-style-micro-interactions"
description: "Provides the micro-interaction-driven UI style (2013-present): single-purpose feedback moments around one user action, covering Saffer's trigger-rules-feedback-loops model, spring physics and Material durations, optimistic UI, haptics, INP budgets and reduced-motion fallbacks. Use when designing state feedback, buttons, toggles, likes and async action responses."
---

# UI Style: Micro-interaction-Driven UI

Small, single-purpose feedback moments around one user action — the style defined by feedback, not look. Canon: Dan Saffer's *Microinteractions* (O'Reilly, 2013) with the Trigger/Rules/Feedback/Loops-and-Modes model; popularized by Material's ink ripple (2014) and the Twitter heart pop (2015); matured into spring-physics optimistic UI. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing state feedback: buttons, toggles, likes, submits, undo.
- Tuning durations, springs and easing for tactile response.
- Meeting INP budgets while animating interaction states.

---

## 🕰️ Definition and Timeline

- Saffer's model (2013) → Material ink ripple (2014) → Twitter heart (2015) → Dribbble showcase era → spring-physics component libraries (Motion), optimistic UI, haptic-aware mobile patterns.

---

## 🎨 Visual DNA

- Invisible until engaged: ripple radii, checkmark morphs, toggle-thumb springs, skeleton shimmer, optimistic checkmark on submit, button press scale (0.96–0.98), 1–2px shadow lifts.

---

## 🖱️ Interaction and Motion

- Durations: 150–250 ms for state feedback, ~300 ms ripples (Material guidance); MD3 "emphasized" easing `cubic-bezier(0.2, 0, 0, 1)`; spring damping ≈ 0.7–1.0 (slight overshoot reads as tactile); two-phase press→release; loading→success morph in place (no layout swap); pull-to-refresh loops; haptics (`navigator.vibrate`).

---

## 🛠️ Implementation Notes

- CSS transitions on `transform`/`opacity` only; Motion springs and gesture hooks (`whileHover`, `whileTap`); GSAP Flip for layout-state morphs; View Transitions API for cross-state DOM morphs; `@starting-style` (Chrome 117+) for first-render enter transitions; Rive state machines for designer-authored vectors; WAAPI for one-shots.

---

## ♿ Accessibility and Performance

- Every interaction must land inside **INP < 200 ms** — animation decorates the state change, never gates it; composited properties only; 60 fps = 16.67 ms; target sizes ≥ 24px (WCAG 2.2, 2.5.8) / 44 pt Apple / 48 dp Material; never signal state by color alone; `prefers-reduced-motion` cuts springs to crossfades; visible `:focus-visible` states are micro-interactions too.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** everywhere in product UI — this is the baseline of "feels native"; highest ROI on destructive actions (confirm/undo) and async states (submit/like/save).
- **Avoid:** decoration-only animation on non-interactive elements (mystery meat); animation that delays perceived response; delight at scale on data-entry forms.

---

## ⚠️ Pitfalls

- Delight tax on performance budgets; gimmick overload ("dancing buttons"); Dribbble-shot interactions that never survive real input rates; over-springing causing motion sickness.

---

## 📚 Sources

- Dan Saffer, *Microinteractions: Designing with Details*, O'Reilly, 2013 — https://www.oreilly.com/library/view/microinteractions-full-color/9781491945919/
- Material Design 3 motion overview — https://m3.material.io/styles/motion/overview
- Apple HIG, "Motion" — https://developer.apple.com/design/human-interface-guidelines/motion
- MDN, "`prefers-reduced-motion`" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Motion (prev. Framer Motion) — https://motion.dev/
- W3C, WCAG 2.2 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-material-you](../ui-style-material-you/SKILL.md), [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md).
- For interaction fundamentals, see [ui-ux-principles](../../../engineering/practices/ui-ux-principles/SKILL.md).
- Newer sibling styles: [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md).
