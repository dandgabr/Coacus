# Example: Table Lookup with Indirect Addressing (Panchtilak)

Adapted from IA-32 (`int 0x80`) to x86_64 NASM (Linux). Demonstrates direct-offset and indirect addressing modes for array manipulation, and the `write`/`exit` syscalls (x86_64 numbers: 1 and 60).

```nasm
section .data
    msg     db "Values: ", 0
    msg_len equ $ - msg
    newline db 0x0A

    ; Tabelas na seção de dados (direct-offset addressing)
    byte_table  db 14, 15, 22, 45
    word_table  dw 134, 345, 564, 123

section .bss
    ; Buffers estáticos zero-filled (reservados, não inicializados)
    out_buf resb 16

section .text
    global _start

_start:
    ; --- Direct-offset addressing: acessa elementos por índice ---
    movzx   r8, byte [byte_table + 2]   ; 3º elemento (22)
    movzx   r9, word [word_table + 3*2] ; 4º elemento (123)

    ; --- Indirect addressing: base register percorre o array ---
    lea     rbx, [byte_table]           ; effective address em RBX
    mov     rcx, 4                      ; contagem (count register)
.fill_loop:
    mov     al, [rbx]                   ; lê o elemento corrente
    ; (processamento do valor iria aqui)
    add     rbx, 1                      ; avança para o próximo byte
    dec     rcx
    jnz     .fill_loop                  ; loop while CX != 0 (flags)

    ; write(1, msg, msg_len)
    mov     rax, 1                      ; syscall: sys_write
    mov     rdi, 1                      ; fd: stdout
    lea     rsi, [rel msg]
    mov     rdx, msg_len
    syscall

    ; exit(0)
    mov     rax, 60                     ; syscall: sys_exit
    xor     rdi, rdi
    syscall
```

How to assemble and run:

```bash
nasm -f elf64 table_lookup.asm -o table_lookup.o
ld table_lookup.o -o table_lookup
./table_lookup
```

Key points extracted from the book:

- **Indirect addressing** uses base registers (`EBX`/`RBX`, `EBP`) and index registers (`ESI`/`EDI`) between brackets — ideal for arrays.
- **Direct-offset addressing** (`BYTE_TABLE[2]` or `BYTE_TABLE + 2`) is managed by the assembler's symbol table.
- `MOVZX` (move with zero-extend) avoids partial reads when loading bytes/words into 64-bit registers.
- The loop uses `CX`-like counting (`RCX` + `DEC`/`JNZ`), the book's pattern for iteration.
