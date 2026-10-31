---
name: cro-onboarding-experimentation
description: "Provides Conversion Rate Optimization (CRO), product onboarding funnels, A/B testing statistical rigor, user activation, and friction elimination based on Ron Kohavi (Trustworthy Online Controlled Experiments), Sean Ellis (Hacking Growth), and the Fogg Behavior Model (B=MAP). Use when analyzing conversion funnels, designing product activation sequences, planning multivariate experiments, or auditing drop-off points."
---

# Conversion Rate Optimization & Activation Experimentation

Establish rigorous online controlled experimentation protocols, statistical test validity, onboarding funnel optimization, and behavioral activation loops.

---

## 🔬 1. Trustworthy Experimentation & Statistical Discipline (Kohavi Framework)

Online controlled experiments (A/B testing) prevent shipping changes based on the Highest Paid Person's Opinion (HiPPO).

### A. The Experimentation Integrity Checklist
1. **Sample Size & Power Calculation (Pre-Flight):**
   - Calculate minimum detectable effect (MDE) and sample size before launching any experiment.
   - Enforce standard statistical bounds: $\alpha = 0.05$ (type I error / false positive rate), $\beta = 0.20$ (power $1 - \beta = 0.80$).
   - Never stop a test early because results look promising after a few days (*peeking problem* inflates false positive rates from 5% to over 30%).
2. **Sample Ratio Mismatch (SRM) Test:**
   - Always run a chi-squared ($\chi^2$) goodness-of-fit test on incoming traffic variants (e.g., expected 50/50 split).
   - If $p < 0.001$ on the ratio of users assigned to treatment versus control, the experiment suffers from Sample Ratio Mismatch (redirect drop-off, bot filtering asymmetry, or tracking race conditions). Invalidate and abort the test immediately.
3. **Guardrail Metrics:**
   - Every experiment must define both a **Target Metric** (e.g., signup conversion, checkout completion) and **Guardrail Metrics** (e.g., page load latency, bounce rate, support ticket volume, 30-day retention).
   - A treatment that increases short-term signups while degrading page load speed by $400\text{ms}$ or increasing 7-day churn fails the guardrail test.

---

## ⚡ 2. The Fogg Behavior Model in Product Onboarding ($B = MAP$)

A behavior happens only when three elements converge simultaneously:
$$B = M \cdot A \cdot P$$
- **$M$ (Motivation):** The user's internal desire to achieve the outcome.
- **$A$ (Ability):** The ease with which the user can complete the task (lower friction = higher ability).
- **$P$ (Prompt / Trigger):** The cue that invites the user to take action now.

```
High Motivation
▲              Action Line
│              . *
│           . *     [Successful Behavior]
│        . *        Target Action Triggered
│     . *
│  . *              [Failed Attempts]
│ *                 High friction, weak prompt, low motivation
└──────────────────────────────────────────────────────────► High Ability (Easy)
```

### Actionable Activation Rules:
1. **Reduce Steps to Value (Time-to-Value - TTV):**
   - Defer non-critical setup steps (email verification, team invites, profile avatars) until after the core "Aha! moment" has occurred.
   - Example: Let developers run their first query against a sandbox database before forcing them to configure OAuth SSO.
2. **Empty States as Launchpads:**
   - Never show an empty white container with "No data found".
   - Supply pre-seeded templates, one-click demo data, or guided playground environments so users experience value immediately.

---

## 📊 3. Funnel Drop-Off Audit & Diagnostic Protocol

When diagnosing conversion friction across an existing funnel:

```
Step 1: Landing Page ──► Step 2: Signup Form ──► Step 3: Workspace Setup ──► Step 4: Core Action (Aha!)
      (Drop 65%)               (Drop 20%)                (Drop 45%)                 (Drop 30%)
```

### Diagnostic Sequence:
1. **Quantitative Telemetry Check:**
   - Measure drop-off rates at every step broken down by device type (desktop vs. mobile), browser, and traffic acquisition channel.
   - A sharp drop-off isolated to mobile Safari signals an interface layout bug or autofill breakdown rather than copy friction.
2. **Field-Level Form Analytics:**
   - Identify form fields with high time-spent, multiple backspaces, or high exit rates.
   - Eliminate unnecessary fields: every additional form input decreases B2B conversion by an average of 3% to 5%.
3. **Cognitive Load & Choice Architecture:**
   - Apply Hick's Law ($T = b \cdot \log_2(n + 1)$): reducing the number of choices logarithmically reduces decision time and abandonment.
   - Highlight one clear recommended default tier or action path.

---

## 🔄 4. ICE / RICE Prioritization for Growth Ideas

Prioritize experiment backlogs objectively using the RICE framework:

$$\text{RICE Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}$$

- **Reach:** How many users will encounter this change in a given quarter?
- **Impact:** How much will this increase conversion for those who encounter it? (3 = massive, 2 = high, 1 = medium, 0.5 = low).
- **Confidence:** How certain are you of the reach and impact estimates? (1.0 = high data/evidence, 0.8 = medium, 0.5 = low/speculative).
- **Effort:** How many engineering/design person-weeks are required? (1 to 5).

---

## 📚 References & Authority

- Kohavi, Ron, Tang, Diane, & Xu, Ya. *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press, 2020.
- Ellis, Sean, & Brown, Morgan. *Hacking Growth: How Today's Fastest-Growing Companies Drive Breakout Success*. Currency, 2017.
- Fogg, B.J. *Tiny Habits: The Small Changes That Change Everything (Fogg Behavior Model)*. Houghton Mifflin Harcourt, 2019.
- Hulick, Samuel. *The Elements of User Onboarding*. User Onboard Press, 2014.
