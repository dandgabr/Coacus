---
name: academic-control-systems-theory
description: "Specializes in Classical and Modern Control Theory, Industrial Robotics, and Automation building on Katsuhiko Ogata (Modern Control Engineering), John J. Craig (Introduction to Robotics Mechanics and Control), and the IEC 61131-3 standard. Covers Root Locus, Bode/Nyquist Diagrams, PID with Anti-windup, State Space, Kalman Controllability and Observability, the Linear Quadratic Regulator (LQR with the Riccati ARE), Luenberger Observers, ZOH Discretization in the Z-Plane, Deadbeat Control, Model Predictive Control (MPC), the Kalman Filter, Forward/Inverse Kinematics (Denavit-Hartenberg), the Robotic Jacobian, Lagrange-Euler Dynamics, ROS 2, SLAM, and PLC Automation (Structured Text ST, Ladder LD, SCADA, Modbus, Profinet, OPC-UA)."
---

# Control Theory, Industrial Robotics, and Automation (IEC 61131-3)

This skill establishes the theoretical foundation, rigorous mathematical formulations, and practical engineering applications of control, dynamic system modeling, manipulator and mobile robotics, and industrial process automation.

---

## 🎛️ 1. Classical Control in the Frequency Domain

### 1.1 PID with Anti-Windup (Clamping and Back-Calculation)
The continuous PID controller law in parallel form:
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) \, d\tau + K_d \frac{de(t)}{dt}$$

```
        ┌─────────────────────────────────────────────────────────────┐
        │                 Saturação do Atuador u_sat                  │
        └──────────────────────────────┬──────────────────────────────┘
                                       │ u_sat - u (Erro de Saturação)
                                       ▼
    e(t) ───[ Ki ]───(+)───[ 1/s ]───(+)───[ u(t) ]───[ Saturação ]───> u_sat(t)
                      ▲               │
                      └───[ 1/Tt ]────┘ (Realimentação Anti-Windup)
```

### 1.2 Nyquist Stability Criterion
The number of closed-loop poles in the right half-plane ($Z$) is given by $Z = N + P$, where $P$ is the number of open-loop poles in the right half-plane and $N$ is the number of clockwise encirclements of the critical point $(-1 + j0)$ by the Nyquist diagram $G(s)H(s)$.

---

## 🚀 2. Modern State-Space Control and Optimal Control

### 2.1 Continuous Model and Controllability and Observability Matrices
$$\dot{\mathbf{x}}(t) = \mathbf{A}\mathbf{x}(t) + \mathbf{B}\mathbf{u}(t), \quad \mathbf{y}(t) = \mathbf{C}\mathbf{x}(t) + \mathbf{D}\mathbf{u}(t)$$
- **Controllability**: $\mathcal{C} = \begin{bmatrix} \mathbf{B} & \mathbf{AB} & \mathbf{A}^2\mathbf{B} & \cdots & \mathbf{A}^{n-1}\mathbf{B} \end{bmatrix}, \quad \text{rank}(\mathcal{C}) = n$.
- **Observability**: $\mathcal{O} = \begin{bmatrix} \mathbf{C}^T & (\mathbf{CA})^T & (\mathbf{CA}^2)^T & \cdots & (\mathbf{CA}^{n-1})^T \end{bmatrix}^T, \quad \text{rank}(\mathcal{O}) = n$.

### 2.2 Linear Quadratic Regulator (LQR)
Minimizes the quadratic cost functional:
$$J = \int_0^\infty \left( \mathbf{x}^T \mathbf{Q} \mathbf{x} + \mathbf{u}^T \mathbf{R} \mathbf{u} \right) dt \implies \mathbf{u}(t) = -\mathbf{K}\mathbf{x}(t), \quad \mathbf{K} = \mathbf{R}^{-1} \mathbf{B}^T \mathbf{P}$$
where $\mathbf{P} = \mathbf{P}^T > 0$ is the unique solution of the **Algebraic Riccati Equation (ARE)**:
$$\mathbf{A}^T \mathbf{P} + \mathbf{P} \mathbf{A} - \mathbf{P} \mathbf{B} \mathbf{R}^{-1} \mathbf{B}^T \mathbf{P} + \mathbf{Q} = \mathbf{0}$$

### 2.3 Luenberger State Observer & Kalman Filter
- **Luenberger Observer**: $\dot{\hat{\mathbf{x}}} = \mathbf{A}\hat{\mathbf{x}} + \mathbf{B}\mathbf{u} + \mathbf{L}(\mathbf{y} - \mathbf{C}\hat{\mathbf{x}})$.
- **Steady-State Kalman Filter**: Gain $\mathbf{L} = \mathbf{P}_e \mathbf{C}^T \mathbf{R}_v^{-1}$, where $\mathbf{P}_e$ solves the error Riccati equation with process noise $\mathbf{Q}_w$ and measurement noise $\mathbf{R}_v$.

---

## 🦾 3. Industrial Robotics, Manipulators, and ROS 2

### 3.1 Denavit-Hartenberg (DH) Homogeneous Transformations
The transformation matrix between consecutive links $^{i-1}\mathbf{T}_i$:
$$^{i-1}\mathbf{T}_i = \begin{bmatrix}
\cos\theta_i & -\sin\theta_i\cos\alpha_i & \sin\theta_i\sin\alpha_i & a_i\cos\theta_i \\
\sin\theta_i & \cos\theta_i\cos\alpha_i & -\cos\theta_i\sin\alpha_i & a_i\sin\theta_i \\
0 & \sin\alpha_i & \cos\alpha_i & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}$$

### 3.2 Lagrange-Euler Dynamics and the Robotic Jacobian
- **Joint Dynamic Equation**:
  $$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \boldsymbol{\tau}$$
- **Cartesian End-Effector Velocity**: $\mathbf{v} = \mathbf{J}(\mathbf{q})\dot{\mathbf{q}}$. Kinematic singularities occur when $\det(\mathbf{J}(\mathbf{q})) = 0$.

---

## 🏭 4. Industrial Automation, PLCs (IEC 61131-3), and SCADA Systems

### 4.1 Function Block in Structured Text (ST - IEC 61131-3)
```iecst
// Bloco Funcional de Controle de Processo com Intertravamento de Segurança
FUNCTION_BLOCK FB_ProcessControl
VAR_INPUT
    bAutoMode     : BOOL;
    rProcessVar   : REAL;
    rSetPoint     : REAL;
    rTolerance    : REAL;
    bEmergencyStop: BOOL;
END_VAR
VAR_OUTPUT
    bActuatorOn   : BOOL;
    bHighAlarm    : BOOL;
    bLowAlarm     : BOOL;
END_VAR

IF bEmergencyStop THEN
    bActuatorOn := FALSE;
    bHighAlarm  := TRUE;
ELSIF bAutoMode THEN
    IF rProcessVar < (rSetPoint - rTolerance) THEN
        bActuatorOn := TRUE;
    ELSIF rProcessVar > (rSetPoint + rTolerance) THEN
        bActuatorOn := FALSE;
    END_IF;
    bHighAlarm := rProcessVar > (rSetPoint + (2.0 * rTolerance));
    bLowAlarm  := rProcessVar < (rSetPoint - (2.0 * rTolerance));
ELSE
    bActuatorOn := FALSE;
END_IF;
END_FUNCTION_BLOCK
```

### 4.2 Industrial Protocols and Networks
- **Modbus RTU/TCP**: Mapping of Coils (`0xxxx`), Discrete Inputs (`1xxxx`), Input Registers (`3xxxx`), and Holding Registers (`4xxxx`).
- **OPC-UA (Open Platform Communications Unified Architecture)**: Object-oriented client-server communication with TLS encryption and X.509 certificates for real-time telemetry with SCADA and MES systems.
- **Profinet / EtherCAT**: Deterministic industrial Ethernet buses with scan-cycle *jitter* in the microsecond range.
