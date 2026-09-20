---
name: detection-engineering-yara-sigma
description: Acts as a specialist in YARA and Sigma rule authoring, covering YARA modules and conditions for file and memory signatures, Sigma specification, log-source mapping, rule conversion to SIEM backends, and the integration of both into malware triage and detection pipelines.
metadata:
  type: defensive
  phase: actions
---

# YARA and Sigma Rule Authoring

This skill guides the AI to write portable, testable detection content in the two formats that anchor open detection engineering.

---

## 🔬 1. YARA

- **Strings**: text, hex and regular expressions with modifiers (`ascii`, `wide`, `nocase`, `fullword`); use `wide` for Windows Unicode strings.
- **Modules**: `pe`, `elf`, `dotnet`, `lnk`, `hash`, `math` and `magic` let a rule reason about file structure, not just bytes.
- **Conditions**: combine string matches, offsets and file properties; use `private` rules for helper logic.
- **Testing discipline**: validate against a labeled sample set and measure false positives, not just true positives.
- **Use cases**: file scanning, memory scanning, sandbox enrichment and threat-intel pivoting.

---

## 📝 2. Sigma

- Vendor-neutral YAML that converts to a target SIEM query (Splunk, Elastic, Sentinel and others).
- The **`logsource`** block (category, product, service) is the contract that declares which telemetry the rule needs.
- Core fields: `title`, `id`, `status`, `description`, `references`, `author`, `date`, `tags` (ATT&CK), `logsource`, `detection`, `falsepositives`, `level`.
- Value modifiers and field mappings handle backend differences; correlation rules (newer specification versions) express multi-event logic.

---

## 🔗 3. Pipeline Integration

1. Author once in Sigma; convert in CI to every backend in use.
2. Attach the SBOM/YARA result to the artifact or the sandbox report.
3. Track rule provenance and version; a detection has an owner and a revision.
4. Re-test on specification upgrades; a conversion that silently drops a field is a blind spot.

---

## 🔗 4. Integration with Other Skills

- For the detection lifecycle, see the [detection-engineering](../detection-engineering/SKILL.md) skill.
- For endpoint telemetry, see the [endpoint-detection-engineering](../endpoint-detection-engineering/SKILL.md) skill.
- For malware triage, see the [malware-analysis-multios](../../appsec/malware-analysis-multios/SKILL.md) skill.
- For NDR detection, see the [ids-ips-ndr-engineering](../ids-ips-ndr-engineering/SKILL.md) skill.
