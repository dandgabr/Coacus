---
name: "ui-style-biopunk"
description: "Provides the canonical Biopunk & Synthetic Biology UI style (1988-present): biological sci-fi and DIY-bio culture featuring dark sterile laboratory slate, fluorescent GFP bioluminescence, cellular membrane optics, DNA sequence ribbons, gel electrophoresis progress meters, and ethical lab telemetry. Use when designing synthetic biology platforms, genomics tools, citizen science labs, or genetic sci-fi entertainment portals."
---

# UI Style: Biopunk & Synthetic Biology

**Biopunk** is the speculative fiction genre and design language in which biotechnology, genomics, and organic wetware—rather than mechanical silicon cyberware—form the foundation of society, power, and resistance. Translating the aesthetics of synthetic biology laboratories, black-market gene clinics, and DIY citizen-science incubators, Biopunk interfaces combine sterile slate environments with vibrant green fluorescent protein (GFP) emission, translucent cellular membranes, gel electrophoresis telemetry, and clinical nucleotide sequence readouts.

---

## 🧭 When to Activate

- Designing scientific interfaces, protocol workflows, DNA sequence browsers, or sample tracking dashboards for biotechnology, bioinformatics, and genomics platforms.
- Developing video games, speculative worldbuilding portals, or interactive fiction focused on biohacking, cloning, genetic synthesis, or transhuman mutation.
- Building open-source biology, citizen-science, or environmental telemetry hubs celebrating scientific literacy and transparent lab records.

---

## 🕰️ Definition, Lineage, and Timeline

- **Origins & Coinage:** First coined in 1988 by Czech biologist and science-fiction writer Eva Hauserová as a biological response to cyberpunk, and expanded in Paul Di Filippo's *Ribofunk* (1996). Early literary precursors include H. G. Wells's *The Island of Doctor Moreau* (1896) and Greg Bear's *Blood Music* (1985).
- **The DIYbio Movement:** Galvanized in the physical world by Meredith Patterson's *A Biopunk Manifesto* (2010), advocating for open-access scientific literacy, decentralized laboratories, and democratization of biological research outside corporate oligopolies.
- **Distinctions from Neighboring Styles:**
  - Unlike **Cyberpunk** (dry silicon, copper circuitry, neon-noir rain, cyberdecks), Biopunk operates on wetware: proteins, viral vectors, agar plates, DNA polymers, and enzymatic reactions.
  - Unlike **Organic Biophilic** (tranquil green leaves, sunlight, natural wood, wellness calm), Biopunk is tense, engineered, visceral, clinical, and provocative.
  - Unlike **Nanopunk** (molecular assemblers, carbon nanotubes, crystal lattices), Biopunk focuses specifically on living organic cells, genomes, and biological replication.
- **Absolute Veto:** Biopunk is NOT generic medical clinic software or gratuitous body-horror gore. Gratuitous mutilation, ungrounded pseudo-scientific health cures, and illegible dripping slime fonts are strictly forbidden.

---

## 🎨 Visual DNA & Subgenre Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  BIOPUNK VISUAL MATRIX                                 │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. Clinical Genome Foundry │ 2. Black Clinic Underground│ 3. Open-Lab Citizen Science  │
│ • Sterile dark slate       │ • Visceral flesh & magenta │ • Petri-dish agar amber      │
│ • GFP fluorescent lasers   │ • Exposed vascular ribbons │ • Gel-electrophoresis scales │
│ • Precise nucleotide mono  │ • High-contrast warning UV │ • Graph protocol notebooks   │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

- **Palette & Radiance:** Sterile laboratory slate (`#0F1A17`), deep agar black (`#070D0B`), fluorescent GFP green (`#7CFF6B`), cold fluorescence cyan (`#2EE8C2`), visceral enzyme magenta (`#E0457B`), bile yellow (`#C7D63B`), and cold clinical white (`#EEF5F1`).
- **Form Factors & Framing:** Rounded membrane borders (`border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%`), 1px luminescent laser hairline dividers, and specimen bracket overlays.
- **Textures & Micro-patterns:** Translucent cell wall diffusion, SVG turbulence fluid membranes, gel electrophoresis band migrations, and running nucleotide strings (`ATCG-GCTA`).

---

## 📐 Lighting Physics, Specular Splits & Surfaces

1. **Fluorescent Protein (GFP) Bioluminescence:**
   - Intense chromatic emission radiating outward from a sterile dark petri substrate.
   ```css
   background: radial-gradient(circle at 50% 40%, rgba(124, 255, 107, 0.15) 0%, rgba(15, 26, 23, 0.98) 100%);
   border: 1px solid rgba(124, 255, 107, 0.45);
   box-shadow: 0 0 25px rgba(124, 255, 107, 0.18), inset 0 0 15px rgba(124, 255, 107, 0.1);
   ```
2. **Agar Membrane Specular Sheen:**
   - High-gloss organic liquid surface tension simulating nutrient agar in a glass dish.
   ```css
   background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(46, 232, 194, 0.05) 50%, rgba(0, 0, 0, 0.4) 100%);
   backdrop-filter: blur(8px);
   box-shadow: inset 1px 1px 0 rgba(255, 255, 255, 0.2), 0 8px 32px rgba(0, 0, 0, 0.5);
   ```

---

## 🏷️ Complete Design Tokens

```css
:root {
  /* Laboratory Environments */
  --bio-slate-bg: #0F1A17;
  --bio-agar-black: #070D0B;
  --bio-surface: #172420;
  --bio-surface-light: #20312C;
  --bio-clinical-white: #EEF5F1;

  /* Fluorophores & Emissions */
  --bio-gfp-green: #7CFF6B;
  --bio-gfp-glow: rgba(124, 255, 107, 0.35);
  --bio-cyan-laser: #2EE8C2;
  --bio-cyan-glow: rgba(46, 232, 194, 0.3);
  --bio-flesh-magenta: #E0457B;
  --bio-bile-yellow: #C7D63B;

  /* Scientific Dividers & Borders */
  --bio-border-hairline: rgba(124, 255, 107, 0.25);
  --bio-border-active: #7CFF6B;
  --bio-membrane-radius: 8px;

  /* Typography */
  --bio-font-display: 'Space Grotesk', 'Rajdhani', sans-serif;
  --bio-font-data: 'IBM Plex Mono', 'Space Mono', monospace;
  --bio-font-body: 'Inter', -apple-system, sans-serif;
}
```

---

## 🔤 Typography & Lettering Architecture

- **Primary Display Headings:** Precision futuristic sans-serifs (*Space Grotesk*, *Rajdhani*) featuring clean mechanical geometry with slight bio-organic flare.
- **Data Readouts & Nucleotide Sequences:** Fixed-pitch monospaced fonts (*IBM Plex Mono*, *Space Mono*) for sample lots, molecular weights (kDa), base pairs (bp), and protocol steps.
- **Body & Protocol Text:** Crisp, neutral neutral grotesque (*Inter*, *IBM Plex Sans*) ensuring maximum legibility during rapid laboratory triage.

---

## 🖱️ Interaction Dynamics, Sound Cues & Motion

- **Membrane Osmosis Hover:** Cards and interactive elements expand with subtle organic fluid tension (`border-radius` morphing by 2-4% on hover).
- **Gel Electrophoresis Progress:** Loading bars advance as migrating translucent protein bands under simulated ultraviolet light.
- **Bioluminescent Pulse:** Status indicators breathe with slow, circadian biological rhythm (3-4 second cycle periods).
- **Motion Reduction:** When `prefers-reduced-motion: reduce` is detected, fluid membrane morphing and pulsing glows halt into stable static borders.

---

## 🧩 Canonical Component Specifications

### 1. Specimen Incubator Card (`.bio-specimen-card`)
A dark slate container with nucleotide lot identification and fluorescent GFP hairline accents.
```html
<article class="bio-specimen-card">
  <div class="bio-card-header">
    <span class="bio-lot-tag">LOT: BAC-9904 // CRISPR-v3</span>
    <h3 class="bio-title">Bioluminescent Assay</h3>
  </div>
  <p class="bio-metric">Target: Luciferase reporter plasmid • Transfection Efficiency: 94.2%</p>
</article>
```
```css
.bio-specimen-card {
  background: var(--bio-surface);
  border: 1px solid var(--bio-border-hairline);
  border-radius: var(--bio-membrane-radius);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(124, 255, 107, 0.04);
  padding: 1.75rem;
  position: relative;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.bio-specimen-card:hover {
  border-color: var(--bio-border-active);
  box-shadow: 0 6px 24px rgba(124, 255, 107, 0.15), inset 0 0 20px rgba(124, 255, 107, 0.08);
}
.bio-lot-tag {
  font-family: var(--bio-font-data);
  font-size: 0.75rem;
  color: var(--bio-cyan-laser);
  letter-spacing: 0.08em;
  display: block;
  margin-bottom: 0.5rem;
}
```

### 2. Fluorescent Assay Action Button (`.bio-btn`)
An action button glowing with green fluorescent emission against dark slate.
```css
.bio-btn {
  background: rgba(124, 255, 107, 0.12);
  color: var(--bio-gfp-green);
  border: 1px solid var(--bio-gfp-green);
  font-family: var(--bio-font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.7rem 1.6rem;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(124, 255, 107, 0.2);
  transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.1s ease;
}
.bio-btn:hover {
  background: var(--bio-gfp-green);
  color: #070D0B;
  box-shadow: 0 0 20px rgba(124, 255, 107, 0.45);
  transform: translateY(-1px);
}
.bio-btn:active {
  transform: translateY(1px);
}
```

### 3. Electrophoresis Telemetry Rail (`.bio-progress-rail`)
A progress tracker simulating stained DNA fragments migrating under ultraviolet electrophoresis.

### 4. Nucleotide Sequence Header (`.bio-sequence-banner`)
A dense header ribbon continuously displaying active base-pair coordinates (`A-T-C-G`).

---

## ♿ Accessibility & Environmental Contrast (WCAG 2.2)

- **Luminescent Contrast:** Fluorescent GFP green (`#7CFF6B`) on dark laboratory slate (`#0F1A17`) yields an extraordinary contrast ratio of 12.4:1; cold clinical white (`#EEF5F1`) achieves 15.6:1 (surpassing WCAG AAA requirements).
- **Hazard Accents:** Saturated magenta (`#E0457B`) must be restricted to borders or large icons, or paired with a minimum 4.5:1 text backing.
- **Photosensitivity Protections (WCAG 2.3.1):** Ultraviolet flicker animations and cellular pulses must never exceed 2.0 Hz.
- **Focus Indicators:** Neon green double ring with 2px offset (`outline: 2px solid var(--bio-gfp-green); outline-offset: 3px;`).

---

## ✅ When to Use / ❌ When to Avoid

### Ideal Use Cases
- Biotech enterprise dashboards, DNA sequencing viewers, and wet-lab automated workflow tools.
- Sci-fi gaming portals, bio-cybernetic character planners, and speculative biology literature.
- Citizen science documentation, open-source genetics databases, and CRISPR research archives.

### Anti-Patterns & Prohibitions
- Consumer mental health counseling or physical wellness portals where clinical biohazard tension induces anxiety.
- Standard corporate HR or accounting software.
- Commercial medical claims advertising unregulated home genetic treatments.

---

## 📚 Authoritative Sources & Historical Artifacts

- Eva Hauserová, "Biopunk: Notes on a Developing Subgenre", *Ikarie XB-1*, 1988/1990.
- Meredith Patterson, *A Biopunk Manifesto*, UCLA Outlaw Biology Symposium, 2010.
- Paul Di Filippo, *Ribofunk*, Four Walls Eight Windows, 1996.
- Gregory Stock, *Redesigning Humans: Choosing Our Genes, Changing Our Future*, Houghton Mifflin, 2002.

---

## 🔗 Cross-Skill Integration & Dialect Relations

- **Sibling Speculative Styles:** [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-nanopunk](../ui-style-nanopunk/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md).
- **Scientific & Data Peers:** [ui-style-dark-mode-first](../ui-style-dark-mode-first/SKILL.md), [ui-style-terminal-tui](../ui-style-terminal-tui/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md).
## Appearance and Interaction Verification

Give electrophoresis progress a stable numerical/semantic value and label; stop decorative band travel without hiding progress, and use shape/text alongside fluorescence for sample state.
