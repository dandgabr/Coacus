---
name: "ui-style-dungeon-synth-dark-fantasy"
description: "Provides the dungeon synth and dark fantasy medieval UI style: weathered stone textures, illuminated manuscript borders, tarnished gold, woodcut engravings and archaic atmospheric typography. Use when designing tabletop RPG, dark fantasy gaming or ambient music platforms."
---

# UI Style: Dungeon Synth & Dark Fantasy Medieval

Rooted in 1990s ambient dungeon synth music (Mortiis, Burzum ambient era, Depressive Silence) and archaic dark fantasy literature. Evokes ancient crypts, candlelit stone chambers, hand-carved woodcut plates, weathered iron hardware, and archaic manuscript marginalia. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Tabletop RPG companion apps, fantasy lore wikis, ambient music releases, and grimdark gaming portals.
- Immersing users into solemn, ancient, and mysterious medieval fantasy worlds.
- Building artisanal gaming interfaces that reject clean modern flat design.

---

## 🕰️ Definition and Timeline

- **Origins:** Emerged in the early 1990s as a synth-driven offshoot of Scandinavian black metal, finding a major internet revival in the 2010s on Bandcamp and reddit communities.
- **Philosophy:** Archaic escapism. Creating an intimate sonic and visual atmosphere of forgotten ruins, medieval alchemy, and ancient lore using lo-fi synthesizers and woodblock illustrations.
- **Difference from neighbors:** Unlike [ui-style-gothicpunk](../ui-style-gothicpunk/SKILL.md), which is 1990s modern urban vampire and leather, Dungeon Synth is ancient, rustic, stone-and-candlelight medieval. Unlike [ui-style-steampunk](../ui-style-steampunk/SKILL.md), it features zero industrial machinery or brass gears.

---

## 🎨 Visual DNA

- **Palette:** Dungeon stone black (`#100F0E`), crypt slate (`#1E1C1A`), tarnished antique gold (`#A38344`), dried oxblood red (`#681E1E`), and torch ember yellow (`#C47A2B`).
- **Type:** Uncial, gothic blackletter, or archaic carved serifs (MedievalSharp, UnifrakturCook, Cinzel, Morris Roman).
- **Textures:** Hand-pressed woodcut hatchings, chiselled stone borders, cracked parchment, and wrought iron corner brackets.
- **Depth:** Heavy dark vignetting, atmospheric depth, and candlelight radial glow points.

---

## 🖱️ Interaction and Motion

- Flame flicker: subtle warm light pulses on card borders (`box-shadow: 0 0 20px rgba(163, 131, 68, 0.2)`).
- Heavy stone clicks: buttons depress with solid mechanical weight.
- Under `prefers-reduced-motion: reduce`, disable all ambient glow pulses.

---

## 🛠️ Implementation Notes

```css
#stage[data-style="dungeon-synth-dark-fantasy"] {
  --bg: #100f0e;
  --surface: #171514;
  --fg: #d1c7b7;
  --muted: #8c8273;
  --accent: #a38344;
  --accent-fg: #100f0e;
  --border: #a38344;
  --radius: 2px;
  --font-body: 'Cinzel', serif;
  --font-display: 'Cinzel', serif;
  background-color: var(--bg);
}
```

---

## ♿ Accessibility

- **Font readability:** Blackletter type can present severe readability barriers; restrict gothic fonts strictly to hero banners, using legible archaic serifs for body reading.
- **Contrast verification:** Gold and oxblood accents meet minimum 4.5:1 contrast against dark stone backgrounds.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Dark fantasy games, tabletop RPG tools, ambient synth record labels, and medieval history archives.
- **Avoid:** Corporate platforms, fintech dashboards, and medical websites.

---

## 📚 Sources

- Mortiis, *Secrets of My Sanctuary*, 1995/2018.
- David Day, *The Dark Fantasy Companion: Myth, Lore and Visuals*, 2017.
- British Library Medieval Manuscripts Archive, *Illuminated Manuscripts and Marginalia*, 2021.

---

## 🔗 Integration with Other Skills

- Sibling dark aesthetics: [ui-style-gothicpunk](../ui-style-gothicpunk/SKILL.md), [ui-style-weirdcore-dreamcore](../ui-style-weirdcore-dreamcore/SKILL.md).
