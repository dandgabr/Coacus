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

- **Infinite Marquee Loop:** Continuous linear ticker scroll built from one duplicated track translated by `-50%`; the CSS default is `20s`, and script replaces it with a duration derived from the copy width so speed stays constant (see Implementation Notes).
- **Pause Control First:** A visible pause/play button owns playback. Hover and focus pause is a convenience on top of it; on its own it does not satisfy WCAG 2.2.2, because touch, keyboard-only and screen-reader users never hover.
- **Staggered Character Reveals:** Headlines enter with masked per-character vertical slides (`y: 100% -> 0%`), with the total stagger capped. Split, stagger, scramble and typewriter mechanics, including the accessible-name pattern, live in [text-effect-recipes.md](../ui-motion-interaction/references/text-effect-recipes.md); do not restate them here.
- **Variable-Axis Breathing:** Hover thickens the type from thin to ultra-black (`wght: 200 -> 900`) over `var(--motion-state)` from [motion-timing-engines.md](../ui-motion-interaction/references/motion-timing-engines.md). `wght` changes advance widths, so this relayouts the line on every frame and pushes neighbouring words: prefer the width-neutral `GRAD` axis (as in the implementation notes below), or reserve the widest state's inline size (a fixed-width box or an invisible bold copy stacked in the same grid cell) before animating `wght`.
- Under `prefers-reduced-motion: reduce`, freeze all infinite ticker animations immediately, displaying static horizontal typographic lists.

---

## 🛠️ Implementation Notes

```html
<section class="marquee" aria-labelledby="marquee-title" data-playing>
  <h2 id="marquee-title" class="visually-hidden">Drop schedule</h2>
  <button class="marquee__toggle" type="button" aria-pressed="false">Pause</button>
  <div class="marquee__viewport">
    <div class="marquee__track">
      <ul class="marquee__content">
        <li>Drop 07 · Friday 18:00</li><li>Restock · Sizes S–XL</li><li>Free returns</li>
      </ul>
      <ul class="marquee__content" aria-hidden="true" inert>
        <li>Drop 07 · Friday 18:00</li><li>Restock · Sizes S–XL</li><li>Free returns</li>
      </ul>
    </div>
  </div>
</section>
```

```css
:root {
  --tk-bg: #0a0a0a;
  --tk-fg: #ffffff;
  --tk-accent: #ffe600;
  --tk-font-mono: 'Space Mono', monospace;
  --tk-gap: 3rem;
}
.marquee {
  background: var(--tk-accent);
  color: #000000;
  font-family: var(--tk-font-mono);
  font-weight: 700;
  text-transform: uppercase;
}
.marquee__viewport { overflow: hidden; }
.marquee__track {
  display: flex;
  inline-size: max-content;                 /* = 2 × one content copy */
  animation: tk-marquee 20s linear infinite;
}
.marquee__content {
  display: flex;
  flex-shrink: 0;
  gap: var(--tk-gap);
  padding-inline-end: var(--tk-gap);        /* seam gap equals the inner gap */
  margin: 0;
  list-style: none;
}
.marquee:not([data-playing]) .marquee__track,
.marquee:hover .marquee__track,
.marquee:focus-within .marquee__track { animation-play-state: paused; }
@keyframes tk-marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
@media (prefers-reduced-motion: reduce) {
  .marquee__track { animation: none; inline-size: auto; }
  .marquee__content { flex-wrap: wrap; flex-shrink: 1; }
  .marquee__content[aria-hidden="true"] { display: none; }
  .marquee__toggle { display: none; }
}
```

```js
const root = document.querySelector('.marquee');
const toggle = root.querySelector('.marquee__toggle');
toggle.addEventListener('click', () => {
  const paused = toggle.getAttribute('aria-pressed') !== 'true';
  toggle.setAttribute('aria-pressed', String(paused));
  root.toggleAttribute('data-playing', !paused);
});

// Fill: repeat whole item sets until one copy is at least as wide as the viewport,
// so every seam is the same inner gap, then rebuild the clone and derive the duration.
const PX_PER_SECOND = 80;                   // constant reading speed at every width
const viewport = root.querySelector('.marquee__viewport');
const track = root.querySelector('.marquee__track');
const [copy, clone] = track.children;
const originals = [...copy.children];
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
function fill() {
  copy.replaceChildren(...originals);
  const setWidth = copy.getBoundingClientRect().width;
  if (!reduce.matches && setWidth > 0) {
    const repeats = Math.ceil(viewport.clientWidth / setWidth) - 1;
    for (let r = 0; r < repeats; r++) {
      for (const li of originals) {
        const extra = li.cloneNode(true);
        extra.setAttribute('aria-hidden', 'true');   // the list is read once
        extra.inert = true;
        copy.append(extra);
      }
    }
  }
  clone.replaceChildren(...[...copy.children].map((n) => n.cloneNode(true)));
  const copyWidth = copy.getBoundingClientRect().width;
  if (copyWidth > 0) track.style.animationDuration = `${copyWidth / PX_PER_SECOND}s`;
}
new ResizeObserver(fill).observe(viewport);  // runs once on observe, then on resize
document.fonts.ready.then(fill);             // real font metrics change the set width
reduce.addEventListener('change', fill);
```

- **Seamless loop math:** duplicate the content once, so the track is exactly 2× one copy. Translating the track from `0` to `-50%` moves it by one copy width; at the end of each cycle the clone sits exactly where the original started, so the jump back to `0` is invisible. The seam stays invisible only if the gap after the last item equals the inner gap (hence `padding-inline-end` instead of a track-level `gap`) and each copy is at least as wide as the viewport. Never stretch a short copy to the viewport (`min-inline-size: 100vw`): the stretched copy leaves blank space before its padding, so the seam gap grows wider than the inner gap. Repeat whole item sets inside the copy instead (the `fill()` script, or the template when the width is known), marking repeats `aria-hidden` and `inert` so the list is announced once. Keep the speed constant across widths by deriving duration from copy width (`duration = copyWidth / pxPerSecond`); the CSS `20s` is only the no-script default.
- **Clone semantics:** the duplicate is presentation only. It gets `aria-hidden="true"` so it is not read twice, and `inert` so links inside it are neither focusable nor clickable; `aria-hidden` alone leaves hidden focusable links in the tab order.
- **Pause contract:** the visible `Pause` toggle (`aria-pressed`) is the WCAG 2.2.2 mechanism; hover and focus pause supplement it. Keep the button outside the moving track and size it to the target-size minimum in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- **Split headlines:** follow the accessible-text contract in [text-effect-recipes.md](../ui-motion-interaction/references/text-effect-recipes.md): one visually-hidden full copy plus `aria-hidden` fragments, never `aria-label` on a generic `span` or `div`.
- Avoid animating `letter-spacing` directly as it causes heavy browser reflows; animate `transform` or use the variable-font `GRAD` (grade) axis which is reflow-free.

---

## ♿ Accessibility

- **WCAG 2.2.2 (Pause, Stop, Hide):** Any scrolling text track that moves automatically and lasts more than 5 seconds MUST provide a visible, operable pause/play control bound to playback state. Hover/focus pause can supplement this control; it does not satisfy the criterion on its own. Level, scope and testing live in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- **Duplicate Track:** The seamless-loop clone carries `aria-hidden="true"` and `inert`, so its content is neither announced twice nor reachable by keyboard.
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
## Appearance and Interaction Verification

Define a wrapping or scrollable static ticker fallback with all content reachable; size display type to its owner at font-load, hover-axis and localization extremes; provide a persistent operable pause control rather than treating hover/focus alone as the full pause contract.
