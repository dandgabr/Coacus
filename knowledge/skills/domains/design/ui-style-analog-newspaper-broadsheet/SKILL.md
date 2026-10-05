---
name: "ui-style-analog-newspaper-broadsheet"
description: "Provides the broadsheet newspaper and letterpress print UI style: multi-column editorial grid, ornamental drop-caps, hairline column rules, woodblock illustrations and authentic newsprint texture. Use when designing longform journalism, literary presses or historical archives."
---

# UI Style: Broadsheet Newspaper & Letterpress

Translates the authoritative, multi-column format of classical daily broadsheet newspapers and letterpress printing into modern digital interfaces. Characterized by strict multi-column vertical rules, ornate drop caps, headline decks, and authentic ink-on-paper textures.

---

## 🧭 When to Activate

- Longform investigative journalism, literary journals, historical archives, legal gazettes, and editorial publications.
- Conveying timeless journalistic credibility, literary depth, and historical authenticity.

---

## 🎨 Visual DNA

- **Palette:** Yellowed newsprint paper (`#F5F2EB`), archival printer's ink black (`#1C1B1A`), faded lead gray (`#595652`), and vintage red headline ink (`#A82C2C`).
- **Type:** Classical editorial serif families (Playfair Display, Merriweather, Georgia, Newsreader) with dramatic drop-caps.
- **Layout:** Strict 3 to 6-column text flows separated by 1px solid hairline rules, centered headline decks, and publication datelines.

---

## 🛠️ Implementation Notes

```css
.broadsheet-article {
  background: #f5f2eb;
  color: #1c1b1a;
  font-family: 'Newsreader', serif;
  column-count: 3;
  column-gap: 2rem;
  column-rule: 1px solid #d4cebe;
}
.drop-cap {
  float: left;
  font-size: 4rem;
  line-height: 0.8;
  padding-right: 8px;
  font-weight: 700;
}
```

---

## ♿ Accessibility

- Multi-column CSS layouts (`column-count`) must be handled carefully on mobile viewports: use CSS media queries to collapse columns to single column on viewports under 768px.
- High contrast (> 10:1) between archival ink and newsprint background guarantees easy reading.
