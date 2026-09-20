---
name: web-search-specialist
description: "Specialist in Advanced Web Research and Search Engines (Google, DuckDuckGo, Bing, SearXNG, Yahoo, Mojeek). Masters boolean operators, Google Dorks, structural filters (site, filetype, intitle, inurl), temporal search, disambiguation strategies, and fact/primary-source verification."
---

# Web Search Specialist & Search Engine Intelligence

This skill establishes the advanced methodology for investigation, information retrieval, and query engineering on internet search engines (**Google, DuckDuckGo, Bing, SearXNG, Yahoo, Mojeek, and Kagi**).

---

## 🎯 1. Fundamental Principles of Web Search

1. **Noise Economy and High Precision**:
   - Avoid purely conversational queries when the goal is to locate technical documents, tables, raw data, or specific pages.
   - Use discriminating keywords instead of stopwords or verbose phrases.
2. **Source Triangulation**:
   - Never trust a single isolated result for critical factual claims or statistics.
   - Cross-check primary sources (official sites, government bodies, original reports) with reliable secondary sources.
3. **Progressive Search Strategy (Scoping & Funneling)**:
   - **Step 1 (Broadening)**: Broad exploratory query to identify the correct terminology and industry synonyms.
   - **Step 2 (Narrowing)**: Application of quotes and inclusion/exclusion operators to eliminate obvious noise.
   - **Step 3 (Targeted Extraction)**: Use of structural operators (`site:`, `filetype:`, `intitle:`, `inurl:`) to locate source documents or canonical portals.

---

## 🔍 2. Canonical Catalog of Search Operators & Dorks

### A. Basic Boolean Operators and Modifiers

| Operator | Syntax | Function and Effect | Practical Example |
| :--- | :--- | :--- | :--- |
| **Double Quotes** | `"exact term"` | Forces exact literal matching and exact word order. | `"Inbound Marketing"` |
| **Minus Sign** | `-term` | Excludes pages containing the specified word or domain (no space after the hyphen). | `digital marketing -course -free` |
| **OR / Pipe** | `A OR B` or `A | B` | Returns results containing term A or term B. | `"kubernetes" OR "k8s"` |
| **Wildcard** | `*` | Acts as a placeholder for one or more unknown words in the phrase. | `"the secret of * business"` |
| **Numeric Range** | `num1..num2` | Searches numbers, dates, or monetary values within a continuous range. | `security report 2023..2025` |

---

### B. Structural and Metadata Operators

| Operator | Syntax | Description | Application Example |
| :--- | :--- | :--- | :--- |
| **`site:`** | `site:domain.com` | Restricts the search exclusively to the specified domain or TLD (e.g., `.gov.br`, `.edu`). | `vulnerabilities site:gov.br` |
| **`filetype:` / `ext:`** | `filetype:pdf` | Restricts the search to specific file extensions (`pdf`, `xlsx`, `csv`, `docx`, `pptx`, `json`). | `"data overview" filetype:pdf` |
| **`intitle:`** | `intitle:"term"` | Requires the term to appear in the page title (`<title>`) of the HTML. | `intitle:"annual report" market` |
| **`allintitle:`** | `allintitle: term1 term2`| Requires all listed words to be present in the title. | `allintitle: ai benchmark productivity` |
| **`inurl:`** | `inurl:term` | Requires the term to be present in the URL path. | `inurl:blog "offensive security"` |
| **`allinurl:`** | `allinurl: term1 term2` | Requires all words to be part of the URL. | `allinurl: docs api authentication` |
| **`intext:` / `allintext:`** | `intext:"term"` | Guarantees the term is in the body text (ignoring titles and URLs). | `intext:"CVE-2024-"` |
| **`related:`** | `related:site.com` | Finds websites similar or thematically related to the given domain. | `related:github.com` |
| **`cache:`** | `cache:site.com` | Displays the search engine's cached version of the address. | `cache:example.com/article` |

---

### C. Temporal Filters and Chronological Operators (Google)

- `after:YYYY-MM-DD`: Returns pages published or indexed after the specified date.
- `before:YYYY-MM-DD`: Returns pages published or indexed before the given date.
- **Combined Example**: `security incident after:2024-01-01 before:2024-12-31`

---

### D. Search-Engine-Specific Operators and Features

#### 1. Microsoft Bing
- **`contains:type`**: Locates pages containing links to specific formats (`contains:pdf`, `contains:mp4`).
- **`loc:code`**: Restricts results to specific countries (`loc:br`, `loc:us`).
- **`prefer:term`**: Applies higher relevance weight to certain terms without making them strictly mandatory.
- **`feed:term`**: Finds RSS or Atom feeds on the subject.

#### 2. DuckDuckGo
- **`!bangs`**: Enables immediate redirection to internal searches on thousands of services (`!g` for Google, `!w` for Wikipedia, `!gh` for GitHub, `!so` for StackOverflow, `!arxiv` for arXiv).
- **Quotes and Minus**: Strict matching with no algorithmic personalization or filter bubble (*anti-tracking*).

#### 3. SearXNG & Private Engines (Mojeek, Startpage)
- Impartial aggregation and search independent of user profiling.
- Strict boolean syntax recommended (`AND`, `OR`, `NOT`).

---

## 🛠️ 3. High-Performance Heuristic Techniques

### 1. Direct Search for Primary Documents and Reports
To obtain concrete research and numbers without intermediaries:
```text
"search term" (report OR survey OR benchmark OR study) filetype:pdf site:gov.br OR site:org
```

### 2. OSINT Investigation and Public Asset Discovery (Ethical Google Dorking)
- **Locating public technical documentation or Swagger**:
  ```text
  intitle:"swagger ui" inurl:"/api/v1" "specification"
  ```
- **Locating logs or diagnostic dumps**:
  ```text
  filetype:log "exception" intext:"stack trace"
  ```

### 3. Semantic Disambiguation
If the term is polysemous (e.g., *Java* the language vs. *Java* the geographic island):
```text
"Java" -programming -software -code -jdk -oracle
```

### 4. Citation and News Origin Extraction
```text
"exact phrase from a statement" after:2024-01-01 site:reuters.com OR site:bloomberg.com
```

---

## 📋 4. Web Researcher Response Protocol

When presenting search results to the user or other agents:
1. **Executive Synthesis**: A direct summary of the answers found.
2. **Auditable Sources**: A list with direct links or references to the domains consulted.
3. **Search Strings Used**: Explicit display of the operators used to enable reproducibility.
4. **Confidence Level and Divergences**: Indication of consensus or discrepancies identified among the sources.
