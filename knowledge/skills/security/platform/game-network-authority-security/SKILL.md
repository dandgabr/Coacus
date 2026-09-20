---
name: game-network-authority-security
description: Acts as a Game Network Authority specialist covering server-authoritative design, need-to-know replication, RPC validation, client prediction and reconciliation, packet manipulation and replay, lag switches and game server DDoS.
metadata:
  type: defensive
  phase: recon
---

# Game Network Authority and Protocol Security

This skill guides the AI to build the primary systemic defense against cheating: a server that does not trust the client.

---

## 🏛️ 1. Never Trust the Client

- The server computes positions, hits, damage and economy outcomes from client-supplied **inputs**, never from client-supplied **results**.
- A client that reports "I hit the enemy" is a client asking to be believed; the server must be able to verify it from the inputs and its own simulation.
- Client-authoritative designs are the single largest source of exploitable cheats.

---

## 🔄 2. Replication

- **Need-to-know**: never send a client state it should not see (opponents behind walls, hidden units); this is the root cause of wallhack/ESP effectiveness.
- Replicate what the client needs to render, not the whole world.
- Validate RPC arguments server-side: reject NaN, impossible view angles, out-of-range values and impossible timings.
- Treat every RPC as an untrusted public API.

---

## 🧮 3. Prediction and Reconciliation

- Client-side prediction improves responsiveness; the server remains authoritative and corrects the client's simulation.
- The client must accept server corrections without allowing them to be manipulated to gain advantage.
- Lockstep and deterministic protocols mitigate look-ahead cheats; document the model's assumptions.

---

## 🚨 4. Network Attacks

| Attack | Countermeasure |
| :--- | :--- |
| **Packet manipulation** | Authenticate and integrity-protect protocol messages; do not trust client-computed fields |
| **Replay** | Nonces, sequence numbers and short-lived session keys |
| **Lag switch** | Detect abnormal latency patterns and cap the advantage they confer |
| **DDoS on game servers** | Network-layer protection, edge scrubbing, region distribution |
| **Protocol reverse engineering** | Encrypt and obfuscate where it raises cost, but never rely on obscurity for authorization |

---

## 📈 5. Monitoring

- Instrument for impossible states (teleporting, instant reaction, damage out of sequence) as server-side signals.
- Feed those signals into the anti-cheat detection pipeline.

---

## 🔗 6. Integration with Other Skills

- For detection and enforcement, see the [game-anticheat-engineering](../game-anticheat-engineering/SKILL.md) skill.
- For engine-level protections, see the [game-engine-security](../game-engine-security/SKILL.md) skill.
- For protocol security in general, see the [api-protocol-security](../../appsec/api-protocol-security/SKILL.md) skill.
- For the economic layer, see the [game-economy-fraud-security](../game-economy-fraud-security/SKILL.md) skill.
