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
   - Use exact terms: `Resumo Profissional` (or `Professional Summary`), `Experiência Profissional` (`Work Experience`), `Formação Acadêmica` (`Education`), `Habilidades Técnicas` (`Technical Skills`).
   - Avoid creative terms such as "What drives me" or "My journey".
3. **Contact Data Formatting**:
   - Put name, email, phone, LinkedIn, and city/country in the main upper body of the document (never in Word/PDF footers or headers).
4. **Uniform Date Format**:
   - Use a consistent format across all positions: `MM/AAAA - MM/AAAA` (e.g., `03/2022 - Atual`).

---

## 🎯 2. Keyword Engineering and Scoring

ATS algorithms rank candidates by comparing the density, frequency, and semantic context of the job posting's keywords against the resume:

- **Mapping Hard Skills and Tools**:
  - Extract the technologies, methodologies, and certifications required in the job description.
  - Ensure both the full term and its acronym appear:
    - Example: `Search Engine Optimization (SEO)`, `Amazon Web Services (AWS)`, `Continuous Integration / Continuous Delivery (CI/CD)`.
- **Mandatory Contextualization**:
  - Do not create sterile keyword lists at the end of the document (modern parsers penalize them). Integrate the terms into achievement descriptions.

---

## 📊 3. Impact Formula for Experience Bullets (Google XYZ Formula)

Every achievement bullet must follow the high-impact formula:
$$\text{Achieved [X]}, \text{ as measured by [Y]}, \text{ by doing [Z]}$$

- **Weak**: "Responsible for developing the payments API."
- **Strong (XYZ)**: "Reduced payments processing latency by 35% (from 1.2s to 780ms) for 200,000 daily transactions by refactoring endpoints and implementing a distributed Redis cache."

---

## ✅ 4. Pre-Submission Checklist (ATS Audit)

- [ ] Single-column layout with no tables, text boxes, or images.
- [ ] Name and contacts in the document body (not in a header/footer).
- [ ] At least 75% to 85% semantic match on essential keywords.
- [ ] Achievements quantified with percentages, financial amounts, latency, or volume.
- [ ] File saved as `.docx` or `.pdf` with a selectable text layer (not rasterized).
