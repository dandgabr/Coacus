---
name: "ui-style-brutalist-data-dense"
description: "Provides the brutalist data-dense and financial terminal UI style: zero wasted pixels, compact tabular streams, inline sparklines, amber/green telemetry and maximum information efficiency. Use when building financial trading desks, monitoring consoles or developer observability dashboards."
---

# UI Style: Brutalist Data-Dense & Terminal Console

Inspired by financial trading consoles (Bloomberg Terminal, Reuters Eikon) and mission-critical NOC/SRE monitoring boards. Rejects decorative padding, expansive whitespace, and slow transitions in favor of extreme data throughput, compact cell matrices, and lightning-fast information triage. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Trading desks, cryptocurrency orderbooks, infrastructure observability dashboards, network telemetry boards, and logistics operations.
- Power users needing maximum information density per square millimeter of screen real estate.
- Building tools where seeing 100 data points simultaneously without scrolling saves critical minutes.

---

## 🕰️ Definition and Timeline

- **Origins:** Michael Bloomberg introduced the Bloomberg Terminal in December 1982. Its dense amber-and-green tabular matrix set the global standard for high-frequency finance.
- **Philosophy:** Zero decorative friction. Every pixel must convey actionable telemetry. Whitespace is considered an operational hazard when it pushes critical alarms off-screen.
- **Difference from neighbors:** Unlike [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), which is sequential CLI command-line output, Brutalist Data-Dense is a multi-column, live tabular grid matrix with synchronized inline graphs. Unlike [ui-style-linear-saas](../ui-style-linear-saas/SKILL.md), it features zero ambient glow, zero curved pill badges, and zero padding waste.

---

## 🎨 Visual DNA

- **Palette:** Pitch console black (`#0C0D0E`), terminal amber (`#FF9E00`), trading profit green (`#00E676`), loss/alert red (`#FF1744`), and steel gray metrics (`#8A919E`).
- **Layout & Structure:** Compact tabular grids, line-height `1.2`, 2px cell paddings, zero margin gaps, and inline sparkline trend graphs.
- **Type:** Tabular monospaced and fixed-pitch sans-serif fonts (JetBrains Mono, Roboto Mono, Fira Code, Consolas) with tabular numeral features enabled.
- **Borders & Dividers:** 1px solid hairline slate dividers (`#282E38`), sharp 0px radius corners.

---

## 🖱️ Interaction and Motion

- Instantaneous data refresh: data cells update in real time with momentary single-frame green/red background flashes.
- Keyboard-first: every action is bindable to keyboard hotkeys with visible shortcut bracket cues (`[B]uy`, `[S]ell`).
- Zero easing transitions: state changes happen immediately (`transition: none`).

---

## 🛠️ Implementation Notes

```css
#stage[data-style="brutalist-data-dense"] {
  --bg: #0c0d0e;
  --surface: #121417;
  --fg: #e1e4e8;
  --muted: #768390;
  --accent: #ff9e00;
  --accent-fg: #000000;
  --border: #282e38;
  --radius: 0;
  --gap: 8px;
  --pad: 10px;
  --font-body: 'JetBrains Mono', 'Roboto Mono', monospace;
  --font-display: 'JetBrains Mono', monospace;
  font-size: 13px;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **High-contrast telemetry:** Amber and green metrics against pure black easily exceed 8:1 contrast ratios.
- **Accessible live streams:** Streaming telemetry cells must utilize screen-reader accessible `aria-live="polite"` regions and distinct positive/negative prefix symbols (`+`, `-`) rather than color alone (WCAG 1.4.1).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Fintech trading desks, network operations centers, server observability dashboards, and logistics dispatchers.
- **Avoid:** Consumer marketing landing pages, storytelling blogs, and luxury brand showcases.

---

## 📚 Sources

- Michael Bloomberg, *Bloomberg by Bloomberg*, John Wiley & Sons, 1997.
- Edward Tufte, *Envisioning Information*, Graphics Press, 1990.
- SRE Observability Guidelines, *High-Density Telemetry Design*, Google Cloud, 2021.

---

## 🔗 Integration with Other Skills

- Sibling technical styles: [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-tactile-brutalism](../ui-style-tactile-brutalism/SKILL.md), [ui-style-blueprint-cad-schematic](../ui-style-blueprint-cad-schematic/SKILL.md).
