---
name: "ui-style-kinetic-marquee-ticker"
description: "Provides the kinetic marquee and high-density ticker UI style: continuous horizontal and vertical text ribbons, stock exchange telemetry density, bold monospaced metrics and relentless informational momentum. Use when designing streetwear, financial fintech or live event surfaces."
---

# UI Style: Kinetic Marquee & High-Density Ticker

Driven by contemporary streetwear (Off-White, A-COLD-WALL*), financial ticker tapes, and digital festival line-ups. Features endless looping text ribbons, high-density telemetry streams, and relentless visual kinetic rhythm. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Streetwear drops, festival line-ups, live event trackers, financial telemetry platforms, and breaking news portals.
- Infusing dynamic energy, real-time urgency, and dense informational flow.
- Breaking static layout monotony with continuous horizontal typographic ribbons.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in the physical stock ticker tapes of the late 19th century and neon Times Square news zippers (1928), entering digital design through streetwear typography (Virgil Abloh, 2013–2019) and Awwwards brutalist portfolios.
- **Philosophy:** Information as physical kinetic flow. Rejecting static page stops in favor of a relentless stream of real-time momentum and high-density telemetry.
- **Difference from neighbors:** Unlike [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md), which focuses on expressive letterform animations on scroll, Kinetic Marquee Ticker specifically focuses on infinite looped ribbons, high-speed telemetry streams, and stock exchange data density.

---

## 🎨 Visual DNA

- **Palette:** High-voltage safety yellow (`#FFE600`), warning orange (`#FF5500`), electric cyan (`#00F0FF`), pitch black (`#0A0A0A`), and crisp white (`#FFFFFF`).
- **Type:** Ultra-wide condensed grotesques, heavy all-caps display fonts, and monospaced tabular metrics (Space Mono, Monument Extended, Druk Wide).
- **Ribbons & Tracks:** Endless animated horizontal and vertical banners running across page margins at variable speeds.
- **Dividers:** Barcodes, coordinate tags, crosshairs, and live blinking indicator dots.
- **Depth:** Sharp hard offset black borders and zero-radius boxes.

---

## 🖱️ Interaction and Motion

- Infinite marquee loop: continuous smooth linear ticker scrolling (`animation: marquee 15s linear infinite`).
- Hover pause: hovering over a ticker pauses its motion so users can read specific updates.
- Under `prefers-reduced-motion: reduce`, immediately stop all automatic ticker scrolling (WCAG 2.2.2 compliance).

---

## 🛠️ Implementation Notes

```css
#stage[data-style="kinetic-marquee-ticker"] {
  --bg: #0a0a0a;
  --surface: #141414;
  --fg: #ffffff;
  --muted: #888888;
  --accent: #ffe600;
  --accent-fg: #000000;
  --border: #ffe600;
  --radius: 0;
  --shadow: 4px 4px 0 0 #ffe600;
  --font-body: 'Space Mono', monospace;
  --font-display: 'Space Mono', monospace;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **WCAG 2.2.2 Pause, Stop, Hide:** Any scrolling ticker that starts automatically and lasts more than five seconds must have a pause control or pause on mouse hover and keyboard focus.
- **High contrast:** Warning yellow on black provides superior contrast (> 12:1).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Product drops, music festivals, live telemetry consoles, financial trading hubs, and streetwear retail.
- **Avoid:** Calm reading applications, accessibility-focused government portals, and legal contracts.

---

## 📚 Sources

- Virgil Abloh, *Figures of Speech*, Prestel, 2019.
- W3C, *Understanding Success Criterion 2.2.2: Pause, Stop, Hide*, 2023.
- Awwwards Annual Trends in Web Design, *The Kinetic Web*, 2022.

---

## 🔗 Integration with Other Skills

- Movement relatives: [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md), [ui-style-brutalist-data-dense](../ui-style-brutalist-data-dense/SKILL.md).
