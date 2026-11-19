# Agent Roles

**Status:** normative
**Scope:** the specialty of each canonical agent under `knowledge/agents/`, its
declared boundaries, and the overlap between agents.

## Rule

An agent is one role on one domain. Two agents never own the same duty, and an
agent that cannot say what it does not own is not finished.

### Responsibility boundaries

Every agent source carries a `## Responsibility boundaries` section. It holds a
table `| Concern | Owner |` of the neighbouring duties the agent does not own, with
the agent that owns each, followed by a sentence that states what the agent owns
and does not own. An owner named in backticks MUST be an existing agent. An owner
written without backticks (for example "the default coding agent") is free text and
is not checked.

### Exclusive skills

A skill that defines a specialty is attached to the agent that owns that
specialty. Another agent that needs the knowledge asks the owner or loads the
skill on demand; it does not carry it permanently. The practice skills that nearly
every agent loads (`version-freshness`, `clean-code-reusability`,
`security-privacy`) are ignored when measuring overlap.

### Overlap

When at least 90% of the skills of the agent with fewer skills (at least five
skills, baseline practice skills excluded) also appear in another agent, the two
roles are one role seen twice, or one is a subset of the other. Merge them, or
split the skills so each keeps an exclusive core.

### Author and reviewer stay separate

A role that creates and the role that audits the result are never merged, even
when their skills overlap (for example `skill-creator` and `skill-auditor`, or
`game-sprite-artist` and `game-art-director`). Independence of the review is the
purpose of the pair.

### Splitting and merging

A merge is declared data, not a silent deletion: the retired agent's useful skills
and routing terms move to the absorbing agent, the lexicon and the corpus counts
are updated, and `generate` regenerates the artifacts. A split creates agents that
each have a description, a boundary table and at least one routing term.

## Rationale

Agents were added over time from several sources, so some became supersets of
others, some carried skills their body never used, and the router returned ties
between agents that look alike. Making the boundary a required, checked section
turns a review habit into a build error.

## Enforcement

- `engine/validators/specialty.py` (via `validate` and the `generate` pre-flight)
  checks the boundary section, that its owners exist, and the overlap ceiling.
- `tests/test_specialty_validator.py` covers each rule.
- The router's lexicon coverage is enforced by `engine/validators/routing.py`
  ([routing](routing.md)).
