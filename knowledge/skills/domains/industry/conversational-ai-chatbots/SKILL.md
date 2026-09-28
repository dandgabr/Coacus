---
name: "conversational-ai-chatbots"
description: "Provides conversational AI engineering based on production chatbot practice, covering bot archetypes (FAQ, routing, process-oriented), the measure-identify-implement-deploy improvement cycle, intent and generative understanding metrics, RAG evaluation in three layers, guardrail ladders, generative data augmentation for intents, complexity and context design patterns, handoff summarization and business-goal metric mapping. Use when building, measuring or continuously improving chatbots, virtual assistants or LLM-backed conversational agents."
---

# AI Skill: Conversational AI and Chatbots

This skill guides the AI to build and continuously improve conversational agents as measured, iterated products rather than one-shot deployments. It synthesizes production chatbot lifecycle practice from Freed's conversational AI literature. Models named in any source decay; the lifecycle principles endure.

---

## 🧭 When to Activate

- Designing a new chatbot, virtual assistant or LLM-backed support agent.
- Measuring or improving an existing conversational agent's performance.
- Choosing between intents, search and retrieval-augmented generation for a request class.
- Designing guardrails, evaluation sets or human handoff flows.
- Augmenting training data with generated utterances.

---

## 🔁 The Improvement Cycle

Continuous improvement is the core pattern: **MEASURE** performance against explicit outcome dimensions → **IDENTIFY** the lowest performers with an effort/benefit estimate → **IMPLEMENT** the prioritized backlog → **DEPLOY** the release and tell users what changed. Repeat forever; a chatbot is never finished.

---

## 🧩 Bot Archetypes and GenAI Levers

- **FAQ bot:** static question/answer pairs or dynamically generated answers.
- **Routing agent:** classifies and directs to the right specialist or flow.
- **Process-oriented bot:** drives multi-step task flows backed by real APIs.
- Generative AI addresses three chronic pain points: weak intent understanding (better training data or RAG replacing recognition), user-facing complexity (simpler prose, flow testing) and immediate opt-outs (more engaging dialogue).

---

## 📏 Measurement

- **Outcome taxonomy beyond containment:** automated resolution, intentional transfer, abandonment, failure to understand, user escalation, contained-by-bot; map each to business metrics (conversion, average handle time, first-contact resolution, deflected contacts, cost).
- **Effectiveness** (does each interaction achieve the goal) and **coverage** (how much of the demand space is handled) are the two master axes; re-baseline both whenever business goals change.
- **Traditional NLU:** per-intent precision, recall, F1; test with k-fold cross-validation before launch, then representative blind sets annotated from production logs as the gold standard and regression asset.
- **Generative understanding:** define "good" up front — format and persona match, appropriate length, hallucination-free, free of hateful/profane content, prompt-injection resilient, correct and flow-progressing; manual review of log samples becomes the golden set; thumbs feedback captures understanding at scale.

---

## 🧭 Intents vs Search vs RAG

- **Intents** for closed, high-volume, process-linked requests.
- **Search** for lookup over documents.
- **RAG** for generated answers grounded in a curated corpus — with honest costs: repository preparation, ingestion pipeline effort, index freshness, latency and explicit fallback rules (when to search, when to answer, when to escalate).

---

## 📊 RAG Evaluation in Three Layers

Evaluate each layer independently, then end-to-end:

1. **Indexing:** indexing speed, storage, scalability; vector-index recall rate alongside queries-per-second and latency (approximate search trades accuracy; compare with standard ANN benchmarks).
2. **Retrieval:** precision and recall of retrieved context; tuning levers are search parameters, embedding model choice, metadata filtering and reranking.
3. **Generation:** correctness, context fit and groundedness — the answer is right, right for the user's situation, and supported by the retrieved documents, not fabricated.

---

## 🛡️ Guardrail Ladder

Defense in depth, from safest to most surgical:

1. Model and training-data selection (read model cards; exclude biased data slices).
2. Input prefiltering (keyword/classifier screening; cap input length as a cheap defense).
3. Contextual instructions (inject date, persona and session context to reduce stale-data hallucination).
4. Output postfiltering (profanity checks; grounding checks via similarity between answer and retrieved sources).
5. Human-in-the-loop as the default for high-stakes actions.

Treat prompt injection as a standing threat; parameterized templates and output monitoring are part of the ladder.

---

## 🧪 Generative Data Augmentation

- Generate contextual synonyms per intent — plain "synonyms of X" prompts fail; ground the role and scenario first.
- Expand with verb and verb-phrase synonyms, grammatical variations and templated combinations; check every generated batch for cross-intent confusion.
- Use the data-variety matrix: small/low-variation sets for smoke tests, large/high-variation for training; greedy decoding for reproducibility.

---

## 🧠 Complexity and Context Patterns

- Complexity harms users and metrics: untangle dialogue flows, use known user data to skip steps, align with the user's mental model, accept flexible response phrasing, and back self-service flows with real APIs.
- Harness known context (identity, history, authenticated state) to remove repeated questions; context is friction removal.
- Reduce opt-outs as a first-class workstream: engaging prose, faster time-to-value, clear escalation paths.

---

## 🤝 Human Handoff

- Agents cannot read multi-page transcripts. Summaries combine structured metadata (IDs collected, session counts, sentiment) with a short free-text summary; filter collected data to what the human actually needs.
- Route with an explicit handoff design, never as an error path of last resort.

---

## ⚠️ Pitfalls

- Treating containment as the only metric; it can be gamed by trapping users.
- Launching intents without an orphan-utterance stopping rule — intent sprawl follows.
- Shipping RAG without per-layer evaluation; a weak retrieval layer masquerades as a model problem.
- Trusting generated augmentation without confusion checks.
- Wholesale replacement of classic conversational AI by generative components; augmentation beats replacement.

---

## 🔗 Integration with Other Skills

- For the RAG mechanics behind grounded answers, see [ai-llm-engineering-rag](../ai-llm-engineering-rag/SKILL.md).
- For model- and component-level evaluation rigor, see [ai-model-evaluation](../ai-model-evaluation/SKILL.md).
- For guardrail threat modeling, see [ai-agentic-security](../../../security/ai/ai-agentic-security/SKILL.md) and [ai-llm-slm-security](../../../security/ai/ai-llm-slm-security/SKILL.md).
- For the product framing of assistant features, see [ai-application-engineering](../ai-application-engineering/SKILL.md).
