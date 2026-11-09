# Seam Pop and Stride Measurement

## Locomotion Cycle Testing

A locomotion cycle is only game-ready when it loops indefinitely without perceptual disruption:

1. **Seam Pop Testing**: Play the looped animation continuously at target game framerate ($12\text{ fps}$, $24\text{ fps}$, or $60\text{ fps}$). Observe the head top and weapon tip at the wraparound cut frame ($F_{\text{last}} \to F_0$). A jump exceeding 2 pixels indicates an unclosed cycle requiring retake or in-betweening.
2. **Foot Strike Ground Pinning**: The lead foot must make contact and stay anchored at a constant horizontal position while the torso translates forward. Zero foot-sliding across ground pixels during the stance phase is mandatory.
3. **Stride Measurement Metric**: Calculate the stride length $L_{\text{stride}}$ in world pixels:
   $$L_{\text{stride}} = X_{\text{strike,right}} - X_{\text{strike,left}}$$
   Record this value in the runtime metadata to synchronize game engine movement velocity with the visual footwork rate.
