---
name: "edtech-andragogy"
description: "Acts as a specialist in Educational Technology (EdTech) and adult learning methodologies (Andragogy), mastering instructional design, gamification, and interoperability standards (SCORM, LTI, xAPI)."
---

# 🧠 Educational Technology and Andragogy (edtech-andragogy)

This skill provides methodological guidelines, instructional design standards, and technology integration specifications aimed at adult education (Andragogy) and educational technology systems (EdTech). It should be activated whenever the agent is asked to design learning paths, conceive UX flows for e-learning platforms, structure corporate training programs, or integrate technical interoperability standards.

---

## 🎯 Skill Objective
Enable the agent to act as a Senior Instructional Designer and EdTech Engineer, ensuring that the content and software tools created meet adults' cognitive needs, promote continuous engagement, and use market-interoperable protocols.

---

## 👨‍💼 Andragogy: Adult Learning Methodology

Unlike Pedagogy (focused on children), Andragogy (formulated by Malcolm Knowles) focuses on the characteristics of the adult learner. Interfaces, platform flows, and content must follow its 6 fundamental principles:

| Principle | Practical Application in LMS / Platform Design |
| :--- | :--- |
| **Need to Know** | Clearly display the benefits of each lesson and its practical applicability at work or in the career before the course begins. |
| **Self-Concept** | Offer autonomy. Allow the adult learner to navigate at their own pace, choose their topic order, and decide when to take assessments. |
| **Role of Experience** | Create qualified discussion forums, open case studies, and spaces where learners can share their own professional experiences. |
| **Readiness to Learn** | Align content with everyday challenges. Adults learn best what they need to solve an immediate problem at work. |
| **Orientation to Learning** | Replace pure memorization of theoretical topics with active methodologies focused on solving real problems (*Problem-Based Learning*). |
| **Internal Motivation** | Focus on internal achievements (self-esteem, job satisfaction, personal development) and less on purely external rewards (grades). |

---

## 📐 Instructional Design Frameworks

### 1. ADDIE Model (Waterfall / Traditional)
Ideal for educational projects with a rigid, regulated, or large-scale scope.
*   **A**nalysis: Identification of the target audience, pedagogical objectives, and constraints.
*   **D**esign: Drafting of the script, assessment methods, taxonomy, and screen flow.
*   **D**evelopment: Creation of interactive content, media, and course assembly.
*   **I**mplementation: Launch of the training to learners on the LMS platform.
*   **E**valuation: Effectiveness measurement (Kirkpatrick Evaluation Model - Reaction, Learning, Behavior, and Results).

### 2. SAM Model (Agile / Iterative)
*Successive Approximation Model*: Ideal for fast, flexible development, using short prototyping cycles and continuous feedback (*Design Loops*).
*   Prioritize creating a **Minimum Viable Prototype (MVP)** of the course for quick testing with a small group of learners before full development.

---

## 🔌 EdTech Interoperability Standards

To ensure that content and third-party platforms work harmoniously with any LMS (Moodle, Canvas, Blackboard), use the following standards:

### 1. SCORM (1.2 / 2004)
*   **What it is**: The traditional course packaging standard.
*   **Focus**: Track course completion and transmit basic quiz scores to the LMS gradebook.
*   **Use**: Ideal for legacy self-paced content and closed packages purchased from third parties.

### 2. LTI (Learning Tools Interoperability - 1.3 / Advantage)
*   **What it is**: An integration protocol based on OAuth2 and OpenID Connect for attaching external software tools (e.g., virtual programming labs, simulators, video conferencing tools) directly inside the LMS.
*   **Benefits**: Enables Single Sign-On (SSO) for the learner from the LMS to the external tool and returns grades or progress generated outside the LMS back to the main gradebook securely.

### 3. xAPI (Experience API / Tin Can)
*   **What it is**: The modern standard for collecting learning experiences and behavior.
*   **Differentiator**: Records events in statement format (*Actor-Verb-Object*, e.g., "John viewed video Y", "Mary completed simulation Z") that occur inside or outside the LMS (mobile apps, VR, physical simulations).
*   **Storage**: Information is written to an event database called a **LRS (Learning Record Store)**.

---

## 🎮 Gamification and Active Learning

*   **Microlearning**: Break long content into 3-to-5-minute knowledge pills (short videos, interactive infographics, quizzes) to respect adults' limited time.
*   **Open Badges**: Implement verifiable digital badges and certificates based on the Open Badges specification to celebrate competency development achievements.
*   **Storytelling**: Contextualize scenarios with decision-making simulations where the learner takes on a simulated role facing real everyday corporate problems.

---

## 🔗 Related Skills
*   **Moodle Core**: [program-moodle](../../../platforms/program-moodle/SKILL.md) — General customization and Moodle LMS APIs.
*   **Moodle Design & UX**: [program-moodle-design](../../../platforms/program-moodle/SKILL.md) — Visual application of active methodologies and WCAG accessibility.
