# Behavioral Validation for Skill Changes

Use when a skill change is intended to alter an agent's decisions, especially for a complex or high-impact workflow. Structural validation and behavioral evaluation answer different questions.

## Define a realistic task

Provide the user request, the relevant skill and minimum raw artifacts needed to do the work. Keep expected answers, suspected defects, proposed fixes and scoring criteria away from the executing agent unless the task itself requires them. Give explicit side-effect boundaries and an isolated output location.

Choose cases for the actual failure class: application and variation for a technique; recognition and counterexamples for a pattern; retrieval and accurate use for a reference; realistic conflicting pressures for a discipline rule. Include a case where the guidance should preserve an already-correct result rather than add work.

## Compare before and after honestly

Freeze the old content and record its revision. Use a fresh execution context for the candidate and the same raw inputs. Capture actual choices and artifacts, not only whether the answer mentions a keyword. Read the outcomes against a fixed rubric.

A passing baseline is a passing baseline. Do not manufacture a failure, redefine the rubric after seeing the result or claim demonstrated improvement from unchanged passes. The change may still resolve a documented contradiction or reference gap; report that rationale and the limit of the experiment. Use a no-guidance control or repeated samples when needed to attribute the effect or estimate variability. A single sample does not establish reliability.

## Test skill activation

For a skill whose discovery description or routing behavior changes, prepare a
small activation set with positive requests that should invoke it and near-miss
requests that share vocabulary but should not. Include realistic wording
variation, and include each supported user language when language should not
change routing. Keep the expected skill and rationale in the evaluator rubric,
not in the prompt sent to the executing agent. Label the positive activation
and near-miss cases explicitly. Record the prompt set revision
and compare the baseline, candidate, and a no-skill control when attribution is
needed.

An activation query is a test fixture, not proof of runtime activation or that
a runtime loaded the skill. Claim observed activation only when the harness exposes verifiable
activation telemetry or an equivalent artifact. When the harness does not
expose that evidence, report the query-set coverage and the limitation; do not
infer activation from an answer that merely repeats skill terminology.

## Compare behavioral benchmarks reproducibly

Use the same task set, raw inputs, rubric, model and harness settings for the
no-skill control, old guidance and candidate guidance. Record revisions and
environment details, run repeated samples when results are stochastic, and
report task-level outcomes as well as aggregate values. At minimum compare
correctness, safety-boundary adherence and task completion; include latency,
token use or cost when those values are available. Mark unavailable measures
as unavailable, and do not claim a benchmark improvement from a single sample
or from a metric that the run did not record.

For code simplification tasks, also record lines changed or an appropriate
complexity measure as context. Fewer lines alone do not establish an
improvement; preserve behavior and require the same correctness, safety and
verification criteria as the baseline.

## Distinguish evidence depth

A reasoning answer can establish a diagnosis or proposed next action. It cannot establish that a browser rendered a repair, a mutation was killed, an installer changed the intended destination or a deployment serves fresh bytes. Execute those probes when the claim requires them and the environment permits them. Otherwise record their status explicitly.

For visual cases, use the relevant fixture and [rendered interface oracles](../../../../knowledge/skills/frameworks/framework-testing/references/rendered-ui-oracles.md). Include output geometry, paint, interaction or revision evidence appropriate to the claim. Source matching and schema validity are useful integrity checks, not substitutes for these outcomes.

## Preserve the evaluation boundary

Keep the evaluator independent from the author where useful. Do not give it the desired verdict. State the inspected revision, directly examined cases, unavailable capabilities and unresolved findings. Assess serious findings and rerun the evidence invalidated by a fix; do not reclassify an unsupported check as passed to finish the workflow.

## Capture learning without overgeneralizing

Record observation, source authority, limitation, destination, counterexample and evaluation. Prefer improving an existing owner skill over creating another overlapping one. A project-specific count, theme, provider or local tool does not become a universal requirement. Keep the source observation separate from the proposed instruction and the instruction's measured outcome.

## Match instruction form to the observed gap

Use a positive procedure for a missing technique, a clear structural slot for omitted required content, or an observable completion predicate when an agent cannot tell done from incomplete. Sharpen the reference trigger before inlining a whole guide. Preserve a valid counterexample so a stronger instruction does not create unrelated work. For wording experiments, hold the realistic surrounding context fixed, use fresh samples and manually inspect flagged responses; quoted counterexamples and template echoes can produce false keyword matches.
