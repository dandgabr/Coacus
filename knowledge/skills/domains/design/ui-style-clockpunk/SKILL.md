---
name: "ui-style-clockpunk"
description: "Provides the clockpunk UI and UX style: Renaissance clockwork retrofuturism of gears, orreries, astronomical dials and parchment drawings, covering components, annotated-diagram navigation, flows, microcopy, states, drafting type and gear-train motion. Use when designing museum, education, watchmaking, craft or puzzle products that want a mechanical-precision interface and usable flows."
---

# UI Style: Clockpunk

Retrofuturism built from springs, weights, escapements and cams rather than steam: the 16th-18th century imagined with extraordinary clockwork. On the web it becomes parchment, ink line-work, geared dials and deliberate, ticking motion. Genre facts come from the fetched sources; the rest is marked.

---

## 🧭 When to Activate

- Designing components, navigation and flows (not just look-and-feel) for watch, horology, astronomy, calendar, science-history or museum interfaces.
- Fantasy or alternate-history worlds in a Renaissance or Enlightenment register.
- Explainers where mechanisms (ratios, timing, cycles) are the content and comprehension must be tested.

---

## 🕰️ Definition and Timeline

- **Coinage:** the term originated in the GURPS Steampunk sourcebook (Wikipedia, "Clockpunk"; exact year unverified). Canonical works listed there: Margaret Cavendish's The Blazing World, Jay Lake's Mainspring, S. M. Peters's Whitechapel Gods, Ian Tregillis's The Mechanical.
- **Era and ethos:** the Early Modern Period (16th-18th century) with "clockwork, gears, and Da Vincian machinery designs". For some, "clockpunk is steampunk without steam". The "punk" is a humanist craft ethic: precision made by hand, knowledge as an instrument, no engine of mass industry.
- Real anchor: Leonardo's Codex Atlanticus (1,119 pages, 1478-1519, Biblioteca Ambrosiana) and Paris Manuscript B (1488-1490) hold the engineering sketches the genre quotes (Wikipedia, "Leonardo da Vinci's notebooks").
- **Versus neighbors:** [ui-style-steampunk](../ui-style-steampunk/SKILL.md) is Victorian, riveted, brass-and-leather, heavy and ornamented; clockpunk is lighter, linear, drafted, precise and quiet. [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md) is curated archival prestige; clockpunk is a machine-world aesthetic with mechanism as the motif.

---

## 🎨 Visual DNA

- **Palette:** parchment (`#F1E6CC`), iron-gall ink (`#2A2118`), sepia wash (`#8A6B43`), gilt (`#B8923A`), lapis (`#27437A`), cinnabar accent (`#A63A2B`). Night-sky variant: lapis-black ground (`#0F1626`) with gilt linework.
- **Type:** humanist and old-style serifs (EB Garamond, Cormorant, IM Fell), italic annotations as marginalia, small-caps labels; a handwritten script only for short notes.
- **Texture:** laid-paper grain, foxing spots, ink bleed, compass-drawn construction lines left visible.
- **Layout:** codex-style pages: central diagram with annotated leader lines, columns of notes, circular dials, zodiac rings, orrery concentric layouts, ruled margins.
- **Iconography:** fine hairline SVG gears, escapement anchors, springs, sundials, astrolabes; constant stroke width (1-1.5 px), no filled heavy shapes.

---

## 🖱️ Interaction and Motion

- Motion is a train of gears: a primary rotation drives secondary ones at true ratios (for example 12:1 hour to minute); everything stays mathematically coupled.
- Escapement feel: stepped ticking via `animation-timing-function: steps(n)`, not smooth tweening.
- Scroll as winding: scroll progress rotates a main wheel; section changes advance a dial notch.

---

## 🧩 UX Patterns

- **IA and navigation:** a codex or orrery metaphor: chapters as folios, a dial or ring as a time/section selector, marginal annotations as secondary nav. Keep a linear table of contents, visible page titles, search and a conventional menu; the dial must be a shortcut, never the only path (heuristics 4, 7).
- **Key flows:** onboarding as "turning the first page" with 2-3 labeled steps and skip; forms and checkout plain, ruled-line fields with visible labels; search with instant suggestions; settings as a simple list with a "Reset to defaults" (heuristic 3).
- **Microcopy:** measured, scholarly, brief ("Wind the mechanism", "Folio 3 of 12"); avoid pseudo-archaic grammar that slows reading.
- **States:** loading = a wheel advancing in steps with a text status; empty = a blank folio with a prompt and action; error = "The escapement slipped: your date is out of range (1 to 31)."; success = ink-line check mark draws once plus a text confirmation.
- **Feedback and affordance:** hover callouts reveal annotations but the same text is also on focus and tap; clickable diagram parts get a gilt outline and a cursor change; ticking is feedback only when it signals real progress (heuristic 1).
- **Trust and load risks:** dense annotated drawings overload working memory (heuristic 8); constant ticking competes with reading; faux handwriting looks unreliable for prices or dates.
- **Usability checks:** (1) task success on locate-a-fact-in-a-diagram, at least 85%; (2) time on task to reach any folio from home, target under 15 s; (3) SUS at least 68 (unverified benchmark), plus a comprehension quiz after an explainer.
- Basis: Nielsen's heuristics (NN/g, fetched) and WCAG 2.2 (W3C, fetched). The rest is unverified synthesis.

---

## 🛠️ Implementation Notes

```css
:root { --parch:#F1E6CC; --ink:#2A2118; --gilt:#B8923A; --lapis:#27437A; }
body { background: var(--parch); color: var(--ink); font-family: "EB Garamond", serif; }
.codex { background-image:
  repeating-linear-gradient(0deg, transparent 0 31px, #2A211822 31px 32px); }
.dial {
  border-radius: 50%; border: 1.5px solid var(--ink);
  background: repeating-conic-gradient(from 0deg, var(--ink) 0 .5deg, transparent .5deg 6deg);
}
.wheel-a { animation: turn 60s steps(60) infinite; }
.wheel-b { animation: turn 5s  steps(60) infinite reverse; }  /* ratio kept explicit */
@keyframes turn { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .wheel-a, .wheel-b { animation: none; } }
```

- Generate gear teeth in SVG with a small build script or a `<path>` plus `stroke-dasharray`; link rotation durations by one CSS variable so ratios cannot drift.

---

## ♿ Accessibility

- Hairline strokes and light sepia text fail quickly: body text 4.5:1 (1.4.3); essential diagram lines and dial marks 3:1 (1.4.11, W3C). Do not rely on 1px gilt on parchment.
- Ticking animation: honor `prefers-reduced-motion: reduce` (MDN) and offer a pause control for anything running over 5 s (2.2.2).
- Text on textured paper must sit on a flat or very low-contrast grain; do not run noise under paragraphs (1.4.3, 1.4.12 text spacing must not break layouts).
- Annotated diagrams need text equivalents (1.1.1) and keyboard-reachable callouts (2.1.1); do not hide meaning in hover only (1.4.13).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** horology and craft brands, planetarium and science-museum sites, educational explainers, fantasy lore wikis.
- **Caution:** SaaS (illustration and hero only), long-form reading (keep body plain).
- **Avoid:** transactional flows, dense data tables, anything where perpetual ticking competes with attention.
- **Cultural note:** Renaissance technology borrowed from Islamic, Chinese and other traditions; credit sources and avoid a Eurocentric "lone genius" framing when telling the history.

---

## ⚠️ Pitfalls

- Fake mechanics: gears that turn but drive nothing, or ratios that contradict each other; Perpetual spinning clocks causing motion discomfort and CPU cost; Over-aged parchment lowering contrast and printing badly; Collapsing into steampunk: adding rivets, goggles and brass plates erases the lighter drafted identity.

---

## 📚 Sources

- Wikipedia contributors, "Clockpunk" (Wikipedia) — https://en.wikipedia.org/wiki/Clockpunk (coinage, era, works; fetched)
- Wikipedia contributors, "Leonardo da Vinci's notebooks" (Wikipedia) — https://en.wikipedia.org/wiki/Leonardo_da_Vinci%27s_notebooks (Codex Atlanticus, Paris Manuscript B; fetched)
- MDN, "conic-gradient()" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Understanding SC 1.4.11 Non-text Contrast" (W3C WAI), 2023 — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- NN/g, Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (fetched)
- GURPS coinage year, palette and type choices: `unverified` / this skill's suggestions.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
