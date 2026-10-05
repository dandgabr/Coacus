---
name: "ui-style-terminal-tui"
description: "Provides the terminal / TUI UI style (1970s-present, web revival 2015-present): monospace cell grid, box-drawing frames, ANSI palettes and keyboard-first interaction, covering the character-cell layout model, ANSI color tiers, block-cursor and prompt motion, and accessible web emulation. Use when designing developer tools, CLI-adjacent dashboards, terminal-themed marketing pages or real terminal applications."
---

# UI Style: Terminal / TUI

Interface as a grid of character cells: one monospace font, box-drawing frames, a 16-color ANSI palette and keyboard-first control. Native in terminal applications (ncurses, Ratatui), imitated on the web by developer-tool brands. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing real TUIs (dashboards, file managers, editors, monitoring) or their web counterparts.
- Building developer-tool landing pages, docs or playgrounds with a terminal identity.
- Deciding how much terminal fidelity a browser surface can afford without hurting accessibility.

---

## 🕰️ Definition and Timeline

- A TUI is an early form of human-computer interaction from before bitmapped displays and GUIs; it often uses box-drawing characters for structure and persists in terminal emulators today.
- Lineage: ECMA-48 (1976) and ANSI X3.64 (1979) escape codes; DEC VT100 (1978) spread them; the IBM PC's CP437 supplied box-drawing glyphs; Norton Commander, WordPerfect and Lotus 1-2-3 defined the DOS-era look; curses/ncurses carried it across Unix.
- Modern wave: Ratatui (Rust, immediate-mode rendering) and similar libraries; web pages emulate it for developer audiences.
- Difference from neighbors: [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md) is sci-fi spectacle (glow, scanlines, HUD chrome); terminal/TUI is functional and cell-quantized, with no glow required. [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md) celebrates bitmap graphics and GUI nostalgia; this style is text-first.

---

## 🎨 Visual DNA

- **Type:** one monospace family (JetBrains Mono, IBM Plex Mono, Berkeley Mono, Iosevka); a single size scale in whole "rows"; line-height as an integer multiple of the cell height.
- **Grid:** layout in `ch` and `lh` units; every box, gutter and rule snaps to character cells.
- **Frames:** Unicode Box Drawing block (U+2500-U+257F: `┌ ─ ┐ │ └ ┘ ├ ┤`) or CSS borders that imitate them; titles inset into the top rule.
- **Color:** ANSI 16 palette with a tuned background (e.g. `#0c0c0c`/`#f5f5f0`); semantic accents only (green ok, red error, yellow warn, cyan info); 256-color and 24-bit as progressive enhancement.
- **Chrome:** status bar with key hints (`q quit  / search  ? help`), prompt glyph (`$`, `>`), inverse-video selection, block cursor.

---

## 🖱️ Interaction and Motion

- Keyboard first: visible shortcuts, vim/arrow navigation, command palette; mouse optional.
- Motion is discrete: blinking cursor, typed output, line-by-line reveal, spinners of braille or ASCII frames; stepped timing (`steps()`), never eased.
- Selection by inverse video, not color alone; focus always a visible cell-aligned block.

---

## 🛠️ Implementation Notes

```css
:root {
  --bg: #0c0c0c; --fg: #d8d8d0; --dim: #8a8a84;
  --ok: #5fd75f; --warn: #ffd75f; --err: #ff5f5f; --info: #5fd7ff;
  --cell: 1ch; --row: 1.5rem;
}
body { background: var(--bg); color: var(--fg);
  font: 400 16px/var(--row) "JetBrains Mono", ui-monospace, monospace;
  font-variant-numeric: tabular-nums slashed-zero; font-variant-ligatures: none; }
.box { border: 1px solid var(--dim); padding: var(--row) 2ch; }
.sel { background: var(--fg); color: var(--bg); }
.cursor { display: inline-block; width: 1ch; background: var(--fg);
  animation: blink 1.06s steps(1) infinite; }
@keyframes blink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .cursor { animation: none; } }
```

- Real TUIs: honor color tiers (detect 4-bit, 8-bit, 24-bit; respect `NO_COLOR`) and redraw only changed cells.
- Web emulation: render real DOM text, never a canvas or image of text; keep ASCII art `aria-hidden` with a text alternative.

---

## ♿ Accessibility

- 1.4.3 contrast (4.5:1): dim gray and pure ANSI blue/red on black frequently fail; test every pair, retune the palette.
- 1.4.1: never rely on color for status; add glyph or word (`ERR`, `OK`).
- 1.4.11 (3:1) for frames and focus cells; 2.4.7 and 2.4.11 for visible, unobscured focus; 2.1.1 full keyboard operation without keyboard traps (2.1.2).
- 1.4.4 and 1.4.10: use `rem`/`ch`, allow reflow at 320 CSS px; fixed-width boxes must not force horizontal scrolling.
- ASCII/box art read aloud as noise: hide with `aria-hidden` and use real headings, lists and tables.
- `prefers-reduced-motion: reduce`: stop blink, typewriter and spinner animation; show final text.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** developer tools, observability, infra and security products, CLI docs, hacker-culture brands, genuine terminal applications.
- **Caution:** consumer onboarding, forms with long text (monospace slows reading of prose).
- **Avoid:** audiences new to computing, content-heavy editorial, mobile-first commerce.

---

## ⚠️ Pitfalls

- Fake terminals that cannot be selected, copied or searched; typewriter effects delaying content.
- Mixing proportional fonts into the grid and breaking alignment; CJK and emoji widths misaligning cells.
- Box-drawing glyphs falling back to a different font and tearing frames.
- Cosplay: `$ sudo` jokes with no real command-line affordance.

---

## 📚 Sources

- "Text-based user interface" (Wikipedia) — https://en.wikipedia.org/wiki/Text-based_user_interface
- "Box-drawing characters" (Wikipedia) — https://en.wikipedia.org/wiki/Box-drawing_characters
- "ANSI escape code" (Wikipedia) — https://en.wikipedia.org/wiki/ANSI_escape_code
- Ratatui project, "Ratatui" — https://ratatui.rs/
- MDN, "font-variant-numeric" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
- MDN, "prefers-reduced-motion" (Mozilla) — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- `NO_COLOR` convention and the cell-snapping rules above are practitioner synthesis: `unverified` here.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-cyberpunk-hud](../ui-style-cyberpunk-hud/SKILL.md), [ui-style-retro-computing-pixel](../ui-style-retro-computing-pixel/SKILL.md), [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md).
