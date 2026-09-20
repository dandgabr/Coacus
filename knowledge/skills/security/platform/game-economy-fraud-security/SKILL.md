---
name: game-economy-fraud-security
description: Acts as a Game Economy and Fraud Security specialist covering real-money trading (RMT), in-game economy abuse, account theft and resale, cheat-marketplace economics, boosting-for-hire and the security of blockchain and play-to-earn game mechanics.
metadata:
  type: defensive
  phase: actions
---

# Game Economy and Fraud Security

This skill guides the AI to protect the in-game economy and the accounts that participate in it, where cheating meets fraud.

---

## 💰 1. Economy Abuse

| Abuse | Description |
| :--- | :--- |
| **RMT** | Selling in-game value for real money, often via botting or stolen accounts |
| **Gold/item farming** | Automated farming that distorts the economy |
| **Duplication** | Exploiting economy bugs to create value from nothing |
| **Market manipulation** | Coordinated buying/selling to corner a market |
| **Chargeback fraud** | Purchasing then reversing payment after consuming value |

Protection requires server-authoritative economy rules, anomaly detection on transaction patterns, and rate limits on value transfer.

---

## 🔑 2. Account Security

- Credential stuffing and phishing target game accounts because they hold value.
- Enforce phishing-resistant MFA, session controls and anomaly detection on login and trade.
- Account recovery is a major attack path; a weak recovery flow defeats strong authentication.
- Detect and disrupt account-resale and shared-account behavior where policy forbids it.

---

## 🕶️ 3. Cheat Marketplaces

- Cheating-as-a-service runs on cloud VMs and hardware DMA cards, largely invisible to host-side anti-cheat.
- Disrupt supply where legally and ethically possible; monitor distribution channels; treat cheat distribution as fraud infrastructure.

---

## ⛓️ 4. Blockchain and Play-to-Earn

- Token and NFT mechanics add smart-contract risk, wallet-key theft and on-chain market manipulation.
- Apply Web3 security to on-chain game components (see the [blockchain-cryptocurrency](../../../domains/industry/blockchain-cryptocurrency/SKILL.md) skill) while keeping off-chain game logic authoritative.
- Economic design mistakes (tokenomics) create security incentives; involve security in economy design, not after.

---

## 🔗 5. Integration with Other Skills

- For detection and enforcement, see the [game-anticheat-engineering](../game-anticheat-engineering/SKILL.md) skill.
- For the economy's network authority, see the [game-network-authority-security](../game-network-authority-security/SKILL.md) skill.
- For account security and IAM, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- For competitive integrity, see the [esports-integrity-governance](../../grc/esports-integrity-governance/SKILL.md) skill.
