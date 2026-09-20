---
name: hpc-supercomputing-clusters
description: Provides architecture, engineering, and operations patterns for HPC (High Performance Computing) clusters and supercomputers based on Supercomputers for Linux SysAdmins (Sergey Zhumatiy). Covers workload managers (Slurm Workload Manager), low-latency interconnects (InfiniBand/RDMA), parallelism libraries (OpenMPI, MPICH), parallel file systems (Lustre, GPFS, Ceph), and GPU-accelerated computing.
---

# HPC Clusters and Supercomputer Engineering

This skill establishes the guidelines for designing, deploying, and operating **High Performance Computing (HPC)** environments and supercomputers on Linux, drawing on the book by **Sergey Zhumatiy**.

---

## 🚀 1. Topology of an HPC Cluster

```
                       ┌─────────────────────────┐
                       │  Nó Mestre / Head Node  │
                       │   (Slurm Controller)    │
                       └────────────┬────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
   [ Rede de Gerenciamento 10GbE ]           [ Rede InfiniBand / RDMA 200Gbps ]
           │                                                 │
 ┌─────────▼─────────┐                             ┌─────────▼─────────┐
 │ Storage Paralelo  │                             │  Nós de Computo   │
 │ (Lustre / CephFS) │                             │ (CPUs + GPUs H100)│
 └───────────────────┘                             └───────────────────┘
```

---

## 📋 2. Job Management with Slurm Workload Manager

### Batch Job Script Example (`submit_job.sh`)
```bash
#!/bin/bash
#SBATCH --job-name=scientific_sim
#SBATCH --output=logs/sim_%j.log
#SBATCH --error=logs/sim_%j.err
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:4
#SBATCH --time=12:00:00
#SBATCH --partition=gpu_cluster

module load openmpi/4.1.5-cuda-12.2

srun --mpi=pmix ./bin/simulation_engine --dataset /shared/lustre/input.dat
```
