# Color Font Effects

Use this recipe when color belongs inside a letterform or icon and the source should remain native text. Read the [palette specimen](../examples/color-font.html) for a working light and dark appearance. Use CSS text color for single-fill text.

## Choose the asset and palette together

1. Check that the licensed font contains the needed glyphs and a color table appropriate to the target. COLR describes paint per glyph, and CPAL provides the entries those paints can reference. A font can reference the current text color or bake in parts of its artwork. A custom palette changes the referenced entries only.
2. Declare a readable system or outline face first. Use `tech(color-COLRv1)` in the color font source. Check the technology and CSS palette property independently. Keep the outline face in the final stack for missing glyphs and an unavailable resource.
3. Name one palette per semantic surface with `@font-palette-values`. Inspect the font palette indices before assigning colors. Recheck paint over the actual background, including a gradient's endpoints and overlapping fills that define the silhouette. An engine can paint COLR and parse a custom palette while still drawing the font's default palette. Use an asset whose default colors are readable on the intended surfaces, or choose an outline font on an unverified surface.
4. In forced colors, use the outline face and system text color if font paints would override user-selected colors. Keep the heading or label as real HTML text in every mode. Use normal wrapping and let the box grow.

Check the accessibility tree and rendered pixels independently. Tokens and parsed declarations cannot establish that a color glyph painted.

## Exercise the fallback

- Compare both example surfaces with the font loaded and its request blocked. Check the displayed letters, heading name, selection and native wrapping.
- Set a longer translated phrase at 320 CSS pixels and at 200% zoom. Compare before and after font readiness. Let text wrap without clipping. Measure nearby control displacement if the product sets a layout target.
- Emulate forced colors and inspect the restored system text fill. For icons whose meaning depends on color, supply a text label or other semantic cue.
- Render a monochrome variant for targets that lack the font technology or the CSS palette property. Verify browser support for each capability before deploying.

## Sources and asset

Reviewed 2026-11-27. [OpenType COLR specification](https://learn.microsoft.com/en-us/typography/opentype/spec/colr) and the [CSS Fonts palette specification](https://www.w3.org/TR/css-fonts-4/#font-palette-prop) define paint and palette behavior. [Chromium color-font examples](https://developer.chrome.com/blog/colrv1-fonts) and the [WebKit standards discussion](https://github.com/WebKit/standards-positions/issues/415) document implementation context.

The example uses a renamed Latin subset of [Nabla from Google Fonts](https://github.com/google/fonts/tree/5026800714d07231937d92eb4cceabf06e05d74e/ofl/nabla), created from the pinned TrueType source. The subset preserves the COLR table and removes the separate SVG paint table so the example exercises COLR paint. Its default palette is adjusted for the example's large text on both surfaces. The example package includes its [font license](../examples/assets/OFL.txt). The specimen itself is authored for Coacus.
