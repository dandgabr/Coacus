---
name: "ui-style-risograph-zine"
description: "Provides the risograph / zine UI style (print origins 1980, zine culture 1970s-present, web revival 2010s-present): limited spot-color inks, multiply overprint, misregistration and halftone grain, covering Riso print mechanics, zine DIY ethos, CSS blend-mode overprint and contrast-safe ink palettes. Use when designing indie, cultural or community-driven interfaces that mimic spot-color print."
---

# UI Style: Risograph and Zine

A screen translation of two-to-three-ink spot-color printing and DIY zine culture: flat saturated inks, overprint where layers multiply into a third color, slight misregistration and grainy halftones on uncoated paper. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Indie, arts, community, music, publishing or event brands that want a handmade print identity.
- Illustration-led pages where a limited ink palette unifies mixed imagery.
- Translating a printed zine or riso poster series into a web presence.

---

## 🕰️ Definition and Timeline

- Risograph: a brand of digital duplicator by Riso Kagaku Corporation, introduced in Japan in 1980. A thermal head burns microscopic holes in a master wrapped on a drum, and ink is forced through onto paper; soy-based inks; colors are separate drums, run one pass per color.
- Artist adoption: risograph printing gained traction among artists in the 2010s, especially for zines and comics (Wikipedia, Risograph).
- Zines: noncommercial, homemade publications, typically in editions of 1,000 or fewer; fanzines coined as a term in 1940; punk zines (for example *Sniffin' Glue*) in the late 1970s; riot grrrl zines in the 1990s (Wikipedia, Zine).
- Distinct from [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md): this is an ink-and-process simulation (spot colors, overprint, misregistration), not generic grain. Distinct from [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md): flat overprinted inks, not smooth gradient maps. Distinct from [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md): print-process constraint over mixed media.

---

## 🎨 Visual DNA

- **Inks:** two or three spot colors on off-white paper; typical riso-like hues: fluorescent pink `#FF48B0`, blue `#0078BF`, yellow `#FFE800`, green `#00A95C` (`unverified` as official ink values, treat as approximations).
- **Overprint:** where inks overlap, the result is darker (multiply), producing a third color for free.
- **Misregistration:** layers offset 1-3px so edges show a colored fringe.
- **Texture:** halftone dots, stipple and uneven ink coverage; paper tooth.
- **Type:** chunky grotesques, mono, slab or hand-lettered; tight layouts with rules and boxes.
- **Layout:** photocopy-zine energy: boxes, stickers, page numbers, folio marks.

---

## 🖱️ Interaction and Motion

- Keep motion print-like: hover shifts one ink layer 2px to reveal misregistration; 100-200ms.
- Page transitions as "next sheet" wipes in one ink color, brief and optional.
- No smooth glow, blur or glassy depth; effects should feel mechanical.
- Under `prefers-reduced-motion: reduce`, remove wipes and layer shifts; keep static overprint.

---

## 🛠️ Implementation Notes

```css
:root { --paper: #f6f1e7; --ink-a: #ff48b0; --ink-b: #0078bf; --ink-text: #1a1a2e; }
body { background: var(--paper); color: var(--ink-text); }
.riso { position: relative; isolation: isolate; }
.riso .layer-a { background: var(--ink-a); mix-blend-mode: multiply; }
.riso .layer-b { background: var(--ink-b); mix-blend-mode: multiply; transform: translate(2px, -1px); }
.halftone { background: radial-gradient(circle, var(--ink-a) 30%, transparent 32%) 0 0 / 6px 6px; }
.riso a:hover .layer-b { transform: translate(4px, -2px); }
@media (prefers-reduced-motion: reduce) { .riso * { transition: none; } }
```

- Use `mix-blend-mode: multiply` inside an isolated stacking context so overprint ignores unrelated backgrounds.
- Convert photos to single-ink (grayscale then colorize with multiply), and halftone by pattern or pre-rendered asset.
- Pair with a faint grain overlay for paper tooth; keep text in one dark ink with no misregistration.
- Define inks as semantic tokens (`--ink-a`, `--ink-b`) so multiply results can be pre-checked.

---

## ♿ Accessibility

- 1.4.3 Contrast (Minimum): fluorescent pink, yellow or light green on paper commonly fail; reserve them for fills and use dark ink for text. Test overprint results too.
- 1.4.11 Non-text Contrast: UI boundaries and focus indicators need 3:1 against paper; do not rely on a pastel ink.
- 1.4.1 Use of Color: two-ink schemes must not encode state by hue alone; add labels, icons or patterns.
- 1.4.12 Text Spacing: avoid misregistration or halftone on body text; it hurts reading and low vision.
- 2.4.7 Focus Visible: use a solid dark outline, not an ink shift.
- Honor `prefers-reduced-motion`; avoid flicker or flashing layer shifts.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** indie shops, publishers, galleries, festivals, zines, community sites, illustration portfolios.
- **Caution:** SaaS marketing pages (accent sections only), multi-step commerce.
- **Avoid:** dashboards, finance, healthcare, dense forms; any surface where fine color judgment is required.

---

## ⚠️ Pitfalls

- Using more than three inks turns it into generic "colorful"; the limit is the style.
- Multiply on dark backgrounds disappears; the style needs a light paper base.
- Fake misregistration on text damages legibility.
- Fluorescent hues render differently across wide-gamut and sRGB displays.
- Over-clean vector shapes with no texture look like flat design wearing a costume.

---

## 📚 Sources

- Wikipedia, "Risograph" (Wikimedia) — https://en.wikipedia.org/wiki/Risograph
- Wikipedia, "Zine" (Wikimedia) — https://en.wikipedia.org/wiki/Zine
- MDN Web Docs, "mix-blend-mode" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode
- MDN Web Docs, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Jimmy Chion, "Grainy Gradients" (CSS-Tricks), 13 Sep 2021 — https://css-tricks.com/grainy-gradients/
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", Recommendation 12 Dec 2024 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-gradient-duotone](../ui-style-gradient-duotone/SKILL.md), [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md).
