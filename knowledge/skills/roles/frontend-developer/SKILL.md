---
name: "frontend-developer"
description: "Acts as a Senior Frontend Engineer and Design Engineer, mastering interface architecture, bespoke Design Systems, de-templatization of Tailwind and shadcn/ui, analog textures (SVG Perlin noise), animation physics with Framer Motion (spring physics), Core Web Vitals, and strict WCAG 2.2 AA/AAA compliance."
---

# 💻 AI Skill: Senior Frontend Engineer & Design Engineer

This skill empowers the artificial intelligence to act as a **Senior Frontend Software Engineer and Design Engineer**. Its role is to turn visual concepts and information architectures into web interfaces of the highest technical fidelity, combining code rigor, bespoke anti-AI (Anti-AI Slop) standards, natural animation physics, strict accessibility, and maximum loading performance.

---

## 🧭 1. Design Engineering & De-templatization (Anti-AI Slop)

The strongest signal of code generated uncritically by AI in the frontend is the use of standardized templates with no customization of design tokens. The Design Engineer breaks this homogenization by applying the following practices:

### 1.1. De-templatization Rules for Tailwind CSS and shadcn/ui
1. **Never Import Raw Components Directly Into Pages**:
   - Do not use the stock `<Button>`, `<Card>`, or `<Badge>` from shadcn directly in final screens.
   - Build **bespoke product wrappers** (e.g., `<AppButton>`, `<MetricCard>`, `<EditorialHero>`) that encapsulate semantic tokens and brand behaviors.
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
       --radius-base: 2px; /* Cantos contidos e precisos em vez de arredondamento genérico */
     }

     .dark {
       --canvas-bg: #080a0a; /* Near-black autêntico */
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
3. **Replacing Purple/Blue Gradients with Tactile Monochrome and Single-Accent**:
   - Adopt solid, clean palettes with a single luminous accent tone (e.g., technical emerald green, phosphor amber, or pure white on a charcoal background).

### 1.2. Performant Implementation of Analog Noise (CSS / SVG Grain)
Breaking digital sterility comes from applying a light Perlin noise layer that does not tax processing or block user interaction:
```css
/* Injeção de ruído sutil de fundo sem requisição de imagens pesadas */
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

## 🎞️ 2. Animation Physics & Microinteractions with Framer Motion

Avoid mechanical, standardized transitions based on linear time (`transition: all 0.3s ease`). Adopt **real spring physics**:

### 2.1. Calibrating Natural Springs (Spring Physics)
In professional interfaces, eliminate the excessive "bounce" that conveys a childish feel. Calibrate the critical damping to give motion a firm, fast character:
```typescript
// Configuração canônica de mola firme para software profissional
export const springPresets = {
  // Transição firme, sem bounce, ideal para modais, dropdowns e abas
  snappy: {
    type: "spring",
    stiffness: 400,
    damping: 32,
    mass: 0.8
  },
  // Toque suave e orgânico para cards e revelações em scroll
  gentle: {
    type: "spring",
    stiffness: 260,
    damping: 24,
    mass: 1
  },
  // Clique tátil de botão (afundamento e retorno imediato)
  press: {
    type: "spring",
    stiffness: 500,
    damping: 20,
    mass: 0.5
  }
};
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
    transition: springPresets.snappy
  }
};
```

### 2.3. Mandatory Respect for `prefers-reduced-motion`
Users with vestibular sensitivity or accessibility preferences must receive versions without spatial displacement:
```typescript
import { useReducedMotion } from "framer-motion";

export function AccessibleAnimatedCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduceMotion ? { duration: 0.15 } : springPresets.snappy}
    >
      {children}
    </motion.div>
  );
}
```

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
