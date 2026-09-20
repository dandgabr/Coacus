---
name: framework-spring-boot
description: "Provides engineering and architecture patterns for enterprise applications with Spring Boot 3.x+, covering Spring MVC REST, constructor dependency injection, immutable DTOs (Records), Virtual Threads (Loom), validation, Spring Data JPA, and testing with Testcontainers."
---

# Spring Boot Server Engineering & Best Practices

This skill establishes the software engineering standards and rules for enterprise applications and microservices built with **Spring Boot 3.x+** and modern Java (Java 17/21/25).

---

## 🧭 1. Architectural and Design Principles
1. **Clean Layer Separation**:
   - Keep framework annotations at the entry points (REST Controllers), configuration, and infrastructure adapters.
   - Avoid coupling domain classes to serialization or persistence annotations whenever possible.
2. **Idiomatic Dependency Injection**:
   - Strictly use constructor injection with `final` fields. Avoid direct `@Autowired` on fields (it makes testing harder and couples the class to the DI container).
   - Inject interfaces or specialized beans instead of direct implementation classes.
3. **Immutability and Modern DTOs**:
   - Use Java `record` for all Data Transfer Objects (Requests and Responses), guaranteeing immutability and structured validation with Jakarta Bean Validation (`@Valid`, `@NotNull`, `@NotBlank`, and so on).

---

## ⚡ 2. Performance, Concurrency, and Virtual Threads
- **Virtual Threads (Project Loom)**: In Spring Boot 3.2+, enable `spring.threads.virtual.enabled=true` for the embedded Tomcat server and for asynchronous tasks blocked on I/O.
- **Avoid Pinning**: On routes that use Virtual Threads, audit the use of `synchronized` and replace it with `ReentrantLock` in blocks that make network or database calls.
- **Spring Data JPA**: Avoid N+1 queries by using `JOIN FETCH`, `@EntityGraph`, or dedicated DTO projections.

---

## 🧪 3. Testing Strategy
- **Fast Unit Tests**: Test services and business rules without loading the Spring context (`MockitoExtension`, instantiating the class directly).
- **Focused Layer Tests**: Use `@WebMvcTest` to validate REST endpoints, security filters, and Jackson serialization without initializing the database.
- **Integration Tests with Testcontainers**: Use `@SpringBootTest` with Testcontainers for real PostgreSQL, MySQL, or Redis instances.
