---
name: "lang-typst"
description: "Provides engineering and modern digital typography patterns using Typst. Covers markup syntax, custom functions, creating reusable templates, show/set rules, advanced math, tables, page layout, and bibliography via Hayagriva/BibTeX."
---

# AI Skill: Typst Engineering (Typst Specialist)

This skill guides the AI to act as a specialist in the **Typst** layout language and system, focusing on creating academic documents, technical reports, presentations, and articles with high typographic quality, clean syntax, expressive code, and fast compilation.

---

## 🧭 Typst Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Layout Configuration and `set` and `show` Rules
- **Separation of Content and Style**: Define global style rules using `#set` instructions at the top of the document or inside a template.
- **Selector Transformation (`show`)**: Use `#show` rules to customize the appearance of specific elements (such as headings, links, code blocks, or tables) declaratively.
- **Initial Page Configuration**:
  ```typst
  #set page(
    paper: "a4",
    margin: (x: 2cm, top: 2.5cm, bottom: 2.5cm),
    header: align(right)[_Technical Report_],
    footer: [
      #align(center)[#counter(page).display("1 / 1", both: true)]
    ]
  )
  #set text(font: "Liberation Serif", size: 11pt, lang: "en")
  ```

### 2. Operation Modes (Text, Math, and Code)
- **Text Mode**: Natural writing with lightweight syntax (`*bold*`, `_italic_`, `= Heading`).
- **Math Mode (`$`)**: Use inline blocks `$ x^2 $` or display blocks `$ sum_(i=1)^n i = (n(n+1))/2 $`.
- **Code Mode (`#`)**: Every command or logic in Typst starts with `#`. A multi-line code block uses `#{ ... }`.

### 3. Functions and Modularity
- **Reusable Templates**: Export a main template function that receives structured parameters (title, authors, abstract, body) and applies the layout rules via `#show: doc => template(doc)`.
- **Named Parameters**: Prefer named parameters with sensible defaults in custom functions.

### 4. Tables, Figures, and Idiomatic Layout
- **Tables with `table`**: Use the new table API with `table.header` and explicit per-column alignment:
  ```typst
  #table(
    columns: (1fr, 2fr, 1fr),
    align: (left, left, center),
    stroke: 0.5pt + luma(150),
    table.header([*ID*], [*Description*], [*Status*]),
    [01], [Firmware update], [OK],
    [02], [Integrity check], [Pending]
  )
  ```
- **Callout Boxes**: Create stylized visual blocks using `block` with rounded borders and subtle fill.

### 5. Bibliography and Package Management
- **Native Bibliographies**: Use `#bibliography("works.bib", style: "ieee")` for transparent integration with `.bib` or `.yml` files (Hayagriva).
- **Typst Universe Packages**: Import official packages with the syntax `#import "@preview/package:version"`.

---

## 🧰 Recommended Code Patterns

### Professional Report / Technical Article Template

```typst
// template.typst
#let project(
  title: "",
  authors: (),
  abstract: none,
  logo: none,
  body
) = {
  // Global page configuration
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 3cm),
    numbering: "1",
  )
  
  // Typography configuration
  set text(font: "DejaVu Serif", size: 11pt, lang: "en", region: "US")
  set par(justify: true, leading: 0.65em)
  set heading(numbering: "1.1")

  // Visual customization of the headings
  show heading: it => [
    #v(0.5em)
    #text(fill: rgb("#1a365d"), weight: "bold")[#it]
    #v(0.3em)
  ]

  // Header / Condensed cover page
  align(center)[
    #if logo != none {
      image(logo, width: 25%)
      v(1em)
    }
    #text(size: 20pt, weight: "bold", fill: rgb("#1a365d"))[#title]
    #v(1em)
    #grid(
      columns: (1fr,) * calc.min(authors.len(), 3),
      gutter: 1em,
      ..authors.map(author => align(center)[
        #text(weight: "medium")[#author.name] \
        #text(size: 9pt, fill: luma(100))[#author.email]
      ])
    )
    #v(1.5em)
  ]

  // Abstract (if any)
  if abstract != none {
    rect(
      width: 100%,
      fill: rgb("#f7fafc"),
      inset: 12pt,
      radius: 4pt,
      stroke: 0.5pt + rgb("#e2e8f0")
    )[
      #text(weight: "bold", fill: rgb("#2d3748"))[Abstract] \
      #v(0.3em)
      #abstract
    ]
    #v(1.5em)
  }

  // Document Body
  body
}
```

### Example of Using the Template with Blocks and Math

```typst
#import "template.typst": project

#show: doc => project(
  title: "Performance Analysis of Distributed Algorithms",
  authors: (
    (name: "Dandara Gabriel", email: "dandara@example.com"),
    (name: "Alex Silva", email: "alex@example.com")
  ),
  abstract: [
    This document presents a comparative evaluation of throughput and latency between asynchronous messaging architectures operating under high load.
  ],
  doc
)

= Introduction

The scalability of modern distributed systems depends directly on the communication pattern adopted between the receiving and sending nodes.

#let callout(title: "Note", body, color: blue) = {
  block(
    fill: color.lighten(90%),
    stroke: (left: 4pt + color),
    inset: 10pt,
    radius: (right: 4pt),
    width: 100%,
    [
      #text(weight: "bold", fill: color.darken(20%))[#title] \
      #body
    ]
  )
}

#callout(title: "Important", color: rgb("#2b6cb0"))[
  Ensure that the cluster nodes are synchronized via the NTP protocol before starting the load tests.
]

= Mathematical Formulation

The average response time $T(n)$ for a queueing system with $n$ concurrent requests is modeled by the equation:

$ T(n) = sum_(k=1)^n (lambda_k / (mu_k - lambda_k)) + float("overhead") $

Where $lambda_k$ represents the arrival rate and $mu_k$ the service rate of channel $k$.

= Experimental Results

#figure(
  table(
    columns: (1fr, 1.5fr, 1fr),
    align: (center, left, right),
    stroke: 0.5pt + luma(180),
    table.header([*Metric*], [*Algorithm*], [*Average Value*]),
    [Throughput], [Event-Driven Reactive], [45,200 req/s],
    [p99 Latency], [Event-Driven Reactive], [1.2 ms],
    [Throughput], [Blocking I/O Standard], [12,800 req/s],
  ),
  caption: [Performance Comparison between Architectures]
)
```

## 🔒 Security Issues and Safe Practices

- **Sandbox Escaping**: Configure the Typst compiler in restricted mode (sandbox enabled) to prevent arbitrary operations that read local files or unauthorized network paths.
- **Denial of Service (DoS)**: Optimize loops, recursive functions, and dynamic formatting rules to prevent malicious scripts from inducing infinite recursion and consuming the server's entire CPU.
