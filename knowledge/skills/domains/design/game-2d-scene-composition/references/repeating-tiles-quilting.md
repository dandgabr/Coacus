# Repeating Tiles and Quilting Seams

## Repeating Texture Generation

For horizontal or vertical scrolling backdrops (ground strips, brick walls, skies, water surfaces), repeating textures must loop seamlessly without visible boundaries.

## Minimum Error Quilting Algorithm

When generating or joining repeating tile chunks of period $P$ with overlap margin $O$:

1. **Overlap Error Surface**: Compute the squared color difference between the left overlap strip and the right overlap strip:
   $$E(x, y) = \|I_{\text{left}}(x, y) - I_{\text{right}}(x, y)\|^2$$
2. **Dynamic Programming Cut**: Trace the path of least cumulative error from top to bottom across the overlap zone.
3. **Alpha Seam Blending**: Blend the boundary pixels smoothly along the calculated minimum error path rather than a straight vertical line.
4. **Verification**: Inspect two adjacent repeated copies at $1\times$, $2\times$, and $4\times$ zoom to verify that repeating patterns, high-frequency noise, or architectural edges do not produce noticeable rhythm artifacts.
