---
name: lang-csharp
description: Provides software engineering patterns in modern C# (C# 12/13/14, .NET 8/10 LTS) based on the official documentation (learn.microsoft.com/en-us/dotnet/csharp) and C# 2026 Enterprise Mastery (Victor Mihailov). Covers records and primary constructors, pattern matching, Span<T>/memory-efficient code, async/await and Task, LINQ and collections, pragmatic SOLID, tactical DDD, performance (GC, allocation tracing, pooling), observability, and modern cloud-native API patterns with Minimal APIs.
---

# AI Skill: C# Software Engineering (Modern .NET)

This skill guides the AI to write modern, idiomatic, and performant C# code, based on the official Microsoft documentation (learn.microsoft.com/dotnet/csharp, C# 14 / .NET 10 LTS) and *C# 2026 Enterprise Mastery* (Victor Mihailov).

---

## 🧭 1. Modern C# (C# 9 → C# 14)

- **Records** (`record class` / `record struct`): immutability with value-equality semantics for DTOs and Value Objects; non-destructive mutation via `with`.
- **Primary constructors** (C# 12): reduce ceremony in classes and structs that need no extra construction logic.
- **Collection expressions** (C# 12): `[1, 2, ..other, 9]` — unified initialization syntax with spread.
- **Full pattern matching**: type patterns, property patterns, list patterns (C# 11), relational/logical (`and`, `or`, `not`) in exhaustive `switch` expressions — prefer these over `if/else` chains.
- **`field` backed properties** (C# 14): validate in the `set` without declaring an explicit field — `set => field = value ?? throw new ArgumentNullException(nameof(value));`.
- **Extension members** (C# 14): `extension` blocks add **extension properties** and static members (including operators), beyond classic extension methods.
- **Null-conditional assignment** (C# 14): `customer?.Order = GetCurrentOrder();` replaces a basic null check before assignment.
- **Span<T> first-class** (C# 14): implicit conversions among `Span<T>`, `ReadOnlySpan<T>`, and `T[]` — more natural generics and extension receivers; `params` accepts `ReadOnlySpan<T>` (C# 13), avoiding array allocation.
- **`System.Threading.Lock`** (C# 13): the `lock` statement emits `EnterScope()`/`Dispose` — faster and type-safe compared with `Monitor` over an object.
- **Required members** (C# 11), **file-local types** (C# 11), **file-scoped namespaces** (C# 10), and **global usings** (C# 10): organization and expressiveness.

---

## 🏛️ 2. Pragmatic SOLID and Domain Modeling

- **SRP through cohesion of change**: "one reason to change, not one method"; extract sub-steps when a method mixes levels of abstraction.
- **OCP/DIP with composition**: program to abstractions; inject dependencies (native DI in .NET) instead of newing up inside domain classes.
- **LSP/ISP**: small, cohesive interfaces; avoid "god" interfaces that force empty implementations (they violate LSP).
- **Tactical DDD**: Aggregates with protected invariants, immutable Value Objects (records), Domain Events for side effects; small aggregates with clear boundaries (rule of thumb: an aggregate references others by ID, not by direct navigation).
- **GoF at runtime**: many patterns are built in — Builder (object initializers + required), Strategy (delegates/lambdas), Iterator (`IEnumerable`), Observer (`IObservable`/events), Decorator/Proxy (DI + middleware); **don't implement what the runtime gives you**.
- **Code that lasts**: names that reveal intent, methods at one level of abstraction, early guard clauses, classes closed for modification but open for extension.

---

## ⚡ 3. Performance (GC, Span, Async, AOT)

### 3.1 Memory management and GC
- **Generational GC**: short-lived temporary objects are cheap (Gen0); avoid the LOH (Large Object Heap) for buffers >= 85 KB — use `ArrayPool<T>.Shared`/`MemoryPool<T>` for large reusable buffers.
- **Allocation and profiling**: `dotnet-counters monitor --counters System.Runtime` for GC in production; `dotnet-trace collect --profile gc-verbose` for a 30 s allocation trace; `dotnet-gcdump collect` for a heap snapshot and analysis of the most-allocated types.
- **Struct vs class**: small immutable structs avoid indirection and GC, but beware copying large structs (pass by `in`/`ref readonly`).
- **Pooling and stackalloc**: `stackalloc` for short-lived buffer operations (up to ~1 KB), `Span<T>` for allocation-free slices, `string.Create` for built strings.

### 3.2 Span and memory-efficient code
- Pass `ReadOnlySpan<T>`/`Span<T>` on hot paths (parsing, slicing) instead of arrays/String; avoid intermediate `.ToString()`/`.ToArray()`.
- `Utf8JsonReader`/`Utf8JsonWriter` for high-performance JSON without materializing a `string`.
- **AVX10.2, method devirtualization, and improved inlining** arrive with the .NET 10 runtime — design stable abstraction layers so the JIT can optimize.

### 3.3 Correct async/await
- `async all the way` — never `.Result`/`.Wait()` (deadlock + thread starvation); `ConfigureAwait(false)` in infrastructure libraries.
- **`ValueTask<T>`** for often-synchronous paths (avoids Task allocation); Task when always asynchronous.
- `IAsyncEnumerable<T>` + `await foreach` for async streams; `CancellationToken` propagated through the whole async chain.
- Avoid `async void` (event handlers only); light context capture in hot loops.

### 3.4 Native AOT and cloud-native
- **NativeAOT** for startup < 100 ms and a minimal footprint (serverless/container APIs); disable unsupported dynamic reflection.
- JSON: `System.Text.Json` with source generators (`JsonSerializerContext`) — no reflection, AOT-compatible, and faster.
- Minimal APIs for lightweight endpoints; analyze image size (`dotnet publish /p:PublishAot=true`).

---

## 🏗️ 4. Enterprise Application Patterns (.NET 10)

- **Cloud-Native APIs**: ASP.NET Core 10 (Minimal APIs, integrated OpenAPI, `WebSocketStream`), versioning idioms, and Idempotency-Key on mutations.
- **Observability**: native OpenTelemetry (traces/metrics/logs), structured `ILogger` (no Sensitive Data), ActivitySource for distributed correlation.
- **Entity Framework Core 10**: improved LINQ, multiple named query filters, improved Cosmos DB — see EF Core pitfalls under [jpa-hibernate-performance](../../data/jpa-hibernate-performance/SKILL.md) N+1 equivalents (lazy loading + projection).
- **Security**: Data Protection API, authentication/authorization with passkeys (Identity .NET 10), PQC (ML-DSA) available in the .NET 10 crypto libraries.
- **Resilience**: Microsoft.Extensions.Resilience/Polly v8 (circuit breaker, timeout, retry with backoff) on outbound calls.

---

## 🧪 5. Implementation and Review Protocol (C#)

1. **Model the domain** with records + primary constructors; validate invariants in the constructor/property (`field` keyword).
2. **Define the concurrency strategy** (`async/await` for I/O, `System.Threading.Lock` for exclusion, `Channel<T>` for producer-consumer pipelines).
3. **Perf-first on the hot path**: spans, pooling, source-generated JSON; measure with BenchmarkDotNet before accepting an optimization.
4. **Instrument**: `dotnet-counters`, `dotnet-trace`, `dotnet-gcdump`, JFR-like with EventCounters — see the book example (30 s trace, heap dump, analysis of the most-allocated types).
5. **Tests**: xUnit/NUnit with MTP (`dotnet test` .NET 10), WebApplicationFactory for endpoints; cover domain invariants.
6. **Document** the API with XML comments and OpenAPI; explicit versioning.

---

## 🔗 Integration with Other Skills

- [backend-developer](../../roles/backend-developer/SKILL.md): service integration and REST/gRPC contracts.
- [framework-rest-api](../../frameworks/framework-rest-api/SKILL.md): idiomatic HTTP API design for ASP.NET Core.
- [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md): eliminating work on hot paths and tail latency.
- [code-optimizer](../../roles/code-optimizer/SKILL.md): the optimization agent orchestrates this skill in C# refactors.
- [lang-java](../lang-java/SKILL.md): a direct concurrency parallel (Loom vs async/await) and JVM vs CLR.
