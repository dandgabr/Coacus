---
name: lang-assembly-x64
description: Provides software engineering and programming patterns in x86_64 Assembly (Linux POSIX and Windows x64) based on The Assembly Language Reimagined (John Schwartzman) and Assembly Programming Language For Beginners (Panchtilak, Kavishankar). Covers Intel and AT&T syntax, general-purpose and SIMD registers (AVX/SSE), direct system calls (syscalls), the System V AMD64 ABI, stack manipulation, CPU flags, addressing modes, string instructions, procedures/recursion/macros, and low-level optimization.
---

# x86_64 Assembly Engineering (Intel 64 / AMD64)

This skill sets out clean-code guidelines and conventions for **x86_64 Assembly** development (NASM/Yasm and GCC/GAS), covering registers, function calling conventions (ABIs), pointer manipulation, and Linux system calls.

> 📖 **Canonical reference**: see [references/assembly-beginners-guide.md](references/assembly-beginners-guide.md) for the fundamentals from *Assembly Programming Language For Beginners* (Panchtilak, Kavishankar) — segmented memory model (.data/.bss/.text/stack), IA-32 registers, CPU flags (ZF/CF/OF/SF/DF), addressing modes (register/immediate/direct/direct-offset/indirect), essential arithmetic/logic/control instructions, string instructions with repeat prefixes (MOVS/LODS/STOS/CMPS/SCAS + REP), procedures and stack (PUSH/POP/CALL/RET), recursion (termination condition), macros, Linux `int 0x80` syscalls (sys_exit/sys_fork/sys_read/sys_write/sys_open/sys_close table), file handling, and dynamic allocation with `sys_brk`.

---

## 💻 1. x86_64 Architecture Registers

| 64-bit | 32-bit | 16-bit | 8-bit (Low/High) | Role in the System V ABI (Linux) |
| :--- | :--- | :--- | :--- | :--- |
| `rax` | `eax` | `ax` | `al` / `ah` | Function return value / Syscall Number |
| `rdi` | `edi` | `di` | `dil` | 1st function argument |
| `rsi` | `esi` | `si` | `sil` | 2nd function argument |
| `rdx` | `edx` | `dx` | `dl` / `dh` | 3rd function argument |
| `rcx` | `ecx` | `cx` | `cl` / `ch` | 4th function argument (or `r10` in syscalls) |
| `r8`  | `r8d` | `r8w`| `r8b` | 5th function argument |
| `r9`  | `r9d` | `r9w`| `r9b` | 6th function argument |
| `rsp` | `esp` | `sp` | `spl` | Stack Pointer (top-of-stack pointer) |
| `rbp` | `ebp` | `bp` | `bpl` | Base Pointer (function frame pointer) |

---

## 🛠️ 2. Example: Pure Hello World in NASM (Linux Syscalls)

```nasm
section .rodata
    msg db "Hello, x86_64 Assembly!", 0x0A
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1          ; syscall: sys_write
    mov rdi, 1          ; fd: stdout
    lea rsi, [rel msg]  ; buffer address (Position-Independent)
    mov rdx, len        ; count
    syscall

    ; exit(0)
    mov rax, 60         ; syscall: sys_exit
    xor rdi, rdi        ; status: 0
    syscall
```

---

## 🏁 Additional Fundamentals (Panchtilak)

Adapted from *Assembly Programming Language For Beginners* (ported from IA-32 to x86_64 where applicable):

- **Segmented memory model**: `.data` (static, fixed size), `.bss` (zero-filled buffers with `RESB`/`TIMES`), `.text` (code), and stack — maps onto x86_64's `.rodata`/`.data`/`.bss`/`.text`.
- **Data registers** with canonical roles: `AX` (accumulator — I/O and arithmetic), `BX` (base — indexed addressing), `CX` (count — loops), `DX` (I/O and the `DX:AX` pair in multiply/divide). In x86_64: `RAX`, `RBX`, `RCX`, `RDX`.
- **Essential flags**: `ZF` (zero result), `CF` (unsigned carry), `OF` (signed overflow), `SF` (sign), `DF` (string direction via `STD`/`CLD`), `TF` (single-step debug), `IF` (interrupts).
- **Common idioms**: `XOR EAX, EAX` to zero a register; `TEST`/`CMP` + `JZ`/`JE`/`JNZ` for flag-based conditional branches.
- **Addressing modes**: register (fastest, no memory), immediate (constant), direct (named variable — symbol table), direct-offset (`TABLE[2]` / `TABLE + 2` for tables), indirect (base/index in brackets — `MOV EBX, [MY_TABLE]` + `ADD EBX, 2` for arrays).
- **String instructions** with `DS:SI`/`ES:DI` pairs and B/W/D suffixes: `MOVS`, `LODS`, `STOS`, `CMPS`, `SCAS`; repetition with `REP`/`REPE`/`REPNE` gated on `CX`.
- **Procedures**: `CALL proc_name` + `RET`; LIFO stack via `PUSH`/`POP` (`SS:ESP`); recursion requires a termination condition (e.g., factorial `Fact(n) = n * fact(n-1)`, stopping at `n == 0`).
- **Macros** (`%macro` in NASM) expand textually at each use — prefer procedures for large bodies (less generated code).
- **IA-32 syscalls (`int 0x80`)**: number in `EAX`, arguments in `EBX`/`ECX`/`EDX`/`ESI`/`EDI`/`EBP`, result in `EAX`. In x86_64 use `syscall` with different numbers (e.g., `sys_write=1`, `sys_exit=60`) and arguments in `RDI`/`RSI`/`RDX` — see the register table above.
- **File handling**: `sys_creat` (8), `sys_open` (5), `sys_write` (4), `sys_close` (6); reads with `sys_read` (3) into `.bss` buffers.
- **Dynamic allocation with `sys_brk` (45)**: extends the data break in `EBX` (current address → current + size); fill blocks with `REP STOSD` + `STD`/`CLD`.
