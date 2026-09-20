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
    header: align(right)[_Relatório Técnico_],
    footer: [
      #align(center)[#counter(page).display("1 / 1", both: true)]
    ]
  )
  #set text(font: "Liberation Serif", size: 11pt, lang: "pt")
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
    table.header([*ID*], [*Descrição*], [*Status*]),
    [01], [Atualização de firmware], [OK],
    [02], [Verificação de integridade], [Pendente]
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
  // Configuração global de página
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 3cm),
    numbering: "1",
  )
  
  // Configuração de tipografia
  set text(font: "DejaVu Serif", size: 11pt, lang: "pt", region: "BR")
  set par(justify: true, leading: 0.65em)
  set heading(numbering: "1.1")

  // Personalização visual dos títulos
  show heading: it => [
    #v(0.5em)
    #text(fill: rgb("#1a365d"), weight: "bold")[#it]
    #v(0.3em)
  ]

  // Cabeçalho / Capa resumida
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

  // Resumo (se houver)
  if abstract != none {
    rect(
      width: 100%,
      fill: rgb("#f7fafc"),
      inset: 12pt,
      radius: 4pt,
      stroke: 0.5pt + rgb("#e2e8f0")
    )[
      #text(weight: "bold", fill: rgb("#2d3748"))[Resumo] \
      #v(0.3em)
      #abstract
    ]
    #v(1.5em)
  }

  // Corpo do Documento
  body
}
```

### Example of Using the Template with Blocks and Math

```typst
#import "template.typst": project

#show: doc => project(
  title: "Análise de Desempenho de Algoritmos Distribuídos",
  authors: (
    (name: "Dandara Gabriel", email: "dandara@example.com"),
    (name: "Alex Silva", email: "alex@example.com")
  ),
  abstract: [
    Este documento apresenta uma avaliação comparativa de throughput e latência entre arquiteturas de mensageria assíncrona operando sob alta carga.
  ],
  doc
)

= Introdução

A escalabilidade de sistemas distribuídos modernos depende diretamente do padrão de comunicação adotado entre os nós receptores e emissores.

#let callout(title: "Nota", body, color: blue) = {
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

#callout(title: "Importante", color: rgb("#2b6cb0"))[
  Certifique-se de que os nós do cluster estejam sincronizados via protocolo NTP antes de iniciar os testes de carga.
]

= Formulacão Matemática

O tempo médio de resposta $T(n)$ para um sistema de fila com $n$ requisições concorrentes é modelado pela equação:

$ T(n) = sum_(k=1)^n (lambda_k / (mu_k - lambda_k)) + float("overhead") $

Onde $lambda_k$ representa a taxa de chegada e $mu_k$ a taxa de serviço do canal $k$.

= Resultados Experimentais

#figure(
  table(
    columns: (1fr, 1.5fr, 1fr),
    align: (center, left, right),
    stroke: 0.5pt + luma(180),
    table.header([*Métrica*], [*Algoritmo*], [*Valor Médio*]),
    [Throughput], [Event-Driven Reactive], [45.200 req/s],
    [Latência p99], [Event-Driven Reactive], [1.2 ms],
    [Throughput], [Blocking I/O Standard], [12.800 req/s],
  ),
  caption: [Comparativo de Desempenho entre Arquiteturas]
)
```

## 🔒 Security Issues and Safe Practices

- **Sandbox Escaping**: Configure the Typst compiler in restricted mode (sandbox enabled) to prevent arbitrary operations that read local files or unauthorized network paths.
- **Denial of Service (DoS)**: Optimize loops, recursive functions, and dynamic formatting rules to prevent malicious scripts from inducing infinite recursion and consuming the server's entire CPU.
