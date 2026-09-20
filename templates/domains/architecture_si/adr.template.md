# ADR [Number]: [Concise Architectural Decision Title]

* **Status**: [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED by ADR-XXXX]
* **Decision Makers**: [Security Architect, Tech Lead, Principal Engineer]
* **Date**: [YYYY-MM-DD]
* **Tags**: [security, messaging, database, authentication, cloud]

---

## Context and Problem Statement
[Describe the system context, the technical or functional need, and the engineering challenge that motivated this decision.]

---

## Decision Drivers (Key Forces and Requirements)
* **Driver 1**: [e.g. p99 latency below 50ms under 10k RPS]
* **Driver 2**: [e.g. strict compliance with LGPD (Art. 11 - Sensitive Health Data)]
* **Driver 3**: [e.g. dynamic secret rotation without service downtime]

---

## Considered Options
1. **Option 1**: [Alternative A Name - e.g. Implementation via Apache Kafka]
2. **Option 2**: [Alternative B Name - e.g. Implementation via RabbitMQ / AMQP]
3. **Option 3**: [Alternative C Name - e.g. Synchronous REST calls with Circuit Breaker]

---

## Decision Outcome
Chosen **[Option X: Alternative Name]**, because [technical rationale, alignment with the drivers, and cost/benefit analysis].

---

## Consequences and Trade-offs

### 🟢 Positive Consequences
* [Direct benefit 1: e.g. Temporal decoupling and durable on-disk retention]
* [Direct benefit 2: e.g. Ease of onboarding new analytical consumers]

### 🔴 Negative Consequences / Operational Costs
* [Accepted trade-off 1: e.g. Greater operational complexity in cluster management]
* [Accepted trade-off 2: e.g. Need to handle eventual consistency and idempotency]

---

## Pros and Cons of the Analyzed Alternatives

### [Option 1: Alternative A Name]
* **Pros**: [Strength]
* **Cons**: [Weakness]

### [Option 2: Alternative B Name]
* **Pros**: [Strength]
* **Cons**: [Weakness]

---

## Links and References
* [RFC / Project Technical Documentation](<project-doc-url>)
* [Applicable OWASP ASVS Security Standard](https://owasp.org/www-project-application-security-verification-standard/)
