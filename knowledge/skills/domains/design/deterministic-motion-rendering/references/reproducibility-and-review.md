# Reproducibility and Media Review

Reviewed 2026-10-27. Use this reference for capture/export planning and delivered
media inspection. The receipt and acceptance procedure are Coacus conventions,
not claims that a library guarantees platform-independent pixels.

## Record the reproducibility boundary

Record scene revision, input/asset hashes, seed, exact rate and frame range,
dimensions, viewport/DPR, font identities, browser/renderer/OS/GPU mode,
color/alpha handling, capture settings and encoding invocation. Resolve actual
tool versions from the environment when executing; do not fill them from memory.

Distinguish these claims:

- Input and scene-state identity: identical declared inputs and evaluated state.
- Pixel identity: identical decoded image samples within a specified environment.
- File identity: identical encoded bytes, including metadata and container details.

Repeat captures in a controlled environment for exact comparison. Cross-platform
baselines require justified visual tolerances and explicit masks; a mask cannot
silently exclude the subject being verified. Different fonts or input hashes
invalidate the claimed baseline. Container metadata can differ even when decoded
pixels agree. Neither equal fps nor an MP4/WebM extension establishes losslessness.

## External export recipe

This illustrative command assembles contiguous zero-based PNG files at an exact
rate into a lossy H.264 delivery copy. Confirm locally available encoders,
dimensions, color expectations and delivery requirements before adopting it.
Keep source captures or a separately specified master when required.

```text
ffmpeg -framerate 30000/1001 -start_number 0 -i frames/frame-%06d.png -frames:v 300 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart delivery.mp4
```

Check that files `frame-000000.png` through `frame-000299.png` are present and
uniquely numbered before encoding. Do not overwrite an existing approved export
without the task's authorization. The example omits audio; when adding it,
declare sample rate, start offset and the intended end/hold/padding policy.
Do not use automatic trimming or retiming to hide an unexplained duration mismatch.

Inspect the actual delivered file independently:

```text
ffprobe -v error -count_frames -show_entries stream=index,codec_type,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,start_time,duration:format=duration -of json delivery.mp4
ffmpeg -v error -i delivery.mp4 -map 0:v:0 -f framemd5 decoded-frames.txt
```

The first command counts decoded frames and reports stream/container information;
the second records decoded-video frame hashes. Compare hashes only after fixing
the decoded pixel format and comparison pipeline. Lossy encoding means source PNG
hashes need not equal decoded video hashes. For content comparison, decode selected
frames with the declared color/pixel conversion and inspect them against captures
using justified tolerances. A decoder can conceal damaged frames, so also inspect
diagnostics and continuity rather than trusting frame count alone.

Validate the declared frame count, rational timing, dimensions and expected
duration, allowing only explained encoder/container timebase rounding. Inspect
start, end, cuts and high-motion samples. Check audio onset and end, narration
alignment and audible defects when audio exists. Metadata alone cannot prove
lip sync, narrative coherence or legibility.

## Review coverage and reporting

Review technical export evidence separately from whether the audience understands
the intended change. Inspect continuity, typography at the viewing size, cuts,
holds and factual content. Preserve intentional stillness; do not force constant
motion or universal frame-rate targets.

For each acceptance claim, record observed outcome, not run, or not applicable
with a reason. Missing media/tools limit the report to a plan. Static scenario
validation checks schema; reasoning evals assess decisions; only project-level
runtime evidence can establish actual frame equality or successful encoding.
Use existing interface verification for embedded playback and controls.

## Sources

- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots): rendering varies with browser, operating system, hardware and settings.
- [FFmpeg image2](https://ffmpeg.org/ffmpeg-formats.html#image2): image sequence inputs and framerate.
- [FFmpeg codecs](https://ffmpeg.org/ffmpeg-codecs.html): encoder-specific options; availability depends on the local build.
- [ffprobe](https://ffmpeg.org/ffprobe.html): decoded frame counting and stream inspection; interval seeking is not exact.
- [FFmpeg frame hash formats](https://ffmpeg.org/ffmpeg-formats.html#framemd5): per-frame decoded data checksums.
