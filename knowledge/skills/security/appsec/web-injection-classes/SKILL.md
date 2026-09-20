---
name: web-injection-classes
description: Acts as a specialist in web injection and client/server exploitation classes, covering SQL/NoSQL/LDAP/OS-command injection, XSS (reflected, stored, DOM), CSRF, SSRF, HTTP request smuggling, CRLF injection, insecure deserialization and prototype pollution, with prevention and detection guidance for each class.
metadata:
  type: defensive
  phase: weaponize
---

# Web Injection and Exploitation Classes

This skill guides the AI to identify, exploit-in-a-lab and remediate the injection and parsing classes that dominate web application incidents. It complements the risk ranking in the [owasp-top-10-2025](../owasp-top-10-2025/SKILL.md) skill with the concrete mechanics.

---

## 🧪 1. Injection Classes

### 1.1 SQL and NoSQL Injection
- **SQL**: user input concatenated into a query. Prevention is **parameterized queries or prepared statements**, never string escaping. Detection: error-based, boolean-based and time-based probes.
- **NoSQL**: object injection where a JSON body becomes an operator (for example, a `$ne` clause). Prevention is schema validation and type coercion at the boundary.

### 1.2 OS Command and Code Injection
- Never pass user input to a shell. Prefer a vetted library call over `exec`/`system`. Where a shell is unavoidable, use allowlists and argument arrays.
- **Code injection** includes template injection and dynamic evaluation; treat any evaluation of user-controlled content as remote code execution.

### 1.3 XSS (Cross-Site Scripting)
- **Reflected, stored and DOM-based**. Prevention is contextual output encoding plus a strict Content-Security-Policy with nonces; sanitize rich HTML with a vetted library on the server.
- DOM XSS lives entirely in the browser: audit sinks such as `innerHTML`, `eval` and `location` assignment.

### 1.4 CSRF (Cross-Site Request Forgery)
- Use SameSite cookies, per-session anti-CSRF tokens, and origin/Referer checks on state-changing requests.
- Token-bound APIs and custom headers reduce exposure but do not replace server-side authorization.

### 1.5 SSRF (Server-Side Request Forgery)
- An attacker makes the server issue a request to an internal or metadata endpoint.
- Prevention: allowlist destinations, block link-local and private ranges, disable redirects, and require IMDSv2-style authenticated metadata. SSRF in the cloud frequently escalates to credential theft.

### 1.6 HTTP Request Smuggling
- Arises from disagreement between front-end and back-end parsers over `Content-Length` and `Transfer-Encoding`. Prevention is a normalized, hardened proxy and rejection of ambiguous framing.

### 1.7 CRLF Injection and Header Injection
- Unsanitized input in headers or redirects enables response splitting and cache poisoning. Strip CR/LF from any value that reaches a header.

### 1.8 Insecure Deserialization
- Native deserialization of untrusted data enables gadget-chain execution. Prefer data-only formats (JSON) with schemas; where native serialization is required, enforce allowlists and sign the payload.

### 1.9 Prototype Pollution (JavaScript)
- Writing to `__proto__` or `constructor.prototype` via a deep-merge or recursive parser poisons the prototype chain, enabling universal gadgets and, in Node.js, remote code execution.
- Prevention: reject `__proto__`/`constructor`/`prototype` keys in merge and parse routines, prefer `Object.create(null)` or `Map`, freeze prototypes, and keep dependencies patched. Academic work such as *Silent Spring* and *GHunter* demonstrates multiple real RCEs via this class.

---

## 🛡️ 2. Cross-Cutting Prevention Rules

1. Validate and canonicalize input at every trust boundary; encode output in the correct context.
2. Run with least privilege so a single injection cannot reach the whole system.
3. Centralize query construction, templating and HTTP client logic in vetted helpers.
4. Add detection rules for injection payloads and anomalous outbound requests; log and alert on them.

---

## 🔗 3. Integration with Other Skills

- For API and protocol-specific surfaces, see the [api-protocol-security](../api-protocol-security/SKILL.md) skill.
- For static verification of these classes in code, see the [sast-code-review](../sast-code-review/SKILL.md) skill.
- For dynamic testing, see the [dast-application-testing](../dast-application-testing/SKILL.md) skill.
