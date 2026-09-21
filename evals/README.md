# Behavior evals

`evals/` holds **LLM behavior** evaluations (testing). They are separate from
`tests/` (deterministic infrastructure): a behavior eval asks whether an agent
actually *follows* the framework, not whether the code is correct.

## Two tiers

| Tier | What it does | Where it runs |
|---|---|---|
| **Static** | Validates every `evals/scenarios/<id>/scenario.json` (schema, harness exists, checks well-formed, no secrets/paths) | Blocking `ci` job + scheduled `evals.yml` + `python3 scripts/coacus_eval.py validate` |
| **Live** | Drives a real agent CLI with the scenario prompt, captures the transcript, applies deterministic checks, optionally judges against the rubric | **Local/manual only** — needs an installed harness CLI and credentials, which CI does not have |

## Scenario format

```json
{
  "id": "bootstrap-activation",
  "title": "SessionStart bootstrap activates the entry skill",
  "harness": "opencode",
  "prompt": "…",
  "checks": [
    { "kind": "contains", "value": "This is just a small change" },
    { "kind": "not_contains", "value": "none" }
  ],
  "rubric": ["…"],
  "acceptance": "…"
}
```

`checks` are deterministic (`contains`, `not_contains`, `regex`); `rubric` is the
judge input; `acceptance` is the human-readable criterion.

## Running live

```bash
# one scenario
python3 scripts/coacus_eval.py run --scenario bootstrap-activation

# all scenarios, judged by a pluggable command (reads {scenario, transcript} JSON on stdin)
python3 scripts/coacus_eval.py run --judge-cmd "my-judge"

# judged by an orchestrated subagent through the same harness (multi-agent pattern)
python3 scripts/coacus_eval.py run --judge-agent

# override the scenario's harness — exercise any locally installed live CLI
python3 scripts/coacus_eval.py run --scenario skill-first-discipline --harness codex
```

The live runner drives a real agent CLI and never runs in CI. Each harness
declares its non-interactive invocation in `harnesses/<h>/harness.json`
(`live_cli`): `opencode run`, `codex exec`, `agy --print`. A harness without one
is reported as `NO_RUNNER` (currently `claude-code`, `cursor` and
`command-code`, whose binaries/live paths were not available or do not fire the
`SessionStart` bootstrap in print mode). `--harness` overrides the scenario's target, so one
scenario runs against every installed CLI.

## Seeded scenarios (F5)

- `bootstrap-activation` — the SessionStart bootstrap injects the entry skill.
- `skill-first-discipline` — the single-scan + skill-first rules are known.
- `artifact-lifecycle` — generated output is never hand-edited.
- `governance-cap-and-toon` — the cap (5, orchestrator included) and `@STATUS`.
- `evidence-before-claims` — run the verification command before claiming done.
- `brainstorm-before-build` — explore intent/design before writing code.

## Judge

Two judge modes, both opt-in:
- `--judge-cmd` runs any command, passing `{"scenario", "transcript"}` on stdin
  (plug an LLM or a script later).
- `--judge-agent` routes the rubric through the harness as an orchestrated
  subagent (the multi-agent-orchestrator pattern).

With neither flag the runner reports deterministic checks only — no LLM needed.
