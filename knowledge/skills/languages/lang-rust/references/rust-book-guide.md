# Rust — Reference Guide (Official Book / rust-lang.org)

Consolidated from "A Linguagem de Programação Rust" (The Rust Programming Language — rust-br.github.io/rust-book-pt-br) and the official rust-lang.org/pt-BR/learn documentation (The Book, Rust by Example, Rustlings, Cargo Book, Rustonomicon, Reference).

---

## 1. Getting Started (Ch. 1–2)

- **Toolchain via rustup**: `rustup` manages versions of `rustc`, `cargo`, and local docs (`rustup doc`). Components: `rustfmt`, `clippy`.
- **Cargo (essential)**:
  - `cargo new <projeto>` → `src/main.rs` + `Cargo.toml` structure.
  - `cargo build` / `cargo run` / `cargo check` (fast, no binary produced) / `cargo build --release` (optimized).
  - `Cargo.toml`: `[package]` (name, version, edition), `[dependencies]`. **Edition** defines language compatibility (2015/2018/2021) — backward-compatible.
- Default project structure: `src/main.rs` (binary) + `src/lib.rs` (library) + `tests/` (integration).

## 2. Common Concepts (Ch. 3)

- **Variables**: `let` = immutable by default; `let mut` for mutability; `const` (type + computable constant value, `SCREAMING_SNAKE_CASE`).
- **Shadowing**: redeclaring `let` in the same scope replaces the binding (and allows changing the type).
- **Scalar types**: `i8/u8 … i128/u128`, `isize/usize`, `f32/f64` (`f64` default), `bool`, `char` (4 bytes, Unicode).
- **Integers**: `_` literal separator, hexadecimal `0x`, octal `0o`, binary `0b`, byte `b'A'`. Overflow in release **wraps** (`wrapping_add`, `checked_add`, `saturating_add`, `overflowing_add`).
- **Tuples**: `(i32, f64)` with destructuring and `.0/.1` access; unit type `()`.

```rust
fn main() {
    let tup: (i32, f64, char) = (500, 6.4, 'x');
    let (x, y, z) = tup;                    // pattern matching
    let five_hundred = tup.0;
}
```

- **Arrays**: fixed size `[i32; 5]`, allocated on the stack; `a[0]` access; out-of-bounds → **panic** (bounds check).
- **Functions**: `snake_case` names; required parameter types; **the last expression is the return value** (no `;`):
  ```rust
  fn plus_one(x: i32) -> i32 { x + 1 }
  ```
- **Doc comments** `///` become docs in `cargo doc`.
- **Control flow**: `if/else` (the condition must be `bool`, no truthiness); `if` is an expression; **labeled loops** `'outer: loop` and `break 'outer value`/`continue`; `loop` returns a value; `while`; `for x in` over ranges/iterators:
  ```rust
  let r = loop { break 5 * 2; };     // loop como expressão → 10
  for num in (1..4).rev() { ... }
  ```

## 3. Ownership, Borrowing, and Slices (Ch. 4) — Rust's single foundation

- **Ownership rules**:
  1. Every value has **a single owner**.
  2. When the owner goes out of scope, the value is **dropped** (RAII).
  3. Assigning/moving non-Copy values **moves** ownership (shallow copy + invalidates the origin).
- **Stack vs Heap**: types known at compile time go on the stack; `String` (data on the heap) moves, `i32` copies (Copy/Clone).
- **Move semantics**: assigning one `String` to another transfers ownership (`use of moved value` if you use the origin afterward).
- **Copy trait**: integers, floats, bool, char, tuples of Copy types. `Clone` for an explicit deep copy (`s.clone()`).

```rust
let s1 = String::from("olá");
let len = calcular(&s1);            // borrowing — não transfere posse
fn calcular(s: &String) -> usize { s.len() }
let mut s2 = String::from("a");
s2.push_str("b");
let r1 = &s2; let r2 = &s2;         // N referências imutáveis OK
// let r3 = &mut s2;                // ERRO: &mut enquanto há & vivas
let r4 = &mut s2;                   // OK após r1/r2 usarem e morrerem (NLL)
```
- **Borrowing**: `&T` (shared, many) OR `&mut T` (exclusive, one). Never both at the same time.
- **Dangling references** are impossible in safe Rust: the borrow checker guarantees the data outlives the reference.
- **Slices**: a non-owning view over a collection — `&str` (string slice), `&[i32]` (array slice):
  ```rust
  fn first_word(s: &str) -> &str { s.split_whitespace().next().unwrap_or("") }
  // &String é coerível para &str (deref coercion); prefira &str em APIs
  ```

## 4. Structs (Ch. 5)

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,     // tuple structs: struct Point(i32, i32);
}                           // unit structs: struct AlwaysEqual;

impl User {
    fn new(email: String) -> Self {
        User { active: true, username: String::from("anônimo"), email, sign_in_count: 1 } // field init shorthand
    }
    fn email(&self) -> &str { &self.email }              // método (associated function com receiver)
    fn to_upper_email(mut self) -> Self {                 // consumer builder-style
        self.email = self.email.to_uppercase(); self
    }
}
let u = User::new(String::from("a@b.c"));
```
- **Struct update syntax**: `..outro` copies the remaining fields (**moves** the non-Copy ones).
- **Methods** (`&self` = borrow, `&mut self` = mut borrow, `self` = consume) and **associated functions** without a receiver (constructors `::new`).
- Field access can be "out of borrow" (the borrow checker separating fields).

## 5. Enums and Pattern Matching (Ch. 6, 18)

```rust
enum IpAddr { V4(u8, u8, u8, u8), V6(String) }        // enums carregam dados
enum Shape { Circle(f64), Square(f64), Triangle(f64) }

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Square(s) => s * s,
        Shape::Triangle { base, height } => (base * height) / 2.0,
    }
}

enum Option<T> { Some(T), None }           // do core, elimina null
fn dividir(x: f64, y: f64) -> Option<f64> {
    if y == 0.0 { None } else { Some(x / y) }
}

if let Some(val) = talvez_valor() { ... }  // um caso só
let x = 5;                                  // let pode desestruturar
let (a, b) = (1, 2);
```
- **`match` is exhaustive** (every case must be covered; `_` as catch-all).
- Guards `x if x > 5`, `@` bindings (`n @ 1..=5`), `|` or-patterns, `..` ranges, struct/tuple destructuring, matches on `Result`/`Option`.
- **`Option<T>`**: never an implicit `None`; useful methods `.unwrap_or(default)`, `.map`, `.and_then`, `.ok_or(err)`, `.expect("msg")` (only in tests/invariants).

## 6. Modules and Packages (Ch. 7)

- **Package** = 1+ crates; **crate** = the compilation unit (lib or binary); **module** = organizes code inside the crate.
- Modules form a tree; `mod` declares; `pub` makes public; absolute paths (`crate::`) or relative ones (`super::`, `self::`).
- `use` imports (rename with `use foo::bar as baz`), `pub use` re-exports, modules in separate files `mod nome;` → `src/nome.rs` or `src/nome/mod.rs`.
- **Idiom: thin binary crate, library crate with the logic + tests** (`lib.rs` + a small `main.rs`).

## 7. Common Collections (Ch. 8)

| Collection | Description / idiom |
| :--- | :--- |
| `Vec<T>` | dynamic array on the heap (`vec![1,2,3]`, `push/pop`, index with `[]` (panics) or `.get(i) -> Option<&T>`); iterate with `for x in &v`. |
| `String` | UTF-8, `String::from`, `+`/`format!`; index access **does not work** (variable-length UTF-8) — use `chars()`, `bytes()`, or slices that respect character boundaries. |
| `HashMap<K, V>` | `insert`, `get(&k) -> Option<&V>`, entry API (`map.entry(k).or_insert(0)` += 1), `remove`, iteration `for (k, v) in &map` (arbitrary order). |
- Ownership: `insert(s.clone())` or move; common `String` keys; iterators own the values (unless `&map`/`&vec`).

## 8. Error Handling (Ch. 9) — no exceptions

- **`panic!`** = unrecoverable (invariant bug, array OOB, unhandled unwrap). **`Result<T, E>`** = recoverable:
  ```rust
  enum Result<T, E> { Ok(T), Err(E) }
  ```
- **`?`** propagates `Err` and unwraps `Ok` (also on `Option<T>`); it works in functions that return `Result`/`Option`.
- `.unwrap()`/`.expect()` **never in production** (prototype/test/invariant code only).
- Strategy: "Don't enter panic" — use `Result` for expected failures (file, network, parse) and `panic!`/unreachable for programmer bugs.
- Library errors: enumerate with `#[error(...)]` (`thiserror`); apps: `anyhow::Result` + `?` + context `.context("...")`.

## 9. Generics, Traits, and Lifetimes (Ch. 10)

- **Generics**: `<T>` on functions/structs/impls — zerocost via **monomorphization** (code specialized per type at compile time).
  ```rust
  fn maior<T: PartialOrd>(list: &[T]) -> &T { ... }
  struct Point<T> { x: T, y: T }

  impl<T: std::fmt::Display> Point<T> {
      fn print(&self) { println!("{}", self.x); }
  }
  ```
- **Traits = behavior contracts** (interfaces with default methods):
  ```rust
  trait Resumir {
      fn resumir(&self) -> String;
      fn preview(&self) -> String { format!("Lendo: {}", self.resumir()) } // default
  }
  impl Resumir for Artigo { fn resumir(&self) -> String { ... } }
  ```
- **Trait bounds**: `<T: Resumir>`; multiple bounds with `where` or `impl Resumir + Clone`.
- **Returning traits** (opaque types): `fn cria() -> impl Resumir { ... }` (a single type); trait objects `Box<dyn Resumir>` for **dynamic dispatch** (heterogeneous/vtable).
- **Trait objects `dyn Trait`**: `&dyn Trait` or `Box<dyn Trait>` for runtime polymorphism.

### Lifetimes

- They guarantee that references stay valid (**they do not change the lifetime — they only describe it**):

```rust
// Elision rule: 1 ref-input → 1 lifetime de saída implícita
fn maior<'a>(a: &'a str, b: &'a str) -> &'a str { if a.len() > b.len() { a } else { b } }

struct Livro<'a> {
    titulo: &'a str,   // struct não pode sobreviver às suas referências
}
impl<'a> Livro<'a> { fn first(&self) -> &'a str { self.titulo } }
```
- `'static` = lives for the entire program (literals, `Box::leak`).

## 10. Testing (Ch. 11) — integration with cargo test

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn um_mais_um() { assert_eq!(1 + 1, 2); }

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn falha() { let v: Vec<i32> = vec![]; v[0]; }

    #[test]
    fn io_erro() -> Result<(), Box<dyn std::error::Error>> {
        let f = File::open("inexistente")?;
        Ok(())
    }

    #[test]
    #[ignore]
    fn caro() { ... }
}
```
- `cargo test` runs unit tests + integration tests (in `tests/`) + doc-tests.
- Unit tests live next to the module (`#[cfg(test)] mod tests { use super::*; ... }`); integration tests in `tests/*.rs`; docs in `///` with ``` examples.

## 11. Idiomatic I/O Project (Ch. 12) — minigrep

- CLI: `std::env::args()` / `std::env::var`; file reading with `fs::read_to_string`; separate config/search into `src/lib.rs`, I/O into `main.rs`.
- Errors on **stderr**: `eprintln!` (for pipes); `Result<(), Box<dyn Error>>` as the return of main.

## 12. Functional Features — Closures and Iterators (Ch. 13)

```rust
let nums = vec![1, 2, 3, 4, 5];
let soma = nums.iter().filter(|&&x| x % 2 == 0).map(|x| x * 2).sum::<i32>();
// soma com closures capturando por referência/move
let clonado = nums.clone();
let pares = nums.iter().filter(|x| x % 2 == 0).collect::<Vec<_>>();
```
- **Closures**: infer types; capture by borrow (`Fn`), mutably (`FnMut`), or ownership (`FnOnce`); `move` transfers ownership (necessary for threads/tasks).
- **Iterators are lazy** — `.collect()` consumes; **no cost**: compiled to the same native loop.
- Closures/iterators are zero-cost: prefer `.iter().map/filter/sum` over manual loops when they are a classic fit.

## 13. Cargo, Crates.io, and Workspaces (Ch. 14)

- **Release Profile** (`Cargo.toml`):
  ```toml
  [profile.dev]
  opt-level = 0
  [profile.release]
  opt-level = 3
  ```
- `cargo publish` (crates.io) — requires semantic versioning and a README.
- **Cargo Workspaces**: a monorepo with multiple crates sharing a lockfile/target.

## 14. Smart Pointers (Ch. 15) — Box, Rc, RefCell, Arc, Mutex

| Smart Pointer | Idiomatic use |
| :--- | :--- |
| `Box<T>` | heap allocation, known size (recursion, `dyn Trait`). |
| `Rc<T>` | **single-thread** ref counting (not `Send`); cycles require `Weak<T>`. |
| `Arc<T>` | **thread-safe** ref counting (atomic) for sharing between threads. |
| `RefCell<T>` | interior mutability with a **runtime** check (single-thread); `borrow()/borrow_mut()`. |
| `Mutex<T>` / `RwLock<T>` | **thread-safe** interior mutability (lock/guard). |
- **Drop** (`impl Drop for X`) → RAII; **Deref** (auto-coercion `&SmartPtr` → `&T`).

### Reference cycles = leak (even in Rust)
`Rc<RefCell<T>>` with a cycle → leaks. Solution: use `Weak<T>` (`upgrade() -> Option<Rc<T>>`) on the non-owning side.

## 15. Concurrency (Ch. 16) — fearless concurrency

- **OS threads**: `std::thread::spawn(move || ...)`; `join()` waits; data is moved via `move`.
- **Channels**: `std::sync::mpsc::channel()` (`mpsc::Sender/receiver`); ownership transfer by message.
- **Arc + Mutex**: sharing mutability between threads:
  ```rust
  let counter = Arc::new(Mutex::new(0));
  let mut handles = vec![];
  for _ in 0..10 {
      let c = Arc::clone(&counter);
      handles.push(std::thread::spawn(move || { *c.lock().unwrap() += 1; }));
  }
  for h in handles { h.join().unwrap(); }
  ```
- **Send/Sync** marker traits — guarantees enforced by the compiler: `Send` = transferable between threads; `Sync` = shareable (`&T` is Send).
- Modern alternative: **Tokio** (`tokio::spawn`, async/await) for I/O concurrency; `rayon` for data parallelism (par_iter).

## 16. Rust OOP and Design Patterns (Ch. 17)

- Rust **has no classes**; it uses **traits + structs + impl** (composition > inheritance); trait objects `Box<dyn Trait>` for runtime polymorphism; the state pattern via enums that swap states (more idiomatic than OO).

## 17. Advanced Types / Macros / Unsafe (nomicon)

- **Newtype**: `struct Meters(f64);` for type safety.
- **Type aliases**: `type Kilometers = f64;`
- **Never type `!`**: for functions that never return (`panic!`, `continue`, `process::exit`).
- **DST**: `str`, `[T]`, `dyn Trait` (unknown size) — behind `&`/`Box`.
- **Macros**: `macro_rules!` (declarative) and proc macros (`derive`, attribute, function-like) — code that generates code.
- **unsafe**: `unsafe { ... }` enables raw pointer deref, calling FFI, mutating statics, accessing union fields. Encapsulate it in safe abstractions with a `// SAFETY:` comment.

## 18. Keywords at a Glance

`as`, `break`, `const`, `continue`, `crate`, `dyn`, `else`, `enum`, `extern`, `false`, `fn`, `for`, `if`, `impl`, `in`, `let`, `loop`, `match`, `mod`, `move`, `mut`, `pub`, `ref`, `return`, `self`, `Self`, `static`, `struct`, `super`, `trait`, `true`, `type`, `unsafe`, `use`, `where`, `while`, `async`, `await`.
