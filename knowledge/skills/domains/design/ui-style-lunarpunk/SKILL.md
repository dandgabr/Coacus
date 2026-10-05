---
name: "ui-style-lunarpunk"
description: "Provides the lunarpunk UI and UX style (circulating by 2022): solarpunk's nocturnal sibling pairing night settings, bioluminescent glow and violet palettes with calm night-first flows, consent and privacy patterns and restful microcopy, covering palette, components and dark-mode contrast. Use when designing privacy-first, wellness, night-mode or community-safety products."
---

# UI Style: Lunarpunk

A darker, introspective branch of solarpunk: sustainable, green futures seen at night, with bioluminescence, mystery and, in crypto circles, privacy by design. Synthesized from the sources below; see Sources.

---

## 🧭 When to Activate

- Designing night-first components, patterns and flows for meditation, sleep, astronomy, folklore, music, games or communities with a spiritual or occult-adjacent tone.
- Privacy, consent, encryption and zero-knowledge products whose UX must make hidden-by-default data understandable and controllable.
- Brands and design systems that share solarpunk values but need an after-dark mood.

---

## 🕰️ Definition and Timeline

- Wikipedia: "a subgenre of solarpunk with a darker aesthetic" leaning toward fantasy, with night settings (often bioluminescence and purple), spirituality or the occult, green cities, sustainable technologies and a more introspective side of solarpunk utopias.
- Chronology: the earliest dated source read is a March 3, 2022 community article presenting lunarpunk as solarpunk's nocturnal counterpart; the term's coinage date and originator are `unverified` (the page does not state them).
- Two strands: (1) the aesthetic/fiction strand above (night, cycles, mystery); (2) a crypto-privacy strand, descended from cypherpunk, centered on encryption, opacity and zero-knowledge proofs against surveillance. State which strand a project follows.
- Versus [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md): same ecological optimism, inverted light. Versus [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md) and [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md): lunarpunk is not neon-noir dystopia; its darkness is restful and communal. Versus [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md): that skill is a theming system; this adds genre iconography and ethos.

---

## 🎨 Visual DNA

- **Color:** midnight ground (`#0E1224`, `#141A33`), violet (`#7C5CFF`), orchid (`#B57BEE`), bioluminescent teal (`#2FE0C2`), moon silver (`#D9DEF2`), restrained firefly gold (`#F2D36B`). Glow as accent, not wash.
- **Type:** elegant but organic: Cormorant, Fraunces or Spectral for display; clean humanist sans for body at generous size and line height; thin celestial or runic ornament sparingly.
- **Motifs:** crescent and phase cycles, mushrooms and moths, constellations, fireflies, mist, glowing flora, lantern-lit green rooftops, star charts, tarot-like framing (handled respectfully).
- **Layout:** layered depth through translucency and soft vignettes; large calm negative space; centered or radial compositions that echo the moon.
- **Privacy iconography (crypto strand):** veils, blurred or redacted panels that reveal on intent, lock-and-leaf hybrids.

---

## 🖱️ Interaction and Motion

- Slow, lunar timing: 600-1200ms fades, phase transitions, pulses at about 4s period; glow intensifies on focus or hover.
- Reveal-on-intent for private data (blur to clear on click), never on mere hover for touch users.
- Starfield or firefly canvases are optional ambience: cap particle counts, pause offscreen.

---

## 🧩 UX Patterns

- **IA and navigation:** a "night sky" or lunar-cycle metaphor (phases, constellations, rooms) for content groups; keep a persistent, plainly labeled primary nav, search, account and help. Metaphor gives way to convention for navigation, forms, checkout and settings; do not hide controls in "mystery" (Nielsen heuristics 2, 4 and 6).
- **Flows:** onboarding is unhurried and explains what is stored, where and for how long before asking for anything; ask once (WCAG 3.3.7); authentication offers methods without cognitive tests such as puzzle recall or transcription (WCAG 3.3.8), e.g. passkeys and password-manager-friendly fields.
- **Privacy and consent UX:** private by default; per-purpose toggles with equal-weight Accept and Decline, plain-language summary, reversible at any time from settings (heuristic 3); show a "what is visible to whom" panel; reveal-on-intent is an explicit button, never hover, and always re-hides.
- **Search and settings:** local or encrypted search should say what it can and cannot see; settings group Privacy, Notifications, Quiet hours; "Day theme" toggle always present.
- **Voice:** calm, gentle, non-alarmist ("Your data stays on this device"); no fear tactics, no occult jargon where plain words serve.
- **States:** empty = a quiet prompt ("Nothing here yet. The night is open."); loading = slow fade plus text status (heuristic 1); error = what happened, what is safe, how to retry (heuristic 9); success = a restrained glow plus explicit confirmation text.
- **Risks:** low-light fatigue and halation; opacity mistaken for security or, inversely, hiding information users need (recognition over recall); dark-pattern consent when glow guides only toward "Accept".
- **Checks:** task success for 3 privacy tasks (find what is stored, revoke consent, delete account) at or above 90 percent; time on task; comprehension quiz of the consent summary (unverified synthesis); SUS; test in dim and bright ambient light.

---

## 🛠️ Implementation Notes

```css
:root {
  --night: #0E1224; --night-2: #141A33; --moon: #D9DEF2;
  --violet: #7C5CFF; --glow: #2FE0C2; --gold: #F2D36B;
}
body { background: radial-gradient(120% 80% at 50% 0%, var(--night-2), var(--night)); color: var(--moon); }
.glow-card { background: rgb(20 26 51 / .72); border: 1px solid rgb(124 92 255 / .55);
  box-shadow: 0 0 24px -6px rgb(47 224 194 / .45); border-radius: 20px; }
.firefly { animation: drift 9s ease-in-out infinite alternate; }
@keyframes drift { to { transform: translate(12px, -18px); opacity: .5; } }
.private { filter: blur(6px); transition: filter .4s; }
.private[data-revealed="true"] { filter: none; }
@media (prefers-reduced-motion: reduce) { .firefly { animation: none; } .private { transition: none; } }
```

- Provide a light theme via `prefers-color-scheme` or a toggle; the style is night-first, not night-only.
- Prefer CSS gradients and SVG over heavy video; glow via `box-shadow` or `drop-shadow` is cheap.

---

## ♿ Accessibility

- Dark ground needs light text: keep body text at 4.5:1 or better (1.4.3); violet on midnight often falls short, so lighten (`#A794FF`) for text and keep saturated violet for fills.
- Glow is not a boundary: borders and icons still need 3:1 (1.4.11); focus indicators must be clearly visible against glow (2.4.7, 2.4.13).
- Avoid pure white on pure black halation for long text; use off-white and 1.6+ line height. Support `prefers-contrast` and forced colors with real borders.
- Blur-to-reveal private fields must be keyboard operable with an accessible name and not expose content to assistive tech while hidden if it is meant to be private (4.1.2).
- Flashing or pulsing under 3 per second (2.3.1); honor `prefers-reduced-motion`; give a pause for ambient loops (2.2.2).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** wellness and sleep, astronomy, fantasy and music brands, creative communities, privacy tools with a humane voice.
- **Caution:** low-vision-heavy audiences (dark UI is not universally easier to read); spiritual imagery, which should respect real traditions rather than costume them.
- **Avoid:** data-dense enterprise tools, outdoor or bright-sun mobile contexts, products that need urgent legibility.

---

## ⚠️ Pitfalls

- Muddy low-contrast purple-on-navy; glow overload that destroys hierarchy.
- Treating "private" as pure aesthetics: opacity in the UI is not security (see the security-privacy skill).
- Conflating the crypto-bro strand with the fiction strand; sources on the crypto framing are low-authority essays and blogs.
- Generic "dark mode plus purple" with no ecological or communal content.

---

## 📚 Sources

- "Cyberpunk derivatives" (Wikipedia), accessed 2026, lunarpunk entry quoted above — https://en.wikipedia.org/wiki/Cyberpunk_derivatives
- "Solarpunk" (Wikipedia), accessed 2026 — https://en.wikipedia.org/wiki/Solarpunk
- "What is Lunarpunk?" (Solarpunk Station), March 3, 2022 — https://solarpunkstation.com/2022/03/03/what-is-lunarpunk/ (page read; community blog, low authority: nocturnal counterpart to solarpunk; purple and black bioluminescent palettes; mushroom-derived materials; restorative, safe-night-space ethos; the page does not say when the term originated)
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (page read)
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", 12 December 2024 — https://www.w3.org/TR/WCAG22/ (3.3.7 and 3.3.8 text read; consent-pattern specifics are unverified synthesis)

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-gothicpunk](../ui-style-gothicpunk/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md).
