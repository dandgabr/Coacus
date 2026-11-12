# Controller Timing and Game Feel

Use this reference when character poses must agree with controller state, input forgiveness or impact feedback. These are design choices to tune through playtesting, not universal durations.

## Input intent and grace

Define separate configurable windows for time since leaving a grounded state (coyote time) and recent jump intent (input buffering). Specify whether each window includes its boundary, which states are eligible, and which rule takes priority when both apply. Define whether releasing the button cancels the buffer and which clock advances each window during pause or hit stop. Consume an accepted intent once; clear or deliberately retain it on death, respawn and state changes. Define moving-platform momentum separately. Corner correction and collision tolerance must respect hazard rules, one-way platforms and the intended challenge.

Test presses just inside, at and outside each boundary. Test presses before landing, releases before landing, overlapping windows and duplicate consumption. Also test moving platforms, death, respawn and pause. Compare outcomes at different render rates with the same simulation inputs and timing. [Celeste's creator](https://www.maddymakesgames.com/articles/celeste_and_forgiveness/) describes held-input buffering, coyote time, corner correction and platform momentum as that game's choices. [Disc Room's developer](https://jwaaaap.substack.com/p/disc-room-game-feel) describes spatial and temporal collision tolerance with explicit exceptions; neither example establishes a default window for another game.

## Impact timeline and clocks

Specify startup, active collision, hit registration, optional impact hold and recovery as one timeline. Choose what advances during hit stop: actor animation and movement, projectiles, camera, audio, UI and global simulation can each differ. Define the hit-stop timer's clock explicitly so it can expire even when simulation is frozen, including pause and resume interactions. Decide whether inputs during the hold are ignored, sampled or buffered, which clock ages them, and how simultaneous hits, repeated overlaps and retriggers resolve. Ensure each intended hit registers once and no state stays frozen after resumption.

Step through collision and recovery; check timer behavior, input retention, overlapping hits, pause and interruption. Compare feedback in isolation and in combination. Pose, sound, visual impact and optional haptics can reinforce one another; stronger effects are not automatically better. Keep the target, threat and next action readable. Disc Room's developer describes directional camera impact and clear death attribution in the linked article above; the exact treatment remains game-specific.

## Accessible feedback and controls

Provide remapping and, where applicable, hold/toggle alternatives and timing or speed assistance. Persist independent shake and haptic intensity settings with a true off value. Do not rely solely on sound or color for essential information: pair each cue with a distinguishable alternative appropriate to the action. With optional effects off, retain impact direction, damage and attack-readiness information. Include players with relevant disabilities in playtests.

Test core scenarios with sound muted, visual effects disabled and haptics disabled independently; verify remapped prompts, saved settings and available alternatives to repeated or sustained input. An option alone does not prove accessibility. See [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/full-list/) for the underlying control and sensory recommendations and [Microsoft's camera-motion guidance](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/117) for motion options.
