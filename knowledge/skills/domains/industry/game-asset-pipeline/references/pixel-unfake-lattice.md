# Pixel Unfake and Backbone Lattice

## The Pixel Art Inconsistency Problem

When AI image generators or raster scalers produce "pixel art", the output often exhibits mixed-resolution artifacts:
- Uneven block sizes (e.g., 2.3px wide pixels alongside 3.1px pixels).
- Rotational sub-pixel blurring that destroys 1px hard outlines.
- Jittering edges across animated sequence frames.

## Backbone Lattice Recovery Pipeline

The Backbone Lattice workflow restores authentic integer-grid pixel art:

1. **Fractional Pitch Detection**: Compute the spatial autocorrelation and edge-gradient frequency across the image. The true block pitch $p$ is measured as a float (e.g., $p = 16.4\text{ px}$).
2. **Optimal Phase Locking (`_best_phase`)**: Sweep the offset grid phase $(x_0, y_0)$ from $0$ to $p-1$ to locate the alignment that maximizes color uniformity within grid cells.
3. **Median-Cut Palette Quantization**: Cluster the colors into a restricted run-wide palette (e.g., 16, 32, or 64 colors) to eliminate frame-to-frame color shimmer.
4. **Alpha Binarization**: Set $\alpha = 0$ for background cells and $\alpha = 255$ for character cells. Avoid intermediate transparency in classic 8-bit/16-bit styles.
5. **Integer Nearest Upscale**: Upscale the snapped low-resolution logical matrix to the target atlas cell size using an exact integer factor ($S = H_{\text{cell}} // H_{\text{logical}}$).
