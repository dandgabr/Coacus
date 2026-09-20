---
name: framework-testing-javascript
description: "Acts as a Specialist in Automated Testing and QA Engineering in the JavaScript and TypeScript ecosystem (Node.js, React, Vue, NestJS). Covers the all-in-one Jest framework and the modular Mocha architecture with Chai and Sinon.js, mastering Spies, Stubs, Mocks, BDD/TDD assertions, Snapshots, Fake Timers, asynchronous testing, and code coverage with Istanbul/c8."
---

# Automated Testing in JavaScript & TypeScript: Jest & Mocha

This skill establishes the engineering guidelines and standards for developing and automating tests in the JavaScript and TypeScript ecosystem, spanning batteries-included solutions such as **Jest** and modular compositions with **Mocha + Chai + Sinon.js**.

---

## 🧭 1. Framework Comparison and Selection Guidelines

| Characteristic | Jest | Mocha + Chai + Sinon.js |
| :--- | :--- | :--- |
| **Architecture** | "All-in-one" framework (Runner + Assertions + Mocks) | Decoupled runner with a plugin ecosystem |
| **Mocks & Spies** | Native (`jest.fn()`, `jest.spyOn()`, `jest.mock()`) | Via Sinon.js (`sinon.stub()`, `sinon.spy()`) |
| **Assertions** | Rich native matchers (`expect(val).toBe()`) | Chai library (`expect`, `should`, `assert`) |
| **Snapshot Testing** | Native support (`toMatchSnapshot()`) | Requires additional plugins |
| **Typical Environment** | React, Vue, NestJS, TypeScript, Next.js | Legacy Node.js microservices, Express, pure ESM |

---

## ⚡ 2. Jest: Native Test and Mock Patterns

### 2.1 Unit Tests and Native Matchers
```typescript
import { calculateOrderTotal } from './calculator';

describe('calculateOrderTotal', () => {
  it('deve calcular o total com desconto e frete corretamente', () => {
    const items = [{ price: 100, quantity: 2 }, { price: 50, quantity: 1 }];
    const discount = 20;
    const shipping = 15;

    const result = calculateOrderTotal(items, discount, shipping);
    expect(result).toBe(245); // (200 + 50) - 20 + 15
  });

  it('deve lançar erro para quantidade negativa', () => {
    const invalidItems = [{ price: 100, quantity: -1 }];
    expect(() => calculateOrderTotal(invalidItems, 0, 0)).toThrow('Quantidade inválida');
  });
});
```

### 2.2 Module and Asynchronous Function Mocks
```typescript
import { UserService } from './user.service';
import { UserRepository } from './user.repository';

jest.mock('./user.repository');

describe('UserService', () => {
  let userService: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    jest.clearAllMocks();
    mockRepo = new UserRepository() as jest.Mocked<UserRepository>;
    userService = new UserService(mockRepo);
  });

  it('deve retornar usuário quando encontrado no repositório', async () => {
    mockRepo.findById.mockResolvedValue({ id: 'u1', name: 'Alice' });
    const user = await userService.getUser('u1');
    
    expect(mockRepo.findById).toHaveBeenCalledWith('u1');
    expect(user.name).toBe('Alice');
  });
});
```

---

## ☕ 3. Mocha + Chai + Sinon.js: Modular Architecture

### 3.1 BDD Testing with Chai and a Sinon.js Sandbox
```javascript
const { expect } = require('chai');
const sinon = require('sinon');
const { PaymentService } = require('../src/payment.service');
const { PaymentGateway } = require('../src/payment.gateway');

describe('PaymentService (Mocha + Chai + Sinon)', () => {
  let sandbox;
  let paymentService;
  let gatewayMock;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    gatewayMock = new PaymentGateway();
    paymentService = new PaymentService(gatewayMock);
  });

  afterEach(() => {
    sandbox.restore(); // Restaura todos os stubs e spies
  });

  it('deve processar o pagamento e registrar transação', async () => {
    const stub = sandbox.stub(gatewayMock, 'charge').resolves({ status: 'SUCCESS', id: 'tx-999' });

    const result = await paymentService.processPayment({ amount: 100 });
    
    expect(stub.calledOnce).to.be.true;
    expect(result.status).to.equal('SUCCESS');
    expect(result.id).to.equal('tx-999');
  });
});
```

---

## 🧪 4. Fake Timers and Asynchronous Tests

### 4.1 Jest Fake Timers
```typescript
jest.useFakeTimers();

it('deve executar callback após debounce de 300ms', () => {
  const callback = jest.fn();
  const debounced = debounce(callback, 300);

  debounced();
  expect(callback).not.toHaveBeenCalled();

  jest.advanceTimersByTime(300);
  expect(callback).toHaveBeenCalledTimes(1);
});
```
