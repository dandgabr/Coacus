# CSS and SVG Compositing

Use masks to control where a layer paints and SVG filter graphs to combine derived pixels. Place effects on a decorative pseudo-element or a separate SVG overlay. Keep text, the base outline, keyboard focus and pointer hit testing on the original element. If clipping hides actual content, use the [reveal and collapse guidance](reveal-collapse-loading.md) to keep its interaction state aligned.

## Construct a two-layer cutout

List the full outer surface first and the inset hole second. The first layer is the source, and the lower layer is the destination. With `mask-composite: subtract`, the source survives only where the destination is transparent. Choose `intersect` to keep their overlap or `exclude` to keep the nonoverlapping parts of both layers. An opaque outer shape and a fully opaque inset use `subtract` to form a ring.

```css
.control {
  position: relative;
  border: 2px solid currentColor;
}
@media (forced-colors: none) {
  @supports (mask-composite: subtract) and (mask-mode: alpha) {
    .control::before {
      content: "";
      position: absolute;
      inset: 5px;
      padding: 8px;
      pointer-events: none;
      background: var(--decorative-gradient);
      mask-image: linear-gradient(black, black), linear-gradient(black, black);
      mask-mode: alpha, alpha;
      mask-repeat: no-repeat;
      mask-origin: border-box, content-box;
      mask-clip: border-box, content-box;
      mask-composite: subtract;
    }
  }
}
```

- **Alpha** uses opacity, so opaque black and opaque white both cover the mask layer. **Luminance** multiplies luminance by alpha, so opaque white covers and opaque black contributes zero coverage. For the same cutout using luminance, use white for both the outer mask and the inset. Gray in the inset leaves partial source coverage.
- Set each layer's mode explicitly. The default `match-source` uses alpha for image sources and normally uses luminance for an SVG `<mask>` reference. A URL ending in an SVG filename as an image is distinct from a URL fragment that references an SVG `<mask>`.
- Paint the ordinary outline separately from the enhancement. The masking specification treats an unavailable source as transparent black. The assembled mask can still paint unexpectedly when a URL fails. For a required external layer, enable the assembled effect only after the image decodes, as in the example. Keep a system-color focus outline outside the masked layer. A painted hole does not make a CSS mask's host click-through.

## Generate clipped specular relief

Keep a flat emblem as the base. Render a second copy with a filter that outputs only the lit highlights. Use named results for the graph:

1. `feGaussianBlur` reads `SourceAlpha` and produces `rounded`, the height map with softened edges.
2. `feSpecularLighting` reads `rounded` and produces `shine`. Set the light direction and surface scale in the same coordinate system as the drawing.
3. `feComposite` with `operator="in"` keeps `shine` only where the original `SourceAlpha` exists. Paint that result over the flat base. If the graph must return a complete emblem, merge the base and clipped highlights with `feMerge`.

Set `filterUnits` and `primitiveUnits` deliberately. The example uses `userSpaceOnUse` for both, and its filter region provides a margin around a seal drawn within a fixed view box. Tight bounds can clip light or blur. Oversized bounds increase the filtered area. Verify a lit edge, a flat interior and a pixel outside the silhouette. Reserve expensive filter graphs for small surfaces and profile before animating them.

## Check the paints and interaction

Serve [compositing.html](../examples/compositing.html) over HTTP. The luminance sample uses a local SVG image. Compare the alpha and luminance rings and the seal at a narrow and a wide viewport, at device pixel ratios 1 and 2. Sample the ring edge, the cleared interior, the normal outline and the lit edge. Add `?plain` to suppress the enhancement, then block `compositing-mask.svg` and confirm that the luminance link still has an outline, label and the same clickable area. Tab to every link with forced colors active and confirm the focus outline survives.

## Compatibility sources

Reviewed 2026-11-27. Unprefixed `mask-composite` is documented in Chrome 120, Firefox 53 and Safari 15.4. The prefixed property uses different operators. Test the exact source and mode, especially an SVG `<mask>` fragment and default `match-source` in Safari. The specular primitives use standard SVG filter syntax. Verify pixels on each target engine because a supported property can still paint a different result. [MDN browser-compat-data 8.1.11](https://www.npmjs.com/package/@mdn/browser-compat-data/v/8.1.11), [CSS Masking](https://www.w3.org/TR/css-masking-1/#the-mask-composite), [Filter Effects](https://www.w3.org/TR/filter-effects-1/#FilterPrimitivesOverview).
