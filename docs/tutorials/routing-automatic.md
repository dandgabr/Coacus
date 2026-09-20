# Tutorial — choose agents automatically (Mode A)

**Time:** about 10 minutes. **Prereqs:** a checkout, `python3`, and
`.agents/routing.json` present (`python3 scripts/coacus.py generate` if it is
missing). Run every command from the repository root.

Mode A is the automated path: you give a prompt, and the router **proposes** the
best agents from the generated index. It is deterministic, offline and lexical —
no model call. It proposes; it never spawns.

## 1. Route a prompt

```bash
python3 scripts/coacus_route.py "faça um pentest no app android" --top 3
```

```
27.0	mobile-security-specialist	cybersecurity	android,app,mobile,pentest
6.0	pentester-agent	cybersecurity	pentest
5.0	fullstack-developer	software-engineering	app
```

One row per candidate: `score<TAB>name<TAB>category<TAB>matched-terms`. Higher
score is a better fit; `matched-terms` shows **why** the agent surfaced, which is
also how you debug a bad ranking.

The scorer weighs curated triggers most, then the agent name, then the
description and skill slugs. See
[routing](../standards/routing.md) for the weights.

## 2. Read the ranking

- The top row is the primary recommendation; the rest are alternates.
- A high score with several matched terms is a confident match.
- A row matched only on a generic word (for example `app`) is weak — expect noise
  below the first or second row on short prompts.

## 3. Constrain the result

**By count** — limit how many candidates you want:

```bash
python3 scripts/coacus_route.py "reduzir a latência das consultas no postgres" --top 2
```

**By floor** — raise the minimum score so weak matches disappear:

```bash
python3 scripts/coacus_route.py "otimizar consultas" --min-score 10
```

```
no agent above the score threshold
```

(`--min-score` prints the message and exits non-zero when nothing clears the
floor — that is a valid "no confident match" signal, not an error.)

## 4. Never over-subscribe concurrency

`--max-slots` caps the proposal at the governor's **free slots**, so routing can
never suggest more parallel agents than the concurrency cap allows
([orchestration-governance](../standards/orchestration-governance.md)):

```bash
python3 scripts/coacus_route.py "segurança de rede" --max-slots
```

Check the budget directly if you want to see the number:

```bash
python3 scripts/coacus_governor.py status   # the slots_free field
```

## 5. Add a semantic reranker (optional)

The lexical scorer is strong on shared vocabulary and weaker on distant
paraphrase. Plug in a reranker behind the same interface with `--rerank`: it
reads JSON on stdin and prints agent names, one per line, in the order you want.

```bash
cat > /tmp/rerank.py <<'EOF'
import json, sys
data = json.load(sys.stdin)
for c in reversed(data["candidates"]):   # stand-in for a semantic reranker
    print(c["name"])
EOF

python3 scripts/coacus_route.py "ci cd github actions pipeline" --top 4 \
  --rerank "python3 /tmp/rerank.py"
```

The reranker **fails open**: if the command is missing or exits non-zero, the
lexical order is returned unchanged, so routing never breaks because the optional
piece is absent.

## 6. Make it automatic in the session (opt-in)

So you do not call the router by hand, install the OpenCode hook. It runs the
router on each user message and appends the candidates to the prompt:

```bash
COACUS_ROUTER_HOOK=1 python3 scripts/coacus_install.py opencode
```

The opt-in is recorded in the install manifest; `--verify` replays it, so a later
plain `--verify` does not report the hook as unexpected. Without
`COACUS_ROUTER_HOOK=1`, the hook is **not** installed — routing is never a hidden
dependency.

## What you learned

- Route a prompt with `--top`; read `matched-terms` to justify or debug a ranking.
- `--min-score` sets a confidence floor; `--max-slots` respects the governor.
- `--rerank` adds an optional semantic layer and fails open.
- The OpenCode hook makes the proposal automatic and is opt-in.

Next: read [routing](../standards/routing.md) for the index and the weights, or
[choose agents manually](routing-manual.md) for the explicit path.
