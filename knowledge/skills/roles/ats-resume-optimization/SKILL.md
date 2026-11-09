---
name: ats-resume-optimization
description: "Specialist in Resume Engineering and Optimization for ATS (Applicant Tracking Systems). Masters single-column parsing, keyword semantic density, acronyms, XYZ-formula impact metrics, and job-description compatibility auditing."
---

# ATS Resume Optimization & Keyword Engineering

This skill establishes the technical and analytical methodology for architecting, reviewing, and optimizing resumes aimed at **ATS (Applicant Tracking Systems)** such as Greenhouse, Lever, Workday, Taleo, iCIMS, and Ashby.

---

## 🧭 1. Principles of Algorithmic Resume Parsing

The ATS converts the file into raw text through OCR or a semantic parser before computing the relevance score (*Match Score*). To prevent data loss and structural corruption:

1. **Strictly Single-Column Layout**:
   - Never use tables, multi-column grids, floating text boxes, or sidebars.
   - Text placed inside text boxes is frequently ignored by the parser.
2. **Universal, Standardized Headings**:
   - Use exact terms: `Professional Summary`, `Work Experience`, `Education`, `Technical Skills` (or their equivalents in the resume language).
   - Avoid creative terms such as "What drives me" or "My journey".
3. **Contact Data Formatting**:
   - Put name, email, phone, LinkedIn, and city/country in the main upper body of the document (never in Word/PDF footers or headers).
4. **Uniform Date Format**:
   - Use a consistent format across all positions: `MM/YYYY - MM/YYYY` (e.g., `03/2022 - Present`).

---

## 🎯 2. Keyword Engineering and Scoring

ATS algorithms rank candidates by comparing the density, frequency, and semantic context of the job posting's keywords against the resume:

- **Mapping Hard Skills and Tools**:
  - Extract the technologies, methodologies, and certifications required in the job description.
  - Ensure both the full term and its acronym appear:
    - Example: `Search Engine Optimization (SEO)`, `Amazon Web Services (AWS)`, `Continuous Integration / Continuous Delivery (CI/CD)`.
- **Mandatory Contextualization**:
  - Do not create sterile keyword lists at the end of the document (modern parsers penalize them). Integrate the terms into achievement descriptions.

### 4-State Keyword Coverage Matrix
When auditing a resume against a target job specification, classify every requirement into one of four distinct states:
1. **Covered**: Keyword or skill explicitly present in the resume with contextual proof.
2. **Synonym-Only**: Concept present under an alternate phrasing (e.g. *Postgres* when the job requests *PostgreSQL*, or *REST API* when the job requests *HTTP Web Services*). Prefer adopting the job posting's exact term if factually accurate.
3. **Missing (Have it)**: The candidate possesses this skill (corroborated in profile/background sources) but it is currently omitted from the draft. Add contextual bullet points to bridge the gap.
4. **Missing (Real gap)**: The candidate lacks this competency. **Strictly forbid keyword stuffing or fabricating experience.** Acknowledge real gaps for coverage in interview preparation or as adjacent bridge experiences.

---

## 📊 3. Impact Formula for Experience Bullets (Google XYZ Formula)

Every achievement bullet must follow the high-impact formula:
$$\text{Achieved [X]}, \text{ as measured by [Y]}, \text{ by doing [Z]}$$

- **Weak**: "Responsible for developing the payments API."
- **Strong (XYZ)**: "Reduced payments processing latency by 35% (from 1.2s to 780ms) for 200,000 daily transactions by refactoring endpoints and implementing a distributed Redis cache."

### Tenure-to-Output Ratio & In-Progress Credentials
- **Long Tenure Re-balancing:** When a candidate has spent multiple years (3+ years) at a single company with only 2–3 brief bullets, parsers and hiring managers perceive low output velocity. Apply three honest remedies:
  1. Break the tenure into distinct phases or promotions (e.g. *Software Engineer II* → *Senior Engineer*).
  2. Surface secondary initiatives, architecture decisions, and cross-team mentoring.
  3. Frame the multi-year cycle explicitly around the domain's long-horizon delivery lifecycle (e.g., medical device certification, compliance overhauls).
- **In-Progress Academic & Professional Credentials:** Never list an in-progress degree or certification as completed. Always use explicit status notation: `In progress, expected MM/YYYY` or `Candidate, Thesis defense MM/YYYY`.

---

## ✂️ 4. Relevance-Weighted Content Cutting (Signal Over Chronology)

When a resume exceeds the targeted page budget (e.g. 1 or 2 pages), never truncate older experiences blindly based on chronology alone:
1. **Relevance Scoring:** Score each bullet point across three dimensions:
   - *Target Posting Match:* Direct alignment with critical job requirements.
   - *Document Uniqueness:* Demonstrates a capability not evidenced in other bullets.
   - *Narrative Offload:* Can this bullet be omitted from the resume because it is better suited for deep discussion in the cover letter?
2. **Pruning Sequence:** Cut bullets with the lowest total relevance score first. Summarize early foundational roles into single-line scope summaries rather than deleting them entirely.

---

## 🔍 5. Post-Compilation PDF Text-Layer Audit

Before submitting any compiled PDF resume:
1. **Extract Raw Text Layer:** Use `pdftotext -layout -enc UTF-8` or `pypdf` to inspect the literal character stream seen by ATS parsers.
2. **Defect Checklist:**
   - **No corrupted CID glyphs:** Search for `(cid:NNN)` or `\uFFFD` character replacements caused by missing font encodings.
   - **No icon-only contacts:** Ensure phone numbers, email addresses, and LinkedIn URLs include complete literal text rather than relying on decorative font glyphs.
   - **Reading order verification:** Verify that text extracted from two-column headers or horizontal metadata strips reads in logical sequence without interleaving names and phone numbers.
   - **ASCII date separators:** Verify that all date intervals use standard ASCII hyphens (`-`) rather than Unicode en-dashes (`--` or `U+2013`), which frequently corrupt Workday date tokenizers.

---

## ✅ 6. Pre-Submission Checklist (ATS Audit)

- [ ] Single-column layout with no tables, text boxes, or images.
- [ ] Name and contacts in the document body (not in a header/footer).
- [ ] At least 75% to 85% semantic match on essential keywords.
- [ ] Achievements quantified with percentages, financial amounts, latency, or volume.
- [ ] File saved as `.docx` or `.pdf` with a selectable text layer (not rasterized).
