---
name: "ui-style-indie-web-revival"
description: "Provides the indie web revival UI style (2013-present): personal, hand-built static sites in the spirit of GeoCities, Neocities and the IndieWeb, with webrings, 88x31 buttons, guestbooks, system fonts and owner-controlled expression, covering structure, semantics, performance and WCAG handling. Use when designing personal, community or zine-like sites that value ownership, quirk and lightweight HTML over polished SaaS templates."
---

# UI Style: Indie Web Revival

Personal-website aesthetics as a stance: handmade static HTML, quirky and owner-controlled, opposing platform sameness. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Personal sites, digital gardens, band, zine, fan and community pages.
- Projects that value ownership, longevity and low weight over conversion polish.
- Requests for "Neocities look", "GeoCities", "webring", "personal homepage" or "IndieWeb".

---

## 🕰️ Definition and Timeline

- Neocities: created by Kyle Drake 23 May 2013, launched 28 June 2013, to revive free hosting in the spirit of defunct GeoCities; frames itself as "static HTML websites" and a counterforce to social media; free hosting, user ownership, no ads, no data sales.
- IndieWeb: ownership and control of your online presence; own your data; POSSE (Publish on Own Site, Syndicate Elsewhere); simple interoperable protocols.
- Related artifacts: web badges, webrings, personal pages (Wikipedia lists them alongside Neocities).
- Distinction from [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md): brutalism is an aesthetic of rawness; this is a culture and publishing model whose look is playful, personal and nostalgic, not necessarily harsh.
- Distinction from [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md) and [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md): those are visual eras; this is defined by personal ownership, often borrowing 1990s-2000s web idioms.

---

## 🎨 Visual DNA

- **Structure:** hand-written HTML and CSS, few or no frameworks; a home page with "about", links, blog or log, guestbook, links to friends.
- **Type:** system fonts or a single web font; default serifs or monospace used on purpose; visible link underlines.
- **Color:** owner's taste: tiled backgrounds, saturated links, or soft pastel; a stated palette per site, not a framework default.
- **Ephemera:** 88x31 buttons, webrings, visitor-style counters, "under construction" jokes, now-pages, RSS links, sticker graphics.
- **Layout:** simple single column or table-like grids; asymmetry and personality over system consistency.

---

## 🖱️ Interaction and Motion

- Minimal: hover underlines, small GIF-like loops, cursor tricks used sparingly.
- Navigation is plain links; no JS required for reading. Stateful features (guestbook, webmention) are server-side or third-party.

---

## 🛠️ Implementation Notes

```css
:root { --bg:#fffbe6; --fg:#1a1a1a; --link:#0645ad; --accent:#d4380d; }
body { max-width: 62ch; margin: 2rem auto; padding: 0 1rem; font: 1.125rem/1.6 Georgia, serif; background: var(--bg); color: var(--fg); }
a { color: var(--link); text-decoration: underline; }
a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.badge { width: 88px; height: 31px; image-rendering: pixelated; }
.marquee-ish { animation: slide 12s linear infinite; }
@media (prefers-reduced-motion: reduce) { .marquee-ish { animation: none; } }
```

- Use semantic HTML (`header`, `nav`, `main`, `article`); add `rel="me"` and an RSS/Atom feed for IndieWeb discoverability.
- Give every badge and graphic an `alt`; keep the whole site static and cacheable.

---

## ♿ Accessibility

- Tiled or loud backgrounds often break 1.4.3 contrast; put text on a solid panel.
- Animated GIFs, marquees and blinking ephemera: pause or remove (2.2.2), no flashing (2.3.1), honor `prefers-reduced-motion`.
- Alt text for 88x31 buttons and image links (1.1.1, 2.4.4); webring links need descriptive text.
- Semantic headings and landmarks (1.3.1, 2.4.1); keyboard operability of guestbooks (2.1.1); visible focus (2.4.7).
- Link color differs by more than color alone, so keep underlines (1.4.1); target size 24px minimum for badge links (2.5.8).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** personal sites, blogs, digital gardens, zines, fan and club pages, portfolios with personality.
- **Caution:** small business pages (credibility cues still needed).
- **Avoid:** transactional, regulated or enterprise products; sites needing consistent design-system governance.

---

## ⚠️ Pitfalls

- Nostalgia pastiche without function: autoplay audio, unreadable backgrounds, tiny text.
- Reproducing the look while still depending on silos, which loses the ownership point.
- Hotlinking third-party badge or counter services that leak visitor data; self-host assets.

---

## 📚 Sources

- Wikipedia contributors, "Neocities" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Neocities
- Neocities, "About" (Neocities) — https://neocities.org/about (accessed 2026-10-05)
- IndieWeb community, "Why" (indieweb.org) — https://indieweb.org/why (accessed 2026-10-05)
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2" (W3C Recommendation), 12 Dec 2024 — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md), [ui-style-y2k-revival](../ui-style-y2k-revival/SKILL.md), [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md), [ui-style-hand-drawn-sketch](../ui-style-hand-drawn-sketch/SKILL.md), [ui-style-collage-scrapbook](../ui-style-collage-scrapbook/SKILL.md), [ui-style-calm-quiet-ui](../ui-style-calm-quiet-ui/SKILL.md).
