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
harness and any credentials it needs, so they run locally rather than in CI.
Live process execution is supported only on POSIX; on Windows it fails closed
with `UNSUPPORTED_PLATFORM`. Static validation remains available on Windows.
Examples of live runs:

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

All scenarios fail closed with `--judge-agent`: the harness
CLI has not been verified to isolate tools from untrusted transcripts. Use an
explicit `--judge-cmd` only when the operator trusts that command to handle
untrusted input safely; Coacus does not sandbox it. If both options are given,
`--judge-agent` takes precedence and all scenarios fail closed.

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

### Judge command contracts

`--judge-agent` is unsupported for all scenarios because tool-free isolation is
not verified. Its result fails both legacy and required scenarios. When both options are supplied, it takes precedence. Judge commands
are trusted by the operator and are not sandboxed; instructions and base64
encoding are not security boundaries.

The command receives JSON on stdin. Legacy input is `{"scenario": {...},
"transcript": "..."}`. An explicit `VERDICT: PASS` or `VERDICT: FAIL` in
stdout, or stderr if stdout is empty, gates the result only when it is exactly
one standalone verdict line. Malformed, duplicate or conflicting verdicts,
command failure or an unavailable judge fail the scenario. Without a configured
judge, legacy scenarios use deterministic checks only; their rubrics are not judged.

The runner skips the judge when the harness status is not OK or any deterministic
check fails. The judge report marks it as skipped and gives the reason.

Required scenarios receive `instructions`, `scenario`, and a `transcript` object
with `trust: "untrusted"`, `encoding: "base64-utf8"`, boolean `truncated`, and
`base64` encoding at most 32768 transcript bytes. Output must be only a JSON
object `{"verdicts": [true, false]}` with exactly one boolean per rubric item,
in order, without extra or duplicate keys. All verdicts must be true to pass.
Truncation, invalid output, command failure or an unavailable judge fails a
required scenario. Commands have a 600-second deadline and a 1 MiB limit per
output stream. Process-group cleanup cannot contain deliberately detached
processes and is not an OS sandbox.
