---
name: "ui-style-one-page-long-scroll"
description: "Provides the one-page long-scroll style (2011-2018): single-page vertical narratives of full-height poster sections, covering the Apple product-page template, scroll-snap standardization, NN/g attention data (74% in the first two screenfuls) and the deep-linking costs. Use when building launch pages or deciding between one-pagers and multi-page architectures."
---

# UI Style: One-Page Long-Scroll

Single-page marketing sites: a vertical stack of viewport-height poster sections — one idea per section, oversized display type, sticky nav and scroll-triggered reveals. Antecedents in the parallax one-pagers (Nike Better World, 2011); the template everyone copied is Apple's product pages (Mac Pro 2013 → iPhone X 2017). Peak 2011–2018. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Building product launches, campaign pages or linear portfolio narratives.
- Deciding between a one-pager and a multi-page architecture.
- Implementing native scroll snapping without breaking reading.

---

## 🕰️ Definition and Timeline

- Apple's flat, scroll-told product pages (2013–2017) established the grammar; One Page Love (Rob Hope, since 2008) is the canonical gallery (9,000+ sites indexed).
- Decline ~2018–2019: SEO/analytics pain and scroll-hijacking fatigue; the pattern survives in landing pages; scroll control standardized into CSS scroll snap (Baseline "widely available" April 2022).

---

## 🎨 Visual DNA

- Oversized display headlines, tight tracking; each viewport-height section is a poster with one idea; generous leading, center-aligned modules; restrained palettes letting photography carry sections; full-bleed imagery; floating product renders with soft shadows; sparse iconography (scroll-cue chevrons); progress dots.

---

## 🖱️ Interaction and Motion

- Scroll-triggered reveals (IntersectionObserver); parallax layers via `transform: translate3d`; smooth anchor scrolling; per-section autoplaying video; progress bars; sticky nav that changes style on scroll.

---

## 🛠️ Implementation Notes

- Sections: `min-height: 100svh`; `scroll-behavior: smooth` for anchors.
- Native snapping: container `scroll-snap-type: y proximity` (avoid `mandatory` on long pages — aggressive snapping harms reading); children `scroll-snap-align: start`; `scroll-margin` for sticky-header offsets.
- Reveals: IntersectionObserver toggling classes; compositor-friendly properties only (`transform`, `opacity`); `prefers-reduced-motion` gate for all parallax.
- Deep-linking: use fragment anchors + `history.pushState`; keep server-rendered full HTML for SEO.

---

## ♿ Accessibility and Evidence

- NN/g eyetracking (120 participants, 130k+ fixations): users spend **57% of viewing time above the fold** and **74% in the first two screenfuls** — long-scroll pages bury content; "false floors" stop scrolling; scroll-hijacking breaks native muscle memory; autoplaying per-section video hurts performance and accessibility.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** product launches, campaigns, portfolios, genuinely linear stories.
- **Avoid:** multi-topic content, docs, e-commerce catalogs, anything requiring return visits to specific sections; mobile users on slow connections (huge single payloads).

---

## ⚠️ Pitfalls

- Burying key content below the attention cliff; analytics attribution and deep-linking degrade; single mega-payload first paint.

---

## 📚 Sources

- Therese Fessenden, "Scrolling and Attention", NN/g, Apr 15, 2018 — https://www.nngroup.com/articles/scrolling-and-attention/
- Jakob Nielsen, "Scrolling and Attention" (original research), NN/g, 2010 — https://www.nngroup.com/articles/scrolling-and-attention-original-research/
- One Page Love, Rob Hope — https://onepagelove.com/
- MDN, "`scroll-snap-type`" (Baseline Apr 2022) — https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-type
- web.dev, "Well-controlled scrolling with CSS Scroll Snap", 2018 — https://web.dev/articles/css-scroll-snap
- Frank Chimero, "The Web's Grain", 2015 [essay path unverified] — https://frankchimero.com

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md), [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md).
