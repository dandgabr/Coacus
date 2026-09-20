---
name: academic-classical-mechanics-relativity
description: "Specializes in Advanced Classical Mechanics, Analytical Dynamics, Chaos Theory, and Special and General Relativity building on Classical Mechanics (Herbert Goldstein), Mechanics (Landau & Lifshitz), Gravitation (Misner, Thorne, Wheeler), and Spacetime and Geometry (Sean Carroll). Covers Lagrangian and Hamiltonian Formalisms (Euler-Lagrange, Legendre Transform, Poisson Brackets, Canonical Transformations, Hamilton-Jacobi, and Noether's Theorem), Three-Dimensional Rigid Body Dynamics (Inertia Tensor, Euler Angles, Euler Equations of Motion), Small Oscillation Theory and Normal Modes, Deterministic Chaos Theory (Lyapunov Exponents, Poincaré Sections, Strange Attractors), Covariant Special Relativity (Minkowski Four-Vectors, Electromagnetic Tensor Fμν), and General Relativity (Geodesics, Riemann Curvature Tensor, Einstein Field Equations, and Schwarzschild Metric)."
---

# Advanced Classical Mechanics and Relativity Theory (Goldstein & Landau)

This skill establishes the mathematical and physical foundations of variational analytical mechanics, many-body and rigid-body system dynamics, chaos theory, and the relativistic geometry of Lorentz and Einstein spacetime.

---

## ⚙️ 1. Lagrangian and Hamiltonian Formalism

### 1.1 Hamilton's Principle and Euler-Lagrange Equations
Hamilton's principle of least action $\delta S = \delta \int_{t_1}^{t_2} L(q_i, \dot{q}_i, t) \, dt = 0$ governs motion in generalized coordinates $q_i$:

$$\frac{d}{dt}\left( \frac{\partial L}{\partial \dot{q}_i} \right) - \frac{\partial L}{\partial q_i} = Q_i^{nc}$$

where $L = T - V$ is the Lagrangian function and $Q_i^{nc}$ are generalized non-conservative forces.

- **Noether's Theorem**: For every continuous symmetry of the action (invariance under a one-parameter group), there exists a conserved quantity:
  - Invariance under time translation $\implies$ Conservation of Total Energy $H$.
  - Invariance under spatial translation $\implies$ Conservation of Total Linear Momentum $\mathbf{P}$.
  - Invariance under spatial rotation $\implies$ Conservation of Total Angular Momentum $\mathbf{L}$.
  - Cyclic coordinate ($\frac{\partial L}{\partial q_k} = 0$) $\implies$ Constant conjugate momentum $p_k = \frac{\partial L}{\partial \dot{q}_k} = \text{const}$.

### 1.2 Hamiltonian Mechanics and Poisson Brackets
The Hamiltonian function $H(q, p, t)$ obtained via the Legendre Transform $H = \sum_i p_i \dot{q}_i - L$:

$$\dot{q}_i = \frac{\partial H}{\partial p_i}, \quad \dot{p}_i = -\frac{\partial H}{\partial q_i}$$

- **Poisson Brackets**: $\{f, g\} = \sum_i \left( \frac{\partial f}{\partial q_i} \frac{\partial g}{\partial p_i} - \frac{\partial f}{\partial p_i} \frac{\partial g}{\partial q_i} \right)$.
- **Time Evolution of an Observable**: $\frac{df}{dt} = \{f, H\} + \frac{\partial f}{\partial t}$.
- **Hamilton-Jacobi Equation**: $H\left( q_i, \frac{\partial S}{\partial q_i}, t \right) + \frac{\partial S}{\partial t} = 0$, where $S(q_i, \alpha_i, t)$ is Hamilton's principal function.

---

## 🔄 2. Rigid Body Dynamics and Small Oscillations

### 2.1 Inertia Tensor and Euler Equations
The symmetric second-order inertia tensor $\mathbf{I}$:

$$I_{jk} = \int_V \rho(\mathbf{r}) \left( r^2 \delta_{jk} - x_j x_k \right) dV$$

- **Euler Equations for a Rigid Body in Principal Axes ($1, 2, 3$)**:
  $$I_1 \dot{\omega}_1 - (I_2 - I_3) \omega_2 \omega_3 = N_1$$
  $$I_2 \dot{\omega}_2 - (I_3 - I_1) \omega_3 \omega_1 = N_2$$
  $$I_3 \dot{\omega}_3 - (I_1 - I_2) \omega_1 \omega_2 = N_3$$
  where $\mathbf{N}$ is the applied external torque.

### 2.2 Small Oscillation Theory and Normal Modes
For small perturbations $\boldsymbol{\eta} = \mathbf{q} - \mathbf{q}_0$ around stable equilibrium ($\nabla V(\mathbf{q}_0) = 0$):
$$L \approx \frac{1}{2} \dot{\boldsymbol{\eta}}^T \mathbf{M} \dot{\boldsymbol{\eta}} - \frac{1}{2} \boldsymbol{\eta}^T \mathbf{K} \boldsymbol{\eta}$$
- **Natural Frequencies ($\omega$)**: Solutions of the secular equation $\det(\mathbf{K} - \omega^2 \mathbf{M}) = 0$.

---

## 🌀 3. Deterministic Chaos Theory and Non-Linear Systems

- **Sensitivity to Initial Conditions (Butterfly Effect)**: Exponential divergence of neighboring trajectories in phase space $\delta \mathbf{x}(t) \approx \delta \mathbf{x}(0) e^{\lambda t}$.
- **Maximum Lyapunov Exponent ($\lambda_{max}$)**:
  $$\lambda_{max} = \lim_{t \to \infty} \frac{1}{t} \ln \frac{\|\delta \mathbf{x}(t)\|}{\|\delta \mathbf{x}(0)\|}$$
  If $\lambda_{max} > 0$, the system exhibits deterministic chaotic dynamics.
- **Poincaré Section**: A discrete stroboscopic mapping that reduces the continuous dimensionality of the fractal strange attractor.

---

## 🌌 4. Special and General Relativity Theory

### 4.1 Special Relativity in Covariant 4-Vector Notation
Minkowski metric $\eta_{\mu\nu} = \text{diag}(-1, 1, 1, 1)$ with $x^\mu = (ct, x, y, z)$:

- **Invariant Interval**: $ds^2 = \eta_{\mu\nu} dx^\mu dx^\nu = -c^2 d\tau^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2$.
- **Four-Momentum**: $P^\mu = m \frac{dx^\mu}{d\tau} = (\gamma m c, \gamma m \mathbf{v}) = (E/c, \mathbf{p}) \implies P_\mu P^\mu = -\frac{E^2}{c^2} + p^2 = -m^2 c^2$.
- **Maxwell Electromagnetic Tensor**:
  $$F^{\mu\nu} = \begin{bmatrix} 0 & E_x/c & E_y/c & E_z/c \\ -E_x/c & 0 & B_z & -B_y \\ -E_y/c & -B_z & 0 & B_x \\ -E_z/c & B_y & -B_x & 0 \end{bmatrix}, \quad \partial_\mu F^{\mu\nu} = \mu_0 J^\nu$$

### 4.2 General Relativity and Einstein Field Equations
Gravity described as the curvature of pseudo-Riemannian spacetime with metric $g_{\mu\nu}$:

- **Geodesic Equation (Free Fall)**:
  $$\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0, \quad \Gamma^\mu_{\alpha\beta} = \frac{1}{2} g^{\mu\sigma} \left( \partial_\alpha g_{\beta\sigma} + \partial_\beta g_{\alpha\sigma} - \partial_\sigma g_{\alpha\beta} \right)$$
- **Einstein Field Equations with Cosmological Constant $\Lambda$**:
  $$G_{\mu\nu} + \Lambda g_{\mu\nu} = R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$
- **Schwarzschild Metric in Static, Spherically Symmetric Vacuum**:
  $$ds^2 = -\left(1 - \frac{2GM}{c^2 r}\right) c^2 dt^2 + \left(1 - \frac{2GM}{c^2 r}\right)^{-1} dr^2 + r^2 (d\theta^2 + \sin^2\theta \, d\phi^2)$$
  where $r_s = \frac{2GM}{c^2}$ is the event horizon radius of the Schwarzschild black hole.
