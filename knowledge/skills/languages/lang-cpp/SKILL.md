---
name: "lang-cpp"
description: "Provides software engineering patterns in modern C++ based on the international standard ISO/IEC 14882 (focusing on C++23 - ISO/IEC 14882:2024, C++20, C++17, and C++14) and the documentation at en.cppreference.com, covering RAII, Smart Pointers, Concepts, Modules, Coroutines, std::expected, std::print, Ranges, CMake, and the C++ Core Guidelines."
---

# AI Skill: Modern C++ Engineering (ISO/IEC 14882 Specialist)

This skill guides the AI to act as a specialist in the **modern C++** language, relying strictly on the official international standard **ISO/IEC 14882** and the technical references at [en.cppreference.com](https://en.cppreference.com/). The focus spans the most recent revision, **C++23 (ISO/IEC 14882:2024)**, **C++20 (ISO/IEC 14882:2020)**, C++17, C++14, and C++11, ensuring adherence to the principles of *Zero-Cost Abstractions*, safe resource management via **RAII**, fearless concurrency, and alignment with the **C++ Core Guidelines**.

---

## 🧭 Evolution of the ISO/IEC 14882 Standards and Modern C++ Features

When designing software in C++, use the latest tools and abstractions supported by the project's compiler:

### 1. ISO/IEC 14882:2024 (C++23 - Most Recent Standard)
- **Monadic Error Handling (`std::expected`)**: An efficient replacement for exceptions and traditional error codes (`std::expected<T, E>`), providing chaining with `.and_then()`, `.transform()`, and `.or_else()`.
- **Native Formatter and Printing (`std::print` / `std::println`)**: Direct, typed printing to streams without the overhead of `std::cout` (`#include <print>`).
- **New Performance Containers (`std::flat_map` / `std::flat_set`)**: Container adapters based on contiguous memory vectors with excellent cache locality.
- **Generators and Coroutines (`std::generator`)**: Simplified creation of lazily-evaluated iterators and sequences based on coroutines (`co_yield`).
- **Deducing `this` (Explicit Object Parameters)**: Simplifies class methods, lambda recursion, and the CRTP pattern.
- **Additional Utilities**: Native byte swapping (`std::byteswap`), `std::span` extensions, and the `[[assume(expr)]]` attribute.

### 2. ISO/IEC 14882:2020 (C++20)
- **Concepts and Constraints (`concepts` and `requires`)**: Compile-time metaprogramming validation with readable error messages (`template <std::integral T>`).
- **C++ Modules (`module`, `import`, `export`)**: Replacing the traditional header model (`#include`) with compiled modules that isolate scope and dramatically reduce build times.
- **Ranges and Pipelines (`std::ranges`)**: Functional composition of algorithms using the pipe operator `|` (`views::filter`, `views::transform`).
- **Native Coroutines**: Support for suspendable functions with `co_await`, `co_yield`, and `co_return`.
- **Spaceship Operator (`<=>` / Three-Way Comparison)**: Automatic generation of all comparison operators (`auto operator<=>const = default;`).
- **Text Formatting (`std::format`)**: Fast, safe string interpolation inspired by Python syntax.
- **Concurrency and Threads**: `std::jthread` (an RAII, auto-joining thread) and cancellation tokens (`std::stop_token`).

### 3. ISO/IEC 14882:2017 (C++17) & 14882:2014 (C++14)
- **C++17**: Value utility types (`std::optional`, `std::variant`, `std::any`), allocation-free views (`std::string_view`), Structured Bindings (`auto [x, y] = point;`), filesystem support (`std::filesystem`), `if` with a local initializer, and parallel algorithms (`std::execution::par`).
- **C++14**: `std::make_unique`, generic lambdas (`auto x`), `std::shared_lock`, and relaxed `constexpr`.

### 4. ISO/IEC 14882:2011 (C++11 - The Foundation of Modern C++)
- Move Semantics with rvalue references (`std::move`, `std::forward`).
- Smart Pointers for RAII: `std::unique_ptr` (exclusive ownership), `std::shared_ptr`, and `std::weak_ptr`.
- Native concurrency: `<thread>`, `<mutex>`, `<atomic>`, `<future>`.

---

## 🛠️ Engineering Guidelines and the C++ Core Guidelines

### 1. RAII (Resource Acquisition Is Initialization)
- **Zero Manual Leaks**: Never call `new` or `delete` explicitly. Encapsulate resource management (memory, sockets, files, mutexes) in RAII objects (`std::unique_ptr`, `std::lock_guard`, `std::fstream`).
- **Rule of Zero, Three, or Five**: If a class needs to manage resources explicitly, define or delete the 5 special member functions (destructor, copy constructor, copy assignment, move constructor, move assignment). Prefer the *Rule of Zero* by delegating management to smart pointers and standard containers.

### 2. Safe Error Handling and Immutability
- **`const` by Default**: Mark variables, references, and member methods as `const` whenever the value does not mutate.
- **`constexpr` and `consteval`**: Move as much computation as possible to compile time.
- **`noexcept`**: Mark functions that are guaranteed not to throw exceptions (especially move constructors and move assignment operators).

---

## 🧰 Recommended Code Patterns

### 1. C++23: Monadic Error Handling with `std::expected` and Native Printing (`std::print`)
```cpp
#include <print>
#include <expected>
#include <string_view>

enum class MathError {
    DivisionByZero,
    NegativeLogarithm
};

constexpr std::expected<double, MathError> divide(double a, double b) noexcept {
    if (b == 0.0) {
        return std::unexpected(MathError::DivisionByZero);
    }
    return a / b;
}

int main() {
    auto result = divide(10.0, 2.0)
        .transform([](double val) { return val * 100.0; });

    if (result.has_value()) {
        std::println("[+] Sucesso! Resultado calculado: {:.2f}", result.value());
    } else {
        std::println(stderr, "[-] Erro no cálculo matemático.");
    }
    return 0;
}
```

### 2. C++20: Concepts, Ranges, and the Spaceship Operator (`<=>`)
```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <concepts>
#include <compare>

// Definição de conceito em C++20
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

struct Item {
    std::string name;
    double price;

    // Operador de comparação espaçonave C++20
    auto operator<=>(const Item&) const = default;
};

template <Numeric T>
T calculate_sum(const std::vector<T>& values) {
    T sum = 0;
    for (const auto& v : values) {
        sum += v;
    }
    return sum;
}

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Filtro e transformação com C++20 Ranges
    auto even_squares = numbers 
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * n; });

    std::cout << "[+] Quadrados pares: ";
    for (int val : even_squares) {
        std::cout << val << " ";
    }
    std::cout << "\n";
    return 0;
}
```

### 3. Safe Resource Management with Smart Pointers (`std::unique_ptr`)
```cpp
#include <memory>
#include <string>
#include <iostream>

class DatabaseConnection {
public:
    explicit DatabaseConnection(std::string conn_str) 
        : connection_string_(std::move(conn_str)) {
        std::cout << "[+] Conexão aberta: " << connection_string_ << "\n";
    }

    ~DatabaseConnection() {
        std::cout << "[-] Conexão fechada automaticamente por RAII.\n";
    }

    void execute_query(std::string_view query) const {
        std::cout << "    Executando: " << query << "\n";
    }

private:
    std::string connection_string_;
};

int main() {
    // Alocação segura sem chamar 'new'
    auto db = std::make_unique<DatabaseConnection>("Server=localhost;Port=5432;");
    db->execute_query("SELECT * FROM users;");
    
    // Conexão desalocada automaticamente no término do escopo
    return 0;
}
```

---

## ⚙️ Modern Build System Configuration (CMakeLists.txt C++23)

```cmake
cmake_minimum_required(VERSION 3.26)
project(cpp23_modern_project CXX)

# Impoe o padrão C++23 (ISO/IEC 14882:2024)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(app_main src/main.cpp)

# Bateria estrita de compilação e flags de segurança
if (MSVC)
    target_compile_options(app_main PRIVATE /W4 /WX /permissive-)
else()
    target_compile_options(app_main PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror)
endif()
```

---

## 🔒 Security Issues and Safe Practices

- **Resource Management (RAII)**: Avoid manual management with `new` and `delete`. Use Smart Pointers (`std::unique_ptr`, `std::shared_ptr`) to mitigate Use-After-Free and Memory Leaks.
- **Object Slicing and Type Confusion**: Be careful when converting base-class pointers to derived classes. Use `dynamic_cast` to perform runtime checks safely.
- **Operator Overloading and Copy Constructors**: Avoid resource leaks on object assignment by correctly implementing the copy constructor and assignment operator (Rule of Three/Five/Zero).
- **Virtual Method Injection (vtable hijacking)**: Prevent unintended inheritance by declaring classes or methods as `final` to reduce the attack surface for control-flow hijacking.

## 🔗 Integration with Other Skills

- For direct development and interoperability with C code (C23/C17), see [lang-c](../lang-c/SKILL.md).
- To run unit tests on C++ code using modern frameworks, see [framework-testing](../../frameworks/framework-testing/SKILL.md) and [framework-criterion](../../frameworks/framework-criterion/SKILL.md).
- To audit memory safety, Use-After-Free, buffer overflow, and C++ code security vulnerabilities, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
