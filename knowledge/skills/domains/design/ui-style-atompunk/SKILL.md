---
name: "ui-style-atompunk"
description: "Provides the atompunk and space-age retro-futurism UI style (1945-1969): atomic-age optimism with Cold War undertones, Googie boomerangs and starbursts, Populuxe pastels, rounded rocket-age type, cantilevered layouts and orbit components. Use when designing retro-space, diner, science-museum, game or nostalgic brand interfaces and their flows."
---

# UI Style: Atompunk & Space-Age Retro-Futurism

The "-punk" genre built on the pre-digital Atomic, Jet, and Space Ages (1945–1969): the glorious tomorrow that mid-century modernism promised, translated into starbursts, pastel chrome, cantilevered layouts, orbit rings, and neon pylon signage. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing interfaces, components, navigation, and flows for sci-fi, games, diners, retro-tech brands, space museums, and editorial features in an atomic-age voice.
- Needing the genre's double edge: sunny technological progress on the surface, civil-defense anxiety underneath.
- Implementing Googie architecture motifs (parabolas, boomerangs, flying saucers, diagrammatic atoms).

---

## 🕰️ Definition and Timeline

- **Era:** Pre-digital period 1945–1969; mid-century modernism fused with Atomic, Jet, and Space Ages and Cold War culture; visual style leans Populuxe and Raygun Gothic. Fed by 1950s sci-fi cinema, early James Bond films, and *The Twilight Zone*. Canonical media: *The Iron Giant*, *The Incredibles*, and the *Fallout* franchise.
- **Atomic Age:** Dated from the Trinity test (16 July 1945). Post-war optimism (Ford Nucleon concept, atomic motifs on household appliances) deepened through the 1960s into fallout shelters and anti-nuclear activism.
- **Googie Architecture:** Southern California, roughly 1945 to early 1970s; name from Googie's Coffee Shop (John Lautner, 1949), popularized by Douglas Haskell in a 1952 *House and Home* article. Characterized by upswept roofs, acute cantilever angles, diagrammatic atoms, glass, steel, and neon pylons.
- **Raygun Gothic & Atompunk:** "Raygun Gothic" was coined by William Gibson in "The Gernsback Continuum" (1981) as a "tomorrow that never was". Atompunk was discussed by Bruce Sterling (*Wired*, 2008), adding the rebellious, anachronistic "-punk" ethos.
- **Distinction from neighbors:** Unlike [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), which is 1920s–1940s industrial grit, chrome-and-steel machinery, and Art Deco, Atompunk is post-war pastel gloss and space optimism. Unlike [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md), which is restrained domestic minimalism, Atompunk adds aerodynamic space/atomic iconography and exuberant futurism.

---

## 🎨 Visual DNA

- **Palette:** Populuxe pastels (turquoise `#2EC4B6`, flamingo `#FF8FA3`, butter `#FFE29A`, salmon `#FF8C69`) on warm cream `#FFF7E6`, anchored by deep navy `#12233A` or charcoal `#1F2933`, with tomato red-orange (`#E4572E`) as a signal accent.
- **Typography:** Rounded or script display for signage (Pacifico or Lobster-class), geometric sans for UI controls (Josefin Sans, Poppins), condensed or atomic-caps for section headers; monospaced readouts for "control panel" telemetry; never use script for body copy.
- **Shapes & Motifs:** Boomerangs, starbursts, kidney and amoeba blobs, atomic orbit rings with orbiting electrons, parabolic swooshes, cantilever diagonals, rocket fins, and rivet-like perimeter dots.
- **Texture & Layout:** Chrome gradients, enamel fills, subtle halftone or screen-print offset under 6% opacity; asymmetric tilted panels, pylon-style navigation bars, and scalloped ticket cards.
- **Iconography:** Diagrammatic atoms, rockets, satellites, rayguns, radar sweeps, and vintage CRT television sets drawn as crisp, single-weight SVGs.

---

## 🖱️ Interaction and Motion

- Orbit rings rotate slowly (`animation: spin 24s linear infinite`); starbursts pulse once on hover; neon flicker on load for under one second.
- Optimistic mechanical transitions: toggle switches and dial rotations (200–400ms ease-out); scroll reveals as angled slide-and-rotate panels (300–500ms).
- Under `prefers-reduced-motion: reduce`, disable all rotations, continuous pulses, and neon flicker, replacing them with instant opacity states.

---

## 🧩 UX Patterns

- **IA and Navigation:** Pylon-sign or "departures board" metaphor with 4–6 prominent sections. Clear, standard labels ("Menu", "Projects", "Contact") accompany themed headers; preserve conventional positions for search, cart, and account (Consistency and Standards).
- **Flows:** Onboarding structured as a 3-step "launch countdown" with an explicit skip button; single-column form layouts with standard validation (WCAG 3.3.7); search inputs remain conventional with retro placeholder copy.
- **Microcopy:** Brochure optimism with concrete information first ("Order confirmed. Launching delivery Thursday"); keep error messages professional and actionable without nuclear jokes in sensitive financial or personal data flows.
- **States:** Empty = "Nothing in orbit yet" with a primary action; Loading = rotating atomic ring with status text; Error = clear explanation and recovery steps (WCAG 3.3.1); Success = starburst badge confirmation.

---

## 🛠️ Implementation Notes

```css
:root {
  --cream: #FFF7E6;
  --ink: #1F2933;
  --navy: #12233A;
  --teal: #2EC4B6;
  --flamingo: #FF8FA3;
  --tomato: #E4572E;
  --butter: #FFE29A;
  --chrome: #D9DEE5;
}
body { background: var(--cream); color: var(--ink); font-family: "Josefin Sans", system-ui, sans-serif; }
.starburst {
  aspect-ratio: 1; background: var(--tomato);
  clip-path: polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
.orbit { border: 2px solid var(--chrome); border-radius: 50%; animation: spin 24s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.panel { transform: rotate(-1.5deg); border-radius: 2rem 0.5rem 2rem 0.5rem; box-shadow: 6px 6px 0 var(--teal); }
@media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }
:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px; }
```

- Draw atoms and rockets as inline SVG using `currentColor` so palette changes require only a token update.
- Use `border-radius` and `clip-path` for aerodynamic swooshes rather than heavy raster assets.

---

## ♿ Accessibility

- **Contrast:** Pastels on cream fail WCAG 1.4.3 (4.5:1 text) and 1.4.11 (3:1 UI borders); keep text on dark navy or charcoal, reserving pastels for card backgrounds and accents.
- **Typography:** Restrict decorative script faces strictly to short titles; maintain high legibility with real HTML text (1.4.5) supporting user spacing overrides (1.4.12).
- **Motion:** Strictly respect `prefers-reduced-motion`; ensure no element flashes more than 3 times per second (WCAG 2.3.1) and provide pause controls for continuous loops (2.2.2).
- **Layout:** Tilted containers must not clip text or interactive focus rings at 400% zoom (1.4.10 Reflow); touch targets must be at least 24×24px (2.5.8).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Space-themed events, diner/hospitality brands, indie games, entertainment microsites, science museums, and retro-futuristic editorial features.
- **Caution:** Commercial SaaS applications (limit styling to heroes, badges, and empty states).
- **Avoid:** Healthcare, safety-critical dashboards, financial banking portals, or contexts where nuclear imagery could trivialize historical weapons testing or radiation hazards. Never use mushroom clouds decoratively.

---

## ⚠️ Pitfalls

- Oversimplifying the style into just pastel colors and rounded fonts while losing the angular Googie structural architecture.
- Conflating Atompunk with cyberpunk neon or synthwave grids, which belong to distinct historical aesthetics.
- Relying on heavy photorealistic chrome skeuomorphism that harms performance and contrast.

---

## 📚 Sources

- Wikipedia, "Cyberpunk derivatives" (Atompunk section) — https://en.wikipedia.org/wiki/Cyberpunk_derivatives
- Wikipedia, "Googie architecture" (origins, starbursts, neon pylons) — https://en.wikipedia.org/wiki/Googie_architecture
- Wikipedia, "Raygun Gothic" (Gibson 1981 coinage) — https://en.wikipedia.org/wiki/Raygun_Gothic
- Wikipedia, "Atomic Age" (1945 start, optimism and Cold War anxiety) — https://en.wikipedia.org/wiki/Atomic_Age
- Bruce Sterling, "Here Comes 'Atompunk.' And It's Dutch. So there.", *Wired*, 2008.
- W3C, "Web Content Accessibility Guidelines 2.2" (1.4.3, 1.4.11, 2.2.2, 2.3.1, 2.5.8) — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For accessibility discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Closest neighbors: [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-mid-century-modern](../ui-style-mid-century-modern/SKILL.md), [ui-style-steampunk](../ui-style-steampunk/SKILL.md).
- Aesthetic contrasts: [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-bauhaus](../ui-style-bauhaus/SKILL.md).
