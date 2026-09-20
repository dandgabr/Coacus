---
name: "lang-markdown"
description: "Provides complete guidelines for authoring, engineering, and formatting in Markdown (CommonMark, GitHub Flavored Markdown - GFM, and MDX). Covers hierarchical document structuring, advanced code and table formatting, visual elements (GFM alerts, Mermaid diagrams), LaTeX math equations, linting standards (MarkdownLint), technical documentation (READMEs, ADRs, Changelogs), and JSX/MDX integration."
---

# AI Skill: Markdown Engineering and Formatting (Markdown Specialist)

This skill guides the AI to act as a **Markdown** specialist, spanning the **CommonMark** and **GitHub Flavored Markdown (GFM)** specifications and modern extensions such as **MDX**. It ensures the creation of technical documentation, manuals, guides, API guides, architecture decision records (ADRs), and README files that are visually appealing, readable, semantic, and fully compliant with linting standards.

---

## 🎯 Skill Objective

Enable the AI assistant to produce Markdown documents with technical, semantic, and aesthetic excellence, avoiding common syntax errors, ensuring compatibility across different parsers, and applying best practices in technical markup.

---

## 🛠️ Formatting Guidelines and Standards

When writing or refactoring Markdown documents, apply the following rules strictly:

### 1. Hierarchy and Semantic Structure
- **Single Level-1 Title (`#`)**: Every standalone document must contain only one top-level (`#`) heading.
- **Progressive Nesting**: Never skip heading levels (e.g., jumping from `##` straight to `####`).
- **Heading Spacing**: Always keep one blank line before and after each heading line.
- **Capitalization**: Keep a consistent pattern (e.g., Title Case or Sentence case) throughout the heading tree.

### 2. Advanced GFM (GitHub Flavored Markdown) Syntax
- **Native GFM Alerts / Callouts**: Use the official typed blockquote syntax to highlight crucial information:
  ```markdown
  > [!NOTE]
  > Informações contextuais e explicações úteis.

  > [!TIP]
  > Dicas de otimização, boas práticas e sugestões.

  > [!IMPORTANT]
  > Requisitos essenciais e avisos indispensáveis.

  > [!WARNING]
  > Alterações que podem quebrar funcionalidade ou avisos de atenção.

  > [!CAUTION]
  > Riscos elevados de perda de dados ou ações destrutivas.
  ```

- **Aligned and Formatted Tables**:
  - Always include the separator row with alignment specification (`:---` for left, `:---:` for center, `---:` for right).
  - Keep uniform visual spacing in columns using aligned `|` pipes to make the raw source easier to read.
  ```markdown
  | Recurso | Suportado | Complexidade | Observação |
  | :--- | :---: | ---: | :--- |
  | CommonMark | Sim | Baixa | Padrão base |
  | GFM | Sim | Média | Suporta tabelas e alertas |
  | MDX | Sim | Alta | Componentes React |
  ```

- **Task Lists**:
  - Use `- [ ]` for pending items and `- [x]` for completed ones. Keep one character of space between the brackets.

- **Footnotes**:
  - Declare the note in the body text via `[^1]` or `[^key]` and describe it at the end of the file: `[^1]: Detailed explanation of the note.`.

- **Strikethrough and Highlights**:
  - Struck text: `~~removed text~~`.

---

### 3. Code Blocks and Diffs
- **Fenced Code Blocks**: Always declare the language identifier explicitly after the three backticks (```json, ```typescript, ```bash, etc.).
- **Diff Blocks**: To show code changes, use the `diff` language:
  ```diff
  - const old = "obsolete";
  + const updated = "updated";
  ```
- **Escaping Backticks**: To display code blocks inside Markdown instruction blocks, use four-backtick delimiters (````).

---

### 4. Viewable Diagrams and Math
- **Mermaid Diagrams**: Integrate flowcharts, sequence diagrams, charts, and mind maps using the `mermaid` identifier:
  ```mermaid
  flowchart LR
      A[Entrada Markdown] --> B[Parser GFM / MDX]
      B --> C[Renderização HTML/UI]
  ```
- **Math Equations (KaTeX / MathJax)**:
  - Inline: `$E = mc^2$`
  - Block on its own line:
    ```markdown
    $$
    \hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} dx
    $$
    ```

---

### 5. Metadata Headers (Frontmatter) and MDX
- **YAML Frontmatter**: Place it at the top of the file, delimited by `---`:
  ```yaml
  ---
  title: "Guia Completo de Markdown"
  description: "Manual de referência rápida e avançada para marcação em Markdown."
  author: "Equipe de Engenharia"
  date: "2026-08-06"
  tags: ["markdown", "gfm", "mdx", "docs"]
  ---
  ```
- **MDX Syntax (React in Markdown)**:
  - Lets you import and use JSX components inside the Markdown file:
  ```mdx
  import { Button, Alert } from '@/components/ui';

  <Alert type="success">
    Componente React renderizado via MDX!
  </Alert>

  <Button onClick={() => alert("Clicado!")}>Ação</Button>
  ```

---

### 6. Quality Standards and Error Prevention (MarkdownLint)
- **Line Breaks**: Prefer an explicit `<br>` when you need a forced line break, avoiding two trailing spaces at the end of a line (invisible and easy to delete by accident).
- **Final Line**: Always ensure the file ends with exactly one blank line (MD047).
- **Raw URLs**: Instead of pasting bare URLs (`https://example.com`), wrap them in angle brackets (`<https://example.com>`) or create semantic links (`[Link Name](https://example.com)`).
- **Image Alt Text**: Every image must have a descriptive alternative text: `![Descriptive alternative text](https://example.com/image.png)`.

---

## 📚 Skill Structure

- [SKILL.md](SKILL.md): Core guides and Markdown engineering specifications.
- **`scripts/`**: Executable Markdown automation and validation scripts.
- **`examples/`**: Default models and templates (technical README, ADR, Changelog).
- **`resources/`**: Auxiliary resources and icon/badge palettes.
- **`references/`**: Reference documentation for the CommonMark, GFM, and MarkdownLint specifications.

## 🔒 Security Issues and Safe Practices

- **Cross-Site Scripting (XSS)**: Always sanitize or disable the rendering of raw HTML tags inside Markdown when the final HTML is displayed in web browsers.
- **Link Injection**: Use validators for user-generated links and paths, ensuring that dangerous schemes such as `javascript:` or `data:` are blocked.
- **Image and Media Validation**: Route external image URLs through image proxies to avoid leaking end-user IPs.
