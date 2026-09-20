---
name: academic-electrical-power-energy-systems
description: "Specializes in Electric Power Systems (EPS), Energy Generation, Transmission and Distribution, Rotating Electrical Machines, and Power Electronics building on Power System Analysis (Grainger, Stevenson), Electric Machinery (Fitzgerald, Kingsley), Power Electronics (Rashid), and ABNT/IEEE/IEC standards. Covers Admittance/Impedance Matrices (Ybus, Zbus), Power Flow (Newton-Raphson, Fast Decoupled), Symmetrical and Asymmetrical Short-Circuit Calculation (Fortescue Symmetrical Components), Digital Power System Protection (ANSI 50/51, 21, 87 Functions and IEC 61850), Synchronous and Induction Machines, Power Transformers, Low/Medium Voltage Electrical Installations (ABNT NBR 5410 and NBR 14039), Power Electronics and Three-Phase Inverters (SVPWM, SiC/GaN Converters), Smart Grids (Microgrids, BESS Storage), and Multiphysics/Electromagnetic Simulation (OpenDSS, FEMM)."
---

# Electric Power Systems, Machines, and Energy (Grainger & Stevenson)

This skill establishes the steady-state and dynamic analysis engineering of high-, medium-, and low-voltage electrical networks, modeling and control of rotating electrical machines, sizing of static power converters, and substation automation under the IEC 61850 standard.

---

## ⚡ 1. Electrical Network Analysis and Power Flow

### 1.1 Matrix Formulation of the Network and Bus Equations
The relationship between injected nodal currents $\mathbf{I}_{bus}$ and complex bus voltages $\mathbf{V}_{bus}$ is governed by the Nodal Admittance Matrix $\mathbf{Y}_{bus}$:

$$\mathbf{I}_{bus} = \mathbf{Y}_{bus} \mathbf{V}_{bus}$$

- **Elements of the $\mathbf{Y}_{bus}$ Matrix**:
  - $Y_{ii} = \sum_{k \in \Omega_i} y_{ik} + y_{sh,i}$ (Sum of all admittances connected to bus $i$)
  - $Y_{ij} = -y_{ij}$ (Negative of the series admittance between buses $i$ and $j$)

### 1.2 Newton-Raphson Algorithm for Power Flow
The active power $P_i$ and reactive power $Q_i$ injection equations at bus $i$ ($V_i = |V_i| e^{j\theta_i}$):

$$P_i = |V_i| \sum_{k=1}^N |V_k| |Y_{ik}| \cos(\theta_i - \theta_k - \gamma_{ik})$$
$$Q_i = |V_i| \sum_{k=1}^N |V_k| |Y_{ik}| \sin(\theta_i - \theta_k - \gamma_{ik})$$

- **Linearized Jacobian Matrix System**:
  $$\begin{bmatrix} \Delta \mathbf{P} \\ \Delta \mathbf{Q} \end{bmatrix} = \begin{bmatrix} \mathbf{J}_1 & \mathbf{J}_2 \\ \mathbf{J}_3 & \mathbf{J}_4 \end{bmatrix} \begin{bmatrix} \Delta \boldsymbol{\theta} \\ \Delta |\mathbf{V}|/|\mathbf{V}| \end{bmatrix} = \begin{bmatrix} \frac{\partial \mathbf{P}}{\partial \boldsymbol{\theta}} & \frac{\partial \mathbf{P}}{\partial |\mathbf{V}|} |\mathbf{V}| \\ \frac{\partial \mathbf{Q}}{\partial \boldsymbol{\theta}} & \frac{\partial \mathbf{Q}}{\partial |\mathbf{V}|} |\mathbf{V}| \end{bmatrix} \begin{bmatrix} \Delta \boldsymbol{\theta} \\ \Delta |\mathbf{V}|/|\mathbf{V}| \end{bmatrix}$$

---

## 🛡️ 2. Short Circuit, Symmetrical Components, and Digital Protection

### 2.1 Fortescue Theorem and Sequence Networks
Any unbalanced three-phase system of voltage/current phasors is decomposed into three decoupled symmetrical systems: Positive ($1$), Negative ($2$), and Zero ($0$) sequence:

$$\begin{bmatrix} \mathbf{V}_a \\ \mathbf{V}_b \\ \mathbf{V}_c \end{bmatrix} = \begin{bmatrix} 1 & 1 & 1 \\ 1 & a^2 & a \\ 1 & a & a^2 \end{bmatrix} \begin{bmatrix} \mathbf{V}_0 \\ \mathbf{V}_1 \\ \mathbf{V}_2 \end{bmatrix}, \quad \text{where } a = e^{j 120^\circ} = -\frac{1}{2} + j\frac{\sqrt{3}}{2}$$

- **Interconnection of Sequence Networks by Fault Type**:
  1. **Symmetrical Three-Phase Fault (3F)**: Only the positive-sequence network acts: $I_{f1} = \frac{V_{th}}{Z_{1,th} + Z_f}$.
  2. **Single Line-to-Ground Fault (1LG)**: Networks in series ($1$, $2$, $0$): $I_{f1} = I_{f2} = I_{f0} = \frac{V_{th}}{Z_{1,th} + Z_{2,th} + Z_{0,th} + 3Z_f}$.
  3. **Line-to-Line Fault (2F)**: Positive and negative networks in parallel ($Z_{1,th} \parallel Z_{2,th}$).
  4. **Double Line-to-Ground Fault (2LG)**: Positive, negative, and zero networks in parallel.

### 2.2 Protection Philosophy and IEC 61850 Standard
```
Principais Funções ANSI de Proteção:
├── ANSI 50/51: Sobrecorrente Instantânea e Temporizada (Curvas IEC/IEEE)
├── ANSI 50N/51N: Sobrecorrente de Neutro / Residual de Terra
├── ANSI 21: Proteção de Distância Mho / Quadrilateral (Zonas Z1: 80-85%, Z2: 120%, Z3 reversa)
├── ANSI 87: Proteção Diferencial Percentual (87T Transformadores com restrição harmônica 2ª/5ª, 87B Barramentos)
└── ANSI 27/59: Subtensão e Sobretensão

Arquitetura de Subestações Digitais (IEC 61850):
├── Process Bus: Tráfego de Sampled Values (SV - IEC 61850-9-2LE a 4800/4000 Hz) e GOOSE (mensagens de trip < 3 ms)
└── Station Bus: Tráfego MMS para Sistemas SCADA e sincronização temporal IEEE 1588 PTP (Precision Time Protocol)
```

---

## 🔄 3. Electrical Machines and Power Transformers

### 3.1 Three-Phase Power Transformers
- **Equivalent Circuit Referred to the Primary**:
  - No-Load Test Parameters: Iron loss resistance $R_c = \frac{V_{1}^2}{P_0}$ and magnetizing reactance $X_m = \frac{V_{1}^2}{Q_0}$.
  - Short-Circuit Test Parameters: Equivalent resistance $R_{eq} = \frac{P_{cc}}{I_{cc}^2}$ and leakage reactance $X_{eq} = \sqrt{Z_{cc}^2 - R_{eq}^2}$.
- **Connection Groups**: Dyn11 (Delta primary, Wye with neutral secondary phase-shifted by $+30^\circ$), YNd1, YNy0.

### 3.2 Synchronous and Induction Machines
- **Salient-Pole Synchronous Generator (Blondel Two-Reaction Theory)**:
  $$P = \frac{E_f V}{X_d} \sin\delta + \frac{V^2 (X_d - X_q)}{2 X_d X_q} \sin(2\delta)$$
  where the second term represents the reluctance torque.
- **Three-Phase Induction Motor (TIM)**:
  - Slip: $s = \frac{n_s - n_r}{n_s}$
  - Electromagnetic Torque Equation (Kloss):
    $$T = \frac{3 R_2' / s}{\omega_s \left[ (R_1 + R_2'/s)^2 + (X_1 + X_2')^2 \right]} V_{1,th}^2$$

---

## 🔌 4. Power Electronics and Three-Phase Inverters (SVPWM)

### 4.1 Space Vector PWM (SVPWM)
In three-phase voltage source inverters (VSI) with 6 IGBT/SiC semiconductor switches, the reference voltage vector $\mathbf{V}_{ref} = V_\alpha + j V_\beta$ is synthesized by combining the two adjacent active vectors ($\mathbf{V}_1 \dots \mathbf{V}_6$) and the null vectors ($\mathbf{V}_0, \mathbf{V}_7$):

$$T_1 = \frac{\sqrt{3} T_s |\mathbf{V}_{ref}|}{V_{dc}} \sin\left( \frac{\pi}{3} - \theta \right), \quad T_2 = \frac{\sqrt{3} T_s |\mathbf{V}_{ref}|}{V_{dc}} \sin(\theta), \quad T_0 = T_s - T_1 - T_2$$

- **Advantage over sinusoidal SPWM**: Raises DC bus utilization by $+15.5\%$ without entering overmodulation ($V_{max,linear} = \frac{V_{dc}}{\sqrt{3}}$ versus $\frac{V_{dc}}{2}$).

---

## 📋 5. Electrical Installations and Regulatory Compliance (LV and MV)

| Regulatory / Technical Standard | Scope of Application | Critical Engineering Requirements |
| :--- | :--- | :--- |
| **ABNT NBR 5410** | Low-Voltage Installations ($\le 1000\text{V AC}$) | Sizing by 6 criteria: Minimum Cross-Section, Ampacity, Voltage Drop ($\le 4\%$), Overload, Short Circuit, and Shock Protection (RCD $\le 30\text{mA}$, BEP Equipotential Bonding). |
| **ABNT NBR 14039** | Medium-Voltage Installations ($1.0\text{kV}$ to $36.2\text{kV}$) | Enclosed and masonry substations, relay-fuse protection coordination, dry-type vs oil-immersed transformers, insulation and dielectric clearances in air. |
| **NR-10** | Safety in Electrical Installations and Services | Electrical Installation Dossier (PIE), Preliminary Risk Analysis (APR), ATPV clothing for Arc Flash protection, Risk and Controlled Zones. |
| **PRODIST Modules 3 and 8 (ANEEL)** | Grid Access and Electric Power Quality (QEE) | Total harmonic distortion limits ($THD_V \le 10\%$, $THD_I$), voltage fluctuation (*Flicker* $P_{st}, P_{lt}$), voltage unbalance, and power factor ($\ge 0.92$). |
