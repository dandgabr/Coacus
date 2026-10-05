---
name: "ui-style-atompunk"
description: "Provides the atompunk UI and UX style (1945-1969 retrofuture): atomic-age optimism with Cold War undertow, covering components (starburst, signage, orbit), navigation and flows, voice and state microcopy, Populuxe palettes, reduced-motion-safe animation and usability checks. Use when designing retro-space, diner, science-museum, game or nostalgic brand interfaces and their flows."
---

# UI Style: Atompunk

The "-punk" genre built on the pre-digital Atomic, Jet and Space Ages: the tomorrow that mid-century America promised and never delivered, translated into starbursts, pastel chrome, cantilevered layouts and neon pylon signage. Synthesized from fetched sources; see Sources.

---

## 🧭 When to Activate

- Designing interfaces, components, navigation and flows (not just look-and-feel) for microsites, games, diners, retro-tech brands or editorial features in an atomic-age voice.
- Needing the genre's double edge: sunny progress on the surface, civil-defense anxiety underneath.
- Choosing between a generic retro look and an atompunk-specific one with its own motifs and tone.

---

## 🕰️ Definition and Timeline

- Era: Wikipedia's derivatives article ties atompunk to the pre-digital period 1945-1969 (Atomic, Jet and Space Ages; mid-century modernism, Cold War espionage, Googie, Populuxe, Raygun Gothic). Coinage date is not given there: `unverified`.
- Atomic Age is dated from the Trinity test, 16 July 1945. Optimism (Ford Nucleon concept, atomic motifs on household goods) darkened through the 1960s into fallout shelters and anti-nuclear activism.
- Googie: roughly 1945 to early 1970s; name from Googie's Coffee Shop (John Lautner, 1949), popularized by Douglas Haskell in a 1952 House and Home article.
- "Raygun Gothic" was coined by William Gibson in "The Gernsback Continuum" (1981), a "tomorrow that never was". It is the aesthetic ancestor; atompunk adds the "-punk" stance (alienated protagonists, rebellion, technology pushed to anachronistic extremes).
- (LitReactor, Hope 2014, humorous) A 2014 LitReactor column glosses atompunk as "dieselpunk, but focused on" the early-1950s post-war era (Daniel Hope, Feb 17 2014): a humorous, low-weight definition.
- Difference from [ui-style-retro-futurism-atompunk](../ui-style-retro-futurism-atompunk/SKILL.md): that skill is the shared Googie / Space Age page. This one is atompunk-specific: genre ethos, dual-tone narrative, a fixed token set and the fallout shadow side. Versus [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md): dieselpunk is 1920s-40s grit and Art Deco; atompunk is post-war gloss.

---

## 🎨 Visual DNA

- **Palette:** Populuxe pastels (turquoise `#2EC4B6`, flamingo `#FF8FA3`, butter `#FFE29A`) on cream `#FFF7E6`, anchored by charcoal `#1F2933` and one hot accent (tomato `#E4572E`). Neon signage tones only on dark navy grounds.
- **Type:** rounded or script display for signage (Pacifico-like scripts, Lobster-like), geometric sans for UI (Josefin Sans, Poppins), condensed or atomic-ish caps for headers; never script for body copy.
- **Shapes:** starbursts, boomerangs, kidney and amoeba blobs, orbit rings with electrons, parabolic arcs, cantilever diagonals, acute angles.
- **Texture and layout:** chrome gradients, enamel fills, grain under 6% opacity; asymmetric tilted panels, pylon-style nav, scalloped ticket cards.
- **Iconography:** atom diagram, rocket, satellite, ray gun, radar sweep, television set; draw as single-weight SVG.

---

## 🖱️ Interaction and Motion

- Orbit rings rotate slowly; starbursts pulse once on hover; neon flicker on load for under one second only.
- Scroll reveals as slide-and-rotate-in of panels from an angled axis, 300-500 ms, ease-out.
- Under `prefers-reduced-motion: reduce`, replace rotation, pulses and flicker with static states or opacity fades.

---

## 🧩 UX Patterns

- **IA and navigation:** a "departures board" or pylon-sign metaphor: 4-6 top sections as signs, with plain labels ("Menu", "Contact") beside any themed name. The metaphor yields to convention for search, cart, account and checkout: keep standard icons, positions and labels (Consistency and Standards).
- **Flows:** onboarding as a 3-step "launch countdown" with skip; forms single-column, no redundant entry (WCAG 3.3.7), no puzzle-style login (3.3.8); search is a plain field with a themed placeholder only.
- **Microcopy:** brochure optimism, concrete first ("Order placed. Arrives Thursday"), one retro flourish per screen at most; no jokes in errors involving money or data.
- **States:** empty = "Nothing in orbit yet" plus one primary action; loading = ring spinner with text for waits over 1 s; error = what failed, why, fix, in text (3.3.1) not red-only; success = starburst confirmation with the next step.
- **Feedback and affordance:** signage-style buttons keep a real button shape, pressed state and focus ring; neon glow is decoration, never the only state cue.
- **Risks:** novelty labels raise recall load (Recognition Rather than Recall); script type and tilt slow scanning; irony about nuclear themes can erode trust.
- **Checks:** task success of at least 90% on find-and-buy tasks; time on task no worse than a plain baseline by more than 10%; SUS of 68 or higher. Review against NN/g's ten heuristics (Visibility of System Status, Error Prevention, Aesthetic and Minimalist Design). Thresholds are `unverified` synthesis; the heuristics are sourced.

---

---

## 🛠️ Implementation Notes

```css
:root {
  --cream: #FFF7E6; --ink: #1F2933; --teal: #2EC4B6; --flamingo: #FF8FA3; --tomato: #E4572E;
}
body { background: var(--cream); color: var(--ink); font-family: "Josefin Sans", system-ui, sans-serif; }
.starburst {
  aspect-ratio: 1; background: var(--tomato);
  clip-path: polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
.orbit { border: 2px solid var(--ink); border-radius: 50%; animation: spin 24s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.panel { transform: rotate(-1.5deg); border-radius: 2rem 0.5rem 2rem 0.5rem; box-shadow: 6px 6px 0 var(--teal); }
@media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }
:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px; }
```

- Build atom, rocket and starburst as inline SVG with `currentColor` so palette swaps stay one token change.

---

## ♿ Accessibility

- Pastels on cream almost always fail 1.4.3 (4.5:1 text) and 1.4.11 (3:1 UI and icon edges); put text on charcoal or tomato-dark, and pastels only as fills.
- Neon on dark: verify contrast per color; avoid glow as the only boundary. Glow or text-shadow must not reduce legibility (1.4.3).
- Script display fonts hurt readability for dyslexic users; restrict to short headings and keep real text, not images of text (1.4.5).
- Motion: honor `prefers-reduced-motion` (MDN, Baseline since January 2020); nothing flashes more than three times per second (2.3.1); pause control for any loop over 5 seconds (2.2.2).
- Tilted layouts must not clip content at 400% zoom (1.4.10 Reflow); targets at least 24 by 24 CSS px (2.5.8); visible focus not hidden by offset shadows (2.4.7, 2.4.11).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** diners and hospitality, indie games and film, science-museum or space-themed brands, editorial retrofuturism, event posters.
- **Caution:** brands tied to energy, nuclear or defense: the iconography invites irony or backlash; handle atom motifs with care.
- **Avoid:** healthcare, safety-critical dashboards, and any context where "atomic" imagery could trivialize real weapons testing or nuclear harm. Do not use mushroom-cloud imagery decoratively.

---

## ⚠️ Pitfalls

- Reducing the style to pastel plus rounded font: it loses the angular, aerodynamic structure.
- Treating nostalgia as neutral: the era's 1950s social norms (gender, race) are not part of the aesthetic worth reviving.

---

## 📚 Sources

- Wikipedia, "Cyberpunk derivatives" (Atompunk and Sandalpunk sections; the -punk framework), accessed 2026 — https://en.wikipedia.org/wiki/-punk
- Wikipedia, "Googie architecture" (era, origin of name, starbursts, neon pylons) — https://en.wikipedia.org/wiki/Googie_architecture
- Wikipedia, "Raygun Gothic" (Gibson 1981 coinage) — https://en.wikipedia.org/wiki/Raygun_Gothic
- Wikipedia, "Atomic Age" (1945 start, optimism and Cold War anxiety) — https://en.wikipedia.org/wiki/Atomic_Age
- Daniel Hope, "Punkpunk: A Compendium of Literary Punk Genres" (LitReactor), 17 Feb 2014 (low-weight, humorous) — https://litreactor.com/columns/punkpunk-a-compendium-of-literary-punk-genres
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Nielsen, "10 Usability Heuristics for User Interface Design" (NN/g), 1994, reviewed 30 Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- W3C, "Web Content Accessibility Guidelines 2.2" (3.3.7, 3.3.8, 3.3.1) — https://www.w3.org/TR/WCAG22/
- Atompunk coinage date and canonical works: `unverified`.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Closest: [ui-style-retro-futurism-atompunk](../ui-style-retro-futurism-atompunk/SKILL.md), [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md).
- Contrast: [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md).
