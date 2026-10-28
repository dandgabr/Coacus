---
name: web-3d-object-modeling
description: >-
  Provides procedural editable 3D object modeling for web layouts from text or reference images. Use when constructing parametric objects, reviewing shapes, preparing interactive models, or rendering static page images.
---

# Web 3D Object Modeling

Build reusable objects as editable programs. Establish the intended page size, style, motion and output. Separate visible evidence in an image from assumptions about hidden surfaces; do not promise recovered geometry or CAD precision from one view.

1. Decompose the object into named parts and identify proportions, materials, attachments and moving pivots. Block out major silhouettes before detail.
2. Build a scene-independent factory, documenting options, units, origin and bounds. Return a root object, named parts and a disposal operation. The consuming page owns camera, lights, renderer, controls and animation. Dispose only owned resources.
3. Review front, side and three-quarter views under fixed lighting, then inspect at the intended layout size. Correct silhouette and assembly before fine detail.
4. Deliver editable source and requested interactive integration. Render requested PNG or WebP with recorded camera, lighting, dimensions and background or transparency. Use a fixed seed when generation is stochastic.
5. If GLB is requested, retain the parametric source separately, check materials, reimport and compare visually. GLB does not preserve the authoring program.

Read [modeling and delivery](references/modeling-and-delivery.md) for practical procedures and [research and optional tools](references/research-and-tools.md) for provenance and optional CAD workflows. Use [browser GPU graphics](../ui-gpu-graphics-web/SKILL.md) for rendering lifecycle, performance and accessibility, and [immersive web design](../../../domains/design/ui-style-3d-immersive-webgl/SKILL.md) for composition. Measure asset size, triangles, draw calls and texture costs against project budgets. Retain usable HTML and a poster when graphics are unavailable or motion is reduced.
