---
name: "webassembly"
description: "Specialist in WebAssembly (Wasm) based on the official MDN Web Docs documentation (developer.mozilla.org/pt-BR/docs/WebAssembly), complemented by WebAssembly: The Definitive Guide (Brian Sletten), Programming WebAssembly with Rust (Kevin Hoffman), and Learn WebAssembly (Mike Rourke). Covers concepts (Module, Instance, Memory, Table, multiplicity), the JavaScript WebAssembly API (instantiateStreaming, compileStreaming, Global, Tag/Exception, JSPI with Suspending/promising), compilation from C/C++ (Emscripten), Rust (wasm-pack), and AssemblyScript, the .wat/WABT text format, SIMD, types (i32/i64/f32/v128/funcref/externref), IndexedDB caching, execution in Workers, shared memory (SharedArrayBuffer/Atomics), dynamic linking, and security/sandboxing."
---

# AI Skill: WebAssembly (Wasm Specialist)

This skill guides the AI to act as a specialist in **WebAssembly**, aligned with the official **MDN Web Docs** documentation (https://developer.mozilla.org/pt-BR/docs/WebAssembly). It covers everything from architecture concepts (Module, Memory, Table, Instance) to advanced use of the JavaScript API, cross-language compilation (C/C++, Rust, AssemblyScript), the `.wat` text format, SIMD, exceptions, and JSPI.

> 📖 **Canonical reference**: see [references/wasm-mdn-guide.md](references/wasm-mdn-guide.md) for the consolidated guide (concepts, JavaScript API, Memory, Tables, Globals, value types, security).
>
> 📚 **Complementary references**:
> - [references/wasm-definitive-guide.md](references/wasm-definitive-guide.md) — *WebAssembly: The Definitive Guide* (Brian Sletten): WABT toolchain, WASI, Emscripten, non-browser runtimes, host↔guest patterns.
> - [references/wasm-with-rust.md](references/wasm-with-rust.md) — *Programming WebAssembly with Rust* (Kevin Hoffman): wasm-bindgen, wasm-pack, Yew, Rust hosts.

---

## 🧭 Fundamental Guidelines

While working under this skill, apply the following patterns:

### 1. Correct Mental Model
- **Wasm complements JavaScript, it does not replace it**: they run side by side in the same VM; use wasm for computational hot paths (3D games, AR/VR, computer vision, image/video editing, codecs, cryptography) and JS/DOM for the application layer.
- **1:1 concepts with the JS API**: `Module` (compiled binary, stateless, shareable via `postMessage()` as a `Blob`), `Instance` (Module + state), `Memory` (resizable `ArrayBuffer` — Linear Memory in **64 KB** pages), `Table` (resizable array of references — `funcref`, the basis for function pointers).
- **Multiplicity**: 1 Module → N Instances; 0–1 Memory/Table per Instance; 1 Memory/Table shared by N Instances (the foundation of dynamic linking).

### 2. Loading and Instantiation
- **Always prefer streaming**: `WebAssembly.instantiateStreaming(fetch(url), importObject)` — compiles and instantiates straight from the stream, with no intermediate `ArrayBuffer`.
- Serve `.wasm` with the MIME type `application/wasm` and CORS enabled (a requirement for compile streaming).
- Validate first when the byte origin is untrusted: `WebAssembly.validate(bytes)`;
- Introspection: `Module.imports()`, `Module.exports()`, `Module.customSections()`.
- Cache large byte modules in **IndexedDB** to speed up startup.

### 3. JS ↔ Wasm Boundary
- Imports use a **two-level namespace**: `{ imports: { imported_func: fn } }` ↔ `(import "imports" "imported_func")`.
- Only primitive numeric types cross the boundary by default; structured data passes through **Linear Memory** via `Uint8Array`/`Int32Array` etc. over `memory.buffer`.
- `i64` crosses the boundary as `BigInt`. Host-side references use `externref`; functions use `funcref` in a `WebAssembly.Table`.
- Frequent JS↔wasm calls carry a boundary cost: **move the whole loop into wasm**, do not iterate element by element through exports.

### 4. Memory
- Always declare `initial` and preferably `maximum` in `WebAssembly.Memory` (efficient pre-reservation; exceeding it throws `RangeError`).
- ⚠️ **Buffer detachment**: after `memory.grow()`, `memory.buffer` is **new** — recreate all TypedArrays; old views become invalid.
- Shared memories (`shared: true`) → a `SharedArrayBuffer` transferable between Window/Worker with `postMessage()`; synchronize with `Atomics`.
- Prefer defining `maximum` up front rather than growing indefinitely (fragmentation/reallocation).

### 5. Compilation by Toolchain
- **Emscripten (C/C++)**: produces `.wasm` + JS glue + HTML; implements SDL/OpenGL/POSIX over Web APIs; wasm does not access the DOM — it only calls JS. Use it to port legacy C/C++ code and apps with AL.
- **Rust**: `wasm-pack` + the `wasm-bindgen` crate; generates a typed npm package; prefer it for new modules with an ergonomic ABI.
- **AssemblyScript**: TypeScript-like syntax; small bundle; performance slightly below C/Rust; ideal for web devs without a C background.
- **Direct WAT**: for custom tools/compilers; convert with WABT (`wat2wasm`, `wasm2wat`).

### 6. Errors and Exceptions
- Handle specifically: `CompileError` (invalid bytes), `LinkError` (incompatible imports/exports), `RuntimeError` (`unreachable`, out-of-bounds memory access), `SuspendError` (JSPI).
- Structured exceptions: `WebAssembly.Tag` + `WebAssembly.Exception` (`is()`, `getArg()`, `stack`); in wasm use `try_table`/`catch`/`throw`/`throw_ref`.
- **JSPI** (when available): `new WebAssembly.Suspending(promiseFn)` for suspending imports and `WebAssembly.promising(export)` to turn a wasm export into a function returning a Promise — wasm pauses during async operations without blocking.

---

## 🛠️ Recommended Code Patterns

### Idiomatic streaming loading
```javascript
const importObject = {
  imports: { imported_func: (arg) => console.log(arg) },
};

WebAssembly.instantiateStreaming(fetch("simple.wasm"), importObject)
  .then(({ instance }) => instance.exports.exported_func())
  .catch((err) => {
    if (err instanceof WebAssembly.CompileError) {
      console.error("Bytes wasm inválidos ou MIME incorreto:", err);
    }
  });
```

### Exchanging data via Linear Memory
```javascript
const memory = new WebAssembly.Memory({ initial: 10, maximum: 100 });

WebAssembly.instantiateStreaming(fetch("memory.wasm"), { js: { mem: memory } })
  .then(({ instance }) => {
    let i32 = new Uint32Array(memory.buffer);
    for (let i = 0; i < 10; i++) i32[i] = i;
    const sum = instance.exports.accumulate(0, 10);
    // ⚠️ se o módulo chamar memory.grow internamente, recrie a view:
    i32 = new Uint32Array(memory.buffer);
  });
```

### Shared Global for dynamic linking
```javascript
const sharedCounter = new WebAssembly.Global({ value: "i32", mutable: true }, 0);

WebAssembly.instantiateStreaming(fetch("global.wasm"), { js: { global: sharedCounter } })
  .then(({ instance }) => {
    sharedCounter.value = 42;          // JS escreve
    instance.exports.incGlobal();      // wasm incrementa
    console.log(sharedCounter.value);  // 43
  });
```

### Table as an array of functions (function pointers)
```javascript
WebAssembly.instantiateStreaming(fetch("table.wasm")).then(({ instance }) => {
  const tbl = instance.exports.tbl;
  console.log(tbl.get(0)()); // 13 — get() devolve a referência; segundo () invoca
});
```

---

## 🔒 Security and Safe Practices

- **Sandbox and Same-Origin Policy**: wasm runs under the same browser policies; no direct access to the DOM, network, or filesystem — all I/O interaction goes through JS glue.
- **Binary validation**: never instantiate `.wasm` from untrusted sources without `WebAssembly.validate()`; binaries are data, and a malicious wasm can abuse JS imports (e.g., importing `eval`-like behavior via glue).
- **Minimal import surface**: expose only the JS functions strictly necessary for the module; prefer wrappers that whitelist operations.
- **Memory limits**: always set `maximum` to prevent client memory exhaustion; handle `RangeError` in `grow()`.
- **Shared memory**: require `SharedArrayBuffer` with correct COOP/COEP in multi-threaded mode (Atomics for synchronization — data races produce undefined behavior).
- **DoS via wasm**: modules with infinite loops block the main thread — run them in a Web Worker when processing is long.
- **Supply chain**: confirm the provenance of third-party `.wasm` (SBOM/signature); recompile from audited source when possible.

## 🧰 Toolchain Beyond MDN

Beyond the MDN guide, the production wasm ecosystem (cf. *WebAssembly: The Definitive Guide* — Brian Sletten) revolves around:

- **WABT (WebAssembly Binary Toolkit)**: `wat2wasm` (text→binary), `wasm2wat` (binary→text), `wasm-objdump -x` (section/symbol inspection), `wasm-interp` (execution REPL), `wasm-validate`, and `wasm2c`. Use `--debug-names` in `wat2wasm` to preserve function/local names (Custom section) during debugging.
- **WASI**: a portable I/O contract (`wasi_snapshot_preview1` — `fd_write`, `proc_exit`, `environ_get`...). Modules export `memory` + `_start`. Security via **capabilities** (unforgeable handles): grant access with flags such as `wasmtime --dir=.` (preopened file descriptors). Toolchains: `wasi-sdk` (clang/C), Rust `wasm32-wasi`, `cargo wasi run`.
- **Non-browser runtimes**: Wasmtime, Wasmer, wasm3, WasmEdge — embeddable as a plug-in/serverless engine. In Wasmtime (Rust): `Engine` → `Store` (isolation unit) → `Module` → `Instance` + typed `get_typed_func`. Valid hosts (Hoffman) must: load/validate, expose exports, satisfy imports, execute, and **isolate** modules from one another.
- **Emscripten**: beyond MDN, key flags: `-s INVOKE_RUN=0` + `Module.callMain()` (deferred `main` execution), `-s MODULARIZE=1` (Promise-like API), `-s USE_SDL=2` (port), virtual MEMFS filesystem (C code that writes to disk runs in the sandbox), `emcc --bind` (embind for C++↔JS classes), `-s SIDE_MODULE=1` (dynamic linking).
- **Threading**: `shared` memories + `Atomics.wait/notify` inside Web Workers (requires COOP/COEP); confirm support via feature testing before depending on the proposal.

Full details: [references/wasm-definitive-guide.md](references/wasm-definitive-guide.md)

## 🦀 Wasm + Rust in the Browser

Idiomatic `wasm-bindgen` pattern (cf. *Programming WebAssembly with Rust* — Kevin Hoffman, ch. 4): the `#[wasm_bindgen]` macro injects metadata into the `.wasm`; the CLI reads that metadata and generates the JavaScript "wrapper bridge" — including JS classes from Rust structs.

```rust
use wasm_bindgen::prelude::*;

// Import 'window.alert'
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

// Export a 'hello' function
#[wasm_bindgen]
pub fn hello(name: &str) {
    alert(&format!("Hello, {}!", name));
}
```

Manual build (book): `cargo build --target wasm32-unknown-unknown` + `wasm-bindgen target/wasm32-unknown-unknown/debug/bindgenhello.wasm --out-dir .`. In production prefer `wasm-pack build --target web|bundler|nodejs|no-modules` (generates an npm package with `.d.ts`).

Extra tips from the book:
- Nominal imports: `#[wasm_bindgen(js_namespace = console)] fn log(s: &str);` and external JS classes via `pub type Display; #[wasm_bindgen(method, structural, js_namespace = ROT)]`.
- Serialization: with the `serde-serialize` feature + `serde`, send Rust structs as `JsValue` (`JsValue::from_serde(&stats).unwrap()`) — lighter than mirroring classes on both sides.
- UI in pure Rust: the **Yew** framework (components + Virtual DOM), without writing JS glue by hand.

Full details: [references/wasm-with-rust.md](references/wasm-with-rust.md)

## 🔗 Integration with Other Skills
- [lang-c](../lang-c/SKILL.md) / [lang-cpp](../lang-cpp/SKILL.md): C/C++ source code compiled via Emscripten to the wasm target.
- [lang-rust](../lang-rust/SKILL.md): Rust modules with `wasm-pack`, `wasm-bindgen`, and the `wasm32-unknown-unknown` target.
- [lang-typescript](../lang-typescript/SKILL.md): typed glue code (`WebAssembly.Module`, `Memory`, `Instance`, `exports`) and libraries such as AssemblyScript.
- [frontend-developer](../../roles/frontend-developer/SKILL.md): integrating wasm modules into web applications (fetch, workers, perf budget, Core Web Vitals).
- [program-containers](../../infrastructure/program-containers/SKILL.md): Wasm outside the browser (Wasmtime/Wasmer runtimes, WASI) for server-side and edge workloads.
