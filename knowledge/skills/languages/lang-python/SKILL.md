---
name: "lang-python"
description: "Provides software engineering patterns in Python 3 based on the official documentation (docs.python.org/pt-br/3), covering the Zen of Python (PEP 20), the style guide (PEP 8), the Data Model (__dunder__), Pattern Matching (PEP 634), Advanced Typing (PEP 484/695), Asyncio, the Standard Library, and modern frameworks."
---

# AI Skill: Python Engineering (Python 3 Specialist)

This skill guides the AI to act as a specialist in the **Python 3** language, aligned strictly with the guidelines of the official language documentation ([docs.python.org/pt-br/3](https://docs.python.org/pt-br/3/)), the Language Reference, the Standard Library Reference, and the Python Enhancement Proposals (PEPs). The goal is to build idiomatic, expressive, maintainable, safe, and high-performance code.

---

## 🧭 General Guidelines and Language Fundamentals (docs.python.org)

While working under this skill, apply the official Python Software Foundation principles strictly:

### 1. Philosophy and Idiomatic Style (PEP 20, PEP 8 & PEP 257)
- **The Zen of Python (PEP 20)**:
  - *Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex.*
  - Avoid unreadable code tricks ("code golf") in favor of clarity and maintainability.
- **PEP 8 Style Guide**:
  - Naming: `snake_case` for variables, functions, and methods; `PascalCase` for classes; `ALL_CAPS` for constants.
  - Strict 4-space indentation (never mix tabs and spaces).
  - Import organization at the top of the file, split into 3 blocks: (1) Standard Library, (2) Third-Party Libraries, and (3) Local Modules.
- **Docstring Conventions (PEP 257)**:
  - Write explanatory docstrings for modules, classes, and public functions using the triple-quote convention `"""Explanatory text."""`.

### 2. Language Data Model (Data Model & Dunder Methods)
- **Special Methods (__dunder__)**: Implement the Pythonic behavior of your custom classes using the official Data Model:
  - Representation: `__str__` (for user-friendly display) and `__repr__` (for unambiguous debugging).
  - Context Managers: `__enter__` and `__exit__` (synchronous) or `__aenter__` and `__aexit__` (asynchronous with `async with`).
  - Collections and Iteration: `__len__`, `__getitem__`, `__setitem__`, `__iter__`, `__next__`.
  - Comparison and Hashing: `__eq__` and `__hash__` for objects usable as dictionary and set keys.

### 3. Structural Pattern Matching (PEP 634/635/636)
- Use the `match / case` statement (Python 3.10+) to destructure sequences, dictionaries, and class instances cleanly:

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float

def process_event(event: tuple | Point) -> str:
    match event:
        case Point(x=0, y=0):
            return "Origem central"
        case Point(x=x, y=y) if x == y:
            return f"Ponto na diagonal principal: {x}"
        case ("click", x, y):
            return f"Clique no ponteiro: ({x}, {y})"
        case ("key", str(k)) if len(k) == 1:
            return f"Tecla pressionada: {k}"
        case _:
            return "Evento desconhecido"
```

### 4. Static Typing System and Generics (PEP 484, PEP 526 & PEP 695)
- **Type Annotations (`typing`)**: Apply type hints to function signatures and core domain attributes.
- **Modern Generic Syntax (Python 3.12+ - PEP 695)**:
  - Declare generics directly with the `type` keyword and bracketed parameters:

```python
# Sintaxe PEP 695 (Python 3.12+)
type Result[T] = dict[str, T]

class Repository[T]:
    def __init__(self, initial_data: list[T]) -> None:
        self._items: list[T] = initial_data

    def get_first(self) -> T | None:
        return self._items[0] if self._items else None
```

---

## 🛠️ Standard Library Highlights (Python Standard Library)

When implementing solutions, prioritize the language's mature built-in modules before adding external dependencies:

- **Object Orientation and Data**:
  - `dataclasses`: Creating data classes with `dataclass(slots=True, frozen=True)`.
  - `enum`: Defining strongly typed enums (`Enum`, `IntEnum`, `StrEnum`).
  - `collections`: `defaultdict`, `Counter`, `deque`, `namedtuple`.
- **I/O and File System**:
  - `pathlib`: Object-oriented file path manipulation (`Path(__file__).parent`).
  - `contextlib`: Simplified context manager creation with `@contextmanager`.
  - `json`: Safe JSON serialization and parsing.
- **Asynchronous Execution and Concurrency**:
  - `asyncio`: Native event loop, coroutines (`async def`), tasks (`asyncio.create_task`), and semaphores (`asyncio.Semaphore`).
  - `concurrent.futures`: Parallel processing based on threads (`ThreadPoolExecutor`) or processes (`ProcessPoolExecutor`).
- **Operation and Debugging**:
  - `logging`: Structured logging configured per module (`logging.getLogger(__name__)`).
  - `unittest`: Native unit test suite (for compatibility without external packages).

---

## 🧰 Recommended Code Patterns

### 1. Custom Context Manager (`contextlib`)
```python
from contextlib import contextmanager
from typing import Generator
import time
import logging

logger = logging.getLogger(__name__)

@contextmanager
def execution_timer(task_name: str) -> Generator[None, None, None]:
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        logger.info(f"Tarefa '{task_name}' concluída em {elapsed:.4f}s")
```

### 2. Native Asyncio Application with Signal Handling
```python
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

async def worker_task(task_id: int, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        logger.info(f"Iniciando task {task_id}")
        await asyncio.sleep(0.5)
        logger.info(f"Concluída task {task_id}")

async fn main() -> None:
    semaphore = asyncio.Semaphore(3)
    tasks = [asyncio.create_task(worker_task(i, semaphore)) for i in range(10)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ⚙️ Modern Environment Management and Packaging (PEP 621)

- **`pyproject.toml`**: Centralize project metadata, dependencies, and tool configuration (`pytest`, `black`, `mypy`, `ruff`) in a single file per PEP 621.
- **Virtual Environments (`venv`)**: Isolate dependencies using the native module `python -m venv .venv` or modern high-performance managers such as `uv` or `poetry`.

---

## 🔒 Security Issues and Safe Practices

- **Insecure Deserialization (CWE-502)**: Never deserialize untrusted data using `pickle`, `marshal`, or `shelve`. When using PyYAML, always force the call through `yaml.safe_load()`.
- **Command and Code Injection**: Avoid using `eval()`, `exec()`, and `subprocess.Popen(..., shell=True)` with user-supplied data. Use the object-oriented API with argument lists.
- **Mutable Default Arguments**: Avoid defining lists or dictionaries as default arguments in functions (e.g., `def func(val=[])`), because they persist across calls and can cause logic bugs and data leakage.
- **Path Traversal (CWE-22)**: Use `pathlib.Path` and validate resolved path safety against base paths with `Path.resolve()` (e.g., preventing navigation to parent folders via `../`).

## 🔗 Integration with Other Skills

- To create parameterized unit and integration test suites in Python, see [framework-pytest](../../frameworks/framework-testing-python/SKILL.md) and [framework-unittest](../../frameworks/framework-testing-python/SKILL.md).
- To integrate and optimize relational and NoSQL database access in Python (SQLAlchemy, psycopg, PyMongo, Tortoise ORM), see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md), [db-postgresql](../../data/db-postgresql/SKILL.md), [db-sqlite](../../data/db-sqlite/SKILL.md), [db-mariadb](../../data/db-mariadb/SKILL.md), and [db-mongodb](../../data/db-mongodb/SKILL.md).
- To develop offensive tools, network scripts, and security utilities in Python, see [pentest-scripter-python-bash-go](../../security/appsec/pentest-scripter-python-bash-go/SKILL.md).
- To audit Python code against security flaws (SAST) and apply clean-code fixes, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md) and [clean-code-reusability](../../engineering/practices/clean-code-reusability/SKILL.md).
