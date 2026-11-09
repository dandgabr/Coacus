# Refraction and Chromatic Dispersion Shaders

Depth reference for the "Refraction and Chromatic Dispersion" section of [the GPU graphics skill](../SKILL.md). The visual style, its gate and its CSS fallback chain are owned by the [glassmorphism refraction dialect](../../../../domains/design/ui-style-glassmorphism/references/refraction-dialect.md); this file covers only the GPU path.

---

## 1. Pipeline

1. **Capture the background** into a texture: a WebGL/WebGPU scene you already render (best case: render it to an offscreen target), a `<video>` or `<img>` uploaded as a texture, or a rasterized snapshot of the page region.
2. **Describe the lens surface** with a signed distance field (SDF) of the control shape, for example a rounded rectangle. The SDF gradient near the rim is the surface normal; its magnitude falls to zero in the flat centre.
3. **Offset the lookup:** sample the background at `uv + normal.xy * strength * rimFalloff`. A refraction index is optional; a hand-tuned strength reads the same at UI scale.
4. **Disperse per channel:** sample red, green and blue with slightly different offsets (for example 1.0, 1.015 and 1.03 times the base offset) to fake chromatic aberration at the rim. Keep the spread small; wide fringes read as a rendering bug.
5. **Composite** a tint layer (the readable "Tinted" surface) and a specular rim on top, then output.

## 2. Fragment Sketch (GLSL ES 3.0)

```glsl
#version 300 es
precision highp float;
uniform sampler2D uBackground;   // captured backdrop
uniform vec2  uSize;             // control size in px
uniform float uRadius, uStrength, uDispersion, uTint;
in vec2 vUv; out vec4 outColor;

float sdRoundRect(vec2 p, vec2 b, float r) {
  vec2 q = abs(p) - b + r;
  return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}

void main() {
  vec2 p = (vUv - 0.5) * uSize;
  float d = sdRoundRect(p, uSize * 0.5, uRadius);
  vec2 e = vec2(1.0, 0.0);
  vec2 n = normalize(vec2(
    sdRoundRect(p + e.xy, uSize * 0.5, uRadius) - sdRoundRect(p - e.xy, uSize * 0.5, uRadius),
    sdRoundRect(p + e.yx, uSize * 0.5, uRadius) - sdRoundRect(p - e.yx, uSize * 0.5, uRadius)));
  float rim = smoothstep(-24.0, 0.0, d);            // 0 in the centre, 1 at the edge
  vec2 off = n * uStrength * rim / uSize;
  float r = texture(uBackground, vUv - off * (1.0)).r;
  float g = texture(uBackground, vUv - off * (1.0 + uDispersion)).g;
  float b = texture(uBackground, vUv - off * (1.0 + 2.0 * uDispersion)).b;
  vec3 col = mix(vec3(r, g, b), vec3(1.0), uTint);  // tint raises legibility
  outColor = vec4(col, step(d, 0.0));
}
```

The WGSL port is mechanical: `textureSample(bg, samp, uv)` per channel, the same SDF, and a uniform buffer for the parameters. Prefer an analytic normal over finite differences when the shape is fixed.

## 3. Constraints

- **Snapshots break live DOM.** A captured page region does not update with text selection, focus rings, hover states, form input, video frames or scroll unless you recapture it, and recapture per frame is too slow. Use the shader only over a background you already own on the GPU (a canvas scene, a video texture); over live HTML prefer the CSS blur.
- **Cost:** Every pixel of the control samples the background three times plus the tint. Clamp device pixel ratio, render on demand when the backdrop is static, and stop the loop when the canvas leaves the viewport. Continuous refraction on a full-width bar measurably drains battery on mobile.
- **Context loss:** On `webglcontextlost` or `device.lost`, remove the canvas from view and fall back to the CSS glass surface (opaque default, plain blur where supported) until the context is restored and resources are rebuilt. The control must stay usable with no GPU at all.
- **Reduced transparency:** Under `prefers-reduced-transparency: reduce` (Chrome 118, Firefox 113, not Safari), skip the shader and render the opaque surface. Because Safari lacks the query, the tinted default must already pass contrast.
- **Reduced motion:** Under `prefers-reduced-motion: reduce`, freeze any specular or wobble driven by pointer, scroll or device orientation; a static refraction frame is acceptable.
- **Contrast:** Text never renders inside the shader. Keep labels in HTML above the canvas and measure them against the worst refracted frame.

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **prefers-reduced-transparency: Chrome 118, Firefox 113, no Safari** (verified) — MDN browser-compat-data 8.1.6 (2026-10-15)
- **GLSL ES 3.0 (WebGL 2.0)** (verified) — Khronos Group, WebGL 2.0 Specification
