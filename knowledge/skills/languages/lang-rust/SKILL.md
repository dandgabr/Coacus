---
name: "lang-rust"
description: "Provides software engineering patterns in Rust based on the official documentation (doc.rust-lang.org), the Brazilian Portuguese translation 'A Linguagem de Programação Rust' (rust-br.github.io/rust-book-pt-br), 'The Rust Programming Language 3rd Edition' (Klabnik, Nichols, Krycho), and 'Programming Rust 2nd Edition' (Blandy, Orendorff, Tindall), covering Ownership, Borrowing, Lifetimes, Structs, Enums and exhaustive Pattern Matching, Modules and Crates, Collections (Vec/String/HashMap), error handling (Result/Option/thiserror), Generics and Traits, zero-cost Closures and Iterators, Smart Pointers (Box/Rc/Arc/RefCell/Mutex), Concurrency (threads, channels, Send/Sync), Async (Tokio), Testing (cargo test), Cargo Workspaces and Profiles, Unsafe Rust/Nomicon, and FFI."
---

# AI Skill: Rust Engineering (Rust Specialist)

This skill guides the AI to act as a specialist in the **Rust** language, following strictly the guidelines of the official documentation ([rust-lang.org/pt-BR/learn](https://www.rust-lang.org/pt-BR/learn)) — *The Book* (The Rust Programming Language, with a [pt-BR translation](https://rust-br.github.io/rust-book-pt-br/title-page.html)), *Rust by Example*, *Rustlings*, *The Cargo Book*, *The Rustonomicon*, and the *Reference* — always via `rustup doc` for offline consultation. The goal is to create code that is safe against data races, free of memory leaks (no Garbage Collector), concurrent, and extremely performant.

> 📖 **Canonical reference**: see [references/rust-book-guide.md](references/rust-book-guide.md) for the consolidated guide to the Book's chapters (common concepts, ownership/borrowing/slices, structs, enums and match, modules, collections, errors, generics/traits/lifetimes, testing, closures/iterators, Cargo/workspaces, smart pointers, concurrency, advanced patterns, and keywords).
> 📖 **Advanced reference**: see [references/programming-rust-advanced-guide.md](references/programming-rust-advanced-guide.md) for deep topics (memory layout/size/align, advanced traits and generics, unsafe/raw pointers/unions/unsafe traits, atomics and memory orderings, `macro_rules!` macros with fragment specifiers, Pin/Unpin and Futures internals, FFI with `repr(C)`, and panic safety).

---

## 🧭 General Rust Development Guidelines

While working under this skill, apply strictly the fundamentals of memory safety and fearless concurrency:

### 1. Ownership, Borrowing, and Lifetimes
- **Single Ownership**: Every value in Rust has a single owner at a time. When the owner goes out of scope, the value is deallocated automatically via the `Drop` trait (RAII).
- **Move Semantics**: Assigning non-Copy types (e.g., `String`) transfers ownership and invalidates the source ("use of moved value"). `Copy` types (integers, floats, bool, char) copy implicitly; a deep copy is explicit with `.clone()`.
- **Borrowing Rules**:
  - You may have any number of immutable references (`&T`) **OR** exactly one mutable reference (`&mut T`) within a given scope, but never both simultaneously.
  - References must always be valid (prevention of dangling pointers).
- **Slices (`&str`, `&[T]`)**: Prefer borrowed views in API signatures — `fn first_word(s: &str) -> &str` instead of `&String`, taking advantage of deref coercion.
- **Lifetimes**:
  - Use explicit lifetime annotations (`'a`) on structs and functions only when the compiler cannot elide them under the Lifetime Elision Rules.
  - In structs that hold references, ensure the struct does not outlive the borrowed data (`struct Book<'a> { title: &'a str }`).

### 2. Idiomatic Data Modeling (Structs, Enums, and Pattern Matching)
- **Structs + `impl`**: fields private by default (exposed with `pub`), methods with `&self`/`&mut self`/`self`, and constructors as associated functions (`::new`). Document with `///`.
- **Enums with data**: Model states and messages as an `enum` with payloads (`enum Shape { Circle(f64), Square { side: f64 } }`) — equivalent to discriminated unions.
- **Exhaustive `match`**: The compiler requires full case coverage; use guards (`x if x > 5`), `@` bindings, or-patterns `|`, and destructuring. For a single case, prefer `if let` / `let else`.
- **Preference for `Option<T>`**: The absence of a value is always explicit — there will never be `null`/`NullPointerException`; `.unwrap_or`, `.map`, `.and_then`, `.ok_or(err)` compose safely.
- **Newtypes**: `struct Meters(f64);` for type-safety in units and domain invariants.

### 3. Idiomatic Error Handling (`Result` and `Option`)
- **No Runtime Exceptions**: Rust does not use exceptions. Recoverable errors must be represented by the enum type `Result<T, E>` (`Ok`/`Err`) and optional values by `Option<T>`; programmer invariant failures use `panic!`.
- **Propagation Operator `?`**: Prefer propagating errors using the `?` operator instead of repeated `match` calls or `.unwrap()`.
- **Ban on `.unwrap()` in Production**: Avoid `.unwrap()` and `.expect()` in production code, except in unit tests or mathematically proven invariants.
- **Panics as a DoS Vector**: Prefer non-panicking methods — `.get(i)` instead of `v[i]`, `checked_add`/`saturating_add` instead of arithmetic operators on untrusted inputs.
- **Chained Error Handling**: Use established crates such as `thiserror` (for defining library errors) and `anyhow` (for flexible error handling in binary applications, with `.context()`).

### 4. Zero-Cost Abstraction, Traits, and Generics
- **Trait-Based Polymorphism**: Define shared behavior using `trait` (with default methods). Prefer static dispatch (*monomorphization*) using `impl Trait` or generics `<T: Trait>` with bounds in `where`.
- **Dynamic Dispatch (`dyn Trait`)**: Use `Box<dyn Trait>` only when it is strictly necessary to allocate heterogeneous types at runtime (dynamic dispatch via vtable).
- **Closures and Iterators (Ch. 13)**: Prefer the zero-cost functional style — `iter().filter().map().sum()` compiles to a native loop. Understand the closure capture traits: `Fn` (borrow), `FnMut` (mutable borrow), `FnOnce` (consume); use `move` when transferring data to threads/tasks.
- **Automatic Derivations**: Use decorator attributes such as `#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]` on structs and enums whenever appropriate.

### 5. Project Organization (Modules, Crates, and Cargo)
- **Structure**: Package → crates (lib/binary) → modules (`mod`/`pub`/`use`/`super::`/`crate::`). Standard idiom: **a library crate with the logic + a thin binary crate** (minimal `main.rs`).
- **Cargo.toml**: declare the edition (2015/2018/2021), dependencies (with features), and **profiles** (`[profile.release] opt-level = 3`); use `cargo check` for fast iteration, `cargo test` for all test levels (unit, integration in `tests/`, doc-tests).
- **Workspace**: monorepos with multiple crates sharing `Cargo.lock`/`target` (Cargo Workspaces).
- **Code Quality and Formatting**:
  - **`rustfmt`**: Strict official code formatting (`cargo fmt`).
  - **`clippy`**: Official linter to catch anti-patterns and optimizations (`cargo clippy -- -D warnings`).
- **Dependency Security**: Run `cargo audit` periodically to check third-party crates for known vulnerabilities.

### 6. Concurrency and Asynchronous Programming (`Async/Await`)
- **Static Concurrent Safety**: Types that can be transferred safely between threads implement the marker trait `Send`. Types that can be accessed concurrently through immutable references implement `Sync`.
- **Primitive Synchronization**: Use `Arc<T>` (Atomic Reference Counting) for shared ownership across threads and `Mutex<T>` or `RwLock<T>` for concurrent interior mutability.
- **Asynchronous Ecosystem (`Future`)**:
  - Use the `async/await` pattern with an established async runtime such as **Tokio** or `async-std`.
  - Avoid synchronous I/O blocking in async tasks (use `tokio::task::spawn_blocking` when necessary).

### 7. Unsafe Rust and FFI
- **Strict Encapsulation of `unsafe`**: Isolate `unsafe` blocks inside fully safe abstractions and public functions (*safe wrappers*).
- **Safety Invariants**: Document the preconditions and safety invariants in detail (`// SAFETY: ...`) on every `unsafe` block.
- **FFI (Foreign Function Interface)**: Use `extern "C"` and C-compatible types (`c_char`, `c_int`) for safe interoperability with C/C++.

## 🚀 Modern Rust (Edition 2024 / TRPL 3rd ed.)

In its 3rd edition (Rust 1.85+), the Book reflects the idioms of the **2024 edition** — declared with `edition = "2024"` in `Cargo.toml`. Highlights:

- **Async as a canonical chapter**: the 3rd ed. brings a new Chapter 17 (Fundamentals of Asynchronous Programming) covering `async`/`await` together with the `Future` and `Stream` traits — it is no longer an "advanced" appendix.
- **`let else`**: for refutable patterns, `let Some(x) = value else { return; };` handles the non-matching case with an exit (diverging) block instead of propagating `Option` (TRPL, Ch. 19). Non-exhaustive pattern errors in `let` suggest migrating to `let else`.
- **`Future` trait objects**: `dyn Future<Output = ()>` is not `Unpin` — the compiler will point to `Box::pin` when it is necessary to pin heterogeneous futures collected in `Box<dyn Future>` (TRPL, Ch. 17, Pin/Unpin).
- **`Box<dyn Error>` as the default error type**: returning `Result<T, Box<dyn Error>>` in `main` and in tests accepts any error type via `?` — the idiomatic 3rd ed. pattern for applications before migrating to `anyhow`.

```rust
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let greeting_file = File::open("greeting.txt")?;
    Ok(())
}
```

- **`anyhow` in applications**: for binaries, `anyhow::Result` + `?` + `.context(...)` provides a root-cause report with a backtrace (Programming Rust, Ch. 7); for libraries, keep `thiserror`.
- **Generics over arrays via const bounds**: `[T; N]` with a constant `N` enables generic APIs over array size (Programming Rust, Ch. 5 and Ch. 10).
- **Async closures**: the body of an `async fn` compiles to an `async move` block that retains parameters by ownership — prefer `async move` when transferring captures into tasks (TRPL, Ch. 17).
- **Miri for unsafe**: the 3rd ed. introduces the use of `cargo +nightly miri` as a dynamic verifier of undefined behavior in `unsafe` code (Ch. 20).
- **Guaranteed compatibility**: editions are backward-compatible — code from earlier editions keeps compiling with the correct `edition` in `Cargo.toml` (Appendix E).

---

## 🛠️ Tooling and Project Management (Cargo & Toolchain)

- **Dependency Configuration (`Cargo.toml`)**:
  - Define dependencies, optional features, and compilation profiles.
  - Use `cargo check` during development for fast compiles without machine code generation.
- **Code Quality and Formatting**:
  - **`rustfmt`**: Strict official code formatting (`cargo fmt`).
  - **`clippy`**: Official linter to catch anti-patterns and optimizations (`cargo clippy -- -D warnings`).
- **Dependency Security**: Run `cargo audit` periodically to check third-party crates for known vulnerabilities.

---

## 🧰 Recommended Code Patterns

### 1. Idiomatic Error Handling with `Result` and `thiserror`
```rust
use std::fs::File;
use std::io::{self, Read};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("falha de E/S ao ler o arquivo de configuração")]
    Io(#[from] io::Error),
    #[error("formato de configuração inválido: {0}")]
    InvalidFormat(String),
}

pub fn read_config(path: &str) -> Result<String, ConfigError> {
    let mut file = File::open(path)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    
    if content.is_empty() {
        return Err(ConfigError::InvalidFormat("arquivo vazio".into()));
    }
    
    Ok(content)
}
```

### 2. Asynchronous Concurrency with Tokio and Channels
```rust
use tokio::sync::mpsc;
use tokio::task;

#[derive(Debug)]
pub struct WorkItem {
    pub id: u64,
    pub payload: String,
}

pub async fn run_pipeline(items: Vec<WorkItem>) {
    let (tx, mut rx) = mpsc::channel::<String>(32);

    for item in items {
        let tx_clone = tx.clone();
        task::spawn(async move {
            let result = format!("Processado item {}: {}", item.id, item.payload);
            let _ = tx_clone.send(result).await;
        });
    }

    drop(tx); // Fecha o transmissor original para permitir que o receptor termine quando as tasks concluírem

    while let Some(message) = rx.recv().await {
        println!("[+] Recebido: {}", message);
    }
}
```

### 3. Builder Pattern with Static Validation
```rust
#[derive(Debug)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
}

pub struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
}

impl ServerConfigBuilder {
    pub fn new() -> Self {
        Self { host: None, port: None }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn build(self) -> Result<ServerConfig, &'static str> {
        let host = self.host.ok_or("host é obrigatório")?;
        let port = self.port.unwrap_or(8080);
        Ok(ServerConfig { host, port })
    }
}
```

---

## 🔒 Security Issues and Safe Practices

- **Unsafe Blocks and Undefined Behavior**: Isolate `unsafe` blocks to the strict minimum (raw pointer deref, FFI, static mutation, union field access). Make sure the memory-safety assumptions Rust requires are respected, avoiding data misalignment or null references. Document with `// SAFETY: ...`.
- **Reference Cycles Leak Memory Even in Rust**: `Rc<RefCell<T>>` with a cycle destroys the release guarantees — use `Weak<T>` (with `upgrade() -> Option<Rc<T>>`) on the non-owning side of the cycle.
- **Interior Mutability**: `RefCell<T>` violates borrowing rules at **runtime** (panic on a duplicate `borrow_mut`) — restrict it to single-threaded and small surfaces; between threads use `Mutex<T>`/`RwLock<T>` and avoid deadlock (lock in a fixed order, release the guard early).
- **Data Races in Unsafe**: Although the Rust compiler guarantees the thread-safety of safe code, incorrect use of `Send`/`Sync` and raw pointers inside `unsafe` blocks can introduce complex race conditions.
- **Panics as a DoS Vector**: Strict arithmetic operations or vector index accesses can cause a `panic!` at runtime if they fail. Use safe methods such as `.get()` or `.checked_add()` to avoid sudden service interruptions.
- **UTF-8 Strings**: Never index a `String` by byte (it can cut a multibyte character/freeze) — iterate with `chars()`/`bytes()` or use slices at valid character boundaries.
- **Arithmetic Overflow**: in release, overflow wraps silently — validate inputs before operating; for counters/protocols use Checked/Saturating APIs.

## 🔗 Integration with Other Skills

- To apply static analysis and security review to Rust code, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- To integrate compile-time verified database access in Rust (`sqlx`, `diesel`, `tokio-postgres`, `mongodb`), see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md), [db-postgresql](../../data/db-postgresql/SKILL.md), [db-sqlite](../../data/db-sqlite/SKILL.md), [db-mariadb](../../data/db-mariadb/SKILL.md), and [db-mongodb](../../data/db-mongodb/SKILL.md).
- To develop offensive tools, security agents, or high-performance parsers in Rust, see [pentest-scripter-python-bash-go](../../security/appsec/pentest-scripter-python-bash-go/SKILL.md).
- To model the architecture and communication between software components using Rust, see [software-architect](../../roles/software-architect/SKILL.md).
