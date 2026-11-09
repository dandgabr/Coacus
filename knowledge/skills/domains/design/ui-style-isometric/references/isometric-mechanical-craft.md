# Isometric Mechanical Apparatus & Cutaway Craft

A technical guide for authoring complex isometric apparatus, cutaway diagrams, and
functional mechanical explainers in 2D vector formats.

## 1. The Metaphorical Instrument Principle

In technical communication and system architecture, physical machines provide
intuitive spatial metaphors for abstract software flows:
- A pin-tumbler cylinder lock explains cryptographic key derivation or cache hashing.
- A multi-axis gantry plotter illustrates concurrent work queues and thread scheduling.
- A spring-loaded dial indicator visualizes animation physics, damping, and tolerance limits.
- An optical prism or filter array demonstrates event routing and data pipelines.

Every mechanical figure balances structural realism with communicative clarity:
moving parts have clearance, support columns rest on physical bases, and energy
flows along legible directional paths.

## 2. Four-Tone Shading and Solids of Revolution

Planar isometric projections use three primary face luminosities derived from an
infinite light source positioned above and to the left of the viewer:
- **Top face (direct illumination):** 1.15× base luminance.
- **Left face (diffuse reflection):** 1.00× base luminance.
- **Right face (shadow zone):** 0.80× base luminance.
- **Cavity / interior cutaway:** 0.60× base luminance.

### Curved Surfaces and Hermite Shading

For cylindrical columns, rotating shafts, and solids of revolution (lathed geometry),
discrete three-tone shading produces jarring banding artifacts. Use analytic
surface-normal calculation with monotone cubic Hermite interpolation:

$$\frac{dr}{ds} = \text{surface gradient along longitudinal axis}$$

Interpolate surface luminance continuously from the silhouette edge to the highlight
band. This eliminates shade staircases while preserving sharp specular creases at
fillets, collars, and chamfered shoulders.

## 3. Segmented 3D Conduit and Cable Routing

Pipes, wire harnesses, and structural conduits that cross multiple depth planes
cannot be drawn as single monolithic paths without breaking painter's algorithm
layering:

1. **Depth chunking:** Break continuous runs into discrete segments at every axis
   turn or plane crossing.
2. **Collar and clamp gaps:** Insert mechanical collars or bracket gaps where conduits
   pass through bulkheads or behind structural columns.
3. **Elliptical end caps:** Terminate pipe openings with true 30-degree isometric
   ellipses ($b/a = \tan(30^\circ) \approx 0.577$).

## 4. Depth Sorting and Ray-Cast Painter's Ordering

To guarantee correct occlusion in complex multi-assembly figures without a runtime
z-buffer:
- Calculate the centroid depth coordinate $D = x + y + z$ for every solid component
  in world space.
- Where two components overlap in screen space but share similar centroid depths,
  evaluate separating planes along the major projection axes ($30^\circ$, $90^\circ$,
  $150^\circ$).
- Wrap-around assemblies (such as coil springs enclosing guide rods or bearing cages
  enclosing shafts) must be split into front and rear halves, sorted respectively
  before and after the enclosed part.

## 5. Automated Geometric Verification Checklist

Before finalizing an isometric vector figure, verify geometric integrity against
four defect criteria:

1. **Zero line-end floating:** Every line endpoint must terminate within 1 px of a
   perimeter outline, intersection vertex, or seam stroke. Unanchored floating lines
   signal unfinished vector drafting.
2. **Zero interpenetration:** Moving assemblies must demonstrate clearance across
   all operational states (rest, expanded, retracted).
3. **Support chain continuity:** No structural component may hang unsupported in
   mid-air; every bearing, bracket, and chassis plate must trace a continuous path
   to the foundational baseplate.
4. **Label orthogonality:** Text callouts and dimension indicators must remain upright
   and unskewed in viewport space, connected to inspection points via crisp angled
   leader lines with circular terminal anchors.
