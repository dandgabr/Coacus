---
name: academic-electromagnetism-electrodynamics
description: "Specializes in Classical Electromagnetism and Advanced Electrodynamics building on Introduction to Electrodynamics (David J. Griffiths) and Classical Electrodynamics (John David Jackson). Covers Maxwell's Differential and Integral Equations, Lorenz and Coulomb Gauges, Retarded and Liénard-Wiechert Potentials, Electromagnetic Radiation Theory and the Larmor Formula, Wave Propagation in Material Media and Conductors (Skin Effect and Kramers-Kronig Relations), Waveguide Theory (TE, TM, and TEM Modes), and the Four-Dimensional Covariant Formulation of Electromagnetism."
---

# Classical Electromagnetism and Maxwell's Electrodynamics (Griffiths & Jackson)

This skill establishes the unified theory of static and time-dependent electric and magnetic fields in material media, electromagnetic wave propagation, waveguides, radiation from accelerated charges, and the covariant relativistic formulation.

---

## ⚡ 1. The Fundamental Maxwell Equations

### 1.1 Differential and Integral Form in Linear Material Media
$$\begin{aligned}
\nabla \cdot \mathbf{D} &= \rho_f &\iff \oiint_{\partial V} \mathbf{D} \cdot d\mathbf{a} &= Q_{f,enc} \quad &\text{(Gauss's Law)} \\
\nabla \cdot \mathbf{B} &= 0 &\iff \oiint_{\partial V} \mathbf{B} \cdot d\mathbf{a} &= 0 \quad &\text{(Absence of Monopoles)} \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} &\iff \oint_{\partial S} \mathbf{E} \cdot d\mathbf{l} &= -\frac{d\Phi_B}{dt} \quad &\text{(Faraday's Law)} \\
\nabla \times \mathbf{H} &= \mathbf{J}_f + \frac{\partial \mathbf{D}}{\partial t} &\iff \oint_{\partial S} \mathbf{H} \cdot d\mathbf{l} &= I_{f,enc} + \iint_S \frac{\partial \mathbf{D}}{\partial t} \cdot d\mathbf{a} \quad &\text{(Ampère-Maxwell Law)}
\end{aligned}$$

- **Constitutive Relations**: $\mathbf{D} = \varepsilon \mathbf{E} = \varepsilon_0 \mathbf{E} + \mathbf{P}$ and $\mathbf{H} = \frac{1}{\mu} \mathbf{B} = \frac{1}{\mu_0}\mathbf{B} - \mathbf{M}$, with the local Ohm's Law $\mathbf{J}_f = \sigma \mathbf{E}$.

### 1.2 Poynting Theorem and Vector (Energy Conservation)
$$\mathbf{S} = \mathbf{E} \times \mathbf{H} \quad [\text{W/m}^2], \quad -\frac{\partial u_{em}}{\partial t} = \nabla \cdot \mathbf{S} + \mathbf{J}_f \cdot \mathbf{E}$$
where $u_{em} = \frac{1}{2} (\varepsilon |\mathbf{E}|^2 + \mu |\mathbf{H}|^2)$ is the volumetric energy density.

---

## 🔮 2. Potential Theory, Gauges, and Retarded Potentials

### 2.1 Lorenz and Coulomb Gauges
Defining $\mathbf{B} = \nabla \times \mathbf{A}$ and $\mathbf{E} = -\nabla V - \frac{\partial \mathbf{A}}{\partial t}$:
- **Lorenz Gauge**: $\nabla \cdot \mathbf{A} + \mu\varepsilon \frac{\partial V}{\partial t} = 0 \implies$ Decouples the inhomogeneous wave equations:
  $$\nabla^2 V - \frac{1}{c^2}\frac{\partial^2 V}{\partial t^2} = -\frac{\rho}{\varepsilon_0}, \quad \nabla^2 \mathbf{A} - \frac{1}{c^2}\frac{\partial^2 \mathbf{A}}{\partial t^2} = -\mu_0 \mathbf{J}$$
- **Retarded Potentials ($t_r = t - \frac{|\mathbf{r} - \mathbf{r}'|}{c}$)**:
  $$V(\mathbf{r}, t) = \frac{1}{4\pi\varepsilon_0} \int \frac{\rho(\mathbf{r}', t_r)}{|\mathbf{r} - \mathbf{r}'|} d^3\mathbf{r}', \quad \mathbf{A}(\mathbf{r}, t) = \frac{\mu_0}{4\pi} \int \frac{\mathbf{J}(\mathbf{r}', t_r)}{|\mathbf{r} - \mathbf{r}'|} d^3\mathbf{r}'$$

### 2.2 Liénard-Wiechert Potentials for Point Charges
For a charge $q$ with trajectory $\mathbf{w}(t)$ and velocity $\boldsymbol{\beta} = \frac{\mathbf{v}}{c}$:
$$V(\mathbf{r}, t) = \frac{1}{4\pi\varepsilon_0} \frac{q}{(r - \mathbf{r} \cdot \boldsymbol{\beta})}, \quad \mathbf{A}(\mathbf{r}, t) = \frac{\mathbf{v}(t_r)}{c^2} V(\mathbf{r}, t)$$

---

## 📡 3. Electromagnetic Radiation and Waveguides

### 3.1 Radiation from Accelerated Charges and the Larmor Formula
The total power radiated by a non-relativistic accelerated charged particle in vacuum:

$$P = \frac{\mu_0 q^2 a^2}{6\pi c} = \frac{q^2 a^2}{6\pi \varepsilon_0 c^3}$$

- **Liénard Relativistic Generalization**:
  $$P = \frac{\mu_0 q^2 \gamma^6}{6\pi c} \left( a^2 - \left|\frac{\mathbf{v} \times \mathbf{a}}{c}\right|^2 \right)$$

### 3.2 Propagation in Conductors and Skin Effect
In media with high conductivity $\sigma \gg \omega\varepsilon$, the wave vector becomes complex $k = \beta + i/\delta$:
$$\delta = \sqrt{\frac{2}{\omega \mu \sigma}} \quad \text{(Skin Depth)}$$

### 3.3 Rectangular Waveguides (Dimensions $a \times b$)
- **Cutoff Frequency for $TE_{mn}$ and $TM_{mn}$ Modes**:
  $$\omega_{mn} = c \sqrt{\left(\frac{m\pi}{a}\right)^2 + \left(\frac{n\pi}{b}\right)^2}$$
- **Fundamental $TE_{10}$ Mode ($a > b$)**: Lowest cutoff frequency $\omega_{10} = \frac{\pi c}{a}$, with phase velocity $v_p = \frac{c}{\sqrt{1 - (\omega_{10}/\omega)^2}} > c$ and group velocity $v_g = c \sqrt{1 - (\omega_{10}/\omega)^2} < c$ ($v_p \cdot v_g = c^2$).
