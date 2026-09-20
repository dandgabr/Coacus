---
name: python-performance-parallelism
description: Acts as a specialist in Python optimization, high performance, and parallelism, based on High Performance Python 2nd Edition (Gorelick & Ozsvald), Fast Python (Tiago Antão), and Parallel and High Performance Programming with Python 2nd Edition (Fabio Nelli). Covers profiling (cProfile, line_profiler, py-spy, scalene), CPU and memory optimization, vectorized NumPy/pandas, multiprocessing vs. threads vs. asyncio (GIL/free-threading), Cython/Numba, GPUs (CUDA/RAPIDS), Dask/Ray/PySpark, and distributed parallelism on cloud/serverless.
---

# AI Skill: Python High Performance and Parallelism

This skill guides the artificial intelligence to diagnose and eliminate CPU, memory, and I/O bottlenecks in Python, and to scale workloads across multiple cores, machines, and GPUs, based on *High Performance Python* (Gorelick & Ozsvald), *Fast Python* (Tiago Antão), and *Parallel and High Performance Programming with Python* (Fabio Nelli).

---

## 📏 1. Golden Rules of Optimization

1. **Measure before optimizing**: never optimize on intuition — profile first (the 90/10 rule: 90% of the time is in 10% of the code).
2. **Optimize the algorithm before the code**: a complexity downgrade (O(n²) → O(n log n)) beats any micro-optimization.
3. **Move the hot loop to C**: builtins, NumPy, Cython, Numba, or a native library — pure Python should orchestrate, not iterate, on hot paths.
4. **Conscious trade-off**: latency vs. throughput vs. memory vs. readability — document the chosen trade-off.
5. **Benchmark in a representative environment**: realistic data, an isolated machine, warmup, and statistical repetitions (`timeit`, `pytest-benchmark`).

---

## 🔍 2. Profiling (the mandatory starting point)

| Tool | Scope | Typical use |
| :--- | :--- | :--- |
| `cProfile` / `profile` | Functions (callers/callees, tottime/cumtime) | First pass: `python -m cProfile -s cumtime script.py` |
| `line_profiler` (`@profile`) | Line by line | Locate the hot line inside the identified function |
| `memory_profiler` / `tracemalloc` | Memory per line/snapshot | Leaks and RAM spikes |
| `py-spy` | Sampling (CPU) in production | Flamegraphs without instrumenting code (`py-spy dump`/`py-spy top`) |
| `pyinstrument` | Hierarchical statistical profiler | Lower overhead than cProfile, stack view |
| `scalene` | CPU + memory + GPU together | Integrated diagnosis with % interpreted vs. native |
| `perf` + `python -X importtime` | OS level, imports | Cold start, startup time |

- **Flow**: cProfile → identify the hot function → line_profiler → understand the line → only then optimize.

---

## 🧮 3. CPU Optimization (pure Python → native code)

### 3.1 Data structures and algorithms
- Choose by amortized complexity: `set`/`dict` (O(1) membership) vs. `list` (O(n)); `collections.deque` for queues/fronts; `heapq` for priorities; `Counter`/`defaultdict` for aggregations.
- **Comprehensions > loops with append**; avoid loops with repeated method calls (hoist invariants out of the loop).
- Localize **string formatting**: f-strings/join > concatenation in a loop; avoid accumulating strings with `+` (O(n²)).

### 3.2 NumPy and vectorization
- **Single rule: no Python loops over arrays** — operate on whole vectors/matrices (broadcasting, ufuncs).
- Vectorize phenomena such as the Julia set, normalizations, and distances: array-wise addition/subtraction instead of element by element (typically 100×+).
- Ideal: homogeneous numeric data; poor: heterogeneous/structured data (use pandas or dicts).

### 3.3 Efficient pandas
- **Chainable and vectorized**: `.assign`, `.query`, `.eval` (numexpr backend); **never** `iterrows()` (use `itertuples` at worst, or vectorized operations).
- `category` dtype for repeated columns (roughly 10× less memory); downcast numerics (`pd.to_numeric(..., downcast=)`).
- Avoid `apply` along the row axis — vectorize or use native methods; an aligned index costs: reset it when not needed.

### 3.4 Compilation and native acceleration
- **Cython**: optional statically-typed superset (`cdef`, typed memoryviews) — speeds up pure loops; use `cython -a` to analyze Python↔C interactions.
- **Numba**: `@njit(parallel=True)` (prange) — LLVM JIT for numeric functions; `@vectorize`/`@guvectorize` for ufuncs; the first call pays compilation (cache=True).
- Rule: profile → isolated hot function → Numba if purely numeric, Cython if it mixes Python structures.

---

## 💾 4. Memory Optimization

- **Iterators and generators** instead of materialized lists (streaming files/lines); `yield from` composition.
- Compact structures: homogeneous `array.array`, `__slots__` on classes with many objects, `dataclasses(slots=True)`, reduced NumPy types (float32/int32 when sufficient).
- Del and GC: break reference cycles; `gc.collect()` at boundary points (batches); watch out for LRU caches (`functools.lru_cache(maxsize=...)`).
- Columnar persistence: **Parquet** (embedded schema, compression, partial reads by columns/predicates) over CSV; memmap for arrays larger than RAM (`np.memmap`, zarr).
- Chunk processing: pandas `chunksize`/dask for datasets larger than memory.

---

## 🧵 5. Concurrency and Parallelism (the decision map)

### 5.1 The GIL and modern Python
- **GIL**: a single thread executes Python bytecode at a time — pure threads do not speed up CPU-bound work (but they release the GIL on I/O and in NumPy/C calls).
- **Python 3.13+ free-threading (PEP 703, experimental)**: builds without the GIL; historical context — verify library support before adopting.
- `concurrent.futures.uninterruptible` does not exist — know `ThreadPoolExecutor` (I/O-bound) vs. `ProcessPoolExecutor` (CPU-bound).

### 5.2 Decision tree
```
Tarefa CPU-bound?
├─ Numérica/Array → NumPy/Numba (@njit parallel)/GPU
├─ Função Python pura isolável → multiprocessing/ProcessPoolExecutor
│   └─ serializável (pickle)? Não → shared memory (multiprocessing.shared_memory)
└─ Mixed → joblib/Swarm paralelismo nivelado
I/O-bound?
├─ Muitas conexões/concorrência alta (1000+) → asyncio (uvloop)
├─ I/O bloqueante legado → threads (ThreadPoolExecutor)
└─ Firewall de subprocessos → multiprocess na borda apenas
Máquina cheia → Dask (distribuído local) / Ray (clusters)
```

### 5.3 Correct multiprocessing
- `ProcessPoolExecutor` / `Pool.map` with efficient chunks (`chunksize` tuned — too small means IPC overhead, too large means load imbalance).
- Serialization cost: `pickle` of arguments/returns — prefer pure functions with compact inputs/outputs (NumPy arrays).
- **Sharing**: `multiprocessing.shared_memory.SharedMemory`/`Array`; a manager proxy only at low frequency; fork vs. spawn (Linux fork is fast, spawn is cross-platform safe; check CUDA compatibility).

### 5.4 asyncio
- For high-concurrency I/O-bound work (HTTP websockets, scrapers, microservice mesh).
- Correct `async/await`: never block the event loop (heavy synchronous I/O, CPU-bound); run CPU blocks in `run_in_executor`.
- `asyncio.gather` (fan-out), `Semaphore` (limit), reused `aiohttp`/`httpx.AsyncClient` (connection pooling enabled).

### 5.5 Distributed: Dask, Ray, or Spark
- **Dask**: scalable pandas/NumPy parallelism (`dask.dataframe`), local scheduler → cluster (SLURM/K8s); lazy columnar partitioning.
- **Ray**: tasks (stateless remote functions), actors (stateful), Ray Data/Datasets for ML pipelines; cloud autoscaling.
- **PySpark**: >= TB scale; DataFrames with the Catalyst optimizer; prefer pandas UDFs (Arrow) over Python row UDFs.
- **joblib**: simple embarrassingly parallel work with a memmap backend (large NumPy, zero-copy).

---

## 🎮 6. GPU and Hardware Acceleration

- **CUDA via Python**: Numba `@cuda.jit` (manual kernels), CuPy (a GPU-mirrored NumPy API), PyTorch tensor ops.
- **RAPIDS**: cuDF (GPU pandas-like) and cuML (sklearn-like) for data/ML pipelines at medium and large dataset sizes.
- Transfer rule: operate *in place* — minimize CPU↔GPU transfers (batch operations, fused kernels); you pay dearly for transfers.
- Engineering consideration: the GPU pays off when compute dominates; small tabular data does better on CPU/vectorized.

---

## 🏹 7. Advanced Multiprocessing (FPGA, Quantum, and Serverless)

- **Stateless servers** (serverless, ch. 14): serverless map-reduce with AWS Lambda (fan-out with SQS/Step Functions); suitable for event-driven process shuffling.
- **FPGA (global chapters)**: via PYNQ/Zynq with Python — a high-frequency trading/inference niche; an extremely high engineering cost.
- **Quantum computing (ch. 16)**: Qiskit in simulation — experimental only.

---

## 🧪 8. Optimization Protocol (executable checklist)

1. **Measure the baseline**: time (wall + CPU) and memory (tracemalloc) with representative data.
2. **Profile**: cProfile → line_profiler → scalene (CPU vs. native vs. memory).
3. **Discard unnecessary work**: caching (`lru_cache`), lazy loading, dedupe, early exit, result reuse.
4. **Apply the hierarchy of improvements**: algorithm/structure → NumPy/pandas vectorization → compilation (Numba/Cython) → concurrency (async/threads/processes) → distributed (Dask/Ray/Spark) → hardware (GPU).
5. **Validate**: same result (equality tests), statistical benchmark (n ≥ 5, variance), memory monitored.
6. **Document**: original bottleneck, technique applied, gain (in time / memory), and assumed trade-off.

---

## 🔗 Integration with Other Skills

- [latency-engineering](../latency-engineering/SKILL.md): capacity modeling (Little/Amdahl) before scaling vertically.
- [lang-python](../../../languages/lang-python/SKILL.md): base language idioms and style.
- [lang-java](../../../languages/lang-java/SKILL.md): concurrency contrast (GIL vs. virtual threads) and JVM vs. CPython.
- [lang-csharp](../../../languages/lang-csharp/SKILL.md): async/await and Task Parallel Library parallelism contrast.
- [data-intensive-systems](../../../data/data-intensive-systems/SKILL.md): batch processing and data-intensive pipelines (MapReduce/Dataflow).
- [code-optimizer](../../../roles/code-optimizer/SKILL.md): the optimization agent orchestrates this skill in Python refactorings.
