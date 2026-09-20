---
name: lang-java
description: Provides software engineering patterns in modern Java (Java 17/21/25 LTS) based on the official documentation (docs.oracle.com/en/java), Java Concurrency in Practice (Goetz), and JVM best practices. Covers lambdas/Streams, Records and sealed classes, Virtual Threads (Project Loom), safe concurrency (Executor framework, immutability, happens-before, CompletableFuture), Collections, Pattern Matching, JCTools/Agrona, and JVM tuning (G1/ZGC, JIT).
---

# AI Skill: Java Software Engineering (Modern Java and Concurrency)

This skill guides the AI to write modern, idiomatic, thread-safe Java code, based on the official Java documentation (JDK 21/25 LTS — docs.oracle.com/en/java) and *Java Concurrency in Practice* (Brian Goetz et al., Addison-Wesley).

---

## 🧭 1. Modern Java (Language)

- **Records**: use for immutable data (Value Objects, DTOs). Compose with `record` patterns for safe deconstruction.
- **Sealed classes/interfaces**: model closed hierarchies (ADTs) combined with pattern matching in exhaustive `switch`.
- **Text blocks and switch expressions**: prefer `switch` as an expression (arrows, compiled exhaustiveness) over if/else chains.
- **Optional**: return type for queries that may be empty; **never** for fields or parameters (anti-pattern).
- **Streams**: express pipelines over collections; be careful on hot paths (lambda/box allocation); use traditional loops where the profiler points to a bottleneck.
- **Var and generics**: `var` for an obvious local type; write generics with PECS (correct `extends`/`super` wildcards) and bounded types.
- **Immutability by default**: `final` fields, closeable classes, immutable collections (`List.of`, `Map.copyOf`). Immutable objects are thread-safe for free.

---

## 🔀 2. Safe Concurrency (Java Concurrency in Practice)

### 2.1 Shared state and visibility
- **Rule of thumb**: whenever more than one thread accesses the same mutable state, **all** access paths must use the same lock.
- **Volatile**: guarantees visibility and ordering (happens-before), not compound atomicity. Use it for stop flags and safe publication; never for `count++`.
- **Happens-before**: monitor locks, `volatile`, `Thread.start/join`, `Executor.submit`, and `CompletableFuture` establish happens-before; without it, JIT reorderings make published data inconsistent (stale data, reordering).
- **Escape analysis and publication**: publish immutable objects freely (safe publication); mutable objects require synchronization, `final` fields, or fences.
- **Thread confinement**: stack confinement (locals), `ThreadLocal` — zero synchronization when state does not cross threads.

### 2.2 Composing thread-safe objects
- **Delegation**: compose safety from thread-safe classes (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `AtomicLong`, `BlockingQueue`).
- **Multi-variable invariants** (e.g., `lower <= upper`): require **a single lock** covering every field of the invariant; delegating per variable breaks the invariant.
- **Fragile client-side locking**: only works if the "client" knows which lock the class uses; prefer extension by composition.
- **Immutability as a strategy**: immutable objects can be shared without a lock (the happens-before rule for the `final` field).

### 2.3 Building blocks (java.util.concurrent)
- **Executor framework**: never create a raw `Thread` in production — decouple submission from execution with `ExecutorService` (named thread pools, `ManagedThreadFactory` in containers).
- **BlockingQueues** (`ArrayBlockingQueue`, `LinkedBlockingQueue`, `SynchronousQueue`): producer/consumer with natural backpressure.
- **Synchronizers**: `CountDownLatch` (wait for N events), `Semaphore` (limit access), `CyclicBarrier` (synchronization points), `Phaser` (phases).
- **ConcurrentHashMap**: do not synchronize the map manually; use `compute`, `computeIfAbsent`, `putIfAbsent` for per-key atomicity.
- **CompletableFuture**: non-blocking async composition (`thenApply/thenCompose/thenCombine`, `orTimeout`); avoid `get()` without a timeout.

### 2.4 Task execution and pools
- **Pool size**: CPU-bound ≈ `Runtime.availableProcessors()`; IO-bound ≈ `cores × (1 + wait/compute)`. Prefer bounded queues (`ArrayBlockingQueue`) + a saturation policy (`CallerRunsPolicy` to degrade gracefully, or rejection with backpressure).
- **Platform executors vs `newVirtualThreadPerTaskExecutor`**: I/O-intensive with millions of tasks → Virtual Threads; CPU-intensive → a fixed pool of Platform Threads.
- **Find the exploitable parallelism** (Amdahl's Law): adding threads beyond the CPU core count does not speed up CPU-bound workloads; it adds cache pollution and context switches.

### 2.5 Cancellation, shutdown, and liveness
- **Cooperation**: implement cancellation via interruption (`Thread.interrupt`, periodic `isInterrupted` checks) or a `volatile` cancel flag.
- **Time-outs on every blocking call**; never `Thread.stop`/`suspend` (deprecated/destructive).
- **Deadlock** (lock-ordering cycles): order lock acquisition globally; alternatives with `tryLock` timeout (recovery without deadlock).
- **Starvation and livelock**: avoid thread priorities; fairness (`new ReentrantLock(true)`) only where strictly necessary.
- **Graceful shutdown**: `shutdown()` + `awaitTermination` + shutdown hooks for persistent state.

### 2.6 Contention and performance
- **Reduce contention**: short lock scope, lock striping/concurrent collections, copy-on-write for read-heavy, atomics (CAS) for light counters (`LongAdder` under high contention).
- **Nonblocking algorithms** (CAS/lock-free): `AtomicReference`/`AtomicStampedReference` (ABA with versioning); prefer mature libraries (JCTools, Agrona) over homemade lock-free code.
- **False sharing**: pad fields shared across threads onto distinct cache lines (`@Contended`/jdk.internal.vm.annotation or manual padding).

---

## 🧵 3. Virtual Threads (Project Loom, JDK 21+)

Based on the official documentation (docs.oracle.com/en/java/javase/21/core/virtual-threads.html, JEP 444):

- **What they are**: `java.lang.Thread` instances implemented by the Java runtime (not the OS), mapping millions of virtual threads onto a few platform *carrier threads*. A blocking I/O operation suspends (unmounts) the virtual thread, freeing the carrier.
- **They provide scale (throughput), not speed (latency)**: they do not run code faster than platform threads; they exist to widen concurrency in thread-per-request servers.
- **When to use them**: very high concurrent throughput with mostly I/O-blocked tasks (HTTP, JDBC); **not** for CPU-intensive or long-running tasks.
- **Write simple synchronous code with blocking I/O**: the thread-per-request style with blocking APIs benefits most; avoid mixing synchronous blocking code with asynchronous frameworks (callbacks/chained CompletableFuture do not benefit).
- **Never pool virtual threads**: create one executor per task with `Executors.newVirtualThreadPerTaskExecutor()` (lightweight, closeable with try-with-resources). The number of virtual threads should equal the number of concurrent tasks, like "strings for names".
- **Use `Semaphore` to limit concurrency** (e.g., an external service that accepts 10 simultaneous calls) instead of a thread pool — queues of blocked threads are equivalent to queues of tasks. Database connection pools already work as semaphores.
- **Pinning**: a virtual thread **does not unmount from its carrier** when it blocks inside a `synchronized` block/method or a `native`/FFM method. Frequent, long pinning hurts scalability.
  - Detection: JFR event `jdk.VirtualThreadPinned` (default > 20 ms) or `-Djdk.tracePinnedThreads=full|short`.
  - Fix: replace `synchronized` with `ReentrantLock` (`lock.lock(); try { ... } finally { lock.unlock(); }`) at long points; keep `synchronized` for short/infrequent operations.
- **ThreadLocal**: be careful with caches of expensive objects in `ThreadLocal` (e.g., `SimpleDateFormat`) — with millions of virtual threads, each task instantiates a new object (the opposite of the intended effect). Prefer shared immutable objects (`DateTimeFormatter`) or Scoped Values.
- **Observability**: dumps with `jcmd <pid> Thread.dump_to_file -format=json <file>`; JFR events `jdk.VirtualThreadStart/End/Pinned/SubmitFailed`.

---

## ⚡ 4. JVM Tuning and Performance Best Practices

- **GC**: G1 (balanced default), ZGC/Shenandoah (sub-ms latency with large heaps); size `-Xms`/`-Xmx` equal in production; monitor pauses and full GC frequency.
- **JIT**: small hot methods get inlined; avoid megamorphic call sites (stay bimorphic), large cold methods break inlining.
- **Measurement**: microbenchmarks with JMH (forks, warmup, blackhole); never a bare `System.nanoTime`; async-profiler/flamegraphs for CPU and allocation.
- **Collections**: choose by access profile (`HashMap` vs `ConcurrentHashMap`, `ArrayDeque` instead of `Stack`, typed `EnumMap`); sizing properly (`initialCapacity`) avoids rehashing.
- **Strings and I/O**: `StringBuilder` in loops; buffers with an adequate size; explicit UTF-8.

---

## 🧪 5. Implementation and Review Protocol (Java)

1. **Model shared state**: identify shared mutable variables and choose a strategy (immutable > confinement > concurrent collection > lock).
2. **Decouple tasks with Executors**: define a documented policy (pool size, queue, saturation, naming, context propagation).
3. **Prove thread-safety**: identified invariant + the mechanism that protects it + a concurrent stress test (e.g., jcstress for advanced algorithms).
4. **Prefer high-level APIs** (`java.util.concurrent`) over hand-rolled primitives (`synchronized/wait/notify`).
5. **Instrument and measure**: p99 latency, GC, contention (jstack, JFR, jitwatch) before/after the change.
6. **Document**: shared states with the lock/guard that protects them, invariant rationale, and shutdown policy.

---

---

## 🧼 6. Java Distiller: Refactoring, Modernization, and Idiomatic Code (Java 21/25)

Inspired by the *Java Distiller* principles from the SouJava community, apply rigorous simplification and the elimination of accidental complexity:

### 6.1 Canonical Modernization Transformations
1. **POJO / JavaBean to Record**:
   - Replace verbose data-transport classes (manual getters, setters, equals, hashCode) with `record`.
   - Use deconstruction with Record Patterns:
     ```java
     if (response instanceof SuccessResponse(var payload, var timestamp)) {
         process(payload);
     }
     ```
2. **Imperative Loops to Stream Pipelines & Gatherers**:
   - Convert loops with accumulators and list mutation into declarative Streams:
     ```java
     // Before: imperative accumulator loop
     // After:
     var activeNames = users.stream()
         .filter(User::isActive)
         .map(User::name)
         .toList();
     ```
3. **Switch Expressions & Sealed Hierarchies**:
   - Eliminate `instanceof` trees and manual casts. Use exhaustive `switch` with type pattern matching:
     ```java
     return switch (event) {
         case OrderCreated e -> handleCreated(e);
         case OrderCancelled e -> handleCancelled(e);
     };
     ```
4. **Legacy Date/Calendar to `java.time`**:
   - Eliminate `java.util.Date`, `Calendar`, and `SimpleDateFormat` (not thread-safe). Use `Instant`, `LocalDate`, `ZonedDateTime`, and `DateTimeFormatter`.
5. **Eliminating Clutter ("Distill, don't decorate")**:
   - Remove intermediate abstractions that only delegate calls without adding domain value.
   - Preserve identical functional behavior with fewer lines and greater expressiveness.

---

## 🔗 Integration with Other Skills

- [jpa-hibernate-performance](../../data/jpa-hibernate-performance/SKILL.md): efficient persistence (N+1, batching, cache) in Java.
- [backend-developer](../../roles/backend-developer/SKILL.md): service and API integration with REST/gRPC contracts.
- [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md): thread pool sizing with Little's Law and lock contention reduction.
- [lang-python](../lang-python/SKILL.md) and [python-performance-parallelism](../../engineering/practices/python-performance-parallelism/SKILL.md): concurrency equivalents in Python (GIL vs Loom).
- [code-optimizer](../../roles/code-optimizer/SKILL.md): the optimization agent orchestrates this skill in Java refactors.
