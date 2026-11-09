---
name: security-assessment-planning
description: >-
  Plans application security reviews across source code, live web applications,
  APIs, and CI supply chains. Use when a request spans multiple assessment
  surfaces or needs a scoped review plan before testing.
---

# Security assessment planning

Use this skill to choose a bounded review path and reuse the relevant Coacus
procedures. Planning does not authorize testing, scanning, requests, fuzzing,
account creation, or changes to a target. Apply the assigned security agent's
authorization gate before any active action; when authorization or scope is
missing or ambiguous, stop at a plan and request clarification.

## Route by assessment surface

- **Local source code:** begin with [SAST code review](../sast-code-review/SKILL.md).
  Add [OWASP ASVS](../appsec-owasp-asvs/SKILL.md) when the request needs a
  control-based application checklist.
- **Live web application:** use [modern web application testing](../pentest-web-application-modern/SKILL.md)
  for an authorized target; use [DAST application testing](../dast-application-testing/SKILL.md)
  only when dynamic testing is explicitly in scope.
- **API:** use [OWASP API security](../pentester-owasp-api-security-2023/SKILL.md)
  and [API protocol security](../api-protocol-security/SKILL.md) where protocol
  behavior matters.
- **CI and dependencies:** use [software supply-chain security](../software-supply-chain-security/SKILL.md)
  and [secure SDLC](../secure-sdlc-ssdf/SKILL.md).
- **Cross-surface review:** select only the relevant procedures above. A broad
  or comprehensive audit is a distinct mode; use it only when explicitly
  requested, and record excluded surfaces rather than implying full coverage.

## Build the plan

1. Restate the requested outcome, repository or target, supplied authorization
   boundary, and any exclusions. Treat unknown scope as unknown; do not infer
   permission from ownership language or from access to a URL.
2. Identify surfaces and trust boundaries. For each selected surface, name the
   linked procedure and the evidence available (source paths, API contract,
   deployment environment, or CI configuration).
3. Separate permitted static review from active testing. The latter needs a
   literal in-scope target and applicable rules of engagement before action.
   If absent, return a plan with active steps marked blocked pending scope.
4. Define coverage and stop conditions. Include likely exclusions, test-data
   limits, environment/rate constraints, and whether execution of untrusted
   build or application code is unavailable. Do not execute target code without
   an isolated, authorized environment.
5. Report candidates with evidence and status (`confirmed`, `needs validation`, or `rejected`), tracking vulnerability lifecycle in the engagement graph:
   - `DETECTED_VULNERABILITY`: Initial scanner heuristic or unconfirmed hypothesis.
   - `CONFIRMED_VULNERABILITY`: Corroborated by independent probe or code trace.
   - `HAS_VULNERABILITY`: Exploitation verified with reproducible proof-of-concept.
   Do not present an unverified candidate as a proven vulnerability.
   For findings that need filtering, follow [review findings pipeline](../../../engineering/practices/review-findings-pipeline/SKILL.md).

## Operational protocols

- **Passive Lateral Discovery (<scope_check_protocol>):**
  When testing reveals unannounced assets (subdomains, internal CIDRs, exposed buckets), register them strictly as finding candidates. Never scan or exploit lateral discoveries without explicit user scope authorization.
- **Memory Sanitization (<anonymization>):**
  Before storing reusable vulnerability guides or procedural playbooks in long-term memory, sanitize customer assets with placeholders: `{target_ip}`, `{target_domain}`, `{username}`, `{password}`, `{token}`.
- **Non-Interactive Batch CLI:**
  Security tooling running in containerized environments must use non-interactive batch invocations (e.g., `msfconsole -q -x "...; exit"`), verify listener port availability, and validate CLI arguments against tool manuals to prevent flag collisions.

## Plan output

Return a concise plan containing:

- objective, target/repository, and authorization status;
- selected surfaces and the Coacus procedures to use;
- coverage, evidence sources, exclusions, and blocked actions;
- execution prerequisites and stop conditions;
- expected report fields, including candidate status and evidence location.

Do not claim a surface was assessed until its procedure produced evidence. Do
not expand a focused request into a full audit merely because this router lists
multiple surfaces.
