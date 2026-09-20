# Code Reuse Examples in Python

Dispatcher pattern for extensions without modifying the core:

```python
from pathlib import Path
from typing import Callable, Dict

Handler = Callable[[Path, Path], str]

CONVERTERS: Dict[str, Handler] = {}

def register_converter(extension: str):
    """Decorator para registrar dinamicamente novos conversores de documento."""
    def decorator(fn: Handler):
        CONVERTERS[extension.lower()] = fn
        return fn
    return decorator

@register_converter('.txt')
def handle_txt(src: Path, dst: Path) -> str:
    content = src.read_text(encoding='utf-8')
    dst.write_text(f"# {src.stem}\n\n{content}", encoding='utf-8')
    return str(dst)
```
