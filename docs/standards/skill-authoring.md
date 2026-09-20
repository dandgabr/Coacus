# Skill Authoring

**Status:** normative
**Scope:** every `SKILL.md` under `knowledge/skills/` and
`methodology/workflows/`, and every reference or example asset shipped beside
one.

## Rule

### One body, agnostic

A canonical skill body prescribes ACTIONS and intentions. It MUST NOT name a
harness tool. "Read a file", "run shell commands", "search files" — never `Read`,
`Bash`, `grep`, `view_file` or any other native tool name.

Per-harness tool mappings live OUTSIDE the canonical body, in
`references/<harness>-tools.md`, linked from a "Harness Adaptation" section when
one applies. The mapping data also lives in `harnesses/<h>/harness.json`
(`tool_mapping`, `tool_denylist`).

Porting a skill to a new harness MUST NOT edit the body. It adds or updates a
reference file and, when needed, a harness manifest.

### Location and depth

Both skill roots share one flat name namespace:

- `knowledge/skills/<category>[/<subcategory>]/<skill>/SKILL.md` — depth 2 or 3
  below the root.
- `methodology/workflows/<skill>/SKILL.md` — depth 1 below the root.

A `SKILL.md` MUST live at the correct depth for its root. Nested `SKILL.md` files
beneath another skill directory are forbidden.

### Frontmatter

- `name` — kebab-case and MUST equal the enclosing directory name.
- `description` — REQUIRED, English, third person, trigger-oriented. It is the
  discovery surface, so it MUST say what the skill does and when it applies.
- Slugs MUST be globally unique across both roots.

### Content

- Local markdown links MUST resolve. Broken relative links fail validation.
- Reference assets (`references/`, `examples/`) are exempt from the anti-tool
  rule: that is their sanctioned purpose.

## Rationale

A skill that cites concrete harness tools locks itself to one harness; the next
harness needs a copy and the two copies drift. Keeping the body agnostic and the
mapping external means the canonical content is written once and every harness
gets a thin adapter.

## Enforcement

- `engine/validators/skills.py` (via `python3 scripts/coacus.py validate`) checks
  frontmatter parsing, kebab-case name equal to the directory, required
  description, global slug uniqueness, correct placement depth, no nested
  `SKILL.md`, and resolution of local links.
- `engine/validators/hygiene.py` enforces the tool-name denylist over canonical
  skill bodies, authoring templates, the bootstrap wrapper and workflow skills.
  The denylist is the union of a built-in seed and every
  `harnesses/*/harness.json` `tool_denylist`; `references/` directories are
  exempt.
- `tests/test_skills.py` covers the placement and link rules.
