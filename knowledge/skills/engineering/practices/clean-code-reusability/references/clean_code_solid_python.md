# SOLID & Clean Code in Python

Practical guidelines for clean, sustainable Python code.

- **Single Responsibility (SRP)**: Each module should have a single reason to change (e.g., conversion in `document_converter.py`, analysis in `document_analyzer.py`).
- **Open/Closed (OCP)**: Format extensions should be added by writing new handler functions without modifying the central logic.
- **Dependency Inversion (DIP)**: Use abstractions and `typing.Protocol` to decouple components.
- **Exception Handling**: Avoid silent generic catches (`except: pass`); always log or propagate errors with context.
