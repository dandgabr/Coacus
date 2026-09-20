# WebAssembly: The Definitive Guide (Brian Sletten) — Consolidated Notes

> Source: *WebAssembly: The Definitive Guide — Safe, Fast, and Portable Code* (Brian Sletten, O'Reilly, 2022).
> Complements [wasm-mdn-guide.md](wasm-mdn-guide.md) (the MDN guide) with the perspective of the toolchain, WASI, Emscripten, and execution outside the browser.

---

## 1. Execution Model and Modules (ch. 1–3)

- WebAssembly was conceived for software that is **safe, fast, portable, and compact** — not as a replacement for JavaScript, but as a complement within the same VM.
- A **module** is the compiled (binary) form of a program; execution requires: loading/validating bytes → satisfying imports (functions, memories, globals) → instantiating (`Instance`) → invoking exports or running `start`.
- The binary format is sectioned (types, imports, functions, tables, memory, globals, exports, start, elem, code, data, custom). Use `wasm-objdump -x` to inspect each section.
- **Linear memory** is the only by-value data channel between host and guest; `Memory` is an `ArrayBuffer` (or `SharedArrayBuffer`) in 64 KB pages. Strings/structures must be serialized into memory + passed (pointer, length).
- **Tables** decouple function pointers from `code` and enable **dynamic linking** (side modules with `-s SIDE_MODULE=1`; main module with `MAIN_MODULE=1`).
- The MVP deliberately left out threads, GC, and exceptions (they did not exist in every language) — they all return as independent *proposals*, adopted by runtimes incrementally (ch. 12).

## 2. WABT Toolchain (ch. 2–3, Appendix)

Install via **wabt** (brew/apt/npm) or from the [WebAssembly Binary Toolkit](https://github.com/WebAssembly/wabt). Tools cited in the book:

| Tool | Use |
|---|---|
| `wat2wasm` | Converts text `.wat` → binary `.wasm` |
| `wasm2wat` | Converts the binary back to text (reading/debugging) |
| `wasm-objdump` | Inspects sections/symbols (`-x` for detail; `-d` for disassembly) |
| `wasm-interp` | Runs modules directly in the terminal (a wasm REPL) |
| `wasm-validate` | Validates the binary's conformance |
| `wasm2c` | Generates C code from a wasm binary (native embedding) |

The book's patterns for building modules "by hand":

```bash
wat2wasm hello.wat -o hello.wasm
wasm-objdump -x hello.wasm
# preserve function/local names for debugging (Custom section):
wat2wasm hello.wat -o hellodebug.wasm --debug-names
wasm-objdump -x hellodebug.wasm
```

- Without `--debug-names`, objdump shows only numeric indices; function/local *names* live in a **Custom section** that is not observable through the semantics.
- Modules can live in files or inline in JS via `WebAssembly.Module` from bytes; the book demonstrates a REPL with `wasm-interp` and, in the browser, with the minimal glue of `instantiateStreaming`.

## 3. WASI — WebAssembly System Interface (ch. 11–12)

- **Problem**: the wasm MVP has no I/O; every host would reinvent access to files, the console, time, RNG, and sockets. WASI standardizes a portable and secure *contract*.
- The module imports functions from the `wasi_snapshot_preview1` namespace (historically `wasi_unstable`), e.g., `fd_write` (stdout), `fd_read`, `proc_exit`, `environ_get`, `random_get`, `clock_time_get`.
- A WASI module exports `memory` and `_start` (the program's `main`). A minimal `fd_write` example in Wat (from the Wasmtime tutorial reproduced in the book):

```wat
(module
  (import "wasi_unstable" "fd_write"
    (func $fd_write (param i32 i32 i32 i32) (result i32)))
  (memory 1)
  (export "memory" (memory 0))
  (data (i32.const 8) "hello world\n")
  (func $main (export "_start")
    ;; iov.iov_base = 8, iov.iov_len = 12, io = fd 1 (stdout)
    (i32.store (i32.const 0) (i32.const 8))
    (i32.store (i32.const 4) (i32.const 12))
    (call $fd_write (i32.const 1) (i32.const 0) (i32.const 1) (i32.const 20))
    drop))
```

```bash
wasmtime hello.wat   # WASI hosts executam .wat diretamente
wasmer  hello.wat
```

- **Capability-based security**: the module does not receive direct access to file handles/sockets — it receives *opaque, unforgeable handles* ("preopened file descriptors"). Without the capability, the libc call fails:

```bash
# falha: sem capability de escrita no diretório atual
wasmtime target/wasm32-wasi/release/hello-fs.wasm
# funciona: concede o diretório como preopen
wasmtime --dir=. target/wasm32-wasi/release/hello-fs.wasm
wasmer  --dir=. target/wasm32-wasi/release/hello-fs.wasm
```

- **Toolchains**: `clang` + **wasi-sdk** (the WASI sysroot for C/C++), Rust with `cargo build --target wasm32-wasi`, or `cargo install cargo-wasi` + `cargo wasi run`.
- **WASI runtimes** cited: **Wasmtime** (Bytecode Alliance, formerly Mozilla), **Wasmer**, **wasm3**, **WasmEdge** (blockchains/vehicles); platforms: Istio/Envoy plugins, Fastly Compute@Edge, Cloudflare Workers, wasmCloud (actors), Krustlet (Kubernetes).

### Embedded Runtimes via Wasmtime (Rust host)

Wasmtime's central types: `Engine` (configuration shareable between threads) → `Store` (the isolation unit; objects do not leak between Stores) → `Module` (the compiled form) → `Instance` (module + state).

```rust
use wasmtime::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let engine = Engine::default();
    let mut store = Store::new(&engine, ());
    let module = Module::from_file(&engine, "hello.wat")?;
    let instance = Instance::new(&mut store, &module, &[])?;
    let how_old =
        instance.get_typed_func::<(i32, i32), (i32), _>(&mut store, "how_old")?;
    let age: i32 = how_old.call(&mut store, (2021i32, 2000i32))?;
    println!("You are {age}");
    Ok(())
}
```

There is also an equivalent API in **bash** (`wasmtime hello.wat --invoke how_old 2021 2000`) and bindings for C/Python/.NET. Host use cases: secure plug-ins, serverless, proxy filters, hot-swap, rules/blockchain engines.

### Host ↔ Guest Patterns (Hoffman, ch. 6 + Sletten)

A "good host" must: (1) **load and validate** the wasm binary; (2) **expose exports** with invocation glue; (3) **satisfy imports** or fail with a clear error; (4) **execute the module** (including `start`); (5) **isolate modules** — a module cannot call another's private functions or corrupt its data; a failure in one module must never bring down the host or another module.

## 4. Emscripten (ch. 5–6)

- Based on **LLVM**; it generates `.wasm` + JS glue (and optional HTML). It is the practical route for porting legacy C/C++ code: it provides `emcc`, wasm versions of `cc`, `make`, `configure`, a partial libc, SDL, and OpenGL over Web APIs.
- The `Module` object in the generated JS is the interface between the two worlds. Flags cited in the book:

```bash
emcc hello.c -o hello.js                            # roda main() ao carregar
emcc hello.c -o hello.js -s INVOKE_RUN=0            # não executa main() automaticamente
emcc hello.c -o hello.js -s INVOKE_RUN=0 \
  -s EXTRA_EXPORTED_RUNTIME_METHODS="['callMain']"  # expõe Module.callMain()
emcc with-glue.c -O3 -s WASM=1 -s USE_SDL=2 -s MODULARIZE=1 -o custom-loading.js
```

- `-s INVOKE_RUN=0` + `Module.callMain()` lets you call `main` in response to events (e.g., a button click); `-s MODULARIZE=1` turns loading into a Promise-like API (useful for custom loading, cf. Rourke ch. 5).
- **Virtual file system (MEMFS)**: C/C++ code that writes to disk runs unmodified — Emscripten emulates an in-memory FS on top of the browser sandbox. This lets you port third-party libraries (e.g., bitmap, libsodium) nearly "drop-in".
- **embind**: `-s MODULARIZE=1` with `emcc --bind -o example.js example.cpp` to expose C++ classes/functions to JS with type conversion.
- For pure modules (without heavy glue), use `-s SIDE_MODULE=1` when compiling libraries that will be linked dynamically.

## 5. Web APIs and Bindings (ch. 8–10)

- **Node.js/Deno**: wasm works natively (no DOM); good for secure native extensions of Node (an alternative to C++ addons), mitigating **supply-chain attacks** by sandboxing third-party modules.
- **Rust+wasm-bindgen** (details in [wasm-with-rust.md](wasm-with-rust.md)): the book also uses wasm-bindgen for **threads** and generates *TypeScript Declaration files* (`*.d.ts`) ready for npm consumption.
- **TensorFlow.js**: the WebAssembly backend accelerates inference when WebGL is insufficient; SIMD/threads (`/s` 128-bit SIMD, `v128`) push browser ML performance even higher.
- **Testing/proposals**: Multi-Value Return (functions return multiple values — it solves the `(ptr,len)` string pattern), Reference Types (`externref`/`funcref` in tables), Module Linking, Feature Testing (`WebAssembly.validate` per proposed feature), Threads, GC, Exceptions.

## 6. Threading and Memory (cross-cutting concepts)

- **Memory API**: `grow(delta)` expands in 64 KB pages; TypedArray views become **detached** after growth — recreate the views after every `grow()`.
- **Threading**: the threads proposal adds *shared* memories (`SharedArrayBuffer`) + atomic instructions. In the browser: each thread runs a `Web Worker` with the **same** shared memory (transferred via `postMessage`); blocking/synchronization with `Atomics.wait`/`notify` (in the worker; not on the main thread). It requires COOP/COEP headers to enable `SharedArrayBuffer`. Emscripten exposes it via `-pthread`/`PTHREAD_POOL_SIZE` (ch. 12 "threads, garbage collection, and exceptions" as evolving proposals).
- **Stack/Heap**: inside linear memory there is a fixed *data/stack* region (addresses in `__data_end`/`__heap_base` in the exports — visible in `wasm-objdump -x` of Rust modules); dynamic allocations go to the heap (dlmalloc/emmalloc in Emscripten; the AssemblyScript runtime does its own GC since v0.18). `memory.grow()` is the only expansion mechanism.
- **Feature testing**: check proposal by proposal at runtime before depending on threads/SIMD/multi-value.

## 7. Where Not to Use wasm

- Replacing JavaScript in the application/DOM layer;
- Small apps where the cost of the glue and the binary outweighs the gain;
- UI logic — wasm does not access the DOM; every interaction crosses the JS boundary.

**Where it shines** (Sletten, ch. 1/9/15/16): games, codecs, cryptography (libsodium), ML (TensorFlow), legacy C/C++ in the browser, server extension (Istio/proxies), edge/serverless (Fastly, Cloudflare), IoT (Raspberry Pi, cf. Hoffman ch. 7), plug-in platforms, decentralized applications (ewasm/Polkadot/IPFS).

---

### Links

- Fundamentals/JS API/Memory/Tables → [wasm-mdn-guide.md](wasm-mdn-guide.md)
- Rust/wasm-bindgen/wasm-pack → [wasm-with-rust.md](wasm-with-rust.md)
- Emscripten with C/C++ and SDL projects → *Learn WebAssembly* (Mike Rourke, Packt): EMSDK setup, `emcc` flags `WASM=1`, `USE_SDL=2`, `MODULARIZE=1`, `ALLOW_MEMORY_GROWTH=1`, `SIDE_MODULE=1` (dynamic linking), and a build with a custom Makefile.
