---
name: "ai-application-engineering"
description: "Provides expert patterns for building applications on foundation models based on AI Engineering (Chip Huyen), Building Large Language Models, Hands-On Large Language Models, Mastering LLM Applications with LangChain and Hugging Face, and RAG Systems. Covers evaluation methodology (perplexity, AI-as-a-judge), prompting and sampling, RAG architecture with hybrid retrieval and reranking, agent patterns, fine-tuning and inference optimization (quantization, LoRA/QLoRA, speculative decoding), and the LangChain/Hugging Face stack with deployment."
---

# AI Skill: AI Application Engineering (Foundation Models)

This skill guides the AI to engineer applications around foundation models — evaluate before optimizing, ground before generating, and control cost/latency deliberately. It builds on *AI Engineering* (Huyen), *Building LLMs* (Sabe), *Hands-On Large Language Models* (Alammar & Grootendorst), *Mastering LLM Applications with LangChain and Hugging Face*, and *RAG Systems* (Ray).

Resolve current model and library versions (Hugging Face, LangChain, Transformers, vLLM) from their publishers before pinning them.

---

## 🧭 When to Activate

- Designing an LLM feature: evaluation, prompting, RAG, fine-tuning, agents, serving.
- Diagnosing hallucinations, latency, or cost.
- Choosing between prompting, RAG, and fine-tuning.
- Implementing hybrid retrieval, reranking, or query rewriting.
- Deploying and versioning an LLM application.

---

## 📏 Evaluation First

- **Language-model metrics:** entropy, cross entropy (`H(P,Q) ≠ H(Q,P)`), bits-per-character/byte, and **perplexity = exp(cross-entropy)**. Lower is better, but structured data, vocabulary size and context length shift PPL — compare only like with like.
- **Exact/task metrics:** functional correctness; similarity to reference (ROUGE, BERTScore, Levenshtein, cosine); **AI-as-a-judge** (calibrate against human labels, set judge temperature 0); comparative/ranking (pairwise, Elo-style).
- **Evaluate every component and end-to-end.** A judge is a guardrail, not ground truth.

---

## ✍️ Prompting and Sampling

- In-context learning (zero/few-shot); system vs user prompt (system tends to carry more weight and mitigates prompt attacks). Be explicit, provide context, and **decompose** complex tasks.
- **Chain-of-thought** ("think step by step", one-shot CoT), self-critique, and **version prompts** as tested artifacts.
- **Sampling:** temperature (0 deterministic, ~0.7 creative), top-k, **top-p/nucleus** (0.9–0.95), beam search. Early stopping can truncate closing JSON brackets — use grammar-constrained decoding for structured output.
- Defensive prompting against direct/indirect **prompt injection**, jailbreaking and information extraction; see [ai-llm-slm-security](../../../security/ai/ai-llm-slm-security/SKILL.md).

---

## 🔍 RAG Architecture

Index + retriever + generator. Retrieval families: **term-based/sparse** (BM25, Elasticsearch) and **embedding-based/dense**. Use **hybrid search** with **Reciprocal Rank Fusion**:

```text
Score(D) = Σᵢ 1 / (k + rᵢ(D)),  k ≈ 60
```

- **Chunking:** 512–1,024 tokens with ~20% overlap; multiple vectors per document beats one vector per document; add titles/surrounding context.
- **Rerank** candidates (cross-encoder, e.g. Cohere Rerank) before prompt assembly; **rewrite queries** to resolve ambiguity/identity; consider contextual retrieval.
- **Vector stores:** ANN libraries (HNSW, IVF, PQ) and databases (FAISS, Chroma, Weaviate, Pinecone); see [vector-databases](../../../data/vector-databases/SKILL.md).
- **Query rewriting must refuse rather than hallucinate** when identity cannot be resolved.

---

## 🤖 Agents

Plan → reflect → execute → reflect. **Decouple planning from execution**: validate plans (invalid-action elimination, step caps, AI judge) before spending FLOPs. **Function calling** exposes tools; control flow is sequential/parallel/if/for; **intent classification** (with an `IRRELEVANT` intent) routes tool choice. Keep a human in the loop at plan/validate/execute for risky actions. See [ai-agentic-security](../../../security/ai/ai-agentic-security/SKILL.md) for the security model.

---

## 🎛️ Fine-Tuning and Inference Optimization

- Training memory = weights + activations + gradients + optimizer states (trainable params drive gradients/states).
- **PEFT** (adapters, **LoRA** with rank `r` and `lora_alpha ≈ 2r`) and **QLoRA** (4-bit NF4 + paged optimizers) fine-tune large models on one GPU:
```python
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                bnb_4bit_compute_dtype="float16", bnb_4bit_use_double_quant=True)
peft_config = LoraConfig(r=64, lora_alpha=32, lora_dropout=0.1, task_type="CAUSAL_LM",
                         target_modules=["q_proj","k_proj","v_proj","o_proj"])
```
- Distillation, pruning, **quantization** (PTQ/QAT; weight > activation sensitivity), **speculative decoding**, batching (throughput ↔ latency), and KV-cache reuse.
- Metrics: **TTFT** (prefill, parallelizable, populates KV cache), **TPOT** (decode, sequential), total latency, tokens/s.

---

## 🔧 The LangChain / Hugging Face Stack

```python
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema.output_parser import StrOutputParser
chain = prompt_template | llm | StrOutputParser()   # LCEL pipe composition
chain.invoke({...})
```
- Building blocks: prompt templates, chat models, output parsers, retrievers, chains, memory, agents, tools, callbacks, **LangServe** for REST.
- **RAG flow (Load → Split → Store → Retrieve → Generate):** `DirectoryLoader`, `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`, `HuggingFaceEmbeddings`, `Chroma.from_documents(...)`, `as_retriever(search_type="mmr", search_kwargs={"k": 8})`, `RetrievalQA.from_llm(...)`.
- `HuggingFacePipeline.from_model_id(...)` for local inference; `HuggingFaceEndpoint` for API inference. Deploy with Gradio, Telegram bots, or SageMaker endpoints.

---

## 🏭 Production Architecture (Huyen; Ray)

- Stack layers: application development → model development → infrastructure (serving, data/compute, monitoring).
- Architecture progression: enhance context → guardrails → **model router/gateway** → caches → agent patterns → observability → orchestration → user feedback loops.
- Cache at query, embedding and retrieval layers; parallelize embedding with preprocessing; monitor response time, error rate, retrieval quality and model latency.
- **RAG does not fix bad data — it exposes it.** Data access control → filtering → output control, with audit/traceability.

---

## ⚠️ Pitfalls

- Optimizing before evaluating; no versioned evaluation means no measurable improvement.
- Assuming pure vector search suffices (exact terms blur) — add keyword/metadata filtering.
- Chunk overlap that is too small loses boundary context; too small overall raises index cost.
- Unvalidated agent plans spend compute and take unsafe actions.
- Presenting unverified model output as authoritative (see [explainable-ai](../explainable-ai/SKILL.md) on overreliance).

---

## 🔗 Integration with Other Skills

- For MLOps/LLMOps pipelines and deployment, see [ai-llm-engineering-rag](../ai-llm-engineering-rag/SKILL.md).
- For embeddings and ANN indexes, see [vector-databases](../../../data/vector-databases/SKILL.md).
- For LLM/agent security, see [ai-llm-slm-security](../../../security/ai/ai-llm-slm-security/SKILL.md) and [ai-agentic-security](../../../security/ai/ai-agentic-security/SKILL.md).
- For distributed training/inference at scale, see [distributed-ml-scaling](../../../data/distributed-ml-scaling/SKILL.md).
