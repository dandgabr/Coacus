---
name: "cpp-template-metaprogramming"
description: "Provides expert patterns in C++ template metaprogramming and generic programming based on the ISO/IEC 14882 standard (C++17/20/23), covering deduction and CTAD, full and partial specialization, variadic templates and fold expressions, non-type template parameters, SFINAE/enable_if, tag dispatch, the detection idiom, C++20 concepts and requires clauses with subsumption ordering, type traits and constexpr computation, if constexpr, CRTP and policy-based design, mixins, typelists, type erasure, template instantiation cost control and compile-time performance."
---

# AI Skill: C++ Template Metaprogramming and Generic Programming

This skill guides the AI to act as a specialist in **template metaprogramming (TMP)** and **generic programming** in modern C++, building on *C++ Template Metaprogramming in Practice: A Deep Learning Framework* (Li Wei) and *Template Metaprogramming with C++* (Marius Băncilă), and always deferring to the normative ISO/IEC 14882 standard and [en.cppreference.com](https://en.cppreference.com/).

The core idea: **make information a type, not runtime data.** Tags, categories, constraints and dimensions become types checked by the compiler, enabling reuse and compile-time validation instead of runtime branching.

---

## 🧭 When to Activate

- Designing generic libraries, policy-based components, expression templates or compile-time DSLs.
- Replacing SFINAE-heavy code with concepts, or diagnosing ambiguous/verbose overload errors.
- Solving "compile-time performance" problems: instantiation explosion, code bloat, long builds.
- Building static polymorphism (CRTP) where virtual dispatch is unavailable or too costly.
- Implementing type erasure, typelists, or heterogeneous compile-time containers.

---

## 🧱 Template Fundamentals

### Parameter kinds and deduction

Three parameter kinds: **type** (`typename T`), **non-type** (`int N`, and C++20 literal class types), and **template-template** (`template <typename> class C`). Function templates deduce arguments from the call; class templates use **Class Template Argument Deduction (CTAD, C++17)** driven by compiler-generated *deduction guides*, which users may supply with a trailing-return syntax in the same namespace:

```cpp
template <typename T> wrapper(T) -> wrapper<T>;
template <typename Iter>
range_t(Iter first, Iter last) -> range_t<typename std::iterator_traits<Iter>::value_type>;
```

CTAD from aggregate initialization was extended in C++20, making factory functions such as `std::make_pair` largely redundant.

### Specialization

- **Full (explicit) specialization** fixes every argument; **partial specialization** fixes some.
- It is illegal to place a fully specialized nested template inside a non-fully-specialized class template. The workaround is a **dummy partial specialization** so `Fun_<int>` still resolves:

```cpp
template <typename T, typename TDummy = void> struct Fun_ { /* primary */ };
```

### Variadic templates and fold expressions

A parameter pack may expand in fifteen contexts (template/function parameter and argument lists, brace/parenthesized initializers, base specifiers, member-initializer lists, fold expressions, `using`, lambda captures, `sizeof...`, align-specifiers, attributes). **Fold expressions (C++17)** collapse a pack over a binary operator and cut both instantiations and overload count:

```cpp
return (0 + ... + values);      // binary left fold with init
(v.push_back(args), ...);        // unary left fold over the comma operator
```

Unary folds fail on an empty pack; binary folds carry an initial value. Nested recursive templates keyed on an outer loop parameter cannot reuse instantiations — **split loops so instantiation keys are globally unique**, and prefer **short-circuit metafunctions** (a `false` specialization that never touches the recursive operand) over `cond && Recursive<...>`.

---

## 🛠️ SFINAE, Tag Dispatch and the Detection Idiom

**SFINAE** removes a candidate when substitution fails in the *immediate context* (template parameters, return type, parameter list) — never from the function body, where failures are hard errors.

```cpp
template <typename T, typename std::enable_if<uses_write_v<T>>::type* = nullptr>
void serialize(std::ostream& os, T const& value) { value.write(os); }
```

**Detection idiom** via `std::void_t` maps a pack to `void` to trigger substitution failure:

```cpp
template <typename T, typename = void> struct is_container : std::false_type {};
template <typename T>
struct is_container<T, std::void_t<typename T::value_type, typename T::size_type,
    decltype(std::declval<T>().size()), decltype(std::declval<T>().begin())>>
  : std::true_type {};
```

**Tag dispatch** selects an overload from an empty tag class passed as the last argument:

```cpp
namespace details {
  void advance(It& it, Distance n, std::random_access_iterator_tag);
  void advance(It& it, Distance n, std::bidirectional_iterator_tag);
}
template <typename Iter, typename Distance>
void advance(Iter& it, Distance n) {
  details::advance(it, n, typename std::iterator_traits<Iter>::iterator_category{});
}
```

Order of preference for modern code: **concepts → `if constexpr` → SFINAE/enable_if → tag dispatch**.

---

## 🚦 Concepts and Constraints (C++20)

A **concept** is a named set of constraints; a **requires clause** gates participation; a **requires expression** checks well-formedness. Four requirement categories: **simple** (`a + b;`), **type** (`typename T::value_type;`), **compound** (`{ expr } -> ReturnType;`), and **nested** (`requires C<T>;`).

```cpp
template <typename T> concept arithmetic = std::is_arithmetic_v<T>;
template <arithmetic T> T add(T a, T b) { return a + b; }
```

**Ordering and subsumption.** Constraints normalize into conjunctions/disjunctions of **atomic constraints**. If A implies B, A *subsumes* B; the strictly more-constrained overload wins. Crucially, **concepts order overloads; raw type-trait booleans do not** — identical type-trait overloads produce ambiguity while the concept form resolves. Conjunctions inside a concept-wrapped fold short-circuit per argument: `(Integral<T> && ...)`. Abbreviated templates (`void f(arithmetic auto x)`) are the sugar.

Prefer concepts over SFINAE mainly for **diagnostics and ordering**.

---

## 🧮 Type Traits and Compile-Time Computation

Type traits *query* (category, properties, supported operations) or *transform* (cv/ref/pointer, sign, `std::conditional`, `std::decay`) types. The idiom is a primary template deriving `std::false_type`/`std::true_type` plus a `_v` variable template.

**`if constexpr`** discards a branch at compile time (no short-circuit: both operands must be well-formed) and replaces tag dispatch for value-level branching — but it **cannot select different return types**, which still needs specialized templates.

```cpp
template <typename T> void serialize(std::ostream& os, T const& v) {
  if constexpr (uses_write_v<T>) v.write(os); else os << v;
}
```

**Two-phase lookup:** non-dependent names bind at definition, dependent names at instantiation. `this->` / `Base<T>::` makes a name dependent; `typename` disambiguates dependent *types*, `template` dependent *templates* (`obj.template foo<T>()`). **Forwarding references** require exactly `T&&`.

---

## 🔗 CRTP, Policy Design, Mixins, Typelists, Type Erasure

**CRTP** (`class Derived : public Base<Derived>`) delivers static polymorphism where virtual cannot be used (members that are themselves templates or static):

```cpp
template <typename D> struct Base {
  template <typename TI> void Fun(const TI& in) { static_cast<D*>(this)->Imp(in); }
};
struct Derive : Base<Derive> { template <typename TI> void Imp(const TI& in) { /*...*/ } };
```

**Mixins** invert CRTP: a mixin template *derives from* its argument, adding behavior.

**Type erasure** hides unrelated types behind a uniform interface; the non-allocating form stores a function pointer plus an aligned buffer instead of heap-allocating a wrapper.

**Typelists** manage type sequences — the variadic form `template <typename... Ts> struct typelist {};` is simplest; operations (`front_t`, `back_t`, `at_t`, `push_back`, `pop_front`) are partial specializations.

**Policy-based design** treats behavior as types composed by **composition (preferred)** or private inheritance (empty-base optimization). Policies are behavior, traits are attributes.

---

## ⚙️ Compile-Time Performance and Pitfalls

- **Instantiation explosion**: compilers retain every generated instance; nested recursion keyed on a loop parameter exhausts RAM. Split loops, use tags (declare-only types) rather than function parameters, and encapsulate internals in a dedicated `detail`/`NS*` namespace.
- **Diagnostics** from metaprogram failures are cryptic; concepts improve them and should be preferred.
- **Header-only distribution** means no information hiding and mandatory recompilation of every includer — split compile-heavy/secret logic into static libraries.
- **Uninstantiated code is untested** — demand high test coverage for templates.

The **MetaNN case study** (Li Wei) builds a deep-learning framework with compile-time `CategoryTags`, a `VarTypeDict` heterogeneous dictionary (keys are empty struct tags because strings cannot be template arguments), lazy **expression templates** (`Add<Add<X,Y>,Z>`), and a two-phase **register → compute** evaluation. The design lessons transfer to any compile-time DSL: make information a type, separate orthogonal concerns into small metafunctions, preserve laziness, and control instantiation growth deliberately.

---

## 🔗 Integration with Other Skills

- For the language-level feature set, see [lang-cpp](../lang-cpp/SKILL.md).
- For compiler/backend implementation details that consume this IR, see [llvm-compiler-infrastructure](../../engineering/practices/llvm-compiler-infrastructure/SKILL.md).
- For memory-safety implications of template-heavy code, see [sast-code-review](../../security/appsec/sast-code-review/SKILL.md).
