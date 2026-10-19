# Behavioral Validation for Skill Changes

Use when a skill change is intended to alter an agent's decisions, especially for a complex or high-impact workflow. Structural validation and behavioral evaluation answer different questions.

## Define a realistic task

Provide the user request, the relevant skill and minimum raw artifacts needed to do the work. Keep expected answers, suspected defects, proposed fixes and scoring criteria away from the executing agent unless the task itself requires them. Give explicit side-effect boundaries and an isolated output location.

Choose cases for the actual failure class: application and variation for a technique; recognition and counterexamples for a pattern; retrieval and accurate use for a reference; realistic conflicting pressures for a discipline rule. Include a case where the guidance should preserve an already-correct result rather than add work.

## Compare before and after honestly

Freeze the old content and record its revision. Use a fresh execution context for the candidate and the same raw inputs. Capture actual choices and artifacts, not only whether the answer mentions a keyword. Read the outcomes against a fixed rubric.

A passing baseline is a passing baseline. Do not manufacture a failure, redefine the rubric after seeing the result or claim demonstrated improvement from unchanged passes. The change may still resolve a documented contradiction or reference gap; report that rationale and the limit of the experiment. Use a no-guidance control or repeated samples when needed to attribute the effect or estimate variability. A single sample does not establish reliability.

## Distinguish evidence depth

A reasoning answer can establish a diagnosis or proposed next action. It cannot establish that a browser rendered a repair, a mutation was killed, an installer changed the intended destination or a deployment serves fresh bytes. Execute those probes when the claim requires them and the environment permits them. Otherwise record their status explicitly.

For visual cases, use the relevant fixture and [rendered interface oracles](../../../../knowledge/skills/frameworks/framework-testing/references/rendered-ui-oracles.md). Include output geometry, paint, interaction or revision evidence appropriate to the claim. Source matching and schema validity are useful integrity checks, not substitutes for these outcomes.

## Preserve the evaluation boundary

Keep the evaluator independent from the author where useful. Do not give it the desired verdict. State the inspected revision, directly examined cases, unavailable capabilities and unresolved findings. Assess serious findings and rerun the evidence invalidated by a fix; do not reclassify an unsupported check as passed to finish the workflow.

## Capture learning without overgeneralizing

Record observation, source authority, limitation, destination, counterexample and evaluation. Prefer improving an existing owner skill over creating another overlapping one. A project-specific count, theme, provider or local tool does not become a universal requirement. Keep the source observation separate from the proposed instruction and the instruction's measured outcome.

## Match instruction form to the observed gap

Use a positive procedure for a missing technique, a clear structural slot for omitted required content, or an observable completion predicate when an agent cannot tell done from incomplete. Sharpen the reference trigger before inlining a whole guide. Preserve a valid counterexample so a stronger instruction does not create unrelated work. For wording experiments, hold the realistic surrounding context fixed, use fresh samples and manually inspect flagged responses; quoted counterexamples and template echoes can produce false keyword matches.
