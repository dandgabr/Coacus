# Period GUI Appearance: Workbench-Inspired Light Adaptation

Use this branch when the user requests a light retro desktop. Choose the reference era explicitly; a phosphor terminal and a windowed Workbench desktop are different dialects. Do not retain black CRT panels with inherited dark ink merely because the parent skill defaults to a terminal.

## Source and scope

The AmigaOS manual describes Workbench through screens, menus, windows, gadgets, icons and requesters. It describes selected window frames changing color and gadgets appearing raised or depressed. Those interaction and material cues support a desktop adaptation. They do not establish one exact palette for every Workbench release.

Primary documentation: [AmigaOS Manual: Workbench Fundamentals](https://wiki.amigaos.net/wiki/AmigaOS_Manual:_Workbench_Fundamentals), sections Windows and Gadgets, accessed 2026-10-19. Verify release-specific screenshots or manuals before calling a palette an exact historical reproduction. The values below are a proposed accessible adaptation, not sampled historical colors.

## Light material recipe

Use opaque pale gray window interiors, dark ink, thin contrasting frames, squared controls and a restrained blue selection role. Keep raised/recessed edge pairs and visible selected versus inactive window chrome. Example roles:

```css
.period-desktop {
  --period-canvas: #b8bec7;
  --period-surface: #eeeeee;
  --period-ink: #151515;
  --period-rule: #4b5058;
  --period-selection: #23477d;
  --period-on-selection: #ffffff;
  --period-edge-light: #ffffff;
  --period-edge-dark: #60656c;
  background: var(--period-canvas);
  color: var(--period-ink);
  accent-color: var(--period-selection);
}
.period-window {
  background: var(--period-surface);
  color: var(--period-ink);
  border: 1px solid var(--period-rule);
  padding: clamp(1rem, 3%, 2rem);
}
.period-button {
  background: var(--period-surface);
  color: var(--period-ink);
  border: 2px solid;
  border-color: var(--period-edge-light) var(--period-edge-dark) var(--period-edge-dark) var(--period-edge-light);
}
.period-button:active { border-color: var(--period-edge-dark) var(--period-edge-light) var(--period-edge-light) var(--period-edge-dark); }
.period-button:focus-visible { outline: 2px solid var(--period-selection); outline-offset: 3px; }
```

Map title, description, table, input, placeholder, disabled and checked roles together. A sprite or logo needs its own meaningful ink/backing pair; opaque black artwork cannot be repaired by changing inherited text color. Preserve selectable semantic text and ordinary keyboard behavior rather than recreating every historical mouse gesture.

## CRT decoration is optional

A light desktop does not require green glow or scanlines. If period display texture is requested, declare viewport versus complete-content ownership, keep it decorative and pointer transparent, and verify top/middle/bottom at both wide/short and narrow/tall sizes. Check the resulting text composite; do not count bloom as readable ink.
