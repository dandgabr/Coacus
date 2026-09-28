---
name: "ui-style-card-based-ui"
description: "Provides the card-based UI style (2013-present): self-contained content containers in grids and masonry, covering Material's card anatomy, Bootstrap 4 standardization, masonry techniques, container transforms and the density and reading-order pitfalls. Use when designing feeds, commerce grids, dashboards or any card-component system."
---

# UI Style: Card-Based UI

Self-contained content containers — "content and actions about a single subject" — in masonry or grid arrangements. Prehistory: Trello kanban (2011), Pinterest's masonry feed; codified by Material Design (June 25, 2014) with defined anatomy, elevation and container-transform motion; standardized for the web by Bootstrap 4 (2018); the bento trend is its direct descendant. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing mixed-media feeds, commerce grids, kanban or social timelines.
- Building card component systems (anatomy, elevation, actions).
- Choosing masonry versus grid and its assistive-tech costs.

---

## 🕰️ Definition and Timeline

- Pinterest popularized masonry (founded 2010); Material (2014) codified card anatomy — thumbnail → header → subhead → supporting text → actions; Bootstrap 4 cards (v4.0, 2018 — https://getbootstrap.com/docs/4.0/components/card/) replaced "panels, wells, and thumbnails"; Masonry.js (David DeSandro) is the layout library of record; Luke Wroblewski's 2014 "Cards" essay framed the pattern [unverified URL].

---

## 🎨 Visual DNA

- **Anatomy (Material):** media/thumbnail, header, subhead, supporting text, action row.
- **Surfaces:** white/elevated cards on tinted backgrounds; Material 2 corner radius + subtle resting shadow; flat bordered variants (Bootstrap offers both).
- **Shapes:** rounded rectangles, uniform gutters, fixed media ratios.
- **Iconography:** action icons in card footers; **layout:** equal-height flex rows, multi-column masonry, later true CSS Grid.

---

## 🖱️ Interaction and Motion

- Whole-card tap targets; hover lift; Material's container transform (card expands to full screen as a parent-child transition — "cards don't flip" is an explicit don't); swipe-to-dismiss, drag-to-reorder (kanban); infinite scroll with skeleton loaders.

---

## 🛠️ Implementation Notes

- Masonry: `column-count` + `break-inside: avoid` (Bootstrap 4's approach, with its own caveat that it is not bulletproof) or Masonry.js/Isotope positioning.
- Modern grids: `grid-template-columns: repeat(auto-fill, minmax(240px, 1fr))`; flexbox equal heights; `aspect-ratio` for stable media boxes; container queries for self-adaptive cards.

---

## ♿ Accessibility

- Masonry ordering disrupts screen-reader and scan order; infinite scroll harms findability and deep linking; "boxy sameness" and container-in-container nesting; density loss versus lists/tables; Material-style depth only helps when metaphors stay consistent (NN/g).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** heterogeneous items needing scannable self-contained grouping — feeds, commerce, streaming, kanban.
- **Avoid:** dense data tables/enterprise tooling, strict reading-order requirements, CMS firehoses without curation.

---

## ⚠️ Pitfalls

- Virtualized long card lists cost performance; visual masonry order ≠ DOM order unless corrected; every-card-equal-weight flattens hierarchy.

---

## 📚 Sources

- Google, "Cards — Material Design (M2)" — https://m2.material.io/components/cards
- Bootstrap Team, "Cards · Bootstrap 4.0" — https://getbootstrap.com/docs/4.0/components/card/
- MDN, "Card component" (CSS Layout Cookbook) — https://developer.mozilla.org/en-US/docs/Web/CSS/How_to/Layout_cookbook/Card
- David DeSandro, "Masonry" — https://masonry.desandro.com/
- Kate Moran, "Flat Design..." (documents the card metaphor in flat 2.0), NN/g, 2015 — https://www.nngroup.com/articles/flat-design/
- Luke Wroblewski, "Cards", lukew.com, 2014 [unverified URL]

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md), [ui-style-material-you](../ui-style-material-you/SKILL.md), [ui-style-one-page-long-scroll](../ui-style-one-page-long-scroll/SKILL.md).
