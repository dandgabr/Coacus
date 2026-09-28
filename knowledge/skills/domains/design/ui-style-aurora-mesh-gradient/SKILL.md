---
name: "ui-style-aurora-mesh-gradient"
description: "Provides the aurora / mesh gradient UI style (2018-present): ambient multi-color blurred backgrounds with grain, covering the pure-CSS radial-gradient mesh recipe, Stripe minigl lineage, SVG feTurbulence grain, contrast scrims and motion gating. Use when designing atmospheric hero backgrounds or implementing banding-free gradient fields."
---

# UI Style: Aurora / Mesh Gradient

Ambient multi-color backgrounds — large soft color fields blending like light in a sky, often with grain. Lineage: gradient-mesh illustration, Instagram's 2016 gradient, Stripe's animated WebGL homepage canvas (2021, reverse-engineered as "minigl"); named "Aurora UI" by Michał Malewicz (2021); dark-mode aurora glows became the 2022–2023 SaaS signature. Still a live default for hero backgrounds. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing hero sections, empty states or brand splash moments.
- Implementing banding-free animated gradient fields.
- Auditing text contrast over multi-hue animated backgrounds.

---

## 🕰️ Definition and Timeline

- Stripe's 2021 site redesign shipped the animated WebGL gradient (minigl), reverse-engineered by Kevin Hufnagl (Oct 2021): four-color canvas, ~12° skewY tilt, ScrollObserver pause.
- Grain went mainstream with Jimmy Chion's "Grainy Gradients" (CSS-Tricks, Sept 13, 2021). Linear-class dark aurora glows defined dev-tool marketing 2022–2023.

---

## 🎨 Visual DNA

- **Fields:** 2–4 hues feathered with no hard edges; the Stripe canon (indigo→violet→coral, e.g. `#3a3aff / #ff61ab / #E63946 / #6ec3f4`); diagonal composition.
- **Dark variant:** near-black canvas with 1–2 glowing color pools.
- **Grain:** monochrome noise at 3–8% opacity kills banding.
- **Type:** large white/near-white display floating over the atmosphere; depth via blur/luminance, never shadow.

---

## 🖱️ Interaction and Motion

- Slow infinite hue/position drift (10–20s loops); scroll-linked color shifts; hover intensifies glow pools; pause when off-screen (IntersectionObserver — Stripe's own approach); everything gated on `prefers-reduced-motion`.

---

## 🛠️ Implementation Notes

```css
.aurora {
  background:
    radial-gradient(at 20% 30%, #3a3aff, transparent 50%),
    radial-gradient(at 80% 70%, #ff61ab, transparent 50%),
    #0a0a1a;
}
```

- Optional `filter: blur(60–100px)` on absolutely-positioned color blobs.
- Grain: SVG `feTurbulence type='fractalNoise'` + `filter: contrast(170%) brightness(1000%)` + blend mode (Chion's recipe).
- Animated variants: WebGL (Stripe-class) or CSS `@keyframes` translating blob layers; generators: meshgradient.in ("Meshy").

---

## ♿ Accessibility

- **Text-over-gradient is the core hazard:** mid-luminance multi-hue fields make a single text color fail somewhere on the field — use a dark scrim at the text zone and verify 4.5:1 at every text position across animation frames; keep text off the brightest pool; gate animation for vestibular safety; full-screen WebGL costs SEO/perf budget.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** hero sections, empty states, splash/brand moments.
- **Avoid:** content-dense pages, forms, long reading sessions, light-mode enterprise UI.

---

## ⚠️ Pitfalls

- Banding on large gradients (hence the grain arms race); animated-background contrast regressions ship silently; 2023–25 SaaS aurora sameness.

---

## 📚 Sources

- Michał Malewicz, "Aurora UI — new visual trend for 2021", Hype4 — https://hype4.academy/articles/design/aurora-ui-new-visual-trend-for-2021
- Kevin Hufnagl, "How To: Create the Stripe Website Gradient Effect", Oct 2021 — https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/
- Jimmy Chion, "Grainy Gradients", CSS-Tricks, Sep 13, 2021 — https://css-tricks.com/grainy-gradients/
- Bram.us, "How To create the Stripe Website Gradient Effect", Oct 13, 2021 — https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect/
- meshgradient.in — https://meshgradient.in/
- MDN, "Using media queries for accessibility" — https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Media_queries/Using_for_accessibility

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-glassmorphism](../ui-style-glassmorphism/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md).
