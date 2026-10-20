# Text Effect Recipes

Use when animating text itself: split-text reveals, staggered entrances, scramble/decode, typewriter, and number tickers or odometers. These are mechanics, independent of any visual style; style skills such as [ui-style-kinetic-typography](../../ui-style-kinetic-typography/SKILL.md) link here. Durations, easing and spring presets come from [motion-timing-engines.md](motion-timing-engines.md): CSS below uses its tokens (`--motion-state`, `--motion-layout`, `--motion-narrative`, `--ease-enter`), and script reads the same tokens with the `motionMs()` helper shown in [pointer-and-gesture.md](pointer-and-gesture.md#global-gating). Accessibility obligations (2.2.2, 2.3.1, 2.3.3, 4.1.3 and the reduced-motion house policy) live in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../../engineering/practices/web-accessibility-wcag/SKILL.md).

## The accessible-text contract (applies to every recipe)

Animated fragments are presentation; the accessible name is the real sentence.

```html
<h1 class="fx-text">
  <span class="visually-hidden">Ship faster with fewer regressions</span>
  <span class="fx-text__visual" aria-hidden="true"><!-- split / scrambled / typed fragments --></span>
</h1>
```

```css
.visually-hidden {
  position: absolute !important; width: 1px; height: 1px;
  margin: -1px; padding: 0; overflow: hidden;
  clip-path: inset(50%); white-space: nowrap; border: 0;
}
```

- One visually-hidden full copy plus `aria-hidden="true"` on the animated fragments. Screen readers read one continuous sentence; per-character spans otherwise read as letters or stutter.
- Never put `aria-label` on a generic `span`, `div` or `p`: ARIA 1.2 prohibits naming those roles and assistive technology ignores it inconsistently.
- Links or emphasis inside the text must live in the visually-hidden copy (real, focusable) and only as styling in the visual copy, or the text must not be split.
- Never announce intermediate states. No `aria-live` on anything that changes per frame.
- Without JavaScript, or before the effect runs, the final text must already be visible. Hide fragments, not content.

## Split text

Split only after web fonts load, or line breaks are computed with fallback metrics and break again when the real font swaps in.

```js
await document.fonts.ready;
const split = SplitText.create('.fx-text__visual', {
  type: 'words, chars',    // no 'lines': breaks are not frozen, so no autoSplit needed
  aria: 'hidden',          // we provide the visually-hidden copy ourselves
  mask: 'words',           // wrapper with clipping for slide-up reveals
  onSplit(self) {          // build animations here; returning one lets revert() kill it
    return gsap.from(self.chars, {
      yPercent: 100, opacity: 0, duration: motionMs('--motion-layout') / 1000, ease: 'power3.out',
      stagger: { amount: 0.4 },
    });
  },
});
// On teardown (route change, unmount):
split.revert();            // restores the original markup and kills the returned animation
```

GSAP SplitText options that matter (rewritten in 3.13, free since then):

| Option | Use |
|---|---|
| `aria: 'auto' \| 'hidden' \| 'none'` | `'auto'` adds an `aria-label` to the split element and hides the pieces; it drops the semantics of nested links. Prefer `'hidden'` plus your own visually-hidden copy. |
| `autoSplit` + `onSplit()` | Re-split when fonts load or the element width changes. It only earns its cost when `type` includes `'lines'` (word and char splits do not depend on width, and the example already awaits `document.fonts.ready`). Return the animation from `onSplit` so it is reverted and resynchronised on each re-split. |
| `mask: 'lines' \| 'words' \| 'chars'` | Adds a clipping wrapper per piece for reveal-from-below effects; one type only. |
| `deepSlice` | Default `true`: a nested element that wraps across lines is subdivided so lines do not grow taller. |
| `revert()` | Restores the original DOM. Call it on teardown and before re-splitting manually. |

Pitfalls:

- Splitting into per-character inline-blocks breaks kerning pairs and ligatures (`fi`, `ffl`, contextual alternates), so split text looks looser than the original. Split by words or lines when the font relies on them, and revert after the entrance so the resting state uses native shaping.
- Line splits freeze line breaks at split time. User text-spacing overrides (SC 1.4.12; test values in the `🎞️ Motion and Animation` section of [web-accessibility-wcag](../../../../engineering/practices/web-accessibility-wcag/SKILL.md)) applied after the split must not clip or overlap; `autoSplit` covers width changes, not user stylesheets, so revert to unsplit text once the animation ends.
- Split only display headings and short phrases. Splitting body copy multiplies nodes and style recalculation.
- SplitType is stale (last publish 2023-10-22); prefer GSAP SplitText or a small custom splitter that follows the contract above.
- Reduced motion: skip the split entirely and show the text. Splitting and then animating with zero duration still pays the DOM cost and the shaping loss.

## Stagger

Stagger communicates order, not quantity. Cap the total spread regardless of item count, using the stagger cap in [motion-timing-engines.md](motion-timing-engines.md), or the last item arrives after the user has moved on.

```css
.fx-stagger {
  --fx-stagger-step: 40ms;   /* per-item offset */
  --fx-stagger-cap: 400ms;   /* total spread: take the value from the stagger cap */
}
/* Fallback first: server or template writes --i on each item. */
.fx-stagger > * {
  transition: opacity var(--motion-state) var(--ease-enter), transform var(--motion-state) var(--ease-enter);
  transition-delay: calc(var(--i, 0) * var(--fx-stagger-step));
}
/* Enhancement: tree-counting functions remove the --i bookkeeping. */
@supports (transition-delay: calc(sibling-index() * 1ms)) {
  .fx-stagger > * {
    transition-delay: calc((sibling-index() - 1) * min(var(--fx-stagger-step), var(--fx-stagger-cap) / sibling-count()));
  }
}
```

`sibling-index()` and `sibling-count()` are Baseline newly available since 2026-08-18 (Chrome 138, Firefox 154, Safari 26.2), so the `--i` fallback is mandatory. With the fallback, clamp in the template (`--i: min(index, 10)`) to keep the cap.

```js
// GSAP: per-item spacing or a total budget, with an origin.
gsap.from('.card', { y: 16, opacity: 0, stagger: { each: 0.04, from: 'start' } });
gsap.from('.cell', { scale: 0.9, opacity: 0, stagger: { amount: 0.4, from: 'center' } });

// Motion
import { animate, stagger } from 'motion';
animate('.row', { opacity: [0, 1], y: [8, 0] }, { delay: stagger(0.04, { from: 'first' }) });
```

Prefer `amount` (total budget) over `each` for lists of unknown length. Reduced motion: no stagger; everything appears together with a short opacity fade or instantly.

## Text scramble

Characters cycle through random glyphs and resolve left to right into the final string. Decorative; the final text must be accessible from the start.

```js
function scramble(visualEl, finalText, { duration = motionMs('--motion-narrative'), chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' } = {}) {
  const start = performance.now();
  // Each character resolves at a staggered time across the first 70% of the run.
  const resolveAt = [...finalText].map((_, i) => (i / finalText.length) * 0.7 * duration + Math.random() * 0.3 * duration);
  let frame = 0;
  const tick = (now) => {
    const t = now - start;
    let out = '', done = true;
    for (let i = 0; i < finalText.length; i++) {
      const ch = finalText[i];
      if (ch === ' ' || t >= resolveAt[i]) out += ch;
      else { done = false; out += chars[(Math.random() * chars.length) | 0]; }
    }
    visualEl.textContent = out;                   // visual copy is aria-hidden
    frame = done ? 0 : requestAnimationFrame(tick);
  };
  frame = requestAnimationFrame(tick);
  return () => { cancelAnimationFrame(frame); visualEl.textContent = finalText; };
}
```

GSAP's ScrambleTextPlugin (free) does the same with `scrambleText: { text, chars, revealDelay, speed }`.

Pitfalls:

- Use a monospace font, or fix each character cell width, or the line width jitters every frame and reflows the surrounding layout.
- Keep the final text in the visually-hidden copy; never `aria-live`, which would announce every random frame.
- A looping or repeating scramble that runs longer than 5 seconds needs a visible pause/stop control (SC 2.2.2).
- Rapid full-word glyph changes at high contrast over a large area can count as flashing; keep it to small text and short runs and check SC 2.3.1.
- Reduced motion: render the final text directly.

## Typewriter

Text appears character by character with a caret.

```html
<p class="fx-type-line"><span class="fx-type" style="--fx-type-chars: 22">Hello, motion engineer</span></p>
```

```css
/* CSS-only: monospace, single line, known string length (--fx-type-chars). */
.fx-type-line { min-block-size: 1lh; }             /* reserve the line: no vertical jump */
.fx-type {
  display: inline-block;                           /* width applies; it is ignored on inline boxes */
  font-family: ui-monospace, monospace;
  white-space: nowrap;
  overflow: clip;                                  /* hides untyped glyphs visually, not from AT */
  inline-size: calc(var(--fx-type-chars) * 1ch);   /* resting state = complete text */
  border-inline-end: 0.08em solid currentColor;    /* caret rides the clipped edge */
  animation:
    fx-type var(--motion-narrative) steps(var(--fx-type-chars), end) both,
    fx-caret 1s step-end var(--motion-narrative) 4; /* blink after typing; finite: 4 blinks */
}
@keyframes fx-type { from { inline-size: 0; } }    /* 0 → N ch, one character per step */
@keyframes fx-caret { 50% { border-inline-end-color: transparent; } }
@media (prefers-reduced-motion: reduce) {
  .fx-type { animation: none; border-inline-end-color: transparent; }
}
```

- The box width is animated, so each step relayouts the line; `steps(N)` limits that to N layouts in total, and the element ends at its natural width, so put it on its own line (or in a container sized to the final width) so neighbouring content does not shift as it types. The caret is the element's own end border, so it is always at the last revealed character and needs no pseudo-element that clipping would hide.
- `--motion-narrative` is for decorative, non-blocking text only; a typewriter that gates reading or a task is out of scope (see the gate below).
- `steps(N)` plus `ch` is only correct for monospace, single-line strings whose length is known. Proportional fonts, wrapping, variable strings and localisation (translated length, CJK full-width glyphs, combining marks, emoji clusters, right-to-left scripts) need a JavaScript typer that advances by grapheme (`Intl.Segmenter`) and writes into an `aria-hidden` visual copy.
- The full text is exposed from the start: the CSS version keeps all text in the DOM and only clips it visually (`overflow: clip` does not remove text from the accessibility tree); the JavaScript version keeps the full string in the visually-hidden copy. Announce, if anything, only the final value (SC 4.1.3), never each character.
- A blinking caret is moving content: give the blink a finite iteration count or stop it when typing ends; an infinite blink beside other content longer than 5 seconds needs a stop mechanism (SC 2.2.2).

> **Default: No** — typewriter reveal of AI chat replies in operational UIs
> - **Allowed when:** the text genuinely streams from the server and is rendered as it arrives, or the surface is a marketing demo.
> - **Evidence required:** no artificial delay added to text that is already complete; users can read, copy and act on the full reply immediately; the reply is announced once, when complete.
> - **Fallback:** render the complete reply at once, optionally with a short opacity fade.

## Number ticker and odometer

A value counts or rolls to its final number. The final number is real text; intermediate values are decoration.

### CSS counter ticker (integers)

```css
@property --n { syntax: '<integer>'; inherits: false; initial-value: 0; }
.fx-ticker__visual {
  font-variant-numeric: tabular-nums;             /* fixed digit width: no jitter */
  transition: --n var(--motion-narrative) var(--ease-enter);
  counter-reset: n var(--n);
}
.fx-ticker__visual::after { content: counter(n); }
.fx-ticker.is-done .fx-ticker__visual { --n: 1280; }
@media (prefers-reduced-motion: reduce) {
  .fx-ticker__visual { transition: none; }        /* jumps to the final value */
}
```

```html
<p class="fx-ticker">
  <span class="visually-hidden">1,280 active users</span>
  <span class="fx-ticker__visual" aria-hidden="true"></span>
</p>
```

Registering `--n` as `<integer>` makes it interpolate (and round) instead of flipping; `counter()` turns it into text. Generated content is exposed to assistive technology, so the wrapper is `aria-hidden` and the real value sits in the visually-hidden copy. `counter()` cannot group thousands or show decimals or currency; use the digit-roll pattern for formatted numbers.

### Rolling digits with `Intl.NumberFormat#formatToParts`

```js
function odometer(el, value, locale = navigator.language, opts = {}) {
  // Accessible copy: the user's locale, including its native digits.
  el.querySelector('.visually-hidden').textContent = new Intl.NumberFormat(locale, opts).format(value);
  // Visual copy: the columns hold 0–9, so force Latin digits for the rolling part only;
  // separators, grouping and currency position still follow the locale.
  const parts = new Intl.NumberFormat(locale, { ...opts, numberingSystem: 'latn' }).formatToParts(value);
  const visual = el.querySelector('.fx-odo__visual');      // aria-hidden
  const targets = [];
  visual.replaceChildren(...parts.flatMap((p) =>
    p.type === 'integer' || p.type === 'fraction'
      ? [...p.value].map((d) => {
          const col = document.createElement('span');
          col.className = 'fx-odo__col';                    // column of 0–9 stacked vertically
          col.style.setProperty('--d', 0);                  // inserted at 0 ...
          col.innerHTML = '<span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span>';
          targets.push([col, d]);
          return col;
        })
      : [Object.assign(document.createElement('span'), { textContent: p.value })] // group, decimal, currency stay static
  ));
  // ... and the target is set only after the 0 state has been styled. One frame callback
  // runs before that first style pass, so wait for the following frame.
  requestAnimationFrame(() => requestAnimationFrame(() => {
    for (const [col, d] of targets) col.style.setProperty('--d', d);
  }));
}
```

```css
.fx-odo__visual { font-variant-numeric: tabular-nums; display: inline-flex; }
.fx-odo__col { display: inline-flex; flex-direction: column; line-height: 1.2; block-size: 1.2em; overflow: clip;
  /* each child moves by the digit */ }
.fx-odo__col > span { transform: translateY(calc(var(--d) * -100%)); transition: transform var(--motion-narrative) var(--ease-enter); }
@media (prefers-reduced-motion: reduce) { .fx-odo__col > span { transition: none; } }
```

Pitfalls:

- Use `tabular-nums` (or a monospace digit set) so digits do not change width while counting.
- Freshly inserted columns render at their final `--d` with no transition, which is why the recipe inserts them at `--d: 0` and sets the target on a later frame. When the digit count is unchanged, update `--d` on the existing columns instead of rebuilding them, so each digit rolls from its previous value.
- Native digits (Arabic-Indic, Devanagari and others) cannot roll through a 0–9 column of Latin glyphs; `numberingSystem: 'latn'` keeps the visual copy consistent, while the visually-hidden copy keeps the locale's own digits. If the product must show native digits visually, build each column from that numbering system's ten glyphs instead.
- Format with the user's locale: separators, digit grouping, currency position and native digits vary. `formatToParts()` keeps separators static and rolls only digits.
- No live region on intermediate values. If the update matters (a status change), announce the final value once through an existing status region.
- A ticker that starts when scrolled into view is still automatic motion; keep it short (well under 5 seconds) and run it once.
- Reduced motion: set the final value immediately.

## Version Sources

Moving release pins in this file were resolved 2026-10-20 (Baseline from web-features 3.43.0, browser support from MDN BCD 8.1.6):

- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap ; SplitText options and the 3.13 rewrite from https://gsap.com/docs/v3/Plugins/SplitText ; ScrambleTextPlugin from https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin ; free-licence terms from https://gsap.com/standard-license
- **motion 14.4.0** (verified) — https://motion.dev/changelog
- **split-type 0.3.4** (verified, stale) — https://registry.npmjs.org/split-type ; last publish 2023-10-22
- **`sibling-index()` / `sibling-count()`** — Baseline newly available 2026-08-18; Chrome 138, Firefox 154, Safari 26.2 (verified) — https://web-platform-dx.github.io/web-features-explorer/
- **Registered custom properties (`@property`)** — Baseline 2024-07-09 (verified) — https://github.com/mdn/browser-compat-data
- **`steps()`, `font-variant-numeric: tabular-nums`, `Intl.NumberFormat#formatToParts`** — Baseline widely available (verified) — https://web-platform-dx.github.io/web-features-explorer/
