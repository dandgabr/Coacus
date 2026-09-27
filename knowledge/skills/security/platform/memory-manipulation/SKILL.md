---
name: "memory-manipulation"
description: "Acts as a specialist in memory manipulation and low-level security, covering dynamic allocation, pointer management, vulnerabilities (buffer overflows, UAF, double free), offensive techniques (heap grooming, ROP), and modern mitigations (MTE, CFI, ASan)."
metadata:
  type: offensive
  phase: exploitation
  tools: [pwntools, gdb-gef, pwndbg, radare2, ropper, ROPgadget, one_gadget, angr, WinDbg, IDA]
  mitre: [T1203, T1068, T1211, T1212, T1055]
---

# AI Skill: Memory Manipulation and Security

This skill equips the AI agent to act as a low-level specialist in memory management, debugging, auditing, and security. It covers the main memory manipulation techniques, classic and modern vulnerabilities, offensive exploitation vectors, and defense mechanisms at the compiler, operating system, and hardware levels.

---

## 🎯 Skill Objective

Guide the agent in identifying, fixing, and preventing security flaws and memory management bugs in low-level languages and compiled systems (especially C, C++, Assembly, Rust, and Go), ensuring software robustness against memory corruption attacks through a scientific, evidence-based approach.

## 🛠️ Instructions for the AI

1. **Activation Context**:
   - Activate this skill whenever working with C/C++, Rust (unsafe), or Assembly code, or when analyzing segmentation faults (segfaults), memory leaks, and memory corruption vulnerabilities.
   
2. **Step-by-Step Execution (Finding Lifecycle)**:
   - **Step 1 (Static Analysis/Taint Analysis)**: Trace user-controlled data paths (sources) to critical memory destinations (sinks). Inspect the pointer lifecycle and buffer boundaries.
   - **Step 2 (Crash and Root Cause Verification)**: When analyzing a crash, use deterministic record-and-replay (for example, `rr`) to step back to the exact instruction that corrupted memory.
   - **Step 3 (Mitigation Mapping)**: Do not make static assumptions. Test the flaw by rebuilding the execution scenario under different compilation profiles (*Permissive*, *Distro*, *Hardened*) to determine the real feasibility of exploitation.
   - **Step 4 (Defense and Hardening)**: Formulate mitigations applied to the code (logic fixes) and to compilation (security flags, ASan/MSan/UBSan sanitizers).

---

## 🧠 Fundamental Memory Concepts

To manipulate or debug memory effectively, the agent must understand how a process organizes its Virtual Address Space:

1. **Stack**:
   - Managed automatically by the compiler.
   - Stores local variables, function parameters, and return addresses.
   - Grows downward (toward lower addresses on the x86/x64 architecture).
   - Allocations are fast, but strictly local in scope (LIFO).

2. **Heap**:
   - Managed dynamically by the programmer at runtime through calls such as `malloc()`, `calloc()`, `realloc()`, `free()`, or the `new`/`delete` operators.
   - Stores long-lived data whose size is not known at compile time.
   - Heap managers (for example, *ptmalloc* in glibc, *jemalloc*, *Segment Heap* on Windows) organize free memory into lists (bins, fastbins, tcache) for fast reuse.

3. **Static Segments (Data, BSS, and Text)**:
   - **Text**: Contains machine-code instructions (usually read-only and executable).
   - **Data**: Initialized global and static variables.
   - **BSS**: Uninitialized global and static variables (zeroed at startup).

4. **Pointer Arithmetic**:
   - Direct manipulation of memory addresses. Pointer increments depend on the base type (for example, `char* ptr` advances 1 byte, whereas `int* ptr` advances 4 bytes on most 32/64-bit systems).

---

## 🗺️ Exploitation Techniques and Mapping Table

| Technique | MITRE ATT&CK | CWE | Mitigations Bypassed/Targets | Tools |
| :--- | :--- | :--- | :--- | :--- |
| **Stack Overflow -> ROP** | T1203 | CWE-121 | Bypasses DEP/NX using *gadgets* in memory | `pwntools`, `ropper`, `one_gadget` |
| **Ret2csu / SROP** | T1203 | CWE-121 | Bypasses scarcity of register *gadgets* | `pwntools`, `ROPgadget` |
| **Tcache/Fastbin Poisoning** | T1203 | CWE-416 | Heap metadata targets (glibc) | `pwndbg`, `gdb-gef` |
| **Safe-Linking Bypass** | T1203 | CWE-416 | Heap pointer obfuscation (glibc) | Custom XOR Scripts |
| **House of Orange / Einherjar** | T1203 | CWE-415 | Heap exploitation without direct `free()` calls | `gdb-gef` |
| **FSOP (File Structure Oriented)** | T1203 | CWE-787 | Manipulation of `_IO_FILE` structures (glibc) | `pwndbg` |
| **Format String Arbitrary Write** | T1203 | CWE-134 | Arbitrary read and write through `%n` specifiers | `pwntools` |
| **Type Confusion (V8 JIT)** | T1203 | CWE-843 | Sandbox escapes in modern browsers | `d8`, `Ghidra` |

---

## ⚠️ Primary Memory Problems and Vulnerabilities

### 1. Stack-Based Buffer Overflow

- **What It Is**: A write beyond the bounds of a local array on the stack, overwriting control metadata.
- **Impact**: Overwrites the function return address to divert the execution flow.

### 2. Heap Overflow / Heap Corruption

- **What It Is**: A write beyond the bounds of a buffer allocated dynamically on the heap.
- **Impact**: Overwrites neighboring chunk metadata, allowing free-write pointers to be redirected (*arbitrary write*).

### 3. Use-After-Free (UAF)

- **What It Is**: Using a pointer after the associated memory block has been released through `free()`.
- **Impact**: Allows reading or replacing new object structures allocated at the same address (for example, vtables).

### 4. Double Free

- **What It Is**: Calling `free()` on the same address more than once without intermediate allocations.
- **Impact**: Corrupts the allocator's free-list structure, allowing overlapping buffers to be returned in future allocations.

### 5. Integer Overflow / Underflow

- **What It Is**: Arithmetic operations that exceed the maximum/minimum value supported by the numeric type.
- **Impact**: Often results in very small allocations that subsequently overflow during data transfers.

### 6. Format String Vulnerability

- **What It Is**: Passing unsanitized user input directly to format arguments (for example, `printf(user_input)`).
- **Impact**: Allows arbitrary reading (using `%p`, `%x`) and writing to memory addresses (using `%n`).

### 7. Out-of-Bounds Read

- **What It Is**: The program reads data beyond the established buffer boundary.
- **Impact**: Leaks information in memory (such as cryptographic keys or addresses used to bypass ASLR).

### 8. Memory Leaks

- **What It Is**: Repeated heap allocations without a corresponding release.
- **Impact**: Progressive RAM exhaustion, leading to system hang or termination by the OOM killer.

### 9. Type Confusion

- **What It Is**: Allocated memory interpreted under an incompatible type at access time.
- **Impact**: Allows tampering with internal function pointers or virtual method tables.

### 10. Memory Race Conditions (TOCTOU / Race Conditions)

- **What It Is**: Unsynchronized access to shared data under multithreading, where memory changes between the logical check (*time-of-check*) and its actual use (*time-of-use*).
- **Impact**: Authentication bypasses and corruption of critical variables.

---

## 🧪 Empirical Validation Pipeline (Crash-to-Exploitability)

To analyze memory corruption vulnerabilities rigorously, follow this validation protocol:

### 1. Recording and Replay (Root Cause)

Use deterministic execution recording tools, such as **`rr`** on Linux:

- Record the crash: `rr record ./executavel < payload`
- Replay and debug in reverse: `rr replay`
- Step back to the exact write instruction that corrupted the pointer or register using reverse *hardware watchpoints*.

### 2. Reachability Validation

- Compile the application with code-coverage instrumentation (such as `gcov`/`lcov` or Clang profile flags).
- Make sure to document physical and coverage evidence that the exploit path actually reaches and passes through the affected line of code before labeling a flaw as confirmed.

### 3. Empirical Mitigation Matrix

Compile the proof of concept under different profiles to gauge security effectiveness:

| Profile | Objective | Critical Compilation Flags |
| :--- | :--- | :--- |
| **Permissive** | Is the basic bug exploitable? | `-fno-stack-protector -z execstack -no-pie -Wl,-z,norelro` |
| **Distro** | Exploitation in a standard environment | `-D_FORTIFY_SOURCE=2 -fstack-protector-strong -fPIE -pie -Wl,-z,relro` |
| **Hardened** | Resilience under strict protections | `-D_FORTIFY_SOURCE=3 -fstack-protector-all -pie -Wl,-z,now -fsanitize=safe-stack` |
| **Sanitized** | Behavior under dynamic analysis | `-fsanitize=address,undefined -fno-omit-frame-pointer` |

---

## 🛡️ Modern Mitigations and Defenses

### 1. Hardware-Based Protections

- **Memory Tagging Extension (MTE / ARMv8.5+)**: Physical validation of keys (*tags*) associated with pointers, raising immediate exceptions on a mismatch.
- **Pointer Authentication (PAC)**: Integrity cryptography applied to control pointers and function return addresses.
- **Control-flow Enforcement Technology (CET / Intel & AMD)**: Hardware-implemented shadow stacks for ROP verification.

### 2. Software- and Compiler-Based Protections

- **ASLR (Address Space Layout Randomization)**: Randomization of base load addresses.
- **DEP / NX (No-Execute)**: Blocks instruction execution in data segments (stack and heap).
- **Stack Canaries**: Random guard values verified before function returns.
- **CFI (Control Flow Integrity)**: Runtime validation of legitimate indirect jump and control-flow targets.

### 3. Kernel Space Protections (SMEP & SMAP)

- **SMEP (Supervisor Mode Execution Prevention)**: Prevents the kernel from executing user-space code.
- **SMAP (Supervisor Mode Access Prevention)**: Prevents kernel read/write access to user-page data, mitigating control-flow hijacking in local privilege escalation exploits.

---

## 🧬 C++ Object Model, Lifetime and Allocation (Roy)

A rigorous mental model of memory is the precondition for both secure and high-performance code.

### Object model, alignment and lifetime
- A **byte** is the smallest addressable unit (at least 8 bits, not necessarily an octet); an **object** has an address, non-zero storage, a lifetime, a type and a storage duration (`automatic`, `static`, `thread_local`). Functions have addresses but **are not objects** (`std::is_object_v`).
- **Alignment** must be a power of 2; violating it is undefined behavior. `alignof(T)` gives natural alignment; `alignas` raises (never lowers) it. Composite alignment is the worst member alignment; `sizeof == alignof` does not generalize to composites because of padding. Overaligned types need `operator new(size_t, std::align_val_t)`; plain `new` only guarantees `std::max_align_t`.
- Lifetime control: `std::memcpy`, `std::bit_cast` (C++20), and `std::start_lifetime_as`/`std::start_lifetime_as_array` (C++23). Reading a **non-active union member is UB**; `std::launder()` is an optimization barrier for type-punned pointers and should be used sparingly.
- **UB vs IFNDR**: compilers optimize *around* undefined behavior (deleting branches and loops); ODR violations are IFNDR.

### Value semantics and exception safety
- Copy-and-swap is the safe assignment idiom; move constructors/assignment are `noexcept`. `std::move` **does not move** — it is a cast marking an object movable; forward with `std::forward<Args>(args)...`.
- Destructors are implicitly `noexcept`; throwing during unwinding calls `std::terminate()`. Make functions exception-safe and exception-neutral (bare `throw;` re-throws).

### Smart pointers and the ownership trap
- `std::make_unique<T>(args...)` avoids ownerless resources; two `new` calls in one constructor can interleave and leak on throw.
- `std::make_shared<T>(args)` co-locates object and control block in one allocation. `std::shared_ptr` cycles leak — break them with `std::weak_ptr` (`if (auto sp = w.lock()) { ... }`), and return `weak_ptr` from caches.
- Polymorphic deletion requires `virtual ~Base() = default`.

### Overloading allocation operators
Overload the full group (`operator new/new[]/delete/delete[]`); the sized form `operator delete(void*, std::size_t)` (C++14) and `std::destroying_delete_t` (C++20) let a class own finalization and deallocation. `new X` allocates **and** constructs; a throwing constructor triggers the matching `operator delete`. Placement `new` drives memory-mapped hardware regions. A leak detector must over-allocate by `sizeof(std::max_align_t)` and return `static_cast<std::max_align_t*>(p) + 1` — hiding a size header of the wrong width causes misalignment and crashes.

### Arenas, PMR and deferred reclamation
- **Arena / bump allocation**: allocate by pointer bump, deallocate as a no-op, free wholesale — deterministic and low-fragmentation; a size-bucketed variant adds `std::mutex` and sequential blocks.
- **Deferred reclamation** separates finalization (destructor) from reclamation (free).
- **Allocators** trade *objects*, not bytes, and expose `construct`/`destroy`/`rebind`; `std::allocator_traits<A>` wraps them statically. C++17 **PMR** (`std::pmr::memory_resource`, `polymorphic_allocator<T>`, `monotonic_buffer_resource`, `synchronized_pool_resource`, `new_delete_resource`) lets containers carry a runtime resource; note `std::pmr::vector` is a distinct type with no implicit copy.
- C++11-and-later **value types** (`std::array`, custom `Vector<T>` built on `std::construct_at`/`std::destroy_at`) eliminate manual `new`/`delete` and shrink the attack surface for UAF and double-free.
- **Trivial relocation** (`std::is_trivially_relocatable_v`, `std::relocate`) is a contemporary direction to let containers move without per-element reallocation.

---

## 🔒 Global Security and Compliance Guidelines

- Strictly follow the directives set in [appsec-owasp-asvs](../../appsec/appsec-owasp-asvs/SKILL.md) and [clean-code-reusability](../../../engineering/practices/clean-code-reusability/SKILL.md).
- Replace insecure legacy functions and patterns with managed memory allocation types and modern safe abstractions.
- For the full language-level ownership and RAII contract, see [lang-cpp](../../../languages/lang-cpp/SKILL.md).
