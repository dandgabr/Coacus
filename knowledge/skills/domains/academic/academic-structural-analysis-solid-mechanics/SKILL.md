---
name: academic-structural-analysis-solid-mechanics
description: "Specializes in Solid Mechanics, Matrix Structural Analysis, Finite Element Analysis (FEA), Soil Mechanics, and Geotechnical Engineering building on James M. Gere & Barry J. Goodno (Mechanics of Materials), Aslam Kassimali (Matrix Analysis of Structures), and Braja M. Das (Principles of Geotechnical Engineering). Covers Plane Stress and Strain State (Mohr's Circle, Von Mises and Tresca Yield Criteria), Bending, Shear, and Torsion in Beams, Euler Column Buckling, the Direct Stiffness Method, Finite Element Formulation, Terzaghi's Principle of Effective Stress, Soil Classification (USCS, AASHTO), Permeability and Darcy's Law, Terzaghi's One-Dimensional Consolidation Theory, the Mohr-Coulomb Failure Criterion, Earth Pressure (Rankine/Coulomb), and Bearing Capacity of Shallow and Deep Foundations (Meyerhof, Terzaghi, Hansen)."
---

# Solid Mechanics, Structural Analysis, and Geotechnical Engineering

This skill establishes the mathematical foundations and numerical methods for structural analysis of concrete, steel, and composite elements, combined with the constitutive models of soil mechanics and geotechnics for foundations and retaining structures, grounded in **Gere & Goodno**, **Kassimali**, and **Braja M. Das**.

---

## 🏗️ 1. Solid Mechanics and Stress State

### 1.1 Mohr's Circle and Yield Criteria
- **Principal Stresses ($\sigma_1, \sigma_2, \sigma_3$)**:
  $$\sigma_{1,2} = \frac{\sigma_x + \sigma_y}{2} \pm \sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}, \quad \tau_{max} = \frac{\sigma_1 - \sigma_2}{2}$$
- **Von Mises Yield Criterion (Distortion Energy)**:
  $$\sigma_{vm} = \sqrt{\frac{1}{2} \left[ (\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2 \right]} \le \frac{f_y}{\gamma_m}$$
- **Maximum Shear Stress Criterion (Tresca)**:
  $$\tau_{max} = \frac{\sigma_1 - \sigma_3}{2} \le \frac{f_y}{2 \gamma_m}$$

### 1.2 Euler Column Buckling
Elastic critical buckling load for a column with effective length $K L$:
$$P_{cr} = \frac{\pi^2 E I}{(K L)^2}, \quad \sigma_{cr} = \frac{\pi^2 E}{\lambda^2} \quad \left(\text{where } \lambda = \frac{K L}{r} \text{ is the slenderness ratio}\right)$$

---

## 📐 2. Matrix Structural Analysis and Finite Element Analysis (FEA)

### 2.1 Direct Stiffness Method
For a framed structure with $n$ degrees of freedom:
$$\mathbf{K} \mathbf{u} = \mathbf{F}$$
- **Local Stiffness Matrix of the 2D Beam Element**:
  $$\mathbf{k}_e = \begin{bmatrix}
  \frac{EA}{L} & 0 & 0 & -\frac{EA}{L} & 0 & 0 \\
  0 & \frac{12EI}{L^3} & \frac{6EI}{L^2} & 0 & -\frac{12EI}{L^3} & \frac{6EI}{L^2} \\
  0 & \frac{6EI}{L^2} & \frac{4EI}{L} & 0 & -\frac{6EI}{L^2} & \frac{2EI}{L} \\
  -\frac{EA}{L} & 0 & 0 & \frac{EA}{L} & 0 & 0 \\
  0 & -\frac{12EI}{L^3} & -\frac{6EI}{L^2} & 0 & \frac{12EI}{L^3} & -\frac{6EI}{L^2} \\
  0 & \frac{6EI}{L^2} & \frac{2EI}{L} & 0 & -\frac{6EI}{L^2} & \frac{4EI}{L}
  \end{bmatrix}$$

---

## 🌍 3. Soil Mechanics and Terzaghi's Principle

### 3.1 Principle of Effective Stress
$$\sigma' = \sigma - u$$
where $\sigma$ is the total vertical stress due to the soil's own weight and surcharges, $u$ is the pore-water pressure, and $\sigma'$ is the effective stress that governs shear strength and consolidation.

### 3.2 Shear Strength (Mohr-Coulomb Criterion)
$$\tau_f = c' + \sigma' \tan \phi'$$
where $c'$ is the effective cohesion and $\phi'$ is the effective internal friction angle of the soil.

### 3.3 Terzaghi's One-Dimensional Consolidation Theory
Governing differential equation of excess pore pressure $\bar{u}(z,t)$:
$$\frac{\partial \bar{u}}{\partial t} = c_v \frac{\partial^2 \bar{u}}{\partial z^2}, \quad c_v = \frac{k}{\gamma_w m_v}$$
The total primary consolidation settlement $S_c$ for a normally consolidated soil of thickness $H_0$:
$$S_c = \frac{C_c H_0}{1 + e_0} \log_{10}\left( \frac{\sigma'_0 + \Delta\sigma'}{\sigma'_0} \right)$$

---

## 🏛️ 4. Foundation Geotechnics and Earth Pressure

1. **Earth Pressure (Rankine)**:
   - Active Earth Pressure Coefficient: $K_a = \tan^2\left(45^\circ - \frac{\phi'}{2}\right) = \frac{1 - \sin\phi'}{1 + \sin\phi'}$
   - Passive Earth Pressure Coefficient: $K_p = \tan^2\left(45^\circ + \frac{\phi'}{2}\right) = \frac{1 + \sin\phi'}{1 - \sin\phi'}$
2. **Bearing Capacity of Shallow Foundations (General Terzaghi/Meyerhof Equation)**:
   $$q_{ult} = c' N_c s_c d_c + q N_q s_q d_q + \frac{1}{2} \gamma B N_\gamma s_\gamma d_\gamma$$
   where $N_c, N_q, N_\gamma$ are the dimensionless bearing capacity factors depending exclusively on $\phi'$.
