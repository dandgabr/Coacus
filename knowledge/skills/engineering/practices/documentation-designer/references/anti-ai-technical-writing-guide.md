# Editorial Review for Technical Prose

## Choose the language of the deliverable

1. Follow an explicit target language or regional variant, subject to the destination repository's artifact rules. A request to revise prose implies keeping its language unless translation is requested.
2. For edits and additions inside an existing section, inherit that section's language and established variant. In mixed-language documents, apply this per section. Preserve intentional language changes, quotations, and technical literals. Choose the language of the conversation separately.
3. For a new document, follow the destination project's convention when the request leaves the language open. Otherwise use the request language. For Portuguese, English, and Spanish with no regional convention, use Brazilian Portuguese, American English, and neutral Latin American Spanish respectively.
4. Apply the relevant language skill to the deliverable. For varieties without dedicated guidance, use the shared review and follow any regional conventions supplied by the author, project, or reader.

## Revise for the reader

1. Identify what the reader needs to know or do. Lead with the finding in a report, the prerequisite and action in a how-to, or the failed assertion in a test summary. A decision record leads with the decision and the reason recorded for it.
2. Cut setup that delays the point, generic praise, redundant endings, and explanations the intended reader already has. Vary sentence length where it clarifies how facts fit together. Keep deliberate repetition when it helps the reader follow a procedure or compare results.
3. Compare the final prose with the source. Keep meaning, scope, attribution, severity, and uncertainty. Preserve filenames, identifiers, commands, flags, link destinations, error messages, units, counts, and test states. Keep quoted material, code blocks, frontmatter, and raw output intact during a prose edit. Use details supplied by the evidence. If the evidence is incomplete, keep the uncertainty visible.

For a procedure with a copyable command, give the prerequisite first and put
the command on its own line. Use a fenced code block in Markdown. Put the
expected output after the command so the reader can check success.

For a report, attribute observations to their source. When evidence supports
investigating a possible cause, state what it might explain and whether it has
been confirmed. If the reader needs to open a log or other evidence, give its
reference a short sentence or line of its own. Describe the contents only
when the source establishes them.

## Examples with source facts

| Deliverable | Source facts | Revised prose |
| --- | --- | --- |
| Report | The queue reached 80 jobs at 09:00 UTC. An upstream slowdown is suspected. | The queue reached 80 jobs at 09:00 UTC. An upstream slowdown remains a hypothesis. |
| Guide | The service must be running. The operator then runs `demo check --read-only`. | Start with the service running. Run `demo check --read-only`. |
| Tests | The export suite recorded 12 passed, 1 failed, 3 skipped. `test_empty_export` expected an empty file and received a header row. Browser tests were outside the run. | `test_empty_export` failed. It expected an empty file and received a header row. Twelve export tests passed and three were skipped. Browser tests were outside the run. |

Before publishing, also check that the document serves its intended Diátaxis purpose, code examples include their prerequisites, and diagrams render with their existing labels.

The reader-focused revision and final comparison with the source were informed by [Humanizer at revision a48c60c2a3f7a0f6ecc8f9b8d2b1ef71c7927155](https://github.com/blader/humanizer/blob/a48c60c2a3f7a0f6ecc8f9b8d2b1ef71c7927155/SKILL.md). Reviewed on 2026-11-19.
