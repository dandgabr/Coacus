---
name: "ui-style-sandalpunk"
description: "Provides the sandalpunk (bronzepunk) UI and UX style: a retrofuturist ancient world where Greek, Roman or Egyptian civilization never fell, covering components (stele cards, dials, friezes), navigation and flows, state microcopy, marble and bronze palettes and monumental capitals. Use when designing history, education, mythology, game or heritage interfaces, with care around real cultures."
---

# UI Style: Sandalpunk (Bronzepunk)

A speculative-fiction aesthetic that imagines classical-era technology (Archimedes, Hero of Alexandria, the Antikythera mechanism, bronze automata) advanced into a futuristic world while ancient cultural identity persists. Translated here into marble, bronze, monumental type and engraved geometry. Synthesized from fetched sources; see Sources. The genre is niche and loosely defined.

---

## 🧭 When to Activate

- Designing interfaces, components, navigation and flows (not just look-and-feel) for mythic or classical-future games, tabletop settings, museum features or editorial about the ancient world.
- Wanting gravitas without Victorian steam: stone, bronze and geometry instead of brass and gears.
- Needing a genre frame for "what if Rome never fell" worldbuilding sites.

---

## 🕰️ Definition and Timeline

- Wikipedia's derivatives article describes sandalpunk (also "Bronzepunk") as imagining ancient civilizations such as Rome or Egypt that "never collapsed, instead evolving into futuristic superpowers while preserving their ancient cultural identity". No coinage date or originator is given there: `unverified`.
- A 2014 LitReactor column (Daniel Hope) lists sandalpunk with bronzepunk, ironpunk and candlepunk as ever-finer period labels and treats them with humor: the genre is thin and contested, so avoid claiming a canon.
- The "-punk" suffix carries the cyberpunk legacy: technology as world-foundation, marginalized protagonists, rebellion, sometimes utopia. Here the tension is empire versus the enslaved or conquered; a good sandalpunk UI can carry that irony.
- Difference from neighbors: [ui-style-steampunk](../ui-style-steampunk/SKILL.md) is Victorian brass and steam; [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md) is Renaissance clockwork; [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md) is a refined archive look with no fictional technology. Sandalpunk is classical antiquity plus speculative machinery.

---

## 🎨 Visual DNA

- **Palette:** marble white `#F4F1EA`, warm travertine `#D9CBB0`, bronze `#8C5A2B` / `#B87333`, verdigris `#3E8E7E`, Tyrian purple `#66023C`, lapis `#1F3A93`, obsidian `#16130F`. Gold only as a thin accent.
- **Type:** monumental Roman capitals for headings (the Trajan typeface, Carol Twombly 1989 for Adobe, derives from the capitalis monumentalis of Trajan's Column and is caps-only, display-size, and heavily overused in film posters); a humanist serif body (Cormorant, EB Garamond, Source Serif); Greek-letter numerals as accents.
- **Shapes:** columns and entablatures, pediments, arches, meander (Greek key) borders, laurel wreaths, amphora silhouettes, hexagonal tessellations, circular astrolabe and Antikythera dials.
- **Texture:** marble veining (subtle SVG noise), hammered bronze, incised-stone letters via inset text-shadow.
- **Layout:** symmetrical, axial, frieze-like horizontal bands, generous margins; cards as steles and tablets.
- **Iconography:** aeolipile, water clock, gear dials with Greek lettering, bronze owls and winged automata, trireme. Single-weight engraved line.

---

## 🖱️ Interaction and Motion

- Slow, weighty: dials rotate in measured steps, panels slide like doors on a temple, 400-700 ms ease-in-out.
- Hover engraves: letters darken and underline with a drawn meander line.
- Under `prefers-reduced-motion: reduce`, replace dial rotation and slides with opacity or static state changes.

---

## 🧩 UX Patterns

- **IA and navigation:** a forum or temple-precinct metaphor: Agora (home), Library (docs), Workshop (product), Oracle (help), each with a plain subtitle. Metaphor yields to convention for search, cart, account, settings and checkout (Consistency and Standards).
- **Flows:** onboarding as a short "initiation" of 3 steps with skip; forms in single columns with clear labels, no redundant entry (WCAG 3.3.7) and no cognitive-test login (3.3.8); search is a standard field, not a scroll-and-find "archive".
- **Microcopy:** measured, declarative, slightly formal; Latin or Greek only as decoration beside the English label; never obscure an action behind a mythic name.
- **States:** empty = "The scroll is blank" plus a primary action; loading = slow dial with a text status for waits over 1 s; error = plain cause and fix in text (3.3.1); success = a laurel mark with the next step.
- **Feedback and affordance:** engraved surfaces still need clear button shapes, hover and pressed states and focus rings; dial steps must announce value changes to assistive tech.
- **Risks:** mythic labels raise recall load (Recognition Rather than Recall); caps and tracking slow reading; "empire" tone can read as authoritarian in trust-sensitive flows.
- **Checks:** task success of at least 90% on locating a named page; first-click accuracy on nav of at least 80%; SUS of 68 or higher. Review against NN/g heuristics (Match Between System and the Real World, Visibility of System Status, Error Prevention). Thresholds are `unverified` synthesis; the heuristics are sourced.

---

---

## 🛠️ Implementation Notes

```css
:root { --marble:#F4F1EA; --bronze:#8C5A2B; --ink:#16130F; --verdigris:#3E8E7E; }
body { background: var(--marble); color: var(--ink); font-family: "EB Garamond", Georgia, serif; }
h1, h2 { font-family: "Cinzel", "Trajan Pro", serif; text-transform: uppercase; letter-spacing: .12em; }
.meander {
  height: 14px; border-block: 2px solid var(--bronze);
  background: repeating-linear-gradient(90deg, var(--bronze) 0 2px, transparent 2px 14px);
}
.stele { border: 2px solid var(--bronze); border-radius: 2px 2px 40% 40% / 2px 2px 14% 14%; padding: 2rem; }
.dial { transition: transform .6s steps(12, end); }
@media (prefers-reduced-motion: reduce) { .dial { transition: none; } }
:focus-visible { outline: 3px solid var(--verdigris); outline-offset: 3px; }
```

- All-caps headings: keep them short; apply `lang` attributes if Greek or Latin text is included.

---

## ♿ Accessibility

- Widely tracked capitals reduce reading speed: limit to headings, real text only (1.4.5), body in mixed case.
- Contrast: 4.5:1 for body text, 3:1 for dial and meander UI edges (1.4.3, 1.4.11); gold-on-marble routinely fails.
- Decorative frieze and column backgrounds must carry no meaning; use `aria-hidden` on ornaments.
- Motion: honor `prefers-reduced-motion`; avoid parallax tied to scroll (vestibular); pause control for loops (2.2.2).
- Focus: 2.4.7 and 2.4.11 not obscured by sticky ornamental headers; targets 24 px minimum (2.5.8); Greek or Latin passages marked with `lang` (3.1.2).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** fantasy and historical games, museum and archive features, mythic brands, education about antiquity, premium editorial.
- **Cultural sensitivity:** the genre borrows from real civilizations (Greece, Rome, Egypt, others) whose symbols still carry meaning. Consult the culture's own scholarship, avoid caricature, and do not use sacred or religious imagery as mere decoration. Slavery, conquest and imperial violence were real: do not present empire as pure aspiration, and avoid fascist-adjacent revival of Roman imagery (fasces, eagle standards, salutes) that extremist movements have appropriated.
- **Avoid:** finance and legal brands implying authority through marble clichés, and any product where the aesthetic stands in for real history.

---

## ⚠️ Pitfalls

- Marble-and-gold stock look that reads as a luxury-condo template.
- Using Trajan-style caps everywhere: the overuse is a known meme.

---

## 📚 Sources

- Wikipedia, "Cyberpunk derivatives" (redirect target of "Sandalpunk"; Bronzepunk definition) — https://en.wikipedia.org/wiki/Sandalpunk
- Daniel Hope, "Punkpunk: A Compendium of Literary Punk Genres" (LitReactor), 17 Feb 2014 — https://litreactor.com/columns/punkpunk-a-compendium-of-literary-punk-genres
- Wikipedia, "Trajan (typeface)" (Carol Twombly, 1989, Adobe) — https://en.wikipedia.org/wiki/Trajan_(typeface)
- Aesthetics Wiki, "Sandalpunk" (low authority, lead only; example works such as Atlantis: The Lost Empire, `unverified` as canon) — https://aesthetics.fandom.com/wiki/Sandalpunk
- Nielsen, "10 Usability Heuristics for User Interface Design" (NN/g), 1994, reviewed 30 Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- W3C, "Web Content Accessibility Guidelines 2.2" (3.3.7, 3.3.8, 3.3.1) — https://www.w3.org/TR/WCAG22/
- MDN, "prefers-reduced-motion" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Coinage date, originating authors and canonical works of sandalpunk: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-clockpunk](../ui-style-clockpunk/SKILL.md), [ui-style-steampunk](../ui-style-steampunk/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
- Contrast: [ui-style-art-deco](../ui-style-art-deco/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
