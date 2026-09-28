---
name: "ui-style-claymorphism"
description: "Provides the claymorphism UI style (2021-2023): inflated pastel shapes with curved edges and dual inner shadows simulating soft clay, covering the shadow formula, the CSS fidelity gap, NFT/3D-tool lineage (Spline, toy-face artists), contrast trade-offs and appropriate brand contexts. Use when designing playful inflated UI or assessing clay-style marketing assets."
---

# UI Style: Claymorphism

Puffy "fluffy 3D" UI — inflated shapes with curvature beyond plain rounded corners and dual inner shadows simulating soft clay, usually in pastel palettes with 3D clay characters. Named and defined by Michał Malewicz (2021). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing kid/family, education or playful-fintech onboarding surfaces.
- Integrating 3D clay renders (Spline-class) into web layouts.
- Assessing pastel inflated mockups for contrast compliance.

---

## 🕰️ Definition and Timeline

- Drivers named by Malewicz: the NFT/metaverse 3D boom, Spline democratizing browser 3D, Pitch's clay key visuals as first mainstream sighting, artists Amrit Pal Singh (toy faces) and Sam Briskar (Avatarz), Icons8 3D packs.
- Peak 2021–2022; faded through 2023 as 3D hype cooled; DNA survives in soft-elevation OS work and illustrated marketing sites.

---

## 🎨 Visual DNA

- **Shapes:** corner rounding beyond 50% of the box with edge midpoints bowed outward (curved edges, not just rounded corners — Figma recipe: add midpoint handles, mirror, drag out).
- **Color:** pastel/candy palettes with chunky saturated accents.
- **Depth:** two inner shadows (top-left lighter, bottom-right darker) create the dome; one large soft drop shadow — often offset along X, deliberately "breaking UI shadow rules".
- **Type:** chunky friendly display faces; **icons:** simple filled; generous padding everywhere.

---

## 🖱️ Interaction and Motion

- Squishy hover/press (scale 0.96–1.02 with inner-shadow deepening); bouncy spring easings; clay characters float with subtle idle loops (baked renders or Spline embeds, not CSS).

---

## 🛠️ Implementation Notes

```css
.clay {
  border-radius: 40px;
  box-shadow: 35px 35px 68px rgb(120 120 180 / 0.5),
              inset -8px -8px 16px rgb(120 120 180 / 0.6),
              inset 0 11px 28px #ffffff;
}
```

- The tinted outer + colored inner shadows are the signature (widely circulated formula; generator at claymorphism.com).
- True edge curvature is not achievable in pure CSS yet — ship SVG or 3D renders for bowed edges.
- Dark mode works only if shapes are not fully black — inner shadows must stay visible.

---

## ♿ Accessibility

- Pastel-on-pastel repeats the neumorphism trap: pale type and pale shadows fail WCAG 1.4.3 at body sizes; white inner highlights vanish on light backgrounds; test at 200% zoom and with contrast simulation; reinforce button states with color/outline beyond the clay effect.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** kid/family brands, education, playful fintech onboarding, NFT/creator marketing.
- **Avoid:** enterprise dashboards, dense data UI, anything needing sober credibility.

---

## ⚠️ Pitfalls

- Reads as childish by design ("relieve our childhood" is the pitch); heavy 3D asset weight; the CSS fidelity gap; quick trend churn post-2022.

---

## 📚 Sources

- Michał Malewicz, "Claymorphism in User Interfaces", Hype4, 2021 — https://hype4.academy/articles/design/claymorphism-in-user-interfaces
- Hype4, claymorphism.com CSS generator — https://claymorphism.com
- Spline — https://spline.design
- Adrian Bece, "Neumorphism and CSS" (inner-shadow grammar predecessor), CSS-Tricks, 2020 — https://css-tricks.com/neumorphism-and-css/
- W3C, WCAG 2.1 SC 1.4.3 — https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-neumorphism](../ui-style-neumorphism/SKILL.md), [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md).
- For 3D asset pipelines, see [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
