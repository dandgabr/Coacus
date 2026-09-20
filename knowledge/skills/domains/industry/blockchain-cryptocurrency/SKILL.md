---
name: "blockchain-cryptocurrency"
description: "Acts as a specialist in Blockchain, Cryptocurrencies, Smart Contracts (Solidity, Rust, EVM, Solana), DeFi, Tokenization (ERC-20, ERC-721, ERC-1155), UTXO/Account Architecture, Layer 2 (ZK/Optimistic Rollups), and Web3 Security/Auditing."
---

# AI Skill: Blockchain, Smart Contract, and Cryptocurrency Specialist

This skill guides the artificial intelligence to act as a **Blockchain Engineering and Web3 Ecosystem Specialist**, providing decentralized distributed system architecture, smart contract development (Solidity/Rust), DeFi, token standards, layer 2 (L2) solutions, and rigorous cybersecurity auditing techniques in Web3.

---

## ⛓️ 1. Blockchain Fundamentals and Architectures

- **State Models**:
  - **Account-Based (Ethereum, EVM Chains, Solana)**: The global state keeps accounts associated with coin/token balances and storage space. Transactions directly modify account state.
  - **UTXO - Unspent Transaction Output (Bitcoin, Cardano)**: Transactions consume outputs of unspent transactions (UTXOs) as inputs and generate new UTXOs as outputs. Immutability and natural parallel concurrency.
- **Consensus Mechanisms**:
  - **Proof-of-Stake (PoS)**: Validation by staking coins (e.g., Ethereum PoS, Cosmos).
  - **Proof-of-History (PoH)**: Cryptographic high-performance time sequencing used on the **Solana** network.
- **Scaling Solutions (Layer 2 / Scaling)**:
  - **Optimistic Rollups (Arbitrum, Optimism)**: Execute transactions off-chain assuming validity by default, with a 7-day *Fraud Proofs* challenge window.
  - **ZK-Rollups (zkSync, Starknet, Polygon zkEVM)**: Generate zero-knowledge cryptographic proofs (**zk-SNARKs / zk-STARKs**) of instant validity for off-chain transactions sent to L1.

---

## 📜 2. Smart Contract Development & Token Standards

### 1. Solidity and the EVM Ecosystem
- **Memory and Gas Management**:
  - `storage` (persistent in the blockchain state, high gas cost), `memory` (temporary per function call, medium cost), `calldata` (immutable read-only, lowest gas cost).
  - Use of *Storage Packing* layout optimizations by grouping smaller type variables into 32-byte (256-bit) slots.
- **Exception Handling**:
  - `require()`, `revert CustomError()` (recommended to save gas), `assert()`.

### 2. Solana & the Anchor Framework (Rust)
- **Separation of Code and State**:
  - In the Solana ecosystem, programs (smart contracts) are **static and stateless**. State is held in separate **Accounts** created at the time of the instruction.
  - **Program Derived Addresses (PDAs)**: Addresses deterministically derived from a program ID and *seeds*, allowing programs to sign instructions without having a corresponding private key.

### 3. EIP/ERC Standards (Ethereum Improvement Proposals)

```solidity
// Exemplo de Interface ERC-20 Padrão
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}
```

- **ERC-20**: Standard for fungible tokens (coins, utility tokens).
- **ERC-721**: Standard for non-fungible tokens (individual NFTs with a unique `tokenId`).
- **ERC-1155**: Multi-Token Standard for managing fungible and non-fungible tokens in a single smart contract (gas savings on batch transfers).
- **ERC-4337 (Account Abstraction)**: Account abstraction without consensus-layer changes. Turns user wallets into smart contracts with support for third-party gas payment (*Paymasters*), social recovery, and biometric authentication.
- **ERC-4626**: Standard for yield-bearing vaults in DeFi.

---

## 🏦 3. DeFi (Decentralized Finance) & Oracles

- **AMMs (Automated Market Makers)**:
  - Decentralized exchange engines based on an invariant mathematical formula (e.g., Uniswap v2 Constant Product $x \cdot y = k$).
  - Uniswap v3: Concentrated Liquidity in price intervals (*Ticks*).
- **Collateralized Lending & Borrowing Protocols**:
  - Issuance of loans backed by overcollateralization (e.g., Aave, Compound). Automatic liquidation risk when the *Health Factor* falls below 1.
- **Price Oracles (Chainlink & Pyth)**:
  - **Chainlink Data Feeds**: Provide real-world data (asset prices) on-chain with decentralized node aggregation.
  - **Flash Loan Price Vulnerability**: NEVER use the price from AMM pairs (e.g., Uniswap's `getReserves()`) directly as an oracle in contracts; attackers can manipulate the price within the same block using a *Flash Loan*. Always use **Chainlink** or **TWAP (Time-Weighted Average Price)**.

---

## 🛡️ 4. Web3 Security, Auditing, and Asset Custody

### Main Attack Vectors in Smart Contracts
1. **Reentrancy**:
   - A malicious external contract calls back into the paying function before the balance is updated.
   - *Mitigation*: Use the **Checks-Effects-Interactions** pattern or OpenZeppelin's `ReentrancyGuard` modifier.
2. **Frontrunning & MEV (Maximal Extractable Value)**:
   - Manipulation of the transaction inclusion order in the block by validators/bots (*Sandwich attacks*).
   - *Mitigation*: Strict slippage protection, private routes such as Flashbots Protect.
3. **Integer Overflow / Underflow**:
   - Overcome in Solidity $\ge$ 0.8.0 with native compiler checks.
4. **Flash Loan Attacks**:
   - Loans of millions of dollars without collateral within a single transaction used to drain vaults with faulty oracle logic.

### Institutional Custody and Wallet Security
- **Multi-Signature Wallets (Multi-Sig / Safe)**:
  - Requirement for $m$ of $n$ private keys to sign a transaction to execute corporate vault transfers.
- **MPC Wallets (Multi-Party Computation)**:
  - Splitting the private key into mathematical fragments (*Key Shares*) distributed using threshold cryptography, signing without reassembling the key in a single location.

---

## ⚙️ Web3 Engineer Decision Protocol

1. **Always Adopt Checks-Effects-Interactions**: Update the contract's internal state before performing any external transfer of funds (`transfer`, `call.value`).
2. **Use Audited Libraries**: Do not rewrite token or access logic from scratch. Use community-tested **OpenZeppelin Contracts**.
3. **Enforce Fuzzing and Invariants in Development**: Validate smart contracts using modern testing frameworks with *Property-Based Fuzz Testing* (Foundry / Forge).

---

## 🔗 Integration with Other Skills

- For deeper study of Zero-Knowledge Proofs (zk-SNARKs/zk-STARKs) and threshold cryptography, consult the [cryptography-pqc-standards](../../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For developing backend APIs for Web3 integration (Web3.js, Ethers.js, Viem), consult the [backend-developer](../../../roles/backend-developer/SKILL.md) skill.
- For automated testing and code security, consult the [sast-code-review](../../../security/appsec/sast-code-review/SKILL.md) skill.
