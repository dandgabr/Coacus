---
name: javascript-high-performance
description: "Specialist in JavaScript Performance based on Hands-On JavaScript High Performance (Justin Scherer). Covers profiling and observability with DevTools tools (Chrome Performance/Memory/Rendering tabs, jsPerf, and correct benchmarking), immutability versus mutability trade-offs (Redux, Immutable.js, RAII, lazy evaluation, tail-call, and currying), modern vanilla JavaScript (Collections, Proxies, Typed Arrays, DOM APIs, Fetch/Promises), Svelte as a framework compiled to vanilla, Node.js without a DOM (fs, net, http, streams, and non-blocking I/O), message passing (pipes, sockets, TCP/UDP, HTTP/2, QUIC), data formats alternative to JSON (MessagePack, schema-based Protocol Buffers), Web Workers (dedicated/shared, transferrables, SharedArrayBuffer), Service Workers (offline cache), build and deploy with Rollup/CircleCI, and WebAssembly in the browser."
---

# AI Skill: JavaScript High Performance

This skill guides the AI to act as a specialist in **JavaScript performance**, covering everything from profiling with browser tools to code architecture (mutability, streams, workers, data formats, and WASM), based on *Hands-On JavaScript High Performance* (Justin Scherer, Packt).

> 📖 **Canonical reference**: see [references/js-high-performance-book-guide.md](references/js-high-performance-book-guide.md) for the chapter-by-chapter summary of the book and [examples/performance-patterns.md](examples/performance-patterns.md) for the practical patterns.

---

## 🧭 General Guideline

- **Measure before optimizing**: use the Performance tab of Chrome DevTools to locate the real bottleneck (scripting, rendering, painting) — never optimize based on assumptions.
- **Everything is a trade-off**: immutability buys safety at the cost of speed/memory; native collections beat libraries; MessagePack may be neither smaller nor faster than native JSON. Make a conscious choice, not dogma.
- **Prefer the runtime's primitives**: the engine (V8 etc.) optimizes built-ins better than libraries; avoid abstraction layers on hot paths.
- **Keep the main thread free**: any processing > ~16 ms should be offloaded to Workers, streams, or WASM.

---

## 🔍 1. Profiling and Observability

### Chrome DevTools Tabs
- **Performance**: runtime timeline recording (Scripting/Rendering/Painting, call stack flame chart, event log). Use it to find long-running functions, forced reflows, and GC pauses.
- **Memory**: heap snapshots (comparison between snapshots to detect memory leaks — objects retained between captures), allocation instrumentation, and allocation timeline.
- **Rendering**: FPS meter and paint flashing to detect excessive layouts/paints in real time.
- Other engines: Safari (Web Inspector with Timeline), Firefox (Performance tools), and Edge (a Chromium fork) — different engines optimize differently, so validate across multiple browsers.

### Correct Benchmarking (jsPerf and the like)
- Beware of **engine optimizations** that distort results (dead code elimination) — consume the results of the test functions.
- Compare across **multiple browsers/engines**; no single-engine result is definitive.
- Remove stray code from the test cases — any extra work skews the measurements.

---

## ⚖️ 2. Immutability versus Mutability

- **Immutability** (Redux, Immutable.js) brings predictability, undo/redo, and cheap change detection (same reference = same data), but in high-performance applications you pay for it with increased time and memory: every change copies structures.
- **Immutable.js** (List, Map, Set with structural tries) yields cleaner code and a functional architecture, but for large datasets native operations (`for` loops, arrays, mutable objects) are faster and less memory hungry.
- **Hybrid strategy**: immutability in the state/UI layer (a reference change triggers re-render), disciplined mutability on computational hot paths (parsers, data transformations, in-memory joins).
- **Safe mutable writing**: encapsulate mutation in small modules (the RAII / scope-bound resource management pattern — release/close resources in the same scope that created them, inspired by C++/Rust); avoid mutating objects shared across modules.

### Functional Techniques with a Conscious Cost
- **Lazy evaluation**: generate collections on demand (generators/iterators) instead of materializing giant arrays.
- **Tail recursion**: prefer turning recursion into iteration (loops) — engines do not guarantee TCO, and stack overflow is a real risk.
- **Currying**: powerful for composition, but it creates closures and intermediate functions — avoid it in extremely high-frequency code.

---

## 🌐 2. Modern Vanilla JavaScript

- **Block-scoped let/const**, arrow functions, and modules — modern code is also code the engine optimizes predictably.
- **Collections**: `Map`/`Set`/`WeakMap`/`WeakSet` — `WeakMap`/`WeakSet` allow key GC (metadata without leaks); `Map` beats objects as a dictionary for dynamic keys.
- **Typed Arrays** (`Int32Array`, `Float64Array`, `ArrayBuffer`): contiguous, typed memory, essential for large numeric data, binary data, and transfer with Workers.
- **Proxies and getters/setters**: enable reactivity (the basis of frameworks such as Svelte/Vue), but every access intercepts — do not use them in hot loops.
- **Efficient DOM**: centralized `querySelector`/`querySelectorAll`; **Document Fragments** for batch insertions (a single reflow); Shadow DOM and Web Components for encapsulation; `<template>` for cheap markup cloning.
- **Fetch + Promises**: Promises are lazy-friendly; `AbortController` support to cancel requests (avoids unnecessary network and parsing work).

---

## 🧩 3. Svelte and the "Compiled to Vanilla" Paradigm

- Svelte compiles components into imperative vanilla JS — no virtual DOM, no runtime in production; each state mutation generates minimal, precise DOM update code.
- The performance lesson: **less runtime = more speed**. When a framework library is the bottleneck, consider alternatives that push work to build time (compilers, aggressive tree shaking).
- Practical applications (Todo, weather app) show that small components with local state avoid cascading re-renders.

---

## 🟩 4. Node.js without a DOM

- `package.json` as the configuration hub (scripts, dependencies, type module).
- **Native modules**: `fs` (file I/O), `net` (TCP sockets), `http` (server/services) — no libraries for the basics; the standard lib is the fastest.
- **Streams and non-blocking I/O**: never read large files entirely into memory — a pipeline with Readable/Writable/Duplex/Transform streams processes in chunks, keeping memory constant and the event loop free.
- **Custom streams**: implement `Readable`/`Writable`/`Transform` (with `highWaterMark` for backpressure) and use generators to simplify pipelines.

---

## 📬 5. Message Passing and Protocols (Node.js)

- Local/process communication: `net` with Unix domain sockets / TCP, IPC between processes (cluster).
- `cluster` module: multiply processes per CPU core to saturate the hardware (Node is single-threaded per process).
- **TCP/UDP**: TCP for ordering and reliability; UDP for minimal latency without a handshake.
- **HTTP/2**: stream multiplexing on one connection (eliminates HTTP/1.1 head-of-line blocking), header compression.
- **HTTP/3/QUIC**: UDP-based, 0-RTT handshake, no TCP head-of-line blocking — the future direction of web transport.

---

## 📦 6. Data Formats

- **JSON**: ubiquitous, but verbose and with encode/decode cost on large payloads.
- **Schema-less formats**: JSON, XML — self-describing, larger on the wire.
- **MessagePack** (e.g., the `what-the-pack` lib): compact binary with buffer pre-allocation; it may be neither smaller nor faster than native `JSON.parse`/`stringify` — always measure.
- **Protocol Buffers (proto3)**: a schema shared up front, very compact and fast encoding — the standard for enterprise systems; numeric field IDs make encoding and indexing cheap.
- **Custom format**: for extreme cases, a custom binary encoder/decoder (e.g., schema in front of the data) gives the maximum control over size and speed.

---

## 👷 7. Web Workers and Browser Parallelism

- **Dedicated Workers**: move heavy work (parsing, transformation, data joins, computation) off the main thread; communicate via `postMessage`.
- **Structured clone has a real cost**: sending thousands of objects serializes/deserializes everything — the book's example: 100,000 objects took from 800 ms to 1.7 s and 80–100 MB of heap. Use `Date.now()` + Profiler to visualize the cost.
- **Transferrables**: send the `ArrayBuffer` (`postMessage(view, [view.buffer])`) — **zero copy**; the sender loses access, the receiver gains it. For large binary data this is orders of magnitude faster.
- **Shared Workers**: one worker shared across multiple pages/tabs (e.g., a shared in-memory cache, a single connection).
- **SharedArrayBuffer + Atomics**: true shared memory with synchronization; requires correct COOP/COEP.

---

## 🔁 8. Service Workers and Caching

- ServiceWorker lifecycle: install → waiting → activate; intercept requests with the `fetch` event.
- **Page/template caching for offline** (Cache Storage API), enabling PWA behavior.
- **Save requests for later**: queue offline mutations and replay them when the network returns (a queue pattern in the SW).
- A well-done cache is the cheapest optimization: zero network and processing cost on subsequent requests (TTL/LRU to cap growth, as in the static server chapter).

---

## 🏗️ 9. Build, Deploy, and CI/CD

- **Rollup**: a bundler optimized for ES modules (ESM) — effective tree shaking, smaller bundles; use it to distribute the application (server + assets) in a single distributable.
- Integrate the build into npm scripts (`npm run build`) and the **CircleCI** pipeline (build → tests → security checks → deploy).
- Fewer bytes = less main-thread parsing/compiling; tree shaking is a first-order optimization.

---

## ⚙️ 10. WebAssembly in the Browser

- For hot paths that even optimized JS cannot satisfy (corrective code generators such as Hamming, heavy parsing, numeric math).
- Direct authoring of WAT modules, compiling **C/C++ for the browser**, and shared memory between WASM and JavaScript (Linear Memory over `WebAssembly.Memory`).
- A real case from the book: **SQLite compiled to WASM** running in the browser — a complete client-side database.
- Sandbox: WASM code does not leak memory across modules; load it via a static server with the MIME type `application/wasm`.

---

## 🧪 Recommended Code Patterns

### Native loop on a hot path (vs. abstraction)
```javascript
// ❌ chain of high-order functions on large data: multiple intermediate arrays
const positive = data.filter((x) => x > 0).map((x) => x * 2);

// ✅ a single loop, no intermediate allocations
const result = new Array(data.length);
let count = 0;
for (let i = 0; i < data.length; i++) {
  if (data[i] > 0) {
    result[count++] = data[i] * 2;
  }
}
```

### Binary Transfer to Workers (zero-copy)
```javascript
const view = new Int32Array(1_000_000);
// ... populate ...
worker.postMessage(view, [view.buffer]); // transfere, não copia
// ⚠️ view agora está neutered/detached no remetente
```

### Fragment for batch DOM insertion
```javascript
const frag = document.createDocumentFragment();
for (const item of items) {
  frag.appendChild(createRow(item));
}
container.appendChild(frag); // um único reflow/layout
```

### Simple LRU/TTL Cache
```javascript
const cache = new Map();
const TTL = 5 * 60 * 1000;
function getCached(key) {
  const hit = cache.get(key);
  if (!hit) return null;
  if (Date.now() - hit.ts > TTL) {
    cache.delete(key); // evita crescimento infinito
    return null;
  }
  return hit.value;
}
```

---

## ⚠️ Pitfalls

- **Non-deterministic GC**: massive allocation on hot paths (every user event generating objects) causes GC pauses that are hard to predict; reduce the allocation rate, do not trust that "the GC will handle it".
- **Layout thrashing / forced synchronous layout**: interleaving reads and writes of layout properties (`offsetHeight` ↔ `style.height`) forces a reflow on every iteration — separate reads from writes (or use requestAnimationFrame batching).
- **postMessage with giant objects**: structured clone duplicates memory and freezes the thread — transfer `ArrayBuffer`s or use `SharedArrayBuffer`.
- **Misleading benchmarks**: a single engine, eliminated dead code, or stray code skew the results; test across several browsers and make sure to consume the results.
- **Runtime dependencies**: immutability/functional helper libraries on large datasets cost more than native — "everything is a trade-off".

---

## 🔗 Integration with Other Skills

- [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md): latency laws, tail latency, and elimination of unnecessary work applied to the web.
- [code-optimizer](../../roles/code-optimizer/SKILL.md): the algorithm → structure → runtime → parallelism hierarchy applied to JS applications.
- [webassembly](../webassembly/SKILL.md): Wasm as the ultimate destination for hot paths (Emscripten, wasm-pack, SharedArrayBuffer/Atomics).
- [framework-react](../../frameworks/framework-react/SKILL.md): state immutability, memoization, and re-renders in the React ecosystem.
- [framework-vue](../../frameworks/framework-vue/SKILL.md): reactivity based on getters/setters and Proxies (the same fundamentals as the vanilla chapter).
- [frontend-developer](../../roles/frontend-developer/SKILL.md): integrating performance optimizations into the UI construction cycle.
