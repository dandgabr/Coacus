# Motion Continuity and Frame Arc Verification

## Physical Trajectory Continuity

Every animation frame represents a slice of physical motion. To ensure visual fluidity and prevent disorientation:

1. **Center-of-Mass Parabola**: During jumping or launching animations, plot the trajectory of the pelvis/center of mass across sequential frames. The curve must describe a smooth arc without horizontal or vertical hitches.
2. **Spacing and Acceleration (Slow In & Slow Out)**: Keyframes must reflect acceleration and deceleration. Startup frames cluster closely together, active strike frames exhibit wide spacing, and recovery settles back into dense clustering.
3. **Smear Frame Validation**: If high-speed action uses smear frames or motion trails, ensure the smear aligns strictly with the direction of the limb's velocity vector.
