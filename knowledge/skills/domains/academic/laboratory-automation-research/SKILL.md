---
name: laboratory-automation-research
description: >-
  Guides planning and review of laboratory automation workflows. Use when designing a protocol for laboratory software, checking a simulated run or preparing a handoff to an equipment operator.
---

# Laboratory automation research

1. Define the intended protocol, sample identities, equipment, labware, software and environment. Identify operations that would change a remote service or control physical equipment; a planning request does not establish that such actions have occurred.
2. Review the protocol against the actual equipment and laboratory configuration, including supported device capabilities, labware geometry, deck layout, calibration, consumables, sample traceability and recovery from interruption. Record unknowns instead of assuming a simulated configuration matches the physical setup.
3. Validate the software plan and simulate where supported. Record the exact protocol and configuration reviewed, the simulation backend and its limitations. A successful simulation does not establish calibration, collision safety or successful physical execution.
4. For an authorized physical run, hand off the specific protocol revision and configuration to the trained operator responsible for equipment and institutional procedures. Record actual outcomes and exceptions separately from planned or simulated results.
5. Keep service credentials and sensitive sample information out of shared plans and logs. Before a remote operation, distinguish read access from operations that create, change or transmit data.

The workflow was informed by the [upstream laboratory automation skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/pylabrobot/SKILL.md). Consult the current device and laboratory documentation for actual capabilities and operating requirements.
