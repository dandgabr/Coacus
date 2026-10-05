# 📚 Canonical Encyclopedia of the Core Page Design Styles

This document is the complete canonical reference for the art direction, history, formal attributes, design tokens, and practical applications of the core page design styles.

---

## 🏛️ Family 1: Historical Movements & Avant-Gardes (1890 – 1980)

### 1. Bauhaus & Functional Modernism (1919–1933)
* **Historical Origin**: School founded by Walter Gropius in Weimar/Dessau.
* **Philosophy**: Form strictly follows function. Destruction of superficial bourgeois ornament. Art and technology fused into mass utilitarian production.
* **Formal Attributes**:
  - Elementary geometry: perfect circle, equilateral triangle, square.
  - Strict palette: primary Red (`#D92525`), primary Yellow (`#F2B705`), cobalt Blue (`#0D47A1`), pure Black (`#000000`), and White (`#FFFFFF`).
  - No shadows, no gradients, no rounded corners (`border-radius: 0px`).
* **Typography**: Purely geometric sans-serif typefaces (Futura, Archivo Black, Bayer Universal). Headings with heavy weight and tight leading.
* **Token Example**:
  ```css
  --color-primary: #d92525;
  --color-secondary: #0d47a1;
  --color-accent: #f2b705;
  --color-surface: #ffffff;
  --color-text: #000000;
  --border-width: 3px;
  --radius: 0px;
  --font-display: 'Futura', 'Archivo Black', sans-serif;
  ```

### 2. Swiss Style / International Typographic Style (1950s)
* **Historical Origin**: Switzerland (Zurich and Basel), led by Josef Müller-Brockmann, Armin Hofmann, and Emil Ruder.
* **Philosophy**: Clear, objective, universal visual presentation of information. The designer acts as an invisible mediator of the content.
* **Formal Attributes**:
  - Strict modular grid (12 or 16 columns) calibrated mathematically.
  - Logical asymmetry: alignment is strictly flush left with an unjustified right margin (*ragged right*).
  - Generous white space treated as an active architectural element.
  - High-contrast monochromatic documentary photography instead of illustrations.
* **Typography**: Pure, neutral grotesques (Neue Haas Grotesk, Helvetica, Akzidenz-Grotesk, Univers).
* **Token Example**:
  ```css
  --color-bg: #f4f4f4;
  --color-text: #111111;
  --color-accent: #ff3b30;
  --grid-columns: 12;
  --gutter: 24px;
  --radius: 0px;
  --font-sans: 'Neue Haas Grotesk', 'Helvetica Neue', Arial, sans-serif;
  ```

### 3. De Stijl / Neoplasticism (1917–1931)
* **Historical Origin**: The Netherlands, founded by Theo van Doesburg and immortalized by Piet Mondrian's paintings.
* **Philosophy**: Expression of a new universal spiritual harmony through radical abstraction and reduction to the primary laws of geometry.
* **Formal Attributes**:
  - Only orthogonal black lines (horizontal and vertical) with striking thickness (3px to 6px).
  - Rectangular blocks filled with saturated primary colors and non-colors (white, light gray, and black).
  - Total absence of curves, diagonals, shadows, and textures.
* **Typography**: Sans-serif typography in text boxes with rigid outlines.

### 4. Art Deco (1920s–1930s)
* **Historical Origin**: Paris (Exposition Internationale des Arts Décoratifs et Industriels Modernes, 1925).
* **Philosophy**: The glamour of technological progress, speed, industrial wealth, and the modern luxury of the Jazz Age.
* **Formal Attributes**:
  - Exact bilateral symmetry and refined geometric ornamentation.
  - Stepped forms (ziggurats), fans, sunbursts, and metallic arches.
  - Palette: polished Gold (`#D4AF37`), bronze, ebony Black (`#0A0A0A`), and petrol blue.
* **Typography**: Decorative display typefaces with elongated stems, high waist, and elegant thin lines (Poiret One, Broadway, Park Lane).

### 5. Art Nouveau & Arts and Crafts (1890–1914)
* **Historical Origin**: Europe (France, Belgium, England with William Morris and Alphonse Mucha).
* **Philosophy**: Humanist and aesthetic resistance against the dehumanization and coldness of the mechanical Industrial Revolution.
* **Formal Attributes**:
  - Dynamic, fluid curved lines inspired by flora (vines, leaves, stems, waves).
  - Hand-illustrated frames with organic borders and botanical details.
  - Earthy palette: olive green, terracotta, soft mustard, aged paper, and matte gold.
* **Typography**: Expressive serifs with complex calligraphic ligatures and floral details.

### 6. Memphis Design (1981–1987)
* **Historical Origin**: Milan, founded by Ettore Sottsass and the Memphis group.
* **Philosophy**: Playful, iconoclastic reaction against austere minimalism and rigid modernist functionalism.
* **Formal Attributes**:
  - Zigzag patterns (*squiggles*), scattered dots, diagonal stripes, and floating triangles.
  - Post-modern palette: an intentionally garish mix of pastel colors with neon accents (hot pink, canary yellow, turquoise, mint).
  - Dynamic asymmetry, asymmetric shapes, and visual good humor.
* **Typography**: Relaxed typography, display with thick, cheerful strokes.

---

## 💾 Family 2: The Early Digital Era & Retro Nostalgia (1980 – 2012)

### 7. Retro-Computing / 8-bit & 16-bit
* **Origin**: The dawn of personal computing and classic consoles (Commodore 64, NES, Game Boy, Apple II).
* **Philosophy**: The poetics of memory and graphics-resolution limitations from the early microprocessor era.
* **Formal Attributes**:
  - Intentionally pixelated resolution, reduced indexed palettes (4-color CGA, 16-color EGA).
  - Subtle CRT scanlines (*scanlines*) and slight cathode-ray tube distortion.
  - Windows with beveled bars in the style of Windows 95 or Mac OS System 7.
* **Typography**: Bitmap and pixelated fonts (Press Start 2P, Silkscreen, VT323).

### 8. CLI / Terminal / Text-based UI (TUI)
* **Origin**: VT100 terminals and text-oriented operating systems (UNIX, DOS).
* **Philosophy**: Maximum efficiency, elimination of graphical intermediaries, and transparency of data.
* **Formal Attributes**:
  - Monochromatic black or deep charcoal background (`#121212`).
  - Monochromatic colors in phosphor green (`#00FF66`) or warm amber (`#FFB000`).
  - Frames, dividers, and tables built exclusively from ASCII/Unicode characters (`┌─┐│└─┘`).
  - Blinking block cursor at the end of the active line.
* **Typography**: Rigorous monospaced fonts (JetBrains Mono, Fira Code, IBM Plex Mono).

### 9. Classic Web Brutalism & Data-Dense
* **Origin**: The 1990s web, digital brutalism of the 2010s, and high-frequency Bloomberg consoles.
* **Philosophy**: The raw truth of web materials: unadorned HTML, links, and high-density tabular data throughput without decorative friction.
* **Formal Attributes**:
  - Standard HTML tags rendered without superfluous CSS decoration.
  - Native underlined blue hyperlinks (`#0000EE`) and visited purple (`#551A8B`).
  - Native tables with hairline borders, zero margin waste, and inline sparklines.
* **Typography**: System monospaced or Times New Roman fonts across standard HTML hierarchies.

### 10. Y2K Futurism (1998–2003)
* **Origin**: Turn-of-the-millennium culture, rave, and dot-com bubble optimism.
* **Philosophy**: Euphoria over the arrival of the 21st century and a cyberspace without borders.
* **Formal Attributes**:
  - Melted liquid metal, shiny 3D chrome, translucent orbs.
  - Iridescent gradients, electric cyan, metallic silver, and electronic-circuit details.
* **Typography**: Rounded bubble fonts (*bubble fonts*), stretched cybernetic typography.

### 11. Frutiger Aero / Web 2.0 Gloss (2004–2013)
* **Origin**: Windows Vista/7 Aero, Mac OS X Aqua, and Nintendo Wii/DS consoles.
* **Philosophy**: Clean technological utopianism: the harmonious fusion of cutting-edge technology, nature, and ecology.
* **Formal Attributes**:
  - Polished glass surfaces with a white horizontal gloss (*glossy reflection*).
  - Blue skies with fluffy white clouds, crystal-clear translucent water, green leaves with dew, and tropical fish.
  - Three-dimensional orbs with a bubble effect, photographic bokeh, and lens flare.
* **Typography**: Clean, polished humanist fonts (Segoe UI, Frutiger, Myriad Pro).

### 12. Skeuomorphism (Classic, Modern Hybrid & Aqua)
* **Origin**: Apple iOS 1 through 6, Mac OS X Aqua, and modern precision audio/instrument design.
* **Philosophy**: Immediate affordance through tactile metaphors of everyday physical objects (wood, leather, milled aluminum dials, water-drop buttons).
* **Formal Attributes**:
  - Physical material simulations: stitched leather, felt, brushed aluminum, and knurled dials.
  - Dimensional bevels, top-down lighting angles, and debossed letterpress text shadows.
* **Typography**: Helvetica Neue / SF Pro with inner shadows and embossed bevels.

---

## 📐 Family 3: Modern Minimalism & Design Systems (2012 – 2023)

### 13. Flat Design 1.0 (2012–2015)
* **Origin**: Windows Phone Metro UI, iOS 7, and Windows 8.
* **Philosophy**: Radical rejection of simulating physical materials on electronic screens.
* **Formal Attributes**:
  - Total elimination of shadows, reflections, gradients, and bevels.
  - Solid, saturated color blocks in a purely two-dimensional arrangement.
* **Typography**: Pure sans-serif fonts in simple dialog boxes.

### 14. Flat 2.0 & Material Design / Material You (2015–Present)
* **Origin**: Google Material Design (M1, M2, and Material You / M3).
* **Philosophy**: The physical metaphor of "quantum digital paper" with logical elevations and transition physics.
* **Formal Attributes**:
  - Logical z-index elevations (1dp to 24dp) producing soft, realistic shadows.
  - Physical acceleration and deceleration curves on every animation.
  - Dynamic tonal palettes extracted from the user's environment (M3).
* **Typography**: Roboto and Google Sans.

### 15. Neumorphism / Soft UI (2019–2020)
* **Origin**: A conceptual trend on Dribbble.
* **Philosophy**: The interface sculpted as a relief in the same continuous material as the background plane.
* **Formal Attributes**:
  - The element has exactly the same color as the background canvas.
  - Volume is shaped by two opposing shadows: a dark shadow at the bottom-right and a white light at the top-left.
  ```css
  background: #e0e5ec;
  box-shadow: 9px 9px 16px #a3b1c6, -9px -9px 16px #ffffff;
  border-radius: 16px;
  ```

### 16. Glassmorphism & VisionOS Spatial Elevation (2020–Present)
* **Origin**: macOS Big Sur, Windows 11 Fluent, and Apple visionOS.
* **Philosophy**: Spatial depth and optical hierarchy through layers of frosted glass, specular border light tracking, and environmental luminescence.
* **Formal Attributes**:
  - `backdrop-filter: blur(24px to 40px) saturate(180%)` with semi-transparent white/obsidian layers.
  - Calibrated 1px specular highlight border simulating physical overhead lighting.
  - Deep 3D z-axis elevation and gaze/cursor responsive illumination.

### 17. Claymorphism & Plasticine Stop-Motion (2021–Present)
* **Origin**: Playful 3D web (Spline) and clay animation cinema (Aardman, Will Vinton).
* **Philosophy**: Tactile coziness, human craftsmanship, and warm modeled-clay volumes.
* **Formal Attributes**:
  - Generously rounded corners (`border-radius: 32px` to `48px`) with bowed edge midpoints.
  - Dual opposing inner shadows creating an inflated dome volume + soft ambient drop shadow.
  - Earthy plasticine and pastel candy colors, with optional 12fps stepped stop-motion animation.

---

## 🚀 Family 4: Contemporary Avant-Garde & Anti-AI Styles (2024 – 2026+)

### 18. Bento Grid (Modularity & Density)
* **Origin**: Apple promo pages, Linear, Raycast.
* **Philosophy**: High information density presented cleanly, scannably, and compartmentalized.
* **Formal Attributes**:
  - Modular grid with cells of varying proportions (1x1, 2x1, 1x2, 2x2).
  - Contained rounded corners (8px to 16px) and subtle low-opacity borders.
  - Each cell tells a visual micro-narrative with dedicated graphics.

### 19. Brutalist Monochrome & Engineered Minimalism
* **Origin**: Architectural New Brutalism, Susan Kare 1-bit Mac, Vercel Geist, Linear.
* **Philosophy**: Software architecture treated as high-precision engineering; uncompromising binary contrast.
* **Formal Attributes**:
  - Strict black-and-white binary palette (`#000000` and `#FFFFFF`, zero gray).
  - 1px hairline rules, exposed grid scaffolding, coordinate tags, and corner ticks (`+`).
  - Technical micro-typography and instant hover color inversion.

### 20. Neo-Brutalism / Nu-Brutalism
* **Origin**: Figma, Gumroad, Retool, Substack.
* **Philosophy**: Rejection of corporate coldness and sterility; an affirmation of raw confidence and attitude.
* **Formal Attributes**:
  - Solid black borders from 2px to 4px.
  - Hard offset shadows with zero blur (`box-shadow: 4px 4px 0px #000000`).
  - Ultra-saturated colors in high contrast.
  - Buttons that physically sink on hover/active (`transform: translate(2px, 2px)` with a reduced shadow).

### 21. Editorial / Archive Luxury & Horizontal Gallery
* **Origin**: Kinfolk, Readymag, independent fashion magazines, Stripe Press, museum exhibition curation.
* **Philosophy**: The slowness, prestige, and literary pacing of print publishing and museum curatorial archives.
* **Formal Attributes**:
  - Generous asymmetric margins, numbered footnotes, and oldstyle numerals.
  - Monumental display serifs (*Instrument Serif*, *Fraunces*, *PP Editorial New*) paired with neutral sans-serifs.
  - Archival tones (bone, linen, taupe, charcoal) with optional continuous horizontal ribbon galleries.

### 22. Solarpunk (Ecological, Pastoral & Biomorphic)
* **Origin**: Regenerative climate movements, William Morris Arts & Crafts, and parametric biomimicry.
* **Philosophy**: Technological progress in symbiotic harmony with natural ecosystems, community agency, and biological growth.
* **Formal Attributes**:
  - Sunlit gold, leaf greens, warm terracotta, oatmeal linen, and fertile loam.
  - Organic asymmetric cards, Voronoi cell partitions, and vine-like growth transitions.
  - Low-data, low-energy performance budgets paired with verifiable sustainability claims.

### 23. Cyberpunk & Sci-Fi Tactical HUD
* **Origin**: Fictional sci-fi interfaces (FUI), Territory Studio (*Blade Runner 2049*), *Cyberpunk 2077*.
* **Philosophy**: Neon-noir street-level dystopia combined with high-tech military instrument telemetry.
* **Formal Attributes**:
  - Absolute black background (`#000000`, `#07060F`).
  - Military HUD details: 45-degree chamfered corners, targeting reticles, calibration brackets, and telemetry streams.
  - Acidic neon accents: electric cyan (`#00F0FF`), hot magenta (`#FF003C`), and hazard yellow (`#FCEE0A`).
  - Subtle scanlines and chromatic glitch slicing.

### 24. Acid Graphics / Deconstructivist Anti-Design
* **Origin**: 1990s rave culture revisited by the post-internet avant-garde (David Carson, digital underground).
* **Philosophy**: Deliberate breaking of any grid and conventional good-taste standard in the name of pure visual expressiveness.
* **Formal Attributes**:
  - Deformed, liquefied (*liquid chrome*), stretched typography.
  - Chaotic digital collages in overlapping layers with no containment in boxes.
  - A mix of medieval Gothic fonts (Blackletter) with mono fonts and esoteric symbols.

---

## 🧩 Family 5: Extended Styles

Each style below has a dedicated deep-dive skill in the design style library.

- **Terminal TUI** — Monospace grids, box-drawing frames, phosphor palettes, keyboard-first use. See [ui-style-terminal-tui](../../../domains/design/ui-style-terminal-tui/SKILL.md).
- **Retro Computing / Pixel** — 8/16-bit pixel art, bitmap fonts, limited palettes, dithering. See [ui-style-retro-computing-pixel](../../../domains/design/ui-style-retro-computing-pixel/SKILL.md).
- **Linear-style SaaS** — Dark-first panels, low-alpha 1px borders, radial glows. See [ui-style-linear-saas](../../../domains/design/ui-style-linear-saas/SKILL.md).
- **Glitch** — Signal-corruption effects with layered offsets and clip-path slices. See [ui-style-glitch](../../../domains/design/ui-style-glitch/SKILL.md).
- **Grain and Noise Texture** — SVG noise layers that warm flat color and dither gradient banding. See [ui-style-grain-noise-texture](../../../domains/design/ui-style-grain-noise-texture/SKILL.md).
- **Broken Grid** — Deliberate overlap and offset on a CSS Grid with a sane reading order. See [ui-style-broken-grid](../../../domains/design/ui-style-broken-grid/SKILL.md).
- **Hand-Drawn Sketch** — Wobbly outlines, scribbled underlines and handwriting type. See [ui-style-hand-drawn-sketch](../../../domains/design/ui-style-hand-drawn-sketch/SKILL.md).
- **Collage, Scrapbook & Dadaist Photomontage** — Layered cutouts, tape, torn edges, stamps and ransom-note anti-art typography. See [ui-style-collage-scrapbook](../../../domains/design/ui-style-collage-scrapbook/SKILL.md).
- **Risograph and Zine** — Spot-color overprint, misregistration and halftone. See [ui-style-risograph-zine](../../../domains/design/ui-style-risograph-zine/SKILL.md).
- **Vaporwave and Synthwave** — Nostalgic neon horizons and pastel retro-internet imagery. See [ui-style-vaporwave-synthwave](../../../domains/design/ui-style-vaporwave-synthwave/SKILL.md).
- **Calm / Quiet UI** — Reduced stimulation, soft contrast and explanatory motion. See [ui-style-calm-quiet-ui](../../../domains/design/ui-style-calm-quiet-ui/SKILL.md).
- **Bauhaus** — Primary colors and geometric primitives, function first. See [ui-style-bauhaus](../../../domains/design/ui-style-bauhaus/SKILL.md).
- **De Stijl** — Primaries, black grid lines and asymmetric balance. See [ui-style-de-stijl](../../../domains/design/ui-style-de-stijl/SKILL.md).
- **Art Deco** — Symmetry, metallic accents and sunburst motifs. See [ui-style-art-deco](../../../domains/design/ui-style-art-deco/SKILL.md).
- **Art Nouveau and Arts & Crafts** — Whiplash curves, organic ornament and craft heritage. See [ui-style-art-nouveau-arts-crafts](../../../domains/design/ui-style-art-nouveau-arts-crafts/SKILL.md).
- **Memphis** — Confetti patterns, squiggles and clashing color. See [ui-style-memphis](../../../domains/design/ui-style-memphis/SKILL.md).
- **Atompunk & Space-Age Retro-Futurism** — Googie starbursts, boomerangs, orbit components and atomic optimism. See [ui-style-atompunk](../../../domains/design/ui-style-atompunk/SKILL.md).
- **Indie Web Revival** — Neocities-era personal sites, webrings and system fonts. See [ui-style-indie-web-revival](../../../domains/design/ui-style-indie-web-revival/SKILL.md).
- **Mid-Century Modern** — Flat geometry in atomic orange, turquoise and olive. See [ui-style-mid-century-modern](../../../domains/design/ui-style-mid-century-modern/SKILL.md).
- **Isometric** — Axonometric UI and illustration with parallel lines. See [ui-style-isometric](../../../domains/design/ui-style-isometric/SKILL.md).
- **Card-based UI** — Modular cards, scannable content chunks and structured collections. See [ui-style-card-based-ui](../../../domains/design/ui-style-card-based-ui/SKILL.md).
- **Split-Screen Dualism** — 50/50 dual vertical canvases, complementary color polarity and synchronized scroll. See [ui-style-split-screen-dualism](../../../domains/design/ui-style-split-screen-dualism/SKILL.md).
- **Blueprint & CAD Technical Schematic** — Architectural cyanotype blueprints, crosshairs, dimension ticks and drafting grids. See [ui-style-blueprint-cad-schematic](../../../domains/design/ui-style-blueprint-cad-schematic/SKILL.md).
- **Fluid Liquid & Metaball Morph** — Viscous blob physics, SVG goo filters and jelly transitions. See [ui-style-fluid-liquid-morph](../../../domains/design/ui-style-fluid-liquid-morph/SKILL.md).
- **Holographic Foil & Iridescent Chrome** — Dynamic rainbow refraction angles, pearlescent shimmer and metallic specular flares. See [ui-style-holographic-foil-iridescent](../../../domains/design/ui-style-holographic-foil-iridescent/SKILL.md).
- **Weirdcore & Liminal Dreamcore** — Surreal liminal photography, low-res JPG artifacts, unsettling dreamlike typography and lo-fi nostalgia. See [ui-style-weirdcore-dreamcore](../../../domains/design/ui-style-weirdcore-dreamcore/SKILL.md).
- **Kawaii Pastel & Soft Aesthetic** — Pillowy marshmallow rounded shapes, soothing pastel candies and friendly sticker microcopy. See [ui-style-kawaii-pastel-soft](../../../domains/design/ui-style-kawaii-pastel-soft/SKILL.md).
- **Broadsheet Newspaper & Letterpress** — Classical multi-column newspaper layouts, ornate drop-caps, hairline rules and yellowed newsprint. See [ui-style-analog-newspaper-broadsheet](../../../domains/design/ui-style-analog-newspaper-broadsheet/SKILL.md).
- **Constructivism & Agitprop Graphic** — Stark 45° diagonals, scarlet/black/cream palettes and geometric photomontage. See [ui-style-constructivism-propaganda](../../../domains/design/ui-style-constructivism-propaganda/SKILL.md).
- **1960s Psychedelic & Liquid Light** — Vibrating optical colors, kaleidoscopic symmetry and melting liquid lettering. See [ui-style-psychedelic-60s](../../../domains/design/ui-style-psychedelic-60s/SKILL.md).
- **Pop Art & Ben-Day Halftone** — Oversized comic dot screens, bold black ink outlines, primary CMYK inks and comic callouts. See [ui-style-pop-art-halftone](../../../domains/design/ui-style-pop-art-halftone/SKILL.md).
- **Cassette Futurism & Analog Sci-Fi** — 1970s-80s phosphor CRT displays, mechanical keys, magnetic tape data and industrial beige casings. See [ui-style-cassette-futurism](../../../domains/design/ui-style-cassette-futurism/SKILL.md).
- **Silkpunk & Organic Engineering** — East Asian classical antiquity, bamboo and copper structural lines, sumi-e ink washes and origami geometry. See [ui-style-silkpunk](../../../domains/design/ui-style-silkpunk/SKILL.md).
- **Dungeon Synth & Dark Fantasy Medieval** — Ancient crypt stones, tarnished gold, woodcut engravings and archaic gothic typography. See [ui-style-dungeon-synth-dark-fantasy](../../../domains/design/ui-style-dungeon-synth-dark-fantasy/SKILL.md).
- **Scrollytelling & Narrative Scroll** — Scroll-sequenced stories, pinned scenes, stepped annotations and one-page continuous flows. See [ui-style-scrollytelling](../../../domains/design/ui-style-scrollytelling/SKILL.md).
- **Kinetic Typography & Marquee Ticker** — Dynamic text in motion, masked per-glyph reveals, variable-font morphs and infinite loop ribbons. See [ui-style-kinetic-typography](../../../domains/design/ui-style-kinetic-typography/SKILL.md).
- **Expressive Variable Typography & Monumental Anti-Hero** — Extreme typographic scale filling the entire viewport, zero stock imagery, glyph architecture. See [ui-style-expressive-variable-typography](../../../domains/design/ui-style-expressive-variable-typography/SKILL.md).
- **Parallax Scrolling** — Layered vertical depth revealing spatial perspective on scroll. See [ui-style-parallax-scrolling](../../../domains/design/ui-style-parallax-scrolling/SKILL.md).
- **3D Immersive / WebGL** — Interactive 3D scene canvas and real-time graphics. See [ui-style-3d-immersive-webgl](../../../domains/design/ui-style-3d-immersive-webgl/SKILL.md).
- **AI-Native / Generative UI** — Intent-driven dynamic interface composition. See [ui-style-ai-native-generative-ui](../../../domains/design/ui-style-ai-native-generative-ui/SKILL.md).
- **Organic / Biophilic** — Calm nature-inspired forms, earthy tones and biological curves. See [ui-style-organic-biophilic](../../../domains/design/ui-style-organic-biophilic/SKILL.md).
- **Micro-Interactions** — Deliberate animation feedback loops for states and controls. See [ui-style-micro-interactions](../../../domains/design/ui-style-micro-interactions/SKILL.md).
- **Gradient & Duotone** — Two-tone color maps, high-energy duotones and vivid blending. See [ui-style-gradient-duotone](../../../domains/design/ui-style-gradient-duotone/SKILL.md).
- **Aurora / Mesh Gradient** — Organic, shifting multi-point blur meshes and ambient lighting. See [ui-style-aurora-mesh-gradient](../../../domains/design/ui-style-aurora-mesh-gradient/SKILL.md).
- **Dark Mode First** — Deep obsidian surfaces engineered for low-light immersion. See [ui-style-dark-mode-first](../../../domains/design/ui-style-dark-mode-first/SKILL.md).

### The -punk Family

Speculative-fiction aesthetics translated into UI and UX patterns:

- **Steampunk** — Victorian brass, gears and craft ornament as UI metaphor. See [ui-style-steampunk](../../../domains/design/ui-style-steampunk/SKILL.md).
- **Clockpunk** — Renaissance clockwork, parchment and da Vincian mechanics. See [ui-style-clockpunk](../../../domains/design/ui-style-clockpunk/SKILL.md).
- **Dieselpunk** — Interwar and WWII industrial design, Art Deco and Streamline variants. See [ui-style-dieselpunk](../../../domains/design/ui-style-dieselpunk/SKILL.md).
- **Atompunk** — 1945-1969 Atomic and Space Age optimism. See [ui-style-atompunk](../../../domains/design/ui-style-atompunk/SKILL.md).
- **Sandalpunk** — Bronze and Iron Age empires with advanced technology. See [ui-style-sandalpunk](../../../domains/design/ui-style-sandalpunk/SKILL.md).
- **Gothicpunk** — Dark urban gothic with supernatural undertones. See [ui-style-gothicpunk](../../../domains/design/ui-style-gothicpunk/SKILL.md).
- **Solarpunk** — Optimistic, sustainable, community-driven futures. See [ui-style-solarpunk](../../../domains/design/ui-style-solarpunk/SKILL.md).
- **Lunarpunk** — Nocturnal, privacy-minded counterpart to solarpunk. See [ui-style-lunarpunk](../../../domains/design/ui-style-lunarpunk/SKILL.md).
- **Biopunk** — Biotechnology, DIY biology and open science. See [ui-style-biopunk](../../../domains/design/ui-style-biopunk/SKILL.md).
- **Cyberpunk** — Neon-noir dystopian street-level technology. See [ui-style-cyberpunk](../../../domains/design/ui-style-cyberpunk/SKILL.md).
- **Nanopunk** — Nanotechnology futures with no single canonical look. See [ui-style-nanopunk](../../../domains/design/ui-style-nanopunk/SKILL.md).
