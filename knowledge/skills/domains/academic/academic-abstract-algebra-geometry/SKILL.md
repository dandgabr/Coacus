---
name: academic-abstract-algebra-geometry
description: "Specializes in Abstract Algebra, Field and Galois Theory, Advanced Linear Algebra, and Differential Geometry building on Algebra (Serge Lang), Abstract Algebra (Dummit & Foote), Algebra, Topology, Differential Calculus, and Optimization Theory for CS and ML (Jean Gallier, Jocelyn Quaintance), and Differential Geometry of Curves and Surfaces (do Carmo). Covers Group Theory (Normal Subgroups, Noether Isomorphism Theorems, Sylow Theorems), Ring and Ideal Theory (PIDs, UFDs, Euclidean Domains), Field Theory and Galois Theory (Algebraic Extensions, Finite Galois Fields GF(p^n), Automorphisms, Abel-Ruffini Solvability by Radicals), Hilbert Spaces and Quadratic Forms, the Spectral Theorem and Jordan Decomposition, Differential Geometry of Curves and Surfaces (Frenet-Serret Frame, First and Second Fundamental Forms, Gaussian Curvature, Gauss-Bonnet Theorem), Differentiable Manifolds, and the General Stokes Theorem."
---

# Abstract Algebra, Galois Theory, and Differential Geometry (Lang & do Carmo)

This skill provides the axiomatic rigor, structural algebraic formalism, and differential-geometric toolkit for pure mathematics, mathematical physics, algebraic cryptography, theoretical computing, robotics, and manifold learning.

---

## 🏛️ 1. Abstract Algebra: Groups, Rings, and Ideals

### 1.1 Group Theory and Fundamental Theorems
- **Normal Subgroups and Quotient Groups**: $N \triangleleft G \iff gNg^{-1} = N, \; \forall g \in G$. The set of cosets $G/N$ forms a well-defined group.
- **First Isomorphism Theorem (Noether)**: For any group homomorphism $\phi: G \to H$, $\ker(\phi) \triangleleft G$ and:
  $$G / \ker(\phi) \cong \text{Im}(\phi)$$
- **Lagrange's Theorem**: For a finite group $G$ and subgroup $H \le G$, the order $|H|$ divides $|G|$, with $[G:H] = |G|/|H|$.
- **Sylow Theorems**: For a finite group $G$ of order $|G| = p^k m$ with $\gcd(p, m) = 1$:
  1. $G$ contains at least one subgroup of order $p^k$ (a Sylow $p$-subgroup).
  2. All Sylow $p$-subgroups are conjugate to one another.
  3. The number $n_p$ of Sylow $p$-subgroups satisfies $n_p \equiv 1 \pmod p$ and $n_p$ divides $m$.

### 1.2 Rings, Ideals, and Factorization Domains
- **Hierarchy of Commutative Rings**:
  $$\text{Fields} \subset \text{Euclidean Domains (ED)} \subset \text{Principal Ideal Domains (PID)} \subset \text{Unique Factorization Domains (UFD)} \subset \text{Integral Domains}$$
- **Prime and Maximal Ideals**: In a commutative ring $R$ with unity, an ideal $I$ is prime if and only if $R/I$ is an integral domain; $I$ is maximal if and only if $R/I$ is a **field**.

---

## 🔬 2. Field Theory and Galois Theory

### 2.1 Field Extensions and Finite Fields
- **Extension Degree $[E:F]$**: The dimension of $E$ as a vector space over $F$. If $F \subseteq K \subseteq E$, then $[E:F] = [E:K] \cdot [K:F]$ (Tower Theorem).
- **Splitting Fields**: The smallest extension $E/F$ containing every root of a polynomial $f(x) \in F[x]$.
- **Finite Galois Fields $\mathbb{F}_{p^n} = GF(p^n)$**: Existence and uniqueness up to isomorphism for any prime $p$ and integer $n \ge 1$, corresponding to the splitting field of $x^{p^n} - x$.

### 2.2 Fundamental Theorem of Galois Theory and the Abel-Ruffini Theorem
- A finite extension $E/F$ is **Galois** if it is normal and separable ($\text{Gal}(E/F) = \text{Aut}(E/F)$ with $|\text{Gal}(E/F)| = [E:F]$).
- **Galois Correspondence**: There is an inclusion-reversing bijection between intermediate subfields $F \subseteq K \subseteq E$ and subgroups $H \le \text{Gal}(E/F)$ given by $K = E^H$ and $H = \text{Gal}(E/K)$.
- **Abel-Ruffini Theorem**: Polynomial equations of degree $n \ge 5$ are not solvable by radicals in general, because the symmetric group $S_n$ is not a solvable group for $n \ge 5$ (the alternating subgroup $A_n$ is simple for $n \ge 5$).

---

## 🌐 3. Advanced Linear Algebra and the Spectral Theorem

### 3.1 Hilbert Spaces and Quadratic Forms
- **Hilbert Space**: A vector space equipped with an inner product $\langle \mathbf{u}, \mathbf{v} \rangle$ that is complete under the metric induced by the norm $\|\mathbf{u}\| = \sqrt{\langle \mathbf{u}, \mathbf{u} \rangle}$.
- **Spectral Theorem for Self-Adjoint (Hermitian) Operators**: Every self-adjoint linear operator $T: V \to V$ admits an orthonormal basis of eigenvectors associated with purely real eigenvalues:
  $$T = \sum_{i=1}^n \lambda_i \mathbf{v}_i \mathbf{v}_i^\dagger$$
- **Jordan Canonical Form**: Any linear operator over an algebraically closed field ($\mathbb{C}$) decomposes into Jordan blocks $J_k(\lambda) = \lambda \mathbf{I} + \mathbf{N}$.

---

## 📐 4. Differential Geometry of Curves and Surfaces (do Carmo)

### 4.1 Frenet-Serret Frame for Curves in $\mathbb{R}^3$
For a curve $\boldsymbol{\alpha}(s)$ parametrized by arc length ($s$):
$$\begin{bmatrix} \mathbf{T}' \\ \mathbf{N}' \\ \mathbf{B}' \end{bmatrix} = \begin{bmatrix} 0 & \kappa(s) & 0 \\ -\kappa(s) & 0 & \tau(s) \\ 0 & -\tau(s) & 0 \end{bmatrix} \begin{bmatrix} \mathbf{T} \\ \mathbf{N} \\ \mathbf{B} \end{bmatrix}$$

### 4.2 Fundamental Forms and Gaussian and Mean Curvatures
For a regular parametrized surface $\mathbf{x}(u, v)$:
- **First Fundamental Form (Metric)**: $I = E \, du^2 + 2F \, du \, dv + G \, dv^2$.
- **Second Fundamental Form**: $II = e \, du^2 + 2f \, du \, dv + g \, dv^2$.
- **Intrinsic Gaussian Curvature (Gauss's Theorema Egregium)**:
  $$K = \frac{eg - f^2}{EG - F^2}$$
- **Global Gauss-Bonnet Theorem**:
  $$\iint_M K \, dA + \int_{\partial M} \kappa_g \, ds = 2\pi \chi(M) = 2\pi (2 - 2g)$$
  where $\chi(M)$ is the Euler characteristic and $g$ is the genus of the surface.

---

## 🌌 5. Differentiable Manifolds and the General Stokes Theorem

- **Tangent Space and Differential Forms**: $\omega \in \Omega^k(M)$ with exterior derivative $d: \Omega^k(M) \to \Omega^{k+1}(M)$ such that $d^2 = 0$.
- **General Stokes Theorem**:
  $$\int_{\partial M} \omega = \int_M d\omega$$
  It unifies the Fundamental Theorem of Calculus, Green's theorem, the Divergence theorem, and the classical Stokes theorem.
