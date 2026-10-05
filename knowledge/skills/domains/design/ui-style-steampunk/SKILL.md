---
name: "ui-style-steampunk"
description: "Provides the steampunk UI and UX style (1987-present): Victorian-industrial retrofuturism of brass, leather, gauges and airship ephemera, covering components, navigation metaphors, flows, microcopy, states, palette, type and motion. Use when designing heritage-flavored brands, game and event sites, maker storefronts or alternate-19th-century product worlds, including their usability."
---

# UI Style: Steampunk

The Industrial Revolution imagined as if steam power never gave way: exposed mechanism, ornamented machines, handmade objects. Translated to the web as warm metals, aged paper, riveted plates, dials and levers. Synthesized from the sources below; unverified items are flagged.

---

## 🧭 When to Activate

- Designing interface components, navigation and flows (not just look-and-feel) for a brand, game, convention or narrative world set in an alternate Victorian era.
- Maker, leatherwork, watch, spirits and craft storefronts that sell handmade provenance and need checkout to stay usable.
- Interfaces where mechanical metaphors (gauges, valves, levers) explain state, with usability checks to prove they do.

---

## 🕰️ Definition and Timeline

- **Coinage:** K. W. Jeter proposed "steam-punks" in an April 1987 letter to Locus, a tongue-in-cheek variant of cyberpunk, to label work by Tim Powers, James Blaylock and himself (Wikipedia, "Steampunk"). Precursors: Morlock Night (1979), The Anubis Gates (1983), Infernal Devices (1987); The Difference Engine (1990) widened awareness; Laputa: Castle in the Sky (1986) is cited as an early classic.
- **Era and ethos:** 19th-century steam machinery seen through anachronism. The "punk" is DIY craft, a non-luddite critique of technology: celebrate ingenuity and the handmade over sealed, minimalist devices.
- **Versus neighbors:** [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md) imitates real objects to teach affordance; steampunk is a narrative world, with fictional machinery and period ornament. [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md) is the real historical craft revival; steampunk adds engines and airships. [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md) removes steam and moves to the Renaissance.

---

## 🎨 Visual DNA

- **Palette:** aged-paper ground (`#EFE3C8`), sepia ink (`#2B1D12`), brass (`#B5893A`), copper (`#B4633A`), verdigris (`#4F8A78`), oxblood leather (`#5B2A22`), soot (`#1B1612`). Dark-room variant: soot ground with warm brass text.
- **Type:** Victorian display faces (Playfair Display, Abril Fatface, IM Fell, Cinzel Decorative) for headings; a readable text serif (Libre Baskerville, Source Serif) for body; slab or wood-type accents for posters and ticket stubs. Never set body copy in an ornamental face.
- **Texture:** brushed metal, rivet rows, stitched leather, riveted plate corners, paper grain, patina stains. Apply texture to chrome and frames, never under paragraphs.
- **Layout:** framed panels with cartouche headers, bolted bars, handbill and patent-drawing compositions, exploded diagrams with numbered callouts, airship and pipework dividers.
- **Iconography:** gears, cogs, pressure gauges, goggles, keys, valves, zeppelins, compasses; thin engraved line weight, consistent stroke.

---

## 🖱️ Interaction and Motion

- Controls as mechanisms: toggles as levers, sliders as sliding valves, progress as a pressure gauge needle with a slight overshoot and settle.
- Gears turn only in response to user action or loading; durations 200-600 ms, steps eased like a ratchet (`steps()` or `cubic-bezier(.3,1.4,.5,1)`).

---

## 🧩 UX Patterns

- **IA and navigation:** a workshop or airship metaphor: Cargo Hold (shop), Chart Room (search/map), Engine Room (settings), Logbook (account/orders). Always pair the label with a plain subtitle ("Settings") and keep a conventional top bar, breadcrumb and footer; the metaphor yields to convention for cart, login, search, legal and help (heuristics 2, 4, 6).
- **Key flows:** onboarding as a brief "commissioning" in 3 steps with skip; checkout is a plain single-column form with real labels, a visible total and no ornament in fields; search is a standard box, not a lever; settings use ordinary toggles with a brass skin.
- **Microcopy:** formal, wry, short ("Dispatch order", "Back to the Hold"); one metaphor per label, never at the cost of clarity. Errors state cause plus fix in plain words first, flavor second (heuristic 9).
- **States:** loading = gauge filling with a numeric percent; empty = "The Hold is bare" plus one action; error = jammed-valve illustration plus "Card declined. Check the number or try another."; success = a stamped receipt with an order number.
- **Feedback and affordance:** buttons keep plate edges and pressed state; needle value printed beside the gauge (heuristic 1); disabled controls look dull, never merely tarnished.
- **Trust and load risks:** ornament raises cognitive load and can read as unserious in payment steps; fake-aged UI may look broken; escalating cog-spin hides status.
- **Usability checks:** (1) task success on find-product-and-buy, target at least 90% unaided; (2) time on task versus a plain baseline, no more than 10-15% slower; (3) SUS at least 68 (unverified benchmark). Test five users on metaphor labels for recognition (heuristic 6).
- Basis: Nielsen's heuristics (NN/g, fetched) and WCAG 2.2 (W3C, fetched). Section content beyond those is unverified synthesis.

---

## 🛠️ Implementation Notes

```css
:root {
  --paper:#EFE3C8; --ink:#2B1D12; --brass:#B5893A; --copper:#B4633A; --soot:#1B1612;
}
body { background: var(--paper); color: var(--ink); font-family: "Libre Baskerville", serif; }
.plate {
  background: linear-gradient(145deg,#D2A95A,#8E6A2B 55%,#C79B49);
  border: 2px solid #4A3512; border-radius: 6px;
  box-shadow: inset 0 1px 0 #F2D690, inset 0 -2px 4px #0006, 0 3px 8px #0005;
  color: var(--soot);
}
.rivets { background: radial-gradient(circle at 6px 6px,#F2D690 0 2px,#5A4118 3px 4px,transparent 5px) 0 0/ 24px 24px; }
.gauge-needle { transform-origin: 50% 100%; transition: transform .5s cubic-bezier(.3,1.4,.5,1); }
.gear { animation: spin 12s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .gear { animation: none; } .gauge-needle { transition: none; } }
```

- Draw gears and gauges as inline SVG (a tooth path with `stroke-dasharray` or `<use>` for repeats); reuse one symbol, rotate with CSS.

---

## ♿ Accessibility

- Brass on paper and copper on sepia commonly fall under 4.5:1 (1.4.3); test each pair, and reserve brass for large display text or borders, which need 3:1 (1.4.11, W3C).
- Ornamental frames and textured backgrounds must not lower text contrast; keep text on a flat plate.
- Honor `prefers-reduced-motion: reduce` (MDN): stop gear spin, parallax and needle sweep; keep state changes instant (2.3.3 Animation from Interactions, AAA; 2.2.2 for any auto-playing motion over 5 s).
- Mark decorative gears, rivets and flourishes `aria-hidden="true"` (or empty `alt`) so assistive technology does not announce ornament.
- Focus rings (2.4.7, 2.4.11) must contrast against brass; use a dark `outline` with offset, not a metal glow. Targets at least 24 px (2.5.8).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** games and fiction, conventions, craft and heritage brands, museums, portfolios, editorial features.
- **Caution:** SaaS marketing (limit to hero and illustrations), e-commerce (keep checkout plain).
- **Avoid:** dense dashboards, forms-heavy flows, healthcare, finance, anything where decoration slows task completion.
- **Cultural note:** the Victorian setting romanticizes an empire; avoid exoticized colonial imagery and costume stereotypes, and do not present industrial-era labor as consequence-free.

---

## ⚠️ Pitfalls

- Gear confetti: decorating every surface with cogs signals costume, not craft; Skeuo overload: heavy bevels and filters hurt paint performance and legibility; Low-contrast sepia text and tiny ornamental type; Lifted brass-and-gear templates read as generic; derive ornament from a specific fictional world.

---

## 📚 Sources

- Wikipedia contributors, "Steampunk" (Wikipedia) — https://en.wikipedia.org/wiki/Steampunk (coinage, canonical works, ethos; fetched)
- Wikipedia contributors, "Gothic Revival architecture" (Wikipedia) — https://en.wikipedia.org/wiki/Gothic_Revival_architecture (Victorian ornament context; fetched)
- MDN, "conic-gradient()" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Understanding SC 1.4.11 Non-text Contrast" (W3C WAI), 2023 — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- NN/g, Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (fetched)
- Palette hex values and type pairings are this skill's own suggestions, not sourced.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md), [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md), [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
