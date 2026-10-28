---
name: academic-scientific-research
description: "Specializes in Scientific Research Methodology, Systematic Literature Review (PRISMA 2020), PICO/PECO Structuring, PRESS Appraisal, Searching Indexed Databases (PubMed/MeSH, arXiv, IEEE Xplore, Semantic Scholar, Scopus, SciELO), and Citation Networks."
---

# Academic & Scientific Research Methodology

This skill establishes the methodological and operational standard for conducting rigorous scientific investigations, formulating structured questions, running systematic searches in indexed academic databases, and synthesizing evidence without bias.

---

## 🔬 1. Question Formulation Methodology

Choose a systematic, scoping, narrative, or other review design to fit the request; do not describe a limited search as exhaustive. Select a question framework appropriate to the design and domain. PICO and PECO are useful for many comparative questions, but are not mandatory for every research question.

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
   - Screen titles and abstracts against explicit inclusion/exclusion criteria; document reviewer independence and any limits on duplicate screening.
3. **Eligibility**:
   - Obtaining the Full-Text and detailed verification of methodological variables.
4. **Inclusion**:
   - Final set of articles submitted to qualitative synthesis or quantitative meta-analysis.

Record the search date, source, exact query, filters, and access limitations for each database. Distinguish records, retrieved reports, and unique studies when reconciling screening counts. Record full-text exclusion reasons and disclose inaccessible full texts; an abstract or search snippet is not full-text assessment. Do not claim systematic coverage when the search or screening was incomplete.

### B. PRESS (Peer Review of Electronic Search Strategies) Guidelines
- **Conceptual Translation**: Identify the search concepts relevant to the question and develop appropriate free-text synonyms and controlled terms where available.
- **Controlled Vocabularies**: Where the selected database supports an applicable vocabulary, combine its terms with suitable free-text synonyms; record the vocabulary and query syntax actually used.
- **Strict Boolean Operators**:
  - `OR` intra-concept (synonyms and spelling variants).
  - `AND` inter-concept (combination of the selected search concepts).
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
- Link multiple reports of the same study and identify overlapping participant samples where evidence permits; do not count correlated reports as independent studies or silently double-count participants.
- Explicitly report potential biases (Risk of Bias) and the level of evidence (e.g., GRADE).
- Provide complete formal citations (DOI, journal, volume/issue, and authors).
- Check bibliographic identifiers and metadata against the actual source or an authoritative registry; record a citation as unverified when lookup fails. Do not invent missing fields, and distinguish unavailable information from fields that do not apply. A valid identifier alone does not establish that the source supports the cited claim.
- Separate observations, candidate hypotheses, predictions, and rival explanations. State uncertainty and do not infer a causal mechanism or research novelty from a preliminary association or a limited search.
- Distinguish prospective preregistration from a plan written after results are known; disclose exploratory or post hoc changes rather than presenting them as prespecified.
- **Verify versions and editions before asserting them** (version-freshness): resolve the current edition of a standard, protocol or tool from the publisher or an indexed publication in the current session; state the edition/revision with its source and resolution date, and mark an unresolved pin `unverified` rather than presenting it as current. Never cite a version from memory.
