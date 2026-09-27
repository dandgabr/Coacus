---
name: "functional-concurrent-programming"
description: "Provides expert patterns for functional and concurrent programming based on Functional and Concurrent Programming: Core Concepts and Features (Charpentier). Covers pure vs impure functions and immutable data, higher-order functions (map/flatMap/fold), algebraic data types and exhaustive pattern matching, recursion and trampolines, functors and monads with the monad laws, lazy evaluation, threads and locking, thread pools, synchronizers (latches, barriers, semaphores, blocking queues), futures and promises, atomic/CAS, lock-free structures, Fork/Join, actors/CSP and Reactive Streams back-pressure."
---

# AI Skill: Functional and Concurrent Programming

This skill guides the AI to write code that is concurrent by construction — immutability, pure functions, and message passing where possible — and to reason precisely about ordering and synchronization where it is not. It builds on *Functional and Concurrent Programming: Core Concepts and Features* (Charpentier).

---

## 🧭 When to Activate

- Designing concurrent or parallel systems.
- Deciding between shared-state locking and message passing.
- Using higher-order functions, monads, or lazy evaluation functionally.
- Implementing futures/promises, thread pools, or synchronizers.
- Diagnosing deadlocks, data races, or blocking bottlenecks.

---

## 🧩 Functional Foundations

- **Pure vs impure functions:** impurity = side effects *and* nondeterminism (reliance on mutable external state). **Actions** are Unit-returning, side-effect-only functions. Prefer expressions over statements.
- **Immutability:** functional variables and immutable objects; mutable state is implemented *inside* immutable abstractions.
- **Algebraic data types & pattern matching:** case classes, extractors, exhaustive matches (no silent fall-through).
- **Recursion:** tail recursion; **trampolines** to avoid stack growth; recursion on lists and trees.
- **Higher-order functions:** `map`, **`flatMap`** (fundamental — `map` and `filter` derive from it), `fold`/`reduce`, `iterate`, `unfold`, `groupBy`, for-comprehensions.
- **Functor/monad laws:** `unit: A => M[A]`; `flatMap: M[A] => (A => M[B]) => M[B]`; left identity `unit(x).flatMap(f) == f(x)`, right identity `struct.flatMap(unit) == struct`, associativity `struct.flatMap(f).flatMap(g) == struct.flatMap(x => f(x).flatMap(g))`.
- **Lazy evaluation:** by-name arguments, `lazy val`, memoization.

---

## 🔒 Concurrency: Shared State

- Threads introduce **nondeterminism**; **atomicity and locking** restore invariants. Use intrinsic locks deliberately; **thread-safe objects** encapsulate their synchronization policy, avoid reference escape, and hide the lock.
- Respect the **memory model**: `volatile` and happens-before determine visibility; without them a "correct" algorithm races.
- **Thread pools** (fire-and-forget, parallel server, parallel collections) bound resource use; deadlocks are diagnosed from thread dumps.

**Synchronizers:** latches and barriers, semaphores (the two-semaphore idiom), conditions, and **blocking queues** (the workhorse for producer/consumer).

---

## 🚀 Concurrency: Message Passing and Async

- **Futures and promises:** futures are synchronizers with timeouts/failures/cancellation; **promises** are write-once completion handles; compose futures with `flatMap`/`thenCombine`/`zipWith`.
- **Minimize blocking:** atomic operations (`AtomicInteger`, **compareAndSet/CAS**), **lock-free structures** (a lock-free stack pushes/pops via CAS on the top pointer), and **Fork/Join** pools for divide-and-conquer.
- **Asynchronous programming:** async/await style composition.
- **Actors** (Erlang/Akka): immutable messages, sequential mailbox processing, a small thread pool drives many actors; send (`!`) is inherited from **CSP**.
- **Reactive Streams:** `Flux`/`Mono` with **back-pressure** and time-based windowing; non-blocking synchronization throughout.

---

## ⚖️ Guidance

- Prefer immutability and message passing over shared mutable state; fall back to locks only when necessary and encapsulate them.
- Use `flatMap` as the primary composition operator; understand the laws before writing monadic code.
- Bound concurrency with pools and back-pressure; unbounded queues hide overload until collapse.
- Make blocking explicit and rare on latency-sensitive paths.

---

## ⚠️ Pitfalls

- Hidden shared mutable state defeating immutability.
- Lock ordering and lock granularity causing deadlock.
- Relying on non-volatile state across threads.
- Unbounded thread creation or queues.
- Treating `flatMap` chains as free — they can hide allocation and blocking.

---

## 🔗 Integration with Other Skills

- For lock-free/low-latency specifics, see [latency-engineering](../latency-engineering/SKILL.md).
- For language-level concurrency (Java virtual threads, Rust async), see [lang-java](../../../languages/lang-java/SKILL.md) and [lang-rust](../../../languages/lang-rust/SKILL.md).
- For actor/task distribution, see [distributed-systems](../distributed-systems/SKILL.md).
