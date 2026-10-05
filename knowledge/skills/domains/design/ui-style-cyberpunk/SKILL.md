---
name: "ui-style-cyberpunk"
description: "Provides the cyberpunk UI and UX style (1980s-present), with postcyberpunk and cyberprep variants: neon-noir street-level dystopia as components, navigation, flows, microcopy and system states, covering palette, type, texture, motion, CSS/SVG and accessibility. Use when designing game, music, fintech-edge or developer-culture interfaces, weighing neon fatigue and dark-pattern risk."
---

# UI Style: Cyberpunk (with Postcyberpunk and Cyberprep variants)

"High tech, low life" translated to the web: neon light against wet darkness, dense signage, degraded infrastructure and a sense that the interface belongs to someone else's corporation. Distinct from HUD work: this is the world, not the instrument panel. Synthesized from fetched sources; see Sources.

---

## 🧭 When to Activate

- Designing components, navigation, flows and system states (not just visuals) for games, esports, music, film and fiction products with a neon-noir night city mood.
- Tech brands deliberately playing with dystopian irony (security, hacking, crypto-adjacent culture).
- Choosing between the dystopian core, the optimistic postcyberpunk dialect and the leisure-oriented cyberprep dialect.

---

## 🕰️ Definition and Timeline

- Coinage: Bruce Bethke coined the term in 1983 for his short story; Gardner Dozois popularized it through editorials in Isaac Asimov's Science Fiction Magazine. Core formula: "lowlife and high tech" in dystopian futures.
- Canon: Blade Runner (premiered 25 June 1982; Ridley Scott with concept artist Syd Mead, Douglas Trumbull effects; described as "high-tech but decaying" with neon-saturated streets), Akira (1982 manga, 1988 anime), Neuromancer (Ace Books, 1 July 1984; opens on "the sky the color of television tuned to a dead channel"), Mirrorshades (1986, ed. Bruce Sterling), Ghost in the Shell (1995).
- Ethos (the "punk"): marginal hackers and outcasts versus megacorporations, AI and body modification; film noir and hardboiled detective fiction supply the atmosphere; Hong Kong and Tokyo density supply the streets.
- Variants: postcyberpunk keeps augmentation and advanced tech but forgoes the assumption of dystopia; cyberprep keeps the tech in worlds that are "utopian rather than gritty and dangerous," with enhancement for leisure and self-improvement. Cyberprep terminology comes from Wikipedia's derivatives pages; its wider usage is `unverified`.
- Versus [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md): that skill covers futuristic user interface (FUI) telemetry panels and instrument chrome. This skill covers street-level neon-noir atmosphere, signage, narrative framing and genre themes.

---

## 🎨 Visual DNA

- **Palette (core):** near-black blue/violet ground (`#07060f`, `#0d0b1a`), magenta `#ff2a8a`, cyan `#19e6ff`, acid yellow `#f5e642` as sparse signal; one accent per viewport region, not all three.
- **Palette (postcyberpunk):** dusk teal and amber, softer saturation, daylight sections allowed. **Cyberprep:** clean white/chrome surfaces, pastel neon accents, leisure imagery.
- **Type:** condensed sans signage (Bebas Neue, Oswald, Rajdhani), mono for system text (JetBrains Mono, IBM Plex Mono), occasional katakana or kanji as decorative texture only (see Pitfalls). Body stays a calm, readable sans.
- **Texture:** rain streaks, halation glow, scanlines at very low opacity, film grain, dirty-glass overlays, CRT chromatic fringing on headings only.
- **Layout:** dense, overlapping panels like stacked signage; vertical neon text banners; asymmetric grids with one calm reading column; photographic night-city hero with a dark scrim.
- **Iconography:** thin-line schematic glyphs, barcode and QR motifs, corporate logos as fictional world-building, warning stripes.

---

## 🖱️ Interaction and Motion

- Neon flicker on one hero element (3-6 steps, irregular), signage "power-on" on load, glitch offsets on hover for 120-200ms, typewriter or decrypt text for system messages.
- Parallax rain layers behind content; keep foreground text static.
- Always provide a stills-only mode: flicker and glitch are the main vestibular and photosensitivity risks in the genre.

---

## 🧩 UX Patterns

All items below are unverified synthesis except where a source is named.

- **IA and navigation:** metaphor of districts and a "grid" (Market, Archive, Terminal); a persistent top bar plus a command palette (`/` or Ctrl+K) for power users. Yield to convention for primary nav labels, account, cart and search icon placement; the metaphor lives in section names and transitions, not in hiding controls (NN/g heuristics 4 and 6).
- **Onboarding, settings:** a skippable boot sequence (under 5s) ending on a real first task; a Display group (Reduce effects, Contrast boost, Light theme) honoring system preferences.
- **Checkout, forms, search:** drop the fiction: plain labels above fields, visible validation, standard payment patterns, neon only on submit state; terminal-style search input with ordinary results and filters.
- **Microcopy and voice:** terse, dry, second-person system voice ("Access granted", "Signal lost"); every themed message still states the cause and next step in plain words (heuristic 9). Keep irony out of legal, payment and privacy copy.
- **States:** empty = "No signal. Add your first item." with a primary action; loading = progress bar with real percent or step text (heuristic 1), not endless flicker; error = themed header plus plain-language fix and retry; success = brief confirmation line with undo (heuristic 3).
- **Feedback and affordance:** the glow doubles as hover/focus cue but a solid underline, border or icon must also mark interactive elements; thin neon outlines alone read as decoration.
- **Trust and load risks:** dystopian mood plus countdowns, "access denied" gates and fake scarcity edge into dark patterns; avoid. NN/g found light mode generally performs better for readers with normal vision, so keep long text in a lighter or higher-contrast panel and offer a theme choice.
- **Measure:** task success rate on checkout and settings (target at least 90% unaided); time on task versus a plain-theme baseline (themed should not exceed it by more than about 10%, a heuristic threshold, `unverified`); SUS score with a themed versus neutral A/B on at least 5 users per cell.

---

## 🛠️ Implementation Notes

```css
:root { --bg: #07060f; --surface: #12101f; --text: #e9e6ff; --magenta: #ff2a8a; --cyan: #19e6ff; --yellow: #f5e642; }
body { background: radial-gradient(120% 80% at 50% 0, #1a1033 0, var(--bg) 60%); color: var(--text); }
.neon { color: var(--cyan); text-shadow: 0 0 6px color-mix(in srgb, var(--cyan) 70%, transparent), 0 0 24px color-mix(in srgb, var(--cyan) 35%, transparent); }
.panel { background: var(--surface); border: 1px solid color-mix(in srgb, var(--magenta) 60%, transparent); }
.scan::after { content: ""; position: absolute; inset: 0; pointer-events: none;
  background: repeating-linear-gradient(0deg, rgb(255 255 255 / .03) 0 1px, transparent 1px 3px); }
@keyframes flicker { 0%,18%,22%,55%,100% { opacity: 1 } 20%,57% { opacity: .35 } }
.sign { animation: flicker 5s steps(1) infinite; }
@media (prefers-reduced-motion: reduce) { .sign { animation: none; } }
```

- Render glow with `text-shadow`/`filter: drop-shadow` on decorative elements only; never put glow behind body copy.
- SVG: `feTurbulence` plus `feDisplacementMap` for glitch, `feGaussianBlur` for halation; static fallback image for low-power devices.

---

## ♿ Accessibility

- 1.4.3 (Contrast Minimum): neon on black usually passes, but magenta `#ff2a8a` on `#07060f` should be measured; dim "dystopian grey" secondary text is the common failure (needs 4.5:1).
- 1.4.11: thin 1px neon borders on controls must reach 3:1 against the surface; glow does not count.
- 2.3.1: no more than three flashes per second; flicker must be slow and small-area. 2.2.2 (Pause, Stop, Hide): anything auto-animating over 5s needs a pause control. 2.3.3 (Animation from Interactions): motion triggered by scroll or hover must be disableable. Honor `prefers-reduced-motion` by removing flicker, glitch and parallax.
- 1.4.12: scanline and noise overlays must not reduce text legibility; keep `pointer-events: none` and test with text spacing overrides.
- 2.4.7 / 2.4.11: glow can hide focus rings; use a solid high-contrast outline. 1.4.1: do not signal status by hue alone (magenta vs cyan).
- Decorative katakana: mark `aria-hidden="true"`; real foreign-language text needs `lang`.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** game and music launches, fiction and film microsites, hacker-culture events, portfolio heroes.
- **Caution:** SaaS marketing (limit to hero and 404 pages), e-commerce brand pages.
- **Avoid:** long-form reading, banking, healthcare, government, children's products, and data-dense admin tools where glare and noise tax attention.

---

## ⚠️ Pitfalls

- Neon overload: every element glowing erases hierarchy and fatigues the eye on OLED at night.
- Orientalist set dressing: the genre's Tokyo/Hong Kong imagery is a known trope; avoid random East Asian text or signage as pure decoration, and prefer real, correctly written copy or none.
- Irony mismatch: a dystopian corporate-dread mood on a product that asks for trust or payment undermines it.
- The aesthetic is saturated with clichés (purple-pink gradient city); one distinctive material or typographic idea beats stacking all of them.

---

## 📚 Sources

- Wikipedia, "Cyberpunk" (Wikimedia) — https://en.wikipedia.org/wiki/Cyberpunk
- Wikipedia, "Cyberpunk derivatives" (Wikimedia; covers postcyberpunk and cyberprep) — https://en.wikipedia.org/wiki/Postcyberpunk
- Wikipedia (Wikimedia), "-punk", "Blade Runner", "Neuromancer", "Mirrorshades" — https://en.wikipedia.org/wiki/-punk , https://en.wikipedia.org/wiki/Blade_Runner , https://en.wikipedia.org/wiki/Neuromancer , https://en.wikipedia.org/wiki/Mirrorshades
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/ (SC 1.4.3, 1.4.11, 2.3.1, 2.3.3, 2.2.2, 2.4.11)
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed 30 Jan 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/
- Raluca Budiu, "Dark Mode vs. Light Mode: Which Is Better?" (Nielsen Norman Group), 2 Feb 2020 — https://www.nngroup.com/articles/dark-mode/
- Palette, CSS and the UX patterns and thresholds above are original synthesis (`unverified`); Wikipedia pages are summaries, not primary works.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Closest siblings: [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md).
- Related: [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md), [ui-style-biopunk](../ui-style-biopunk/SKILL.md), [ui-style-nanopunk](../ui-style-nanopunk/SKILL.md).
