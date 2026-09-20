# Assembly Fundamentals — Beginner's Guide (Panchtilak, Kavishankar)

Consolidated from *Assembly Programming Language For Beginners — Learn Assembly Programming Language* (Panchtilak, Kavishankar). The book covers the fundamentals of IA-32/x86 Assembly with NASM on Linux: segmented memory architecture, registers, flags, addressing modes, essential instructions, `int 0x80` syscalls, procedures, the stack, recursion, macros, strings, file I/O, and dynamic allocation with `sys_brk`.

> **Adaptation note for x86_64**: the book's examples use the IA-32 interface (`int 0x80`, 32-bit registers). On x86_64 the fundamentals are the same, but use the `syscall` interface (numbers and conventions differ — see the main SKILL.md). The concepts (flags, addressing modes, stack, procedures) carry over directly.

---

## 1. Memory Model (Segments)

An assembly program organizes memory into three segments:

| Segment | NASM Section | Characteristic |
| :--- | :--- | :--- |
| **Data segment** | `.data` | Static; declared data elements; cannot be expanded after the fact |
| **BSS** | `.bss` | Static **zero-filled** buffers for data declared later (`resb`, `resw`, `resd`) |
| **Code segment** | `.text` | Fixed area holding instructions |
| **Stack** | (implicit) | Values passed to functions/procedures |

---

## 2. Registers (IA-32 / x86)

The book groups registers into **general**, **control**, and **segment** registers:

- **Data registers** (32/16/8 bits): `EAX/AX/AL/AH`, `EBX/BX/BL/BH`, `ECX/CX/CL/CH`, `EDX/DX/DL/DH`:
  - `AX` — primary accumulator (I/O and general arithmetic);
  - `BX` — base register (indexed addressing);
  - `CX` — count register (loops, `LOOP`);
  - `DX` — data register (I/O; the `DX:AX` pair in multiply/divide with large values).
- **Pointer registers**: `EIP/IP` (instruction pointer — offset of the next instruction, with `CS:IP`), `ESP/SP` (stack pointer, with `SS:SP`), `EBP/BP` (base pointer — reference to subroutine parameters).
- **Index registers**: `ESI/SI` (source index — string operations) and `EDI/DI` (destination index).
- **Segment registers**: `CS` (code), `DS` (data), `SS` (stack), `ES` (extra).

---

## 3. CPU Flags (Control Registers)

The flags register records the state of every arithmetic/logic operation:

| Flag | Role |
| :--- | :--- |
| **OF** (Overflow) | Overflow of the high-order bit in a **signed** operation |
| **DF** (Direction) | String movement direction (`0` = left→right; `cld`/`std`) |
| **IF** (Interrupt) | Handles/ignores external interrupts (`sti`/`cli`) |
| **TF** (Trap) | Single-step mode (debug) |
| **SF** (Sign) | Sign of the result (most significant bit) |
| **ZF** (Zero) | Zero result (comparisons: `CMP`/`TEST` set ZF) |
| **AF** (Auxiliary Carry) | Carry from the nibble (BCD) |
| **PF** (Parity) | Parity of the result |
| **CF** (Carry) | Carry/borrow from the high-order bit in an **unsigned** operation |

Idiomatic patterns from the book:
- `XOR EAX, EAX` — zeroes the register (and clears CF for `LODSD`/long arithmetic);
- `TEST AL, 01H` + `JZ EVEN_NUMBER` — tests the least significant bit for parity;
- `CMP AL, BL` + `JE EQUAL` — a comparison that produces a conditional jump.

---

## 4. Addressing Modes

| Mode | Description | Example (NASM) |
| :--- | :--- | :--- |
| **Register** | Operands only in registers — **fastest** processing (no memory access) | `MOV EAX, EBX` |
| **Immediate** | The second operand is a constant; the first sets the size | `ADD BYTE_VALUE, 65` |
| **Direct memory** | Offset embedded in the instruction (variable name); the assembler keeps the symbol table | `MOV BX, WORD_VALUE` |
| **Direct-offset** | Arithmetic operators modify the address (table indexing) | `MOV CL, BYTE_TABLE[2]` or `BYTE_TABLE + 2` |
| **Indirect memory** | Base/index registers between brackets (`EBX`, `EBP`, `SI`, `DI`); typical for arrays | `MOV EBX, [MY_TABLE]` / `MOV [EBX], 110` / `ADD EBX, 2` |

NASM data sizes: `DB` (byte, 1), `DW` (word, 2), `DD` (dword, 4), `DQ` (qword, 8), `DT` (tbyte, 10); reservations with `TIMES`/`RESB` series. Constants with `EQU`:

```nasm
MY_TABLE TIMES 10 DW 0   ; 10 words inicializadas a 0
MOV EBX, [MY_TABLE]      ; effective address
MOV [EBX], 110           ; MY_TABLE[0] = 110
ADD EBX, 2               ; EBX = EBX + 2
MOV [EBX], 123           ; MY_TABLE[1] = 123
```

---

## 5. Essential Instructions

- **MOV** — copies data between registers/memory/immediate.
- **Arithmetic**: `ADD`/`SUB`/`INC`/`DEC`; `MUL`/`IMUL` (unsigned/signed — `MOV AL, 10` + `MOV DL, 25` + `MUL DL`); `DIV`/`IDIV`; BCD arithmetic with `AAA`/`AAS`/`AAM`/`AAD`/`DAA`/`DAS`.
- **Logic**: `AND`, `OR`, `XOR`, `NOT`, `TEST` (AND without storing the result — for flags).
- **Conditional jump** (based on the status flags): `JZ`/`JE`, `JNZ`/`JNE`, `JG`/`JGE` (signed), `JA`/`JAE` (unsigned), `JL`/`JLE`, `JB`/`JBE`, `JC`, `JOF`, etc.
- **Loop**:

```nasm
MOV CL, 10
L1:
  ; loop body
  DEC CL        ; (ou LOOP L1, que decrementa CX e salta se != 0)
  JNZ L1
```

- **Strings** (with `DS:SI` source / `ES:DI` destination pairs and B/W/D suffixes):

| Instruction | Operation | Suffixes |
| :--- | :--- | :--- |
| `MOVS` | Moves byte/word/dword from memory to memory | `MOVSB/W/D` |
| `LODS` | Loads from memory into `AL/AX/EAX` | `LODSB/W/D` |
| `STOS` | Stores from `AL/AX/EAX` into memory | `STOSB/W/D` |
| `CMPS` | Compares two items in memory | `CMPSB/W/D` |
| `SCAS` | Compares `AL/AX/EAX` with an item in memory | `SCASB/W/D` |

  Repeat prefixes: `REP`, `REPE`/`REPZ`, `REPNE`/`REPNZ` (combine with `CX` and DF — e.g., `REP STOSD` used in the memory allocation example, preceded by `STD`/`CLD`).

---

## 6. Procedures, Stack, and Recursion

- **Procedure**: a named block ending in `RET`, called via `CALL proc_name`.

```nasm
sum:
    mov eax, ecx
    add eax, edx
    add eax, '0'
    ret
```

- **Stack (LIFO)**: `PUSH`/`POP` using `SS:ESP`. The stack is used to save/restore registers, pass parameters, and return addresses.
- **Recursion**: each recursive call pushes its own context; it requires a **termination condition** (e.g., `Fact(n) = n * fact(n-1)` for `n > 0`, ending at `n == 0`).

---

## 7. Macros

A modularization mechanism: a sequence of instructions assigned to a name, expanded textually at each use (unlike procedures, which are called/jumped to).

---

## 8. Linux System Calls (`int 0x80`)
Steps from the book (IA-32):

```nasm
1. Número da syscall em EAX
2. Argumentos em EBX, ECX, EDX, ESI, EDI, EBP (ordem consecutiva)
3. Interrupção: int 0x80
4. Resultado (código de retorno) em EAX
```

With more than six arguments: `EBX` holds the memory pointer of the first argument.

| EAX | Syscall | EBX | ECX | EDX | ESI | EDI |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `sys_exit` | int (status) | – | – | – | – |
| 2 | `sys_fork` | `struct pt_regs *` | – | – | – | – |
| 3 | `sys_read` | `unsigned int` (fd) | `char *` (buf) | `size_t` | – | – |
| 4 | `sys_write` | `unsigned int` (fd) | `const char *` | `size_t` | – | – |
| 5 | `sys_open` | `const char *` | int (flags) | int (mode) | – | – |
| 6 | `sys_close` | `unsigned int` (fd) | – | – | – | – |

Read + write example:

```nasm
; leitura (sys_read = 3)
MOV ECX, num
MOV EDX, 5
INT 80H
; escrita (sys_write = 4)
MOV ECX, dispMsg
MOV EDX, lenDispMsg
INT 80H
```

The complete syscall list lives in /usr/include/asm/unistd.h.

---

## 9. File Handling (syscalls)

Create/open (`sys_creat` no. 8, `sys_open` no. 5), write (`sys_write` no. 4), close (`sys_close` no. 6):

```nasm
; criação: EAX=8, EBX=filename, ECX=permissões (ex.: 0377 octal)
; escrita: EAX=4, EBX=fd, ECX=buffer, EDX=comprimento
; fechamento: EAX=6, EBX=fd
```

---

## 10. Memory Management (`sys_brk`)

`sys_brk` (syscall no. 45) allocates memory **immediately after the application image**, setting the highest address of the data section; it receives the address in `EBX` and returns `-1` or the negative error code on failure.

```nasm
MOV EAX, 45        ; sys_brk
XOR EBX, EBX
INT 80H            ; endereço atual
ADD EAX, 16384     ; + 16 KB
MOV EBX, EAX
MOV EAX, 45
INT 80H            ; nova quebra definida
```

Fill the block with `REP STOSD` (with `STD`/`CLD` for direction).

---

Full source: the file converted in a local conversion workspace `Programming Language For Beginners ...` (for extracting new details, if needed).
