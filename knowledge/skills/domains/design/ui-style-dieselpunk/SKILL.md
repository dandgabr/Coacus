---
name: "ui-style-dieselpunk"
description: "Provides the dieselpunk UI and UX style (2001-present), with decopunk and oilpunk variants: interwar-to-1950s retrofuturism of Art Deco, Streamline Moderne, noir and poster graphics, covering components, dossier-style navigation, flows, microcopy, states, condensed type and motion. Use when designing game, film, automotive or heritage-industrial interfaces, avoiding real propaganda imagery."
---

# UI Style: Dieselpunk (with Decopunk and Oilpunk variants)

Technology and style of roughly 1918-1950s, pushed further: diesel engines, zeppelins, ocean liners, pulp serials, noir shadows and Deco geometry. Genre facts come from fetched sources; unverified items are flagged.

---

## 🧭 When to Activate

- Designing components, navigation and flows (not just look-and-feel) for noir, pulp, aviation, racing, jazz-age, speakeasy or alternate-history brands and games.
- Posters, event microsites and editorial features wanting strong graphic punch with clear calls to action.
- Dark, high-contrast pages where gritty or glamorous machinery carries the story and tasks must still be completable.

---

## 🕰️ Definition and Timeline

- **Coinage:** game designer Lewis Pollak, 2001, for his RPG Children of the Sun (Wikipedia, "Dieselpunk"; described there as a marketing term). Era: WWI through the 1950s, core "diesel era" 1918-1939.
- **Two schools (Wikipedia):** Ottensian, optimistic and World's Fair utopian; Piecraftian, darker and wartime or dystopian. Canonical works: The Man in the High Castle, BioShock, Sky Captain and the World of Tomorrow.
- **Decopunk variant:** a sleek, shiny subset on Art Deco and Streamline Moderne, "shinier than dieselpunk" with chrome and curves (Wikipedia, "-punk"; the Dieselpunk page also names Decopunk/Coalpunk, 1920s-1950s). Streamline Moderne, 1930s-1940s, adds curves, long horizontal lines, porthole windows and chrome (Wikipedia, "Streamline Moderne").
- **Oilpunk variant:** worlds powered by oil and combustion, theorized by Thorsten Botz-Bornstein on his Kuwait Oilpunk website (Wikipedia, "-punk"; the site itself was not checked, so details are `unverified`). Treat it as a petro-cultural lens: oil slicks, desert and Gulf modernity, pipelines.
- **Ethos:** "punk" as grit and defiance against a glossy official future, or as nostalgia for confident machine-age modernism.
- **Versus neighbors:** [ui-style-art-deco](../ui-style-art-deco/SKILL.md) is the clean decorative style alone; dieselpunk adds grease, noir and militarized machinery. [ui-style-atompunk](../ui-style-atompunk/SKILL.md) covers 1945-1965 Space Age optimism; dieselpunk precedes it and is grittier. [ui-style-atompunk](../ui-style-atompunk/SKILL.md) is its successor era.

---

## 🎨 Visual DNA

- **Palette (grit):** gunmetal (`#2E3338`), oil black (`#14161A`), rust (`#9C4A28`), olive drab (`#5B6038`), tobacco paper (`#D9CBA8`), signal red (`#C2301F`). **Decopunk:** chrome and black with champagne gold (`#D4B26A`), emerald or deep teal (`#0F5B52`), ivory.
- **Type:** condensed grotesques and stencil faces (Bebas Neue, Oswald, Stencil-style display), Deco geometric caps (Poiret One, Limelight), typewriter mono for dossiers.
- **Texture:** halftone, rivet seams, oil stains, film grain, scratched print, torn poster edges. Noir lighting: venetian-blind light bars.
- **Layout:** diagonal poster compositions, stepped ziggurat frames, sunburst and radial Deco rays, speed lines, heavy rules, number stencils.
- **Iconography:** zeppelins, props, wheels, pistons, radio towers, gauges, ocean liners; bold flat silhouettes.

---

## 🖱️ Interaction and Motion

- Heavy and fast: slide-in panels with a hard ease-out, shutter wipes like venetian blinds, a piston-like press on buttons (80-150 ms).
- Deco variant: sunburst rays rotate slowly or expand on hover; chrome sheen sweeps once on entry.

---

## 🧩 UX Patterns

- **IA and navigation:** a case-file or ticket-counter metaphor: Dossiers (content), Departures (events), Ticket Office (checkout), Archive (search). Use a bold fixed header with plain labels as subtitles; the metaphor yields to convention for cart, login, search, legal and accessibility links (heuristics 2, 4).
- **Key flows:** onboarding as a short "briefing" (3 cards, skip); checkout as a plain high-contrast form, large inputs, visible total, no texture behind fields; search a clear box with recent searches; settings as simple toggles with a stamped section header.
- **Microcopy:** terse, hard-boiled, no purple prose ("Order filed", "No match. Try another name"). Keep fictional-regime and wartime phrasing out of functional copy.
- **States:** loading = shutter or reel with a text status; empty = "Nothing on file" plus an action; error = "Payment bounced. Check the card number or use another." with the field marked; success = a stamped "APPROVED" with order ID (never a real-state stamp).
- **Feedback and affordance:** hard-shadow buttons that press down; red alone never signals error (add icon and text, heuristic 9); visited and active nav stay obvious over busy posters.
- **Trust and load risks:** grit can read as unsafe in payment; aggressive caps and stencil slow reading; menace tone can alienate or alarm.
- **Usability checks:** (1) task success on find-event-and-buy, at least 90%; (2) error rate on form completion, target under 5%; (3) SUS at least 68 (unverified benchmark) and a 5-second test for primary CTA recall.
- Basis: Nielsen's heuristics (NN/g, fetched) and WCAG 2.2 (W3C, fetched). The rest is unverified synthesis.

---

## 🛠️ Implementation Notes

```css
:root { --oil:#14161A; --steel:#2E3338; --rust:#9C4A28; --paper:#D9CBA8; --signal:#C2301F; }
body { background: var(--oil); color: var(--paper); font-family: "Oswald", sans-serif; }
.poster { background:
  repeating-conic-gradient(from 0deg at 50% 100%, #FFFFFF10 0 4deg, transparent 4deg 8deg), var(--steel); }
.blinds { background: repeating-linear-gradient(160deg, #FFFFFF22 0 14px, transparent 14px 38px); }
.btn { background: var(--signal); color:#fff; border:2px solid var(--paper); box-shadow: 4px 4px 0 #000; }
.btn:active { transform: translate(3px,3px); box-shadow: 1px 1px 0 #000; }
.btn:focus-visible { outline: 3px solid var(--paper); outline-offset: 3px; }
@media (prefers-reduced-motion: reduce) { .poster, .blinds { animation: none; } }
```

- Halftone via `radial-gradient` dot grid with `background-size`; film grain via a tiled SVG `feTurbulence` at low opacity.
- Decopunk: stepped corners with `clip-path: polygon()`, gold hairlines with repeated borders, chrome with `linear-gradient` bands.

---

## ♿ Accessibility

- Noir dark UI: confirm 4.5:1 for body (1.4.3) and 3:1 for UI boundaries and icons (1.4.11, W3C); rust and olive on charcoal commonly fail.
- Do not rely on red versus green or rust signals alone (1.4.1).
- Grain, halftone and light bars: keep off text blocks; honor `prefers-reduced-motion: reduce` (MDN) by disabling flicker, sweeps and rotating rays; nothing may flash more than three times per second (2.3.1).
- Condensed caps lower readability: avoid all-caps paragraphs; 1.4.12 text-spacing overrides must not clip.
- Focus must stay visible over busy posters (2.4.7, 2.4.11).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** games, film and book promotion, aviation or motorsport brands, cocktail and jazz venues, history-fiction.
- **Caution:** news or civic sites; heavy grunge hurts perceived trust.
- **Avoid:** healthcare, children's learning, and any context where wartime menace is inappropriate.
- **Cultural and ethical note:** the era's visual language includes real regimes' propaganda. Do not reproduce swastikas, real party insignia or hate imagery; invent fictional states and emblems, and do not glorify fascism, colonial oil politics or war. Oilpunk's Gulf and petro-culture references should be handled with local voices, not exoticism.

---

## ⚠️ Pitfalls

- Reading as generic grunge: no commitment to Deco geometry or noir lighting; Stencil, texture and halftone together reducing legibility; Confusing decopunk's polish with dieselpunk's grease and mixing both without a rule; Propaganda-pastiche that accidentally endorses its source.

---

## 📚 Sources

- Wikipedia contributors, "Dieselpunk" (Wikipedia) — https://en.wikipedia.org/wiki/Dieselpunk (coinage, schools, decopunk; fetched)
- Wikipedia contributors, "Art Deco" (Wikipedia) — https://en.wikipedia.org/wiki/Art_Deco (fetched)
- Wikipedia contributors, "Streamline Moderne" (Wikipedia) — https://en.wikipedia.org/wiki/Streamline_Moderne (fetched)
- MDN, "conic-gradient()" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C, "Understanding SC 1.4.11 Non-text Contrast" (W3C WAI), 2023 — https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- NN/g, Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (fetched)
- Palette and type picks: this skill's suggestions; oilpunk site content `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-art-deco](../ui-style-art-deco/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md).
