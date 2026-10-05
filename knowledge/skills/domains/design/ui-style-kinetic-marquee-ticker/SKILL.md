---
name: "ui-style-kinetic-marquee-ticker"
description: "Provides the kinetic marquee and high-density ticker UI style: continuous horizontal and vertical text ribbons, stock exchange density, bold monospaced metrics and relentless informational momentum. Use when designing streetwear, financial fintech or live event surfaces."
---

# UI Style: Kinetic Marquee & High-Density Ticker

Driven by contemporary streetwear (Off-White, A-COLD-WALL*), financial ticker tapes, and festival websites. Features endless looping text ribbons, high-density telemetry streams, and relentless visual kinetic rhythm.

---

## 🧭 When to Activate

- Streetwear drops, festival line-ups, live event trackers, financial telemetry platforms, and breaking news portals.
- Infusing dynamic energy, real-time urgency, and dense informational flow.

---

## 🎨 Visual DNA

- **Palette:** High-voltage safety yellow (`#FFE600`), warning orange (`#FF5500`), electric cyan (`#00F0FF`), pitch black (`#0A0A0A`), and paper white.
- **Type:** Ultra-wide condensed grotesques, heavy all-caps display fonts, and monospaced tabular metrics (Druk Wide, Monument Extended, Space Mono).
- **Ribbons:** Endless animated horizontal and vertical banners running across page margins at variable speeds.
- **Dividers:** Barcodes, coordinate tags, crosshairs, and live blinking indicator dots.

---

## 🛠️ Implementation Notes

```css
.marquee-track {
  display: flex;
  overflow: hidden;
  white-space: nowrap;
  background: #ffe600;
  color: #000;
  font-weight: 900;
  padding: 8px 0;
}
.marquee-content {
  display: flex;
  animation: scroll-left 15s linear infinite;
}
@keyframes scroll-left {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

---

## ♿ Accessibility

- Respect `prefers-reduced-motion: reduce`: pause continuous scrolling ribbons or provide an explicit user play/pause control (WCAG 2.2.2 Pause, Stop, Hide).
