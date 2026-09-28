---
name: "program-markmap"
description: "Specialist in interactive mind-map visualization from Markdown using Markmap (markmap-cli, markmap-lib, markmap-view, KaTeX, autoloader, and SVG/HTML export)."
---

# 🧠 Interactive Mind-Map Visualization with Markmap (Markdown to Mindmap)

This skill guides the artificial intelligence to act as a **Markmap Specialist**, generating interactive, vector (SVG/D3.js), responsive mind maps directly from hierarchical Markdown structures, integrating math formulas (KaTeX), code blocks, icons, and visual customizations.

---

## 🗺️ 1. Markmap Architecture and Operating Principles

**Markmap** parses the Markdown Abstract Syntax Tree (AST) produced by CommonMark/GFM-compatible parsers and builds an interactive tree graph rendered through D3.js:

```mermaid
flowchart LR
    subgraph Input["Structured Markdown"]
        MD["Headings (#, ##, ###)\nNested Lists (- / *)\nKaTeX Formulas\nCode Blocks"]
    end

    subgraph CoreEngine["Transform & View Engine"]
        TRANSFORM["@markmap/transform (AST Parser)"]
        VIEW["@markmap/view & D3.js (Interactive SVG)"]
    end

    subgraph Outputs["Exports & Environments"]
        HTML["Standalone Interactive HTML"]
        SVG["SVG Vector Graphics"]
        CLI["markmap-cli (--watch / --open)"]
    end

    MD --> TRANSFORM --> VIEW --> Outputs
```

---

## 🛠️ 2. Installation and Command-Line Usage (CLI)

The `markmap-cli` package turns Markdown files into interactive presentations instantly:

```bash
# Generate a standalone interactive HTML mind map
npx markmap-cli mindmap.md -o mindmap.html

# Open automatically in the browser with a local development server
npx markmap-cli mindmap.md --open

# Live-Reload mode while editing the documentation
npx markmap-cli mindmap.md --watch
```

---

## 📝 3. Markmap Syntax and Advanced Features

### A. Configuration via YAML Frontmatter
The frontmatter header controls rendering behavior, expansion levels, and colors:

```markdown
---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 2
  duration: 500
  maxWidth: 300
  zoom: true
  pan: true
---

# Corporate Payment System

## Microservices Architecture
- **Order Service**
  - REST API `POST /orders`
  - Event Publisher (Kafka)
- **Payment Service**
  - Gateway Integration (Stripe / Pix)
  - Idempotency Controller
- **Notification Service**
  - Webhooks
  - E-mail Templates

## Database & Storage
- PostgreSQL
  - *Read Replicas*
  - Connections via PgBouncer
- Redis Cache
  - Rate Limiting
  - Session Tokens

## Security & Compliance
- PCI-DSS v4.0
- Card Data Tokenization
- TLS 1.3 End-to-End
```

### B. Integration with Math Formulas (KaTeX / LaTeX)
Markmap supports inline and block math equations:
```markdown
# Machine Learning Algorithms
## Linear Regression
- Cost Function: $J(\theta) = \frac{1}{2m} \sum_{i=1}^m (h_\theta(x^{(i)}) - y^{(i)})^2$
- Gradient Descent: $\theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta)$
```

### C. Styling Nodes with HTML and Badges
Rich visual formatting can be embedded in individual nodes:
```markdown
# 🚀 Engineering Roadmap
## Backend <span class="badge" style="background:#28a745;color:#fff;padding:2px 6px;border-radius:4px;">Q1</span>
- Migration to Go 1.24
- Adoption of gRPC for internal communication
## Frontend <span class="badge" style="background:#007bff;color:#fff;padding:2px 6px;border-radius:4px;">Q2</span>
- Upgrade to React 19
- Core Web Vitals Optimization
```

---

## 🎯 4. Best Practices for Creating Markmaps

1. **Depth Balance**: Keep between 3 and 5 nesting levels to guarantee fluid navigability and avoid visual overload.
2. **Concise Phrases**: Use objective topics, keywords, and backtick-wrapped code instead of long paragraphs.
3. **Using `colorFreezeLevel`**: Freeze the color level at `2` or `3` so that all child nodes share the color of their parent module, making visual semantic grouping easier.
