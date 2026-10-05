---
name: "ui-style-cassette-futurism"
description: "Provides the cassette futurism and analog sci-fi UI style: 1970s-1980s computer interfaces, cathode phosphor screens, tactile rocker switches, magnetic tape motifs and industrial beige equipment. Use when designing retro sci-fi games, hardware emulators or nostalgic brand surfaces."
---

# UI Style: Cassette Futurism & Analog Sci-Fi

A retrofuture subgenre capturing the aesthetic of late 1970s through 1980s consumer electronics and analog computer terminals (exemplified by Alien, Blade Runner, WarGames, and early IBM/DEC mainframes). Characterized by phosphor screens, mechanical keys, magnetic tape data, and heavy industrial styling.

---

## 🧭 When to Activate

- Sci-fi games, audio software, retro synthesizer emulators, hardware documentation, and narrative experiences.
- Simulating functional physical machinery with CRT monitors and mechanical toggle switches.

---

## 🎨 Visual DNA

- **Palette:** Industrial beige (`#E6DEC8`), phosphor green (`#33FF33`), amber CRT (`#FFB000`), deep chassis slate (`#2B303A`), and caution orange (`#FF6700`).
- **Type:** Segmented LED digits, cathode CRT vector type, OCR-A, VT323, and classic monospaced computer fonts.
- **Hardware details:** Chunky rocker switches, push buttons with colored LED status lamps, cassette reels, and printed serial numbers.
- **Effects:** Subtle curved screen vignette, faint scanlines, and momentary phosphor afterglow.

---

## 🛠️ Implementation Notes

```css
.crt-monitor {
  background: #0f1a0f;
  color: #33ff33;
  text-shadow: 0 0 5px rgba(51, 255, 51, 0.7);
  border: 12px solid #e6dec8;
  border-radius: 20px;
  font-family: 'VT323', monospace;
}
```

---

## ♿ Accessibility

- Green or amber text on deep backgrounds must maintain at least 4.5:1 contrast ratio.
- Keep CRT scanlines and flicker subtle, and disable them automatically when `prefers-reduced-motion: reduce` is active.
