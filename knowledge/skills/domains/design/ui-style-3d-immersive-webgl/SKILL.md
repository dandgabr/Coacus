---
name: "ui-style-3d-immersive-webgl"
description: "Provides the 3D immersive web design style (2019-present): WebGL/Three.js scenes as first-class marketing and portfolio media, covering scene architecture, scroll-linked cameras, frame budgets, Spline/model-viewer tooling, context-loss handling and canvas accessibility. Use when building hero 3D scenes, product visualizations or evaluating WebGL/WebGPU work."
---

# UI Style: 3D Immersive (WebGL)

Browser-native 3D as a first-class medium: a single hero scene, scroll-linked camera, PBR materials and particles — the Bruno Simon portfolio (2019) and Spline (2020) era, extending into WebGPU. Synthesized from verified research (three.js r186 current); see Sources.

---

## 🧭 When to Activate

- Building hero-level brand moments or product visualizations in WebGL.
- Deciding between full Three.js scenes, Spline embeds and `<model-viewer>`.
- Budgeting frame time, memory and bundle size for 3D pages.

---

## 🕰️ Definition and Timeline

- Foundation: WebGL 1.0 (Khronos, 2011); Three.js (mrdoob, April 2010). The modern era starts when mobile GPUs caught up: Bruno Simon's drivable portfolio (2019), Three.js Journey (2020), Spline (YC S20) making 3D designer-accessible; Apple product pages; igloo.inc. Forward path: WebGPU (`WebGPURenderer`/TSL in three.js r16x+).

---

## 🎨 Visual DNA

- Dark or gradient-mesh backdrops; emissive accents with bloom; soft PBR materials and frosted-glass panels; particle fields; one hero object as centerpiece; depth via camera parallax and depth-of-field; typography floats over the canvas; grain overlays.

---

## 🖱️ Interaction and Motion

- Scroll-scrubbed camera dollies (timeline drives camera position); pointer-follow with frame-rate-independent damping (`lerp(current, target, 1 - exp(-k * dt))`); raycaster hover springs; drag-to-orbit with inertia; canonical eases `easeOutExpo`, `power3.out`; **60 fps budget = 16.67 ms/frame** (8.3 ms at 120 Hz).

---

## 🛠️ Implementation Notes

- Three.js scene graph + `GLTFLoader` (DRACO compression, KTX2 textures); `InstancedMesh` for particles; postprocessing passes (bloom, DOF); render-on-demand instead of continuous loops; pause rendering when the canvas is off-screen (IntersectionObserver); clamp `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- Spline exports a `<spline-viewer>` web component; react-three-fiber/drei for React; `<model-viewer>` (Google) for product 3D without a scene graph.
- Handle `webglcontextlost`/`webglcontextrestored`; browsers cap concurrent contexts (~8–16 — avoid >2–4).

---

## ♿ Accessibility and Performance

- Canvas content is invisible to screen readers: ship 3D as **enhancement over SSR'd HTML** (`aria-hidden` canvas, real content in the DOM); LCP must come from HTML text/image, never the canvas.
- Honor `prefers-reduced-motion` — show a static poster frame instead of camera motion.
- Budgets: core three.js ≈ 150–200 KB gz before your scene; watch iOS Safari memory kills and Lighthouse collapse on heavy scenes.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** hero brand moments, product visualization, portfolios whose product is the medium, award-ambition campaigns.
- **Avoid:** content-first sites, e-commerce catalogs (use `<model-viewer>`), slow-network mobile audiences, B2B utility products.

---

## ⚠️ Pitfalls

- The "Awwwards sameness" critique (dark bg + floating blob + marquee); maintenance risk when the shader author leaves; context loss mid-scroll; per-scene memory ceilings.

---

## 📚 Sources

- three.js (r186 current) — https://threejs.org/
- MDN, "WebGL: 2D and 3D graphics for the web" — https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API
- Spline — https://spline.design/
- Bruno Simon, "Three.js Journey" — https://threejs-journey.xyz/
- Bruno Simon Portfolio (2019) — https://2019.bruno-simon.com/
- Khronos, "WebGL 2.0 Specification", 2017 — https://registry.khronos.org/webgl/specs/latest/2.0/
- `<model-viewer>` — https://modelviewer.dev/

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md), [ui-style-claymorphism](../ui-style-claymorphism/SKILL.md), [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md).
- For performance budgets, see [latency-engineering](../../../engineering/practices/latency-engineering/SKILL.md).
