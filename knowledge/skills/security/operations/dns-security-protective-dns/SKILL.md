---
name: dns-security-protective-dns
description: Acts as a DNS Security specialist covering DNSSEC validation, encrypted DNS (DoT/DoH) and Oblivious DoH, protective DNS with blocking resolvers, DNS logging and threat detection, and defense against cache poisoning, tunneling and amplification attacks, aligned with NIST SP 800-81r3.
metadata:
  type: defensive
  phase: actions
---

# DNS Security and Protective DNS

This skill guides the AI to secure the resolution path and to use DNS as both a control point and a detection source, following **NIST SP 800-81r3** (Secure DNS Deployment Guide).

---

## 🛡️ 1. Integrity: DNSSEC

- DNSSEC signs zone data so a resolver can prove the answer is authentic and unmodified.
- Validating resolvers should reject bogus answers rather than silently accepting them.
- Sign zone delegations and monitor for expiry; an expired signature breaks resolution.
- DNSSEC does **not** provide confidentiality - it proves integrity only.

---

## 🔐 2. Confidentiality: Encrypted DNS

- **DoT (RFC 7858)** and **DoH** encrypt the query between client and resolver.
- **Oblivious DoH (RFC 9230)** separates the client's identity from the query so the target resolver cannot link them.
- There is a real tension: encrypted DNS improves user privacy but removes enterprise visibility. Resolve it architecturally (a corporate protective resolver with a policy) rather than by blocking encrypted DNS blindly.

---

## 🚫 3. Protective DNS

- A protective resolver blocks resolution of known-malicious domains (malware C2, phishing, cryptomining) and logs every query.
- Use it as a preventive control (block) and a detective one (alert on lookups to newly seen or rare domains).
- Keep blocklists fed by threat intelligence and tune for false positives before enforcing broadly.

---

## 🔎 4. DNS Attacks and Detection

| Attack | Detection signal |
| :--- | :--- |
| Cache poisoning | Unexpected or conflicting answers; validate DNSSEC |
| DNS tunneling / exfiltration | High query entropy, long labels, volume anomalies |
| Amplification DDoS | Large responses to spoofed small queries; implement response-rate limiting |
| NXDOMAIN / random subdomain flood | Burst of nonexistent names |
| Registrar/zone hijack | Unexpected authoritative NS or delegation changes; monitor at the registrar |

---

## 🏗️ 5. Deployment Rules

1. Operate internal resolvers with DNSSEC validation and encrypted transport to upstreams.
2. Centralize query logging and ship it to the SIEM.
3. Harden zone transfers (allow only to authorized secondaries) and the registrar account (MFA, lock).
4. Monitor certificate and DNSSEC expiry as availability controls.

---

## 🔗 6. Integration with Other Skills

- For network architecture, see the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) skill.
- For flow and DPI tooling, see the [network-flow-discovery](../../../mapping/network-flow-discovery/SKILL.md) skill.
- For NDR detection, see the [ids-ips-ndr-engineering](../ids-ips-ndr-engineering/SKILL.md) skill.
- For routing integrity, see the BGP section of the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) skill.
