# Seam Pop and Stride Measurement

## Locomotion Cycle Testing

1. **Seam Pop Testing**: Play the loop continuously at its intended speed. Compare the head, weapon tip and silhouette across the wraparound with neighboring transitions, accounting for each frame's duration and intentional holds. Compare displacement and velocity at the sprite's actual scale; a pixel threshold is a project-specific warning heuristic, not a universal failure.
2. **Foot Strike Ground Pinning**: Measure contact in world space after applying the per-frame pivot, entity translation and any camera transform needed to convert screen measurements. A planted foot on a moving entity usually travels backwards in sprite-local space. For a moving support, measure the planted foot relative to the support, accounting for its translation and rotation; stationary world coordinates are not the correct target. Check for visible sliding during stance rather than imposing a fixed local coordinate; allow artist-reviewed stylization.
3. **Stride Measurement**: Measure stride in world units with the chosen strike landmarks and coordinate convention recorded. Synchronize movement speed with the visual contact cadence where the design requires it. Test in-place and root-motion clips at multiple world speeds and record acceptable exceptions.
