---
name: ai-agentic-security
description: Acts as an Agentic AI Security specialist covering the lethal trifecta (untrusted data, tool access, exfiltration channel), goal hijacking, tool and function-call validation independent of the model, MCP and A2A protocol risks, memory poisoning, multi-agent trust and the OWASP Top 10 for Agentic Applications 2026.
metadata:
  type: defensive
  phase: weaponize
---

# Agentic AI Security

This skill guides the AI to secure systems where a model can take actions, not just generate text. Agentic risk is qualitatively different from prompt injection in a chat: the model now has tools.

---

## ☠️ 1. The Lethal Trifecta

An agent is exploitable when it combines **all three** of: access to untrusted data, the ability to take action (tools), and a channel to exfiltrate. Remove any one leg and the attack collapses. This is the primary design heuristic for agentic security.

---

## 🎯 2. Agent-Specific Threats

| Threat | Description |
| :--- | :--- |
| **Goal hijacking** | Injected content redirects the agent's objective |
| **Unauthorized tool invocation** | The agent calls a tool it should not, or with the wrong arguments |
| **Tool poisoning** | A tool's description or implementation is malicious (name, instructions, runtime) |
| **Memory/context poisoning** | Persistent memory or RAG context is poisoned to influence later turns |
| **Excessive agency** | The agent has more autonomy or privilege than the task requires |
| **Multi-agent propagation** | A compromised agent instructs a peer that trusts it |
| **Agent escape** | The agent reaches the network, filesystem or another sandbox |
| **Rug pull / reputation inflation** | A tool or model changes behavior after being trusted |

Map these to **MITRE ATLAS** (for example, AI Agent Tool Poisoning) and to the **OWASP Top 10 for Agentic Applications 2026**.

---

## 🛡️ 3. Controls

1. **Authorize tool calls outside the model**: the runtime validates every tool call against policy; the model's intent is never sufficient authorization.
2. **Least privilege per tool**: each tool gets a scoped identity and the minimum permission; no shared "god" tool.
3. **Human-in-the-loop for irreversible actions**: writes, deletes, payments and external sends require confirmation or a policy gate.
4. **Sandbox the agent**: confine filesystem, network and process access; block egress except to allowlisted destinations.
5. **Separate trust levels between agents**: a peer's message is untrusted input, not an instruction.
6. **Bound the loop**: step limits, timeouts, budget caps and recursion guards (also the OWASP LLM10 Unbounded Consumption control).
7. **Validate tool definitions**: treat a tool's schema and description as code under review.

---

## 🔌 4. Protocol Surfaces (MCP, A2A)

- **MCP servers** expose tools, resources and prompts; a malicious or compromised server can return poisoned content or reachable SSRF/SQLi/XSS endpoints. Treat every MCP server as untrusted until reviewed.
- **Agent-to-agent (A2A)** communication needs authentication and authorization of the peer, plus schema validation of the messages.
- Apply the four-layer test model: reasoning, tool execution, infrastructure, and inter-agent communication.

---

## 🔗 5. Integration with Other Skills

- For LLM/model-level risks, see the [ai-llm-slm-security](../ai-llm-slm-security/SKILL.md) skill.
- For the content trust boundary in research workflows, see the [untrusted-content-security](../../operations/untrusted-content-security/SKILL.md) skill.
- For AI governance and assurance, see the [ai-governance-assurance](../ai-governance-assurance/SKILL.md) skill.
- For adversarial ML in predictive models, see the [ai-adversarial-ml-security](../ai-adversarial-ml-security/SKILL.md) skill.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **OWASP Top 10 for Agentic Applications 2026** (verified) — genai.owasp.org
