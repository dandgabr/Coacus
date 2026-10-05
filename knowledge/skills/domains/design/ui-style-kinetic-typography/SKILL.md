---
name: "ui-style-kinetic-typography"
description: "Provides the kinetic typography and motion-first UI style (2016-present): type as the primary visual element, per-glyph masked reveals, variable-font axis morphs, continuous infinite marquee tickers, stock exchange telemetry streams and velocity pacing. Covers GSAP SplitText, Motion springs, WCAG 2.2.2 pause compliance and CLS budgets. Use when designing high-impact type heroes, streetwear drops or telemetry-dense ticker interfaces."
---

# UI Style: Kinetic Typography & Marquee Ticker

Typography elevated to the primary visual architecture: words in motion, per-character staggered reveals, variable-font weight and width morphs, and continuous infinite horizontal marquee tickers. Fuses title sequence film design (Saul Bass) with contemporary streetwear drops (Off-White) and high-density telemetry streams. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- High-impact landing page heroes, brand manifestos, digital agency portfolios, and festival announcements.
- Streetwear drops, live event trackers, financial ticker streaming ribbons, and breaking news portals.
- Choreographing variable-font axes with scroll or hover without inducing layout shift.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in cinematic title design (Saul Bass, Pablo Ferro) and 19th-century stock exchange ticker tapes (reborn in Times Square news zippers, 1928).
- **Web Adoption:** Accelerated by GSAP text plugins and OpenType 1.8 variable fonts (September 2016). Consolidated in contemporary web design through Virgil Abloh's typographic language (2013–2019) and Awwwards type-first portfolios (2019–2023).
- **Difference from neighbors:** Unlike [ui-style-expressive-variable-typography](../ui-style-expressive-variable-typography/SKILL.md), which treats type as monumental, architectural static sculpture, Kinetic Typography prioritizes dynamic velocity, continuous loops, and scroll-linked kinetic momentum.

---

## 🎨 Visual DNA

- **Typography:** Giant display grotesques (10–20vw, Monument Extended, Druk Wide, Anton) paired with tabular monospaced metric streams (Space Mono, JetBrains Mono).
- **Color:** Monochromatic high-contrast bases (pitch black `#0A0A0A` or crisp paper white `#F9F9F9`) energized by singular neon accents: hazard yellow (`#FFE600`), warning orange (`#FF5500`), or electric cyan (`#00F0FF`).
- **Ribbons & Tracks:** Endless horizontal animated marquees running edge-to-edge across screen dividers; rotated marquee banners overlapping content sections.
- **Graphic Accents:** Tabular numerals, live blinking indicator dots, ticker tape arrows (`▲`, `▼`), and crosshair coordinate ticks.

---

## 🖱️ Interaction and Motion

- **Infinite Marquee Loop:** Continuous linear ticker scroll (`animation: marquee 18s linear infinite`).
- **Hover Pause Affordance:** Hovering or focusing a moving ticker instantly freezes the track, allowing comfortable reading (WCAG 2.2.2).
- **Staggered Character Reveals:** Headlines enter with masked per-character vertical slides (`y: 100% -> 0%`, stagger 0.03s).
- **Variable-Axis Breathing:** Interactive hover triggers font-weight expansion from thin to ultra-black (`wght: 200 -> 900`, 300ms ease-out).
- Under `prefers-reduced-motion: reduce`, freeze all infinite ticker animations immediately, displaying static horizontal typographic lists.

---

## 🛠️ Implementation Notes

```css
:root {
  --tk-bg: #0a0a0a;
  --tk-fg: #ffffff;
  --tk-accent: #ffe600;
  --tk-font-mono: 'Space Mono', monospace;
}
.marquee-track {
  display: flex;
  overflow: hidden;
  user-select: none;
  background: var(--tk-accent);
  color: #000000;
  font-family: var(--tk-font-mono);
  font-weight: 700;
  text-transform: uppercase;
}
.marquee-content {
  display: flex;
  flex-shrink: 0;
  animation: scroll-marquee 20s linear infinite;
}
.marquee-track:hover .marquee-content,
.marquee-track:focus-within .marquee-content {
  animation-play-state: paused;
}
@keyframes scroll-marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-100%); }
}
@media (prefers-reduced-motion: reduce) {
  .marquee-content { animation: none; }
}
```

- When splitting text into individual character spans, always place `aria-label` with the full text on the parent heading and `aria-hidden="true"` on the split spans so screen readers do not read letter-by-letter.
- Avoid animating `letter-spacing` directly as it causes heavy browser reflows; animate `transform` or use the variable-font `GRAD` (grade) axis which is reflow-free.

---

## ♿ Accessibility

- **WCAG 2.2.2 (Pause, Stop, Hide):** Any scrolling text track that moves automatically and lasts more than 5 seconds MUST provide an accessible pause mechanism (achieved via `:hover`, `:focus-within`, or an explicit pause button).
- **Reading Speed & Contrast:** Keep moving text large and maintain high contrast (safety yellow on black exceeds 12:1).
- **Screen Reader Integrity:** Ensure split or animated headlines remain accessible as continuous sentences in the accessibility tree.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Product launch drops, music festivals, digital agencies, fashion lookbooks, and high-frequency financial telemetry dashboards.
- **Avoid:** Dense documentation pages, healthcare services, government portals, and long-form editorial articles where motion distracts from comprehension.

---

## 📚 Sources

- Motion (formerly Framer Motion), Matt Perry — https://motion.dev/
- Virgil Abloh, *Figures of Speech*, Prestel, 2019.
- W3C, *Understanding SC 2.2.2: Pause, Stop, Hide*, 2023 — https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- GSAP SplitText & ScrollTrigger Documentation — https://gsap.com/docs/v3/

---

## 🔗 Integration with Other Skills

- Sibling typography styles: [ui-style-expressive-variable-typography](../ui-style-expressive-variable-typography/SKILL.md), [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md), [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md).
