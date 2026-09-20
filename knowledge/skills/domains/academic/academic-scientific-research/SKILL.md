---
name: academic-scientific-research
description: "Specializes in Scientific Research Methodology, Systematic Literature Review (PRISMA 2020), PICO/PECO Structuring, PRESS Appraisal, Searching Indexed Databases (PubMed/MeSH, arXiv, IEEE Xplore, Semantic Scholar, Scopus, SciELO), and Citation Networks."
---

# Academic & Scientific Research Methodology

This skill establishes the methodological and operational standard for conducting rigorous scientific investigations, formulating structured questions, running systematic searches in indexed academic databases, and synthesizing evidence without bias.

---

## 🔬 1. Question Formulation Methodology

Before dispatching queries to databases, the research question must be decomposed into a validated conceptual framework:

### A. PICO / PECO Framework
- **P (Population / Problem)**: Population, sample, domain, clinical context, or engineering problem under study.
- **I / E (Intervention / Exposure)**: Proposed intervention, algorithmic technique, treatment, drug, or technology investigated.
- **C (Comparison)**: Control, existing baseline, current state of the art, or placebo (if applicable).
- **O (Outcome)**: Measured outcomes (e.g., accuracy, latency, mortality reduction, throughput, efficacy).
- **S (Study Design - PICOS)**: Eligible study types (randomized clinical trials, peer-reviewed reviews, preprints, empirical studies).

---

## 📜 2. Systematic Review Protocol (PRISMA 2020 & Cochrane)

### A. 4-Phase Flowchart (PRISMA Flow Diagram)
1. **Identification**:
   - Registration of all records retrieved per academic database and complementary searches (grey literature).
   - Automated or DOI / PMID / arXiv ID-assisted duplicate removal.
2. **Screening**:
   - Blind or parallel reading of Titles & Abstracts with explicit inclusion/exclusion criteria.
3. **Eligibility**:
   - Obtaining the Full-Text and detailed verification of methodological variables.
4. **Inclusion**:
   - Final set of articles submitted to qualitative synthesis or quantitative meta-analysis.

### B. PRESS (Peer Review of Electronic Search Strategies) Guidelines
- **Conceptual Translation**: Ensure each PICO component has complete synonyms (free-text terms and controlled terms).
- **Controlled Vocabularies**: Mandatory use of **MeSH** (Medical Subject Headings) in PubMed, **DeCS** in BVS/SciELO, and the **ACM/IEEE Taxonomy** in computing.
- **Strict Boolean Operators**:
  - `OR` intra-concept (synonyms and spelling variants).
  - `AND` inter-concept (combination of PICO dimensions).
  - Sparing use of `NOT` to avoid inadvertent exclusion of relevant studies.

---

## 📚 3. Strategies by Scientific Database and Indexers

| Database | Primary Domain | Syntax and Key Features |
| :--- | :--- | :--- |
| **PubMed / MEDLINE** | Medicine, Biology, Health | `("term"[MeSH Terms] OR "term"[Title/Abstract]) AND ...` |
| **arXiv.org** | Computing, Physics, Mathematics | Category filters (`cat:cs.AI`, `cat:stat.ML`), immediate preprint search. |
| **Semantic Scholar** | Multidisciplinary / AI | Highly Influential Citation graphs, TLDRs, and semantic extraction. |
| **IEEE Xplore** | Electrical Engineering, Computing | `("Document Title":term AND "Abstract":term)`, focus on IEEE standards and conferences. |
| **Google Scholar** | Broad discovery (secondary) | Reverse citation tracking (*cited by*), canonical authors, and h5 metrics. |
| **SciELO & BVS** | Latin America, Lusophone world | Articles in Portuguese/Spanish, bilingual DeCS descriptors. |

---

## 🔗 4. Citation Network Analysis and Snowballing

1. **Forward Snowballing (Later Citations)**:
   - Identify which recent articles cited the seminal/foundational paper to track the evolution of the state of the art.
2. **Backward Snowballing (Earlier References)**:
   - Inspect the bibliography of the selected key articles to recover pioneering primary studies.
3. **Identification of Co-citation and Bibliographic Coupling**:
   - Detect thematic clusters and consolidated consensus versus controversies in the scientific literature.

---

## 📝 5. Evidence Synthesis Guidelines

When structuring academic reports and reviews:
- Present a Table of Study Characteristics (Author, Year, Sample/Dataset, Methodology, Main Metrics, and Limitations).
- Explicitly report potential biases (Risk of Bias) and the level of evidence (e.g., GRADE).
- Provide complete formal citations (DOI, journal, volume/issue, and authors).
