---
name: "ui-style-web-brutalism"
description: "Provides the complete classic and data-dense web brutalism style (2014-present): raw HTML document structure, default browser styling, unadorned links, high-density financial terminal grids, zero padding waste and tabular streams. Covers Pascal Deville's movement naming, Bloomberg Terminal data density, Low-tech Magazine performance and accessibility. Use when building raw anti-corporate statements, financial consoles or performance-critical text sites."
---

# UI Style: Web Brutalism & Data-Dense Console

The raw, unfiltered truth of the web medium: unadorned HTML document structures, default browser styling, exposed hyperlinks, and mission-critical data density. Unifies the classic anti-design web brutalism movement (Pascal Deville, brutalistwebsites.com) with the high-throughput tabular density of financial terminals (Bloomberg, Reuters). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Art, culture, zines, and activist platforms making deliberate anti-corporate statements.
- Financial trading desks, cryptocurrency orderbooks, infrastructure observability dashboards, and network operations centers (NOC).
- Performance-critical, low-bandwidth text applications and solar-powered websites (Low←Tech Magazine).

---

## 🕰️ Definition and Timeline

- **Architectural Roots:** Architectural New Brutalism (Reyner Banham, 1955; Alison and Peter Smithson; Le Corbusier's *béton brut*). Honesty of materials and structural unpretentiousness.
- **Web Brutalism (2014–2019):** Named and curated by Pascal Deville (*brutalistwebsites.com*). Reaction against glossy, frivolous corporate templates. Canonical adopters: Balenciaga, Bloomberg's investigative features, Cards Against Humanity, Low←Tech Magazine.
- **Data-Dense Terminal Strand (1982–present):** Michael Bloomberg introduced the Bloomberg Terminal in 1982. Its dense amber-and-green tabular matrix set the global standard for rapid data triage where whitespace is considered an operational hazard.
- **Difference from neighbors:** Unlike [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), which is playful, colorful, and heavily styled with cartoon drop-shadows, Web Brutalism embraces structural rawness, default HTML elements, and pure data throughput.

---

## 🎨 Visual DNA

- **Typography:** System monospaced and default serif/sans-serif fonts (Times New Roman, Courier, JetBrains Mono, Consolas) rendered with zero webfont bloat.
- **Color Palette:**
  - *Classic Raw Web:* Pure black on pure white, native underlined blue hyperlinks (`#0000EE`), visited purple (`#551A8B`).
  - *Terminal Console:* Pitch black (`#0C0D0E`), terminal amber (`#FF9E00`), trading green (`#00E676`), and alert red (`#FF1744`).
- **Layout & Structure:** Unstyled or hairline `<table>` grids, 2px cell paddings, zero wasted margins, `<hr>` dividers, and visible document scaffolding.
- **Imagery & Media:** Unedited raw-resolution photos, 1-bit dithered bitmaps, and inline SVG sparklines.

---

## 🖱️ Interaction and Motion

- **Zero Decorative Transitions:** Instantaneous state changes (`transition: none`); zero playful bounce or skeleton loaders.
- **Keyboard-First Controls:** Direct keyboard shortcuts indicated with brackets (`[B]uy`, `[S]ell`, `[Esc]`).
- **Data Refresh:** Telemetry cells update instantly, with single-frame background flashes for altered values.

---

## 🛠️ Implementation Notes

```css
:root {
  --wb-bg: #0c0d0e;
  --wb-fg: #e1e4e8;
  --wb-amber: #ff9e00;
  --wb-green: #00e676;
  --wb-border: #282e38;
  --wb-font: 'JetBrains Mono', monospace;
}
body { background: var(--wb-bg); color: var(--wb-fg); font-family: var(--wb-font); font-size: 13px; }
table.data-dense {
  width: 100%;
  border-collapse: collapse;
}
table.data-dense th, table.data-dense td {
  border: 1px solid var(--wb-border);
  padding: 4px 8px;
  text-align: left;
  font-variant-numeric: tabular-nums;
}
a.raw-link {
  color: #00f0ff;
  text-decoration: underline;
}
```

---

## ♿ Accessibility

- **Optimal Information Contrast:** Pure terminal amber and neon green against black easily exceed 8:1 contrast ratios.
- **Live Stream Accessibility:** Dynamic telemetry streams must use `aria-live="polite"` regions and positive/negative text markers (`+`, `-`) rather than relying solely on green/red color (WCAG 1.4.1).
- **Legibility:** Keep line-height comfortable (`1.3` to `1.4`) to prevent dense tabular columns from causing visual fatigue.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Trading orderbooks, server telemetry, developer documentation, performance-constrained networks, and underground cultural zines.
- **Avoid:** Friendly consumer onboarding, family-focused products, and luxury beauty brands where warmth and emotional comfort are required.

---

## 📚 Sources

- Pascal Deville, *Brutalist Websites Archive*, 2014–2022 — http://brutalistwebsites.com/
- Michael Bloomberg, *Bloomberg by Bloomberg*, John Wiley & Sons, 1997.
- Low←Tech Magazine, *How to Build a Low-tech Website*, 2018 — http://solar.lowtechmagazine.com
- Reyner Banham, "The New Brutalism", *Architectural Review*, 1955.
- W3C, *Web Content Accessibility Guidelines 2.2* — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling raw styles: [ui-style-brutalist-monochrome](../ui-style-brutalist-monochrome/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md).
