# Native layout and theme effects

Use this reference for popup geometry, monetary text, materials and decorative
animation. The examples were observed in GNOME Shell 50.5 on 2026-10-08; recheck
native APIs on another runtime. See the [layout evidence](https://github.com/dandgabr/gnome-ai-quota/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/temp/reviews/2026-10-08-native-theme-layout.md).

## Keep decorations out of reading geometry

Place decoration behind native reading and hit-test actors. It must neither
contribute preferred size nor intercept input. Preserve the foreground tree and
its inset when switching Off/Subtle/Full modes; reconstructing different stacks
can move cards even when their CSS is unchanged.

Do not resize decoration children synchronously from allocation notifications
while native layout is still allocating siblings. Queue one idle layout job,
capture its generation and cancel it on rebuild/close/destroy. A finite cached
box is not proof of a valid current allocation. Track queued layout jobs alongside
animation sources and assert they are gone after disable.

Verify opening, closing by outside click, switching to another popup and repeated
theme changes. Capture frames during dismissal: a final screenshot alone misses
a transient popup at the stage origin. Avoid changing whole-menu opacity or
translation in ways that expose unallocated content during native menu closure.

Leave room for lateral card shadows inside the scroll viewport. Gutters, border
radii and clip boundaries must be tested together, including first/last cards.
Keep summary, section heading and footer background rules explicit; inherited
opaque styles can cut rectangles through an otherwise translucent background.

## Stable text is more than a width measurement

Keep numeric foreground actors and glyph state stable across card expansion;
update text only when its formatted value changes. Animate decoration rather than
the reading content. A rounded actor box does not guarantee stable glyph raster
placement. Inspect retained paint/raster frames through expand/collapse and theme
changes rather than inferring stability from preferred width alone.

Give complete currency text priority and allow secondary labels to adapt. Test
large values, both schemes, expanded fonts and RTL. Measure effective Pango/font
attributes and rendered bounds; a CSS declaration does not prove the requested
numeric feature reached the glyph layout. Compare frames and actual pixels for
jitter, truncation and clipping. A legible dark palette does not establish that its
light variant retains contrast or the theme's visual character.

## Describe defaults, compatibility and current state separately

Maintain one validated source of truth for material, motion, texture and packaged
optical presets. If native rendering derives pearlescent sheen or glass highlights
from theme identity, share that derivation with picker metadata rather than
duplicating it in presentation code.

A default indicator describes the chosen material and visible background presets,
not every compatible override. An opaque theme does not claim transparency merely
because it accepts frost. Interaction transitions alone do not claim ambient
effects; a particle preset with zero particles does not claim visible particles.
Static optical backgrounds and textures do qualify when actually rendered.
Tooltips name the material/effect and the mode needed to display it; current user
overrides do not rewrite what the theme defaults are. Keep labels accessible
without adding noninteractive icons to keyboard navigation.

Keep material selection independent from the motion/decorations switch when the
product contract allows glass with Effects Off. Transparency Off yields an opaque
material. Explain native blur fallback and unsupported selections instead of
silently promising a material that is not rendered. Trusted preset permissions
come from the loader's origin, never a user-supplied claim in theme JSON.

## Native GPU effects and WebGL serve different surfaces

A Shell popup uses the native compositor/actor stack; a WebGL preview is a separate
renderer and does not prove the popup has that effect. Choose reusable packaged
native presets for lightweight popup decoration, and sandbox any optional browser
preview without credentials or remote assets. A preview must not become a required
dependency for displaying quotas.

Bound particles and updates; cache static drawing by allocation. Run ambient work
only while the popup is open, obey system reduced-motion settings and preserve an
opaque fallback. Measure repaint counts, pending jobs, actor/source counts and
frame latency after the actual last source change. Define acceptance before the
run: a particle/update bound, expected closed and disabled resource baselines,
and a frame-latency budget for the target refresh rate. After close/disable there
must be no ambient updates; owned resources must return to their documented
baseline rather than merely remain finite. Compare repeated cycles against that
baseline and report measured frame latency against the chosen budget. Check resource reclamation
over repeated open/close and rebuild cycles. A synthetic compositor benchmark
does not establish performance on every physical GPU or display.

## Verify what the person sees

Test every shipped theme in both schemes and relevant material/mode combinations.
Capture individual screenshots with synthetic content on a varied backdrop;
check transparency over the complete popup, not only a tiny empty test patch.
Native blur capability and a passing contrast calculation do not establish
perceptible material or visual acceptance. Keep screenshots and performance
records tied to source digests. A later actor/layout change invalidates prior
frame evidence for the changed path.

See the [default-indicator correction](https://github.com/dandgabr/gnome-ai-quota/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/temp/reviews/2026-10-08-connector-refresh-theme-defaults.md)
and [material diagnosis](https://github.com/dandgabr/gnome-ai-quota/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/temp/reviews/2026-10-08-theme-material-diagnosis.md).
The diagnosis includes a rejected baseline: use its final dispositions, not its
historical palette/capability table as a current renderer specification.
