# TypeScript Handbook — Essential Reference Guide

Consolidated summary of the official TypeScript Handbook documentation (typescriptlang.org/docs/handbook), covering: The Basics, Everyday Types, Narrowing, Generics, and Type Manipulation.

---

## 1. Primitive Types and Fundamental Rules (Everyday Types)

- **Primitives**: `string`, `number`, `boolean` (always lowercase — `String`, `Number`, `Boolean` are rare built-in types and should not be used).
- **Arrays**: `number[]` or `Array<number>` syntax. `[number]` is a **tuple**, not an array.
- **`any`**: disables all type checking for the value. Enable `noImplicitAny` to flag implicit `any` as an error.
- **`unknown`**: a safe alternative to `any` — it requires narrowing before you operate on the value.
- **Type annotations** go **after** the identifier: `let myName: string = "Alice";`. Prefer letting TypeScript **infer** (fewer annotations than you imagine).
- **bigint**: `const big: bigint = 100n;`
- **symbol**: `const s = Symbol("name")` — a unique global reference, never equal to another Symbol.

## 2. Functions

- Type annotations on parameters (after the name) and the return type (after the parameter list).
- Functions that return Promises: annotate with `Promise<T>` on `async` functions.
- **Contextual typing**: anonymous functions/callbacks parameterized in places where TS knows how they will be called receive types automatically (`names.forEach((s) => ...)` — `s` is `string`).
- Optional parameters: `name?: string` → type `string | undefined`; check before use.

## 3. Object Types

- Anonymous object literals: `function printCoord(pt: { x: number; y: number })`.
- **Optional properties**: `last?: string` — reading produces `string | undefined`; use `if (obj.last !== undefined)` or `obj.last?.toUpperCase()`.
- `readonly` for immutability of properties.

## 4. Union Types and Narrowing

- **Union**: `number | string` — values that can be any of the members. You can only operate with properties/features valid for **all** members.
- **Narrowing** (refining the type along the runtime flow):
  - `typeof` type guards (`"string" | "number" | "bigint" | "boolean" | "symbol" | "undefined" | "object" | "function"`). Careful: `typeof null === "object"` in JS!
  - **Truthiness** (falsy values: `0`, `NaN`, `""`, `0n`, `null`, `undefined`). Beware: a truthy check excludes the empty string — prefer specific checks.
  - **Equality** (`===`, `!==`; `== null` covers `null` AND `undefined`).
  - The **`in`** operator (`"swim" in animal`) — optional properties appear on both sides.
  - **`instanceof`** (`x instanceof Date`).
  - **Assignments** and **control flow analysis** (an early return removes members from the union in the following branches).
- Type predicates (custom guards):
  ```typescript
  function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
  }
  ```
  Use: `zoo.filter(isFish)` produces `Fish[]`.
- Assertion functions (TS 3.7+): functions that "assume" a type after the call without an error.

## 5. Type Aliases vs Interfaces

| Aspect | `interface` | `type` |
| :--- | :--- | :--- |
| Extend | `interface Bear extends Animal {...}` | `type Bear = Animal & {...}` |
| Reopen/add fields | ✅ (declaration merging) | ❌ (duplicate error) |
| Rename primitives/unions | ❌ | ✅ (`type ID = number \| string`) |
| Compiler errors | Always named (good messages) | Aliases before 4.2 could vanish |
| Compiler performance | `extends` is usually faster | Intersections can be more expensive |

**Heuristic**: use `interface` until you need `type` features.

## 6. Type Assertions

- `const el = document.getElementById("id") as HTMLCanvasElement;` or the angle-bracket syntax `<HTMLCanvasElement>` (not in `.tsx`).
- Removed at compile time — **no runtime check**. Only convert to more specific/general versions of the type; for "impossible" coercions first go through `any` or `unknown` (`expr as unknown as T`).
- **`as const`** converts the whole object to literal types (`method: "GET"` instead of `string`) — it avoids literal inference errors on objects.

## 7. Literal Types

- Types of exact values: `"left" | "right" | "center"`, `-1 | 0 | 1`, `true`/`false` (`boolean` is an alias for `true | false`).
- **Literal inference**: mutable object properties widen literals to `string` — solve this with an assertion on the field or `as const` on the object.

## 8. `null`, `undefined`, and Non-null Assertion

- With `strictNullChecks` ON (always recommended): test before use; narrowing removes `null`/`undefined`.
- **Postfix `!`** removes null/undefined without a check — use it only when you are absolutely certain (prefer explicit narrowing).
- `nullish coalescing` `??` and optional chaining `?.` are the preferred idioms.

## 9. Discriminated Unions (central pattern)

```typescript
interface Circle { kind: "circle"; radius: number; }
interface Square { kind: "square"; sideLength: number; }
type Shape = Circle | Square;

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.sideLength ** 2;
  }
}
```

- A common literal property (`kind`) = **discriminant**. A `switch`/`if` on the discriminant narrows the union automatically.
- **Exhaustiveness checking** with `never`:
  ```typescript
  default: {
    const _exhaustiveCheck: never = shape; // erro de compilação se sobrar caso
    return _exhaustiveCheck;
  }
  ```
- `never` = an impossible state; assignable to every type, nothing is assignable to `never` (except itself).
- Ideal for message schemas (client/server), machine states, and state-management mutations.

## 10. Generics

- Generic **identity function**: `function identity<Type>(arg: Type): Type { return arg; }` — it captures the input type and carries it to the return (unlike `any`, which loses information).
- **Type argument inference**: `identity("myString")` → `Type = string`. Pass an explicit type only when inference fails.
- Type variables are part of the structure: `function loggingIdentity<Type>(arg: Type[]): Type[]`.
- **Constraints** with `extends`:
  ```typescript
  interface Lengthwise { length: number; }
  function loggingIdentity<Type extends Lengthwise>(arg: Type): Type { ... }
  ```
- **Type parameters referencing other type parameters**:
  ```typescript
  function getProperty<Type, Key extends keyof Type>(obj: Type, key: Key) {
    return obj[key];
  }
  ```
- **Class types in factories**: `function create<Type>(c: { new (): Type }): Type { return new c(); }` (the basis for mixins).
- **Generic parameter defaults**: `create<T extends HTMLElement = HTMLDivElement>` — rules: a parameter with a default is optional; required parameters cannot follow optional ones; the default must satisfy the constraint.
- **Generic classes**: generic only on the **instance side** (static members do not use the type parameter). There are no generic enums/namespaces.
- **Variance annotations** (`in`/`out`/`in out`): an advanced and rare feature — TS infers variance structurally; never write an annotation that does not match the structure. Use it only for performance debugging/extreme cases.

## 11. Creating Types from Types (Type Manipulation)

- **Keys**: keyof — `const Key extends keyof Type` (property names as a union of literals).
- **Value→Type**: `typeof` operator — `type Config = typeof DEFAULT_CONFIG;`.
- **Indexed Access**: `Type["a"]` — extracts the type of a property.
- **Conditional types**: `T extends U ? X : Y` (the type system's if/else); combined with `infer` and conditional distribution over unions.
- **Mapped types**: `{ [K in keyof T]: readonly T[K] }` (the basis for `Partial`, `Readonly`, etc.).
- **Template Literal Types**: types built by concatenating literals: `type EventName = \`${"on"}${Capitalize<Event>}\``.
- **Main utility types** to reuse: `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`, `ReturnType`, `InstanceType`, `Parameters`, `Awaited`, `ThisType`.

## 12. Common Compiler Errors (official numbering)

| Code | Error | Typical cause |
| :-: | :--- | :--- |
| 2322 | `'X' is not assignable to type 'Y'` | Assignment of a value of an incompatible type |
| 2345 | Argument not assignable | Function parameter with an incompatible type |
| 2339 | `Property 'x' does not exist on type ...` | Access without narrowing (union/nonexistent) |
| 18048 | `'x' is possibly 'undefined'` | Optional property without a check |
| 18047 | `'x' is possibly 'null'` | Nullable value without a check |
| 2352 | Conversion may be a mistake | Type assertion between types without overlap (use `as unknown as`) |
| 2367 | Comparison appears to be unintentional | Comparison without overlap (wrong literal, typo) |
| 2872 | This kind of expression is always truthy | Unnecessary truthiness check |
