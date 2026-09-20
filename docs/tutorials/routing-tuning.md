# Tutorial — tune the routing lexicon

**Time:** about 15 minutes. **Prereqs:** a checkout and a passing `validate`. Run
every command from the repository root.

The router's vocabulary lives in one curated file. When a prompt routes to the
wrong agent (or to none), you fix it here — as data, not code. This tutorial tunes
the lexicon and proves the change with the gate.

## 1. Understand the two inputs

The routing index `.agents/routing.json` is **generated**. It merges:

- each agent's canonical facts (name, category, description, skills) from its
  `agent.source.md` — never edited for routing; and
- the curated **triggers** from
  [`knowledge/routing/lexicon.json`](../../knowledge/routing/lexicon.json) — the
  only file you edit to change matching.

The lexicon is bilingual on purpose: prompts are PT-BR or EN, but the canonical
descriptions are English only ([english-only](../standards/english-only.md)). The
triggers bridge the two.

## 2. Reproduce a bad route

Start from the prompt that routed wrong:

```bash
python3 scripts/coacus_route.py "revisar o contrato de API" --top 3
```

Note which agent *should* have won and which terms it matched (`matched-terms`).
If the right agent is absent, its vocabulary lacks a term the prompt used.

## 3. Add a trigger

Edit `knowledge/routing/lexicon.json` and add the missing term to the agent's
list. Keep terms **lowercase** and, for a two-word concept, add it as one phrase
(multi-word triggers match whole):

```json
{
  "agents": {
    "software-architect": ["arquitetura", "contrato de api", "api contract", "especificação"]
  }
}
```

Rules the validator enforces (`python3 scripts/coacus.py validate`):

- every agent has a list (**no agent without triggers**);
- no triggers for a name that is not an agent (a rename cannot silently orphan a
  vocabulary);
- no empty terms and no uppercase terms.

A multi-word trigger is matched as a phrase: adding `contrato de api` makes that
exact phrase score, while the bare word `contrato` alone does not.

## 4. Regenerate and re-check

The index is generated from the lexicon, so regenerate before routing again:

```bash
python3 scripts/coacus.py generate        # rebuild .agents/routing.json
python3 scripts/coacus.py check           # must report no drift
```

Then re-run the prompt from step 2:

```bash
python3 scripts/coacus_route.py "revisar o contrato de API" --top 3
```

The intended agent should now appear, with your term in `matched-terms`.

## 5. Run the gates

Two checks make sure your edit is coherent and did not regress routing:

```bash
python3 scripts/coacus.py validate                 # lexicon + index contracts
python3 -m unittest tests.test_router -v           # scorer
python3 -m unittest tests.test_router_calibration  # observed quality
```

If you changed matching behaviour, add or update a case in
`tests/test_router_calibration.py` so the improvement is locked in.

## 6. Know the limits

The lexicon is precise but literal. Paraphrase beyond the vocabulary
("desaceleração das queries" vs "consultas lentas") is the job of the optional
semantic reranker (`--rerank`), not of more triggers. Add a trigger when you can
name the term a user would actually type; reach for the reranker when the gap is
meaning, not vocabulary.

## What you learned

- Edit only `knowledge/routing/lexicon.json`; the index is generated.
- Lowercase, whole-phrase multi-word triggers; the validator enforces coverage.
- `generate` → `check` → `validate` → tests proves the change.

Next: read [routing](../standards/routing.md) for the weights and the modes.
