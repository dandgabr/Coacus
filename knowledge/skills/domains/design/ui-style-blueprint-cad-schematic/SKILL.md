---
name: "ui-style-blueprint-cad-schematic"
description: "Provides the architectural blueprint and CAD schematic UI style: engineering cyan lines, coordinate crosshairs, dimension tick marks, monospaced drafting notes and technical grid backing. Use when building engineering tools, architecture portfolios or technical hardware docs."
---

# UI Style: Blueprint & CAD Technical Schematic

Derived from traditional cyanotype architectural blueprints (John Herschel, 1842) and modern CAD (Computer-Aided Design) drafting software (AutoCAD, MicroStation). Emphasizes mathematical precision, dimensioning arrows, coordinate crosshairs, grid callouts, and technical drafting aesthetics. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Developer tools, architectural portfolios, robotics hardware telemetry, infrastructure docs, and industrial manufacturing sites.
- Communicating rigorous precision, engineering authority, and transparent mechanics.
- Replacing generic dark SaaS themes with an authentic technical drafting workstation look.

---

## 🕰️ Definition and Timeline

- **Origins:** Invented in 1842 via the cyanotype contact printing process; dominated architectural and engineering drafting for over a century until computerized CAD drafting emerged in the 1980s.
- **Philosophy:** The aesthetics of unvarnished technical truth. Showing the measurements, guidelines, tolerances, and hidden coordinates that make a structure stand.
- **Difference from neighbors:** Unlike [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), which is pure text on a CRT, Blueprint is graphical, vector-drawn, dimension-annotated, and architectural. Unlike [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), which is aggressive, weaponized, and neon, Blueprint is calm, methodical, and constructive.

---

## 🎨 Visual DNA

- **Palette:** Blueprint cyan (`#00F0FF`), drafting deep navy (`#0B1D3A`), precision white (`#FFFFFF`), grid blue (`#1E3A5F`), and revision red (`#FF3B30`).
- **Type:** Architectural drafting fonts, monospaced consoles (Consolas, Space Mono, Technical Drafting Sans).
- **Patterns & Details:** Orthogonal dimension ticks, angle callouts, coordinate crosshairs, millimeter grid paper backgrounds, and title block approval stamps.
- **Borders & Dividers:** 1px solid cyan borders with technical coordinate corner stamps.

---

## 🖱️ Interaction and Motion

- Caliper tracking: hover reveals live dimension callouts or coordinate offsets.
- Drafting reveal: lines draw in with vector stroke animations (`stroke-dashoffset`).
- Under `prefers-reduced-motion: reduce`, disable vector line-draw transitions.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="blueprint-cad-schematic"] {
  --bg: #0b1d3a;
  --surface: rgba(11, 29, 58, 0.85);
  --fg: #00f0ff;
  --muted: #4a7ab5;
  --accent: #00f0ff;
  --accent-fg: #0b1d3a;
  --border: #00f0ff;
  --radius: 0;
  --font-body: 'Space Mono', 'Consolas', monospace;
  --font-display: 'Space Mono', monospace;
  background-color: var(--bg);
  background-image: linear-gradient(rgba(0, 240, 255, 0.15) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 240, 255, 0.15) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

---

## ♿ Accessibility

- **Contrast compliance:** Luminous cyan against deep navy provides excellent contrast (> 9:1). Ensure fine grid lines remain at low opacity (`0.15`) so they do not interfere with text readability.
- **Typography legibility:** Monospaced type must maintain adequate line-height (`1.6`) for comfortable reading.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Engineering platforms, architecture studios, hardware telemetry consoles, and developer tool docs.
- **Avoid:** Fashion lifestyle stores, beauty brands, and casual social apps.

---

## 📚 Sources

- John Herschel, *On the Action of the Rays of the Solar Spectrum on Vegetable Colours*, 1842.
- Francis D. K. Ching, *Architectural Graphics*, John Wiley & Sons, 2015.
- AutoCAD Historical Reference Manual, *The CAD User Interface*, Autodesk, 1986.

---

## 🔗 Integration with Other Skills

- Sibling technical styles: [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-tactile-brutalism](../ui-style-tactile-brutalism/SKILL.md), [ui-style-brutalist-data-dense](../ui-style-brutalist-data-dense/SKILL.md).
