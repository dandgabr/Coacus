# Rust — Advanced Guide (Programming Rust 2nd ed. + TRPL 3rd ed.)

Consolidated from **Programming Rust, 2nd Edition** (Jim Blandy, Jason Orendorff, Leonora Tindall — O'Reilly) and **The Rust Programming Language, 3rd Edition** (Steve Klabnik, Carol Nichols, Chris Krycho — Rust 1.85+, edition 2024). This guide covers deep topics that complement the [Book guide](rust-book-guide.md): memory layout, advanced traits/generics, unsafe, atomics and memory orderings, `macro_rules!` macros, Pin/Futures, and FFI.

---

## 1. Memory Layout: Sizes, Alignment, and `repr` (Programming Rust, Ch. 8/10)

- **`std::mem::size_of::<T>()`** returns the size in bytes of a value of type `T`; **`std::mem::align_of::<T>()`** returns its alignment:

```rust
use std::mem::{size_of, align_of};

assert_eq!(size_of::<i64>(), 8);
assert_eq!(align_of::<(i32, i32)>(), 4);
```

- For values behind references (slices, DSTs), use `size_of_val` and `align_of_val`, which consult the dynamic type of the value:
  - `size_of_val(slice)` of a `&[u8]` with 5 elements = 5 bytes;
  - `size_of_val(text)` of a `&str` with 9 characters = 9 bytes.
- **Field reordering**: Rust reorders struct fields to minimize total size (reduce padding). Zero-sized types (ZSTs) take up no space. This differs from C, which preserves declaration order.
- **`#[repr(Rust)]`** (default): free layout, optimized by the compiler — do not use it for FFI.
- **`#[repr(C)]`**: fields in declaration order, as a C compiler would lay them out — mandatory for interoperability and for unions whose layout matters:

```rust
#[repr(C)]
union SignExtractor {
    value: i64,
    bytes: [u8; 8],
}

fn sign(int: i64) -> bool {
    let se = SignExtractor { value: int };
    unsafe { se.bytes[7] >= 0b10000000 } // sign bit no byte mais significativo
}
```

- **`#[repr(transparent)]`**: guarantees that a single-field wrapper has exactly the layout of the inner field.
- **`#[repr(u8)` / `#[repr(i16)` / etc.]**: fixes an enum's representation to the size of the given integer (useful for C/C++ enums with explicit integers or for safe casting via controlled `transmute`).
- **Fat pointers**: references to slices (`&[T]`, `&str`) and trait objects (`&dyn Trait`) occupy **two words** — a pointer + metadata (length or vtable):
  - Slice: start address + number of elements.
  - Trait object: pointer to the data + pointer to the **vtable** (generated once at compile time, shared by every object of the same type).
- **`Sized`**: a marker trait implemented automatically for every type whose size is known at compile time; `T: Sized` is the default bound on generics. Unsized types (`str`, `[T]`, `dyn Trait`) can only appear behind `&`, `Box`, `Rc`, etc. The bound `?Sized` relaxes this requirement.
- **Union**: all fields share the same memory; the size is that of the largest field, and only one field is active at a time. Reading a union field is `unsafe` (it can reinterpret bits). With `#[repr(C)]`, all fields start at offset 0, enabling manipulated bit extraction (as in the `SignExtractor` example).

## 2. Advanced Traits and Generics (Programming Rust, Ch. 11; TRPL, Ch. 20)

- **Trait objects (dynamic dispatch)**: `Box<dyn Trait>`, `&dyn Trait`, `Rc<dyn Trait>`. In memory, a trait object is a fat pointer (data + vtable). The vtable is unique per concrete type and generated at compile time.

```rust
let shapes: Vec<Box<dyn Draw>> = vec![Box::new(Button), Box::new(Select)];
for s in &shapes { s.draw(); } // dispatch via vtable
```

- **Object safety**: a trait can only be converted to `dyn Trait` if it is "dyn-compatible": methods without generics and without `Self` by value, no non-receiver associated functions, etc. Traits with associated types only become objects if all associated types are specified (`Box<dyn Iterator<Item = i32>>`).
- **Associated types**: bind an output type to the trait, avoiding repeated annotations at the call site:

```rust
use std::ops::Add;

impl Add for Point {          // trait Add<Rhs=Self> { type Output; fn add(...) ... }
    type Output = Point;
    fn add(self, other: Point) -> Point { /* ... */ }
}
```

  - Use associated types when there is **a single logical output type per implementation** (e.g., `Iterator::Item`). Use generic `<T>` when the same implementation must work with multiple types (`Add<i64> for Point`).
- **Default generic parameters and operator overloading**: `Add<Rhs = Self>` with a default type parameter; operator overloading is done by implementing the `std::ops` traits (`Add`, `Mul`, `Index`, `Fn`, ...).
- **Fully qualified syntax**: resolves ambiguity between methods with the same name (own trait vs. imported trait vs. `Self`):

```rust
<Pilot as Flyable>::fly(&person);   // chama Pilot::fly
<<Wizard as Flyable>::fly>(&person);
```

- **Supertraits**: `trait Player: fmt::Display { ... }` requires implementors to also implement `Display`.
- **Newtype pattern for implementing external traits**: `struct Wrapper(Vec<String>);` gets around the orphan rule (external trait + external type), widely used with `Display` over `Vec`.
- **`impl Trait`** (static dispatch via type erasure in signatures):
  - `fn make_adder(x: i32) -> impl Fn(i32) -> i32` — returns a closure without naming the concrete type (one type per function).
  - Unlike `dyn Trait` behind `&`/`Box`: `impl Trait` is static (monomorphized) and does not allow returning heterogeneous types.

## 3. Advanced Unsafe (Programming Rust, Ch. 22; TRPL, Ch. 20)

- **Raw pointers (`*const T`, `*mut T`)**:
  - They can be null, misaligned, and point to freed memory — **dereferencing is always `unsafe`**.
  - Safe Rust can create raw pointers from references (`let p = &mut v[0] as *mut i32;`); arbitrary numbers cannot be dereferenced.
  - They differ from references: no validity guarantee, no exclusive aliasing (which enables fewer optimizations; use `&T`/`&mut T` whenever possible).
- **`unsafe fn`**: declares that the whole function imposes contracts on the caller; the body may operate like an `unsafe` block. Calling it is `unsafe`. Idiomatically, prefix it with `unsafe_` (`Vec::from_raw_parts`-style) and document the precondition.
- **Unsafe traits**: a trait whose contract the compiler does not verify — implementors must manually uphold the invariant:

```rust
pub unsafe trait Zeroable {}

unsafe impl Zeroable for u8 {}   // zeroizar um i8 é seguro
// unsafe impl Zeroable for &T {} // ERRADO: &T zeroizada é null reference
```

  - **`Send` and `Sync` are the canonical unsafe traits**: `Send` requires safety when moving between threads; `Sync` requires safety of shared access (`&T: Send`). Implementing them for inappropriate types destroys the safety of the whole ecosystem (for example, it would make `Mutex` unsafe).
- **Unions**: declared as in C; constructing/assigning fields is safe, but **reading is `unsafe`**. Always use `#[repr(C)]` when a union crosses a boundary with C.
- **Miri** (TRPL 3rd ed., Ch. 20): the official dynamic verifier (`rustup +nightly component add miri` + `cargo +nightly miri test`) for detecting undefined behavior in unsafe code — use it as part of the test suite for unsafe abstractions.

## 4. Detailed Concurrency: Atomics, Memory Orderings, Scoped Threads (Programming Rust, Ch. 19)

- **Atomics (`std::sync::atomic`)**: `AtomicBool`, `AtomicIsize/Usize`, `AtomicI8..I64/AtomicU8..U64`, `AtomicPtr<T>`. Multiple threads can read/write without data races. Methods instead of operators:

```rust
use std::sync::atomic::{AtomicIsize, Ordering};

let atom = AtomicIsize::new(0);
atom.fetch_add(1, Ordering::SeqCst);  // x86-64: lock incq (lock-free)
```

- **Memory orderings (`Ordering`)** — analogous to database transaction isolation levels: they define how strong the causality/time guarantees are versus performance:
  - `SeqCst` (sequentially consistent): the strictest — all operations appear in a single global order. **When in doubt, use `Ordering::SeqCst`** (the performance penalty is usually small).
  - `Acquire`/`Release`: producer-consumer pairs for memory consistency (a release store → an acquire load publishes/observes prior writes).
  - `Relaxed`: guarantees only the atomicity of the individual operation, with no ordering between threads (for independent counters).
  - Rust inherits the orderings from the Standard C++ atomics model; getting orderings wrong causes data races the compiler does not detect.
- **Idiomatic use of AtomicBool: a cancellation flag** between threads (shared in `Arc<AtomicBool>`), checked at checkpoints in the work loop.
- **`std::thread::JoinHandle`**: `thread::spawn` returns `JoinHandle<T>`; `.join()` waits and returns `Result<T, Box<dyn Error>>` (the thread may have panicked).
- **Scoped threads (`std::thread::scope`)**: fork-join with borrowing — the scope's threads can reference local data from the frame that created them, without `Arc`, because the scope guarantees they all finish before it returns:

```rust
let mut results = vec![];
std::thread::scope(|s| {
    for chunk in data.chunks_mut(1000) {
        s.spawn(|| results.push(process(chunk))); // &mut borrowing direto
    }
}); // todas as threads morrem antes de `results` ser usado
```

- **Channels and locks**: remember that `mpsc::Receiver` is single-consumer; for work-stealing between workers use `Arc<Mutex<Receiver<T>>>` or `crossbeam-channel` (which also offers scoped threads and MPMC). `Mutex::lock()` returns `LockResult<Guard>` — the `MutexGuard` implements `Deref/DerefMut` and releases on scope exit (RAII); deadlocks are avoidable with a fixed lock order.
- **`catch_unwind` and panics between threads**: `std::panic::catch_unwind()` catches panic unwinding (used by the test harness); useful for isolating worker threads. Panics in nested `Drop` or `-C panic=abort` abort the entire process.

## 5. Declarative Macros with `macro_rules!` (Programming Rust, Ch. 21; TRPL, Ch. 20)

- `macro_rules!` operates by **pattern matching tokens** (not characters): patterns consume typed fragments, and the template substitutes `$name` with the captured fragment.

```rust
macro_rules! log {
    ($left:expr, $right:expr) => {
        eprintln!("{} / {}", stringify!($left), stringify!($right));
    };
}
```

- **Common errors**: writing `$left:expr` in the **template** (only the pattern should have it!) makes the macro inject spurious `: expr` tokens — the error only shows up at the call site (`cannot find type 'expr' in this scope`). Use only `$left`.
- **Fragment specifiers (Table 21-2 — Programming Rust)**:

| Fragment | Matches | May be followed by |
| :--- | :--- | :--- |
| `expr` | expression: `2 + 2`, `"udon"`, `x.len()` | `=>`, `,`, `;` |
| `stmt` | expression or statement | `=>`, `,`, `;` |
| `ty` | type: `String`, `Vec<u8>` | `=>`, `,`, `;`, `=`, `\|`, `{`, `[`, `:`, `>`, `as`, `where` |
| `path` | path: `fern`, `::std::sync::mpsc` | same as `ty` |
| `pat` | pattern: `_`, `Some(ref x)` | `=>`, `,`, `=`, `\|`, `if`, `in` |
| `item` | item: `struct Point {...}`, `mod ferns` | any |
| `block` | block: `{ s += "ok\n"; true }` | any |
| `meta` | attribute body: `inline`, `derive(Copy, Clone)` | any |
| `ident` | identifier: `std`, `Json` | any |
| `literal` | literal: `1024`, `"Hello"`, `1_000_000f64` | any |
| `lifetime` | `'a`, `'static` | any |
| `vis` | visibility: `pub`, `pub(crate)` | any |
| `tt` | token tree | any |

- **Repetitions**: `$( $x:expr ),+` (one or more, comma-separated), `$( ... ),*` (zero or more); support for an optional trailing comma to allow both forms.

```rust
macro_rules! vec_shortcut {
    ( $( $x:expr ),+ , ) => { {
        let mut v = Vec::new();
        $( v.push($x); )+
        v
    } };
    ( $( $x:expr ),+ ) => { vec_shortcut![ $( $x ),+ , ] };
}
```

- **Useful built-in macros**: `file!()`, `line!()`, `column!()`, `stringify!`, `concat!`, `cfg!`, `env!`. For complex metaprogramming (custom derive, attribute macro, function-like macro), use **proc macros** (the `syn` + `quote` crates).
- **Hygiene**: identifiers created in the template do not leak to the call site; captured fragments preserve the source code's original visibility.

## 6. Pin/Unpin and the Internals of Futures/Async (TRPL 3rd ed., Ch. 17; Programming Rust, Ch. 20)

- **`async fn` desugars**: `async fn f() -> T` is roughly `fn f() -> impl Future<Output = T>`. The body compiles into a **state machine** that produces a `Future`. `async` blocks (`async move { ... }` moves captures by ownership) create anonymous futures.

```rust
use std::future::Future;

async fn page_title(url: &str) -> Option<String> {
    // equivalente a: fn page_title<'a>(url: &'a str) -> impl Future<Output = Option<String>> + 'a
    // o futuro retém os parâmetros emprestados, tornando o Future 'a
    /* ... */
}
```

- **The `Future` trait** (std::future):

```rust
trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

enum Poll<T> { Ready(T), Pending }
```

  - The runtime does the polling; the Future signals readiness via a `Waker` (inside `Context`) so it gets re-polled when the data arrives — the executor does not busy-wait.
- **Pin/Unpin**: futures are often **self-referential** (they hold pointers to their own fields). If a future moves in memory between polls, those internal pointers become invalid. Therefore:
  - `Pin<&mut T>` guarantees the value **will not move** in memory while it is pinned.
  - Most common types (`i32`, `String`, ordinary async closures) are **`Unpin`**: no real pinning is needed, and `Pin<&mut T>` behaves like `&mut T`.
  - A Future that captures references (e.g., generated from an `async fn` with `&str` parameters) is **not Unpin**; to `.poll()` it manually, use `Box::pin(my_future).as_mut().poll(&mut cx)`.

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

fn do_poll<F: Future>(fut: Pin<&mut F>, cx: &mut Context) -> Poll<F::Output> {
    fut.poll(cx) // método poll exige Pin<&mut Self>
}
```

  - `Unpin` is a marker trait auto-implemented for every type whose movement is safe. Combining it with async generics uses `F: Future + Unpin` as a practical bound for manual polling loops.
- **The `Stream` trait**: the asynchronous analogue of `Iterator` — `poll_next` returns `Poll<Option<Item>>` (`Some` = item available; `None` = end). Combinators such as `map`, `filter`, and `timeouts` work through ecosystem extension traits (`futures::StreamExt`).
- **Asynchronous concurrency in practice**: a sequential `.await` runs in series; `tokio::join!`/`try_join!` or `FuturesUnordered` run concurrently. Use `select!` to compose races across multiple effect paths.

## 7. Detailed FFI: `repr(C)`, Strings, Panic Safety (Programming Rust, Ch. 23)

- **C-compatible types**: `std::os::raw::{c_char, c_int, c_uchar, ...}` map 1:1 to the usual C types on every supported platform. `usize` ↔ `size_t` are identical.
- **C-compatible structs**: use `#[repr(C)]` — fields in declaration order, no reordering. Each individual field must also be a C-like type. Without `#[repr(C)]`, Rust reorders fields and ZSTs occupy zero bytes:

```rust
use std::os::raw::{c_char, c_int};

#[repr(C)]
pub struct git_error {
    pub message: *const c_char,
    pub klass: c_int,
}
```

- **Enums**: by default, Rust uses 1 byte for variants without data; `#[repr(C)]` forces the size of `c_int`. For an exact representation of a 16-bit C enum, use `#[repr(i16)]`. Enums with payload (Rust-style tagged unions) **are not** FFI-safe — instead, model a tag + union:

```rust
#[repr(C)] #[derive(Clone, Copy)] pub enum Tag { Float = 0, Int = 1 }

#[repr(C)] pub union FloatOrInt { f: f64, i: i64 }

#[repr(C)] pub struct Value { pub tag: Tag, pub union: FloatOrInt }
```

- **Opaque types**: for C handle types (which Rust only passes around), declare empty ZST structs (`#[repr(C)] pub struct git_repository { _private: [u8; 0] }`) and use opaque `*const`/`*mut`.
- **Extern block**: declares functions defined in another library (linked at the final stage). Functions declared in `extern "C" {}` are `unsafe` by default (calling them requires an `unsafe` block):

```rust
use std::os::raw::c_char;

extern {
    fn strlen(s: *const c_char) -> usize;
}

#[link(name = "git2")]   // linka libgit2
extern {
    pub fn git_libgit2_init() -> c_int;
    pub fn git_repository_open(out: *mut *mut git_repository, path: *const c_char) -> c_int;
}
```

- **Strings — CString/CStr**: `String`/`&str` are not null-terminated and may contain internal null bytes. Never pass a `&str` directly to C. Use:
  - `CString::new(rust_str)` → an owned null-terminated string (fails with `NulError` if the body has an internal `\0`);
  - `c_string.as_ptr()` → `*const c_char` for C functions;
  - `CStr::from_ptr(ptr)` (for bytes borrowed from C) → `to_str() -> Result<&str, Utf8Error>` to convert to `&str` (checks UTF-8).
- **Callbacks — exposing Rust to C**: use `#[no_mangle] extern "C" fn` to export Rust functions; calling through a function pointer only works with C-style conversions. In modern Rust, FFI signatures should use `unsafe extern "C"` if the bodies involve `unsafe`.
- **Panic safety across the boundary**:
  - Unwinding **through C/C++ code is undefined behavior** — a panic in a Rust function called by C can cross C frames and corrupt the process state.
  - Use `std::panic::catch_unwind` at the boundary to catch panics and convert them into return codes/C error codes, or configure the runtime with `panic = "abort"` to abort immediately instead of unwinding.
  - `panic=abort` reduces binary size (no unwinding table needed) but removes the ability to `catch_unwind`.
  - Remember that `catch_unwind` only intercepts panics that unwind — with `abort`, the program dies on the first panic.
- **bindgen/cbindgen**: for extensive C headers, the `bindgen` crate generates `#[repr(C)]` declarations and `extern` blocks from `.h` headers; to generate C headers from Rust APIs, use `cbindgen`.
- **Best practices**: treat the external API as **unsafe by definition** in an internal `raw` module; build **safe wrappers** that translate C contracts (null-terminated, implicit lifetimes, error codes) into idiomatic Rust types (`Result<T, E>`, `&str`, RAII `Drop` for `*_free`).

---

## Chapter References

- Programming Rust 2nd ed.: Ch. 8 (Structs/Layout), Ch. 10–11 (Generics/Traits/fat pointers), Ch. 13 (Utility Traits/Sized), Ch. 19 (Concurrency/Atomics), Ch. 21 (Macros), Ch. 22 (Unsafe), Ch. 23 (FFI/libgit2).
- TRPL 3rd ed. (edition 2024, Rust 1.85+): Ch. 17 (Async Fundamentals, Future/Stream/Pin), Ch. 19 (Patterns and `let else`), Ch. 20 (Advanced Features, Advanced Traits, Macros, unsafe + introduction to Miri), Appendix E (Editions).
