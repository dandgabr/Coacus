---
name: "framework-criterion"
description: "Acts as a specialist in unit testing for the C language using Criterion, covering Test macros, cr_assert/cr_expect, life cycles (.init/.fini), signal and crash testing, stdout/stderr capture, and CMake integration."
---

# AI Skill: Criterion Testing Specialist in C (Criterion Specialist)

This skill guides the AI to act as a **QA and C software engineering specialist focused on the Criterion framework**. Its goal is to guide the creation of modern, safe, and concise C unit test suites (C99, C11, C17, C23), covering memory assertions, signal and system testing, standard input/output redirection, and integration with CMake/Meson pipelines.

---

## 🧭 Criterion Principles and Architecture

When using Criterion in C code projects:
- **Clean, Declarative Syntax**: Use the `Test(suite_name, test_name)` macro to define suites and tests without writing `main()` functions or registering tests manually.
- **Assertions and Expectations**:
  - `cr_assert_*`: Immediately aborts the current test if the condition is false.
  - `cr_expect_*`: Marks the failure in the final report but lets the test keep running.
- **Process Isolation**: Criterion runs each test in a separate isolated process through `fork()`. A crash (such as a `SIGSEGV` from a null pointer) in one test does not abort the whole suite.
- **Native I/O Redirection**: Test `stdout` and `stderr` output by capturing file descriptors natively.

---

## 🛠️ Practical Engineering Guidelines and Code Standards

### 1. Unit Testing C Functions (`cr_assert_eq`, `cr_assert_str_eq`)
- Use typed comparison macros for detailed error messages.

```c
#include <criterion/criterion.h>
#include <criterion/new/assert.h>
#include "calculator.h"

Test(calculator_suite, test_add_positive_numbers) {
    int result = add(15, 25);
    cr_assert_eq(result, 40, "Esperado 40, mas obteve %d", result);
}

Test(calculator_suite, test_string_formatting) {
    char *formatted = format_currency(100.50);
    cr_assert_str_eq(formatted, "$100.50", "String formatada incorreta: %s", formatted);
    free(formatted); // Limpeza de memória
}
```

### 2. Life-Cycle Configuration (`.init` and `.fini`)
- Define setup (`.init`) and teardown (`.fini`) functions directly in the extra parameters of the `Test` macro.

```c
#include <criterion/criterion.h>
#include <stdio.h>
#include "database_driver.h"

static DBConnection *db_conn = NULL;

void setup_db(void) {
    db_conn = db_connect("sqlite::memory:");
    db_create_tables(db_conn);
}

void teardown_db(void) {
    if (db_conn) {
        db_disconnect(db_conn);
        db_conn = NULL;
    }
}

Test(database_suite, test_insert_record, .init = setup_db, .fini = teardown_db) {
    cr_assert_not_null(db_conn, "Conexão com o banco de dados deve estar ativa.");
    int status = db_insert(db_conn, "users", "Alice");
    cr_assert_eq(status, DB_SUCCESS, "Falha ao inserir registro.");
}
```

### 3. Signal, Crash, and Timeout Testing (`.signal` and `.timeout`)
- Make sure defensive C functions handle null pointers or raise `SIGSEGV`/`SIGABRT` where appropriate.

```c
#include <criterion/criterion.h>
#include <signal.h>
#include "utils.h"

// Teste espera que a função dispare Segmentation Fault se receber ponteiro nulo
Test(safety_suite, test_null_pointer_crash, .signal = SIGSEGV) {
    process_buffer(NULL, 100);
}

// Teste é cancelado se demorar mais de 1.5 segundos
Test(performance_suite, test_infinite_loop_prevention, .timeout = 1.5) {
    compute_complex_hash("payload");
}
```

### 4. Standard Output Testing (`stdout` / `stderr`)
- Redirect and validate data printed with `printf`.

```c
#include <criterion/criterion.h>
#include <criterion/redirect.h>
#include <stdio.h>

void setup_redirects(void) {
    cr_redirect_stdout();
    cr_redirect_stderr();
}

Test(cli_suite, test_print_welcome_message, .init = setup_redirects) {
    puts("Bem-vindo ao Sistema!");
    cr_assert_stdout_eq_str("Bem-vindo ao Sistema!\n");
}
```

---

## ⚙️ Build System Integration (CMakeLists.txt)

```cmake
cmake_minimum_required(VERSION 3.14)
project(c_project_tests C)

set(CMAKE_C_STANDARD 11)

find_package(PkgConfig REQUIRED)
pkg_check_modules(CRITERION REQUIRED criterion)

add_executable(run_tests 
    tests/test_main.c 
    src/calculator.c
)

target_include_directories(run_tests PRIVATE src/ ${CRITERION_INCLUDE_DIRS})
target_link_libraries(run_tests PRIVATE ${CRITERION_LIBRARIES})

enable_testing()
add_test(NAME criterion_tests COMMAND run_tests)
```

---

## 🔗 Integration with Other Skills

- [lang-c](../../languages/lang-c/SKILL.md): Ensures compliance with C standards (C11/C17), prevention of undefined behavior (UB), and memory management.
- [qa-engineer](../../roles/qa-engineer/SKILL.md): Guides the design of unit test suites for embedded software and low-level systems.
- [framework-testing](../framework-testing/SKILL.md): Provides the theoretical concepts of TDD and the test pyramid.
