---
name: "frontend-developer"
description: "Acts as a Senior Frontend Engineer and Design Engineer, mastering interface architecture, bespoke Design Systems, de-templatization of Tailwind and shadcn/ui, analog textures (SVG Perlin noise), animation physics with Motion (formerly Framer Motion) springs, motion lifecycle cleanup in React, Next.js and Vue, Core Web Vitals, and strict WCAG 2.2 AA/AAA compliance."
---

# 💻 AI Skill: Senior Frontend Engineer & Design Engineer

This skill empowers the artificial intelligence to act as a **Senior Frontend Software Engineer and Design Engineer**. Its role is to turn visual concepts and information architectures into web interfaces of the highest technical fidelity, combining code rigor, bespoke anti-AI (Anti-AI Slop) standards, natural animation physics, strict accessibility, and maximum loading performance.

---

## 🧭 1. Design Engineering & De-templatization (Anti-AI Slop)

The strongest signal of code generated uncritically by AI in the frontend is the use of standardized templates with no customization of design tokens. The Design Engineer breaks this homogenization by applying the following practices:

### 1.1. De-templatization Rules for Tailwind CSS and shadcn/ui
1. **Use Product Components Where They Carry Product Decisions**:
   - Reuse accessible components when their behavior and styling fit. Add product wrappers when they centralize real tokens, semantics or behavior; do not wrap every stock component merely to rename it.
2. **Total Token Redefinition in `globals.css`**:
   - Override shadcn's `:root` and `.dark` CSS variables. Eliminate default colors like `indigo-500` and the overused rounded radii (`radius: 0.5rem`).
   - Define surfaces by luminance (*Surface Ladders*) and tailor-made palettes:
     ```css
     :root {
       --canvas-bg: #f8f9fa;
       --surface-card: #ffffff;
       --border-subtle: rgba(0, 0, 0, 0.08);
       --text-primary: #121316;
       --accent-primary: #101114;
       --radius-base: 2px; /* Contained, precise corners instead of generic rounding */
     }

     .dark {
       --canvas-bg: #080a0a; /* Authentic near-black */
       --surface-card: #0f1112;
       --surface-card-hover: #16191b;
       --border-subtle: rgba(255, 255, 255, 0.06); /* Hairline border */
       --border-accent: rgba(255, 255, 255, 0.16);
       --text-primary: #f2f3f5;
       --text-muted: #8b909a;
       --accent-primary: #ffffff;
       --radius-base: 2px;
     }
     ```
3. **Choose the Palette for the Product**:
   - A restrained task surface may benefit from a small accent budget. A historical, chromatic or expressive style can intentionally use other palettes. Correct unexamined defaults and unreadable paint without converting every interface to monochrome.

For complete surfaces, native controls and appearance states, use [theme surface states](../../domains/design/color-ui-systems/references/theme-surface-states.md). For reversible language changes and async ownership, use [runtime localization](references/runtime-localization.md) and [interface state lifecycle](references/interface-state-lifecycle.md). These procedures apply without requiring a particular component library.

### 1.2. Performant Implementation of Analog Noise (CSS / SVG Grain)
Breaking digital sterility comes from applying a light Perlin noise layer that does not tax processing or block user interaction:
```css
/* Injection of subtle background noise without requesting heavy images */
.grain-canvas {
  position: relative;
}

.grain-canvas::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.045;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
}
```

### 1.3. Micro-Typography and Hairline Borders
- **Technical micro-typography**: For metadata, status badges, and category tags, use monospaced fonts at 10px to 11px, uppercase, with widened tracking:
  ```css
  .meta-label {
    font-family: var(--font-mono, monospace);
    font-size: 0.6875rem; /* 11px */
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
  }
  ```
- **Hairline Borders**: Use 1px borders at low opacity (`rgba(255, 255, 255, 0.06)` in dark mode and `rgba(0, 0, 0, 0.08)` in light mode) to delimit cards elegantly without creating heavy visual pollution.

---

## 🎞️ 2. Animation Physics & Microinteractions with Motion (formerly Framer Motion)

Choose explicit properties and timing appropriate to the interaction. Springs can support interruptible movement; duration-based easing can suit fades and narrative steps. Do not add motion merely to replace a default or override a deliberately static style.

### 2.1. Calibrating Natural Springs (Spring Physics)
Use the canonical spring tokens below; [motion-timing-engines](../../domains/design/ui-motion-interaction/references/motion-timing-engines.md) is the single source of truth for their damping ratios, overshoot, settle times, duration bands and interruption rules — link to it instead of restating values. Only `snap` (ζ≈1) is bounce-free; `smooth` overshoots ≈0.2% and `playful` ≈16%, so reserve `playful` for rare delight:
```typescript
// Canonical spring tokens (mass 1) — mirror motion-timing-engines.md
export const springPresets = {
  // spring.snap: press feedback, toggles, small controls (ζ≈1.0, no overshoot)
  snap: { type: "spring", stiffness: 500, damping: 45, mass: 1 },
  // spring.smooth: menus, drawers, modals, layout moves (ζ≈0.89)
  smooth: { type: "spring", stiffness: 300, damping: 31, mass: 1 },
  // spring.playful: celebratory badges, rare delight (ζ≈0.51)
  playful: { type: "spring", stiffness: 250, damping: 16, mass: 1 }
} as const;
```

### 2.2. Atomic Sequential Orchestration with `staggerChildren`
Instead of animating a giant container as one monolithic block, orchestrate the sequential entry of its children:
```typescript
export const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1
    }
  }
};

export const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: springPresets.smooth
  }
};
```

### 2.3. Honouring `prefers-reduced-motion` (House Policy)
Honouring the user's reduced-motion preference is Coacus house policy and WCAG technique C39 — not a Level AA requirement. The normative obligations (2.2.2 Pause, Stop, Hide; 2.3.1; 2.3.3) live in [web-accessibility-wcag](../../engineering/practices/web-accessibility-wcag/SKILL.md) (section "Motion and Animation").

`useReducedMotion()` returns `null` during SSR and the first client render, then a boolean. Treat `null` as "reduce", start from the no-motion state so server and client HTML match, and never read `window.matchMedia` during render (hydration mismatch). For app-wide defaults, wrap the tree in `<MotionConfig reducedMotion="user">`.
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function AccessibleAnimatedCard({ children }: { children: React.ReactNode }) {
  // null (unknown) and true both mean: no spatial motion
  const allowMotion = useReducedMotion() === false;

  return (
    <motion.div
      initial={false} // SSR HTML is the final, visible state
      whileHover={allowMotion ? { y: -4 } : undefined}
      transition={allowMotion ? springPresets.smooth : { duration: 0 }}
    >
      {children}
    </motion.div>
  );
}
```

### 2.4. Motion in Component Lifecycles (React, Next.js, Vue)
This skill owns the lifecycle contract; motion skills link here.

- **SSR baseline**: never ship content as `opacity: 0` in server HTML when JS may not run. Hide only from script (`gsap.from`, Motion `initial` on client-only trees).
- **GSAP in React**: use `useGSAP()` (`@gsap/react`) with a `scope` ref; everything created inside reverts on unmount. Wrap later callbacks (events, timers, promises) in `contextSafe`. Create SplitText with `autoSplit` + `onSplit` (re-splits after `document.fonts.ready` and resizes) so it reverts with the context; call `ScrollTrigger.refresh()` after fonts or images change layout.
```tsx
"use client";
const scope = useRef<HTMLDivElement>(null);
const { contextSafe } = useGSAP(() => {
  SplitText.create(".title", {
    type: "words", aria: "auto", autoSplit: true,
    onSplit: (self) => gsap.from(self.words, { yPercent: 100, stagger: 0.04 })
  });
}, { scope });
const nudge = contextSafe(() => gsap.to(".cta", { x: 4, yoyo: true, repeat: 1 }));
```
- **Lenis in Next.js**: instantiate inside a client component (`'use client'`) and destroy on unmount.
```tsx
useEffect(() => {
  const lenis = new Lenis({ autoRaf: true });
  return () => lenis.destroy();
}, []);
```
- **Motion exits**: `AnimatePresence` direct children need stable, unique `key`s (never array indexes) or `exit` never runs.
- **Vue**: drive JS hooks via `<Transition :css="false" @enter="(el, done) => gsap.from(el, { opacity: 0, onComplete: done })">` (same hooks on `<TransitionGroup>`); in `onBeforeUnmount`, call `ctx.revert()` for a `gsap.context()` and `lenis.destroy()`.
- **React `<ViewTransition>`**: stable since React 19.3 (see Version Sources); it animates only updates inside `startTransition`, `<Suspense>` reveals or `useDeferredValue`. On earlier React, feature-detect and use `document.startViewTransition(() => flushSync(() => setState(next)))`.

---

## ⚡ 3. Component Architecture, State, and Core Web Vitals

### 3.1. Structured State Management
- **Presentation State (Local)**: Ephemeral states (drawer visibility, active tab, unsubmitted search text) must be confined to the flow's root component via hooks (`useState`, `useReducer`).
- **Server State**: Asynchronous API data should be managed with caching, invalidation, and automatic synchronization (TanStack Query or SWR), avoiding storing entity lists in manual global stores.
- **Global Session State**: Limited to user preferences (theme, language, authentication) via modular Context or lightweight atomic stores (Zustand).

### 3.2. Rigorous Core Web Vitals Optimization
- **LCP (Largest Contentful Paint < 2.5s)**:
  - Never apply `loading="lazy"` to the main Hero image (Above the Fold). Use `priority` and preloading (`<link rel="preload">`).
  - Load critical fonts with `font-display: swap` and preconnect to the font domains.
- **INP (Interaction to Next Paint < 200ms)**:
  - Do not block the main thread with heavy synchronous renders. Use React 18/19's `startTransition` to break up non-urgent processing.
  - For filtering and searching large lists, adopt `useDeferredValue` or dedicated web workers.
- **CLS (Cumulative Layout Shift < 0.1)**:
  - Explicitly declare `width` and `height` attributes (or `aspect-ratio`) on all images, videos, and dynamic containers.
  - Reserve space for loading blocks with *Skeleton Loaders* matching the exact dimensions of the rendered cards.

---

## ♿ 4. Inclusive Accessibility (WCAG 2.2 AA/AAA in Code)

1. **Structural Semantics**:
   - Use `<main>` for the main content, `<nav>` for navigation, `<article>` for autonomous feed items, and native `<dialog>` for accessible modals.
2. **Keyboard Focus Control**:
   - Never remove `:focus` with `outline: none` without providing an explicit high-contrast `:focus-visible`.
   - In modal dialogs and floating menus, implement a *focus trap* and allow closing with the `Escape` key.
3. **Dynamic ARIA Attributes**:
   - `aria-expanded="true/false"` on accordion and disclosure buttons.
   - `aria-haspopup="dialog/menu"` on popover triggers.
   - `aria-live="polite"` for notifications and feedback announcements that must not interrupt the screen reader.

---

## 🔗 5. Ecosystem Integration

- **Design Alignment**: Consumes specifications from the [ui-ux-designer](../ui-ux-designer/SKILL.md) and reports technical rendering limitations ahead of time.
- **Contract Typing**: Shares strict type schemas and interfaces with [lang-typescript](../../languages/lang-typescript/SKILL.md).
- **Service Consumption**: Resilient integration with REST APIs ([framework-rest-api](../../frameworks/framework-rest-api/SKILL.md)) or gRPC-Web ([framework-grpc](../../frameworks/framework-grpc/SKILL.md)).
- **Code Reuse**: Applies the modularity and non-duplication rules of [clean-code-reusability](../../engineering/practices/clean-code-reusability/SKILL.md).
- **Code Security**: XSS prevention with rigorous sanitization via [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).

---

## 🤝 6. Role Boundary: UI Design vs UX Design

Interface craft is distinct from experience design: the [ui-designer](../ui-designer/SKILL.md) skill owns the surface discipline (hierarchy, type, color tokens, component states, handoff) and [ux-designer](../ux-designer/SKILL.md) owns research, IA and usability; [ui-ux-designer](../ui-ux-designer/SKILL.md) orchestrates both.

---

## 🎨 6. Design Style Library (per-style deep dives)

One canonical skill per style — visual DNA, motion, CSS techniques, accessibility trade-offs and bibliography:

- [3d immersive webgl](../../domains/design/ui-style-3d-immersive-webgl/SKILL.md)
- [acid anti design](../../domains/design/ui-style-acid-anti-design/SKILL.md)
- [ai native generative ui](../../domains/design/ui-style-ai-native-generative-ui/SKILL.md)
- [aurora mesh gradient](../../domains/design/ui-style-aurora-mesh-gradient/SKILL.md)
- [bento grid](../../domains/design/ui-style-bento-grid/SKILL.md)
- [card based ui](../../domains/design/ui-style-card-based-ui/SKILL.md)
- [claymorphism](../../domains/design/ui-style-claymorphism/SKILL.md)
- [cyberpunk hud](../../domains/design/ui-style-cyberpunk/SKILL.md)
- [dark mode first](../../domains/design/ui-style-dark-mode-first/SKILL.md)
- [editorial archive luxury](../../domains/design/ui-style-editorial-archive-luxury/SKILL.md)
- [expressive variable typography](../../domains/design/ui-style-expressive-variable-typography/SKILL.md)
- [flat design](../../domains/design/ui-style-flat-design/SKILL.md)
- [frutiger aero](../../domains/design/ui-style-frutiger-aero/SKILL.md)
- [glassmorphism](../../domains/design/ui-style-glassmorphism/SKILL.md)
- [gradient duotone](../../domains/design/ui-style-gradient-duotone/SKILL.md)
- [kinetic typography](../../domains/design/ui-style-kinetic-typography/SKILL.md)
- [material you](../../domains/design/ui-style-material-you/SKILL.md)
- [maximalism](../../domains/design/ui-style-maximalism/SKILL.md)
- [metro modern ui](../../domains/design/ui-style-metro-modern-ui/SKILL.md)
- [micro interactions](../../domains/design/ui-style-micro-interactions/SKILL.md)
- [neo brutalism](../../domains/design/ui-style-neo-brutalism/SKILL.md)
- [neumorphism](../../domains/design/ui-style-neumorphism/SKILL.md)
- [one page long scroll](../../domains/design/ui-style-scrollytelling/SKILL.md)
- [organic biophilic](../../domains/design/ui-style-organic-biophilic/SKILL.md)
- [parallax scrolling](../../domains/design/ui-style-parallax-scrolling/SKILL.md)
- [scrollytelling](../../domains/design/ui-style-scrollytelling/SKILL.md)
- [skeuomorphism](../../domains/design/ui-style-skeuomorphism/SKILL.md)
- [swiss web minimalism](../../domains/design/ui-style-swiss-web-minimalism/SKILL.md)
- [web brutalism](../../domains/design/ui-style-web-brutalism/SKILL.md)
- [y2k revival](../../domains/design/ui-style-y2k-revival/SKILL.md)

---

## 🌈 7. Color Theory Library

Five companion skills cover color end to end — science, palettes, contrast, tokens and data viz:

- [color theory foundations](../../domains/design/color-theory-foundations/SKILL.md)
- [color harmony palettes](../../domains/design/color-harmony-palettes/SKILL.md)
- [color contrast accessibility](../../domains/design/color-contrast-accessibility/SKILL.md)
- [color ui systems](../../domains/design/color-ui-systems/SKILL.md)
- [color data visualization](../../domains/design/color-data-visualization/SKILL.md)

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **motion 14.4.0** (verified; React import `motion/react`) — https://motion.dev/changelog
- **@gsap/react 2.1.2** (verified) — https://registry.npmjs.org/@gsap/react
- **gsap 3.15.0** (verified) — https://registry.npmjs.org/gsap
- **lenis 1.3.27** (verified) — https://registry.npmjs.org/lenis
- **React `<ViewTransition>` stable in React 19.3.0** (verified; released 2026-09-09, latest 19.3.1) — https://react.dev/blog/2026/09/09/react-19-3 and https://registry.npmjs.org/react
