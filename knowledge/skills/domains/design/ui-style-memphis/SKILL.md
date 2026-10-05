---
name: "ui-style-memphis"
description: "Provides the Memphis Design UI style (1980-1987 origin, recurring revival): clashing pastel and primary palettes, squiggles, terrazzo and plastic-laminate patterns, asymmetric geometry and playful rule-breaking, covering tokens, pattern layers, shape kits and WCAG-safe color handling. Use when designing youthful, irreverent brand, campaign or education surfaces that need postmodern playfulness rather than modernist restraint."
---

# UI Style: Memphis

Postmodern 1980s Italian design translated to interfaces: colorful abstract decoration, asymmetric shapes and deliberate violation of Modernist good taste. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Youth, music, education, creative-tool and campaign sites that must feel loud and playful.
- Illustrated empty states, onboarding and event pages with pattern-led identity.
- Requests for "80s geometric", "squiggle and confetti", "terrazzo" or "Sottsass" looks.

---

## 🕰️ Definition and Timeline

- Memphis Group founded 6 December 1980 in Milan by Ettore Sottsass with young designers and architects; active 1980-1987; Sottsass left in 1985 to focus on his own firm.
- Named after a Bob Dylan song played at the founding meeting, embracing ambiguity and eclectic reference. Materials: plastic laminate, terrazzo.
- Became ubiquitous in 1980s-90s pop culture; later succeeded by Y2K aesthetics.
- Distinction from [ui-style-maximalism](../ui-style-maximalism/SKILL.md): maximalism is about density and excess in general; Memphis is a specific vocabulary (squiggles, triangles, terrazzo, laminate) with flat graphic color.
- Distinction from [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md): Memphis uses pastel clash and decoration, not thick black borders and offset shadows. Distinction from [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md): no chrome, gloss or translucency.

---

## 🎨 Visual DNA

- **Shapes:** circles, triangles, arches, zigzags, squiggles, grids of dots; asymmetry over symmetry; shapes overlap and rotate.
- **Color:** clashing set of 4-6 flats: pink `#FF71CE`, teal `#01CDFE`, yellow `#FFD400`, black, white, plus one primary; use black and white as the stabilizers.
- **Pattern:** terrazzo speckle, black-and-white stripes or dots as large-scale fills, kept to one pattern per region.
- **Type:** geometric or chunky sans display, sometimes outlined or offset; body copy in a neutral sans.
- **Layout:** off-axis blocks, floating decorative shapes in margins, clean text column at center.

---

## 🖱️ Interaction and Motion

- Playful, snappy: shapes bounce, rotate or swap color on hover, 150-300ms with slight overshoot (`cubic-bezier(.34,1.56,.64,1)`).
- Decorative shapes may drift slowly; keep motion off the text column and pauseable.

---

## 🛠️ Implementation Notes

```css
:root { --pink:#ff71ce; --teal:#01cdfe; --yellow:#ffd400; --ink:#111; --paper:#fff; }
.hero { background:
  radial-gradient(circle, var(--ink) 2px, transparent 2.5px) 0 0 / 18px 18px,
  var(--paper); }
.shape-tri { width:0; height:0; border:40px solid transparent; border-bottom-color:var(--teal); }
.squiggle { background: url("squiggle.svg") repeat-x; height: 16px; }
.btn { background: var(--yellow); color: var(--ink); border-radius: 999px 999px 6px 999px; }
@media (prefers-reduced-motion: reduce) { .shape-float { animation: none; } }
```

- Keep decorative shapes as `aria-hidden` SVG or CSS pseudo-elements; text always sits on a solid ink or paper panel.
- Define the palette as semantic tokens (surface, accent, ink) so clashes are chosen, not accidental.

---

## ♿ Accessibility

- Pastels on white fail 1.4.3 (4.5:1 body, 3:1 large); use black or near-black text on pastel fills and test every pairing.
- Do not use pattern or color alone to convey state (1.4.1); controls need 3:1 boundaries (1.4.11).
- Busy backgrounds must not sit behind text; verify under text-spacing overrides (1.4.12) and 400% zoom reflow (1.4.10).
- Moving decoration over 5 seconds needs a pause control (2.2.2); honor `prefers-reduced-motion` and avoid flashing (2.3.1).
- Targets at least 24px (2.5.8) even with irregular shapes; focus indicator contrasts with patterned surroundings (2.4.7, 2.4.13).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** campaigns, youth brands, music and festivals, kids and learning products, portfolio sites.
- **Caution:** SaaS marketing (limit to hero and illustration), long reading pages.
- **Avoid:** banking, healthcare, legal, dense admin UI, any task needing calm focus.

---

## ⚠️ Pitfalls

- Random confetti without a rule set; every shape equally loud so hierarchy collapses.
- Reproducing "80s nostalgia" via neon gradients, which is a different style.
- Pattern fills hurting legibility and page weight; palette that cannot meet contrast.

---

## 📚 Sources

- Wikipedia contributors, "Memphis Group" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Memphis_Group
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- Design Museum, "Memphis" (Design Museum), accessed 2026-10-05 — https://designmuseum.org/memphis (group formed December 1980, debuted 1981; Sottsass left in 1985; plastic laminates, geometric and animal-print patterns, rule-breaking against modernist good taste).
- Hex values, shape vocabulary guidance and the overshoot easing are author's implementation suggestions, not sourced claims.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-maximalism](../ui-style-maximalism/SKILL.md), [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md).
