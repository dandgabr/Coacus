---
name: academic-calculus-differential-equations
description: "Specializes in Differential and Integral Calculus (I to IV), Ordinary Differential Equations (ODEs), Partial Differential Equations (PDEs), Vector Calculus, and Numerical Methods building on Algebra, Topology, Differential Calculus, and Optimization Theory for CS and ML (Jean Gallier, Jocelyn Quaintance), Numerical Algorithms (Justin Solomon), Stewart, and Boyce-DiPrima. Covers Vector Calculus (Gradient, Divergence, Curl, Green's, Stokes', and Gauss Divergence Theorems), Linear and Nonlinear ODEs (Integrating Factor, Variation of Parameters, Laplace Transforms), Classic PDEs (Heat, Wave, and Laplace/Poisson Equations, Fourier Series, Separation of Variables), and Numerical Methods (Euler, RK4, Symplectic Verlet/Leapfrog Integrators, Finite Difference Method FDM, and Finite Element Method FEM)."
---

# Differential and Integral Calculus, ODEs, PDEs, and Numerical Methods

This skill establishes the rigorous toolkit of multivariable calculus, vector calculus, analytical differential equations, and numerical discretization for mathematical physics, system dynamics, signal processing, and computer graphics.

---

## 📐 1. Vector Calculus and Fundamental Integration Theorems

### 1.1 Vector Differential Operators in $\mathbb{R}^3$
Given a scalar field $f(x,y,z)$ and a vector field $\mathbf{F} = [F_x, F_y, F_z]^T$:
- **Gradient**: $\nabla f = \left[ \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z} \right]^T$ (points in the direction of maximum rate of change).
- **Divergence**: $\nabla \cdot \mathbf{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}$ (rate of volumetric expansion per unit time).
- **Curl**: $\nabla \times \mathbf{F} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\ F_x & F_y & F_z \end{vmatrix}$ (measure of infinitesimal circulation).
- **Laplacian**: $\nabla^2 f = \nabla \cdot (\nabla f) = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}$.

### 1.2 Classic Integral Theorems
| Theorem | Integral Formulation | Physical / Geometric Meaning |
| :--- | :--- | :--- |
| **Green's Theorem in the Plane** | $\oint_{\partial D} (L \, dx + M \, dy) = \iint_D \left( \frac{\partial M}{\partial x} - \frac{\partial L}{\partial y} \right) dA$ | Circulation around a closed planar curve equals the curl integrated over the area. |
| **Classical Stokes Theorem** | $\oint_{\partial S} \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot \mathbf{n} \, dS$ | The circulation of $\mathbf{F}$ on the boundary equals the flux of the curl through the surface. |
| **Divergence Theorem (Gauss)** | $\oiint_{\partial V} \mathbf{F} \cdot \mathbf{n} \, dS = \iiint_V (\nabla \cdot \mathbf{F}) \, dV$ | The total net flux of $\mathbf{F}$ leaving a closed volume equals the sum of the internal sources. |

---

## 📈 2. Analytical Ordinary Differential Equations (ODEs)

### 2.1 First-Order Linear ODEs (Integrating Factor)
$$y' + P(x)y = Q(x) \implies \mu(x) = e^{\int P(x) dx} \implies y(x) = \frac{1}{\mu(x)} \left( \int \mu(x) Q(x) dx + C \right)$$

### 2.2 Second-Order Linear ODEs with Constant Coefficients
$$a y'' + b y' + c y = g(x)$$
- **Characteristic Equation**: $a r^2 + b r + c = 0 \implies \Delta = b^2 - 4ac$.
  1. $\Delta > 0$: $y_h(x) = c_1 e^{r_1 x} + c_2 e^{r_2 x}$.
  2. $\Delta = 0$: $y_h(x) = c_1 e^{r x} + c_2 x e^{r x}$.
  3. $\Delta < 0$ ($r = \alpha \pm i \beta$): $y_h(x) = e^{\alpha x} (c_1 \cos \beta x + c_2 \sin \beta x)$.
- **Variation of Parameters Method**: To find the particular solution $y_p(x)$:
  $$y_p(x) = -y_1(x) \int \frac{y_2(x) g(x)}{W(y_1, y_2)(x)} dx + y_2(x) \int \frac{y_1(x) g(x)}{W(y_1, y_2)(x)} dx$$
  where $W(y_1, y_2)(x) = y_1 y_2' - y_2 y_1'$ is the Wronskian determinant.

### 2.3 Laplace Transform for Solving IVPs
$$\mathcal{L}\{f(t)\} = F(s) = \int_0^\infty f(t) e^{-st} dt$$
- $\mathcal{L}\{y'(t)\} = s Y(s) - y(0)$
- $\mathcal{L}\{y''(t)\} = s^2 Y(s) - s y(0) - y'(0)$
- **Convolution Theorem**: $\mathcal{L}^{-1}\{F(s)G(s)\} = (f * g)(t) = \int_0^t f(\tau) g(t - \tau) d\tau$.

---

## 🌊 3. Fundamental Partial Differential Equations (PDEs)

### 3.1 Classification of 2nd-Order PDEs ($A u_{xx} + B u_{xy} + C u_{yy} + \dots = 0$)
- **Hyperbolic ($B^2 - 4AC > 0$)**: Wave Equation $\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$ (propagation and acoustic/electromagnetic waves).
- **Parabolic ($B^2 - 4AC = 0$)**: Heat / Diffusion Equation $\frac{\partial u}{\partial t} = \alpha \nabla^2 u$ (thermal conduction and dissipation).
- **Elliptic ($B^2 - 4AC < 0$)**: Laplace Equation $\nabla^2 u = 0$ / Poisson $\nabla^2 u = f$ (electrostatic potential and incompressible fluids).

### 3.2 Separation of Variables and Fourier Series
For the heat bar equation $u_t = \alpha u_{xx}$ with Dirichlet boundary conditions $u(0,t) = u(L,t) = 0$:
$$u(x, t) = \sum_{n=1}^\infty B_n \sin\left(\frac{n\pi x}{L}\right) e^{-\alpha \left(\frac{n\pi}{L}\right)^2 t}, \quad B_n = \frac{2}{L} \int_0^L f(x) \sin\left(\frac{n\pi x}{L}\right) dx$$

---

## 🧮 4. Numerical Methods for ODEs and PDEs (Solomon)

### 4.1 Classical Fourth-Order Runge-Kutta Method (RK4)
For the IVP $\frac{dy}{dt} = f(t, y), \; y(t_0) = y_0$:
$$y_{n+1} = y_n + \frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4)$$
- $k_1 = f(t_n, y_n)$
- $k_2 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$
- $k_3 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$
- $k_4 = f(t_n + h, y_n + h k_3)$
Local truncation error: $\mathcal{O}(h^5)$; Global error: $\mathcal{O}(h^4)$.

### 4.2 Symplectic Integrators (Verlet and Leapfrog) for Mechanics and Graphics
For Hamiltonian systems $\ddot{\mathbf{x}} = \mathbf{a}(\mathbf{x})$, symplectic integrators conserve mechanical energy and phase-space volume without spurious damping:
- **Velocity Verlet**:
  $$\mathbf{x}_{n+1} = \mathbf{x}_n + \mathbf{v}_n h + \frac{1}{2} \mathbf{a}_n h^2$$
  $$\mathbf{v}_{n+1} = \mathbf{v}_n + \frac{1}{2} (\mathbf{a}_n + \mathbf{a}_{n+1}) h$$

### 4.3 Finite Difference Method (FDM) for PDEs
Approximation of derivatives by central stencil:
$$u_{xx}(x_i, y_j) \approx \frac{u_{i+1, j} - 2u_{i,j} + u_{i-1, j}}{\Delta x^2}$$
$$u_{yy}(x_i, y_j) \approx \frac{u_{i, j+1} - 2u_{i,j} + u_{i, j-1}}{\Delta y^2}$$
- **CFL (Courant-Friedrichs-Lewy) Condition for explicit wave stability**: $C = \frac{c \Delta t}{\Delta x} \le 1$.
