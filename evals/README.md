# Behavioral evaluations

Coacus evaluations describe observable behavior expected from an agent using
the framework. They complement unit tests; they do not certify a model, harness
or every possible interaction.

## Evaluation modes

The static validator is deterministic, requires no LLM or network, and runs in
CI. It checks each scenario's structure, target harness, checks, rubric, secret
patterns and absolute paths:

```bash
python3 scripts/coacus_eval.py validate
```

Live runs are opt-in and execute a real harness CLI. They require the selected
harness and any credentials it needs, so they run locally rather than in CI:

```bash
python3 scripts/coacus_eval.py run
python3 scripts/coacus_eval.py run --scenario artifact-lifecycle
python3 scripts/coacus_eval.py run --harness codex
python3 scripts/coacus_eval.py run --judge-cmd "python3 path/to/judge.py"
python3 scripts/coacus_eval.py run --judge-agent
```

Each harness declares its live command in `harnesses/<h>/harness.json`. Use
`--harness` to run a scenario against another locally available runner. A
missing CLI, timeout or non-zero exit is reported as an unavailable or failed
run, not as a passing evaluation. Without a judge, rubric checks remain
advisory; deterministic scenario checks still run. Transcript output is
redacted by default. Set `COACUS_EVAL_VERBOSE=1` only when local debugging
requires an excerpt, and inspect it before sharing because it may contain
sensitive context.

The opt-in `python3 evals/command_code_mod_probe.py` checks Command Code's
tool-hook failure behavior against a fake loopback provider and a synthetic
file. Run it in an isolated environment with the CLI already installed; it
uses a temporary home and does not require credentials or launch subagents.
It tests `read_file`, not subagent interception or worker lifetime.

## Scenario format

Scenarios live at `evals/scenarios/<id>/scenario.json`. Each JSON object declares
an `id`, `title`, target `harness`, `prompt`, non-empty `checks`, a non-empty
`rubric` and an `acceptance` statement. Checks use `contains`, `not_contains` or
`regex`; the static validator compiles regular expressions and rejects secret
patterns and machine-specific absolute paths. Keep prompts, checks and rubrics
focused on observable outcomes, and avoid credentials or private data.

The `evals` GitHub Actions workflow runs the static validator on a schedule and
on manual dispatch. The blocking CI workflow also runs the static gate; it never
launches a live agent. See [`../docs/standards/testing.md`](../docs/standards/testing.md)
for how evaluations fit with the deterministic test suite.
