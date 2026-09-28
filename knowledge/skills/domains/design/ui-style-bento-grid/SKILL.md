---
name: "ui-style-bento-grid"
description: "Provides the bento grid UI style (2022-present): compartmentalized bento-box layouts of asymmetric rounded tiles with hierarchy expressed by span rather than shadow, covering the CSS grid recipe, Apple keynote lineage, motion patterns, DOM-order accessibility risks and appropriate page types. Use when designing feature overviews, marketing pages or portfolio grids in the Apple bento grammar."
---

# UI Style: Bento Grid

Compartmentalized "bento box" module grids — asymmetric rounded tiles of varying span (hero tile + small stat tiles) on one shared gutter grid, hierarchy expressed purely by span. Named after the Japanese lunchbox; modernized by Apple's WWDC 2022 / iPhone 14 keynote visual language. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing feature overviews, pricing/marketing pages, portfolios or changelogs.
- Converting a feature list into an Apple-style module composition.
- Reviewing bento layouts for source-order and heading accessibility.

---

## 🕰️ Definition and Timeline

- Long prehistory: dashboard widgets, Material cards (2014), Swiss grids; link-in-bio product Bento (bento.me) took the name for card-grid personal pages.
- The modern wave is Apple's: WWDC 2022 and the September 2022 iPhone 14 newsroom module system, tightened through WWDC 2023 decks (deck.gallery's four-deck comparison documents the format).
- 2023–present adoption across SaaS marketing; now default landing-page grammar rather than a passing fad.

---

## 🎨 Visual DNA

- **Grid:** shared gutter (8–24px) + uniform corner radius across all tiles; separation by gap alone, minimal borders.
- **Hierarchy by span:** col/row count — not shadow, not color.
- **Tiles alternate content types:** screenshot, stat, logo cloud, quote, video loop; dark/light tiles alternate for rhythm.
- **Type:** large tight display in the hero tile; small labels elsewhere; icons oversized and centered; internally symmetric, centered content (Apple style).

---

## 🖱️ Interaction and Motion

- Staggered tile reveals on scroll; hover lift or inner parallax on media tiles; autoplaying product clips inside tiles; occasional count-up stats. Motion is per-tile, never grid-wide.

---

## 🛠️ Implementation Notes

```css
.bento { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
.tile-hero { grid-column: span 8; grid-row: span 2; }
.tile-stat { grid-column: span 4; }
.tile { border-radius: 24px; overflow: hidden; }
```

- `aspect-ratio` for consistent tile shapes; media queries collapse spans at tablet/mobile; container queries for per-tile typography.
- Reference: CSS-Tricks "Complete Guide to CSS Grid"; MDN "Card component" cookbook.

---

## ♿ Accessibility

- Best contrast profile of the 2020s styles (solid tile fills) — the risks are **structural**: visual grid placement can scramble DOM/reading order; heading levels scatter across tiles; keep each tile self-contained with its own semantic heading; preserve focus order; giant hero tiles push key info below the fold; avoid low-contrast text-over-image tiles (MDN "Grid layout and accessibility").

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** feature overviews, pricing/marketing, portfolios, changelogs.
- **Avoid:** long-form reading, dashboards with fixed data priority, CMS-generated volatile content (bento is curated composition).

---

## ⚠️ Pitfalls

- Everything-looks-important: uniform prettiness flattens priority; bespoke responsive span mapping; "bento-ification" sameness across SaaS; image-heavy tiles cost performance.

---

## 📚 Sources

- deck.gallery, "Apple's bento grid playbook, four keynote decks compared", 2026 — https://www.deck.gallery/blog/apple-bento-grid-decks-roundup/
- Apple, "Apple introduces iPhone 14 and iPhone 14 Plus", Newsroom, Sep 7, 2022 — https://www.apple.com/newsroom/2022/09/apple-introduces-iphone-14-and-iphone-14-plus/
- Chris Coyier et al., "A Complete Guide to CSS Grid", CSS-Tricks — https://css-tricks.com/snippets/css/complete-guide-grid/
- MDN, "Grid layout and accessibility" — https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Accessibility
- C. Jeffrey Hasan, "Apple's Bento Grid Secret", Medium, 2025 — https://medium.com/@jefyjery10/apples-bento-grid-secret-how-a-lunchbox-layout-sells-premium-tech-7c118ce898aa

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-card-based-ui](../ui-style-card-based-ui/SKILL.md), [ui-style-swiss-web-minimalism](../ui-style-swiss-web-minimalism/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
- For grid mechanics, see [frontend-developer](../../../roles/frontend-developer/SKILL.md).
