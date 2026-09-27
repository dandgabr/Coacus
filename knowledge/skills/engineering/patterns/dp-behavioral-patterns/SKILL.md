---
name: dp-behavioral-patterns
description: "Acts as a specialist in GoF Behavioral Design Patterns, based on Design Patterns (Gang of Four) and Refactoring to Patterns. Covers Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor, organizing algorithms, control flows, and delegation of responsibilities between objects."
---

# Behavioral Design Patterns (GoF Behavioral Patterns)

Behavioral patterns deal with algorithms and the assignment of responsibilities between objects. They describe not only patterns of objects or classes but also the patterns of communication between them, decoupling the sender of a request from its receiver.

---

## ⛓️ 1. Chain of Responsibility
Lets requests pass along a chain of handlers. On receiving a request, each handler decides whether to process it or pass it to the next handler in the chain (for example, HTTP middleware pipelines or authentication filters).

```mermaid
classDiagram
    class Handler {
        <<interface>>
        +setNext(h: Handler) Handler
        +handle(request)
    }
    class BaseHandler {
        -next: Handler
        +setNext(h: Handler) Handler
        +handle(request)
    }
    class AuthHandler {
        +handle(request)
    }
    class RateLimitHandler {
        +handle(request)
    }
    Handler <|.. BaseHandler
    BaseHandler <|-- AuthHandler
    BaseHandler <|-- RateLimitHandler
```

---

## 🕹️ 2. Command
Turns a request into a standalone object that carries all information about the request. This transformation lets you parameterize methods with different requests, queue operations, keep a history, and support *Undo/Redo* operations.

```mermaid
classDiagram
    class Command {
        <<interface>>
        +execute()
        +undo()
    }
    class ConcreteCommand {
        -receiver: Receiver
        -params
        +execute()
        +undo()
    }
    class Invoker {
        -command: Command
        +setCommand(c: Command)
        +executeCommand()
    }
    class Receiver {
        +action()
    }
    Command <|.. ConcreteCommand
    Invoker o-- Command
    ConcreteCommand o-- Receiver
```

---

## 🔁 3. Iterator
Traverses the elements of an aggregate collection (list, tree, graph) without exposing its underlying representation or internal data structure.

```mermaid
classDiagram
    class Iterator {
        <<interface>>
        +hasNext() bool
        +next() Object
    }
    class Aggregate {
        <<interface>>
        +createIterator() Iterator
    }
    class ConcreteIterator {
        -collection
        -cursor
        +hasNext() bool
        +next() Object
    }
    Iterator <|.. ConcreteIterator
```

---

## 🎛️ 4. Mediator
Reduces chaotic dependencies between communicating objects. The pattern restricts direct communication between objects and forces them to collaborate only through a central mediator object (for example, UI form components or an event broker in microservices).

```mermaid
classDiagram
    class Mediator {
        <<interface>>
        +notify(sender, event)
    }
    class DialogMediator {
        -button: Button
        -textBox: TextBox
        +notify(sender, event)
    }
    class Component {
        -mediator: Mediator
        +setMediator(m: Mediator)
    }
    Mediator <|.. DialogMediator
    Component <|-- Button
    Component <|-- TextBox
    DialogMediator o-- Button
    DialogMediator o-- TextBox
```

---

## 💾 5. Memento (Snapshot)
Captures and saves an object's internal state without violating encapsulation, so the object can later be restored to that state.

```mermaid
classDiagram
    class Originator {
        -state
        +save(): Memento
        +restore(m: Memento)
    }
    class Memento {
        -state
        +getState()
    }
    class Caretaker {
        -history: List~Memento~
        +backup()
        +undo()
    }
    Originator ..> Memento : gera/restaura
    Caretaker o-- Memento : armazena
```

---

## 📡 6. Observer (Pub-Sub)
Defines a subscription mechanism to notify multiple observer objects about any events or state changes that occur in the subject object they are observing.

```mermaid
classDiagram
    class Subject {
        -observers: List~Observer~
        +subscribe(o: Observer)
        +unsubscribe(o: Observer)
        +notify()
    }
    class Observer {
        <<interface>>
        +update(context)
    }
    class ConcreteObserverA {
        +update(context)
    }
    Subject o-- Observer
    Observer <|.. ConcreteObserverA
```

---

## 🔄 7. State
Lets an object change its behavior when its internal state changes. The object will appear to change class, replacing giant conditionals (`if/switch`) with polymorphic state classes.

```mermaid
classDiagram
    class Context {
        -state: State
        +changeState(s: State)
        +request()
    }
    class State {
        <<interface>>
        +handle(ctx: Context)
    }
    class DraftState {
        +handle(ctx: Context)
    }
    class PublishedState {
        +handle(ctx: Context)
    }
    Context o-- State
    State <|.. DraftState
    State <|.. PublishedState
```

---

## 🎯 8. Strategy
Defines a family of interchangeable algorithms, encapsulates each one in a separate class, and makes the objects interchangeable at runtime (for example, different payment methods, compression strategies, or routing algorithms).

```mermaid
classDiagram
    class Context {
        -strategy: Strategy
        +setStrategy(s: Strategy)
        +executeStrategy()
    }
    class Strategy {
        <<interface>>
        +execute(data)
    }
    class ConcreteStrategyA {
        +execute(data)
    }
    class ConcreteStrategyB {
        +execute(data)
    }
    Context o-- Strategy
    Strategy <|.. ConcreteStrategyA
    Strategy <|.. ConcreteStrategyB
```

---

## 📐 9. Template Method
Defines the skeleton of an algorithm in a superclass, but lets subclasses override specific steps of the algorithm without changing its overall structure (Inversion of Control / the Hollywood Principle: *"Don't call us, we'll call you"*).

```mermaid
classDiagram
    class AbstractClass {
        +templateMethod()
        #step1()*
        #step2()
        #step3()*
    }
    class ConcreteClassA {
        #step1()
        #step3()
    }
    class ConcreteClassB {
        #step1()
        #step3()
    }
    AbstractClass <|-- ConcreteClassA
    AbstractClass <|-- ConcreteClassB
```

---

## 🚶 10. Visitor
Separates algorithms from the objects they operate on (Double Dispatch), allowing new operations to be added to complex object structures (such as AST syntax trees) without modifying those objects' classes.

```mermaid
classDiagram
    class Element {
        <<interface>>
        +accept(v: Visitor)
    }
    class ConcreteElementA {
        +accept(v: Visitor)
    }
    class Visitor {
        <<interface>>
        +visitElementA(e: ConcreteElementA)
        +visitElementB(e: ConcreteElementB)
    }
    class ConcreteVisitor {
        +visitElementA(e: ConcreteElementA)
        +visitElementB(e: ConcreteElementB)
    }
    Element <|.. ConcreteElementA
    Visitor <|.. ConcreteVisitor
    ConcreteElementA ..> Visitor : e.accept(v) -> v.visitElementA(this)
```

---

## 🅨 11. C++ Behavioral Idioms (Pikus)

- **Policy-Based Design** — Strategy reborn as a *type*: policies are classes with template members, static functions or constant-value classes, composed by **composition (preferred)** or private inheritance (empty-base optimization). Policies may be rebindable (`using value_type = T;`) and constrained with concepts to *disable* (never add) interface members. Drawbacks: long positional policy lists and code bloat.
- **NVI (Non-Virtual Interface) as Template Method**: a public non-virtual method calls a private virtual. Pitfalls are the fragile base class and composability limits; **never apply NVI to destructors**.
- **Visitors in modern C++**: keep the double-dispatch skeleton (`virtual void accept(PetVisitor&)` + `virtual void visit(Cat*)`) and extend it with **Acyclic Visitor** (break the visitor/visitable cycle via cross-casting), generic/lambda visitors, compile-time visitors, and recursive visits that map onto serialization.
- **ScopeGuard**: `MakeGuard` plus a `commit()` relies on lifetime extension of a temporary bound to a `const` reference (hence `commit()` is `const` and `commit_` is `mutable`); variants are generic, exception-driven, and type-erased.
- **Concurrency patterns**: "no sharing is best"; waiting via `condition_variable::wait` and `std::atomic_flag::wait`; a lock-free **publishing protocol** with `memory_order_acquire`/`release`; the **Active Object** (a `std::thread` is itself a type-erased active object wrapping a `Job`/`std::function<void()>`), plus **Reactor**, **Proactor** and **Monitor**.
- **Iterator** is the standard library's home turf — prefer ranges and adaptors (`views::filter`/`transform`) over hand-written iterators; **Observer** maps onto callback/`std::function` registries, mindful of lifetime and reentrancy.

## ⚖️ Comparative Matrix of Behavioral Patterns

| Pattern | Primary Focus | Mechanism |
| :--- | :--- | :--- |
| **Chain of Responsibility** | Sequential request processing | Recursive pointer passing to the next handler |
| **Command** | Encapsulation of a request as an object | Object with `execute()` and `undo()` methods |
| **Iterator** | Sequential traversal of collections | Cursor object with `hasNext()` and `next()` |
| **Mediator** | Centralization of many-to-many communication | Mediator hub decoupling communicating nodes |
| **Memento** | Restoration of state snapshots | Opaque state object for the Caretaker |
| **Observer** | One-to-N event notification | Subscriber list with an `update()` method |
| **State** | Behavior variation by machine state | Delegation to the active state object |
| **Strategy** | Interchangeable alternative algorithms | Strategy-interface composition |
| **Template Method** | Invariant algorithm skeleton | Inheritance with abstract methods/hooks |
| **Visitor** | New operations over composite structures | Double dispatch `accept(visitor)` |
