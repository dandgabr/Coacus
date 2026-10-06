# Chroma Key Selection and Soft-Alpha Unmixing

## The Failure of Hard Chroma Peeling

Traditional naive chroma keying erases pixels whose distance to the key color falls within a threshold, and then strips or "peels" edge boundaries. This destroys:
- Sub-pixel antialiased hair strands.
- Semi-transparent weapon glows and smoke effects.
- 1px dark outlines in pixel art.

## Soft-Alpha Unmixing Model

Instead of binary deletion, decompose boundary transition pixels into foreground RGB and calculated alpha coverage $\alpha \in [0.0, 1.0]$:

$$\alpha = 1.0 - \frac{C_{\text{key}} \cdot (C_{\text{pixel}} - C_{\text{foreground}})}{\|C_{\text{key}}\|^2}$$

Transition pixels close to the key boundary are unmixed into despilled RGB and partial alpha, eliminating colored fringes without eroding silhouette borders.

## Key Selection Strategy

- **Do Not Default Blindly to Magenta**:
  - Warm characters (red hair, pink armor, orange clothing, bronze skin) will suffer boundary erosion under magenta (`#FF00FF`). Use **Pure Green** (`#00FF00`) instead.
  - Cool characters (green clothing, teal scales, olive uniforms) will suffer boundary erosion under green. Use **Magenta** (`#FF00FF`) instead.
  - When characters feature both red and green elements, use a high-contrast tertiary key (such as **Cobalt Blue** `#0000FF` or **Cyan** `#00FFFF`).
