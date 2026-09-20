---
name: "lang-latex"
description: "Provides engineering and academic/scientific typography patterns in LaTeX (LaTeX2e and LuaLaTeX/XeLaTeX). Covers modular multilevel document structuring, bibliography management with BibLaTeX/Biber, illustrations with TikZ, rigorous mathematical formatting (amsmath/mathtools), custom commands (newcommand/ProvideDocumentCommand), and prevention of common compilation errors."
---

# AI Skill: LaTeX Engineering (LaTeX Specialist)

This skill guides the AI to act as a specialist in the **LaTeX** ecosystem (including modernized engines such as XeLaTeX and LuaLaTeX), focusing on the professional writing and structuring of theses, dissertations, technical books, academic articles, and scientific reports.

---

## 🧭 LaTeX Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Modular Project Structuring
- **Clean Master Document**: The main file (`main.tex`) must contain the structured preamble and the calls to chapters/sections via `\input{sections/name.tex}` or `\include{chapters/name.tex}`.
- **Folder Organization**:
  - `figures/`: Images and TikZ schematics.
  - `styles/` or `packages/`: Custom packages and macros (`custom.sty`).
  - `bibliography.bib`: Bibliographic database.

### 2. Engine Choice and Modern Packages
- **Prefer LuaLaTeX / XeLaTeX**: For new projects, use LuaLaTeX or XeLaTeX with the `fontspec` package for native UTF-8 support and system fonts (OTF/TTF).
- **Recommended Essential Packages**:
  - Mathematical Typography: `amsmath`, `amssymb`, `mathtools`.
  - Professional Tables: `booktabs` (avoid vertical lines in academic tables), `tabularx`, `array`.
  - Images and Diagrams: `graphicx`, `tikz`, `pgfplots`.
  - Links and Cross-References: `hyperref`, `cleveref` (must be loaded after `hyperref`).

### 3. Bibliography with BibLaTeX + Biber
- **Replace natbib/BibTeX with BibLaTeX**: Use `biblatex` with the `biber` backend for full UTF-8 support and flexible bibliographic styles (such as ABNT, IEEE, APA):
  ```latex
  \usepackage[backend=biber, style=numeric, sorting=nyt]{biblatex}
  \addbibresource{bibliography.bib}
  ```

### 4. Clean Definition of Macros and Commands
- **Modern Syntax (LaTeX3 / `xparse`)**: Define macros with rich optional arguments using `\NewDocumentCommand` instead of legacy `\newcommand`:
  ```latex
  \NewDocumentCommand{\codevar}{m o}{%
    \texttt{#1}\IfValueT{#2}{\space\textnormal{(#2)}}%
  }
  ```

### 5. Typographic Formatting Best Practices
- **Correct Quotes**: Use ``double quotes'' instead of `"single quotes"`.
- **Hyphen vs. En Dash vs. Em Dash**: Use `-` for compound words, `--` for value ranges (e.g., 10--20), and `---` for explanatory em dashes.

---

## 🧰 Recommended Code Patterns

### Modular Master Document (`main.tex`)

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper, oneside]{article}

% --- Pré-ambulo: Pacotes Fundamentais ---
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}

% Idioma e Ajustes de Margem
\usepackage[portuguese]{babel}
\usepackage[top=3cm, bottom=2cm, left=3cm, right=2cm]{geometry}

% Matemática e Símbolos
\usepackage{amsmath, amssymb, mathtools}

% Tabelas e Figuras
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{tikz}

% Bibliografia Avançada
\usepackage[backend=biber, style=alphabetic, sorting=nyt]{biblatex}
\addbibresource{bibliography.bib}

% Links e Referências Inteligentes
\usepackage[colorlinks=true, linkcolor=blue, citecolor=teal, urlcolor=magenta]{hyperref}
\usepackage{cleveref}

% --- Macros Customizadas ---
\NewDocumentCommand{\vectornorm}{m}{%
  \left\lVert #1 \right\rVert
}

\title{\textbf{Modelagem Estocástica de Redes Complexas}}
\author{Dandara Gabriel \and Equipe de Pesquisa}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Este trabalho apresenta um modelo matemático para previsão de convergência em grafos direcionados orientados a eventos.
\end{abstract}

\tableofcontents
\newpage

% --- Conteúdo Modular ---
\section{Introdução}
A análise de grafos dinâmicos é fundamental para a compreensão de sistemas complexos~\cite{smith2024}.

\section{Fundamentação Matemática}
Dada uma matriz de adjacência $A \in \mathbb{R}^{n \times n}$, a norma Frobenius do operador de transição é dada pela \cref{eq:norma}:

\begin{equation}
\label{eq:norma}
\vectornorm{A}_F = \sqrt{\sum_{i=1}^{n} \sum_{j=1}^{n} |a_{ij}|^2}
\end{equation}

\section{Resultados e Tabelas}
A \cref{tab:resultados} resume o desempenho obtido.

\begin{table}[htbp]
  \centering
  \caption{Desempenho de Convergência do Algoritmo}
  \label{tab:resultados}
  \begin{tabular}{@{}llrr@{}}
    \toprule
    \textbf{Grafo} & \textbf{Método} & \textbf{Iterações} & \textbf{Tempo (s)} \\
    \midrule
    Erdős--Rényi & Standard Power Iter & 1.420 & 3,45 \\
    Erdős--Rényi & Accelerated Krylov  & 310   & 0,82 \\
    Barabási--Albert & Accelerated Krylov & 540 & 1,12 \\
    \bottomrule
  \end{tabular}
\end{table}

\printbibliography

\end{document}
```

### Stylized Highlight Box with `tcolorbox` and a `TikZ` Diagram

```latex
\usepackage[many]{tcolorbox}

% Definindo uma caixa de teorema/aviso elegante
\newtcolorbox{alertbox}[2][]{%
  colback=blue!5!white,
  colframe=blue!75!black,
  fonttitle=\bfseries,
  title=#2,
  arc=2mm,
  #1
}

% Exemplo de Uso:
\begin{alertbox}{Teorema Fundamental de Limite}
Se uma sequência $\{a_n\}$ é limitada e monotônica, então a sequência $\{a_n\}$ é convergente.
\end{alertbox}

% Exemplo de Diagrama TikZ Limpo:
\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}[node distance=2cm, auto, >=stealth']
    \node [draw, circle, fill=blue!10] (A) {Nó A};
    \node [draw, circle, fill=green!10, right of=A, node distance=3cm] (B) {Nó B};
    \node [draw, circle, fill=orange!10, below of=B] (C) {Nó C};

    \draw[->, thick] (A) -- node {$\lambda_{ab}$} (B);
    \draw[->, thick] (B) -- node {$w_{bc}$} (C);
    \draw[->, thick] (C) -| node[near start] {$\mu_{ca}$} (A);
  \end{tikzpicture}
  \caption{Grafo de Transição de Estados}
  \label{fig:tikz_state}
\end{figure}
```

## 🔒 Security Issues and Safe Practices

- **Shell Escape (Code Execution)**: Disable the `--shell-escape` flag when compiling LaTeX documents containing untrusted third-party code, preventing calls to the `\write18` directive.
- **Arbitrary File Inclusion**: Limit access to directives such as `\input`, `\include`, and `\import` to avoid arbitrary reading of confidential files on the host system.
- **Denial of Service (DoS)**: Avoid infinite recursion loops in custom macro definitions that could freeze or lock up the compilation server's CPU.
