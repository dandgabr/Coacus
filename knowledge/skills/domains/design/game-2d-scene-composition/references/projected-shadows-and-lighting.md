# Projected Shadows and Directional Lighting

## Shadow Matrix Projection

Real-time or pre-baked 2D projected shadows transform the actor's silhouette using affine transformation parameters based on the scene's light source:

- **Squash Factor ($S_y$)**: Compresses the shadow vertically to simulate surface angle (e.g., $0.25$ to $0.40$ for oblique sunlight).
- **Shear Factor ($K_x$)**: Skews the shadow horizontally based on the light azimuth angle (e.g., $-0.8$ for morning sun, $+0.8$ for afternoon sun).
- **Anchor Point**: The bottom center contact point ($X_{\text{foot}}, Y_{\text{foot}}$) remains pinned; transformation applies outward from this origin.
- **Color and Opacity**: Dark desaturated tone (e.g., `rgba(20, 15, 30, 0.45)`) blended via multiply against the ground plane.

```text
Actor Sprite:       Light Source (Left High)
     O                     \
    /|\                     \
    / \                      \
Ground Line ----------------- v ------------------
Contact Anchor: *===========> (Cast Shadow skewed right)
```

## Lighting Consistency Checklist

1. **Uniform Light Direction**: All foreground actors and midground architecture must receive key light from the same vector.
2. **Contact Shadow Pinning**: Ensure airborne actors raise their feet above their ground shadow, with the cast shadow scaling down and blurring as elevation increases.
3. **Ambient Occlusion Gradients**: Characters in crouched or ground-hugging poses produce intensified contact shadow density directly beneath their hips/knees.
