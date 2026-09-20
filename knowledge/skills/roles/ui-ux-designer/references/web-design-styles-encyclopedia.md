# 📚 Canonical Encyclopedia of the 24 Page Design Styles

This document is the complete canonical reference for the art direction, history, formal attributes, design tokens, and practical applications of the 24 page design styles.

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

### 9. Classic Web Brutalism / Raw HTML
* **Origin**: The 1990s web and the digital brutalism of the 2010s.
* **Philosophy**: The truth of web materials: hypertext and links in their raw state, without pretending to be paper or a magazine.
* **Formal Attributes**:
  - Standard HTML tags rendered without decorative CSS classes.
  - Native underlined blue hyperlinks (`#0000EE`) and visited purple (`#551A8B`).
  - Native tables with 1px black borders and no complex internal spacing.
* **Typography**: Native Times New Roman across the pure HTML heading scale (`<h1>` to `<h6>`).

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

### 12. Classic Skeuomorphism (2007–2012)
* **Origin**: Apple iOS 1 through 6 and OS X Mavericks.
* **Philosophy**: Easing the touchscreen learning curve through tactile metaphors of everyday objects.
* **Formal Attributes**:
  - Faithful imitation of real textures: stitched leather, walnut wood, linen paper, and green billiard-table felt.
  - Chunky plastic buttons with three-stop gradients, bevels, and multi-layered drop shadows.
* **Typography**: Helvetica Neue with inner shadows and embossed bevels.

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

### 16. Glassmorphism (2020–2023)
* **Origin**: macOS Big Sur and Windows 11 Fluent Design.
* **Philosophy**: Spatial depth and hierarchy through layers of semi-transparent frosted glass.
* **Formal Attributes**:
  - `backdrop-filter: blur(16px)` with a semi-transparent background `rgba(255, 255, 255, 0.1)`.
  - A 1px border with a translucent gradient simulating the glint on the edge of cut glass.
  - Vividly colored background elements to emphasize the blur.

### 17. Claymorphism (2021–2023)
* **Origin**: Friendly 3D web and playful design.
* **Philosophy**: Tactile coziness and warmth through cute, friendly modeled-clay shapes.
* **Formal Attributes**:
  - Very rounded corners (`rounded-3xl` or `rounded-full`).
  - A soft inner shadow at the top to give a sense of inflation, and a diffuse outer shadow with a colored tint.
  - Sweet pastel colors.

---

## 🚀 Family 4: Contemporary Avant-Garde & Anti-AI Styles (2024 – 2026+)

### 18. Bento Grid (Modularity & Density)
* **Origin**: Apple promo pages, Linear, Raycast.
* **Philosophy**: High information density presented cleanly, scannably, and compartmentalized.
* **Formal Attributes**:
  - Modular grid with cells of varying proportions (1x1, 2x1, 1x2, 2x2).
  - Contained rounded corners (8px to 16px) and subtle low-opacity borders.
  - Each cell tells a visual micro-narrative with dedicated graphics.

### 19. Tactile Brutalism & Engineered Minimalism
* **Origin**: Linear, Stripe Press, Vercel.
* **Philosophy**: Software architecture treated as high-precision craftsmanship.
* **Formal Attributes**:
  - Near-black background (`#080A0A`).
  - 1px semi-transparent *hairline borders* (`rgba(255, 255, 255, 0.06)`).
  - Elevation through *surface ladders* (subtle luminance instead of heavy shadows).
  - Technical micro-typography at 10px–11px mono uppercase with expanded tracking.
  - *Single-accent* philosophy (a single vibrant accent color used with extreme moderation).

### 20. Neo-Brutalism / Nu-Brutalism
* **Origin**: Figma, Gumroad, Retool, Substack.
* **Philosophy**: Rejection of corporate coldness and sterility; an affirmation of raw confidence and attitude.
* **Formal Attributes**:
  - Solid black borders from 2px to 4px.
  - Hard offset shadows with zero blur (`box-shadow: 4px 4px 0px #000000`).
  - Ultra-saturated colors in high contrast.
  - Buttons that physically sink on hover/active (`transform: translate(2px, 2px)` with a reduced shadow).

### 21. Editorial / Archive Luxury
* **Origin**: Kinfolk, Readymag, independent fashion magazines, Stripe Press.
* **Philosophy**: The slowness and prestige of print publishing transposed to the digital experience.
* **Formal Attributes**:
  - Generous asymmetric margins that let the content breathe.
  - Numbered footnotes, imposing drop caps, and Roman numerals.
  - Monumental display serifs (*Instrument Serif*, *Fraunces*, *Editorial New*) paired with a neutral sans-serif.
  - Large-scale authorial photography with custom art direction.

### 22. Organic / Solarpunk / Biophilic Design
* **Origin**: Contemporary ecological and regenerative design movements.
* **Philosophy**: The digital as a reflection of nature's organic patterns and biological calm.
* **Formal Attributes**:
  - Fluid shapes with organic curves, no sharp straight corners.
  - Botanical color palettes: moss greens, terracotta, earthy mustard, raw off-white (`#F9F8F6`).
  - Subtle imperfect textures: recycled paper, linen, and light wood.
  - Slow, gentle microinteractions that reduce cognitive anxiety.

### 23. Cyberpunk / Dark Sci-Fi HUD
* **Origin**: Fictional science-fiction interfaces (FUI), games such as Cyberpunk 2077.
* **Philosophy**: The aesthetic of futuristic high technology and the surveillance of advanced systems.
* **Formal Attributes**:
  - Absolute black background (`#000000`).
  - Military HUD details: 45-degree chamfered corners, calibration reticles at the card vertices.
  - Acidic neon colors at extremely high contrast: electric cyan (`#00F0FF`) and magenta (`#FF003C`).
  - Telemetry lines and monospaced elements with system data.

### 24. Acid Graphics / Deconstructivist Anti-Design
* **Origin**: 1990s rave culture revisited by the post-internet avant-garde (David Carson, digital underground).
* **Philosophy**: Deliberate breaking of any grid and conventional good-taste standard in the name of pure visual expressiveness.
* **Formal Attributes**:
  - Deformed, liquefied (*liquid chrome*), stretched typography.
  - Chaotic digital collages in overlapping layers with no containment in boxes.
  - A mix of medieval Gothic fonts (Blackletter) with mono fonts and esoteric symbols.
