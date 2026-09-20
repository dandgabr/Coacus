---
name: "framework-grpc"
description: "Provides engineering patterns for gRPC and Protocol Buffers (proto3). Covers unary and streaming RPCs (Server, Client, Bidirectional), .proto file definitions, HTTP/2 transport, interceptors (middlewares), rich google.rpc.Status error handling, and gRPC-Web."
---

# AI Skill: gRPC Engineering and Architecture (framework-grpc)

This skill guides the AI to act as a specialist in the high-performance RPC framework **gRPC** and the **Protocol Buffers (proto3)** IDL, aligned with the official CNCF and gRPC.io documentation ([grpc.io](https://grpc.io/)). It covers service contract modeling, bidirectional streaming, HTTP/2 transport, interceptors, error handling, and inter-service integration.

---

## 🧭 Contract Specification with Protocol Buffers (proto3)

### 1. `.proto` File Definition Standards
- Use the `syntax = "proto3";` syntax.
- Organize packages logically to avoid collisions (`package company.service.v1;`).
- Assign a unique, sequential numeric tag to fields (`1` through `15` consume only 1 byte in the varint field encoding).

```protobuf
syntax = "proto3";

package billing.v1;

import "google/protobuf/timestamp.proto";

option go_package = "github.com/empresa/billing/v1;billingv1";

service PaymentService {
  // RPC Unário
  rpc ProcessPayment (ProcessPaymentRequest) returns (ProcessPaymentResponse);
  
  // RPC de Streaming de Servidor
  rpc StreamTransactions (StreamTransactionsRequest) returns (stream TransactionEvent);
}

message ProcessPaymentRequest {
  string account_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
  PaymentMethod method = 4;
}

enum PaymentMethod {
  PAYMENT_METHOD_UNSPECIFIED = 0;
  PAYMENT_METHOD_CREDIT_CARD = 1;
  PAYMENT_METHOD_PIX = 2;
}

message ProcessPaymentResponse {
  string transaction_id = 1;
  string status = 2;
  google.protobuf.Timestamp processed_at = 3;
}

message StreamTransactionsRequest {
  string account_id = 1;
}

message TransactionEvent {
  string transaction_id = 1;
  int64 amount_cents = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

---

## 🛠️ Communication Patterns and HTTP/2 Transport

### 1. RPC Operating Modes
1. **Unary RPC**: The client sends a single request and receives a response.
2. **Server Streaming RPC**: The client sends a request and receives a continuous stream of messages.
3. **Client Streaming RPC**: The client sends a stream of messages and awaits a single final response from the server.
4. **Bidirectional Streaming RPC**: Client and server exchange independent streams of messages over the same multiplexed HTTP/2 connection.

### 2. Interceptors (Middlewares)
Use unary and streaming interceptors to:
- Authenticate and extract credentials via metadata headers (`metadata.MD`).
- Collect metrics and distributed tracing (OpenTelemetry / Jaeger).
- Recover from panics (*panic recovery*) and provide centralized call logging.

---

## 🚨 Rich Error Handling (`google.rpc.Status`)

Avoid using only raw gRPC codes (`codes.Internal`, `codes.InvalidArgument`). Return rich error payloads using the `google.rpc.Status` model:

```json
{
  "code": 3,
  "message": "Argumentos inválidos fornecidos para a transação",
  "details": [
    {
      "@type": "type.googleapis.com/google.rpc.BadRequest",
      "field_violations": [
        {
          "field": "amount_cents",
          "description": "O valor deve ser maior que zero"
        }
      ]
    }
  ]
}
```

---

## 🔗 Integration with Other Skills

- For high-performance inter-microservice communication architecture, see [backend-developer](../../roles/backend-developer/SKILL.md) and [software-architect](../../roles/software-architect/SKILL.md).
- To implement gRPC clients/servers in Go, Rust, or Python, see [lang-go](../../languages/lang-go/SKILL.md), [lang-rust](../../languages/lang-rust/SKILL.md), and [lang-python](../../languages/lang-python/SKILL.md).
- For transport-layer security and mTLS authentication in gRPC, see [network-security-onprem-cloud](../../security/operations/network-security-onprem-cloud/SKILL.md) and [auth-protocols-mfa](../../security/operations/auth-protocols-mfa/SKILL.md).
