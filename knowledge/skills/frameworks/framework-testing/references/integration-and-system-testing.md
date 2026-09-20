# 🏗️ Integration, System, and Object-Oriented Testing Guide

This guide consolidates integration architectures and system-level testing based on the methodology of **Paul C. Jorgensen** (*Software Testing: A Craftsman's Approach*) and the ISTQB guidelines.

---

## 1. Decomposition-Based Integration Strategies

Traditional integration maps the functional decomposition hierarchy (module tree).

```
         [ Módulo Raiz ]
          /           \
     [ Módulo A ]   [ Módulo B ]
      /        \          \
  [ Mod A1 ]  [ Mod A2 ] [ Mod B1 ]
```

### 1.1. Comparison of Integration Approaches

| Strategy | Direction | Required Artifacts | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- | :--- |
| **Top-Down** | Root $\rightarrow$ Leaves | **Stubs** (substitutes for unimplemented child modules) | Demonstrates high-level flows early; isolates faults at the top. | Excessive stub creation; critical logic at the leaves is tested late. |
| **Bottom-Up** | Leaves $\rightarrow$ Root | **Drivers** (harnesses that invoke the child modules) | Validates critical and utility subsystems first; no stubs. | Root integrated only at the end; user interface deferred. |
| **Sandwich (Hybrid)** | Both directions converging in the middle | Stubs and Drivers | Balances top and bottom validation simultaneously. | Coordination complexity across the development fronts. |
| **Big Bang** | All modules at once | None | Fast for tiny projects. | **Terrible isolability**: Impossible to locate the root cause of failures in a timely way. |

---

## 2. Call Graph-Based Integration

Overcomes the constraints of static decomposition by focusing on the real invocation dependencies of routines at runtime.

### 2.1. Call Graph Integration Methods
- **Pairwise Integration**: For each edge $(A, B)$ in the call graph, test the direct invocation of module $A$ calling $B$. Eliminates the need to integrate the whole tree at once.
- **Neighborhood Integration**: The subgraph containing a central node $N$, all of its immediate predecessors, and its immediate successors is tested as an isolated cluster.

---

## 3. MM-Paths and System-Level Testing (Jorgensen)

An **MM-Path (Method-to-Method Path)** models the interleaved execution of code segments across distinct modules triggered by a call chain.

### 3.1. Formal Definition of MM-Path
An MM-Path is a sequence of decision paths (DD-Paths) that cross method/module boundaries through function invocations and returns.

```
Módulo A                   Módulo B                   Módulo C
┌──────────┐              ┌──────────┐              ┌──────────┐
│ DD-Path 1│──(chama B)──►│ DD-Path 1│──(chama C)──►│ DD-Path 1│
│          │              │          │              │          │
│ DD-Path 2│◄─(retorna)───│ DD-Path 2│◄─(retorna)───│ DD-Path 2│
└──────────┘              └──────────┘              └──────────┘
```

### 3.2. Atomic System Tests (AST)
- They map the end-to-end response of the system triggered by an external input event (port, interface, queue) to the generation of the corresponding observable output.
- An AST is composed of the concatenation of multiple coordinated MM-Paths.

---

## 4. Testing in Object-Oriented Systems (OO Testing)

Object orientation introduces characteristics that challenge traditional procedural testing:

### 4.1. OO Challenges and Mitigations

1. **Encapsulation**:
   - The object's internal state is not directly observable without inspection methods (`getters` or reflection-based inspection).
   - *Mitigation*: Test state transitions through the public methods that make up the class contract.
2. **Inheritance**:
   - Inherited methods with no syntactic change may fail in the context of the subclass's new state (the subtle-context problem).
   - *Mitigation*: Re-run the parent class's test suite on the subclass (Flattening Rule).
3. **Polymorphism and Dynamic Binding**:
   - The call `shape.draw()` may invoke dozens of distinct implementations at runtime.
   - *Mitigation*: Test polymorphism by instantiating the caller with each registered concrete subclass (Dynamic Binding Matrix).

### 4.2. Test Levels in the OO Hierarchy
- **Intra-Method**: Traditional structural testing applied to a single isolated method.
- **Inter-Method (Intra-Class)**: Tests the interaction among the methods of the same class as they operate on shared state (`self` / `this`).
- **Inter-Class (Cluster Testing)**: Tests the collaboration of coupled classes (Mediator, Observer, Factory patterns).
