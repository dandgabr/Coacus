---
name: "ui-style-gothicpunk"
description: "Provides the gothicpunk (gothic-punk) UI and UX style (1991 onward): decadent modern-gothic nihilism from Vampire: The Masquerade, covering components, cathedral-plan navigation and flows, state microcopy, blackletter and serif type, blood-red on near-black palettes and restrained motion. Use when designing horror, dark-fantasy, goth-music or noir interfaces, with careful use of occult imagery."
---

# UI Style: Gothicpunk (Gothic-Punk)

A modern-gothic aesthetic: gothic architecture and ornament seen through punk nihilism and the 1980s-90s goth scene. Terminology comes from tabletop role-playing, not from a literary movement. Synthesized from fetched sources; see Sources.

---

## 🧭 When to Activate

- Designing interfaces, components, navigation and flows (not just look-and-feel) for vampire, horror, dark-fantasy, tabletop RPG, goth-music or noir editorial products.
- Wanting decadence and menace (gold-chased shadows, looming stone, urban decay) without cyberpunk neon.
- Needing a defensible genre origin for a dark, ornamental, textured brand.

---

## 🕰️ Definition and Timeline

- Wikipedia describes Vampire: The Masquerade (White Wolf Publishing, first edition 1991, lead designer Mark Rein-Hagen) as set in a fictionalized "gothic-punk" version of the modern world where players are vampires. Secondary sources (a fan-wiki, Tropedia, low authority) say the term was coined in the first-edition rulebook and quote White Wolf's own gloss ("Gothic image of looming architecture... chased with gold and silver as it watches over the dispossessed... Punk Nihilism echoes in the overpowered despair of dreams destroyed"). I could not read the rulebook itself: the coinage attribution and quote are `unverified` against primary text.
- The Wikipedia "-punk" and derivatives articles do not mention gothicpunk; it is a game-industry label, not an established literary genre.
- Ethos: the "punk" is nihilism and alienation (per the same secondary account, drawn from punk, hardcore and metal), the "gothic" is decadent architecture and goth-scene visuals. Power structures are corrupt and beautiful.
- Gothic architecture roots: Abbey of Saint-Denis (1135-1144) as the first Gothic building; pointed arches, ribbed vaults, flying buttresses, large traceried windows; Gothic Revival from the mid-18th century in England.
- Difference from neighbors: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md) is neon-lit techno-dystopia; [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md) is polished archive refinement with no menace; [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md) is a theming approach, not a mood. Gothicpunk is the ornamental, decadent, urban-horror register.

---

## 🎨 Visual DNA

- **Palette:** near-black `#0B0A0C`, bone `#E9E2D0`, blood red `#8B0A1A`, oxblood `#4A0D14`, tarnished gold `#B08D3C`, cold steel `#7A8089`. Red and gold are accents, never large text fills on black without testing.
- **Type:** blackletter or gothic display for short headings (Textura, Fraktur-style, UnifrakturCook), high-contrast didone or old-style serif for sub-heads (Playfair Display, Cormorant), a clear sans or serif for body; condensed grotesque stamped labels for the punk side.
- **Shapes:** pointed arches, lancet windows, rose-window radial grids, tracery, gargoyle silhouettes, chains, thorn borders, torn paper and photocopy cut-ups.
- **Texture:** film grain, scratched metal, wet-asphalt reflections, halftone photocopy, ink bleed; vignettes toward black.
- **Layout:** vertical emphasis, tall narrow columns, asymmetric zine collage layered over cathedral geometry, dense footer ornament.
- **Iconography:** candles, rosary-free symbols where possible, roses, bats, ankh-less generic sigils, city skylines with spires, fangs, blood drops as single-weight SVG.

---

## 🖱️ Interaction and Motion

- Slow reveals from darkness: fade-up from black, 500-900 ms; flickering candle glow limited to a few small elements.
- Hover: ember-red underline draws in; gargoyle or tracery parallax kept very small.
- Under `prefers-reduced-motion: reduce`, drop flicker, parallax and animated grain; keep static texture.

---

## 🧩 UX Patterns

- **IA and navigation:** a "cathedral plan" metaphor: nave (primary content), side chapels (secondary sections), crypt (archive, settings). Use plain labels beside themed ones; search, cart, account and checkout follow convention (Consistency and Standards).
- **Flows:** onboarding as a 3-step "initiation" with skip and age or content gate where relevant; forms single-column, no redundant entry (WCAG 3.3.7), no cognitive-test login (3.3.8); search a standard field with clear results.
- **Microcopy:** terse, dark, elegant; menace belongs in flavor text, never in instructions, errors or consent copy; no humor about self-harm or real violence.
- **States:** empty = "Nothing stirs here" plus an action; loading = candle or ring with text status for waits over 1 s; error = cause and fix in text (3.3.1), not red alone; success = a small gold seal and next step.
- **Feedback and affordance:** dark ornament must not hide controls; buttons keep clear shape, hover, pressed and focus states; destructive actions (delete, "embrace" metaphors) get explicit confirmation or undo (User Control and Freedom).
- **Risks:** low-contrast darkness raises cognitive load and eye strain; dense ornament harms Aesthetic and Minimalist Design; dark patterns hide easily in moody UI, so keep cancel and unsubscribe visible.
- **Checks:** task success of at least 90% on core tasks at night-mode brightness; time on task within 10% of a plain baseline; SUS of 68 or higher. Review against NN/g heuristics (Visibility of System Status, Error Prevention). Thresholds are `unverified` synthesis; the heuristics are sourced.

---

---

## 🛠️ Implementation Notes

```css
:root { --ink:#0B0A0C; --bone:#E9E2D0; --blood:#C1121F; --gold:#B08D3C; }
body { background: var(--ink); color: var(--bone); font-family: "Cormorant Garamond", Georgia, serif; font-size: 1.125rem; line-height: 1.6; }
h1 { font-family: "UnifrakturCook", "Old English Text MT", serif; font-weight: 700; letter-spacing: .02em; }
.lancet { clip-path: polygon(50% 0, 100% 35%, 100% 100%, 0 100%, 0 35%); border-top: 2px solid var(--gold); }
.grain::after {
  content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .06;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><filter id='n'><feTurbulence baseFrequency='.8'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
a { color: var(--blood); text-decoration-thickness: 2px; text-underline-offset: 4px; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }
```

- Blood red `#C1121F` on `#0B0A0C` is for large text and graphics only; verify ratios and use bone for body.

---

## ♿ Accessibility

- Dark ground with red text frequently fails 1.4.3; body text in bone, red for large text (3:1) and UI edges (1.4.11); test each pair.
- Blackletter and ornate display faces are hard to read (1.4.3 intent, cognitive load); restrict to short headings, sentence-case body, adequate size.
- Texture and grain overlays must not reduce text contrast; keep opacity low and `pointer-events: none`; offer a no-texture setting where heavy.
- Flicker and flashing: nothing above three flashes per second (2.3.1); respect `prefers-reduced-motion` (MDN); pause for loops (2.2.2).
- Visible focus on dark surfaces (2.4.7, 2.4.11), targets 24 px minimum (2.5.8), and content warnings for graphic imagery before gore or violence.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** horror and vampire games, dark-fantasy and RPG sites, goth and metal music, film and book promotion, nightlife brands, noir editorial.
- **Cultural sensitivity:** gothicpunk draws on Christian architecture and liturgical imagery, occult symbols and folk belief. Use crosses, pentagrams, rosaries and religious relics intentionally and not as shock decor; avoid mocking living faiths. Blackletter has a political history: it was banned by Hitler in 1941 per a Nazi memorandum (Wikipedia), yet is also in neo-Nazi use today `unverified`; avoid pairing it with extremist symbols and consider this when choosing it for German-language or heritage contexts.
- **Avoid:** healthcare, children's, finance, public services, and any context where doom mood undermines trust or accessibility.

---

## ⚠️ Pitfalls

- Illegible red-on-black and blackletter paragraphs.
- Claiming a literary pedigree: the label is from tabletop gaming and is `unverified` beyond that.

---

## 📚 Sources

- Wikipedia, "Vampire: The Masquerade" (White Wolf, 1991, Mark Rein-Hagen; "gothic-punk" wording) — https://en.wikipedia.org/wiki/Vampire:_The_Masquerade
- Tropedia, "Gothic Punk" (fan wiki, low authority; paraphrases White Wolf quote) — https://tropedia.fandom.com/wiki/Gothic_Punk
- Wikipedia, "Gothic architecture" (Saint-Denis 1135-1144; features; Gothic Revival) — https://en.wikipedia.org/wiki/Gothic_architecture
- Wikipedia, "Blackletter" (origin, Textura/Fraktur, 1941 ban) — https://en.wikipedia.org/wiki/Blackletter
- Wikipedia, "-punk" / "Cyberpunk derivatives" (no gothicpunk entry; -punk ethos) — https://en.wikipedia.org/wiki/-punk
- Nielsen, "10 Usability Heuristics for User Interface Design" (NN/g), 1994, reviewed 30 Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- W3C, "Web Content Accessibility Guidelines 2.2" (3.3.7, 3.3.8, 3.3.1) — https://www.w3.org/TR/WCAG22/
- MDN, "prefers-reduced-motion" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- First-edition rulebook text for "Gothic Punk": not read, `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
- Contrast: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md).
