# English Only

**Status:** normative
**Scope:** every tracked artifact — documentation, ADRs and standards, skill
frontmatter and bodies, agent sources, MCP declarations, manifests, templates,
code comments and commit messages.

## Rule

All repository artifacts are written in English. This is not a preference about
tone; it is a single-language contract that makes the corpus reviewable, searchable
and portable across contributors and harnesses.

- Skills, workflows, agents, MCP declarations, docs and templates MUST contain
  English prose.
- Code comments and commit messages MUST be English.
- Legacy non-English material MUST be translated during import, never copied
  verbatim. Imported files are tagged `pending-translation` until their translation
  lands, then `translated`.
- Descriptions in frontmatter MUST be English and written in the third person.

The one standing exception is chat interaction with the repository owner, which
remains Portuguese. That exception governs conversation, not tracked artifacts.

## Rationale

Coacus unifies corpora that arrived with Portuguese content mixed into English
tooling. Allowing both languages means every reader, every search and every
validator must handle two vocabularies, and a duplicated fact can hide behind a
translation. One language makes the corpus uniform and the language check
mechanical.

## Exemptions

A small, explicit set of files is intentionally non-English or intentionally
quotes non-English material. They are listed in `LANGUAGE_EXEMPT` in
`engine/validators/skills.py`, `ASSET_EXEMPT` and `FENCE_EXEMPT` in
`engine/validators/language.py` — for example the Portuguese linguistic skill and
skills that quote upstream Portuguese examples as teaching material. The prose
check SKIPS prose inside fenced code blocks, inline code spans and markdown link
targets, because samples, identifiers and anchor slugs are not prose.

A SEPARATE fence gate covers the excluded area: `language.fence_errors()` scans
inside fenced code blocks for strong Portuguese markers, because an ASCII
diagram, a code comment or a string literal carrying Portuguese is still a
single-language-contract violation (F6b). It runs in the `generate` pre-flight
and in `validate` as a blocking error. Files whose fences legitimately quote
Portuguese are listed in `FENCE_EXEMPT`; individual lines that must stay
Portuguese (a Brazilian place name, a Presidio demo string) are allowed via
`FENCE_LINE_ALLOW`.

## Enforcement

- `engine/validators/language.py` scans `knowledge/skills/**`, `knowledge/agents/**`
  and `methodology/workflows/**` for non-English prose (reported as warnings by
  `python3 scripts/coacus.py validate`) and for non-English content inside code
  fences (`fence_errors()`, reported as blocking errors).
- `engine/validators/skills.py` (`warnings()`) reports non-English markers per
  skill and oversized descriptions.
- Translation itself is delegated to the `linguistic-specialist` agent under
  orchestrator governance; the importer owns the `pending-translation` /
  `translated` tagging.
