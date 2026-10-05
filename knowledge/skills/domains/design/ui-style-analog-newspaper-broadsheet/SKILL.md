---
name: "ui-style-analog-newspaper-broadsheet"
description: "Provides the broadsheet newspaper and letterpress print UI style: multi-column editorial grid, ornamental drop-caps, hairline column rules, woodblock illustrations and authentic newsprint texture. Use when designing longform journalism, literary presses or historical archives."
---

# UI Style: Broadsheet Newspaper & Letterpress

Translates the authoritative, multi-column format of classical daily broadsheet newspapers (*The New York Times*, *The Times*, *Neue Zürcher Zeitung*) and letterpress printing into modern digital interfaces. Characterized by strict multi-column vertical rules, ornate drop caps, headline decks, and authentic ink-on-paper textures. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Longform investigative journalism, literary journals, historical archives, legal gazettes, and editorial publications.
- Conveying timeless journalistic credibility, literary depth, and historical authenticity.
- Presenting longform narrative prose in a layout calibrated for deep, scholarly reading.

---

## 🕰️ Definition and Timeline

- **Origins:** Originates in 17th-century European broadsheets, formalized in the 19th-century mechanized rotary press era, and adapted to digital screens by pioneers of web typography (Khoi Vinh, *The New York Times* digital design team).
- **Philosophy:** Typographic hierarchy as the guarantor of truth. Organizing vast volumes of complex news through disciplined vertical column rules, calibrated type scales, and authoritative serif fonts.
- **Difference from neighbors:** Unlike [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), which is glossy, minimal, and high-fashion oriented, Broadsheet is ink-dense, multi-column, headline-deck structured, and journal-authoritative.

---

## 🎨 Visual DNA

- **Palette:** Yellowed newsprint paper (`#F5F2EB`), archival printer's ink black (`#1C1B1A`), lead gray metadata (`#595652`), and vintage red headline deck ink (`#A82C2C`).
- **Type:** Classical editorial serif families (Newsreader, Playfair Display, Merriweather, Georgia) with dramatic 4-line drop-caps and centered all-caps deck headers.
- **Grid & Layout:** Strict 3 to 6-column text flows separated by 1px solid vertical hairline rules (`column-rule: 1px solid #D4CEBE`), datelines, and article index boxes.
- **Details:** Woodblock and etching engravings, double horizontal section dividing rules (thick-over-thin), and volume numbering.

---

## 🖱️ Interaction and Motion

- Minimal, dignified transitions: link hover triggers subtle archival red color shifts or fine underline reveals.
- Zero decorative bouncing or parallax distractions: motion is strictly functional.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="analog-newspaper-broadsheet"] {
  --bg: #f5f2eb;
  --surface: #ffffff;
  --fg: #1c1b1a;
  --muted: #595652;
  --accent: #a82c2c;
  --accent-fg: #f5f2eb;
  --border: #1c1b1a;
  --radius: 0;
  --font-body: 'Newsreader', 'Georgia', serif;
  --font-display: 'Newsreader', 'Playfair Display', serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Responsive multi-column:** Multi-column text (`column-count`) must automatically collapse into a single column on mobile screens under 768px to prevent horizontal scrolling.
- **Optimal contrast:** Archival printer's ink on newsprint paper delivers superior contrast (> 12:1), guaranteeing effortless longform reading.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Investigative journalism, literary reviews, historical gazettes, legal archives, and longform essays.
- **Avoid:** Fast-paced gaming sites, SaaS admin consoles, and colorful youth lifestyle brands.

---

## 📚 Sources

- Allen Hutt, *The Changing Newspaper: Typographic Trends in Britain and America*, Gordon Fraser, 1973.
- Mario Garcia, *Pure Design: 79 Simple Solutions for Magazine and Newspaper Design*, 2002.
- Society for News Design (SND), *Annual Best of News Design*, 2020–2023.

---

## 🔗 Integration with Other Skills

- Sibling editorial styles: [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md), [ui-style-expressive-variable-typography](../ui-style-expressive-variable-typography/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md).
