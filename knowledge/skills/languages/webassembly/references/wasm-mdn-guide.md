# WebAssembly — MDN Reference Guide

Consolidated from the official MDN Web Docs documentation (developer.mozilla.org/pt-BR/docs/WebAssembly): Concepts, JavaScript API (Module, Instance, Memory, Table, Global), compilation (C/C++, Rust, AssemblyScript), the text format (.wat), and JSPI.

---

## 1. Fundamental Concepts

**What it is**: a low-level, assembly-like language with a compact binary format (`.wasm`), executed with near-native performance in modern browsers. **It does not replace JavaScript** — it complements it by running side by side in the same VM.

**Goals (W3C WebAssembly CG)**:
1. Fast, efficient, and portable (native performance on any platform).
2. Readable and debuggable (text format `.wat` with a 1:1 correspondence to the binary).
3. Safe — a sandbox with the browser's same-origin policy and permissions.
4. Do not break the web (backward compatibility).

**Key concepts (reflected 1:1 in the JS API)**:

| Concept | Definition |
| :--- | :--- |
| **Module** | A binary compiled by the browser into executable code. Stateless; shareable between windows/workers via `postMessage()` as a `Blob`; declares imports/exports like an ES2015 module. |
| **Memory** | A **resizable** `ArrayBuffer` (or `SharedArrayBuffer`) holding a linear array of bytes read/written by wasm memory instructions. |
| **Table** | A **typed and resizable** array of references (e.g., `funcref`) — it cannot live in linear memory for security/portability reasons. The foundation for C/C++ function pointers. |
| **Instance** | A Module paired with all the execution state (Memory, Table, imports). Equivalent to an ES2015 module loaded with a specific set of imports. |

**Multiplicity** (important for dynamic linking):
- A Module can have **N** Instances.
- An Instance uses 0–1 Memory and 0–1 Table (future: 0–N).
- A Memory/Table can be shared by 0–N Instances (common address space → dynamic linking).

## 2. Compilation — Entry Points

1. **Emscripten (C/C++)**: feeds the code into clang+LLVM → transforms it into `.wasm` + generates JS/HTML "glue code" (implements SDL, OpenGL, OpenAL, POSIX over Web APIs). The wasm **does not access the DOM directly** — it only calls JS, which makes the Web API calls.
2. **Rust → Wasm**: via the Rust Wasm Working Group (`wasm-pack`, which generates an npm package).
3. **AssemblyScript**: TypeScript-like syntax → `.wasm`; a small bundle, with performance slightly below C/Rust; ideal for web devs.
4. **Direct Wasm (text format)**: write `.wat` and convert it with tools (WABT `wat2wasm`); playgrounds: WasmFiddle, WasmExplorer.

## 3. Text Format (.wat)

- Module, functions, imports with a **two-level namespace**:
  ```wat
  (module
    (func $i (import "imports" "imported_func") (param i32))
    (func (export "exported_func")
      i32.const 42
      call $i))
  ```
- S-expression; in debug mode, browsers expose `wasm://` in the Debugger panel (breakpoints, call stack, stepping over the text).
- 1:1 conversion `.wat` ↔ `.wasm` (WABT: `wat2wasm`, `wasm2wat`).

## 4. JavaScript WebAssembly API

### Static methods

| Method | Use |
| :--- | :--- |
| `WebAssembly.instantiateStreaming(fetch(url), importObject)` | **Preferred**: compiles+instantiates directly from the response stream (`Response`), without going through an `ArrayBuffer`. |
| `WebAssembly.compileStreaming(source)` | Compiles only → `Promise<Module>`. |
| `WebAssembly.instantiate(bytes \| Module, importObject)` | Requires the extra `response.arrayBuffer()` step. |
| `WebAssembly.compile(bytes)` | Compiles from an `ArrayBuffer`. |
| `WebAssembly.validate(bytes)` | Checks whether the bytes are valid wasm (`boolean`). |
| `WebAssembly.promising(fn)` | **JSPI**: turns a wasm-exported JS function into an AsyncFunction (promise). |

### Canonical example (streaming)

```javascript
const importObject = {
  imports: { imported_func: (arg) => console.log(arg) }, // namespace de 2 níveis
};

WebAssembly.instantiateStreaming(fetch("simple.wasm"), importObject).then(
  (obj) => obj.instance.exports.exported_func(),
);

// Sem streaming (fallback):
fetch("simple.wasm")
  .then((r) => r.arrayBuffer())
  .then((bytes) => WebAssembly.instantiate(bytes, importObject))
  .then(({ instance }) => instance.exports.exported_func());
```

### WebAssembly.Module
- `new WebAssembly.Module(bytes)` (synchronous); `Module.customSections()`, `Module.exports()`, `Module.imports()` (static introspection).
- Cacheable in **IndexedDB** and shareable with workers (a major startup gain).

### WebAssembly.Instance
- `instance.exports` → functions exported as normal JS functions (synchronous call).

### WebAssembly.Memory

```javascript
const memory = new WebAssembly.Memory({ initial: 10, maximum: 100 }); // páginas de 64KB
new Uint32Array(memory.buffer)[0] = 42;      // escrita
memory.grow(1);                              // +1 página (64KB)
```

- The units of `initial`/`maximum`/`grow()` = **64 KB pages**.
- Exceeding `maximum` → `RangeError`. Declaring a maximum allows efficient pre-reservation.
- ⚠️ **Detached buffer**: after `grow()`, `memory.buffer` returns a **new** `ArrayBuffer`; old views become invalid ("detached"). Always recreate the `TypedArray` after a grow.
- Memory can be imported (allowing initial content to be filled via JS and shared between instances) or exported:
  ```javascript
  WebAssembly.instantiateStreaming(fetch("memory.wasm"), { js: { mem: memory } })
    .then(({ instance }) => {
      const i32 = new Uint32Array(memory.buffer);
      for (let i = 0; i < 10; i++) i32[i] = i;
      console.log(instance.exports.accumulate(0, 10));
    });
  ```
- **Shared memories** (`shared: true`): a `SharedArrayBuffer` transferable between Window/Worker via `postMessage()` (use with Atomics).

### WebAssembly.Table

- A resizable array of references (element type: today limited to `funcref`/`externref`); required for C/C++ function pointers (indices stay in linear memory; the reference stays in the table with bounds checking).
- Methods: `set(index, ref)`, `get(index)`, `grow(n)`, `length`.
  ```javascript
  WebAssembly.instantiateStreaming(fetch("table.wasm")).then(({ instance }) => {
    const tbl = instance.exports.tbl;
    console.log(tbl.get(0)()); // 13  — dois parênteses: get() retorna a função
  });
  ```

### WebAssembly.Global

```javascript
const global = new WebAssembly.Global({ value: "i32", mutable: true }, 0);
global.value = 42;                       // set via JS
WebAssembly.instantiateStreaming(fetch("global.wasm"), { js: { global } })
  .then(({ instance }) => {
    instance.exports.getGlobal();        // 42
    instance.exports.incGlobal();        // wasm muta o global
    global.value;                        // 43
  });
```
- `value`: `i32`, `i64`, `f32`, `f64` (and references). `mutable: boolean`.
- A building block for **dynamic linking** between multiple modules.

### Exceptions and JSPI

- `WebAssembly.Tag`, `WebAssembly.Exception` (`is()`, `getArg()`, `stack`): wasm↔JS exception interop; `try_table`/`catch`/`throw` instructions in wasm.
- `WebAssembly.Suspending()` + `WebAssembly.promising()`: **JSPI (JavaScript Promise Integration)** — suspend wasm during Promises and resume afterward, without blocking the main thread.
- Errors: `CompileError`, `LinkError` (incompatible imports/exports), `RuntimeError` (e.g., `unreachable`), `SuspendError`.

## 5. Value Types

| Type | Description |
| :--- | :--- |
| `i32`, `i64` | 32/64-bit integers (i64 crosses the JS boundary as `BigInt`). |
| `f32`, `f64` | 32/64-bit floating point. |
| `v128` | 128-bit SIMD vector (SIMD instructions: splat, shuffle, extract_lane, load/store lane, trunc_sat, i8x16/i16x8/i32x4/f32x4/f64x2). |
| `funcref` | Function reference (tables). |
| `externref` | Opaque reference to JS/(host) values. |
| `exnref` | Exception reference (proposed EH). |

## 6. Module Structures (sections/definitions)

- `func` (types), `data` (bytes in memory), `elem` (table elements), `global`, `memory`, `table`, `tag`.
- Main instructions: control flow (`block`, `loop`, `if...else`, `br`, `br_if`, `br_table`, `call`, `return`, `unreachable`, `select`, `drop`, `nop`), variables (`local.get/set/tee`, `global.get/set`), memory (`load/store`, `grow`, `copy`, `fill`, `init`, `size`), numeric (add/sub/mul/div/rem, bit operators, clz/ctz/popcnt, converts/reinterprets), SIMD.

## 7. Security and Best Practices

- **Sandbox**: the browser's same-origin/permission policy; no direct access to the DOM/file/network — always through JS glue.
- **Validate imports/exports**: mismatches produce `LinkError`; use `WebAssembly.validate()` and `Module.imports()/exports()` for introspection before instantiating.
- **Prefer streaming**: `instantiateStreaming` reduces parse latency (bypasses the `ArrayBuffer`).
- **Cache large modules** in IndexedDB (storing compilable bytes) to speed up startup.
- **CORS/MIME**: serve `.wasm` with `Content-Type: application/wasm` (required for streaming compile).
- **Memory safety**: always recreate TypedArrays after `grow()`; use `Atomics` on memories shared between threads.
- **Synchronous JS↔wasm interactions**: avoid overly hot glue (frequent calls incur a boundary cost); move whole loops inside the wasm.
- **Debugging**: the Debugger panel (Firefox 54+) shows `wasm://` with a text representation, breakpoints, and a call stack.
