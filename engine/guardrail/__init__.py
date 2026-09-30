"""Guardrail package: the runtime policy evaluator (PAER).

The generator (`engine/generators/guardrails.py`) renders native hooks that call
`scripts/coacus_guard.py`; that CLI delegates here. The evaluator is harness
agnostic: it takes a canonical action and the loaded policies and returns a
canonical decision (`allow` / `deny` / `ask` / `note`).
"""
