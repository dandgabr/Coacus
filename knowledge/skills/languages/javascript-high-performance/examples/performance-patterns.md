# Examples of Performance Patterns in JavaScript

Practical patterns extracted from the book *Hands-On JavaScript High Performance* (Justin Scherer). Code in English, explanations in pt-BR. Each example shows the anti-pattern ❌ and the optimized version ✅.

---

## 1. Debounce and Throttle (avoid redundant work)

High-frequency events (`input`, `scroll`, `resize`) fire handlers dozens of times per second. **Debounce** runs only after the pause; **throttle** runs at most once per time window.

```javascript
// ❌ Anti-pattern: handler pesado executado a cada tecla/frame
searchInput.addEventListener('input', (e) => runExpensiveSearch(e.target.value));
window.addEventListener('resize', relayoutEverything);

// ✅ Debounce: só executa quando o usuário para de digitar
function debounce(fn, delay) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// ✅ Throttle: no máximo uma execução por intervalo
function throttle(fn, interval) {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn(...args);
    }
  };
}

searchInput.addEventListener('input', debounce((e) => runExpensiveSearch(e.target.value), 250));
window.addEventListener('resize', throttle(relayoutEverything, 100));
```

**Why it matters**: every execution avoided is less GC pressure and less scripting time on the main thread (visible in the Chrome DevTools Performance tab).

---

## 2. Native Loops vs. Array Methods on Hot Paths

The book compares with jsPerf: on large data, chains of functional methods allocate intermediate arrays at every step. The book's benchmarks (ch. 1) show the `for` loop beating `filter` when the code runs at a very high frequency.

```javascript
// ❌ Anti-pattern: 2 arrays intermediários + iterações múltiplas
const positives = data.filter((x) => x > 0);
const doubled = positives.map((x) => x * 2);
let total = 0;
for (const x of doubled) total += x;

// ✅ Otimizado: um único loop, sem alocações intermediárias
let total = 0;
const result = new Array(data.length);
let count = 0;
for (let i = 0; i < data.length; i++) {
  const x = data[i];
  if (x > 0) {
    result[count++] = x * 2;
    total += x * 2;
  }
}
result.length = count;
```

**Rule**: use `map/filter/reduce` for readability in cold code (runs few times); use native loops on hot paths (parsing, data transformation, rendering large lists).

---

## 3. Memoization and Cache with TTL/LRU

The book builds caches in workers (ch. 10) and in the static server (ch. 9), always remembering: an "infinite cache" leaks memory — bound it by TTL (Time To Live) or LRU (Least Recently Used).

```javascript
// ✅ Memoization com cache limitado por TTL
const cache = new Map(); // key -> { value, ts }
const TTL = 5 * 60 * 1000;
const MAX_ENTRIES = 1000;

function memoize(key, compute) {
  const hit = cache.get(key);
  if (hit && Date.now() - hit.ts <= TTL) {
    return hit.value; // cache hit: zero custo de processamento
  }
  const value = compute(key);
  // evict least-recently-used quando cheio (Map preserva ordem de inserção)
  if (cache.size >= MAX_ENTRIES) {
    const oldest = cache.keys().next().value;
    cache.delete(oldest);
  }
  cache.set(key, { value, ts: Date.now() });
  return value;
}

function getCustomerAttribution(customerId) {
  return memoize(`cust:${customerId}`, (id) => fetchAndDecorate(id));
}
```

**Classic mistake from the book**: "currently, we infinitely increase our cache" — always add a TTL or an LRU eviction to growing caches.

---

## 4. Web Worker Offloading with Transferrables (zero-copy)

Moving gigantic objects via `postMessage` uses **structured clone** (serialize + copy): the book measured 100,000 objects at 800 ms–1.7 s and 80–100 MB of heap.

```javascript
// main.js
const worker = new Worker('heavy.js');

// ❌ Anti-pattern: structured clone de milhares de objetos
// worker.postMessage(dataToSend); // cópia completa + GC pressure

// ✅ Otimizado: TypedArray + transferrable (zero cópia)
const view = new Int32Array(1_000_000);
for (let i = 0; i < view.length; i++) view[i] = i + 1;
worker.postMessage(view, [view.buffer]); // transfere o ArrayBuffer
// ⚠️ view agora está detached — remetente não pode mais acessar

worker.onmessage = (ev) => {
  console.log('result length', ev.data.byteLength);
};
```

```javascript
// heavy.js
self.onmessage = (ev) => {
  const data = ev.data; // recebe instantaneamente, sem cópia
  let sum = 0;
  for (let i = 0; i < data.length; i++) sum += data[i];
  // para devolver, também transfira (novamente zero-copy):
  const result = new Int32Array(1);
  result[0] = sum;
  self.postMessage(result, [result.buffer]);
};
```

**Rule**: large binary data → transferrables; small structured data → normal `postMessage`; true shared memory → `SharedArrayBuffer` + `Atomics`.

---

## 5. Avoiding Layout Thrashing (forced synchronous layout)

Interleaving reads and writes of layout properties forces the browser to recompute layout at every iteration (synchronous reflow). It shows up as yellow/purple spikes in the Performance tab.

```javascript
// ❌ Anti-pattern: read-write intercalado = reflow a cada iteração
const rows = document.querySelectorAll('.row');
for (const row of rows) {
  const h = row.offsetHeight;    // READ (invalida layout)
  row.style.height = h * 2 + 'px'; // WRITE (invalida de novo)
}

// ✅ Otimizado: batch de leituras, depois batch de escritas
const rows = document.querySelectorAll('.row');
const heights = Array.from(rows, (row) => row.offsetHeight); // READ phase
rows.forEach((row, i) => {
  row.style.height = heights[i] * 2 + 'px'; // WRITE phase
});
```

A variant with `requestAnimationFrame` for insertions that change layout within a frame:

```javascript
function addRows(container, items) {
  const frag = document.createDocumentFragment();
  for (const item of items) {
    const row = document.createElement('div');
    row.textContent = item.label;
    frag.appendChild(row);
  }
  requestAnimationFrame(() => {
    container.appendChild(frag); // um único layout/paint
  });
}
```

**Rule**: separate reads from writes; use `DocumentFragment` for batch insertions and monitor with Paint flashing (Rendering tab).

---

## 6. Streaming Large Data (Node.js / browser)

Do not load entire files or payloads into memory — process them in chunks with streams (ch. 7) or compact binary formats (ch. 8).

```javascript
// ❌ Anti-pattern: arquivo inteiro na memória (OOM em arquivos grandes)
const content = fs.readFileSync('big.log', 'utf8');
const lines = content.split('\n').filter((l) => includesError(l));
fs.writeFileSync('errors.log', lines.join('\n'));

// ✅ Otimizado: pipeline de streams, memória constante
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { Transform } from 'node:stream';

const errorFilter = new Transform({
  transform(chunk, enc, cb) {
    const kept = chunk
      .toString()
      .split('\n')
      .filter((l) => l.includes('ERROR'))
      .join('\n');
    cb(null, kept + '\n');
  },
});

await pipeline(
  createReadStream('big.log'),
  errorFilter,
  createWriteStream('errors.log'),
);
```

**Why it matters**: constant memory regardless of file size, a free event loop (non-blocking I/O), and automatic backpressure via `highWaterMark`.
