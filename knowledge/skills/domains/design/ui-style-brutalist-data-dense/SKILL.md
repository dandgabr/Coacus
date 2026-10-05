---
name: "ui-style-brutalist-data-dense"
description: "Provides the brutalist data-dense and financial terminal UI style: zero wasted pixels, compact tabular streams, inline sparklines, amber/green telemetry and maximum information efficiency. Use when building financial trading desks, monitoring consoles or developer observability dashboards."
---

# UI Style: Brutalist Data-Dense & Terminal Console

Inspired by financial trading systems (Bloomberg Terminal, Reuters Eikon) and mission-critical NOC consoles. Rejects decorative fluff, expansive padding, and slow transitions in favor of extreme data throughput, compact cell matrices, and lightning-fast information triage.

---

## 🧭 When to Activate

- Trading desks, cryptocurrency orderbooks, infrastructure observability dashboards, and logistics operations hubs.
- Power users needing maximum information density per square millimeter of screen real estate.

---

## 🎨 Visual DNA

- **Palette:** Terminal black (`#0C0D0E`), console amber (`#FF9E00`), trading green (`#00E676`), loss red (`#FF1744`), and steel gray metrics (`#8A919E`).
- **Layout:** Monospaced tabular grids, condensed line-heights, zero-padding data cells, and live inline sparkline trends.
- **Type:** High-legibility tabular figures and fixed-pitch fonts (JetBrains Mono, Roboto Mono, Fira Code).

---

## 🛠️ Implementation Notes

```css
.dense-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  background: #0c0d0e;
  color: #e1e4e8;
}
.dense-table td, .dense-table th {
  padding: 2px 6px;
  border: 1px solid #21262d;
}
```

---

## ♿ Accessibility

- Despite high density, ensure text meets 4.5:1 contrast standards.
- Provide keyboard shortcuts for swift table navigation and screen-reader accessible `aria-live` regions for streaming metrics.
