---
name: "lang-typescript"
description: "Provides secure and robust software engineering patterns using TypeScript based on the official TypeScript Handbook documentation (typescriptlang.org), Effective TypeScript 2nd Edition (Dan Vanderkam), and Total TypeScript Essentials (Matt Pocock), covering primitive and advanced types, narrowing and type guards, discriminated unions with exhaustiveness checking, generics with constraints, type manipulation (keyof, conditional, mapped, template literal types), utility types, strict compiler safety, and defensive data mapping."
---

# AI Skill: TypeScript Engineering (TypeScript Specialist)

This skill guides the AI to write robust, safe, and highly typed code using the **TypeScript** superset, aligned with the official **TypeScript Handbook** (https://www.typescriptlang.org/docs/handbook/intro.html), *Effective TypeScript 2nd Edition* (Dan Vanderkam), and *Total TypeScript Essentials* (Matt Pocock). The main goal is to guide the AI and developers to avoid runtime errors, build self-cleaning and reusable API contracts, and make the most of the strict safety provided by the compiler.

> 📖 **Canonical reference**: see [references/typescript-handbook.md](references/typescript-handbook.md) for the consolidated Handbook guide (everyday types, narrowing, generics, type manipulation, Utility Types, and the TS error code table).
> 📖 **Effective TypeScript**: see [references/effective-typescript-83-items.md](references/effective-typescript-83-items.md) for the 83 best-practice items from *Effective TypeScript 2nd Edition* (type design, generics, unsoundness, migrations).
> 📖 **Total TypeScript**: see [references/total-typescript-essentials.md](references/total-typescript-essentials.md) for the summary of the 16 chapters of *Total TypeScript Essentials* (narrowing, mutability, classes, deriving types, tsconfig, declaration files).

---

## 🧭 TypeScript Development Guidelines

While working under this skill, apply the following coding standards strictly:

### 1. Strict Compiler Configuration (`tsconfig.json`)
- **Strict Mode**: Ensure the following flags are enabled for maximum protection against null and undefined types:
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noImplicitAny": true,
      "strictNullChecks": true,
      "strictFunctionTypes": true,
      "noImplicitThis": true,
      "alwaysStrict": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noImplicitReturns": true,
      "noFallthroughCasesInSwitch": true
    }
  }
  ```

### 2. Handbook-Grounded Typing
- **Correct Primitives**: Always use `string`, `number`, `boolean` (lowercase). Never `String`/`Number`/`Boolean`. No `int`/`float` — everything is `number` (except `bigint` for huge integers via the `100n` literal).
- **Annotation Restraint**: Prefer letting TypeScript **infer** types; annotate only function parameters/returns exposed to contracts and boundaries. Annotations go **after** the identifier (`let x: string`).
- **Generics with Constraints**: Build generic components that adapt to different shapes — capture the input type and carry it to the output (`<Type>(arg: Type): Type`), with `extends` to guarantee capabilities (`Lengthwise`) and `Key extends keyof Type` for safe property access. Never fall back to `any` to "solve" the problem.
- **`interface` vs `type` Preference**: Use `interface` until you need `type` features (unions, primitive renaming, conditional types). Interfaces have declaration merge, appear named in error messages, and tend to be more performant with `extends`.
- **Utility Types**: Use and combine native utility types (`Partial`, `Pick`, `Omit`, `Readonly`, `Record`, `ReturnType`, `NonNullable`, `Exclude/Extract`, `Awaited`) and **Type Manipulation** (`keyof`, `typeof` operator, Indexed Access, Conditional Types with `infer`, Mapped Types, Template Literal Types) to keep readability and avoid duplicating structures.
- **Discriminated Unions + Exhaustiveness**: Model states and messages with a literal discriminant property (`kind`, `type`, `status`) and a `switch` with **exhaustiveness checking via `never`** — the compiler raises an error when a new union member is added without handling.

### 3. Narrowing and Type Guards
- Use the native narrowing arsenal instead of assertions: `typeof`, truthiness (aware of falsy values: `0, NaN, "", 0n, null, undefined`), strict equality (`===`), `in`, `instanceof`, **control flow analysis** (early returns).
- **Type Predicates**: Create custom guards with `pet is Fish` to reuse checking logic (including in `Array.filter`).
- **Assertions in Moderation**: `as T` is erased at compile time (zero runtime verification). Use it only for "possible" conversions; for complex coercions, `expr as unknown as T`. Prefer `as const` on objects to preserve literal types (avoid literal inference widening `"GET"` → `string`).

### 4. Type Validation at Data Boundaries (API/JSON)
- **Defensive Typing**: Never blindly trust that data received from an external HTTP request or from files matches the declared typing — *type assertions do not validate at runtime*.
- **Runtime Validation**: Use schema validation libraries at runtime (e.g., **Zod**, **Valibot**, **Runtypes**) to inspect and guarantee the input data contract, automatically converting it into valid TypeScript types (schema inference).

---

## 🛠️ Recommended Code Patterns

### Avoid the use of `any` — prefer generics or `unknown`
```typescript
// ❌ Ruim: Perda total de tipagem e segurança
function processData(data: any) {
  return data.name.toUpperCase();
}

//  Bom: Uso de tipos específicos ou Generics
function processData<T extends { name: string }>(data: T): string {
  return data.name.toUpperCase();
}

//  Bom: Entrada arbitrária com contrato explícito antes do uso
function parseJson(input: string): unknown {
  return JSON.parse(input);
}
```

### Discriminated Union with Exhaustiveness Checking
```typescript
interface Circle { kind: "circle"; radius: number; }
interface Square { kind: "square"; sideLength: number; }
interface Triangle { kind: "triangle"; sideLength: number; }

type Shape = Circle | Square | Triangle;

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    case "triangle":
      return (shape.sideLength ** 2) / 2;
    default: {
      // Erro de compilação se um novo membro entrar na união sem case
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
    }
  }
}
```

### Custom Type Guard (Type Predicate)
```typescript
function isFish(pet: Fish | Bird): pet is Fish {
  return "swim" in pet;
}

const zoo: (Fish | Bird)[] = getZoo();
const fishes: Fish[] = zoo.filter(isFish); // narrowing preservado no filtro
```

---

## 🔒 Security Issues and Safe Practices

- **Prototype Pollution**: Validate and sanitize object keys that undergo recursive merge (deep merge) to avoid unwanted injection of properties into JavaScript base classes (such as `__proto__`).
- **Dynamic Code Injection**: Never use `eval()`, `Function()`, or string passing to the `setTimeout()` handler.
- **ReDoS Attacks**: Validate execution-time limits and complexity in regex patterns applied to input validation on a Node.js server.
- **Insecure JSON Deserialization**: Treat the result of `JSON.parse` as `unknown` and validate it with a runtime schema before operating on the value.
- **Responsible Non-null Assertion (`!`)**: The postfix `!` removes `null`/`undefined` without a check — use it only with absolute certainty; prefer explicit narrowing (`if (x !== null)`, `??`, `?.`).

## 🎯 Golden Rules of Type Design (Effective TypeScript)

Consolidation of the items from *Effective TypeScript 2nd Edition* (details in [references/effective-typescript-83-items.md](references/effective-typescript-83-items.md)):

- **Item 29 — Valid states always**: Model the type so that invalid states are **unrepresentable** (`type PageState = { state: "loading" } | { state: "error"; error: string } | { state: "ready"; page: Page }`) instead of loose boolean flags and optional fields.
- **Item 30 — Liberal in inputs, strict in outputs**: Parameters accept wide types (unions); returns/exports are precise and closed.
- **Item 34 — Union of interfaces > interface with unions**: Each variant carries its required fields (`FileLayer | DatabaseLayer`) instead of mixed optional fields.
- **Item 32/33 — Null at the periphery**: Do not embed `null`/`undefined` in reusable aliases; handle them early, at the boundary.
- **Item 35 — Do not use raw `string` for finite domains**: Use literal unions, branded types, or template literal types for IDs, status, routes, and events.
- **Item 37 — Limit optional properties**: `?` produces `| undefined` and vague state; prefer explicit discriminated unions.
- **Item 38 — Avoid confusable positional parameters**: Group repeated parameters of the same type into an object (`{ index: number; count: number }`).
- **Item 40 — Imprecise > inaccurate**: Prefer a "wide but correct" type over a type assertion that lies to the compiler (`as never`), never an **inaccurate type** that does not reflect reality.
- **Item 9/45 — Annotate, do not assert; isolate the unsafe**: Prefer annotations over `as`; if unavoidable, hide the unsafe assertion inside a well-typed function.
- **Item 46/43 — `unknown` > `any`**: Use `unknown` for unknown values; `any`, when unavoidable, with the smallest possible scope.
- **Item 15/23 — Derive, do not duplicate**: Use `keyof`, `typeof`, indexed access, and generics to avoid repetition and keep aliases consistent across the codebase.
- **Item 67/68 — Export types and document with TSDoc**: Every type appearing in a public API is exported; extra semantics go in TSDoc comments (`@param`, `@returns`).
- **Item 64 — Brands for nominal typing**: When typed IDs must not be confusable (`UserId` ≠ `OrderId`), use branded types via intersection.
- **Item 72 — Prefer ECMAScript features**: Enums/parameter properties/namespaces are TS-only; prefer `as const` objects and pure ES modules.

## 🔍 Efficient Narrowing (Total TypeScript)

Narrowing forms (preference in this order — details in [references/total-typescript-essentials.md](references/total-typescript-essentials.md)):

```typescript
type Format = "digital" | "physical";
type Album =
  | { format: "digital"; downloadUrl: string }
  | { format: "physical"; shippingAddress: string };

// 1) Discriminant / disjoint union (melhor desenho possível)
function refund(album: Album): string {
  if (album.format === "digital") return album.downloadUrl;  // narrowed: variante digital
  return album.shippingAddress;                              // narrowed: variante physical
}

// 2) typeof (primitivos) — cuidado com typeof null === "object"
function parse(input: string | number) {
  if (typeof input === "string") return input.trim();
  return input.toFixed(2);
}

// 3) Operador in — existência de propriedade
function hasDownload(album: Album) {
  return "downloadUrl" in album;
}

// 4) Truthiness/nullish (atenção aos falsy: 0, "", NaN, null, undefined)
function name(user: string | null) {
  return user?.toUpperCase() ?? "anonymous";
}

// 5) Exhaustiveness com never: o compilador acusa variante faltante
function label(album: Album): string {
  switch (album.format) {
    case "digital":  return "download";
    case "physical": return "shipping";
    default: {
      const _exhaustive: never = album; // erro se entrar novo formato sem case
      return _exhaustive;
    }
  }
}
```

Complementary golden rules (*Total TypeScript*): use `satisfies` instead of `as` (validates without widening); prefer `@ts-expect-error` over `@ts-ignore` (fails when the error disappears); `const` and `as const` narrow literals that `let` and mutable objects widen.

---

## 🔗 Integration with Other Skills
- [frontend-developer](../../roles/frontend-developer/SKILL.md): Uses TypeScript to build applications with [framework-react](../../frameworks/framework-react/SKILL.md) and [framework-vue](../../frameworks/framework-vue/SKILL.md).
- [backend-developer](../../roles/backend-developer/SKILL.md): Builds typed contracts for RESTful APIs ([framework-rest-api](../../frameworks/framework-rest-api/SKILL.md)) and gRPC clients/servers ([framework-grpc](../../frameworks/framework-grpc/SKILL.md)).
- [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md): Models and optimizes data access in TypeScript (Prisma, TypeORM, Drizzle, Mongoose) aligned with the [db-postgresql](../../data/db-postgresql/SKILL.md), [db-mongodb](../../data/db-mongodb/SKILL.md), [db-mariadb](../../data/db-mariadb/SKILL.md), and [db-sqlite](../../data/db-sqlite/SKILL.md) engines.
- [clean-code-reusability](../../engineering/practices/clean-code-reusability/SKILL.md): Provides code reuse principles and standard documentation (JSDoc) applied to TypeScript development.
