---
name: ai-llm-slm-security
description: "Acts as a Specialist in Security, Governance, Red Teaming, Weight Auditing, and Pentesting of AI Models (LLMs, SLMs, and Predictive Models). Covers mitigation and exploitation of Prompt Injection (direct and indirect), Jailbreaking, data poisoning, model inversion, RAG security, agentic tool abuse, digital weight auditing (safetensors vs pickle exploits with picklescan, trust_remote_code inspection), bias/toxicity evaluation (StereoSet, AdvBench), and full compliance with the OWASP GenAI LLM Top 10 (2026) and the OWASP Machine Learning Security Top 10."
---

# Security, Red Teaming, and Auditing of AI Models (LLMs, SLMs & Machine Learning)

This skill guides the AI to act as a **Senior Specialist in AI Security, Red Teaming, and Model Auditing**, integrating model infrastructure/code security (weight verification and RCE prevention) with governance and behavioral testing against adversarial attacks (aligned with the **OWASP Top 10 for LLM** and **OWASP ML Security**).

---

## 🔒 1. Digital Security of Model Weights and Code

Before loading any checkpoint or AI model in development or production environments:

### 1.1 Format Verification: `.safetensors` vs `.pkl` / `.bin`

- **Golden Rule**: Always use the **`safetensors`** format (Hugging Face), which stores pure, immutable tensors without the ability to serialize executable code.
- **Pickle Exploit Risk**: `.pkl`, `.pt`, or `.bin` files (Python's traditional Pickle) allow arbitrary code execution (`RCE`) during `torch.load()`.

### 1.2 Static Scanning with `picklescan`

```bash
# Varrer diretório de modelos antes de carregar na memória
picklescan --path /caminho/do/modelo/
```

### 1.3 Inspection of `trust_remote_code=True`

- Thoroughly inspect Python files (`modeling_*.py`, `configuration_*.py`) before allowing `trust_remote_code=True`.
- Block external network calls (`requests.get`, `socket`), subprocess execution (`os.system`, `subprocess.Popen`), and dynamic eval (`eval`, `exec`).

---

## 🛡️ 2. Threat Matrix: OWASP GenAI LLM Top 10 (2026)

| ID | Vulnerability | Technical Description | Test Vector & Mitigation |
| :--- | :--- | :--- | :--- |
| **LLM01** | **Prompt Injection** | Direct or indirect manipulation of the model's instruction flow. | Strict delimiters, LLM guardrails (NeMo, Guardrails AI), intent classification, and treating retrieved content as untrusted data. |
| **LLM02** | **Sensitive Information Disclosure** | Leakage of secrets, PII, or API keys memorized in training or retrieved through RAG. | De-identification with Presidio, log scrubbing, and RBAC on the vector database. |
| **LLM03** | **Supply Chain** | Adulterated checkpoints, vulnerable plugins, or malicious dependencies. | AI BOM (model provenance), version pinning, and weight scanning with `safetensors`. |
| **LLM04** | **Data and Model Poisoning** | Insertion of malicious data during fine-tuning or pre-training. | Cryptographic dataset signing, statistical filtering, and data deduplication. |
| **LLM05** | **Improper Output Handling** | Execution of model output without validation by the host system (XSS, SQLi, RCE). | Strict JSON schema validation before dispatching tool calls or rendering output. |
| **LLM06** | **Excessive Agency** | Disproportionate autonomy granted to the model without supervision. | Scope limits, idempotency, and multi-step/human approval for critical actions. |
| **LLM07** | **System Prompt Leakage** | Extraction of hidden system prompts, guardrails or embedded secrets. | Never store secrets in prompts; assume the system prompt is public; enforce authorization server-side. |
| **LLM08** | **Vector and Embedding Weaknesses** | RAG retrieval poisoning, embedding inversion, and cross-tenant leakage in the vector store. | Per-tenant namespaces, retrieval-scope ACL enforcement, and provenance tagging of ingested documents. |
| **LLM09** | **Misinformation** | Confident, unverified or fabricated output presented as fact. | Grounding with citations, retrieval verification, and explicit uncertainty surfacing. |
| **LLM10** | **Unbounded Consumption** | Context exhaustion, infinite tool recursion, or cost amplification. | Request rate limiting, `max_tokens` capping, budget guards, and strict timeouts. |

---

## 🎯 3. Red Teaming and Alignment Evaluation Methodologies

1. **Indirect Prompt Injection**:
   - Insertion of malicious payloads into PDF documents, scraped web pages, or tickets retrieved by the agent's RAG mechanism.
2. **Jailbreak Resistance**:
   - Evaluation with adversarial benchmarks (**AdvBench**, **DecodingTrust**).
   - Persona tests, hypothetical cognitive *framing*, and multi-language injection.
3. **Toxicity and Bias Auditing**:
   - Measurement of bias and stereotype scores with the **StereoSet** and **Jigsaw Toxic Comments** datasets.
4. **Exaggerated Safety (Over-refusal) Auditing**:
   - Verification of whether the model refuses valid benign requests because of simplistic keyword filters.
