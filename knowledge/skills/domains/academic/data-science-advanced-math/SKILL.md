---
name: data-science-advanced-math
description: "Specializes in Advanced Mathematics, Linear Algebra, Topology, Differential Calculus, and Optimization for Machine Learning and Data Science building on Algebra, Topology, Differential Calculus, and Optimization Theory for CS and ML (Jean Gallier, Jocelyn Quaintance), Numerical Algorithms (Justin Solomon), and Essential Math for Data Science (Thomas Nield). Covers Linear Algebra and Matrix Factorizations (SVD, Cholesky, QR, Moore-Penrose, Eigenvalues), Tensor Calculus and Backpropagation (Jacobians, Hessians, Multivariable Taylor), Convex Optimization and Duality (KKT Conditions, Lagrange Multipliers), First- and Second-Order Numerical Optimizers (SGD, AdamW, Newton-Raphson, BFGS, L-BFGS, Levenberg-Marquardt), Large-Scale Linear Systems (Conjugate Gradient, GMRES), Manifold Topology (Isomap, t-SNE, UMAP), and Bayesian Inference/Regularization (MLE, MAP, Lasso, Ridge, Elastic Net)."
---

# Advanced Mathematics, Algebra, and Optimization for Machine Learning

This skill establishes the rigorous mathematical and computational foundations for statistical modeling, Deep Learning architectures, convex/non-convex optimization, and high-dimensional analysis.

---

## 📐 1. Advanced Linear Algebra and Matrix Factorizations for ML

### 1.1 Singular Value Decomposition (SVD)
For any real matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$:
$$\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T = \sum_{i=1}^r \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
- $\mathbf{U} \in \mathbb{R}^{m \times m}$ and $\mathbf{V} \in \mathbb{R}^{n \times n}$ are orthogonal matrices ($\mathbf{U}^T\mathbf{U} = \mathbf{I}, \mathbf{V}^T\mathbf{V} = \mathbf{I}$).
- $\mathbf{\Sigma} = \text{diag}(\sigma_1, \sigma_2, \dots, \sigma_r, 0, \dots, 0)$ with ordered singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$.
- **Eckart-Young-Mirsky Theorem (Low-Rank Approximation)**:
  The best rank-$k$ approximation with $k < r$ in Frobenius or Spectral norm is:
  $$\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T, \quad \|\mathbf{A} - \mathbf{A}_k\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$

### 1.2 Moore-Penrose Pseudo-Inverse ($\mathbf{A}^+$)
$$\mathbf{A}^+ = \mathbf{V} \mathbf{\Sigma}^+ \mathbf{U}^T$$
Solves linear least squares problems $\min_{\mathbf{x}} \|\mathbf{A}\mathbf{x} - \mathbf{b}\|_2^2$ with the minimum-norm solution $\mathbf{x}^* = \mathbf{A}^+ \mathbf{b}$.

### 1.3 Cholesky and QR Factorizations
- **Cholesky ($\mathbf{A} = \mathbf{L}\mathbf{L}^T$)**: For symmetric positive definite (SPD) matrices, computationally twice as fast as LU decomposition. Essential for Gaussian Processes and MCMC sampling.
- **QR ($\mathbf{A} = \mathbf{Q}\mathbf{R}$)**: Factors into an orthogonal matrix $\mathbf{Q}$ and an upper triangular matrix $\mathbf{R}$, providing maximum numerical stability for regressions.

---

## 📈 2. Multivariable Differential Calculus and Tensor Calculus

### 2.1 Gradient Vector, Jacobian Matrix, and Hessian
Given a scalar field $f: \mathbb{R}^n \to \mathbb{R}$ and a vector function $\mathbf{F}: \mathbb{R}^n \to \mathbb{R}^m$:
- **Gradient Vector**: $\nabla f(\mathbf{x}) = \left[ \frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n} \right]^T \in \mathbb{R}^n$
- **Jacobian Matrix**: $\mathbf{J}_{\mathbf{F}}(\mathbf{x}) = \left[ \frac{\partial F_i}{\partial x_j} \right]_{m \times n} \in \mathbb{R}^{m \times n}$
- **Hessian Matrix (2nd-Order Curvature)**: $\mathbf{H}_f(\mathbf{x}) = \left[ \frac{\partial^2 f}{\partial x_i \partial x_j} \right]_{n \times n} \in \mathbb{R}^{n \times n}$

### 2.2 Second-Order Multivariable Taylor Series
$$f(\mathbf{x} + \Delta\mathbf{x}) \approx f(\mathbf{x}) + \nabla f(\mathbf{x})^T \Delta\mathbf{x} + \frac{1}{2} \Delta\mathbf{x}^T \mathbf{H}_f(\mathbf{x}) \Delta\mathbf{x}$$

### 2.3 Tensor Chain Rule and Backpropagation
For composite functions in computational graphs:
$$\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \left( \frac{\partial \mathbf{z}^{(l)}}{\partial \mathbf{W}^{(l)}} \right)^T \frac{\partial L}{\partial \mathbf{z}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{a}^{(l-1)})^T \quad \text{where } \boldsymbol{\delta}^{(l)} = (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)})$$

---

## 🎯 3. Convex Optimization and Duality Theory (Gallier & Quaintance)

### 3.1 Standard Constrained Optimization Problem
$$\min_{\mathbf{x} \in \mathbb{R}^n} f_0(\mathbf{x}) \quad \text{subject to } f_i(\mathbf{x}) \le 0 \; (i=1,\dots,m), \quad h_j(\mathbf{x}) = 0 \; (j=1,\dots,p)$$

### 3.2 Karush-Kuhn-Tucker (KKT) Conditions
If the problem is convex and satisfies the constraint qualification condition (Slater's condition), the following conditions are necessary and sufficient for optimality $(\mathbf{x}^*, \boldsymbol{\lambda}^*, \boldsymbol{\nu}^*)$:
1. **Stationarity**: $\nabla f_0(\mathbf{x}^*) + \sum_{i=1}^m \lambda_i^* \nabla f_i(\mathbf{x}^*) + \sum_{j=1}^p \nu_j^* \nabla h_j(\mathbf{x}^*) = \mathbf{0}$
2. **Primal Feasibility**: $f_i(\mathbf{x}^*) \le 0 \; (\forall i)$ and $h_j(\mathbf{x}^*) = 0 \; (\forall j)$
3. **Dual Feasibility**: $\lambda_i^* \ge 0 \; (\forall i=1,\dots,m)$
4. **Complementary Slackness**: $\lambda_i^* f_i(\mathbf{x}^*) = 0 \; (\forall i=1,\dots,m)$

---

## ⚡ 4. First- and Second-Order Numerical Optimizers

### 4.1 Adam / AdamW Family (First Order with Adaptive Moments)
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t, \quad \mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2$$
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$
- **AdamW (Decoupled Weight Decay)**:
  $$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \left( \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} + \lambda \boldsymbol{\theta}_t \right)$$

### 4.2 Second-Order and Quasi-Newton Methods (BFGS and L-BFGS)
- **Pure Newton Method**: $\Delta\mathbf{x} = - \mathbf{H}_f^{-1}(\mathbf{x}) \nabla f(\mathbf{x})$ (prohibitive $\mathcal{O}(n^3)$ cost for neural networks).
- **L-BFGS (Limited-memory BFGS)**: Keeps only the last $m$ displacement vectors $\mathbf{s}_k = \mathbf{x}_{k+1} - \mathbf{x}_k$ and gradient differences $\mathbf{y}_k = \mathbf{g}_{k+1} - \mathbf{g}_k$, computing the descent direction in $\mathcal{O}(mn)$ time and $\mathcal{O}(mn)$ space.

---

## 🌐 5. Iterative Methods for Large-Scale Linear Systems (Solomon)

### 5.1 Conjugate Gradient (CG) Method
Solves $\mathbf{A}\mathbf{x} = \mathbf{b}$ for symmetric positive definite (SPD) matrices in at most $n$ iterations, generating $\mathbf{A}$-orthogonal directions ($\mathbf{p}_i^T \mathbf{A} \mathbf{p}_j = 0$ for $i \ne j$):
$$\alpha_k = \frac{\mathbf{r}_k^T \mathbf{r}_k}{\mathbf{p}_k^T \mathbf{A} \mathbf{p}_k}, \quad \mathbf{x}_{k+1} = \mathbf{x}_k + \alpha_k \mathbf{p}_k, \quad \mathbf{r}_{k+1} = \mathbf{r}_k - \alpha_k \mathbf{A} \mathbf{p}_k$$
$$\beta_k = \frac{\mathbf{r}_{k+1}^T \mathbf{r}_{k+1}}{\mathbf{r}_k^T \mathbf{r}_k}, \quad \mathbf{p}_{k+1} = \mathbf{r}_{k+1} + \beta_k \mathbf{p}_k$$

---

## 🗺️ 6. Topology, Manifolds, and Non-Linear Dimensionality Reduction

### 6.1 Manifold Learning
- **Isomap**: Preserves geodesic distances computed on $k$-nearest-neighbor ($k$-NN) graphs via Dijkstra + Classical Multidimensional Scaling (MDS).
- **t-SNE (t-Distributed Stochastic Neighbor Embedding)**: Models neighborhood probabilities in the high-dimensional space with a Gaussian distribution and in the low-dimensional space with a Student's t-distribution (1 degree of freedom), minimizing the Kullback-Leibler divergence:
  $$\text{KL}(P \parallel Q) = \sum_i \sum_j p_{j|i} \log \frac{p_{j|i}}{q_{j|i}}$$
- **UMAP (Uniform Manifold Approximation and Projection)**: Based on Riemannian geometry and algebraic topology (Fuzzy Simplicial Sets), guaranteeing preservation of both local and global structure.

---

## 🎲 7. Statistical Inference and Regularization

### 7.1 L1, L2, and Elastic Net Regularization
$$\mathcal{L}_{\text{ElasticNet}}(\mathbf{w}) = \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \left( \alpha \|\mathbf{w}\|_1 + \frac{1 - \alpha}{2} \|\mathbf{w}\|_2^2 \right)$$
- **L1 (Lasso, $\alpha=1$)**: Promotes sparsity by driving exact weights to zero due to the corners of the $L_1$ norm polytope.
- **L2 (Ridge, $\alpha=0$)**: Prevents multicollinearity and smooths the coefficient norm.
