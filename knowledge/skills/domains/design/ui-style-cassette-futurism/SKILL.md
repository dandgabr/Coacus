---
name: "ui-style-cassette-futurism"
description: "Provides the cassette futurism and analog sci-fi UI style (1975-1985 retrofuture): phosphor CRT monitors, mechanical rocker switches, magnetic tape data reels, caution-striped bezels and industrial beige equipment. Use when designing retro sci-fi games, audio software or nostalgic hardware emulators."
---

# UI Style: Cassette Futurism & Analog Sci-Fi

A retrofuture subgenre capturing the aesthetic of late 1970s through early 1980s consumer electronics and analog computer terminals (exemplified by *Alien*, *Blade Runner*, *WarGames*, early IBM mainframes, and Hewlett-Packard laboratory instruments). Characterized by curved phosphor CRT monitors, mechanical rocker switches, magnetic tape reels, and heavy industrial beige casings. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Sci-fi games, synthesizer and audio software, hardware documentation, retro computing emulators, and narrative digital experiences.
- Simulating functional physical machinery with CRT monitors and mechanical toggle switches.
- Building immersive interactive dashboards celebrating tactile analog technology.

---

## 🕰️ Definition and Timeline

- **Era:** Late 1970s to mid-1980s (roughly 1977 to 1986). The transition period from discrete electronics and analog magnetic tape to the first generation of microcomputers.
- **Key aesthetic landmarks:** Ron Cobb's industrial Ron Cobb Semiotic Standard design for *Alien* (1979); Syd Mead's vehicle and console designs for *Blade Runner* (1982); the microchip boom (Commodore PET, Apple II, IBM 5150).
- **Difference from neighbors:** Unlike [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), which is neon-slick, ultra-dense, and holographic, Cassette Futurism is chunky, beige, analog, and mechanical. Unlike [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), which is pure flat text, Cassette Futurism emphasizes the physical industrial enclosure around the screen.

---

## 🎨 Visual DNA

- **Palette:** Industrial chassis beige (`#D8CEB9` or `#C4B99F`), phosphor green (`#33FF33`), amber CRT (`#FFB000`), deep chassis slate (`#1C2321`), caution hazard yellow/orange (`#FF9F1C`), and LED indicator red (`#E63946`).
- **Type:** Cathode CRT monospaced type (VT323, Modern DOS, IBM Plex Mono), segmented LED numbers, and industrial labeling grotesques.
- **Hardware Details:** Chunky bevelled monitor bezels, ventilation grilles, push buttons with colored acrylic lenses, screw heads, and serial number nameplates.
- **Screen Effects:** Subtle curved screen vignette, faint scanlines, phosphor glow (`text-shadow: 0 0 5px rgba(51, 255, 51, 0.7)`), and momentary afterglow.

---

## 🖱️ Interaction and Motion

- Mechanical key click: buttons exhibit distinct 2-stage tactile depression (`transform: translateY(2px)` with shadow collapse).
- Cathode warm-up: initial page load features a momentary phosphor scanline sweep (under 0.8s).
- Under `prefers-reduced-motion: reduce`, disable scanline drift, flicker, and screen curvature animations.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="cassette-futurism"] {
  --bg: #101412;
  --surface: #0a0d0b;
  --fg: #33ff33;
  --muted: #1e824c;
  --accent: #33ff33;
  --accent-fg: #000000;
  --border: #d8ceb9;
  --radius: 8px;
  --font-body: 'VT323', monospace;
  --font-display: 'VT323', monospace;
}
```

---

## ♿ Accessibility

- **Contrast compliance:** High-luminance green (`#33FF33`) or amber (`#FFB000`) against black achieves high contrast (> 8:1).
- **Readability:** VT323 and pixel fonts can be difficult to read at small sizes; ensure minimum `font-size: 18px` for monospaced CRT type.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Game menus, narrative sci-fi websites, audio DAW plugins, hardware simulators, and developer CLI tools.
- **Avoid:** Corporate portals, long-form reading applications, and medical interfaces.

---

## 📚 Sources

- Ron Cobb, *The Alien Portfolio: Industrial Design and Semiotic Standards*, 1979.
- Syd Mead, *Oblagon: Concepts of Car Style*, 1985.
- Smithsonian National Museum of American History, *Computing in the Late 20th Century*, 2019.

---

## 🔗 Integration with Other Skills

- Sibling sci-fi and retro styles: [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-dieselpunk](../ui-style-dieselpunk/SKILL.md), [ui-style-atompunk](../ui-style-atompunk/SKILL.md).
