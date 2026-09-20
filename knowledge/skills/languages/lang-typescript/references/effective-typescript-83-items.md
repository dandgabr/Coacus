# Effective TypeScript (2nd Edition) — The 83 Items Consolidated

An organized summary of *Effective TypeScript: 83 Specific Ways to Improve Your TypeScript, 2nd Edition* (Dan Vanderkam), grouped by the book's 10 chapters. Each item has a one-line explanation; the most impactful items get short code snippets.

---

## Chapter 1 — Getting to Know TypeScript (Items 1–5)

- **Item 1**: TypeScript and JavaScript are separate layers — understand TS as a superset with a static type system that disappears at runtime.
- **Item 2**: Know which compiler options (tsconfig) are active in your project — TS behavior depends directly on them.
- **Item 3**: Code generation is independent of types — type errors do not stop the compiler from emitting JS (except `noEmitOnError`); types never fix runtime bugs.
- **Item 4**: Structural typing: compatibility is defined by **structure**, not by nominal declaration.
- **Item 5**: Limit the use of `any` — each `any` turns off the checker at that point, breaks contracts, and spreads silently.

## Chapter 2 — TypeScript's Type System (Items 6–17)

- **Item 6**: Use the editor to interrogate the type system (hover, quick info, definition) — understanding the inferred type avoids errors before they exist.
- **Item 7**: Think of types as **sets of values**:
  ```typescript
  type A = string;          // conjunto infinito de strings
  type B = "left" | "right"; // conjunto de 2 valores
  type C = never;            // conjunto vazio (⊥)
  // Subtipo = subconjunto; assignable = ∈ conjunto
  ```
  `never` is empty, `unknown` is the universal set, `string` is never assignable to `"left" | "right"`, but the reverse is.
- **Item 8**: Distinguish **type space** from **value space** — the same symbol can exist in both (`type Foo` + `const Foo`); `typeof` means different things in each space.
- **Item 9**: Prefer annotations to assertions (`as`) — an annotation validates the value; an assertion checks nothing (except overlap) and masks real errors.
- **Item 10**: Avoid wrapper types (`String`, `Number`, `Boolean`, `Symbol`, `BigInt`) — use the lowercase primitives.
- **Item 11**: Distinguish **excess property checking** (only on object literals!) from normal structural type checking.
- **Item 12**: Apply types to the **whole function expression** rather than to each parameter:
  ```typescript
  const diceRoll: Record<number, number> = {}; // contexto para a variável
  fetchAll("users", (users: User[]) => {}); // ❌ anote o alvo, não o callback
  // ✅ type FetchAll = (table: string, cb: (rows: unknown[]) => void) => void
  ```
- **Item 13**: Know the differences between `type` and `interface` (see the table in the Handbook reference); heuristic: `interface` until you need `type` features.
- **Item 14**: Use `readonly` to avoid errors associated with mutation (`readonly T[]` arrays, `readonly` properties).
- **Item 15**: Use type operations and generics to **avoid repeating yourself** — derive types (`keyof`, `typeof`, indexed access, mapped types) from a single source of truth.
- **Item 16**: Prefer more precise alternatives to **index signatures** (`Record<K, V>`, mapping keys with `as const`, unmarked interfaces) — an index signature allows arbitrary properties and loses checking.
- **Item 17**: Avoid numeric index signatures (`{[i: number]: T}`) — they are rarely what you want.

## Chapter 3 — Type Inference and Control Flow Analysis (Items 18–28)

- **Item 18**: Do not clutter the code with inferable types — annotate only contract boundaries.
- **Item 19**: Use different variables for values of different types (avoid reusing and widening the type).
- **Item 20**: Understand **how a variable gets its type** (initialization, annotation, context, `const`/`let`).
- **Item 21**: Create objects **all at once** — incremental assignments produce weak types (`{}`/partials).
- **Item 22**: Understand **type narrowing** (checks that refine types along the control flow).
- **Item 23**: Be **consistent in the aliases** you define — reuse the same type name instead of rewriting structures:
  ```typescript
  interface UserInfo { id: string; name: string; }
  function getUser(id: string): UserInfo { ... }  // ✅
  function getUserName(user: { id: string; name: string }) { ... } // ❌ duplicado
  ```
- **Item 24**: Understand the use of **context** in inference (contextual typing on callbacks/literals).
- **Item 25**: Understand **evolving types** (`let x = []` evolves from `any[]` as it is used).
- **Item 26**: Use functional constructs and libraries (map/filter/reduce, lodash) to favor **type flow**.
- **Item 27**: Prefer `async`/`await` to callbacks — a Promise models `T | error` better and preserves type flow.
- **Item 28**: Use classes and currying to create new **inference sites** (generic binding of types in sub-parts).

## Chapter 4 — Type Design (Items 29–42)

- **Item 29**: Prefer types that **always represent valid states** — the type design should make the inconsistent state impossible:
  ```typescript
  // ❌ Estado inválido representável: loaded mas sem dados, loading E erro
  interface State {
    pageError?: string;         // separados, coerentes entre si
    loading: boolean;
    page?: PageContent;
  }
  // ✅ União de estados fechada:
  type PageState =
    | { state: "loading" }
    | { state: "error"; error: string }
    | { state: "ready"; page: PageContent };
  ```
- **Item 30**: **Liberal in what it accepts, strict in what it produces** (Postel): parameters with broad types (unions) and outputs with precise types.
- **Item 31**: Do not repeat type information in documentation — the type IS the source of truth; use TSDoc for semantics that are not encoded in code.
- **Item 32**: Avoid including `null`/`undefined` inside type aliases — the optional contaminates every use (`type FetchResult = T | null` spreads null).
- **Item 33**: Push `null` values to the **periphery** of your types (deal with null early, at the boundary).
- **Item 34**: Prefer a **union of interfaces** to an interface with unions — each variant carrying its own required fields:
  ```typescript
  // ❌ interface Layer { type: "file"|"database"; layout: LayoutSpec; path?: string; db?: string }
  // ✅
  type Layer = FileLayer | DatabaseLayer; // cada variante com seus campos
  ```
- **Item 35**: Prefer more precise alternatives to `string` (literal unions, branded, template literal types).
- **Item 36**: Use a distinct type for special values (e.g., `-1` meaning "not found" → `type NotFoundSentinel = -1` or a `T | null` return).
- **Item 37**: Limit optional properties — `?` properties create `| undefined` and vague states; prefer explicit unity.
- **Item 38**: Avoid **repeated parameters** of the same type (confusable positionals) — group them into an object:
  ```typescript
  // ❌ function getListItem(index: number, count: number): number
  // ✅
  interface IndexAndCount { index: number; count: number }
  function getListItem(opts: IndexAndCount): number { ... }
  ```
- **Item 39**: Prefer **unifying types** to modeling the differences — not every variation deserves its own type (e.g., `Vector3D` and `Vector2D` with identical coords can be unified by a single interface + per-field data).
- **Item 40**: Prefer **imprecise to inaccurate** types (safe `imprecise` > `inaccurate` that lies to the compiler).
- **Item 41**: Name types with the **domain language** of the problem (not the framework/technical structure).
- **Item 42**: Avoid types based on **anecdotal data** (modeling only the cases you could observe, e.g., only 3 error categories seen in logs).

## Chapter 5 — Unsoundness and the any Type (Items 43–49)

- **Item 43**: Use the **narrowest possible scope** for `any` — never in a public return; localize it as much as possible (local cast, not the whole signature).
- **Item 44**: Prefer more precise variants of `any` (`any[]` instead of `any`; `unknown` on input; partially typed functions to fully free ones).
- **Item 45**: **Hide unsafe assertions inside well-typed functions** — the inconsistency stays contained in a single testable point:
  ```typescript
  // ❌ espalhado: JSON.parse(...) as User
  // ✅
  function parseUser(json: string): User {
    return JSON.parse(json); // any contido aqui, retorno seguro
  }
  ```
  (Ideally validate at runtime before this point.)
- **Item 46**: Use `unknown` (not `any`) for values of unknown type — `unknown` requires narrowing, `any` does not.
- **Item 47**: Prefer type-safe approaches to **monkey patching** (interfaces with optional fields, `Object.assign`, symbol-keyed props).
- **Item 48**: Avoid TS **soundness traps** (array covariance, `as`, mutable getters, loose `this`) — know where TS does not protect you.
- **Item 49**: Measure **type coverage** (`type-coverage` package / `strict`) to prevent type-safety regressions.

## Chapter 6 — Generics and Type-Level Programming (Items 50–58)

- **Item 50**: Think of generics as **functions between types** (input `T` → derived output):
  ```typescript
  type ShallowArrayOrSingle<T> = T[] | T;
  type Pick_<Obj, Keys extends keyof Obj> = {
    [K in Keys]: Obj[K];
  };
  ```
- **Item 51**: Avoid **unnecessary type parameters** — do not add a generic the caller has to spell out; let inference do its job.
- **Item 52**: Prefer **conditional types** to overload signatures — a condition in the type system replaces chains of overloads:
  ```typescript
  // Em vez de 3 overloads de getElementById, use conditional:
  type ElemById<Tag extends string> = Tag extends keyof HTMLElementTagNameMap
    ? HTMLElementTagNameMap[Tag]
    : HTMLElement;
  declare function getElementById<Tag extends string>(id: Tag): ElemById<Tag>;
  ```
- **Item 53**: Control the **distribution of unions over conditional types** — naked type params distribute (e.g., the filter `T extends null ? never : T`); use `[T] extends [U]` to prevent distribution.
- **Item 54**: Use **Template Literal Types** to model DSLs and relationships between strings:
  ```typescript
  type Route = `/${string}`;
  type OnEvent = `on${Capitalize<"click" | "focus">}`; // "onClick" | "onFocus"
  type Prop = `${"left" | "right"}${"Top" | "Bottom"}`; // CSS Position
  ```
- **Item 55**: **Write tests for your types** (`Expect<Equal<A, B>>` idiom) — complex types are code and deserve a suite.
- **Item 56**: Pay attention to **how types are displayed** (hover) — if the display confuses you, the type is poorly written.
- **Item 57**: Prefer **tail-recursive** generic types (recursion in the last case) to avoid stack depth in the compiler.
- **Item 58**: Consider **codegen** as an alternative to overly complex types (synthesizing types from real data).

## Chapter 7 — TypeScript Recipes (Items 59–64)

- **Item 59**: Use `never` for **exhaustiveness checking** (the compiler flags a missing case in a union switch):
  ```typescript
  function area(shape: Shape): number {
    switch (shape.kind) {
      case "circle": return Math.PI * shape.radius ** 2;
      case "square": return shape.sideLength ** 2;
      default: {
        const _exhaustive: never = shape; // erro se entrar "triangle"
        return _exhaustive;
      }
    }
  }
  ```
- **Item 60**: Know how to iterate objects safely (`Object.entries` with a typed generic helper, `keyof` + controlled cast).
- **Item 61**: Use **`Record` to keep values in sync** — a `Record<Channel, Handler>` guarantees a handler for each variant:
  ```typescript
  const handlers: Record<Channel, () => void> = { sms: ..., email: ... };
  ```
- **Item 62**: Use **rest parameters + tuple types** for variadic functions (`(...args: [string, number])`, typed spreads, `Parameters<T>`).
- **Item 63**: Use **optional `never` properties to model XOR** — `a?: never` on the variant blocks the b field:
  ```typescript
  type ExclusiveProps =
    | { a: string; b?: never }
    | { a?: never; b: number };
  ```
- **Item 64**: Consider **brands for nominal typing** (the system is structural; a brand adds identity to IDs):
  ```typescript
  type Brand<T, TBrand extends string> = T & { readonly __brand: TBrand };
  type UserId = Brand<string, "UserId">;
  type OrderId = Brand<string, "OrderId">;
  declare function fetchUser(id: UserId): Promise<User>;
  fetchUser(orderId); // ❌ erro — exatamente o que se quer
  ```

## Chapter 8 — Type Declarations and @types (Items 65–71)

- **Item 65**: Put `typescript` and `@types/*` in `devDependencies` (they do not affect prod).
- **Item 66**: Understand the **three versions involved** in type declarations (the TS version, the `@types` version, and the lib version) and their misalignments.
- **Item 67**: **Export every type that appears in public APIs** — do not force users to redeclare/recreate structures.
- **Item 68**: Use **TSDoc** (`@param`, `@returns`, `@remarks` tags) for API comments — they appear on hover.
- **Item 69**: Provide a type for `this` in callbacks when `this` is part of the API:
  ```typescript
  type AddEventListener_ = (ev: string, cb: (this: HTMLElement, e: Event) => void) => void;
  ```
- **Item 70**: **Mirror types** to break dependencies — define your own interfaces instead of importing the whole library (weak coupling).
- **Item 71**: Use **Module Augmentation** to improve third-party types without editing the package:
  ```typescript
  // types/mirror.d.ts
  declare module "express-serve-static-core" {
    interface Request {
      currentUser?: User;
    }
  }
  // `req.currentUser` agora é tipado em todo o projeto
  ```

## Chapter 9 — Writing and Running Your Code (Items 72–78)

- **Item 72**: Prefer **ECMAScript features to TypeScript features** (enums vs `as const` objects, parameter properties, namespaces) — "JS-only" code survives bundler refactors.
- **Item 73**: Use **source maps** to debug TypeScript in the debugger/stack traces.
- **Item 74**: Know how to reconstruct types at **runtime** (serialization/roundtrip: `toJSON`/`reviver`, Zod schemas) — types do not exist at runtime.
- **Item 75**: Understand the **DOM hierarchy** (`HTMLElement` → `HTMLCanvasElement`) to use `instanceof` as correct narrowing.
- **Item 76**: Create a **precise model of the environment** (DOM, Node, Web Worker) — the TS default assumes `dom`, which may not even exist.
- **Item 77**: Understand the relationship between **type checking and unit tests** — types check at compile time; tests check at runtime; neither replaces the other.
- **Item 78**: Pay attention to **compiler performance** (project references, `skipLibCheck`, incremental interfaces).

## Chapter 10 — Modernization and Migration (Items 79–83)

- **Item 79**: Write **modern JavaScript** — what is valid in ES2015+ transpiles less and migrates with less friction.
- **Item 80**: Use **`@ts-check` + JSDoc** to try TypeScript in a `.js` file without converting it.
- **Item 81**: Use **`allowJs`** to mix TS and JS in the same project during migration.
- **Item 82**: Convert **module by module, following the dependency graph** (leaves → root), keeping the project compiling at every step.
- **Item 83**: Migration **is only complete when `noImplicitAny` is enabled** — without it, implicit `any` keeps contaminating the code.

---

### Golden items (executive summary)
1. Types are sets (Item 7) — always ask "which values fit here?".
2. Valid states encoded in the type (Item 29) — a union of states ≥ boolean flags.
3. Accept liberally, produce strictly (Item 30).
4. `unknown` > `any`; `any` with the minimum scope (Items 43–46).
5. Derive types instead of duplicating them (Items 15, 23).
6. `never` guarantees exhaustiveness (Item 59).
7. Template literals + conditional types model textual relationships (Items 52–54).
8. Brands provide nominal typing where it is missing (Item 64).
