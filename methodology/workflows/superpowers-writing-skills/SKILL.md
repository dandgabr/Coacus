---
name: superpowers-writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

<!--
Coacus adaptation of a Superpowers workflow (MIT).
Upstream: https://github.com/obra/superpowers @ 5bf4e78011075bcfc0dc295f0724994cd123ee71
Process artifacts are written under docs/temp/.
Conventions: ../using-coacus/references/coacus-process-conventions.md
-->

# Writing Skills

Create or revise reusable guidance that changes a relevant decision without expanding the user's task. Preserve one canonical source and use the repository's authoring contract; installed copies and generated discovery files are outputs.

## Choose the owner before writing

Find the existing skill and read its package: description, body, references, examples and callers. Resolve the canonical source rather than promoting a stale installed alias. Prefer a focused improvement to an existing owner; create a new skill only when it has a distinct trigger and useful responsibility.

Separate observed failure, inferred cause, proposed instruction and evaluated outcome. Keep observations traceable to their source and revision. A one-project recipe or preference belongs in project context unless its reusable principle and limits can be explained.

Use [writing for agents](references/writing-for-agents.md) for pointer quality, hierarchy and pruning; [invocation model](references/invocation-model.md) for user-invoked versus model-invoked reach. Read the relevant reference rather than loading every resource by default.

## Design the whole package

- Keep purpose, activation conditions, essential constraints and routing in `SKILL.md`.
- Put substantial conditional procedures in named references and link them at the decision where they are needed.
- Add examples or scripts only when they teach or reliably perform a repeated operation. Follow the repository's runtime and portability constraints.
- Define a concept in one place. Replace duplicate passages with a discoverable owner link; do not scatter one procedure among unrelated files.
- Preserve style-specific knowledge and actual task permissions. General taste advice does not override functional requirements or the product's chosen visual language.

A complete review can conclude `no-change` with a reason. Appending the same generic checklist to every skill is not a complete review.

## Frontmatter and discovery

Use a kebab-case name matching the directory and an English, third-person, trigger-oriented description. Follow the local field limits and supported metadata. Explain the capability and when it applies without turning the description into a step-by-step workflow or an exhaustive keyword list.

Use the canonical template for the skill's location. Keep local links resolvable. References and examples should be reachable through an explicit condition; a file nobody is told to consult is not useful progressive disclosure.

## Validate decisions and content

For a change intended to alter agent behavior, define realistic scenarios before claiming success. Use [behavioral validation](references/behavior-validation.md) for old/candidate comparisons, blind forward tests, counterexamples and evidence depth. See the [portable worked comparison](examples/guidance-comparison.md) for a passing-baseline example and an already-correct control. For pressure-test construction, consult [testing skills with subagents](testing-skills-with-subagents.md) when that evaluation is available and authorized.

Read the test-driven-development workflow when implementing executable helpers. For documentation, do not confuse source-pattern tests with demonstrated agent compliance. A baseline that already passes provides no observed failure to fix in that probe; record the actual result rather than manufacture a red/green story. A documented contradiction or missing reference can justify a change with an appropriately limited claim.

Use independent forward evaluation for sufficiently complex or consequential revisions when authorized. Give the executor the task and raw artifacts, not the desired answer. Repeated samples or a no-guidance control can support attribution; choose effort proportional to the claim and state what the experiment did not measure.

For reference facts, verify the source and freshness before adding a current version or historical assertion. Preserve uncertainty explicitly. An evaluation answer mentioning a command does not prove that command ran.

## Check and promote

Check frontmatter, placement, links, references, examples and canonical language. Run changed helpers and the required repository gates. Verify generated output against the sources and record what the actual installer verifies when installation is within scope.

Bind review to the delivered revision and inspected cases. Preserve valid evidence from unaffected changes and rerun invalidated checks. An unavailable runner or unsupported capability remains explicit rather than passing silently.

Present the reviewable result requested by the user. Opening a PR, merging it, installing guidance and publishing a product are different actions with different authorization scopes. Do not install globally or publish as an implied side effect of writing a skill.

## Useful resources

- [Official authoring background](anthropic-best-practices.md): consult for platform-specific authoring considerations; canonical repository rules remain authoritative.
- [Pressure-test techniques](testing-skills-with-subagents.md): consult for realistic conflicting demands and actual response analysis.
- [Persuasion principles](persuasion-principles.md): consult only for a discipline rule whose failure calls for that technique; do not add persuasion machinery to ordinary reference guidance.
- [Graph conventions](graphviz-conventions.dot): use a diagram for a decision or loop that is clearer visually, not as mandatory decoration.

## Completion criteria

The package has a precise trigger, one owner per concept, discoverable resources, no unresolved local links, no fabricated evidence and a validation record proportional to its intended use. A batch review accounts for every requested package, including justified no-change decisions; it does not grant automatic approval to uninspected packages.
