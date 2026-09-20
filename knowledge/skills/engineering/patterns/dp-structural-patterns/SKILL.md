---
name: dp-structural-patterns
description: "Acts as a specialist in GoF Structural Design Patterns, based on Design Patterns (Gang of Four) and Refactoring to Patterns. Covers Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy, explaining how to compose classes and objects into larger, more flexible structures while keeping coupling low."
---

# Structural Design Patterns (GoF Structural Patterns)

Structural patterns explain how to compose classes and objects into larger structures while keeping those structures flexible and efficient. Object composition offers far more runtime flexibility than static class inheritance.

---

## 🔌 1. Adapter

### 1.1 Intent and Motivation
Converts a class's interface into another interface that clients expect. It lets classes with incompatible interfaces work together.

```mermaid
classDiagram
    class Client
    class Target {
        <<interface>>
        +request()
    }
    class Adapter {
        -adaptee: Adaptee
        +request()
    }
    class Adaptee {
        +specificRequest()
    }
    Client --> Target
    Target <|.. Adapter
    Adapter o-- Adaptee : traduz chamada
```

---

## 🌉 2. Bridge

### 2.1 Intent and Motivation
Decouples an abstraction from its implementation, allowing both to vary independently through separate hierarchies linked by composition.

```mermaid
classDiagram
    class Abstraction {
        -impl: Implementation
        +feature()
    }
    class RefinedAbstraction {
        +feature()
        +advancedFeature()
    }
    class Implementation {
        <<interface>>
        +method1()
        +method2()
    }
    class ConcreteImplA {
        +method1()
        +method2()
    }
    class ConcreteImplB {
        +method1()
        +method2()
    }
    Abstraction <|-- RefinedAbstraction
    Abstraction o-- Implementation : ponte
    Implementation <|.. ConcreteImplA
    Implementation <|.. ConcreteImplB
```

---

## 🌳 3. Composite

### 3.1 Intent and Motivation
Composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions of objects uniformly.

```mermaid
classDiagram
    class Component {
        <<interface>>
        +execute()
    }
    class Leaf {
        +execute()
    }
    class Composite {
        -children: List~Component~
        +add(c: Component)
        +remove(c: Component)
        +execute()
    }
    Component <|.. Leaf
    Component <|.. Composite
    Composite o-- Component : contém
```

---

## 🎀 4. Decorator (Wrapper)

### 4.1 Intent and Motivation
Attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

```mermaid
classDiagram
    class Component {
        <<interface>>
        +operation()
    }
    class ConcreteComponent {
        +operation()
    }
    class BaseDecorator {
        -wrappee: Component
        +operation()
    }
    class ConcreteDecoratorA {
        +operation()
        +addedBehavior()
    }
    Component <|.. ConcreteComponent
    Component <|.. BaseDecorator
    BaseDecorator o-- Component
    BaseDecorator <|-- ConcreteDecoratorA
```

---

## 🏛️ 5. Facade

### 5.1 Intent and Motivation
Provides a simplified, high-level interface to a complex subsystem made up of multiple classes, making the subsystem easier to use and decoupling clients from internal details.

```mermaid
classDiagram
    class Client
    class VideoConverterFacade {
        +convertVideo(file, format)
    }
    class AudioMixer
    class BitrateReader
    class CodecFactory
    Client --> VideoConverterFacade
    VideoConverterFacade ..> AudioMixer
    VideoConverterFacade ..> BitrateReader
    VideoConverterFacade ..> CodecFactory
```

---

## 🪶 6. Flyweight

### 6.1 Intent and Motivation
Fits a huge number of objects into RAM by sharing common state (intrinsic state) across multiple objects instead of keeping all the data in every instance (extrinsic state).

```mermaid
classDiagram
    class FlyweightFactory {
        -flyweights: Map
        +getFlyweight(key) Flyweight
    }
    class TreeType {
        -name
        -color
        -texture
        +draw(canvas, x, y)
    }
    class Tree {
        -x
        -y
        -type: TreeType
        +draw(canvas)
    }
    FlyweightFactory o-- TreeType
    Tree o-- TreeType : compartilha estado intrínseco
```

---

## 🛡️ 7. Proxy

### 7.1 Intent and Motivation
Provides a substitute or placeholder for another object to control access to it. Common types: Remote Proxy, Virtual Proxy (Lazy Loading), Protection Proxy (Access Control), and Cache/Log Proxy.

```mermaid
classDiagram
    class ServiceInterface {
        <<interface>>
        +operation()
    }
    class RealService {
        +operation()
    }
    class Proxy {
        -realService: RealService
        +operation()
    }
    ServiceInterface <|.. RealService
    ServiceInterface <|.. Proxy
    Proxy o-- RealService : controla acesso
```

---

## ⚖️ Comparative Matrix of Structural Patterns

| Pattern | Problem Solved | Structural Strategy |
| :--- | :--- | :--- |
| **Adapter** | Incompatible interfaces between legacy/third-party systems | Wraps an existing object, translating calls |
| **Bridge** | Combinatorial subclass explosion in 2 orthogonal dimensions | Separates Abstraction and Implementation via a reference |
| **Composite** | Recursive handling of hierarchical (tree) structures | Treats leaves and composite nodes with the same interface |
| **Decorator** | Dynamic addition of responsibilities without inheritance | Wraps the real object, delegating and adding behavior |
| **Facade** | Complexity of subsystem initialization/orchestration | Simplified entry point for multiple components |
| **Flyweight** | High memory use with millions of similar objects | Separates intrinsic (shared) from extrinsic state |
| **Proxy** | Direct access to a heavy, remote, or protected object | Intercepts requests, applying lazy load, auth, or cache |
