---
name: "framework-graphql"
description: "Provides API engineering and design patterns based on the official GraphQL specification (GraphQL Foundation). Covers Schema Definition Language (SDL), operation types (Query, Mutation, Subscription), resolvers, DataLoader for N+1 prevention, response and error format, introspection, directives, Relay Cursor Connections, and query security."
---

# AI Skill: GraphQL API Engineering and Architecture (framework-graphql)

This skill guides the AI to act as a specialist in the design, architecture, and implementation of **GraphQL APIs**, tightly aligned with the official GraphQL Foundation specifications ([spec.graphql.org](https://spec.graphql.org/)). It covers schema modeling with GraphQL SDL (Schema Definition Language), the construction of executable operations (Queries, Mutations, and Subscriptions), resolver architecture, mitigation of the N+1 problem with DataLoader, standard Relay pagination, strict response format and error handling, and security and optimization best practices.

---

## 🧭 Type System and Schema Definition Language (GraphQL SDL)

### 1. Scalar Types and Null/List Wrappers
- **Native Scalars**: `Int`, `Float`, `String`, `Boolean`, `ID`.
- **Custom Scalars**: Define explicit scalars for specific data validation (e.g., `DateTime`, `JSON`, `EmailAddress`).
- **Type Modifiers (Non-Null and List)**:
  - `[User]`: Nullable list of nullable users.
  - `[User!]`: Nullable list of non-null users.
  - `[User!]!`: Non-null list of non-null users (the most recommended pattern for collections).

### 2. Declarative Schema Definition (SDL)

```graphql
"""
Representa a conta de um usuário no sistema.
"""
type User implements Node {
  id: ID!
  name: String!
  email: String!
  role: UserRole!
  orders(first: Int = 10, after: String): OrderConnection!
  createdAt: DateTime!
}

"""
Padrão de Interface Node para identificação única global (padrão Relay).
"""
interface Node {
  id: ID!
}

enum UserRole {
  ADMIN
  CUSTOMER
  GUEST
}

"""
Entrada de dados para criação de novo usuário.
"""
input CreateUserInput {
  name: String!
  email: String!
  role: UserRole = CUSTOMER
}

type CreateUserPayload {
  user: User
  userErrors: [UserError!]!
}

type UserError {
  field: [String!]!
  message: String!
}

"""
Diretivas nativas e customizadas para alterar comportamentos de execução e validação.
"""
directive @auth(requires: UserRole = ADMIN) on FIELD_DEFINITION | OBJECT
```

---

## 🛠️ Defining Executable Operations (Queries, Mutations & Subscriptions)

### 1. Queries, Fragments, and Aliases
Use explicit variables, reusable fragments, and aliases to avoid collisions and optimize client-side payloads:

```graphql
query GetUserProfileWithOrders($userId: ID!, $orderLimit: Int!) {
  user(id: $userId) {
    ...BasicUserFields
    recentOrders: orders(first: $orderLimit) {
      edges {
        node {
          id
          totalAmount
          status
        }
      }
    }
  }
}

fragment BasicUserFields on User {
  id
  name
  email
  role
}
```

### 2. Mutations and Response Payload Design
Adopt the **Mutation Ingest Input / Payload Output** pattern:
- Mutations must accept a single input parameter (`input: CreateUserInput!`).
- Return a payload containing the created/modified entity and a declarative collection of domain errors (`userErrors`).

```graphql
mutation CreateNewCustomer($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
    userErrors {
      field
      message
    }
  }
}
```

### 3. Subscriptions (Real-Time Communication)
Implement reactive subscriptions over WebSocket/Server-Sent Events (SSE) to push event updates to the client:

```graphql
subscription OnOrderStatusUpdated($orderId: ID!) {
  orderStatusUpdated(orderId: $orderId) {
    id
    status
    updatedAt
  }
}
```

---

## ⚡ Resolver Architecture and N+1 Resolution (DataLoader)

### 1. Execution Model & Resolver Tree
Every field in GraphQL has a resolver. Resolvers receive four standard arguments: `(parent/root, args, context, info)`.

### 2. Preventing the N+1 Problem with DataLoader
Avoid firing multiple SQL/HTTP queries for associated collections by batching and caching requests (*batching and caching*) within the per-HTTP-request life cycle.

```typescript
import DataLoader from 'dataloader';

// Resolver delegando a busca para DataLoader no contexto por requisição
export const resolvers = {
  User: {
    orders: (parent, args, context) => {
      return context.loaders.ordersByUserId.load(parent.id);
    },
  },
};

// Instanciação do DataLoader no context da requisição
export function createLoaders(dbConnection) {
  return {
    ordersByUserId: new DataLoader(async (userIds: readonly string[]) => {
      const orders = await dbConnection.findOrdersByUserIds(userIds);
      // Mapeia os resultados garantindo a mesma ordem das chaves solicitadas
      return userIds.map(id => orders.filter(order => order.userId === id));
    }),
  };
}
```

---

## 📑 Standard Pagination (Relay Cursor Connections Specification)

Whenever you return extensive lists of data, use the **Relay Cursor Connections** specification to support efficient, infinite, bidirectional cursor-based pagination:

```graphql
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  cursor: String!
  node: Order!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## 🚨 Response Format and Strict Error Handling (GraphQL Spec)

The GraphQL specification defines a strict JSON response format made up of `data`, `errors`, and `extensions`:

```json
{
  "data": {
    "user": null
  },
  "errors": [
    {
      "message": "Acesso negado para visualização deste recurso",
      "locations": [
        {
          "line": 3,
          "column": 5
        }
      ],
      "path": ["user"],
      "extensions": {
        "code": "FORBIDDEN",
        "timestamp": "2026-08-07T14:30:00Z"
      }
    }
  ],
  "extensions": {
    "tracing": {
      "version": 1,
      "duration": 4500000
    }
  }
}
```

- **Null Error Bubbling**: If an error occurs in a field declared as Non-Null (`!`), the error propagates to the nearest nullable ancestor. Define fields defensively so small failures do not null out the entire `data` response tree.

---

## 🔒 Security, Introspection Protection, and Rate Limiting

1. **Query Depth Limiting**:
   - Limit the maximum nesting depth of queries (e.g., a maximum of 5 to 7 levels) to prevent DoS attacks with circular recursive queries.
2. **Query Cost Analysis**:
   - Assign a cost per field or collection and refuse execution if the cost exceeds the maximum allowed per request.
3. **Disabling Introspection in Production**:
   - Disable introspection queries (`__schema`, `__type`) in production environments to hide structural details of the internal model from an attacker.
4. **Persisted Queries (Automatic Persisted Queries - APQ)**:
   - Allow only execution of pre-approved SHA-256 query hashes in production to reduce bandwidth and block arbitrary requests.

---

## 🔗 Integration with Other Skills

- To design the full backend architecture and database integration, see [backend-developer](../../roles/backend-developer/SKILL.md) and [software-architect](../../roles/software-architect/SKILL.md).
- To integrate GraphQL clients in the Frontend with React or Vue, see [framework-react](../framework-react/SKILL.md) and [framework-vue](../framework-vue/SKILL.md).
- To audit GraphQL API security against the OWASP API Security Top 10, see [pentester-owasp-api-security-2023](../../security/appsec/pentester-owasp-api-security-2023/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
- To compare with or integrate other API styles, see [framework-rest-api](../framework-rest-api/SKILL.md), [framework-grpc](../framework-grpc/SKILL.md), and [framework-soap](../framework-soap/SKILL.md).
- For secure implementation in TypeScript or Python, see [lang-typescript](../../languages/lang-typescript/SKILL.md) and [lang-python](../../languages/lang-python/SKILL.md).
