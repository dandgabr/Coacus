---
name: "gpu-programming-cuda"
description: "Provides expert patterns in GPU parallel programming with C++ and CUDA based on GPU Programming with C++ and CUDA (Paulo Motta), covering the parallelism taxonomy, SIMT and GPU architecture, the CUDA execution model (kernels, threads, blocks, grids, warps), host-device memory management, coalescing and shared-memory tiling, streams and asynchronous overlap, occupancy, register pressure, reductions and atomics, cuBLAS/Thrust, Nsight profiling and roofline analysis."
---

# AI Skill: GPU Parallel Programming with C++ and CUDA

This skill guides the AI to act as a specialist in **GPU-accelerated computing** with C++ and CUDA, building on *GPU Programming with C++ and CUDA* (Paulo Motta). The GPU is a **throughput** machine: many small cores hide memory latency by executing thousands of warps, in contrast to the CPU's few latency-optimized cores.

Resolve current CUDA Toolkit, compute-capability and library versions from the publisher (NVIDIA) before naming them; the version-agnostic patterns below are stable across recent toolkits.

---

## 🧭 When to Activate

- Designing or optimizing data-parallel kernels (vector/matrix math, image processing, simulation, sorting, reductions).
- Diagnosing kernel performance: long-scoreboard stalls, low occupancy, uncoalesced access, register spilling.
- Deciding between custom kernels and library calls (cuBLAS, Thrust, cuDNN).
- Overlapping host-device transfer with compute using streams.
- Exposing C++ GPU code to Python.

---

## 🧠 Parallelism Taxonomy and Architecture

Three exploitable forms: **data parallelism** (same op over partitioned data), **task parallelism** (distinct ops concurrently), and **pipeline parallelism** (stages feeding the next). Sequential parts are bounded by **Amdahl's Law** and the **critical path** of the decomposition.

GPU structure: **threads** group into **blocks** (a software grouping that can synchronize and share memory), blocks into a **grid**; hardware groups threads into **warps of 32** that execute in lockstep (**SIMT**). **Streaming multiprocessors (SMs)** carry warp schedulers that switch between ready and memory-waiting warps to hide latency. Distinguish **SIMD** (one instruction over many lanes) from **SIMT** (SIMD with per-thread state, hardware-managed).

---

## 🛠️ The CUDA Execution Model

Index patterns and a bounds-guarded kernel:

```cpp
__global__ void vectorAddKernel(float* A, float* B, float* C, int N) {
  int i = threadIdx.x + blockIdx.x * blockDim.x;
  if (i < N) C[i] = A[i] + B[i];
}
// launch: <<<blocksPerGrid, threadsPerBlock, sharedBytes, stream>>>
vectorAddKernel<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
```

`threadIdx/blockIdx/blockDim/gridDim` are `dim3`; the third launch argument sets dynamic shared-memory size (the remainder of the SM partition becomes L1). Query devices with `cudaGetDeviceProperties(&prop, 0)` for `name`, `major/minor` (compute capability), `sharedMemPerBlock`, `maxThreadsPerBlock`, `memoryClockRate`, `memoryBusWidth`.

**Host-device memory:** `cudaMalloc((void**)&d, bytes)`, `cudaMemcpy(dst, src, bytes, cudaMemcpyHostToDevice | cudaMemcpyDeviceToHost)`, `cudaFree`. **Pinned/page-locked** host memory (`cudaHostAlloc` / `cudaMallocHost`) is required for asynchronous transfers; **`cudaMemcpyAsync`** returns control immediately. **Unified memory** (`cudaMallocManaged`) is simpler but migrates pages on demand (variable granularity, slower). **Zero-copy** suits only small datasets.

---

## ⚡ Streams, Events and Synchronization

Streams (`cudaStreamCreate`/`cudaStreamDestroy`, default stream 0) let H2D transfer, compute and D2H overlap across kernels. Synchronize with `cudaStreamSynchronize`, `cudaDeviceSynchronize` (all streams, heavier) or `cudaEventSynchronize`. The **chunk size** for streamed work is the key tuning knob: too small is transfer-bound, too large idles the GPU.

Timing uses CUDA events:

```cpp
cudaEvent_t startEvent, stopEvent;
cudaEventCreate(&startEvent); cudaEventCreate(&stopEvent);
cudaEventRecord(startEvent, 0);
kernel<<<blocks, threads>>>(/*...*/);
cudaEventRecord(stopEvent, 0);
cudaEventSynchronize(stopEvent);
float ms; cudaEventElapsedTime(&ms, startEvent, stopEvent);
```

Intra-block barriers use `__syncthreads()`; atomics and shared-memory tree reductions serialize conflicting accumulation:

```cpp
extern __shared__ double sharedData[];
for (int s = blockDim.x/2; s > 0; s /= 2) {
  if (threadIdx.x < s) sharedData[threadIdx.x] += sharedData[threadIdx.x + s];
  __syncthreads();
}
if (threadIdx.x == 0) result[blockIdx.x] = sharedData[0];
```

---

## 🔬 Memory Hierarchy and Optimization

Hierarchy: global (large, slow, off-chip) → L2 → L1/shared (SM-local) → **registers** (fastest).

- **Coalescing**: consecutive threads accessing contiguous, aligned addresses maximize DRAM efficiency; strided/column access is the worst case.
- **Register pressure**: too many locals spill to local memory; building with `-O3` raises register use and collapses time.
- **Shared-memory tiling** (matmul, `TILE 16`) reuses data across the block:

```cpp
__shared__ float Asub[TILE][TILE], Bsub[TILE][TILE];
int tx=threadIdx.x, ty=threadIdx.y, row=ty+blockIdx.y*blockDim.y, col=tx+blockIdx.x*blockDim.x;
float sum=0.f;
for (int i=0; i<(n+blockDim.x-1)/blockDim.x; i++){
  if (row<n && i*blockDim.x+tx<n) Asub[ty][tx]=A[row*n + i*blockDim.x+tx];
  if (col<n && i*blockDim.y+ty<n) Bsub[ty][tx]=B[(i*blockDim.y+ty)*n + col];
  __syncthreads();
  for (int k=0;k<blockDim.x;k++) sum += Asub[ty][k]*Bsub[k][tx];
  __syncthreads();
}
if (row<n && col<n) C[row*n+col]=sum;
```

- **Loop unrolling** (`#pragma unroll`) and **fused multiply-add** (`fmaf`) raise throughput at the cost of registers.
- **Occupancy** = active warps / SM maximum; **256 threads/block** is the common balance. High occupancy hides latency up to a point; excess waiting warps degrade performance.

**Pitfall:** a tiled kernel can *underperform* the naive one in Debug builds — profile only Release.

---

## 📚 Libraries and Python Integration

- **cuBLAS** uses column-major data; pass `CUBLAS_OP_T` to consume row-major matrices: `cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_T, N,N,N, &alpha, d_A,N, d_B,N, &beta, d_C,N);`
- **Thrust** offers an STL-like interface: `thrust::device_vector<T> d = h; thrust::sort(d.begin(), d.end());`
- **Python exposure**: build a C++ library with a proxy function wrapping malloc/copy/kernel/free, call it via `ctypes`, and aim for **zero-copy** through the array interface.

---

## 📊 Profiling Methodology

Use **Nsight Compute** (`ncu -o report.rpt ./prog`) sections `basic`, `roofline`, `detailed`. Key panels: **GPU Speed of Light** (DRAM/SM throughput), **Roofline** (achieved vs theoretical), **Memory Chart**, **Occupancy**, and **stall reasons** (e.g. *Long Scoreboard* → global-memory latency). Compute theoretical bandwidth from device props:

```cpp
float gbs = 2.0f * ((prop.memoryClockRate/1000) * prop.memoryBusWidth / 8) / 1024; // GDDR doubling
```

CMake with `-DCMAKE_BUILD_TYPE=Release`, `-O3`; debug with `cuda-gdb`.

---

## 🔗 Integration with Other Skills

- For the host language features used by kernels, see [lang-cpp](../lang-cpp/SKILL.md).
- For profiling/bottleneck methodology on the CPU side, see [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md) and [python-performance-parallelism](../../engineering/practices/python-performance-parallelism/SKILL.md).
- For HPC cluster scheduling and interconnects, see [hpc-supercomputing-clusters](../../infrastructure/hpc-supercomputing-clusters/SKILL.md).
