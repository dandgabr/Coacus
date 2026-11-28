# Media-clock overlays

Use a metadata text track for annotations and other changes driven by the
media clock. Keep native captions in a separate captions track under the
viewer's control. Provide a descriptive transcript when timed visuals or
sounds carry meaning, following the
[media accessibility guidance](../../../../engineering/practices/web-accessibility-wcag/SKILL.md#-captions-transcripts-and-audio).

## Render the current cue set

Declare a local WebVTT track with `kind="metadata"`. Set its mode to
`hidden` to evaluate cues without native display. Leave the captions track's
mode alone. Listen for `cuechange`, and refresh when track loading completes.
Compute the overlay from all `activeCues` on each update. Rendering from
the current cue set handles seeking in either direction, overlapping cues and
cue-free gaps without tracking which entries fired. Use stable IDs to map
metadata to actions when needed, and render annotation strings as text.

On pause, keep the current annotation in place. Let the media clock advance
the cue set on resume and at a changed playback rate. Avoid a polling loop or
one timeout per cue. Cancel listeners on teardown and disable the metadata
track when the component owns it. Reinitialize on remount. Keep timed text
outside the playback controls' hit area and reserve space for native captions.
Keep permanent links or buttons available outside the player when a timed
annotation introduces a substantive action. Avoid moving focus or announcing
every change through a live region.

Use `requestVideoFrameCallback()` for pixel effects or overlays that must
align with presented frames. Use the callback's `mediaTime` for frame
identity, retain the latest request ID for cancellation, and resume updates
after a seek where appropriate. Callback delivery can lag presentation, so
measure alignment on target browsers before promising frame-exact latency.
When frame callbacks are missing, keep the cue-based text or static
equivalent. Plain annotations need only media cues.

## Run the example

Serve [media-clock-overlay.html](../examples/media-clock-overlay.html) and its
companion assets from a local HTTP server that handles byte-range requests.
The six-second original
[two-plots clip](../examples/two-plots.webm) contains two static arrangements
of drawn bars. It highlights the left plot from 0 to 2 seconds and the right
plot from 2.4 to 4.4 seconds, with original 440 Hz and 660 Hz tones starting
at 0.2 and 2.65 seconds. It uses a VP9 video stream and Opus audio.
The [annotation track](../examples/two-plots-annotations.vtt),
[native captions](../examples/two-plots-captions.vtt) and inline descriptive
transcript are separate layers.

| Operation | Expected result |
| --- | --- |
| Play from the beginning | The first annotation appears. The native caption for the tone can appear independently. |
| Seek forward to 3 seconds | The second annotation replaces the first. |
| Pause in the second cue | The annotation stays and playback time stops advancing. |
| Seek back to 2.2, then to 1 second | The annotation clears in the gap, then the first annotation returns. |
| Seek to 2.2 seconds and play at 2× | The second cue appears at media time 2.4 seconds. |
| Disable JavaScript or fail the metadata request | Native controls, captions and the descriptive transcript remain available. |

## Compatibility sources

Review date 2026-11-27. Verify native playback and caption choice on target
devices. Test the metadata track from its actual origin and feature-detect
frame callbacks separately. A native caption track or transcript stays
available when the overlay fails. [HTML text track API](https://html.spec.whatwg.org/multipage/media.html#text-track-api),
[video-frame callback processing draft](https://wicg.github.io/video-rvfc/),
[WebM format and codec parameters](https://www.webmproject.org/docs/container/),
[WAI media accessibility](https://www.w3.org/WAI/media/av/).
