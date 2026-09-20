# Programming WebAssembly with Rust (Kevin Hoffman) — Consolidated Notes

> Source: *Programming WebAssembly with Rust* (Kevin Hoffman, The Pragmatic Bookshelf, 2019).
> Covers wasm-bindgen, JavaScript integration, hosts outside the browser, and host/guest patterns. Complements [wasm-mdn-guide.md](wasm-mdn-guide.md) and [wasm-definitive-guide.md](wasm-definitive-guide.md).

---

## 1. wasm-bindgen — Rust ↔ JavaScript Bindings (ch. 4)

- `wasm-bindgen` is a set of **crates + a CLI**. In essence: `#[wasm_bindgen]` (a procedural macro) **injects metadata** into the compiled module; the CLI (`cargo install wasm-bindgen-cli`) reads that metadata, removes it, and generates the "**JavaScript wrapper bridge**" with the functions/classes you want to expose.
- Minimal project (`Cargo.toml` + `src/lib.rs`):

```toml
[package]
name = "bindgenhello"
version = "0.1.0"

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
```

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

```bash
cargo build --target wasm32-unknown-unknown
wasm-bindgen target/wasm32-unknown-unknown/debug/bindgenhello.wasm --out-dir .
```

- Import functions from specific **JavaScript namespaces** and classes from JS libraries (e.g., ROT.js):

```rust
#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);

    #[wasm_bindgen(module = "./index")]
    fn stats_updated(stats: JsValue);

    pub type Display;
    #[wasm_bindgen(method, structural, js_namespace = ROT)]
    fn draw(this: &Display, x: i32, y: i32, ch: &str);
    #[wasm_bindgen(method, structural, js_name = draw, js_namespace = ROT)]
    fn draw_color(this: &Display, x: i32, y: i32, ch: &str, color: &str);
}
```

  - `js_namespace` imports from a specific JS module; `method` + `structural` bind JS class methods to Rust functions with an explicit `this`; `js_name = draw` maps overloads; `pub type Display` inside the `extern` block makes the JS class usable as a Rust struct.
  - On the JS side, Rust structs decorated with `#[wasm_bindgen]` appear as **JS classes** exportable in the generated file: `import { Engine, PlayerCore } from './roguewasm';` — and `new Engine(this.display)` passes a JS class instance into Rust as if it were native.

## 2. `JsValue`, `Option`/`Result`, and Data Passing

- **`JsValue`** is the "any JS value" type. For callbacks that pass dynamic objects, instead of mirroring structs on both sides, send raw JSON through `JsValue` — faster and without generated-class boilerplate.
- With the **`serde-serialize`** feature and `serde`/`serde_derive`, serialize Rust structs to `JsValue`:

```toml
[dependencies]
serde = "^1.0"
serde_derive = "^1.0"

[dependencies.wasm-bindgen]
version = "^0.2"
features = ["serde-serialize"]
```

```rust
#[derive(Serialize)]
pub struct Stats {
    pub hitpoints: i32,
    pub max_hitpoints: i32,
    pub moves: i32,
}

// no callback do jogo:
stats_updated(JsValue::from_serde(&stats).unwrap());
```

- Memory: wasm-bindgen generates `__wbindgen_free()` and equivalent utilities to free linear memory allocated by values crossing the boundary — the JS glue calls this automatically when discarding objects.
- Modules that need to run **inside and outside the browser** (ch. 10, "Designing Code for In and Out of the Browser"): isolate browser-only code behind `#[cfg(target_arch = "wasm32")]` and keep the core logic (engine, rules) host-agnostic — the pattern used in the book's Rogue game.

## 3. The Yew Framework (ch. 5)

- **Yew** is the Rust UI framework (componentized style, with a Virtual DOM) that also compiles to wasm via wasm-bindgen; the book builds a **multi-user live chat** with WebSocket.
- The integration pattern imports JS hooks/services, uses `JsValue`/`serde` for payloads, and handles browser events through callbacks registered by the framework — without writing manual JavaScript glue.
- Browser global API references (`js_sys`, `web_sys`) and utilities (`document()`, `window()`) come from the wasm-bindgen ecosystem (`wasm-bindgen` + `js_sys` + `web_sys`).

## 4. wasm-pack and Distribution

- `wasm-pack` packages Rust+wasm-bindgen modules into **npm** packages and is the recommended route for distributing and consuming modules in web bundlers. The book cites it in the context of **serverless** (deploying modules to Cloudflare Workers via `wasm-pack`).
- Standard workflow (modern, complementing the book): `wasm-pack build --target web|bundler|nodejs|no-modules` — choose the target according to the consumer (direct browser, webpack/npm, Node.js, or your own glue generating TypeScript `*.d.ts`).
- Note that the book (2019, Rust 2018) uses the `wasm-bindgen` CLI + npm/webpack manually; today prefer `wasm-pack` for the same result, keeping the same `#[wasm_bindgen]` attributes.

## 5. Hosts Outside the Browser (ch. 6–7)

- **The contract of a good host** (load/validate, expose exports, satisfy imports, execute, isolate modules) — detailed in [wasm-definitive-guide.md](wasm-definitive-guide.md) §3.
- The book creates hosts in Rust with the **wasmi** crate (an interpreter extracted from Parity's Ethereum client):

```toml
[dependencies]
wasmi = "0.4"
```

```rust
use wasmi::{ImportsBuilder, ModuleInstance, NopExternals, RuntimeValue};

let module = wasmi::Module::from_buffer(buffer)?;
// injeta host functions via ImportsBuilder; invoca exports e lê RuntimeValue
```

- **Host functions**: the host registers Rust functions that the module calls via imports — this is how modules do I/O (satisfying the host contract). A "mock" host that satisfies the same imports makes modules testable outside the real environment.
- **IoT**: chapter 7 runs the same interpreter on a **Raspberry Pi** (ARM) controlling LEDs via GPIO with wasm modules as "indicator modules" — proof of the concept "wasm as a portable plugin on any host".

## 6. Security (Appendix A2)

- Vectors in the browser: wasm modules are data — validate their provenance (signing/authentication), avoid instantiating `.wasm` from untrusted sources without validation, and remember that the module can abuse the **imports** the JS glue grants it (minimal import surface).
- The book recommends **signing and encrypting modules** in the distribution pipeline (Signing/Encrypting WebAssembly Modules) and highlights that the module cannot self-instantiate its execution — the host is the control point.

---

### Links

- WABT/WASI/Emscripten/threads toolchain → [wasm-definitive-guide.md](wasm-definitive-guide.md)
- Base concepts/JS API → [wasm-mdn-guide.md](wasm-mdn-guide.md)
- For C++ *game projects* (Emscripten setup, memory, modularization, build) consult *Learn WebAssembly* (Mike Rourke).
