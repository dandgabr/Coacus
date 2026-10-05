---
name: "ui-style-mid-century-modern"
description: "Provides the mid-century modern UI style (1945-1970s origin, revival from the late 1990s): clean lines without embellishment, honest materials, warm walnut and teal-orange palettes, organic-geometric shapes and generous whitespace, covering tokens, type pairing, layout, motion and WCAG contrast handling. Use when designing warm, human, design-literate brand, furniture, editorial or lifestyle surfaces that want modernist clarity with warmth."
---

# UI Style: Mid-Century Modern

Postwar modernism adapted for screens: simplicity, function and material honesty, warmed by wood tones and gentle organic geometry. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Furniture, home, architecture, hospitality, editorial and lifestyle brands.
- Design-literate products that want warmth without ornament.
- Requests for "Eames", "Scandinavian modern", "retro modern" or "walnut and teal" looks.

---

## 🕰️ Definition and Timeline

- Period 1945-1970s, with a major resurgence from the late 1990s. Figures: Neutra, Koenig, Charles and Ray Eames, Ellwood, Niemeyer, Lina Bo Bardi, Aalto, Jacobsen, Wegner.
- Traits: clean simple lines and lack of embellishment; honest materials; open plans with large windows; indoor-outdoor integration; function equal to form; post-and-beam structure.
- Materials: glass, brick, wood beams, ceramics, metals; tone restrained so form and material dominate.
- Distinction from [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md): Swiss is grid-and-type driven and cool; MCM is warmer, uses wood tones and organic curves.
- Distinction from [ui-style-atompunk](../ui-style-atompunk/SKILL.md): no space-age iconography; Distinction from [ui-style-flat-design](../ui-style-flat-design/SKILL.md): material warmth and illustrative restraint rather than system-driven flatness.

---

## 🎨 Visual DNA

- **Color:** warm neutrals (cream `#F4EDE0`, walnut `#6B4423`) with muted accents: teal `#2A7F7F`, mustard `#D9A441`, burnt orange `#C8553D`; one accent per view.
- **Shapes:** boomerang and kidney curves, tapered legs mapped to tapered rules, circles and arcs balanced against rectangles.
- **Type:** geometric sans headings (Futura-like) with a humanist or slab body; modest scale contrasts; generous leading.
- **Imagery:** product on neutral ground, wood grain as a thin texture, line illustrations with limited palette.
- **Layout:** open compositions, wide margins, asymmetrical balance, large imagery framed like windows.

---

## 🖱️ Interaction and Motion

- Calm and precise: 200-300ms ease-out fades and slides; hover shifts a tapered underline or accent bar.
- No bounce or parallax excess; transitions suggest sliding panels and doors.

---

## 🛠️ Implementation Notes

```css
:root { --cream:#f4ede0; --walnut:#6b4423; --teal:#2a7f7f; --mustard:#d9a441; --ink:#2b2118; }
body { background: var(--cream); color: var(--ink); font: 1.0625rem/1.65 "Source Serif 4", Georgia, serif; }
h1, h2 { font-family: "Josefin Sans", "Futura", sans-serif; letter-spacing: .02em; color: var(--walnut); }
.card { background: #fff; border-radius: 28px 4px 28px 4px; padding: 2rem; }
.btn { background: var(--teal); color: #fff; border-radius: 999px; transition: background 200ms ease-out; }
.btn:focus-visible { outline: 3px solid var(--mustard); outline-offset: 3px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
```

- Express palette as tokens (surface, ink, accent) and keep accents sparing.
- Use whitespace and real material photography rather than faux-texture overlays.

---

## ♿ Accessibility

- Mustard and orange on cream commonly fail 4.5:1 (1.4.3); use dark ink or walnut for text and test accents as large text or UI parts at 3:1 (1.4.11).
- Teal buttons with white text must reach 4.5:1; check hover and disabled states.
- Light, thin geometric display weights degrade at small sizes; keep body at or above 16px and support 200% resize and text spacing (1.4.4, 1.4.12).
- Provide visible focus (2.4.7, 2.4.13) and 24px targets (2.5.8); respect `prefers-reduced-motion`.
- Do not rely on color alone for category or state (1.4.1).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** furniture and interiors, architecture, publishing, cafes, boutique SaaS, portfolios.
- **Caution:** data-heavy tools (use as token palette only).
- **Avoid:** high-energy, tech-forward or gaming brands where restraint reads as dull.

---

## ⚠️ Pitfalls

- Brown-and-orange costume with generic layout; fake wood textures everywhere.
- Overusing the retro palette so contrast and hierarchy collapse.
- Nostalgic stock imagery with no connection to the brand's actual products.

---

## 📚 Sources

- Wikipedia contributors, "Mid-century modern" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Mid-century_modern
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- Eames Foundation, "Charles & Ray Eames Biography" (Eames Foundation), accessed 2026-10-05 — https://eamesfoundation.org/charles-ray/biography/ (Charles 1907-1978, Ray 1912-1988; molded plywood; "What works good is better than what looks good").
- Hex values, font pairings and shape recipes are author implementation suggestions, not sourced claims: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-flat-design](../ui-style-flat-design/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md).
- Related -punk styles: [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
