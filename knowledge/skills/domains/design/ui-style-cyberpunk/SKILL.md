---
name: "ui-style-cyberpunk"
description: "Provides the complete cyberpunk and futuristic sci-fi HUD UI style (1980s-present): neon-noir dystopia, military FUI panels, chamfered corners, scanlines, telemetry loops, chromatic aberration and cybernetic aesthetics. Covers postcyberpunk and cyberprep variants, Territory Studio lineage, CSS clip-path chamfers and photosensitivity accessibility. Use when designing game, esports, crypto, security or sci-fi entertainment interfaces."
---

# UI Style: Cyberpunk & Sci-Fi Tactical HUD

"High tech, low life" translated to the web: neon light against wet darkness, dense signage, degraded infrastructure, and tactical instrument HUD panels ("Fantasy User Interfaces"). Merges atmospheric street-level dystopia with cinematic FUI instrumentation (Alien, Blade Runner 2049, Cyberpunk 2077). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Games, esports streaming hubs, crypto/web3 platforms, developer-tool microsites, cybersecurity dashboards, and sci-fi entertainment portals.
- Tech brands deliberately playing with hacking aesthetics, dystopian irony, and terminal telemetry.
- Designing tactical telemetry panels, radar sweeps, reticle overlays, and chamfered HUD containers.

---

## 🕰️ Definition and Timeline

- **Literary & Cinematic Canon:** Coined by Bruce Bethke in 1983; popularized by Gardner Dozois. Canon: *Blade Runner* (1982, Ridley Scott, Syd Mead), *Neuromancer* (William Gibson, 1984), *Akira* (1988), and *Ghost in the Shell* (1995).
- **Cinematic FUI Strand (HUD):** Pioneered by *Alien* (1979) and *Minority Report* (2002); industrialized by Territory Studio (*The Martian* 2015, *Blade Runner 2049* 2017). Solidified as a web aesthetic following *Cyberpunk 2077* (CD Projekt Red, 2020).
- **Variants:**
  - *Dystopian Core:* Neon cyan, hot magenta, and acid yellow against deep black rainy alleys.
  - *Postcyberpunk:* Advanced technology and cyberware in functional, daylight civic societies.
  - *Cyberprep:* Clean white and chrome utopian aesthetic where augmentation serves leisure.
  - *Tactical FUI / HUD:* Angular instrument readouts, real-time telemetry, calibration brackets, and targeting reticles.
- **Difference from neighbors:** Unlike [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), which is nostalgic 1980s pastel-retro with palm trees, Cyberpunk is gritty, aggressive, surveillance-heavy, and technologically complex.

---

## 🎨 Visual DNA

- **Palette:** Near-black obsidian canvases (`#05060A`, `#07060F`), acid yellow (`#F5E642`, `#FCEE0A`), electric cyan (`#00F0FF`), hot magenta (`#FF003C`), and hazard warning orange (`#FF5500`).
- **Typography:** Techno-industrial sans-serifs (Rajdhani, Orbitron, Share Tech Mono) paired with dense monospaced readouts (JetBrains Mono, Fira Code).
- **Shapes & Panels:** 45-degree chamfered card corners (`clip-path: polygon(...)`), 1px luminescent border hairlines, corner calibration brackets, and circular gauges.
- **Texture & Lighting:** Volumetric neon bloom (`filter: drop-shadow()`), horizontal CRT scanlines (`repeating-linear-gradient`), chromatic aberration, and digital glitch artifacts.
- **Iconography:** Reticles, telemetry coordinate axes, barcode blocks, warning diagonal hazard stripes, and technical circuit glyphs.

---

## 🖱️ Interaction and Motion

- **Decryption Reveals:** Text streams decode into view using rapid cryptographic character scrambles.
- **Telemetry Pulses:** Corner indicators and status badges pulse slowly with live operational rhythm.
- **Glitch Hover:** Buttons glitch with 100–150ms chromatic horizontal slice offsets when hovered.
- Under `prefers-reduced-motion: reduce`, disable all glitch slicing, continuous scanline sweeps, and neon flicker, keeping static illuminated HUD containers.

---

## 🛠️ Implementation Notes

```css
:root {
  --cp-bg: #07060f;
  --cp-surface: #0e0d1a;
  --cp-cyan: #00f0ff;
  --cp-yellow: #fcee0a;
  --cp-magenta: #ff003c;
  --cp-text: #e9e6ff;
}
body { background-color: var(--cp-bg); color: var(--cp-text); }
.hud-panel {
  background: var(--cp-surface);
  border: 1px solid rgba(0, 240, 255, 0.4);
  clip-path: polygon(0 0, calc(100% - 15px) 0, 100% 15px, 100% 100%, 15px 100%, 0 calc(100% - 15px));
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
}
.scanlines::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.3) 0 1px, transparent 1px 3px);
}
.hud-btn {
  background: var(--cp-yellow);
  color: #000000;
  font-family: 'Rajdhani', sans-serif;
  font-weight: 700;
  clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
  border: none;
  padding: 10px 24px;
}
.hud-btn:hover {
  background: var(--cp-cyan);
  box-shadow: 0 0 12px var(--cp-cyan);
}
```

---

## ♿ Accessibility

- **Contrast Safety:** Ensure neon accents on dark backgrounds maintain WCAG 1.4.3 (4.5:1). Secondary gray text is the most common failure point—ensure it stays above `#A1A1A6`.
- **Photosensitivity Safeguards (WCAG 2.3.1):** Never flash neon borders or glitch transitions more than three times per second. Flicker animations must be subtle and slow.
- **Overlay Legibility:** Keep scanline and noise pseudo-elements non-interactive (`pointer-events: none`) and subtle enough that body text remains sharp.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Video games, esports platforms, cyberpunk storytelling, web3 dApps, security operations portals, and promotional tech drops.
- **Caution:** Commercial e-commerce (confine HUD styling to badges and featured cards, keeping checkout completely standard).
- **Avoid:** Government citizen portals, hospitals, financial accounting suites, and reading applications where decorative noise taxes attention.

---

## 📚 Sources

- Territory Studio, "Blade Runner 2049 UI Design Case Study", 2018.
- Nathan Shedroff & Christopher Noessel, *Make It So: Interaction Design Lessons from Science Fiction*, Rosenfeld Media, 2012.
- William Gibson, *Neuromancer*, Ace Books, 1984.
- W3C, *Web Content Accessibility Guidelines 2.2* (1.4.3, 2.3.1, 2.2.2) — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling sci-fi styles: [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md), [ui-style-vaporwave-synthwave](../ui-style-vaporwave-synthwave/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md).
