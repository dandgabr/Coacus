---
name: "ui-style-neumorphism"
description: "Provides the neumorphism / Soft UI style (2019-2020): monochrome extruded and inset shapes built from paired light-dark soft shadows, covering the shadow formula, light-source model, the canonical accessibility failure mode, generator tooling and when the style is acceptable as an accent. Use when evaluating or applying soft-UI embossed surfaces or explaining why the style fails in production UI."
---

# UI Style: Neumorphism (Soft UI)

"New skeuomorphism" — shapes that appear extruded from or pressed into a same-color background via paired light/dark soft shadows. Origin: Alexander Plyuto's Dribbble "Skeuomorph Mobile Banking" shots (December 2019); named by Michał Malewicz (December 2019); peaked January–May 2020 and collapsed under accessibility critique. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Evaluating soft-UI mockups (commonly imported from Dribbble shots).
- Explaining the documented accessibility failure of shadow-based affordance.
- Applying the style safely as a decorative accent.

---

## 🕰️ Definition and Timeline

- Plyuto's shots (Dec 2019) seeded it; Malewicz coined the name (UX Collective, Dec 2019); CSS-Tricks teardown (March 2020) documented the CSS grammar; Malewicz himself predicted it "will not be a huge trend" and later called it "the zombie trend" — by late 2020 it was a punchline, surviving as an accent and as the base recipe claymorphism inflated.

---

## 🎨 Visual DNA

- **Monochrome surface:** element background = page background (or near-identical).
- **Single top-left light source; two shadows per element:** one white/light offset up-left, one dark offset down-right.
- **Rounded corners mandatory;** soft low-contrast gradients for convex/concave surfaces; `inset` shadows for pressed states.
- **Typography minimal, low chroma** — the drained palette is the accessibility problem in embryo.

---

## 🖱️ Interaction and Motion

- Pressed states swap extruded shadows for `inset` shadows on `:active`; physical toggle/slider motion; otherwise minimal — states cannot be differentiated by color, so the motion story is weak by construction.

---

## 🛠️ Implementation Notes

```css
.soft {
  background: #e0e5ec;
  border-radius: 16px;
  box-shadow: -8px -8px 16px #ffffff, 8px 8px 16px rgb(163 177 198 / 0.6);
}
.soft:active { box-shadow: inset -8px -8px 16px #ffffff, inset 8px 8px 16px rgb(163 177 198 / 0.6); }
```

- Background must match the parent (a matching-angle `linear-gradient` fakes convex/concave).
- Generous padding required — the effect consumes small controls; small radii blur the illusion.
- neumorphism.io (Adam Giebl) generates the shadow pairs.

---

## ♿ Accessibility

- The canonical cautionary tale: shadow-based affordance **cannot pass contrast checks**; "everything looks like a button" — inputs, buttons and progress bars become indistinguishable; state colors (error/success/disabled) have no room in a monochrome palette; hierarchy collapses because every element shares the background color. Documented failures for low-vision and color-blind users (UX Collective accessibility critique, 2020).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** sparingly, as decoration on non-interactive cards in controlled light themes.
- **Avoid:** buttons, form controls, navigation, anything with validation states, dark themes, and any accessibility-sensitive product.

---

## ⚠️ Pitfalls

- Affordance failure — users "tap and hope"; Malewicz's own test: if removing the extrusion loses nothing, it is ornament.
- Per-component shadow math; no design-system story (Material-compatible only as garnish).

---

## 📚 Sources

- Adrian Bece, "Neumorphism and CSS", CSS-Tricks, Mar 20, 2020 — https://css-tricks.com/neumorphism-and-css/
- Michał Malewicz, "Neumorphism in user interfaces", UX Collective, Dec 2019 — https://uxdesign.cc/neumorphism-in-user-interfaces-b47cef3bf3a6
- Michał Malewicz, "Neumorphism — the zombie trend", UX Collective, 2020 — https://uxdesign.cc/neumorphism-the-zombie-trend-88cff23de46b
- "Let's talk Neumorphism and Accessibility", UX Collective, 2020 — https://uxdesign.cc/lets-talk-neumorphism-and-accessibility-44a48a6ace72
- Adam Giebl, neumorphism.io — https://neumorphism.io/
- Alexander Plyuto, "Skeuomorph Mobile Banking Continuation", Dribbble, Dec 2019 — https://dribbble.com/shots/8297803-Skeuomorph-Mobile-Banking-Continuation
- W3C, WCAG 2.1 SC 1.4.3 — https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
