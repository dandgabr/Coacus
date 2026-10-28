# Modeling and delivery

Specify subject, reference, intended view, dimensions, materials, interaction, output and visual constraints. Identify uncertainty in hidden surfaces. Construct simple primitives and profiles, use meaningful part names and local transforms, and locate pivots at their hinges. Expose dimensions and colors as parameters; changing one part should preserve unrelated attachments. Use a deterministic seed for stochastic detail.

For a repeated-parts example, make a stylized desk lamp from a base, articulated arm and shade. Parameterize height and color, place the arm pivot at the base hinge, and keep the shade attached when the arm rotates. For an image-guided example, reconstruct a stylized object from an authorized reference: record observed silhouette and colors separately from assumptions about the rear, then compare front, side and three-quarter renders.

The [lamp and mug demonstration](../examples/lamp-and-mug.html) provides an interactive factory and PNG export; the mug uses its linked front-view reference and infers depth. It is a stylized construction, not an image-reconstruction evaluation. Serve it over HTTP and provide network access for its pinned Three.js dependency (0.180.0, verified 2026-10-28 against the [npm registry](https://registry.npmjs.org/three/0.180.0)).

An object factory can expose `{ root, parts, dispose }`; supply an `update` function only for animation. Document owned and borrowed resources. A page owns its renderer and presentation. Verify repeated mount and teardown for unexplained resource growth rather than assuming renderer caches reach zero.

Render PNG or WebP at specified dimensions with recorded camera, lighting, background and transparency. Check it at intended display size. Use it as a fallback where suitable, but deliver the image itself when requested. For optional GLB export, preserve source, verify supported materials and animation, reimport and compare appearance; report unsupported effects.

Sources reviewed 2026-10-28: [Three.js GLTFExporter](https://threejs.org/docs/pages/GLTFExporter.html), [Three.js disposal](https://threejs.org/manual/pages/how-to-dispose-of-objects.html), [glTF Validator](https://github.com/KhronosGroup/glTF-Validator), [model-viewer loading](https://modelviewer.dev/examples/loading/).
