# Loop Repair and RIFE Frame Interpolation

## Locomotion Cycle Discontinuity ("Seam Pop")

When cyclic actions (walk, run, crawl) are generated as video clips or sequential frames, the final frame rarely loops seamlessly back into the first frame. This creates an observable pop or hitch:
- Foot sliding or backward teleportation on the ground plane.
- Head or prop trajectory discontinuity.

## Neural In-Betweening and Seam Healing

1. **Cycle Periodicity Estimation**: Measure frame-to-frame optical flow or alpha-weighted centroid trajectories to identify the candidate cycle window $[F_{\text{start}}, F_{\text{end}}]$.
2. **RIFE Neural Interpolation**: Synthesize missing intermediate frames between the loop seam boundaries using RIFE (Real-Time Intermediate Flow Estimation) to ensure smooth velocity transitions.
3. **Contact-Point Locking**: Pin the strike foot's horizontal position during its contact phase to guarantee zero foot-sliding across ground surfaces.
4. **Duration Standardization**: Ensure all locomotion directions (facing left, right, front, 45°) share identical frame counts and cycle durations before atlas packaging.
