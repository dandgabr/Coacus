---
name: "ui-style-nanopunk"
description: "Provides the nanopunk UI and UX style (1990s-present, weak visual canon): speculative nanotech themes translated into scale-based navigation, grounded components, flows, microcopy and swarm or lattice visuals, covering CSS/SVG and accessibility. Use when a nanotech, materials-science, medtech or deep-tech product needs a molecular-scale interface language and accepts that the genre defines themes more than a look."
---

# UI Style: Nanopunk

A theme more than a look. Nanopunk fiction is about the societal, psychological and bodily impact of nanotechnology; it has no canonical film palette comparable to cyberpunk's neon. This skill is therefore a set of grounded design metaphors (swarm, lattice, scale shift), not a recreation of a fixed visual canon.

---

## 🧭 When to Activate

- Nanotech, advanced materials, semiconductor, biomedical or deep-tech products needing a micro-scale interface language (components, navigation, flows, states), not only visuals.
- Speculative fiction and game projects where nanites are central.
- Deciding whether to commit to a genre label that lacks a recognizable aesthetic.

---

## 🕰️ Definition and Timeline

- Definition: worlds where nanites and bio-nanotechnologies are widely in use and nanotechnology dominates society; focus is on artistic, psychological and societal impact rather than technical detail. Outlook ranges from dystopian risk to optimistic benefit.
- Roots and canon (per Wikipedia): Feynman's 1959 talk and K. Eric Drexler's 1986 Engines of Creation popularized the idea; Neal Stephenson, The Diamond Age (Bantam Spectra, 1995; New Chusan, matter compilers; Hugo 1996), also classed as postcyberpunk; Kathleen Ann Goonan, Queen City Jazz (1997); Linda Nagata; Michael Crichton, Prey (2002); Generator Rex (2010-2013); games such as Crysis, Deus Ex, Metal Gear Solid.
- Recognized as a category in the 2000s; the precise coinage date and originator are `unverified`.
- Honest limit: these works share a concept, not a style. Crysis, Prey and The Diamond Age look nothing alike. Any "nanopunk aesthetic" is an editorial synthesis (fan sources such as Aesthetics Wiki are low authority).
- Versus [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md): no street-level neon-noir by default; the tone can be clinical or hopeful. Versus [ui-style-biopunk](../ui-style-biopunk/SKILL.md): matter and machines at molecular scale rather than organisms and wetware.

---

## 🎨 Visual DNA

- **Palette:** clean lab dark or pale ground (`#0a0f14` or `#f4f7f9`), one luminous signal hue (cold cyan `#4de3ff`, or silver-green `#9ff0d0`), graphite and iridescent greys; avoid neon triads.
- **Type:** precise geometric or technical sans (Space Grotesk, IBM Plex Sans, Sora), mono for measurements (nm, µm, ratios); tight, light-weight display at large size, generous space.
- **Texture:** fine dot fields, hex and diamond lattices, particle clouds, depth-of-field blur, macro-photography softness, thin hairlines.
- **Layout:** scale-shift storytelling (zoom from object to cell to lattice), centered figure with measurement annotations, generous negative space.
- **Iconography:** nodes and edges, hexagonal cells, scale bars, assembler-arm line drawings; avoid generic "DNA helix" (that is biopunk).

---

## 🖱️ Interaction and Motion

- Particles that coalesce into a shape on scroll, hover that disperses then reassembles a swarm, cursor-reactive lattice distortion, zoom transitions between scales.
- Keep loops slow (6-20s) and subtle; the idea is quiet, pervasive activity. Pause when off screen.

---

## 🧩 UX Patterns

All items below are unverified synthesis except where a source is named.

- **IA and navigation:** the metaphor is scale: Overview, Structure, Detail (macro to micro) as a breadcrumb or zoom rail. Yield to convention for global nav, search, account and docs links; zoom is an enhancement over ordinary links, never the only route (NN/g heuristics 4 and 7).
- **Onboarding:** one guided "zoom in" tour of 3 steps maximum, skippable and replayable from Help; teach the scale control by using it.
- **Forms and checkout:** calm, clinical and precise: labels above fields, units shown (nm, µm, mg), inline validation, no animation during input. Search: faceted filters by property (size, material, state) with plain result lists.
- **Settings:** Reduce motion, Particle density, Contrast, Units; defaults follow system preferences.
- **Microcopy and voice:** measured lab-notebook tone ("Assembling... 3 of 5 steps"), concrete numbers over hype; no unsupported claims in medical or materials contexts.
- **States:** empty = a sparse lattice with "Nothing assembled yet" and a primary action; loading = determinate step text, not a swirling swarm (heuristic 1); error = what failed, which step, how to retry (heuristic 9); success = settle animation under 400ms plus a text confirmation.
- **Feedback and affordance:** particles converge on the control being pressed, but buttons keep standard shape, label and focus outline; hairline dots are never the only clue to interactivity.
- **Trust and load risks:** futuristic-science styling can over-signal authority, so cite data and avoid implied efficacy. Particle backdrops add visual noise and raise cognitive load (heuristic 8); NN/g reports light mode generally performs better for normal-vision readers, so keep dense text on a plain, high-contrast surface and offer a theme toggle.
- **Measure:** task success on find-a-property and complete-a-form tasks (target at least 90% unaided); time on task versus a plain baseline; SUS comparison themed versus neutral; threshold targets are `unverified`.

---

## 🛠️ Implementation Notes

```css
:root { --bg: #0a0f14; --ink: #dff6ff; --signal: #4de3ff; --hair: rgb(77 227 255 / .25); }
body { background: var(--bg); color: var(--ink); font-family: "Space Grotesk", system-ui, sans-serif; }
.lattice { background-image:
  radial-gradient(circle, var(--hair) 1px, transparent 1.5px);
  background-size: 22px 22px; }
.scale-bar { border-top: 1px solid var(--signal); font: 12px/1.4 "IBM Plex Mono", monospace; }
.swarm { animation: drift 14s ease-in-out infinite alternate; }
@keyframes drift { to { transform: translate3d(6px, -4px, 0) } }
@media (prefers-reduced-motion: reduce) { .swarm { animation: none; } }
```

- Particles: canvas or WebGL with a capped count, device-pixel-ratio cap and a static SVG poster fallback.
- Ground claims in the real: use real scale data (nm values) only if verified by the client.

---

## ♿ Accessibility

- 1.4.3 (Contrast Minimum) and 1.4.11 (Non-text Contrast): pale-cyan hairlines and dotted textures on dark grounds are low contrast; informational lines need 3:1, text 4.5:1.
- 2.3.1 and 2.2.2 (Pause, Stop, Hide): particle shimmer must not flash; provide a pause control for animation longer than 5s; 2.3.3: scroll- or pointer-triggered motion must be disableable; honor `prefers-reduced-motion` by showing a static composition.
- 1.1.1: provide text alternatives for scientific diagrams (what the scale shift shows); canvas needs a DOM fallback.
- 1.4.1: do not use color alone to encode particle states or data categories.
- 1.4.12: dense dot textures behind text must stay behind a solid or scrimmed panel.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** deep-tech and materials brands, medtech marketing heroes, science communication, game lore sites.
- **Caution:** health claims; futuristic nano imagery can imply unproven efficacy.
- **Avoid:** audiences expecting a recognizable genre look, content-heavy documentation, and any context where fear of "grey goo" would mislead.

---

## ⚠️ Pitfalls

- Pretending a canon exists: labelling generic particle-network visuals "nanopunk" is marketing, not genre fidelity.
- Stock "glowing network" clichés shared with every AI and blockchain site.
- GPU-heavy particle fields hurting Core Web Vitals and battery.
- Scientific overreach: invented nanoscale facts in medical or materials contexts.

---

## 📚 Sources

- Wikipedia, "Nanopunk" (Wikimedia) — https://en.wikipedia.org/wiki/Nanopunk
- Wikipedia, "Cyberpunk derivatives" (Wikimedia) — https://en.wikipedia.org/wiki/Postcyberpunk
- Wikipedia, "-punk" (Wikimedia) — https://en.wikipedia.org/wiki/-punk
- Wikipedia, "The Diamond Age" (Wikimedia) — https://en.wikipedia.org/wiki/The_Diamond_Age
- Wikipedia, "Nanotechnology in fiction" (Wikimedia) — https://en.wikipedia.org/wiki/Nanotechnology_in_fiction
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/ (SC 1.4.3, 1.4.11, 2.3.1, 2.3.3, 2.2.2)
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed 30 Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- Raluca Budiu, "Dark Mode vs. Light Mode: Which Is Better?" (Nielsen Norman Group), 2 Feb 2020 — https://www.nngroup.com/articles/dark-mode/
- Visuals, CSS and UX patterns above are original synthesis; no primary visual canon was found (`unverified`).

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Closest siblings: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md), [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md).
- Related: [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md).
