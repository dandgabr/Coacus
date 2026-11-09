# Runtime Manifest Contracts and Engine Integration

## Runtime Source of Truth (`manifest.json`)

Game engines consume exact rectangular bounding boxes rather than guessing frame coordinates via alpha scanning at runtime:

```json
{
  "game_input": "sprite-sheet-alpha.png",
  "sheet_width": 2048,
  "sheet_height": 2048,
  "cell_width": 256,
  "cell_height": 256,
  "animation": {
    "rows": {
      "idle": { "row": 0, "frames": 6, "fps": 10, "loop": true },
      "walk": { "row": 1, "frames": 8, "fps": 12, "loop": true },
      "attack_light": { "row": 2, "frames": 5, "fps": 15, "loop": false }
    }
  },
  "frame_layout": {
    "rows": {
      "idle": [
        { "x": 0, "y": 0, "w": 256, "h": 256, "anchor_x": 128, "anchor_y": 240 },
        { "x": 256, "y": 0, "w": 256, "h": 256, "anchor_x": 128, "anchor_y": 240 }
      ]
    }
  }
}
```

## Engine Adapters

1. **Aseprite / JSON Array**: Direct export into standard Aseprite frame tags, natively compatible with Phaser, Flame, and PixiJS spritesheet loaders.
2. **Godot Engine (`SpriteFrames`)**: Generates matching resource manifests with defined FPS, loop flags, and texture slice regions.
3. **Unity 2D Sprite Atlas**: Exports sliced multi-sprite texture metadata with preset pivot points (`bottom-center`).
