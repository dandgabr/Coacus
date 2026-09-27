---
name: "distributed-ml-scaling"
description: "Provides expert patterns for scaling data processing and machine learning across machines using Dask and Apache Spark based on Scaling Python with Dask (Karau & Kimmins) and Scaling Machine Learning with Spark (Polak). Covers Dask collections and schedulers, task graphs and lazy execution, Dask-ML, Spark architecture and DataFrames, the MLlib/ML pipeline API, distributed deep-learning bridges (Petastorm, Horovod, TensorFlow/PyTorch strategies), data vs model parallelism, deployment and drift monitoring."
---

# AI Skill: Distributed Data and ML Scaling (Dask & Spark)

This skill guides the AI to scale analytics and machine learning beyond a single machine, and — first — to decide **whether** to scale at all. It builds on *Scaling Python with Dask* (Karau & Kimmins) and *Scaling Machine Learning with Spark* (Polak).

Resolve current release versions of Dask, Spark, Petastorm, Horovod and the framework strategies from their publishers before pinning them.

---

## 🧭 When to Activate

- Data no longer fits in memory, or jobs are too slow on one machine.
- Choosing between pandas/NumPy, Dask, Spark, Ray, or a bigger single node.
- Building a distributed feature-engineering + training pipeline.
- Wiring distributed deep learning (Horovod, `spark-tensorflow-distributor`, `TorchDistributor`).
- Serving batch or streaming predictions and monitoring for drift.

---

## 🧮 Decide First

| Situation | Choice |
|---|---|
| Data + model fit one machine, fast enough | pandas/NumPy/scikit-learn (+Numba) — **do not distribute** |
| Heavy single-node tabular (≤ ~100 GB) not fitting RAM | Polars / H2O DataTable (lazy, single machine) |
| Python-native ETL + ML, pandas/scikit-learn APIs, S3/Parquet | **Dask** (Ray backend optional) |
| Stateful actors, RL, heavy mutable distributed state | **Ray** |
| JVM/Hadoop scale, SQL + MLlib pipelines, largest connector ecosystem | **Spark** |
| Deep-learning training across GPUs | Horovod / spark-tensorflow-distributor / TorchDistributor, or native TF/PyTorch strategies (Spark for the data layer) |

Distinguish **memory-bound** (data doesn't fit → more machines) from **compute-bound** (needs parallelism). GPUs help only vectorized compute-bound work.

---

## 🐍 Dask

Dask exposes NumPy/pandas/scikit-learn-compatible APIs mapped onto a **task graph** executed by a scheduler. Nothing runs until `.compute()`/`.persist()`/`.visualize()`.

- **Collections:** `dask.dataframe` (partitioned pandas; best on Parquet/S3), `dask.array` (subset of `ndarray`, same dtype only), `dask.bag` (messy/unstructured; weak at reductions).
```python
df = dd.read_parquet('./data/*.parquet', split_row_groups=2)
df.describe(percentiles=[.25,.5,.75]).compute()
```
- **Graph discipline:** scheduler overhead is ~1 ms/task — coarser tasks often win. Large or recursive graphs blow up the scheduler; reduce parallelism or checkpoint intermediate state. Batch `dask.compute` calls so graphs fuse.
- **Persist** keeps collections on the cluster (release explicitly via `futures_of(...).release()`); the **client is not fault tolerant** — run it near the scheduler.
- **Schedulers:** `threads` (GIL-releasing native code), `processes` (bypass GIL, serialization cost; use `forkserver` on Unix), and `dask.distributed` (LocalCluster, Kubernetes, YARN, HPC, `dask-on-ray`) with a diagnostics dashboard.
- **`dask.delayed`** wraps arbitrary Python; **futures** for eager side effects; **actors** for per-worker mutable state.
- **Dask-ML:** partition-aware `train_test_split`, `HyperbandSearchCV`, the `joblib` backend for `GridSearchCV`, and distributed XGBoost (`xgb.dask.DaskDMatrix`/`xgb.dask.train`). Inference is near-embarrassingly parallel; training needs weight sync and is less mature. `dask-cuda`/`LocalCUDACluster` for GPUs.
- **Do not use Dask** when data fits one machine, for stateful mutable shared state, or for deep-learning training with heavy synchronous weight exchange.

---

## ⚡ Apache Spark

Architecture: **driver** (`SparkContext`, DAG) → cluster manager (standalone/YARN/K8s) → **executors** running **tasks** on partitions. RDD (untyped) < DataFrame (Catalyst optimizer) < Dataset (typed, perf cost). PySpark crosses Python↔JVM via **Py4J**, so it is slower than Scala; prefer DataFrame/Dataset over RDD.

- **ML API:** `spark.ml` (DataFrame-based; use it, not the legacy RDD-based `spark.mllib`). **Transformers** implement `.transform()`; **estimators** implement `.fit()` and return a model.
```python
from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[tokenizer, hasher, selector, model])
cv = CrossValidator(estimator=pipeline, estimatorParamMaps=grid,
                    evaluator=evaluator, numFolds=3)
cv_model.write().save(path)          # persist; reload with CrossValidatorModel.load(path)
```
- **Data typing:** define `StructType`/`StructField` explicitly; Persist via `.write().save()`; avoid the **small-files problem** by writing typed columnar formats (Parquet/Avro). MLlib vectors are a Spark-specific sparse type — a frequent mismatch when bridging to TF/PyTorch.
- Spark assumes **monoid-style partial training** (associative, splittable); deep learning violates that, hence the **two-clusters approach**: Spark does ETL → Parquet → a dedicated DL cluster trains.

**Distributed deep learning bridge:** a distributed, columnar, row-filterable, versioned **Data Access Layer** with a catalog; **Petastorm** reads/writes Parquet for TensorFlow/PyTorch with sharding and row/field filtering:
```python
from petastorm.spark import SparkDatasetConverter
spark.conf.set(SparkDatasetConverter.PARENT_CACHE_DIR_URL_CONF, cache_path)
converter = make_spark_converter(df_train, parquet_row_group_size_bytes=32000000)
```
**Horovod's Estimator API** glues Spark DataFrames to TF/Keras/PyTorch training.

- **TensorFlow strategies** (`tf.distribute.Strategy`): `MirroredStrategy` (one machine, replicated), `MultiWorkerMirroredStrategy` (multi-machine synchronous all-reduce — standard data parallelism), `ParameterServerStrategy` (async PS; good for sparse lookups, can bottleneck), `CentralStorageStrategy`, `TPUStrategy`.
- **PyTorch:** `DistributedDataParallel` (gradient bucketing + all-reduce), `torch.distributed.rpc` (parameter-server/model/pipeline parallelism, distributed autograd), and the `c10d` collective backend (`init_process_group(backend='nccl'|'gloo'|'mpi')`). Always set a seed; watch stragglers.
- **Data vs model parallelism:** data replication across nodes is simpler; splitting a model across machines fits DAGs but is hard (GPT-3 scale). Combining both is very hard.

**Deployment:** batch prediction, model-in-service, model-as-a-service; MLflow for lifecycle; Structured Streaming for continuous scoring. **Monitor** data drift, concept drift, and domain shift with rule-based checks, **D1**, **Kolmogorov–Smirnov** and **KL divergence** against the training/validation reference distribution.

---

## ⚖️ Pitfalls

- Distributing work that fits one machine adds serialization and scheduler overhead for no gain.
- Dask's client is a single point of failure; Spark's driver is a single point of failure.
- Version skew across workers (Dask) or mismatched MLlib/TF tensor types (Spark) cause silent wrong results.
- `bag.reduce` collapses to one partition — avoid reductions on Bags.
- Dask does not manage GPU resources; misbehaving code can over-allocate.

---

## 🔗 Integration with Other Skills

- For the single-machine data-science workflow, see [python-data-science](../python-data-science/SKILL.md).
- For streaming and event-driven architectures, see [realtime-streaming-event-driven](../realtime-streaming-event-driven/SKILL.md).
- For pipeline/Mesh governance, see [data-mesh-governance](../data-mesh-governance/SKILL.md).
- For GPU kernel-level detail, see [gpu-programming-cuda](../../languages/gpu-programming-cuda/SKILL.md).
