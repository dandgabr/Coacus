---
name: binary-symbolic-execution-fuzzing
description: Acts as a Vulnerability Research specialist covering symbolic and concolic execution (angr, KLEE), coverage-guided fuzzing (AFL++, libFuzzer), the Driller pattern that combines fuzzing with selective symbolic execution, harness design and crash triage.
metadata:
  type: offensive
  phase: exploit
---

# Binary Symbolic Execution and Fuzzing

This skill guides the AI to discover vulnerabilities in binaries and code using automated, coverage-driven techniques. It is offensive vulnerability research, distinct from quality-assurance mutation testing.

---

## 🔍 1. Fuzzing

- **Coverage-guided fuzzing** (AFL++, libFuzzer) mutates inputs and keeps those that reach new code paths.
- A good **harness** is most of the work: it feeds the fuzzer, constrains inputs to the valid format, and detects the target failure condition (crash, sanitizer trip, assertion).
- Use sanitizers (ASan, UBSan, MSan) to turn silent corruption into a detectable failure.
- Seed with realistic and boundary-case inputs; the corpus quality bounds the results.
- Run continuously with a corpus that persists across builds.

---

## 🧠 2. Symbolic and Concolic Execution

- **Symbolic execution** (angr, KLEE) explores paths by reasoning about constraints rather than concrete inputs; it can reach paths fuzzing struggles with (checksums, magic values).
- Build a **control-flow graph**, then explore toward a target state or a sink; solve the collected constraints to get a concrete input.
- The classic failure mode is **path explosion**; constrain the search and bound the depth.

---

## 🤝 3. The Driller Pattern

Combine the two: fuzz to find the shallow paths cheaply, and when the fuzzer stalls at a hard check, invoke selective symbolic execution to discover the input that passes it, then return the new input to the fuzzer corpus. This is the standard approach for defeating magic-value and checksum gates.

---

## 🧪 4. Crash Triage

1. **Deduplicate** crashes by the faulting instruction and the stack.
2. **Determine exploitability** (control of a pointer, control of a length, memory-safety vs denial-of-service).
3. **Minimize** the reproducer.
4. **Map** to a CWE and a severity, and to ATT&CK where relevant.
5. **Report** with a reproducible harness and the root cause.

---

## 🔗 5. Integration with Other Skills

- For exploit construction from a crash, see the [exploit-development-vulnerability-research](../exploit-development-vulnerability-research/SKILL.md) skill.
- For the analysis tooling context, see the [malware-analysis-multios](../../appsec/malware-analysis-multios/SKILL.md) skill.
- For memory-safety primitives, see the [memory-manipulation](../../platform/memory-manipulation/SKILL.md) skill.
- For QA-focused mutation testing (distinct), see the [mutation-fuzzing-testing](../../../frameworks/mutation-fuzzing-testing/SKILL.md) skill.
