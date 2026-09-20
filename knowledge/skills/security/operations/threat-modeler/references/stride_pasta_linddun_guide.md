# Comparative Guide to Threat Modeling Methodologies

Instructions for selecting and applying Threat Modeling methodologies in software architecture projects.

## 1. Methodological Selection Criteria

| Criterion / System Context | Recommended Methodology | Main Focus |
| :--- | :--- | :--- |
| Standard software architectures, APIs, and microservices | **STRIDE** | Technical vulnerabilities in software components |
| High financial risk applications or critical transactions | **PASTA** | Alignment with business risks and attacker vectors |
| Systems handling massive personal data (LGPD/GDPR) | **LINDDUN** | Privacy violations and undue traceability |
| Need for strict mathematical risk scoring | **DREAD** | Quantitative prioritization of remediation (score from 1 to 10) |
| Agile environments / DevSecOps at corporate scale | **VAST** | Continuous visual modeling for engineering teams |

## 2. DREAD Methodology (Score Calculation)

$$\text{DREAD Score} = \frac{D + R + E + A + D_{isc}}{5}$$

- **Damage Potential (D)**: How severe is the damage if the attack succeeds? (1 = Minimal, 10 = Catastrophic)
- **Reproducibility (R)**: How easy is it to reproduce the attack? (1 = Nearly impossible, 10 = Always reproducible)
- **Exploitability (E)**: How much effort and knowledge are required? (1 = Expert with advanced tools, 10 = Lay user with a ready-made script)
- **Affected Users (A)**: How many users are impacted? (1 = A negligible percentage, 10 = All users)
- **Discoverability (Disc)**: How easy is it to discover the vulnerability? (1 = Very difficult, 10 = Public information)
