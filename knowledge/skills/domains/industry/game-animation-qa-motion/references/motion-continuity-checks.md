# Motion Continuity and Frame Arc Verification

## Trajectory and spacing

1. **Trajectory agreement**: Plot the pelvis or center of mass across frames and compare it with the controller's intended trajectory and timing. Investigate unintended hitches; deliberate holds, stylized motion and changes in acceleration are not defects by themselves. A parabola is appropriate only for the relevant constant-gravity ballistic segment, not every jump, fall or recoil. For example, [Celeste's creator describes reduced gravity near a held jump's apex](https://www.maddymakesgames.com/articles/celeste_and_forgiveness/).
2. **Spacing and acceleration**: Inspect frame spacing against the intended acceleration, deceleration and action timing. Slow-in and slow-out are useful choices, not mandatory for every action.
3. **Smear frames**: Check that smears and trails communicate the intended limb motion and remain readable at gameplay speed.
4. **Impact timing**: Compare the collision event, impact pose, any hold and recovery in the running game. For input and clock interactions, consult [controller and game feel](../../../design/game-sprite-design/references/controller-and-game-feel.md).
