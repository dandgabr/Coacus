---
name: "ui-style-kinetic-typography"
description: "Provides the kinetic typography / motion-first hero style (2016-present): type as the primary animated element with per-glyph reveals, variable-axis morphs and marquees, covering GSAP SplitText and Motion patterns, font-variation-settings animation, CLS budgets and screen-reader-safe splitting. Use when designing type-led heroes or animating variable-font headlines."
---

# UI Style: Kinetic Typography (Motion-First)

Type as the primary animated element — per-letter/line reveals, weight/width morphs, marquees — with the headline as the hero. Lineage: film title design; accelerated by GSAP text tooling and variable fonts (OpenType 1.8, September 2016); Awwwards peak 2019–2021; standard hero grammar since. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing type-led heroes for brand, agency or campaign pages.
- Animating variable-font axes safely (which axes reflow).
- Making letter-split animations screen-reader-safe.

---

## 🕰️ Definition and Timeline

- Term inherited from motion design (Saul Bass lineage); web adoption with GSAP SplitText; variable fonts (OpenType 1.8, Sept 2016) made axis animation native; consolidation 2017–2018 (Safari 11, Chrome 62+, Firefox 62); GSAP went free under Webflow (current v3.15 — https://gsap.com/docs/v3/), and Motion (ex-Framer Motion, v13) standardized spring-based type motion.

---

## 🎨 Visual DNA

- Oversized display type (10–20vw), tight tracking (−0.02 to −0.05em); mono accents and index numbers; monochrome + one neon accent; per-glyph masks (overflow-hidden line boxes); infinite marquees; oblique skews; weight interpolation as the morph.

---

## 🖱️ Interaction and Motion

- Per-char stagger 0.02–0.08s with `yPercent: 100 → 0` masked reveals; hover = `wght`/`wdth` morph (200–400 ms, ease-out) or rolling duplicate label; scroll-scrubbed word reveals; scramble/decode-in; springs for enter, expo-out for exits; 300–600 ms reveals, 150–250 ms hovers.

---

## 🛠️ Implementation Notes

- GSAP SplitText (now free) for line/word/char splitting with `aria-label` preservation; Motion `variants` + `staggerChildren` + `AnimatePresence`.
- CSS: transition high-level properties (`font-weight`, `font-stretch`) where possible — `font-variation-settings` is lower-level and must redeclare **all** axes (MDN); register custom properties with `@property` for smooth animation; WAAPI for DOM-light tweens; View Transitions for headline swaps.
- Loading: `font-display: swap` + metric-compatible fallback (`size-adjust`) keeps CLS < 0.1; subset so the hero weight loads first.

---

## ♿ Accessibility and Performance

- Splitting multiplies DOM nodes — cap to lines/words on long copy; `aria-label` on the heading, `aria-hidden` on split spans (screen readers otherwise announce letter-by-letter); no-JS users must not see invisible (`opacity: 0`) headlines; honor `prefers-reduced-motion` with crossfades; WCAG 2.3.1 — no rapid flashing.
- Transform-only animation (reflow kills the 16.67 ms budget); avoid `will-change` accumulation.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** brand/agency sites, portfolios, album/campaign launches — pages whose first impression is the message.
- **Avoid:** dense reading surfaces, dashboards, docs, e-commerce product pages where type is content, not spectacle.

---

## ⚠️ Pitfalls

- Screen readers announcing per-letter; FOUC/CLS from late font swaps; invisible-headline failure without JS; "every portfolio is the same kinetic hero" fatigue.

---

## 📚 Sources

- Motion (prev. Framer Motion), Matt Perry — https://motion.dev/
- GSAP SplitText docs — https://gsap.com/docs/v3/Plugins/SplitText
- Bruno Arizio portfolio case study, Codrops, Dec 2019 — https://tympanus.net/codrops/2019/12/18/case-study-portfolio-of-bruno-arizio/
- MDN, "Variable fonts guide" — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts/Variable_fonts_guide
- Theatre.js — https://www.theatrejs.com/
- MDN, "Web Animations API" — https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-expressive-variable-typography](../ui-style-expressive-variable-typography/SKILL.md), [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
