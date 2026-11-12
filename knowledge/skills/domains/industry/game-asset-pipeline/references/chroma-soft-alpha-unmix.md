# Chroma Key Selection and Soft-Alpha Unmixing

## Failure of Hard Chroma Peeling

Naive threshold deletion and edge peeling can destroy antialiased hair strands, semi-transparent glows or smoke, and one-pixel outlines. Preserve the original asset and inspect the keyed result over both light and dark backgrounds.

## Soft-Alpha Model and Limits

For source-over compositing against an opaque key, `C = alpha * F + (1 - alpha) * K`, where `C` is the observed RGB, `F` is straight foreground RGB, `K` is key RGB, and alpha is coverage. Use the same compositing domain for all three: normally linear-light RGB, or encoded RGB if the source was actually composited there. Record the domain and whether stored output RGB is straight or premultiplied; premultiplied RGB is `alpha * F`. At alpha zero, straight RGB is not recoverable.

One observed RGB and a key cannot uniquely recover both unknown foreground RGB and alpha: the problem is underdetermined. A deterministic keyer can estimate a matte and despill using explicit assumptions, but cannot guarantee recovery of foreground details, especially when foreground and key colors are similar. Compare with the preserved source and seek artist review.

If both `F` and `K` are independently known, the following least-squares estimate follows from the model. A near-zero denominator is ambiguous, not transparent or opaque by default. The tolerance assumes normalized RGB.

```python
def estimate_alpha(observed, foreground, key):
    delta = [f - k for f, k in zip(foreground, key)]
    denominator = sum(d * d for d in delta)
    if denominator < 1e-12:
        return None
    alpha = sum((c - k) * d for c, k, d in zip(observed, key, delta)) / denominator
    return max(0.0, min(1.0, alpha))
```

Validate known opaque, transparent and half-alpha synthetic patches, including the ambiguous foreground-equals-key case. Recompose estimates over light and dark backgrounds; inspect real edges for halos and lost strands. The equation assumes the stated source-over model, not arbitrary color spill or compression.

Source: [W3C source-over compositing](https://www.w3.org/TR/2024/CRD-compositing-1-20240321/#simplealphacompositing).

## Key Selection Strategy

- Do not default blindly to magenta. Warm characters with red hair, pink armor, orange clothing or bronze skin may be better separated from green.
- Cool characters with green clothing, teal scales or olive uniforms may be better separated from magenta.
- When characters feature red and green elements, consider a contrasting tertiary key such as cobalt blue or cyan. Check actual edges and lighting; no key color guarantees separation.
