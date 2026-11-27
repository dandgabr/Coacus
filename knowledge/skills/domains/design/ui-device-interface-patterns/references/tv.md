# TV and Distance Viewing

## Context

Design for a seated viewing position, landscape composition, and the available remote or controller. Validate legibility at the expected viewing distance and account for the actual display and platform safe area.

## Controls

Map every essential action to directional movement, Select, and platform Back. Give rows and grids predictable neighbors. Declare an initial focus target and an ordered fallback when content loads or disappears. Use platform media and text entry controls where available.

## States

Show focused, selected, and playing states separately. Scroll the focused item into view without clipping its indicator. When returning from an item, restore focus to that item if still present or a nearby available target. Provide visible loading and empty states that retain a route back.

## Accessibility

Keep focus easy to see over bright and dark media. Confirm readable text, control names, and captions where applicable. Test rapid directional input, long lists, unavailable controls, and system Back using the actual remote. Keep motion cues supplementary to a stable focus indication.

## Evidence

Samsung's 2022 Input Methods guide describes directional movement and scrolling at a list edge. Use these as period examples and verify current directions, wrapping, and button behavior for the target platform. [Samsung Smart TV Design Guides, Input Methods](https://aresluna.org/ui-style-guides/Samsung/Smart%20TV%20Design%20Guides%20%282022%29/smarttv/design/input-methods.html).

For current directional reachability and distance legibility consult [Android TV adaptive guidance](https://developer.android.com/develop/adaptive-apps/guides/tv/build-adaptive-apps-for-tv) and the target TV platform's documentation.

## Validation

Use only the remote to open a title from a moving row, play or pause, enable captions where available, and return. Repeat after the original card disappears. Verify clear focus, readable labels, and exit behavior from the seating position.
