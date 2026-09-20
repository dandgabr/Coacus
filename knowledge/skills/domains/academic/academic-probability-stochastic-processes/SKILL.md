---
name: academic-probability-stochastic-processes
description: "Specializes in Axiomatic Probability, Measure Theory, and Stochastic Processes building on Probability and Random Processes (Grimmett, Stirzaker), Probability: Theory and Examples (Rick Durrett), and Stochastic Differential Equations (Bernt Øksendal). Covers Probability Spaces (Kolmogorov, σ-algebras, Lebesgue-Stieltjes Measure, Conditional Expectation as Projection in L2), Modes of Convergence (Almost Sure, in Probability, in Lp, in Distribution, Borel-Cantelli Lemmas, and Slutsky's Theorem), Discrete- and Continuous-Time Markov Chains (Chapman-Kolmogorov Differential Equations, Generator Matrix Q, Stationary Distributions), Martingale Theory (Doob's Optional Stopping Theorem), the Poisson Process and Queueing Theory (M/M/1, Little's Law), and Brownian Motion / Itô Stochastic Calculus (Itô's Lemma and SDEs)."
---

# Axiomatic Probability and Stochastic Processes (Grimmett & Durrett)

This skill establishes the formal mechanistic and probabilistic foundations under Measure Theory, convergence of multivariate random variables, Markov chains, martingale theory, point processes, and stochastic differential equations.

---

## 🎲 1. Kolmogorov's Axiomatic Foundation and Measure Theory

### 1.1 Probability Space $(\Omega, \mathcal{F}, P)$
- $\Omega$: Sample space of elementary events.
- $\mathcal{F}$: $\sigma$-algebra of subsets of $\Omega$ closed under complementation and countable unions.
- $P: \mathcal{F} \to [0, 1]$: Finitely additive and $\sigma$-additive probability measure with $P(\Omega) = 1$.
- **Conditional Expectation as Projection in $L^2$**: Given a sub-$\sigma$-algebra $\mathcal{G} \subseteq \mathcal{F}$, $E[X|\mathcal{G}]$ is the unique $\mathcal{G}$-measurable random variable such that:
  $$\int_A E[X|\mathcal{G}] \, dP = \int_A X \, dP, \quad \forall A \in \mathcal{G}$$

### 1.2 Modes of Stochastic Convergence and Borel-Cantelli Lemmas
```
Hierarquia de Modos de Convergência:
  Convergência em Lp (p ≥ 1) ──┐
                               ▼
  Convergência Quase Certa (q.c. / a.s.) ──> Convergência em Probabilidade (P) ──> Convergência em Distribuição (d)
```

- **First Borel-Cantelli Lemma**: If $\sum_{n=1}^\infty P(A_n) < \infty$, then $P(\limsup_{n \to \infty} A_n) = 0$.
- **Second Borel-Cantelli Lemma**: If the events $A_n$ are independent and $\sum_{n=1}^\infty P(A_n) = \infty$, then $P(\limsup_{n \to \infty} A_n) = 1$.
- **Slutsky's Theorem**: If $X_n \xrightarrow{d} X$ and $Y_n \xrightarrow{P} c$ (constant), then $X_n + Y_n \xrightarrow{d} X + c$ and $X_n Y_n \xrightarrow{d} cX$.

---

## 📈 2. Discrete- and Continuous-Time Markov Chains

### 2.1 Discrete Time (DTMC) and the Chapman-Kolmogorov Equation
For a sequence $\{X_n\}_{n=0}^\infty$ satisfying the Markov property $P(X_{n+1}=j \mid X_n=i, \dots, X_0=i_0) = P_{ij}$:
$$P_{ij}^{(n+m)} = \sum_{k \in \mathcal{S}} P_{ik}^{(n)} P_{kj}^{(m)} \iff \mathbf{P}^{(n+m)} = \mathbf{P}^{(n)} \mathbf{P}^{(m)}$$
- **Stationary Distribution $\boldsymbol{\pi}$**: For irreducible and aperiodic chains:
  $$\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi} \quad \text{with } \sum_{i \in \mathcal{S}} \pi_i = 1$$

### 2.2 Continuous Time (CTMC) and the Infinitesimal Generator Matrix $\mathbf{Q}$
Transitions governed by rates $\lambda_{ij} \ge 0$ ($i \ne j$) with $q_{ii} = -\sum_{j \ne i} q_{ij}$:
- **Kolmogorov Differential Equations**:
  - *Backward*: $\frac{d \mathbf{P}(t)}{dt} = \mathbf{Q} \mathbf{P}(t)$
  - *Forward*: $\frac{d \mathbf{P}(t)}{dt} = \mathbf{P}(t) \mathbf{Q} \implies \mathbf{P}(t) = e^{\mathbf{Q} t}$
- **Stationary Equilibrium**: $\boldsymbol{\pi} \mathbf{Q} = \mathbf{0}$.

---

## 🛑 3. Martingale Theory and Stopping Times (Doob)

An integrable stochastic process $\{M_n\}_{n=0}^\infty$ adapted to a filtration $\{\mathcal{F}_n\}_{n=0}^\infty$ is a **Martingale** if $E[|M_n|] < \infty$ and:
$$E[M_{n+1} \mid \mathcal{F}_n] = M_n, \quad \forall n \ge 0$$
- **Stopping Time $\tau$**: A random variable taking values in $\{0, 1, 2, \dots\} \cup \{\infty\}$ such that $\{\tau = n\} \in \mathcal{F}_n$.
- **Doob's Optional Stopping Theorem**: If $M_n$ is a martingale and $\tau$ is a bounded stopping time ($\tau \le K$ a.s.), then:
  $$E[M_\tau] = E[M_0]$$

---

## 📉 4. Brownian Motion and Itô Stochastic Calculus

### 4.1 Wiener Process $W(t)$
1. $W(0) = 0$ almost surely.
2. Independent increments: For $0 \le t_1 < t_2 < \dots < t_k$, $W(t_{i+1}) - W(t_i)$ are mutually independent.
3. Stationary Gaussian increments: $W(t) - W(s) \sim \mathcal{N}(0, t - s)$.
4. Continuous but almost nowhere differentiable paths with finite quadratic variation $[W, W]_t = t$.

### 4.2 Itô's Lemma for Stochastic Differential Equations (SDEs)
For an Itô diffusion process $dX_t = \mu(t, X_t) dt + \sigma(t, X_t) dW_t$ and a twice-differentiable function $f(t, x)$:

$$df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t$$

---

## 🚶 5. Queueing Theory and Birth-Death Processes

- **Little's Law**: In any system at steady state, the average number of entities in the system ($L$) correlates with the average arrival rate ($\lambda$) and the average time in the system ($W$):
  $$L = \lambda W \quad \text{and} \quad L_q = \lambda W_q$$
- **$M/M/1$ Queue with arrival rate $\lambda$ and service rate $\mu$ ($\rho = \lambda/\mu < 1$)**:
  - Probability of $n$ customers: $p_n = (1 - \rho) \rho^n$.
  - Average number in the system: $L = \frac{\rho}{1 - \rho}$.
  - Average time in the system: $W = \frac{1}{\mu - \lambda}$.
