# Frutiger Aero Gloss Components

## 🛠️ Implementation Notes & Pure CSS Components

Use `<button class="aero-btn"><span class="aero-label">Action</span></button>` and `<a class="aero-tab is-active" href="#panel"><span class="aero-label">Panel</span></a>`; keep label ink unfiltered above the specular layers. The local opaque label backing protects the text while the surrounding capsule retains its gloss. Check rest, hover, pressed and forced-color states.

Modular CSS architecture reproducing authentic Frutiger Aero controls with modern CSS features (`backdrop-filter`, pseudo-elements, and forced-colors mode):

```css
/* ==========================================================================
   1. AERO GLOSS BUTTON (.aero-btn)
   Compound 3D Convex Gel Capsule with 50% Razor Specular Split
   ========================================================================== */
.aero-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 28px;
  font-family: var(--aero-font-body);
  font-size: 14px;
  font-weight: 700;
  color: var(--aero-white);
  text-decoration: none;
  cursor: pointer;
  user-select: none;
  border-radius: var(--aero-radius-pill);
  outline: none;
  overflow: hidden;
  isolation: isolate;

  /* Base Layer: Deep chromatic gradient */
  background: linear-gradient(
    180deg,
    #42b4f6 0%,
    var(--aero-sky-500) 48%,
    var(--aero-sky-600) 52%,
    var(--aero-sky-800) 100%
  );
  border: 1px solid var(--aero-sky-950);

  /* Dual Inner Highlight & Contact Drop Shadow */
  box-shadow:
    var(--aero-bevel-top-highlight),
    var(--aero-bevel-bottom-bounce),
    0 4px 10px rgba(0, 45, 82, 0.25);

  text-shadow: 0 -1px 1px rgba(0, 37, 68, 0.75);
  transition: all 180ms cubic-bezier(0.2, 0.8, 0.4, 1);
}

/* 50% Razor-Sharp Top Specular Crescent */
.aero-btn::before {
  content: "";
  position: absolute;
  top: 1px;
  left: 2px;
  right: 2px;
  height: 48%;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.85) 0%,
    rgba(255, 255, 255, 0.45) 45%,
    rgba(255, 255, 255, 0.15) 95%,
    rgba(255, 255, 255, 0.00) 100%
  );
  border-top-left-radius: var(--aero-radius-pill);
  border-top-right-radius: var(--aero-radius-pill);
  border-bottom-left-radius: 40% 15%;
  border-bottom-right-radius: 40% 15%;
  pointer-events: none;
  z-index: 1;
}

/* Secondary Belly Glow (Bottom Desk Reflection) */
.aero-btn::after {
  content: "";
  position: absolute;
  bottom: 1px;
  left: 15%;
  right: 15%;
  height: 30%;
  background: radial-gradient(
    ellipse at 50% 100%,
    rgba(255, 255, 255, 0.45) 0%,
    rgba(255, 255, 255, 0.00) 80%
  );
  border-radius: var(--aero-radius-pill);
  pointer-events: none;
  z-index: 1;
}

.aero-btn:hover {
  background: linear-gradient(180deg, #5ac4ff 0%, #42b4f6 48%, #1ca0f2 52%, #087fd0 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 1), var(--aero-bevel-bottom-bounce), var(--aero-aura-cyan);
  transform: translateY(-1px);
}

.aero-btn:active {
  transform: translateY(1px);
  background: linear-gradient(180deg, var(--aero-sky-800) 0%, var(--aero-sky-600) 48%, var(--aero-sky-500) 52%, #42b4f6 100%);
  box-shadow: inset 0 2px 4px rgba(0, 25, 55, 0.60), inset 0 -1px 1px rgba(255, 255, 255, 0.40), 0 1px 3px rgba(0, 0, 0, 0.30);
  text-shadow: 0 1px 1px rgba(0, 37, 68, 0.75);
}

.aero-label {
  position: relative;
  z-index: 2;
  padding: 0.1em 0.35em;
  border-radius: 0.25em;
  background: #002544;
  color: #FFFFFF;
  text-shadow: none;
}
@media (forced-colors: active) {
  .aero-label { background: ButtonFace; color: ButtonText; }
}

/* Dual-Contrast Focus Ring for WCAG 2.2 SC 1.4.11 */
.aero-btn:focus-visible {
  outline: 2px solid var(--aero-sky-950);
  outline-offset: 3px;
  box-shadow: 0 0 0 5px var(--aero-white), var(--aero-aura-cyan);
}

/* ==========================================================================
   2. AERO WINDOW CONTAINER (.aero-window)
   Translucent Acrylic Chassis with 45° Caustic Light Streak & Content Sanctuary
   ========================================================================== */
.aero-window {
  width: 100%;
  max-width: 680px;
  background: var(--aero-glass-wash);
  backdrop-filter: blur(12px) saturate(140%);
  -webkit-backdrop-filter: blur(12px) saturate(140%);
  border-radius: var(--aero-radius-lg);
  border: 1px solid var(--aero-glass-border);
  box-shadow: var(--aero-shadow-window), inset 0 1px 0 rgba(255, 255, 255, 0.90);
  overflow: hidden;
}

.aero-window-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.55) 0%,
    rgba(255, 255, 255, 0.25) 49%,
    rgba(210, 238, 252, 0.20) 50%,
    rgba(168, 222, 249, 0.35) 100%
  );
  border-bottom: 1px solid rgba(0, 45, 82, 0.15);
  overflow: hidden;
}

/* 45° Diagonal Caustic Flare Reflection */
.aero-window-header::before {
  content: "";
  position: absolute;
  top: -50px;
  left: -20px;
  width: 120px;
  height: 200px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.00) 0%,
    rgba(255, 255, 255, 0.45) 45%,
    rgba(255, 255, 255, 0.00) 70%
  );
  transform: rotate(25deg);
  pointer-events: none;
}

.aero-window-title {
  font-family: var(--aero-font-body);
  font-size: 13px;
  font-weight: 700;
  color: #122130;
  text-shadow: 0 0 6px #ffffff, 0 0 10px #ffffff, 0 1px 2px rgba(255, 255, 255, 0.85);
}

/* Dense reading field: verify the actual alpha composite and ink pair. */
.aero-window-body {
  background: rgba(255, 255, 255, 0.95);
  padding: 24px;
  color: #1a2530;
  font-family: var(--aero-font-body);
  font-size: 14px;
  line-height: 1.6;
}

/* ==========================================================================
   3. SEGMENTED TAB CAPSULE (.aero-tab-group)
   Wii Channels / OS X Recessed Trough with Glossy Sliding Pill
   ========================================================================== */
.aero-tab-group {
  display: inline-flex;
  padding: 3px;
  background: linear-gradient(180deg, #d4dee5 0%, #f0f4f8 100%);
  border: 1px solid #a6b5c0;
  border-radius: var(--aero-radius-pill);
  box-shadow: inset 0 2px 4px rgba(0, 30, 60, 0.20), 0 1px 0 rgba(255, 255, 255, 0.85);
  gap: 2px;
}

.aero-tab {
  padding: 6px 18px;
  font-family: var(--aero-font-body);
  font-size: 13px;
  font-weight: 600;
  color: #3b5062;
  text-decoration: none;
  border-radius: var(--aero-radius-pill);
  border: 1px solid transparent;
  transition: all 180ms ease;
}

.aero-tab.is-active {
  color: var(--aero-white);
  background: linear-gradient(180deg, var(--aero-sky-300) 0%, var(--aero-sky-500) 48%, var(--aero-sky-600) 52%, var(--aero-sky-800) 100%);
  border: 1px solid var(--aero-sky-950);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85), 0 2px 6px rgba(0, 35, 70, 0.30);
  text-shadow: 0 -1px 0 rgba(0, 35, 70, 0.70);
}

/* ==========================================================================
   4. ACCESSIBILITY OVERRIDES (WCAG 2.2)
   ========================================================================== */
@media (prefers-reduced-motion: reduce) {
  .aero-btn, .aero-tab { transition: none !important; transform: none !important; }
  .aero-window-header::before { display: none !important; }
}

@media (forced-colors: active) {
  .aero-btn, .aero-tab.is-active {
    border: 2px solid ButtonText !important;
    background: ButtonFace !important;
    color: ButtonText !important;
  }
  .aero-btn::before, .aero-btn::after { display: none !important; }
  .aero-window { border: 2px solid WindowText !important; background: Window !important; }
}
```

---


Historical bibliography: [parent skill](../SKILL.md#-sources--further-reading). Recipes are illustrative and require rendered state verification.
