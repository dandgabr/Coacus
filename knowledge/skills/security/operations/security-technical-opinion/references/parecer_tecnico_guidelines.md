# Guidelines for Issuing a Security Technical Opinion

Formal, mandatory structure for issuing Information Security Architecture Opinions.

## Structure of the Opinion Sections

1. **Executive Summary and Verdict**:
   - Clear verdict: `APROVADO SEM RESSALVAS`, `APROVADO COM CONDIÇÕES`, or `REPROVADO / BLOQUEADO`.
   - Summary of Go-Live blockers (if any).
2. **Context and Description of the Initiative**:
   - Project name, system, vendor/partner, and business objectives.
3. **Architecture and Trust Zone Mapping**:
   - Mermaid.js diagram highlighting network boundaries (Internet, DMZ, Private VPC).
4. **Threat Modeling (STRIDE / PASTA / LINDDUN)**:
   - Detailed table of threats, attack vectors, and applicable controls.
5. **OWASP ASVS Compliance Audit (V1 to V17)**:
   - Chapter-by-chapter assessment with compliance status.
6. **Consolidated Risk Matrix (Classification P0 to P3)**:
   - 5x5 matrix crossing probability and impact.
7. **Three-Wave Remediation Roadmap**:
   - **Wave 1 (7 days)**: Pre-Go-Live (P0 blockers).
   - **Wave 2 (30 days)**: Priority Post-Go-Live (P1 items).
   - **Wave 3 (30-180 days)**: Risk acceptances and resilience (P2/P3 items).
8. **Closing Statement and Technical Signature**:
   - Date, responsible architect, and traceability hash.
