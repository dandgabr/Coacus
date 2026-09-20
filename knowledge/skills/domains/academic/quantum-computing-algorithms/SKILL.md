---
name: quantum-computing-algorithms
description: "Specializes in Advanced Quantum Mechanics, Theoretical Physics, Quantum Circuits, and Quantum Algorithms building on J. J. Sakurai (Modern Quantum Mechanics), Claude Cohen-Tannoudji (Quantum Mechanics), and Michael A. Nielsen & Isaac L. Chuang (Quantum Computation and Quantum Information). Covers the Dirac Formalism in Hilbert Space, the Quantum Harmonic Oscillator via Ladder Operators, Angular Momentum and Spin 1/2 (Pauli Matrices, Clebsch-Gordan Coefficients), Perturbation Theory and Fermi's Golden Rule, Qubit Fundamentals and the Bloch Sphere, Universal Quantum Gates (Hadamard, Pauli-X/Y/Z, Phase-S/T, CNOT, Toffoli), Quantum Entanglement (Bell States, GHZ), the Quantum Fourier Transform (QFT), Shor's Algorithm (Polynomial Factorization), Grover's Algorithm (Quadratic-Speedup Search), the Variational Quantum Eigensolver (VQE for Quantum Chemistry), and Practical Implementation with Qiskit (IBM) and Cirq (Google)."
---

# Quantum Mechanics, Quantum Information, and Quantum Algorithms

This skill establishes the physical foundations in Hilbert spaces, operator algebra, and quantum logic gates, unifying theoretical quantum mechanics (**Sakurai & Cohen-Tannoudji**) with quantum computer science (**Nielsen & Chuang** and the Qiskit/Cirq ecosystems).

---

## ⚛️ 1. Dirac Formalism in Hilbert Space $\mathcal{H}$

### 1.1 State Vectors, Postulates, and Pauli Algebra
- **Schrödinger Equation**:
  $$i\hbar \frac{d}{dt} |\psi(t)\rangle = \hat{H} |\psi(t)\rangle \implies |\psi(t)\rangle = e^{-i\hat{H}t/\hbar} |\psi(0)\rangle$$
- **Spin 1/2 and Pauli Matrices $\boldsymbol{\sigma}$**:
  $$\hat{\mathbf{S}} = \frac{\hbar}{2}\boldsymbol{\sigma}, \quad \sigma_x = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad \sigma_y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}, \quad \sigma_z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$$
  with commutator $[\sigma_i, \sigma_j] = 2i\varepsilon_{ijk} \sigma_k$ and anti-commutator $\{\sigma_i, \sigma_j\} = 2\delta_{ij} I$.

### 1.2 Perturbation Theory and Fermi's Golden Rule
For a system subjected to a harmonic perturbation $\hat{V}(t) = \hat{V} e^{-i\omega t}$, the transition rate per unit time into a continuum of states with density $\rho(E_f)$ is given by **Fermi's Golden Rule**:
$$W_{i \to f} = \frac{2\pi}{\hbar} |\langle f | \hat{V} | i \rangle|^2 \rho(E_f)$$

---

## 🌐 2. Qubits, the Bloch Sphere, and Universal Quantum Gates

```
                 |0⟩ (Polo Norte)
                   ▲
                   │     / (vetor de estado |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩)
                   │    /
                   │   /
                   │  /
                   │ /
  ─────────────────┼─────────────────► Y
                  /│
                 / │
                /  │
               ▼   ▼
              X   |1⟩ (Polo Sul)
```

- **Qubit**: $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$.
- **Hadamard Gate ($H$)**: Creates a balanced superposition $H|0\rangle = |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$, $H|1\rangle = |-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$.
- **CNOT Gate ($CX$) and Bell State**:
  $$\text{CNOT}(H \otimes I)|00\rangle = |\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

---

## 💻 3. Simulation and Circuits with Qiskit

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Circuito Quântico de Entrelaçamento Máximo (Bell State)
qc = QuantumCircuit(2, 2)
qc.h(0)          # Superposição no Qubit 0
qc.cx(0, 1)      # Entrelaçamento controlado (Q0 -> Q1)
qc.measure([0, 1], [0, 1])

# Execução em simulador quântico
simulator = AerSimulator()
compiled_qc = transpile(qc, simulator)
job = simulator.run(compiled_qc, shots=2048)
counts = job.result().get_counts(qc)
print("Distribuição das Medições:", counts)
# Saída esperada: ~50% '00' e ~50% '11'
```

---

## 📐 4. Fundamental Quantum Algorithms

| Algorithm | Classical Complexity | Quantum Complexity | Impact & Application |
| :--- | :---: | :---: | :--- |
| **Shor's Algorithm** | Sub-exponential $\mathcal{O}(e^{c \sqrt[3]{\ln N (\ln \ln N)^2}})$ | Polynomial $\mathcal{O}((\log N)^3)$ | Breaks RSA/ECC cryptography via the Quantum Fourier Transform (QFT) for phase estimation. |
| **Grover's Search** | Linear $\mathcal{O}(N)$ | Quadratic $\mathcal{O}(\sqrt{N})$ | Search in unstructured databases via amplitude amplification by inversion about the mean. |
| **VQE (Variational Quantum Eigensolver)** | Exponential $\mathcal{O}(2^n)$ | Hybrid Classical-Quantum | Variational minimization of the ground-state energy $\langle \psi(\theta) | \hat{H} | \psi(\theta) \rangle$ for quantum chemistry and new materials. |
| **QPE (Quantum Phase Estimation)** | Exponential | Polynomial $\mathcal{O}(n^2)$ | Determination of the unitary eigenvalues of $\hat{U}|\psi\rangle = e^{2\pi i \theta}|\psi\rangle$. |
