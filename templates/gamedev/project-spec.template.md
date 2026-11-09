# Project Spec Template

Defines the master world scale, canvas constraints, resolution standards, and art direction baseline for a 2D game project.

```yaml
project:
  title: "Game Title"
  genre: "fighting-game" # fighting-game | platformer | beat-em-up | shooter-sideview | topdown-action

  world_scale:
    pixels_per_meter: 100
    baseline_height_reference_m: 1.75
    baseline_height_px: 175

  canvas:
    cell_width: 256
    cell_height: 256
    origin_y: "bottom"
    safe_margin_y_px: 16
    safe_margin_x_px: 24

  rendering:
    pixel_art: false
    integer_scaling_only: false
    outline_thickness_px: 1
    master_palette_id: "fantasy-standard-64"

  collision_system:
    coordinate_space: "cell-relative"
    precision: "integer"
```
