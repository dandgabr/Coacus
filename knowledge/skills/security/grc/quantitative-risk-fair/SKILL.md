---
name: quantitative-risk-fair
description: Acts as a Quantitative Risk specialist applying FAIR (Factor Analysis of Information Risk) to model loss event frequency and loss magnitude, express risk in financial terms and support board-level decisions with calibrated estimates.
metadata:
  type: defensive
  phase: report
---

# Quantitative Risk Analysis (FAIR)

This skill guides the AI to move beyond red/amber/green risk matrices and express cyber risk in terms that business leaders can compare with other risks.

---

## 📊 1. The FAIR Model

- **Risk** = **Loss Event Frequency** x **Loss Magnitude**.
- **Loss Event Frequency** = Threat Event Frequency x Vulnerability (the probability that a threat event becomes a loss event).
- **Loss Magnitude** = Primary Loss (response, replacement, fines) + Secondary Loss (reputation, legal, customer churn), each a distribution rather than a point value.
- Represent inputs as ranges (min/likely/max, ideally with a distribution) and run a Monte Carlo simulation to get an annualized loss exposure.

---

## 🧮 2. Calibration

- Use calibrated estimation: ask experts for ranges and confidence, and test calibration with questions whose answers are known.
- Use empirical data where it exists (incident databases, internal history) and decomposition where it does not.
- Document every assumption; the assumptions, not the arithmetic, are what a review should challenge.

---

## 🎯 3. Using the Output

- Compare the annualized loss exposure of a risk against the cost of the control that would reduce it.
- Rank by expected loss, not by likelihood alone.
- Express risk appetite as a financial threshold the organization accepts.
- Feed the result into the risk register and the board report.

---

## ⚠️ 4. Limits

- Quantitative does not mean precise; it means explicit and comparable.
- A model with garbage inputs produces confident garbage; calibrate and validate.
- Do not let the model replace judgment; it structures it.

---

## 🔗 5. Integration with Other Skills

- For the risk register and program, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- For the architecture risk assessment, see the [security-architecture-patterns](../../operations/security-architecture-patterns/SKILL.md) skill.
- For technical opinions with severity, see the [security-technical-opinion](../../operations/security-technical-opinion/SKILL.md) skill.
- For vendor risk scoring, see the [third-party-risk-management](../third-party-risk-management/SKILL.md) skill.
