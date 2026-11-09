# Showcase Integration Architecture (`estilos-visuais`)

This reference document outlines the integration between the Coacus framework and its live partner showcase repository at `/home/daniel/Code/estilos-visuais`.

---

## 1. Overview & Architectural Role

The **Estilos Visuais** showcase provides an interactive visual testbed and demonstration harness for all 82 canonical UI design styles curated within Coacus (`knowledge/skills/domains/design/ui-style-*`). It allows engineers, designers, and autonomous agents to preview, stress-test, and benchmark design tokens, optical surfaces, typography pairings, and micro-interactions across production components in real time.

---

## 2. Directory & Component Layout

```
estilos-visuais/
├── index.html              # Shell scaffold, ARIA tablist navigation, 4 demonstrative views
├── app.js                  # State router (#slug/view), CSS loader, Driver.js tours, FX lifecycle
├── shell.css               # Isolated CSS styling for the chrome, sidebar, and controls
├── vendor/                 # Locally vendorized libraries (offline-first, zero CDN dependency)
│   ├── driver.js           # Driver.js v1.3+ core engine
│   └── driver.css          # Driver.js presentation stylesheet
├── styles/
│   ├── base.css            # Common layout components for stage views
│   ├── registry.js         # Central manifest of 82 styles across 7 thematic families
│   ├── <slug>.css          # 82 pure stylesheets scoped to #stage[data-style="<slug>"]
│   └── fx/                 # Modular FX engines
│       ├── atompunk.js
│       ├── cassette-futurism.js
│       ├── cyberpunk.js
│       ├── glassmorphism.js
│       ├── lunarpunk.js
│       ├── neo-brutalism.js
│       ├── pop-art-halftone.js
│       ├── psychedelic-60s.js
│       ├── steampunk.js
│       ├── synthwave.js
│       └── y2k-revival.js
```

---

## 3. Four Demonstrative Component Views

Rather than displaying static placeholder cards, the showcase renders four comprehensive, fully styled views inside `#stage`:

1. **Painel (`view-painel`):** Executive summary dashboard with key metric stat cards, primary conversion actions, visual status indicators, and an interactive telemetry stream.
2. **Projetos (`view-projetos`):** Kanban project management board containing three columnar lanes (*A Fazer*, *Em Progresso*, *Concluído*), priority chips, task cards, and assignee avatars.
3. **Equipe (`view-equipe`):** Modular team directory presenting user avatar profiles, role descriptions, contact actions, and online presence badges.
4. **Relatórios (`view-relatorios`):** High-density financial and system performance telemetry table with status pills, numerical columns, and date stamps.

Navigation between views is governed by WAI-ARIA `role="tablist"` tabs in the top header. Clicking a view tab switches active panels without resetting or interrupting the selected visual style.

---

## 4. State Router & Deep-Linking

The showcase maintains state through the URL hash:
```
https://showcase.local/#<style-slug>/<view-id>
```
Example: `index.html#windows-xp/projetos` loads the Windows XP Luna Blue theme and immediately activates the Kanban board view.

---

## 5. Driver.js Interactive Onboarding & Feature Tours

The showcase embeds [Driver.js](https://driverjs.com/) vendorized locally in `vendor/driver.js` (zero external CDN network requests):

1. **Welcome Tour (`startWelcomeTour()`):** Triggers automatically on the user's first visit (stored in `localStorage.getItem('ev_tour_welcome_seen')`) or manually via the "Tour" header button. Highlights:
   - Visual Style Picker & Search filter in the sidebar.
   - Demonstrative View Tabs (`Painel`, `Projetos`, `Equipe`, `Relatórios`).
   - Theme Inversion & Code Inspection drawer.
2. **Per-Style Feature Tour (`startStyleTour(slug)`):** Triggers when a user selects a style for the first time. Steps highlight the unique historical DNA, specific typography choices, and optical surface physics of the active aesthetic.

---

## 6. Modular FX Engine Lifecycle

Interactive animation effects reside in `styles/fx/<slug>.js`. Every FX module must conform to the following contract:

```javascript
// Example: styles/fx/<slug>.js
export default function mount(stage) {
  // 1. Check prefers-reduced-motion immediately
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return () => {}; // No-op cleanup
  }

  // 2. Setup listeners, canvas, or animation frames
  const timer = setInterval(() => { /* ... */ }, 1000);

  // 3. Return mandatory teardown closure
  return () => {
    clearInterval(timer);
    // Remove injected DOM nodes, listeners, and custom properties
  };
}
```

When switching styles, `app.js` invokes the previous style's returned cleanup closure before mounting the next style, preventing memory leaks, stale listeners, and overlapping animations.

---

## 7. Synchronization Protocol

When adding or updating a UI style:
1. **Coacus Authority:** Edit or create `knowledge/skills/domains/design/ui-style-<slug>/SKILL.md` following `docs/standards/ui-style-architecture.md`.
2. **Showcase Style Sheet:** Mirror tokens and classes into `estilos-visuais/styles/<slug>.css`.
3. **Showcase Registry:** Register the style entry in `estilos-visuais/styles/registry.js` with metadata and `fx: true` if an FX engine is provided.
4. **Deterministic Validation:** Run `python3 scripts/coacus.py validate` and `python3 scripts/coacus_design_lint.py knowledge/skills/domains/design/`.
