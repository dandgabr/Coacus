# 🛠️ Practical Guide to Design Engineering & Frontend Craft (Craft UI)

This guide provides high-fidelity code patterns and production-ready snippets for de-templating, animation physics, tactile surfaces, and advanced accessibility.

---

## 1. De-templating Components: The Authorial Wrapper Pattern

Use a product wrapper when it centralizes actual token, semantic or behavior decisions. Reuse a suitable accessible component directly when no wrapper is needed. The following optional motion example is one implementation, not a required treatment for every style:

```tsx
// components/craft/AppButton.tsx
"use client";
import * as React from "react";
import { motion, HTMLMotionProps, useReducedMotion } from "motion/react";
import { springPresets } from "@/lib/animation/springs";

export interface AppButtonProps extends HTMLMotionProps<"button"> {
  variant?: "primary" | "secondary" | "subtle" | "brutalist";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
}

export const AppButton = React.forwardRef<HTMLButtonElement, AppButtonProps>(
  ({ variant = "primary", size = "md", className = "", children, ...props }, ref) => {
    const reduceMotion = useReducedMotion();
    const sizeClasses = {
      sm: "h-8 px-3 text-xs gap-1.5",
      md: "h-10 px-4 text-sm gap-2",
      lg: "h-12 px-6 text-base gap-2.5"
    }[size];

    const variantClasses = {
      primary:
        "bg-white text-black font-medium border border-transparent shadow-sm hover:bg-neutral-200 active:bg-neutral-300",
      secondary:
        "bg-[#141618] text-[#e1e4ea] border border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.18)] hover:bg-[#1a1d20]",
      subtle:
        "bg-transparent text-neutral-400 hover:text-white hover:bg-[rgba(255,255,255,0.04)]",
      brutalist:
        "bg-[#FFE600] text-black font-bold border-2 border-black shadow-[3px_3px_0px_#000] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_#000] active:translate-x-[3px] active:translate-y-[3px] active:shadow-none"
    }[variant];

    return (
      <motion.button
        ref={ref}
        whileTap={!reduceMotion && variant !== "brutalist" ? { scale: 0.98 } : undefined}
        transition={springPresets.snap}
        className={`inline-flex items-center justify-center rounded-[2px] tracking-tight transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus-ring)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--surface-ground)] disabled:opacity-50 disabled:pointer-events-none ${sizeClasses} ${variantClasses} ${className}`}
        {...props}
      >
        {children}
      </motion.button>
    );
  }
);

AppButton.displayName = "AppButton";
```

---

## 2. Performant Analog Noise Injection via SVG Data-URI

Add texture only where it fits the material language. Define its owner and measure its cost and painted effect rather than assuming a small data URI cannot affect performance or contrast:

```css
/* styles/craft-textures.css */

/* Grain layer with Perlin Noise SVG with no network request */
.craft-grain-overlay {
  position: relative;
  isolation: isolate;
}

.craft-grain-overlay::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: -1;
  opacity: 0.045;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
}
```

---

## 3. Spring Architecture in Motion (formerly Framer Motion)

These objects carry the canonical spring tokens; [motion-timing-engines](../../../domains/design/ui-motion-interaction/references/motion-timing-engines.md) is the single source of truth for their values, damping ratios and interruption rules, so update that file first and mirror it here. Preserve a complete static state under reduced motion and validate choices through actual interaction testing:

```typescript
// lib/animation/springs.ts — mirrors the canonical tokens (mass 1)

export const springPresets = {
  // spring.smooth: modals, dropdowns, drawers, layout moves (ζ≈0.89, ≈0.2% overshoot)
  smooth: {
    type: "spring" as const,
    stiffness: 300,
    damping: 31,
    mass: 1
  },
  // spring.snap: press feedback, toggles, small controls (ζ≈1.0, no overshoot)
  snap: {
    type: "spring" as const,
    stiffness: 500,
    damping: 45,
    mass: 1
  },
  // spring.playful: celebratory badges, rare delight only (ζ≈0.51, ≈16% overshoot)
  playful: {
    type: "spring" as const,
    stiffness: 250,
    damping: 16,
    mass: 1
  }
};
```

---

The button example consumes `--focus-ring` and `--surface-ground` from its host theme; verify that pair on the actual surrounding surface. It does not prescribe white focus ink for all appearances.

## 4. Card with Hairline Border and Surface Ladder

```tsx
// components/craft/TactileCard.tsx
import React from "react";

interface TactileCardProps {
  level?: 1 | 2 | 3;
  children: React.ReactNode;
  className?: string;
}

export function TactileCard({ level = 1, children, className = "" }: TactileCardProps) {
  // Surface ladder: luminance increasing with the elevation level
  const levelStyles = {
    1: "bg-[#0c0d0e] border-[rgba(255,255,255,0.06)] hover:border-[rgba(255,255,255,0.12)]",
    2: "bg-[#141618] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.16)]",
    3: "bg-[#1c1f22] border-[rgba(255,255,255,0.12)] shadow-xl"
  }[level];

  return (
    <div
      className={`rounded-[2px] border p-6 transition-all duration-200 ${levelStyles} ${className}`}
    >
      {children}
    </div>
  );
}
```

---

## Version Sources

Moving release pins in this file were resolved 2026-10-20:
- **motion 14.4.0** (verified; React import `motion/react`) — https://motion.dev/changelog
