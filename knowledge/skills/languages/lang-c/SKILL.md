---
name: "lang-c"
description: "Provides software engineering patterns in modern C based on the international standard ISO/IEC 9899 (focusing on C23 - ISO/IEC 9899:2024, C17, C11, and C99) and the official references at en.cppreference.com/w/c, covering keywords (nullptr, bool, constexpr), attributes ([[nodiscard]], [[deprecated]]), safe math (<stdckdint.h>), bit operations (<stdbit.h>), memory debugging, and CMake."
---

# AI Skill: Modern C Engineering (ISO/IEC 9899 & cppreference Specialist)

This skill guides the AI to act as a specialist in the **modern C** language, relying strictly on the official international standard **ISO/IEC 9899** (published by ISO JTC1/SC22/WG14 at [iso-9899.info](https://www.iso-9899.info/wiki/The_Standard)) and the official C reference documentation at [en.cppreference.com/w/c](https://en.cppreference.com/w/c). The main focus is the most recent revision, **C23 (ISO/IEC 9899:2024)**, while keeping support for the C17, C11, and C99 revisions to build high-performance, safe, low-level systems free of Undefined Behavior (UB).

---

## 🧭 C Language Specifications (en.cppreference.com/w/c)

When developing in C, consult the specification and the formal header tables of the Standard Library on `cppreference`:

### 1. ISO/IEC 9899:2024 (C23 - Most Recent Standard)
- **New Native Keywords**:
  - `nullptr`: Strict `nullptr_t` type for null pointers, replacing the numeric ambiguity of `NULL`.
  - `bool`, `true`, `false`: Native boolean types (no dependency on `<stdbool.h>`).
  - `constexpr`: Evaluation of immutable constants at compile time.
  - `auto`: Automatic type inference on variable declarations.
  - `typeof` and `typeof_unqual`: Compile-time type inspection operators.
  - `static_assert`, `alignas`, `alignof`, `thread_local`: Simplified keywords (no `_` prefix).
- **Unified Attribute Syntax (`[[attribute]]`)**:
  - `[[nodiscard]]`: Warns when a function's return value is ignored.
  - `[[maybe_unused]]`: Suppresses warnings for intentionally unused variables or parameters.
  - `[[deprecated("reason")]]`: Flags obsolete functions or types.
  - `[[likely]]` / `[[unlikely]]`: Optimization hints for branch prediction.
  - `[[fallthrough]]`: Explicit declaration of intentional fallthrough in `switch` statements.
  - `[[noreturn]]`: Indicates the function never returns (e.g., `exit`, `abort`).
- **New Libc Security Headers and Functions**:
  - **`<stdckdint.h>`**: Checked integer arithmetic: `ckd_add`, `ckd_sub`, `ckd_mul`.
  - **`<stdbit.h>`**: Standardized bit manipulation: `stdc_count_ones`, `stdc_leading_zeros`, `stdc_trailing_zeros`, `stdc_has_single_bit`, `stdc_bit_ceil`.
  - `memset_explicit`: Sanitization of confidential memory (passwords, keys) immune to compiler dead-store elimination.
  - `memalignment`: Byte-alignment check for pointers.
  - `strdup` and `strndup`: Standardized dynamic string allocation and duplication in libc.
  - `unreachable()`: Optimization macro for unreachable code paths (`<stddef.h>`).
- **Modern Preprocessor and I/O**:
  - `#embed`: Direct inclusion of binary resources as data at compile time.
  - `#elifdef` and `#elifndef`, the `__has_include` and `__VA_OPT__` macros.
  - Binary integer format `%b` and `%B` in `printf`/`scanf` and `0b1010` literals.
  - Null initialization with empty braces: `struct Buffer buf = {};`.

### 2. ISO/IEC 9899:2018 (C17) & 9899:2011 (C11)
- **`<threads.h>` (C11)**: Native thread management (`thrd_create`, `thrd_join`), mutual exclusion (`mtx_t`, `mtx_lock`, `mtx_unlock`), and condition variables (`cnd_t`).
- **`<stdatomic.h>` (C11)**: Lock-free atomic types and operations (`atomic_int`, `atomic_store`, `atomic_load`, `atomic_compare_exchange_strong`).
- **`_Generic`**: Type-based generic expression selection for polymorphic macros.
- **C17**: Technical corrections and clarifications of ambiguities in the C11 standard without adding new syntactic features.

### 3. ISO/IEC 9899:1999 (C99)
- `//` line comments, designated initializers (`.field = val`), compound literals, `inline`, the `restrict` qualifier, fixed-width integers in `<stdint.h>`, and complex types in `<complex.h>`.

---

## 🛠️ Engineering Guidelines and Defect Prevention

### 1. Strict Prevention of Undefined Behavior (UB)
- **Safe Memory Management**:
  - Always zero or initialize dynamically allocated memory (`malloc`/`calloc`).
  - Assign `nullptr` (C23) or `NULL` to pointers immediately after freeing them with `free()`.
  - For allocations holding password or key data, use `memset_explicit()` before `free()`.
- **Integer Overflow**: Avoid signed integer overflow using the checked functions from `<stdckdint.h>` (C23) or prior bounds checks.
- **Avoid VLAs (Variable Length Arrays)**: Prefer dynamic heap allocation or fixed sizes to avoid stack overflow.

### 2. Static Analysis and Sanitizers
- Compile with strict warnings enabled: `-Wall -Wextra -Wpedantic -Wconversion -Wshadow -std=c23`.
- Run with Sanitizers during tests: `-fsanitize=address,undefined,leak`.

---

## 🧰 Recommended C23 Code Patterns (cppreference style)

### 1. Safe Integer Arithmetic and Attributes (`<stdckdint.h>` & C23)
```c
#include <stdio.h>
#include <stdckdint.h>

[[nodiscard]] bool safe_multiply_and_add(int a, int b, int c, int *result) {
    int temp = 0;
    
    // Multiplicação com checagem de estouro em C23
    if (ckd_mul(&temp, a, b)) {
        return false; // Estouro detectado
    }
    
    // Adição com checagem de estouro em C23
    if (ckd_add(result, temp, c)) {
        return false; // Estouro detectado
    }
    
    return true;
}

int main(void) {
    int val = 0;
    if (safe_multiply_and_add(100000, 200000, 50, &val)) {
        printf("[+] Resultado seguro: %d\n", val);
    } else {
        printf("[-] Erro: Estouro de inteiro prevenido!\n");
    }
    return 0;
}
```

### 2. Native C23 Bit Manipulation (`<stdbit.h>`)
```c
#include <stdio.h>
#include <stdbit.h>
#include <stdint.h>

int main(void) {
    uint32_t mask = 0b00111010;
    
    // Funções padronizadas de contagem de bits em C23 (stdbit.h)
    unsigned int ones = stdc_count_ones(mask);
    bool is_power_of_two = stdc_has_single_bit(mask);

    printf("[+] Número de bits 1: %u\n", ones);
    printf("[+] É potência de dois? %s\n", is_power_of_two ? "sim" : "não");

    return 0;
}
```

### 3. Using `nullptr`, Attributes, and Safe Memory Cleanup (`memset_explicit`)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char username[32];
    char secret_token[64];
} UserAccountSecure;

void wipe_sensitive_data(UserAccountSecure *account) {
    if (account == nullptr) {
        return;
    }
    
    // memset_explicit garante que o compilador não otimizará a exclusão
    memset_explicit(account->secret_token, 0, sizeof(account->secret_token));
}

int main(void) {
    // Inicialização vazia C23
    UserAccountSecure user = {};
    snprintf(user.username, sizeof(user.username), "alice");
    snprintf(user.secret_token, sizeof(user.secret_token), "secret_12345");

    printf("[+] Usuário ativado: %s\n", user.username);

    wipe_sensitive_data(&user);
    return 0;
}
```

---

## ⚙️ Modern Build System Configuration (CMakeLists.txt C23)

```cmake
cmake_minimum_required(VERSION 3.25)
project(c23_modern_project C)

# Define o padrão C23 (ISO/IEC 9899:2024)
set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_executable(app_main src/main.c)

# Bateria estrita de avisos do compilador
if (MSVC)
    target_compile_options(app_main PRIVATE /W4 /WX)
else()
    target_compile_options(app_main PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror)
endif()
```

---

## 🔒 Security Issues and Safe Practices

- **Buffer Overflows (CWE-121 / CWE-122)**: Never use unsafe functions such as `strcpy`, `strcat`, `gets`, or `sprintf`. Replace them with safe equivalents such as `strncpy`, `strncat`, `snprintf`, or dynamic string functions.
- **Integer Overflows (CWE-190)**: Validate arithmetic operations before execution if the result is used for memory allocation (e.g., `malloc(width * height)`). Use checked functions (or `<stdckdint.h>` in C23).
- **Use-After-Free & Double Free (CWE-416 / CWE-415)**: Always null out pointers immediately after freeing them (`free(ptr); ptr = NULL;`) to mitigate dangling pointers.
- **Format Strings (CWE-134)**: Never pass user input directly as the format string of printing functions (use `printf("%s", input)` instead of `printf(input)`).

## 🔗 Integration with Other Skills

- To compile C++23 components and interoperate with C, see [lang-cpp](../lang-cpp/SKILL.md).
- To run safe unit tests on C functions using the Criterion framework, see [framework-criterion](../../frameworks/framework-criterion/SKILL.md).
- To audit buffer overflow, format string, and pointer vulnerabilities in C code, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
