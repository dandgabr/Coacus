---
name: "ui-style-web-brutalism"
description: "Provides the canonical Web Brutalism & Data-Dense Console UI style (2014-present): raw HTML document structure, native browser styling, unadorned blue hyperlinks (#0000EE), default monospaced typography, Bloomberg Terminal data density, tabular matrix layouts, and zero decorative padding waste. Use when building anti-corporate cultural statements, financial trading orderbooks, infrastructure telemetry consoles, or performance-critical low-tech platforms."
---

# UI Style: Web Brutalism & Data-Dense Console

**Web Brutalism** represents the raw, unvarnished honesty of the web as a computational and document medium. Coined in 2014 by Pascal Deville (*brutalistwebsites.com*), the style strips away frivolous decorative layers, rounded containers, and modern SaaS homogeny in favor of default HTML semantics, raw browser typography (Times New Roman, Courier, system monospace), native underlined hyperlinks, unpadded tabular matrices, and exposed layout scaffolding. In its data-dense technical dialect, Web Brutalism mirrors the high-throughput efficiency of the Bloomberg Terminal, where screen real estate is optimized purely for information density and zero wasted space.

---

## 🧭 When to Activate

- Cultural manifestos, independent art publications, activist platforms, and anti-corporate design statements.
- Financial trading desks, cryptocurrency orderbooks, network operations center (NOC) consoles, and server cluster observability dashboards where spatial padding is an operational liability.
- Performance-critical, low-bandwidth, solar-powered, or offline-first websites (e.g. *Low←Tech Magazine*) requiring sub-50KB total page weight.

---

## 🕰️ Definition, Lineage, and Timeline

- **Architectural Lineage:** Rooted in architectural New Brutalism (Reyner Banham, 1955; Alison and Peter Smithson; Le Corbusier's *béton brut*—raw, unpainted concrete celebrating the unpretentious truth of materials).
- **The Web Brutalism Movement (2014–2019):** Formalized by Pascal Deville with the creation of *brutalistwebsites.com*, curating hundreds of underground web projects reacting against ubiquitous Bootstrap and Flat Design templates. High-profile adopters include Balenciaga, Cards Against Humanity, and Bloomberg's investigative features.
- **The Financial Data-Dense Lineage (1982–Present):** Pioneered by the Bloomberg Terminal (1982) and Reuters trading feeds. Proved that ultra-dense tabular matrices with zero padding, black backgrounds, and amber/green typography maximize rapid decision-making under intense cognitive load.
- **Distinctions from Neighboring Styles:**
  - Unlike **Neo-Brutalism** (playful, pastel, rounded buttons, cartoon offset drop shadows), Web Brutalism is unstyled, serious, sharp, and structural.
  - Unlike **Terminal TUI** (plain ASCII character matrix), Web Brutalism utilizes native HTML web elements (links, forms, tables, frames).
  - Unlike **Brutalist Monochrome** (artistic black-and-white editorial layouts), Web Brutalism embraces native browser link blue (`#0000EE`) and raw browser form controls.
- **Absolute Veto:** Decorative rounded card corners (`border-radius > 0px`), soft drop shadows, and artificial loading skeleton placeholders. Content must render immediately upon arrival.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                WEB BRUTALISM MATRIX                                    │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Raw HTML Manifesto      │ 2. Financial Telemetry Grid│ 3. Sustainable Low-Tech      │
│ • Pure white canvas        │ • Obsidian dark background │ • Dithered 1-bit grayscale   │
│ • Times New Roman / Courier│ • Amber & neon green data  │ • Zero external webfonts     │
│ • Blue (#0000EE) underlines│ • Hairline <table> matrices│ • Solar battery status meter │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palettes:**
  - *Raw Document:* Pure white (`#FFFFFF`) or newsprint cream (`#F4F4F0`), jet black (`#000000`), default link blue (`#0000EE`), and visited purple (`#551A8B`).
  - *Console Terminal:* Obsidian slate (`#0C0D0E`), terminal amber (`#FF9E00`), trading green (`#00E676`), and alert red (`#FF1744`).
- **Scaffolding & Architecture:** Native HTML `<table>`, `<pre>`, `<code>`, and `<hr>` dividers. Border collapse enabled (`border-collapse: collapse;`), 1px solid hairline grids, and 2px to 4px padding.
- **Image Treatment:** Uncompressed raw images or 1-bit Floyd-Steinberg dithered black-and-white bitmaps to eliminate payload weight.

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Zero Artificial Lighting (The Photon Truth):**
   - No simulated 3D bevels, no drop shadows, and no specular gradients. Surfaces are 100% flat emission.
   ```css
   background-color: #ffffff;
   color: #000000;
   border: 1px solid #000000;
   box-shadow: none;
   border-radius: 0;
   ```
2. **Dense Tabular Cell Grid:**
   - Maximum density with tabular numbers and tight vertical rhythm.
   ```css
   border-collapse: collapse;
   font-variant-numeric: tabular-nums;
   line-height: 1.25;
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Document Grounds */
  --wb-bg-light: #FFFFFF;
  --wb-ink-dark: #000000;
  --wb-link-blue: #0000EE;
  --wb-link-visited: #551A8B;

  /* Terminal Console Grounds */
  --wb-bg-terminal: #0C0D0E;
  --wb-surface-terminal: #14171A;
  --wb-amber: #FF9E00;
  --wb-green: #00E676;
  --wb-red: #FF1744;
  --wb-border-hairline: #282E38;

  /* Typography */
  --wb-font-mono: 'Courier New', Courier, ui-monospace, monospace;
  --wb-font-serif: 'Times New Roman', Times, serif;
  --wb-font-sans: Arial, Helvetica, sans-serif;

  /* Structural Geometry */
  --wb-border: 1px solid #000000;
  --wb-border-cell: 1px solid var(--wb-border-hairline);
  --wb-radius: 0px;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Zero-Webfont Principle:** Rely entirely on operating system font stacks (*Times New Roman*, *Courier New*, *Arial*, *ui-monospace*) to achieve sub-millisecond initial render times and zero network requests.
- **Tabular Figures:** Always apply `font-variant-numeric: tabular-nums` to financial data and time metrics to guarantee strict vertical column alignment across rows.
- **Link Styling:** Blue (`#0000EE`), bold, and permanently underlined (`text-decoration: underline; text-underline-offset: 2px;`). Never hide link affordances behind hover states.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Zero Decorative Easing:** State changes occur instantaneously (`transition: none !important`).
- **Keyboard Accelerators:** Actions display their direct keyboard shortcut in brackets (e.g. `[Q]uit`, `[B]uy`, `[R]efresh`).
- **Data Flash Telemetry:** When live cell values update, the cell background briefly flashes white or amber for 100ms before returning to black.
- **Motion Reduction:** Because Web Brutalism naturally avoids animation, it fully conforms to `prefers-reduced-motion` out of the box.

---

## 🧩 Canonical Component Specifications

### 1. High-Density Telemetry Table (`.wb-table`)
A data matrix optimized for rapid scanning with tabular numbers and hairline borders.
```html
<table class="wb-table">
  <thead>
    <tr>
      <th>SYMBOL</th>
      <th>LAST</th>
      <th>CHANGE</th>
      <th>VOLUME</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>US-TREASURY-10Y</td>
      <td>4.218</td>
      <td class="pos">+0.042</td>
      <td>148,220</td>
    </tr>
  </tbody>
</table>
```
```css
.wb-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--wb-font-mono);
  font-size: 13px;
  background: var(--wb-bg-terminal);
  color: #E1E4E8;
}
.wb-table th, .wb-table td {
  border: 1px solid var(--wb-border-hairline);
  padding: 4px 8px;
  text-align: left;
  font-variant-numeric: tabular-nums;
}
.wb-table th {
  background: var(--wb-surface-terminal);
  color: var(--wb-amber);
  font-weight: 700;
}
.wb-table td.pos { color: var(--wb-green); }
.wb-table td.neg { color: var(--wb-red); }
```

### 2. Bracketed Command Button (`.wb-btn`)
An unpadded, rectangular action trigger resembling raw terminal execution.
```css
.wb-btn {
  background: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  font-family: var(--wb-font-mono);
  font-size: 13px;
  font-weight: bold;
  padding: 4px 10px;
  cursor: pointer;
  border-radius: 0;
}
.wb-btn:hover {
  background: #FFFFFF;
  color: #000000;
}
.wb-btn:focus-visible {
  outline: 2px solid var(--wb-link-blue);
  outline-offset: 2px;
}
```

### 3. Raw Hyperlink Box (`.wb-link-box`)
A structural list of underlined hyperlinks separated by vertical pipes (`|`).

### 4. Telemetry Terminal Feed (`.wb-feed`)
A streaming terminal log component rendering chronological event strings without truncation.

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Extreme Contrast Ratios:** Black on white (`21:1`) and terminal amber (`#FF9E00`) on obsidian black (`11.4:1`) exceed WCAG AAA requirements (7:1).
- **Non-Color State Communication (WCAG 1.4.1):** Financial telemetry cells must always include explicit plus/minus signs (`+`, `-`) or status text beside green and red values so color-blind users can instantly distinguish gain from loss.
- **Live Stream Announcements:** Dynamic data feeds must declare `aria-live="polite"` so screen readers can process updates without interrupting the user.
- **Keyboard Operability (WCAG 2.1.1):** Every action is directly reachable via Tab navigation with explicit high-contrast focus indicators.

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- High-throughput financial trading consoles, cryptocurrency orderbooks, and server infrastructure monitoring.
- Independent developer documentation, system man pages, and text-only blogs.
- Sustainable, solar-powered, or low-bandwidth emergency communication networks.

### Anti-Patterns & Prohibitions
- Consumer lifestyle, luxury fashion retail, or children's educational apps.
- Onboarding flows designed for non-technical users where extreme density triggers anxiety.
- Artificially introducing broken links or illegible text to mock users under the guise of "anti-design".

---

## 📚 Authoritative Sources & Historical Artifacts

- Pascal Deville, *Brutalist Websites Archive*, 2014–2022.
- Michael Bloomberg, *Bloomberg by Bloomberg*, John Wiley & Sons, 1997.
- Kris De Decker, *How to Build a Low-tech Website*, Low←Tech Magazine, 2018.
- Reyner Banham, "The New Brutalism", *The Architectural Review*, 1955.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Brutalist Styles:** [ui-style-neo-brutalism](../ui-style-neo-brutalism/SKILL.md), [ui-style-brutalist-monochrome](../ui-style-brutalist-monochrome/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md).
- **Performance & Minimalist Peers:** [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-retro-computing](../ui-style-retro-computing/SKILL.md), [ui-style-blueprint-cad-schematic](../ui-style-blueprint-cad-schematic/SKILL.md).
