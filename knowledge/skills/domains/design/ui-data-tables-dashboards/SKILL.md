---
name: "ui-data-tables-dashboards"
description: "Provides design engineering patterns for complex data tables, dense data displays, and analytical dashboard architectures. Covers data density modes (compact, default, comfy), tabular numeral typography, column pinning (frozen headers/columns), multi-column sorting and filtering, batch actions, skeleton loading states, empty states, and inline micro-visualizations (sparklines, trend indicators). Use when designing B2B dashboards, financial consoles, analytics portals, or data-heavy administration views."
tags:
  - data-tables
  - dashboards
  - ui-design
  - b2b-saas
  - data-visualization
---

# UI Data Tables & Dashboards: Dense Analytical Interface Architecture

Data tables and analytical dashboards represent the operational core of enterprise software, developer consoles, and financial platforms. Unlike consumer interfaces optimized for casual browsing, data-dense interfaces must maximize **information throughput**, **scanning velocity**, and **decision accuracy** while preventing cognitive overload (Few, 2012; Tufte, 2001).

---

## 🧭 When to Activate

- Designing data-heavy interfaces, CRM list views, financial logs, or admin consoles.
- Implementing tabular views with sorting, filtering, selection, and pagination.
- Architecting metric overview cards (KPI widgets) and analytical dashboards.
- Designing responsive table adaptations, pinned columns, or horizontal scroll containers.
- Defining states for loading (skeletons), zero-data (empty states), and error recoveries in tables.

---

## 📐 Data Density System

Data density must match the user's operational modality. Provide user-controllable density settings or select the canonical density based on usage profile:

| Density Mode | Row Height | Font Size | Cell Padding (X/Y) | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Compact** | 32px | 12px / 0.75rem | 8px / 4px | High-frequency traders, logistics logs, devtools debuggers |
| **Default** | 40px | 13-14px / 0.875rem | 12px / 8px | Standard B2B SaaS, CRM records, inventory lists |
| **Comfy** | 48-56px | 14-15px / 0.9375rem | 16px / 12px | Executive dashboards, customer billing, casual audit logs |

### Rules of Spatial Rhythm
- **Border Scaffolding**: Use subtle 1px divider lines (`rgba(255,255,255,0.08)` in dark mode, `#E2E8F0` in light mode). Avoid heavy alternating row zebra-striping unless rows exceed 15 columns without visual anchors.
- **Row Hover Affordance**: Highlight active rows with a subtle surface contrast step (`+2-4%` lightness) to guide eye tracking across wide viewports.
- **Header Prominence**: Table headers (`<thead>`) must have uppercase or muted medium-weight text (`font-size: 11-12px`, `font-weight: 600`, `letter-spacing: 0.05em`) with background tinting or border separation.

---

## 🔢 Tabular Typography & Content Alignment

Alignment errors create visual friction and make comparison across rows arduous. Follow strict semantic alignment:

1. **Text & Identifiers (Left-aligned)**:
   - Names, emails, titles, status badges, descriptions.
   - Header is left-aligned to mirror cell content.
2. **Numbers & Monetary Values (Right-aligned)**:
   - Quantities, prices, percentages, latencies, dates in numeric formats.
   - Header is right-aligned above the column.
   - Always enforce **tabular figures**:
     ```css
     font-variant-numeric: tabular-nums;
     font-feature-settings: "tnum" 1;
     ```
     This ensures all digits share uniform advance width, preventing jitter when values update in real time or when scanning vertical columns.
3. **Status Badges & Single-character Flags (Center-aligned)**:
   - Booleans (Yes/No, checkmarks), single badges, icon-only toggles.
4. **Action Triggers (Right-aligned / Pinned Right)**:
   - Meatball menus (`···`), edit icons, inline buttons positioned on the far right column.

---

## ⚓ Column Pinning & Horizontal Overflow

When a table exceeds viewport width:
- **Pinned Primary Key (Left)**: The identifier column (e.g., ID, Name, Customer) remains pinned (`position: sticky; left: 0; z-index: 10`) with a subtle drop-shadow or border separator when scrolled.
- **Pinned Actions (Right)**: Context actions remain sticky to the right edge (`position: sticky; right: 0; z-index: 10`) so the user never has to scroll back and forth to execute an action.
- **Scroll Affordance**: Render subtle gradient shadow edges on the container to signal hidden horizontal content to the user.

---

## 🔍 Filtering, Sorting & Batch Actions

### Multi-Column Sorting
- Column headers indicate sorting state clearly: default unsorted icon (`↕` muted), ascending (`↑`), descending (`↓`).
- Secondary sort order should display small order badges (`↑ 1`, `↓ 2`) when multi-column sorting is active.

### Filter Toolbar Architecture
- **Global Search**: Leftmost input with keyboard shortcut (`/` or `Cmd+K`) searching primary text fields.
- **Faceted Popovers**: Dropdown filters with counts (e.g., `Status: Active (14) ▾`, `Role: Admin (3) ▾`).
- **Saved Views**: Allow users to save filter + sort + column visibility combinations as named tabs (`All Items`, `Needs Review`, `Archived`).

### Bulk Selection & Contextual Action Bar
- When 1 or more rows are checked via checkbox:
  - Header row transforms into a **Batch Action Floating Bar** showing selected count (`12 selected`).
  - Actions presented: `Export`, `Bulk Edit`, `Assign`, `Delete` (with destructive confirmation).
  - Include an explicit "Select all 1,420 items matching filter" prompt when paginated.

---

## 📊 Dashboard KPI Cards & Inline Visualizations

Dashboards synthesize table data into actionable top-level metrics:

### Metric Card Anatomy (KPI Widget)
- **Label**: Concise descriptor (`font-size: 12px`, muted uppercase).
- **Primary Value**: High-contrast, large tabular numeral (`font-size: 28-36px`, semibold).
- **Delta Indicator**: Comparison baseline (`+12.4% vs last month`), color-coded (`emerald-500` for positive, `rose-500` for negative, or neutral when directionality is ambiguous).
- **Inline Sparkline**: Minimalist SVG line or area chart (no axis lines, 32-48px height) visualizing the 30-day trend.

### Table Sparklines & Progress Bars
- Embed micro-charts directly in table cells for trend scanning.
- Progress bars inside cells should include the exact numeric percentage beside the visual bar (`[██████░░░░] 60%`).

---

## 🔄 Lifecycle States: Empty, Loading & Errors

1. **Skeleton Loading**:
   - Mirror the exact table structure with animated pulsating bars (`width: 60-80%`, `height: 12px`, `border-radius: 4px`).
   - Never replace the table structure with a single spinner in the center; skeletons preserve perceived layout stability and layout shift metrics (CLS).
2. **Actionable Empty States (Zero-Data)**:
   - When no records exist: Provide a clear icon, explanatory title ("No invoices yet"), secondary guidance, and a primary CTA ("Create your first invoice").
   - When filters yield 0 results: State clearly "No matches for current filters" and provide a "Clear all filters" button.
3. **Inline Error State**:
   - Provide row-level or table-level retry buttons without losing active filter/pagination parameters.
