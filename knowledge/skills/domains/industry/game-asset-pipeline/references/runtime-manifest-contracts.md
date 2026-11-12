# Runtime Manifest Contracts and Engine Integration

## Runtime Source of Truth (`manifest.json`)

Store one record per stable logical frame ID: atlas page and pixel rectangle, original canvas size, trim offset from the canvas top-left, pivot in source-canvas pixels from that same origin, and rotation direction. Rectangles use `[x, y, width, height]`; offsets and pivots use `[x, y]`. Reconstruct by unrotating if necessary and placing the atlas rectangle at the trim offset on a transparent source canvas. Apply the pivot after reconstruction. Multiple IDs or animation steps may refer to the same packed pixels.

An empty frame has `page` and `rect` set to `null`, no pixels, a zero trim offset, and still retains its source size and pivot. An animation step holds a frame ID and a positive duration in milliseconds; repeated IDs preserve the timing of deduplicated images. `loop` wraps to the first step; `once` plays in order and holds the last frame until changed. An adapter must implement or explicitly report differences in end behavior.

This illustrative custom manifest describes a two-pixel atlas, not a guaranteed engine import format:

```json
{
  "pages": [{"image": "atlas.png", "width": 2, "height": 1}],
  "frames": {
    "a": {"page": 0, "rect": [0, 0, 1, 1], "source_size": [3, 2], "trim_offset": [1, 0], "pivot": [1, 2], "rotation": "none"},
    "b": {"page": 0, "rect": [1, 0, 1, 1], "source_size": [3, 2], "trim_offset": [2, 1], "pivot": [1, 2], "rotation": "none"},
    "empty": {"page": null, "rect": null, "source_size": [3, 2], "trim_offset": [0, 0], "pivot": [1, 2], "rotation": "none"}
  },
  "animations": {
    "walk": {"playback": "loop", "steps": [{"frame": "a", "duration_ms": 100}, {"frame": "b", "duration_ms": 200}, {"frame": "a", "duration_ms": 100}, {"frame": "empty", "duration_ms": 50}]},
    "attack": {"playback": "once", "steps": [{"frame": "b", "duration_ms": 200}, {"frame": "a", "duration_ms": 100}]}
  }
}
```

Validate rectangles and trim placement against each actual page and canvas, rotation-aware dimensions, pivot conventions, positive durations and all references. This rectangular contract must not use tight packing: it carries no polygon or mesh geometry. Disable rotation unless the target importer supports it; if supported, explicitly declare the rotation direction and implement its inverse. Test two offset-trimmed frames by reconstructing source pixels and pivot registration; include duplicate and empty frames.

## Legacy `frame_layout` compatibility

The earlier single-sheet grid contract remains valid for existing readers. Its absolute `x`, `y`, `w`, `h` rectangles are sheet pixels; `anchor_x` and `anchor_y` are source-cell-relative pixels. Preserve the surrounding sheet dimensions, cell dimensions and animation row settings when emitting this shape:

```json
{
  "game_input": "sprite-sheet-alpha.png",
  "sheet_width": 2048,
  "sheet_height": 2048,
  "cell_width": 256,
  "cell_height": 256,
  "animation": {"rows": {"idle": {"row": 0, "frames": 1, "fps": 10, "loop": true}}},
  "frame_layout": {"rows": {"idle": [{"x": 0, "y": 0, "w": 256, "h": 256, "anchor_x": 128, "anchor_y": 240}]}}
}
```

The new example is a different custom shape, not a drop-in replacement. For a legacy grid, map each rectangle to page 0, use the cell size as `source_size`, zero trim offset, its anchor as `pivot`, `rotation: none`, and `1000 / fps` milliseconds per step. Map `loop` to playback. Preserve the original `frame_layout` for legacy consumers. Trimmed, rotated, multipage, empty or variable-duration frames cannot generally round-trip to the old grid contract; use an explicitly updated adapter rather than silently discarding information.

## Sampling and Packing

Padding separates frames; extrusion copies their edge texels into a surrounding border. They are distinct from sheet-border padding. For deliberately crisp pixel art use nearest filtering and appropriate integer scaling. For filtered or minified art, extrude edges and choose gutters for the target renderer and mip levels; one pixel is not universally mip-safe. Test high-contrast neighbors at fractional positions, scales and minification. Validate every page against actual device texture-size limits and choose mipmap and filtering settings per renderer.

## Engine Adapters

- **Aseprite / JSON**: Preserve `frame`, `spriteSourceSize`, `sourceSize`, durations and tags. Export options can trim frames and merge duplicates; translate their metadata instead of assuming identical loader formats.
- **Godot (`SpriteFrames`)**: Map each step, duration, playback mode and region through an adapter. At playback speed 1, relative duration equals source duration in seconds multiplied by animation FPS; at another nonzero speed, multiply by its absolute value if preserving the same wall-clock duration. Confirm target behavior.
- **Unity and other engines**: Translate regions, trim offsets and source-space pivots into the target's documented coordinate system. Disable unsupported rotations and do not use tight packing with this rectangular contract. Do not assume this custom JSON or an Aseprite export loads unchanged in Phaser, Flame, PixiJS, Godot or Unity.

When only fixed FPS is available, specify rounding and minimum-frame policy, report timing error, and test unequal holds, one-shot and looping end behavior in the actual target. Do not silently discard timing.

Sources: [Aseprite trimming](https://community.aseprite.org/t/checking-trim-in-export-sprite-sheet-window-cause-the-sprite-to-move-in-the-sheet/1248), [Aseprite CLI](https://www.aseprite.org/docs/cli/), [Godot SpriteFrames documentation, 4.4](https://docs.godotengine.org/en/4.4/classes/class_spriteframes.html), and [Unity atlas settings, 6.2](https://docs.unity3d.com/6000.2/Documentation/Manual/sprite/atlas/sprite-atlas-reference.html) (version-specific, retrieved 2026-11-11).
