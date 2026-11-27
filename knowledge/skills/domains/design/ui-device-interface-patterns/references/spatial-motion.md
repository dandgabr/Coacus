# Spatial and Motion Interfaces

## Context

Identify whether interaction uses head-mounted visuals, gaze, hands, controllers, or a distant motion sensor. Specify the real space, seated and standing positions, field of view, tracking conditions, and any alternate input modes.

## Controls

Separate target discovery, engagement, and confirmation. Treat look or hover as preparation unless the platform intentionally uses dwell activation and makes that progress visible and cancelable. Avoid sustained large reaches for frequent actions. Provide platform-supported buttons, voice, or other accessible inputs for essential actions that can be expressed without body motion.

## States

Show when tracking or engagement is ready, interrupted, or lost. Cancel provisional manipulation on loss, retain committed state, and provide a visible way to recover. Support pause, recenter, and exit where applicable. Avoid triggering a command on reconnection alone.

## Accessibility

Verify seated use, range of movement, alternate inputs, and reduced motion. Keep stationary and world-anchored content readable in the expected environment. Avoid attaching essential navigation to moving objects or putting it outside reachable view.

## Evidence

Microsoft's Kinect guide separates engagement, aiming, selection, and multi-user concerns. Google Glass and Cardboard are distinct historical platforms documented in the [archive map](aresluna-source-map.md). For current gaze and hand interaction consult [Apple visionOS design guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) or the target platform's current guidance.

## Validation

Open an object, interrupt tracking before confirmation, recover without duplicate execution, and finish with the alternate input. Check the same flow seated and with reduced motion enabled on representative hardware.
