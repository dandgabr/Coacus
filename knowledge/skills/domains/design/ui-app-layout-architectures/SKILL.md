---
name: "ui-app-layout-architectures"
description: "Provides structural interface patterns for modern Web App Shells and Mobile application layouts. Covers navigation topologies (collapsible sidebars, nav rails, top navigation, bottom bar tab bars), multi-pane patterns (Master-Detail, Split-View, Inspector Drawers), responsive density transitions, viewport budgeting, safe-area mobile insets (env(safe-area-inset-*)), and touch ergonomics. Use when designing web application shells, desktop software, mobile apps, or multi-panel productivity suites."
tags:
  - app-layout
  - app-shell
  - web-app
  - mobile-app
  - ui-design
  - responsive-design
---

# UI App Layout Architectures: Web & Mobile Shell Topologies

An application layout is the structural skeleton that supports all user interactions. Unlike public content sites driven by vertical scroll documents, applications are **stateful operating environments** requiring clear zones for navigation, primary workflows, contextual inspections, and feedback loops (Nielsen, 1994; Tidwell et al., 2020).

---

## 🧭 When to Activate

- Designing the root layout and navigation frame of a web or mobile application.
- Structuring multi-panel productivity applications (e.g., mail clients, IDEs, CRMs, task managers).
- Implementing responsive breakpoints adapting from desktop sidebars to mobile bottom navigation.
- Budgeting mobile viewports with native status bars, virtual keyboards, and home indicators.
- Managing contextual overlays: side sheets, inspector panels, slide-overs, and modals.

---

## 🏗️ Canonical Web App Shell Topologies

### 1. The Standard Vertical Sidebar Layout
- **Structure**:
  - `Sidebar` (fixed 240-280px width, sticky or full-height).
  - `Header` (fixed 56-64px height, search, notifications, user avatar).
  - `Main Content` (fluid `1fr`, scrollable area).
- **Collapsible Behaviors**:
  - Full expanded state (labels + icons).
  - Compact Rail state (icon-only, 64px width, tooltips on hover).
  - Hidden overlay drawer on tablet/mobile screens (`< 1024px`).
- **Best For**: Multi-tier B2B SaaS, management consoles, cloud provider portals.

### 2. Navigation Rail + Contextual Sidebar (Dual-Nav)
- **Structure**:
  - `Primary Rail` (48-64px, high-level domains: Code, Issues, Settings).
  - `Secondary Tree / List Sidebar` (200-240px, hierarchical files, project boards, channels).
  - `Workspace Canvas` (`1fr`, primary editing pane).
- **Cognitive Flow**: Decouples global context switching from local item navigation.
- **Best For**: Developer IDEs, Slack-like team chat, Notion-like document trees, complex design editors.

### 3. Master-Detail (Split-Pane Architecture)
- **Structure**:
  - `Pane A (List/Index)`: 300-360px wide, list of items with summary badges, search, and sort.
  - `Pane B (Detail View)`: Fluid width, full item inspector, actions, editing form.
  - `Pane C (Optional Context Inspector)`: 280-320px collapsible right panel for metadata, audit logs, or related records.
- **Keyboard Navigation**: Arrow keys (`↑`/`↓`) traverse Pane A; `Enter` focuses Pane B; `Escape` returns to list.
- **Best For**: Email clients, ticket triage systems, support desks, code review interfaces.

### 4. Fluid Canvas with Floating Toolbars
- **Structure**:
  - Infinite or bounded canvas taking 100% of the viewport.
  - Floating pill toolbars pinned to top-center, bottom-center, or left dock.
  - Floating panels for layers, properties, and tool inspectors.
- **Best For**: Visual editors, whiteboards, node-graph workflows, mapping interfaces.

---

## 📱 Mobile Layout Architecture & Touch Ergonomics

Mobile ergonomics are dictated by hardware physics and one-handed thumb interaction (Hoober, 2017).

```
   +-----------------------+  ^
   | [Safe Area / Status]  |  | Top Bar (Brand / Nav icon / Search)
   +-----------------------+  v
   |                       |
   |                       |  Hard-to-reach zone (Informational content)
   |                       |
   |   PRIMARY VIEWPORT    |
   |                       |
   |                       |  Natural thumb reach (Interactive controls, cards)
   +-----------------------+  ^
   |  [BOTTOM TAB BAR]     |  | Bottom Navigation (3-5 core destinations)
   |  [Home Indicator]     |  v Safe-area bottom padding
   +-----------------------+
```

### Mobile Layout Rules
1. **Bottom Navigation Over Top Hamburgers**:
   - Primary destinations (3 to 5 items) belong in a persistent Bottom Tab Bar (`height: 56-64px`).
   - Active tab indicator with clear color accent and label.
2. **Safe-Area Inset Management**:
   - Always respect OS notches and navigation bars:
     ```css
     padding-top: env(safe-area-inset-top);
     padding-bottom: env(safe-area-inset-bottom);
     padding-left: env(safe-area-inset-left);
     padding-right: env(safe-area-inset-right);
     ```
3. **Touch Target Dimensions**:
   - Minimum interactive hit target is **44×44 CSS px** (Apple HIG) or **48×48 dp** (Google Material).
   - Minimum visual padding of 8px between adjacent tap targets to prevent accidental triggers.
4. **Bottom Sheets (Action Drawers)**:
   - Complex menus, filters, and forms on mobile should slide up from the bottom as interactive sheets rather than opening centered modal dialogues.

---

## 🖥️ Viewport Budgeting & Responsive Breakpoints

Implement progressive layout collapse across industry standard breakpoints:

| Viewport Width | Breakpoint | Layout Behavior |
| :--- | :--- | :--- |
| `< 640px` (Mobile) | `sm` | Single-pane stack; bottom nav bar; master/detail pushes to separate screen |
| `640px - 1023px` (Tablet) | `md` | Collapsed icon rail (64px); optional slide-over sheets; 2-column grids |
| `1024px - 1439px` (Desktop) | `lg` | Full expanded sidebar (240px); standard master-detail split |
| `≥ 1440px` (Wide Desktop) | `xl` | 3-pane layout unlocked (Sidebar + Master + Detail + Right Inspector) |

### Overflow & Scroll Boundaries
- **No Body Scroll in App Shells**: In desktop web apps, the `<body>` must have `overflow: hidden; height: 100vh;`.
- **Independent Scroll Containers**: The navigation sidebar, the list pane, and the content pane must each scroll independently with custom subtle scrollbars (`scrollbar-gutter: stable`).
