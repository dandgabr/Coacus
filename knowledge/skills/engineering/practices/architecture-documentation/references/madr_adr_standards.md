# MADR Standard (Markdown Architectural Decision Records)

Formal structure for recording architectural decisions.

## Standard Format

```markdown
# ADR [Number]: [Decision Title]

* **Status**: [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED]
* **Deciders**: [Names / Roles of Those Involved]
* **Date**: [YYYY-MM-DD]

## Context and Problem Statement
[Description of the technical or business scenario and the need for the decision]

## Decision Drivers
* [Driver 1: e.g. p99 latency < 50ms]
* [Driver 2: e.g. strict LGPD compliance]

## Considered Options
* [Option 1: Name of Alternative A]
* [Option 2: Name of Alternative B]
* [Option 3: Name of Alternative C]

## Decision Outcome
[Chosen option and core technical justification]

### Positive Consequences
* [Benefit 1]
* [Benefit 2]

### Negative Consequences / Trade-offs
* [Negative impact 1 or accepted operational debt]
* [Mitigated trade-off]
```
