# Book Guide: Hands-On JavaScript High Performance (Justin Scherer)

> Chapter-by-chapter consolidated reference for the book *Hands-On JavaScript High Performance* (Justin Scherer, Packt Publishing). Author: Justin Scherer. Source: a local conversion workspace `JavaScript High Performance (Justin Scherer) (z-library.sk, 1lib.sk, z-lib.sk).md`.

---

## Chapter 1 — Tools for High Performance on the Web

Profiling and benchmarking tools in the main browsers.

- **DevTools per browser**: Edge (Chromium fork), Safari (Web Inspector), Firefox, Chrome — each engine optimizes differently.
- **Chrome Performance tab** (in-depth): runtime timeline recording with Scripting/Rendering/Painting categories, a call-stack flame chart, and an event log of interactions (click, paint, GC).
- **Chrome Memory tab** (in-depth): Heap Snapshot (comparing snapshots to find retained objects/leaks), Allocation instrumentation on timeline, Allocation sampling.
- **Chrome Rendering tab** (in-depth): Paint flashing, FPS meter, Layout Shift regions — visual telemetry in real time.
- **jsPerf**: correct benchmarking — watch out for engine optimizations (dead code), run on multiple browsers, with no stray code in the test cases.

**Techniques**: profiling-first methodology, comparing a `for` loop vs `Array.filter` in a benchmark (the native loop wins on hot paths).

## Chapter 2 — Immutability versus Mutability: The Balance between Safety and Speed

- **The current fascination with immutability**: Redux and the Flux pattern — immutable store, actions, reducers, change by reference for `connect`/`shouldComponentUpdate`.
- **Immutable.js**: persistent `List`, `Map`, `Set` (tries with structural sharing) — cleaner code, but slower and more memory-hungry than native on large datasets; a practical comparison converting lists of lists into a list of objects (CSV-like): vanilla wins.
- **Writing safe mutable code**: encapsulate mutation, avoid mutable shared state between modules.
- **RAII (Resource Allocation Is Initialization / SBRM)**: release resources in the same scope that created them (inspired by C++/Rust).
- **Functional style**: lazy evaluation (generators/iterators evaluate on demand), tail-end recursion (prefer iteration; TCO is not guaranteed in the engines), currying (composition with the cost of closures).

## Chapter 3 — Vanilla Land: Looking at the Modern Web

The ECMAScript feature set up to 2020 through a performance lens.

- `let`/`const` block scoping, arrow functions, classes, and modules (ESM).
- **Collection types**: `Map`, `Set`, `WeakMap`, `WeakSet` (weak keys allow GC).
- **Reflection and Proxies**: intercepting operations (the basis of reactivity); a cost per access.
- Spread operator, destructuring, power operator, parameter defaults, string templates.
- **Typed Arrays** (`Int8Array`...`Float64Array`, `ArrayBuffer`) for contiguous/typed memory; **BigInt** for arbitrary integers; Internationalization API.
- **DOM**: `querySelector`, `DocumentFragment` (batch insertions = 1 reflow), Shadow DOM, Web Components, `<template>`.
- **Fetch API + Promises**: chaining, `AbortController` to cancel requests.

## Chapter 4 — Practical Example: A Look at Svelte and Being Vanilla

- Svelte = a framework **compiled to vanilla JS**; no virtual DOM and no runtime in production.
- `svelte` compiles reactive declarations into minimal imperative DOM-update code.
- Practical build: a Todo app and a weather app — small components, local state, surgical updates.
- Lesson: pushing work from runtime to build time is performance architecture.

## Chapter 5 — Switching Contexts: No DOM, Different Vanilla (Node.js)

- Installing Node.js and the role of `package.json` (scripts, deps, type).
- Native modules: `fs` (files), `net` (sockets), `http` (server) — no libraries for the basics.
- **First introduction to streams** (non-blocking I/O) and an overview of ES modules in Node.
- Debugging and inspecting Node code (inspector).

## Chapter 6 — Message Passing: Learning about the Different Types

- Local communication with `net` (local/TCP sockets) and IPC between processes.
- **cluster module**: workers per core to scale beyond a single thread.
- TCP (reliable, ordered) vs **UDP** (minimal latency, no handshake).
- **HTTP/2**: multiplexing, binary, header compression — no HTTP/1.1 head-of-line blocking.
- **HTTP/3/QUIC**: UDP-based, 0-RTT; the `node-quic` library.

## Chapter 7 — Streams: Understanding Streams and Non-Blocking I/O

- Readable/Writable/Duplex/Transform interfaces and backpressure via `highWaterMark`.
- Implementing a custom Readable, Writable, Duplex, and Transform from scratch.
- **Generators with streams** for concise pipelines.

## Chapter 8 — Data Formats: Different Data Types Other Than JSON

- Native JSON (`JSON.parse`/`stringify`) as the baseline; schema-less vs schema-based.
- Implementing a **custom binary encoder/decoder** (with the schema sent alongside the data).
- **MessagePack** (the `what-the-pack` lib): a pre-allocated buffer (`initialize(2**22)`), compact binary payload — but it may be neither smaller nor faster than native JSON; trade-offs.
- **Protocol Buffers (proto3)**: a shared schema, numeric field IDs, compact encoding; Node and browser libraries.

## Chapter 9 — Practical Example: Building a Static Server

- Applying chapters 5–8: a static server with `fs` + `http` + streams.
- A templating system (basic server-side rendering).
- **Caching** (with TTL / LRU — "ubiquitous with caches") and **clustering** for scale.

## Chapter 10 — Workers: Dedicated and Shared Workers

- **Dedicated Workers**: offloading processing from the main thread; communication via `postMessage`.
- **The cost of structured clone**: 100,000 objects took 800 ms–1.7 s and 80–100 MB of heap (measured with `Date.now()` + the Performance tab).
- **Transferrables**: `postMessage(view, [view.buffer])` — zero-copy transfer of binaries (an Int32Array of 1M elements); the sender loses access (the buffer is detached).
- Sending binary data in the browser; **Shared Workers** for sharing between pages/tabs.
- **Shared cache in a worker**: "decorating data" (join/attribution on the frontend) with an in-memory cache in the worker; mentions TTL/LRU.

## Chapter 11 — Service Workers: Caching and Making Things Faster

- The ServiceWorker lifecycle (install → waiting → activate), scope.
- **Caching pages/templates for offline use** (Cache Storage) — the basis of a PWA.
- **Save requests for later**: queueing mutations offline and replaying them when the network returns.

## Chapter 12 — Building and Deploying a Full Web Application

- **Rollup**: an ES-module bundler with tree shaking; building the static server into a single distributable; including asset types; integration via npm scripts.
- **CircleCI**: a CI/CD pipeline — build steps, security checks, deploying the build.

## Chapter 13 — WebAssembly: A Brief Look into Native Code on the Web

- Program model and sandbox (no memory leaking between WASM modules).
- Writing **WAT** modules directly; environment setup and loading via the static server (`application/wasm`).
- **Shared memory** between WebAssembly and JavaScript (Linear Memory / `WebAssembly.Memory`).
- **FizzBuzz in WASM** and writing **C/C++ for the web** (compiling to wasm).
- Case: a **Hamming code** generator in C++; **SQLite in the browser** via WASM.

---

## Tools/Technologies Cited in the Book

- DevTools (Chrome Performance/Memory/Rendering, Firefox, Safari Web Inspector, Edge), jsPerf
- Redux, Immutable.js
- Svelte
- Node.js (`fs`, `net`, `http`, `cluster`, streams), `node-quic`
- `what-the-pack` (MessagePack), Protocol Buffers (proto3)
- Web Workers (Dedicated/Shared), Transferrables, Cache Storage, Service Workers
- Rollup, CircleCI
- WebAssembly (WAT, Emscripten/C++), SQLite-in-WASM
