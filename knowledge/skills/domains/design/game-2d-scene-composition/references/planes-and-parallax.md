# Planes, Parallax, and Viewport Layers

## Scene Plane Taxonomy

To construct immersive 2D game scenes, organize elements along distinct virtual depth planes with relative scroll velocities:

```text
[FAR SKY]       z: 0.1   velocity: 0.05x   (Clouds, celestial bodies, distant mountains)
[MIDGROUND]     z: 0.5   velocity: 0.40x   (City skyline, tree lines, architectural backdrops)
[GAMEPLAY]      z: 1.0   velocity: 1.00x   (Characters, obstacles, interactive terrain, shadows)
[FOREGROUND]    z: 1.5   velocity: 1.30x   (Out-of-focus pillars, foliage framing, environmental fog)
```

## Parallax Scrolling Mathematics

The camera tracks a world coordinate $(C_x, C_y)$. The screen rendering position $(S_x, S_y)$ of an element located at $(W_x, W_y)$ on plane $i$ is calculated as:

$$S_x = (W_x - C_x) \times V_{x,i} + O_x$$
$$S_y = (W_y - C_y) \times V_{y,i} + O_y$$

Where:
- $V_{x,i}$ is the velocity factor of plane $i$.
- $(O_x, O_y)$ is the screen origin / viewport center.

## Z-Sorting Rules within Gameplay Plane

When multiple actors and scene props share the gameplay plane ($z = 1.0$):
1. **Y-Sorting Anchor**: Sort render order using the actor's ground contact anchor ($Y_{\text{foot}}$). Lower screen Y renders in front of higher screen Y.
2. **Depth Scale Compensation**: In top-down or 2.5D games, actors walking toward the top of the screen should only scale down if the camera uses perspective projection rather than orthographic rendering.
