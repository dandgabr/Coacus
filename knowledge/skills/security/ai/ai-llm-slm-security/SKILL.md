---
name: ai-llm-slm-security
description: "Acts as a Specialist in Security, Governance, Red Teaming, Weight Auditing, and Pentesting of AI Models (LLMs, SLMs, and Predictive Models). Covers mitigation and exploitation of Prompt Injection (direct and indirect), Jailbreaking, data poisoning, model inversion, RAG security, digital weight auditing (safetensors vs pickle exploits with picklescan, trust_remote_code inspection), bias/toxicity evaluation (StereoSet, AdvBench), and full compliance with the OWASP Top 10 for LLM and OWASP Machine Learning Security."
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

## 🛡️ 2. Threat Matrix: OWASP Top 10 for LLM

| ID | Vulnerability | Technical Description | Test Vector & Mitigation |
| :--- | :--- | :--- | :--- |
| **LLM01** | **Prompt Injection** | Direct or indirect manipulation of the model's instruction flow. | Strict delimiters (`### User Input`), LLM guardrails (NeMo, Guardrails AI), and intent classification. |
| **LLM02** | **Insecure Output Handling** | Execution of model output without validation by the host system (XSS, SQLi, RCE). | Strict JSON schema validation before dispatching tool calls. |
| **LLM03** | **Training Data Poisoning** | Insertion of malicious data during fine-tuning or pre-training. | Cryptographic dataset signing, statistical filtering, and data deduplication. |
| **LLM04** | **Model Denial of Service** | Context exhaustion or infinite recursion of tool calls and RAG chains. | Request rate limiting, `max_tokens` capping, and strict timeouts. |
| **LLM05** | **Supply Chain Vulnerabilities** | Adulterated checkpoints, vulnerable plugins, or malicious dependencies. | SBOM generation, version pinning, and weight scanning with `safetensors`. |
| **LLM06** | **Sensitive Information Disclosure** | Leakage of secrets, PII, or API keys memorized in training or retrieved through RAG. | De-identification with Presidio, log scrubbing, and RBAC access control on the vector database. |
| **LLM07** | **Insecure Plugin Design** | Tools with excessive privileges and no impact validation. | Least privilege on tool APIs and human-in-the-loop confirmation for write/delete operations. |
| **LLM08** | **Excessive Agency** | Disproportionate autonomy granted to the model without supervision. | Scope limits, idempotency, and multi-step approval for critical actions. |

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
