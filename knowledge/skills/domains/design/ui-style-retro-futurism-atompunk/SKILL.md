---
name: "ui-style-retro-futurism-atompunk"
description: "Provides the retro-futurism and atompunk UI style (1945-1969 aesthetic, modern revival): Atomic, Jet and Space Age optimism, Googie boomerangs and starbursts, Populuxe pastels, rounded rocket-age type and Cold War era graphics, covering palette, shapes, type, motion and WCAG handling. Use when designing space-age, atomic-diner, sci-fi-heritage or Fallout-like product, game or event surfaces."
---

# UI Style: Retro-Futurism and Atompunk

The past's vision of the future, specifically the 1945-1969 Atomic and Space Age: optimistic, aerodynamic, ornamented with atoms and orbits. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Sci-fi, gaming, diner, travel, museum and event sites with a mid-century-future mood.
- Brands that want optimism and wonder rather than cyberpunk dystopia.
- Requests for "atomic age", "Googie", "raygun gothic", "Populuxe" or "Jetsons" looks.

---

## 🕰️ Definition and Timeline

- Atompunk: pre-digital period 1945-1969; mid-century modernism with Atomic, Jet and Space Ages and Cold War culture; visual style leans Populuxe and Raygun Gothic. Fed by 1950s sci-fi films, early James Bond films, The Twilight Zone. Examples: The Iron Giant, The Incredibles, the Fallout series.
- Googie architecture: Southern California, roughly 1945 to early 1970s; upswept roofs, boomerangs, flying saucers, diagrammatic atoms, parabolas, glass, steel and neon; shaped by Sputnik (1957) and Gagarin (1961); faded after Apollo 11 and anti-nuclear sentiment.
- Term origin for "atompunk": no single coiner is documented; Bruce Sterling discussed it in Wired, December 2008 ("Here Comes 'Atompunk.' And It's Dutch. So there."). The term "retrofuturism" appears from the early 1980s (1981 Trouser Press review).
- Distinction from [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md): cyberpunk is dark, neon, dystopian and digital; this is bright, hopeful, analog and aerodynamic.
- Distinction from [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md): MCM is restrained domestic modernism; atompunk adds space/atomic iconography and exuberance.

---

## 🎨 Visual DNA

- **Shapes:** boomerangs, starbursts, atom orbits, parabolic swooshes, rounded rectangles like appliance and rocket fins; diagonals for speed.
- **Color:** Populuxe pastels (turquoise `#3FB8AF`, salmon `#FF8C69`, butter `#F6D55C`) with chrome-gray and a deep navy or charcoal ground; red-orange as a signal accent.
- **Type:** rounded or slab geometric display, script accents (diner signage), condensed sans for labels; mono for "control panel" readouts.
- **Texture:** halftone, screen-print offset, faint paper aging; avoid photoreal chrome unless sparing.
- **Layout:** asymmetric hero with orbital diagrams, rivet-like dots, control-panel cards with rounded corners.

---

## 🖱️ Interaction and Motion

- Optimistic and mechanical: dial and toggle metaphors, orbit paths rotating slowly, starbursts scaling in 200-400ms.
- Scroll-driven "launch" transitions allowed on hero only; keep the reading column still.

---

## 🛠️ Implementation Notes

```css
:root { --turq:#3fb8af; --salmon:#ff8c69; --butter:#f6d55c; --navy:#12233a; --chrome:#d9dee5; }
body { background: var(--navy); color: #f5f1e6; }
.starburst { clip-path: polygon(50% 0,60% 35%,100% 50%,60% 65%,50% 100%,40% 65%,0 50%,40% 35%); background: var(--butter); }
.orbit { border: 2px solid var(--chrome); border-radius: 50%; animation: spin 24s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }
```

- Draw atoms and rockets as SVG; build swooshes with `border-radius` or `clip-path`, not raster.
- Define pastels as accent tokens and keep text on navy or cream panels.

---

## ♿ Accessibility

- Pastel-on-pastel and pastel-on-white text fail 1.4.3; light text on navy is the safe default; verify at 4.5:1 body, 3:1 large and UI parts (1.4.11).
- Script and display faces must not be used for body text; keep real HTML text (1.4.5) and support spacing overrides (1.4.12).
- Orbiting, spinning or scroll-launch effects: provide pause (2.2.2), respect `prefers-reduced-motion`, no flashing starbursts (2.3.1).
- Diagrams and atoms that carry meaning need text alternatives (1.1.1); decorative ones `aria-hidden`.
- Diagonal layouts must keep reading order logical in DOM (1.3.2, 2.4.3).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** game and film sites, science museums, diners and hospitality, events, retro-themed product launches.
- **Caution:** SaaS (illustration and hero only), content with nuclear subject matter where tone matters.
- **Avoid:** serious institutional, medical or financial flows; contexts where nostalgia for the Cold War is inappropriate.

---

## ⚠️ Pitfalls

- Slipping into cyberpunk neon or generic "retro wave" gradients, which are different styles.
- Skeuomorphic chrome overload hurting performance and contrast.
- Uncritical glamorization of atomic imagery; treat as historical styling.

---

## 📚 Sources

- Wikipedia contributors, "Atompunk" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Atompunk
- Wikipedia contributors, "Googie architecture" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Googie_architecture
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/
- Palette hex values and clip-path starburst are author suggestions, not sourced. Wikipedia, "Retrofuturism" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Retrofuturism (retrofuturism as "depictions of the future as produced in earlier eras"; Raygun Gothic blends Googie, Streamline Moderne and Art Deco).

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md), [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-art-deco](../ui-style-art-deco/SKILL.md), [ui-style-skeuomorphism](../ui-style-skeuomorphism/SKILL.md).
- Related -punk styles: [ui-style-atompunk](../ui-style-atompunk/SKILL.md), [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-steampunk](../ui-style-steampunk/SKILL.md).
