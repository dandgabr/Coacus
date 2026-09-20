---
name: business-logic-flaws
description: Acts as a specialist in business logic and abuse-case security, covering unrestricted access to sensitive business flows, transaction authorization gaps, race conditions, replay, coupon and refund abuse, and the modeling of misuse cases that static scanners cannot detect.
metadata:
  type: defensive
  phase: exploitation
---

# Business Logic Flaws and Abuse Cases

This skill guides the AI to find and prevent **logic flaws** - vulnerabilities that arise from a correct implementation of the wrong rules. Automated scanners rarely catch them because the code behaves as written; the flaw is in the intended behavior, not the syntax.

---

## 🧠 1. Think in Abuse Cases

For every business flow, ask not only "does it work?" but "how can it be made to work in a way we did not intend?" Pair each use case with an **abuse case** and a control.

| Flow | Abuse case | Control |
| :--- | :--- | :--- |
| Checkout | Negative quantity or price manipulation | Server-side price and quantity validation |
| Refund | Refund to a different payment method | Bind refund to the original instrument |
| Coupon | Reuse, stacking, or brute-forcing codes | Single-use enforcement, rate limits, entropy |
| Transfer | Race condition on the balance | Atomic transactions and idempotency keys |
| Signup | Referral or bonus farming | Identity and rate controls |

---

## ⚙️ 2. High-Risk Logic Classes

1. **Unrestricted access to sensitive business flows** (OWASP API6:2023): an expensive or sensitive operation can be called at will (scraping, SMS sending, purchasing). Mitigate with server-side rate limits and proof of work.
2. **Transaction authorization gaps**: the server trusts a client-supplied amount, discount or role. Recompute all security-relevant values on the server.
3. **Race conditions (TOCTOU)**: concurrent requests pass the same check (double-spend, coupon reuse). Use atomic operations, locking, or idempotency keys.
4. **Replay and idempotency**: a valid request is replayed with profit. Require a nonce or idempotency key and reject duplicates.
5. **State-machine abuse**: the workflow is walked out of order (skip payment, approve one's own request). Enforce server-side state transitions.
6. **Parameter tampering on hidden fields**: role, tenant or price hidden in the client. Never trust hidden fields.

---

## 🧪 3. Methodology

- Map every money-, permission- or trust-changing flow and write its abuse cases before implementation.
- Test with a "malicious but compliant" mindset: valid requests, wrong sequence, wrong values, wrong scale.
- Use property-based testing for arithmetic and state invariants.
- Review logs to detect abuse patterns post-release, since many logic flaws only appear in aggregate.

---

## 🔗 4. Integration with Other Skills

- For the API risk taxonomy this maps to, see the [api-protocol-security](../api-protocol-security/SKILL.md) skill.
- For design-time misuse modeling, see the [threat-modeler](../../operations/threat-modeler/SKILL.md) skill.
- For the overall risk ranking, see the [owasp-top-10-2025](../owasp-top-10-2025/SKILL.md) skill.
