---
name: endpoint-forensics
description: Acts as an Endpoint Forensics specialist covering Windows artifacts (MFT/USN, prefetch, ShimCache/AmCache, SRUM, LNK/jumplists, registry hives, event logs), Linux artifacts (journal, shell history, cron) and macOS artifacts (Unified Log, FSEvents), plus timeline construction.
metadata:
  type: defensive
  phase: actions
---

# Endpoint Forensics

This skill guides the AI to reconstruct what happened on a host from the artifacts it left behind.

---

## 🪟 1. Windows Artifacts

| Artifact | Answers |
| :--- | :--- |
| **MFT / USN journal** | What files existed, were created or deleted, and when |
| **Prefetch** | What executed and how often |
| **ShimCache / AmCache** | What ran, even if deleted; application compatibility and execution |
| **SRUM** | Per-application resource and network usage |
| **LNK files / jump lists** | User file access and recent activity |
| **Registry hives** | Persistence, USB history, autoruns, user activity |
| **Event logs** | Logons, service installs, process creation, PowerShell |
| **Browser artifacts** | Downloads, history, cached credentials |

Always acquire memory before disk when volatile artifacts matter.

---

## 🐧 2. Linux Artifacts

- **systemd journal**: services, units and authentication events.
- **Shell history** and auditd logs; note that attackers clear history and logs.
- **cron/at/systemd timers** for persistence.
- **File timestamps** (careful: MAC times are manipulated by timestomping; correlate with journal).

---

## 🍏 3. macOS Artifacts

- **Unified Log** and **FSEvents**: process execution and filesystem changes.
- **LaunchAgents/Daemons** and login items for persistence.
- **Quarantine flags** and code-signing metadata on downloaded files.
- **TCC database** for privacy-permission grants.

---

## 🧵 4. Timeline Construction

1. Normalize all timestamps to UTC and a single format.
2. Merge artifacts into a super-timeline (disk, memory, network, cloud).
3. Tag the timeline with detection rules and IOCs.
4. Review collaboratively; a timeline is an investigator's instrument, not a report.

---

## ⚠️ 5. Anti-Forensics

Watch for timestomping, log clearing (ATT&CK T1070), history deletion and secure-wipe tools. The absence of an artifact is itself evidence; note gaps explicitly.

---

## 🔗 6. Integration with Other Skills

- For memory analysis, see the [memory-forensics](../../platform/memory-forensics/SKILL.md) skill.
- For the incident process, see the [dfir-forensics](../../operations/dfir-forensics/SKILL.md) skill.
- For endpoint telemetry, see the [endpoint-detection-engineering](../../operations/endpoint-detection-engineering/SKILL.md) skill.
- For Windows internals, see the [windows-internals-security](../../platform/windows-internals-security/SKILL.md) skill.
