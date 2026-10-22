---
name: cover-letter-application-drafter
description: >-
  Provides strategic drafting and adversarial review for cover letters and portal application forms. Use when authoring customized cover letters, completing online application free-text questions, or running dual-agent drafter-reviewer validation.
---

# Cover Letter & Application Form Drafter

This skill governs the production of high-converting, factually grounded cover letters and portal application form responses through a dual-agent *Drafter-Reviewer* architecture.

---

## 🎭 1. Drafter-Reviewer Dual-Agent Workflow

High-stakes application writing must separate the creative drafting process from adversarial evaluation:

1. **The Drafter (Author)**: Generates tailored content based on the target posting, candidate profile, and verified company background.
2. **The Reviewer (Hiring-Manager Proxy)**: Evaluates the draft in a clean, isolated context with read-only tools. The Reviewer acts as a skeptical technical hiring manager.
3. **Structured Review Return Contract**:
   The Reviewer must structure feedback in two mandatory parts:
   - **Part A (Structured Edit Directives):** A JSON array of literal text replacements:
     ```json
     [
       {
         "old_string": "I was responsible for leading cloud migration.",
         "new_string": "Migrated 14 microservices from on-premise VMs to AWS EKS, reducing deployment cycle time by 40%.",
         "reason": "grounding | keyword_match | company_angle | reframing | style"
       }
     ]
     ```
   - **Part B (Narrative Critique):** Strategic feedback on tone, company value proposition, and perceived authenticity.

---

## 🔍 2. Factual Grounding Audit & Interview Backtrack Test

Every statement in an application artifact must withstand deep technical scrutiny during an on-site interview:

### Grounding Audit Against Candidate Sources
- Every metric, technology, company name, and project scope must trace directly to verified candidate documentation (`cv/`, `linkedin/`, `diplomas/`, GitHub codebases).
- **Zero Hallucination:** Never invent statistics, claim unearned ownership of team projects, or pad technical stacks with unverified tools.

### The Interview Backtrack Test
Evaluate all promotional claims against the question: *"If the interviewer asks you to spend 20 minutes explaining this bullet on a whiteboard, can you defend it effortlessly?"*
- **Legitimate Reframing:** Presenting verified experience through the terminology and priorities of the hiring company. Allowed.
- **Gray Zones:** Conflating academic prototypes with production enterprise environments, or claiming individual credit for a cross-departmental migration. Must trigger an explicit user prompt:
  `"Flagged statement: [...]. Keep, soften, or drop?"`
- **Fabrication:** Inventing roles, certifications, or metrics. Strictly prohibited.

### Requirement Coverage & Bridges
- Every non-negotiable requirement in the job posting must be addressed.
- When the candidate has a known gap, never omit it silently. Build an **honest adjacent bridge**:
  $$\text{Acknowledge Gap} \longrightarrow \text{Demonstrate Equivalent Mastery in Adjacent Stack} \longrightarrow \text{Rapid Learning Trajectory}$$
  *(e.g., "While my primary distributed streaming experience is built on Apache Kafka, the partitioned messaging paradigms directly translate to your AWS Kinesis pipelines.")*

---

## ✍️ 3. Forward-Looking Cover Letter Engineering

A cover letter is not a prose recitation of a resume; it is a forward-looking proposal demonstrating what the candidate will build, fix, or optimize for the employer.

### Structural Budget
- **Length:** Strict 1-page budget (250–300 words).
- **Subject Formula:** `Application for [Role Title] — [Specialization / Core Differentiator]`
- **Four Core Paragraphs:**
  1. *The Hook & Alignment:* The specific business challenge or product milestone this team is tackling and why you are applying now.
  2. *Primary Technical Proof Point:* A deep, metric-backed story of a high-complexity project that mirrors their current engineering bottleneck.
  3. *Adjacent Mastery & Velocity:* How your broader background closes their ancillary requirements.
  4. *Forward-Looking Value & Call to Action:* What you will investigate or deliver in your first 90 days.
- **Language & Style Constraints:**
  - Ban generic clichéd openers (*"I am writing to express my enthusiastic interest..."*).
  - Eliminate apologetic framing (*"Although I lack...", "I may not have..."*).
  - Avoid artificial typographical quirks like intrusive em-dashes (`—`) in running prose.
  - Require independent fact-checking for every factual assertion made about the hiring company's products or market position.

---

## 📝 4. Portal Application Form Fields (The Third Artifact)

Modern ATS portals (Greenhouse, Lever, Ashby) feature custom free-text prompts alongside resume uploads. Prepare dedicated responses:

1. **Executive Self-Introduction (100–200 words)**:
   - Lead immediately with the strongest differentiator and current technical focus, not chronological origins.
2. **Structured Project Summaries**:
   - Provide two modular lengths: ~150 words (comprehensive) and ~60 words (elevator pitch).
   - Enforce explicit distinction between individual contribution vs. overall team scope.
3. **Character-Capped Responses**:
   - For fields with strict limits (e.g. 280, 500, or 1000 characters), measure exact string lengths programmatically and provide 4–6 tailored length variants.
4. **Internal `NOTE TO SELF` Blocks**:
   - Accompany form field submissions with tactical notes highlighting rationale, alternative options, and sensitive points to keep in mind if asked during screening.
