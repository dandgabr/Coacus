---
name: framework-testing-python
description: "Acts as a Specialist in Automated Testing and QA Engineering in Python, covering the Pytest ecosystem and the native Unittest framework. Masters modular Fixtures, conftest.py, formal parameterization (BVA/Equivalence Partitioning), subTests, Property-Based Testing (Hypothesis), Mocks (unittest.mock, @patch, MagicMock, pytest-mock), Mutation Testing (mutmut), asynchronous tests (pytest-asyncio), and coverage analysis (pytest-cov)."
---

# Automated Testing in Python: Pytest & Unittest

This skill establishes the engineering standards and methodologies for developing and automating test suites in Python, integrating the advanced **Pytest** ecosystem and the object-oriented standard library **Unittest**.

---

## 🧭 1. Framework Comparison and Selection Guidelines

| Aspect | Pytest | Unittest (Standard Library) |
| :--- | :--- | :--- |
| **Style / Paradigm** | Functional with fixtures and native asserts | Object-oriented, deriving from `unittest.TestCase` |
| **Asserts** | `assert expressao` (with rich AST rewriting) | `self.assertEqual()`, `self.assertRaises()`, etc. |
| **Injection / Setup** | Scoped modular fixtures (`function`, `module`, `session`) | Static life cycle `setUp()`, `tearDown()`, `setUpClass()` |
| **Parameterization** | `@pytest.mark.parametrize` (formal and declarative) | `self.subTest()` inside loops |
| **Dependencies** | Requires `pytest` (`pip install pytest`) | Zero external dependencies (built into Python) |
| **Use Cases** | Modern applications, microservices, ML, APIs, mutation | Lightweight scripts, pure libraries without external dependencies |

---

## ⚡ 2. Pytest: Advanced Engineering Patterns

### 2.1 Formal BVA Parameterization and Decision Tables
```python
import pytest
from my_app.services import validate_withdrawal

# Domínio válido de saque: [10.0, 5000.0]
@pytest.mark.parametrize("amount, balance, is_blocked, expected_status, raises_exc", [
    # BVA: Limites da variável amount
    (9.99, 1000.0, False, None, True),          # min- (Inválido robusto)
    (10.0, 1000.0, False, "APPROVED", False),    # min
    (10.01, 1000.0, False, "APPROVED", False),   # min+
    (500.0, 1000.0, False, "APPROVED", False),   # nom
    (4999.99, 6000.0, False, "APPROVED", False), # max-
    (5000.0, 6000.0, False, "APPROVED", False),  # max
    (5000.01, 6000.0, False, None, True),        # max+ (Inválido robusto)
    # Tabela de Decisão: Condições de Saldo e Bloqueio
    (100.0, 50.0, False, "INSUFFICIENT_FUNDS", False),
    (100.0, 1000.0, True, "CARD_BLOCKED", False),
])
def test_withdrawal_bva_and_decision_rules(amount, balance, is_blocked, expected_status, raises_exc):
    if raises_exc:
        with pytest.raises(ValueError):
            validate_withdrawal(amount=amount, balance=balance, is_blocked=is_blocked)
    else:
        status = validate_withdrawal(amount=amount, balance=balance, is_blocked=is_blocked)
        assert status == expected_status
```

### 2.2 Property-Based Testing with `hypothesis`
```python
from hypothesis import given, strategies as st
from my_app.algorithms import sort_items, compress, decompress

@given(st.lists(st.integers()))
def test_sort_invariants(lst):
    result = sort_items(lst)
    assert len(result) == len(lst)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.binary())
def test_compress_roundtrip(data):
    assert decompress(compress(data)) == data
```

---

## 🏛️ 3. Unittest: Object-Oriented and Dependency-Free Patterns

### 3.1 TestCase and SubTests Structure
```python
import unittest
from my_app.services import UserRegistry, validate_discount

class TestUserRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared_resource = {"environment": "test"}

    def setUp(self):
        self.registry = UserRegistry()
        self.registry.clear()

    def tearDown(self):
        self.registry.clear()

    def test_register_user(self):
        user = self.registry.register("alice@example.com", "Alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertTrue(self.registry.exists("alice@example.com"))

    def test_discount_scenarios_subtest(self):
        test_cases = [
            ("VIP", 100.0, 80.0),
            ("REGULAR", 100.0, 95.0),
            ("ANONYMOUS", 100.0, 100.0),
        ]
        for role, price, expected in test_cases:
            with self.subTest(role=role, price=price):
                result = validate_discount(role, price)
                self.assertAlmostEqual(result, expected, places=2)
```

---

## 🎭 4. Mocks, Spies, and Side-Effect Isolation

### 4.1 Using `unittest.mock` (`@patch` and `MagicMock`)
```python
from unittest.mock import patch, MagicMock
import pytest
from my_app.gateways import PaymentProcessor

def test_payment_with_patch(mocker):
    # Usando pytest-mock ou unittest.mock nativo
    with patch("my_app.gateways.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "PAID", "tx_id": "tx-123"}
        
        processor = PaymentProcessor()
        tx = processor.charge(amount=150.0, token="card_tok_abc")
        
        mock_post.assert_called_once()
        assert tx.status == "PAID"
        assert tx.id == "tx-123"
```

---

## 🧬 5. Mutation Testing (mutmut) and Coverage (pytest-cov)

- **Mutation Score Measurement**:
  $$MS = \frac{\text{Mutantes Mortos (Killed)}}{\text{Total de Mutantes Gerados}} \times 100\%$$
- **Execution Commands**:
  ```bash
  # Cobertura com branch coverage
  pytest --cov=my_app --cov-branch --cov-report=html --cov-fail-under=90

  # Teste de mutação
  mutmut run --paths-to-mutate my_app/
  mutmut results
  ```
