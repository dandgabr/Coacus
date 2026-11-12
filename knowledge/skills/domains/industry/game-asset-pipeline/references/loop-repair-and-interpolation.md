# Loop Repair and RIFE Frame Interpolation

## Locomotion Cycle Discontinuity ("Seam Pop")

A cyclic walk, run or crawl may show a pop at the wraparound cut, including a foot teleport or a discontinuous head or prop trajectory. Review playback at the intended speed before changing authored motion. One-shot clips do not need loop repair.

## Optional Seam Healing

1. **Cycle Periodicity Estimation**: Measure optical flow or alpha-weighted centroid trajectories to identify a candidate cycle window. Respect intentional holds and per-frame durations.
2. **Optional In-Betweening**: If a visible seam needs repair, consider hand editing or neural interpolation such as RIFE. Inspect interpolated silhouettes, props, occlusions and pixel-art edges; interpolation can introduce artifacts and is not a guarantee of smooth velocity. Obtain artist approval.
3. **Contact-Point Review**: Check stance-foot position in world space, accounting for entity movement, pivots and camera transforms. Local foot motion may be needed to keep the foot planted. Preserve deliberate stylization.
4. **Direction Timing**: Preserve authored frame counts, durations, asymmetric timing and one-shot events. Normalize directions only if a specific runtime or design requirement calls for it, with artist approval and playback QA.
