---
name: "vector-databases"
description: "Provides expert patterns for vector databases and similarity search based on Vector Databases: A Practical Introduction (Nitin Borwankar), covering embeddings and distance metrics, ANN indexing algorithms (flat, IVF, HNSW, PQ, SQ, LSH), metadata filtering and hybrid vector+keyword search, pgvector and sqlite-vss/FAISS integration, chunking and data modeling, RAG retrieval pipelines, evaluation metrics and cost/performance trade-offs."
---

# AI Skill: Vector Databases and Similarity Search

This skill guides the AI to act as a specialist in **vector databases** and **semantic similarity search**, building on *Vector Databases: A Practical Introduction* (Nitin Borwankar). The vector type's value is not storage — it is the **similarity-search operator** over dense embeddings, complementing (never replacing) exact-match and keyword search.

Resolve current library/extension versions (FAISS, pgvector, Qdrant, Milvus, Weaviate) from their publishers before pinning them; the algorithms below are stable.

---

## 🧭 When to Activate

- Building semantic search, RAG retrieval, recommendation or image/audio similarity.
- Choosing or tuning an ANN index and its recall/latency/memory trade-off.
- Designing hybrid retrieval that combines embeddings with BM25 or metadata filters.
- Modeling vector schemas in PostgreSQL (pgvector) or SQLite (sqlite-vss).
- Diagnosing "the search misses exact terms" or "filtering is slow/incorrect".

---

## 📐 Embeddings and Distance Metrics

An embedding is an ordered list of floats (e.g. 384 or 768 dimensions). Modern systems combine **sparse** representations (one-hot, TF-IDF — interpretable, memory-heavy, weak semantics) with **dense** embeddings (semantic, support vector arithmetic such as `Vec("King") − Vec("Man") + Vec("Woman") ≈ Vec("Queen")`).

Reference sentence-transformers models: `all-MiniLM-L6-v2` (384 dims, fast), `all-mpnet-base-v2` (768 dims, higher accuracy), `paraphrase-multilingual-mpnet-base-v2` (50+ languages). Best practices: **batch** encode, **chunk** long text, **normalize** (`normalize_embeddings=True`) so that cosine equals inner product, pin the device, and reuse a singleton model.

Metrics:

- **L2 / Euclidean** — magnitude-sensitive; use squared L2 inside least-squares objectives.
- **Inner product** — alignment plus magnitude; on unit vectors equals cosine.
- **Cosine** — direction only; the standard for NLP because it removes the "longer text wins" bias.

Rule of thumb: L2 when magnitude matters, inner product when both matter, cosine when only direction matters.

---

## 🗂️ ANN Indexing Algorithms

- **Flat / brute force** (`IndexFlatL2`, `IndexFlatIP`) — exact, O(n) scan, `4·d` bytes/vector; small datasets only.
- **IVF (inverted file)** — k-means partitions space into `nlist` Voronoi cells; queries probe the `nprobe` nearest cells. Requires **training**. Classes: `IndexIVFFlat`, `IndexIVFPQ`, `IndexIVFScalarQuantizer`. `nprobe` trades accuracy for speed.
- **HNSW** — a multi-layer proximity graph ("highways → local streets"); SOTA speed/recall at high dimensions. Parameters: **M** (graph degree), **efConstruction** (build quality), **efSearch** (query breadth). Higher M raises recall and RAM.
- **PQ (product quantization)** — split a D-dim vector into `m` subvectors, learn a `k`-centroid codebook per subspace, encode each as an integer index; search uses a lookup table and **asymmetric distance computation (ADC)**. Massive compression for millions–billions of vectors.
- **SQ (scalar quantization)** — quantize each dimension independently (`QT_8bit`, `QT_4bit`, `QT_fp16`, …).
- **LSH** — random projections into buckets; parameter-sensitive and generally less accurate than IVF/HNSW.
- **Composite** — `IndexPreTransform` (PCA, normalization), `IndexIDMap`, `IndexRefineFlat`, `IndexShards`.

ANN accepts a candidate within `(1+ε)` of the true nearest neighbor — ε is the tolerance that beats the **curse of dimensionality**.

```python
# FAISS HNSW
index = faiss.IndexHNSWFlat(dimension, M=16)
index.hnsw.efConstruction = 40
index.hnsw.efSearch = 16
index.add(vectors.astype('float32'))
distances, indices = index.search(query, k)

# FAISS IVF (requires training)
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFFlat(quantizer, d, nlist)
index.train(X); index.add(X); index.nprobe = 10
```

---

## 🔎 Filtering and Hybrid Search

FAISS search does **not** push metadata filters down. Use **overfetch-then-filter**: fetch `limit × 2` or more candidates, then filter and rank in SQL. This guards against disjoint semantic/keyword result sets.

Hybrid scoring fuses **normalized** scores, defaulting to **0.7 semantic + 0.3 keyword (BM25)**:

```text
final_score = w_vector · norm(vector_score) + w_text · norm(text_score)
```

Normalize the keyword scores (divide by the max) before combining. In pgvector, cosine distance is `<=>`; similarity is `1 - distance` (0–2 range), so threshold e.g. `> 0.7` for precision. Range search returns everything within a threshold; top-K returns a fixed count.

---

## 🐘 pgvector and sqlite-vss

**pgvector** integrates into the PostgreSQL planner — a single source of truth with ACID, constraints, backups and access control, practical to roughly one million documents:

```sql
CREATE EXTENSION vector;
CREATE TABLE paper_chunks (
  id SERIAL PRIMARY KEY,
  paper_id INTEGER REFERENCES papers(id) ON DELETE CASCADE,
  chunk_text TEXT NOT NULL,
  embedding vector(384),
  UNIQUE (paper_id, chunk_index)
);
CREATE INDEX idx_chunks_embedding ON paper_chunks
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

SELECT paper_id, 1 - (abstract_embedding <=> $1::vector) AS similarity
FROM papers
WHERE 1 - (abstract_embedding <=> $1::vector) > 0.7
ORDER BY similarity DESC LIMIT 3;
```

**sqlite-vss** wraps FAISS as a `vss0` virtual table with factory strings (`"Flat"`, `"IVF100,Flat"`, `"HNSW16"`). **Critical:** use `INSERT ... ON CONFLICT DO UPDATE` (UPSERT); `INSERT OR REPLACE` reassigns `rowid` and breaks the VSS index mapping.

---

## 🧩 Data Modeling, Chunking and Evaluation

- **Chunking**: 512–1,024 tokens (~1–3 paragraphs) with a **sliding window and ~20% overlap**, preferring sentence boundaries. Store `chunk_index`, `section_name`, `page_number`, `char_start/end`.
- **Record the generating model** per row: switching embedding models invalidates stored vectors.
- **Evaluation**: retrieval recall ("does it find the document you know exists"), context relevance and faithfulness; RAGAS and LLM-as-a-Judge for end-to-end quality; IR precision/recall/F1 for retrieval.
- **RAG flow**: ingest → chunk → embed → store → hybrid retrieve → assemble context → prompt → LLM; extend with cross-encoder reranking, query decomposition and citation parsing.

---

## ⚖️ Cost/Performance Ladder and Pitfalls

flat (exact, cheap to build, O(n), RAM-heavy) → IVF/SQ (training, fast) → PQ (compressed, approximate) → HNSW (fastest, RAM-heavy). Tune `nprobe`, `M`, `efConstruction`, `efSearch`; batch queries; monitor memory during build; shard at billions of objects (`IndexShards`) or switch to a dedicated vector database (Milvus, Qdrant, Weaviate, Pinecone).

**Pitfalls:** assuming pure vector search suffices (exact technical terms get blurred — always add keyword or metadata filtering); no push-down filtering; changing embedding models without re-embedding; `REPLACE` breaking the FAISS `rowid` mapping.

---

## 🔗 Integration with Other Skills

- For the PostgreSQL engine and index internals, see [db-postgresql](../db-postgresql/SKILL.md).
- For RAG pipeline engineering, agent patterns and evaluation, see [ai-llm-engineering-rag](../../domains/industry/ai-llm-engineering-rag/SKILL.md).
- For storage engines, replication and scaling, see [data-intensive-systems](../data-intensive-systems/SKILL.md).
