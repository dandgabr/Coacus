# English Only

**Status:** normative
**Scope:** all repository text artifacts — tracked and non-ignored untracked
documentation, ADRs and standards, skill frontmatter and bodies, agent sources,
MCP declarations, manifests, templates, source comments, docstrings and natural-
language string values.

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

Approved bilingual routing data, isolated teaching examples, foreign-language
proper titles, and individually reviewed English labels or structural fragments
use exact content exceptions in `config/language-exceptions.json`. Each entry
binds one SHA-256 digest to one repository path, declares `segment` or `file`
scope, and includes an English justification. A segment exception is permitted
only after a reviewer confirms that the exact text is an approved example, a
proper name, English that the detector cannot confidently classify, or a
non-prose structural fragment. It never permits a directory, file family, or
future text. File scope is limited to the canonical bilingual routing lexicon
and exact-hash activation fixtures that exercise its documented bilingual
behavior; any edit invalidates the exception until the exact reviewed content
is reapproved. Generated indexes are scanned through their canonical sources
and checked for drift. Directory and glob exemptions are prohibited.

## Enforcement

- `engine/validators/language.py` inventories tracked and non-ignored untracked
  text files and classifies prose, comments, docstrings and natural-language
  string values with `lingua-language-detector==2.2.0` (PyPI, resolved
  2026-10-19; [package](https://pypi.org/project/lingua-language-detector/2.2.0/))
  and `wordfreq==3.1.1` (PyPI, resolved 2026-10-19;
  [package](https://pypi.org/project/wordfreq/3.1.1/)). Lingua classifies
  multilingual prose; word-frequency evidence disambiguates short text and
  technical English that Lingua mistakes for another language. Non-English
  detections, unreadable text and unresolved language evidence block `generate`
  and `validate`; uncertain cases say `needs human review`.
- The language gate requires Python 3.12+ because the pinned detector does. Other
  Coacus tooling remains Python 3.10+ and standard-library-only.
- `engine/validators/skills.py` checks structural skill metadata; the
  `engine/validators/skill_quality.py` quality gate blocks descriptions over
  1024 characters. Language findings use the repository-wide blocking gate above.
- Translation itself is delegated to the `linguistic-specialist` agent under
  orchestrator governance; the importer owns the `pending-translation` /
  `translated` tagging.
