---
name: web-portal-cli-scaffolding
description: >-
  Provides end-to-end patterns to reverse-engineer public web portals into zero-dependency agent CLIs. Use when building standalone command-line tools from web portals, APIs, RSS feeds, or HTML listings for automated consumption by agents.
---

# Web Portal CLI Scaffolding

This skill establishes the engineering pattern for reverse-engineering public web portals into self-contained, zero-dependency command-line utilities optimized for autonomous AI agent tool use.

---

## 🎯 1. Reconnaissance-First Portal Classification

Before authoring code or scrapers, systematically inspect the portal using passive network tools (curl or browser inspection) and classify its data surface in order of architectural preference:

| Priority | Strategy | Source Indicator | Reliability | Action |
|:---|:---|:---|:---|:---|
| **1 (Highest)** | **Public / Internal REST / XHR JSON API** | Network inspection reveals `api.domain.com`, `/wp-json/`, or query endpoints returning clean JSON. | High | Query the JSON endpoint directly with appropriate headers; avoids HTML parsing entirely. |
| **2** | **RSS / Atom / XML Feed** | Discoverable `<link rel="alternate" type="application/rss+xml">` or standard feed paths (`/feed`, `/rss.xml`). | High | Parse structured XML elements deterministically without DOM scraping. |
| **3** | **Embedded JSON-LD** | Pages embedding `<script type="application/ld+json">` containing structured schema (e.g. `JobPosting`, `Article`). | Medium-High | Extract the JSON-LD script tag from SSR HTML and deserialize directly. |
| **4** | **Deterministic Server-Side Rendered (SSR) HTML** | Predictable HTML markup with stable CSS classes, IDs, or semantic article cards rendered on initial GET. | Medium | Apply chunked HTML parsing with strict per-card error boundaries. |
| **5 (Rejected)** | **Client-Side Heavy SPA / CAPTCHA / Wall** | Pages requiring JavaScript bundle hydration, Cloudflare turnstiles, or mandatory user authentication. | Low | **Reject automated CLI scaffolding.** Flag domain as requiring manual browser interaction or a sanctioned commercial API. |

---

## 📐 2. Standardized Zero-Dependency Agent CLI Contract

Every portal CLI must operate as an agnostic executable (Python standard library or TypeScript with Bun runtime) with zero external runtime package dependencies.

### Command Surface
Support two fundamental subcommands:
1. `search <keywords> [options]` — Queries portal listings by keyword, location, date range, or category.
2. `detail <id-or-url> [options]` — Retrieves full structured attributes for a specific entity.

### Output Formatting
Every command must accept `--format <json|table|plain>` (defaulting to `json` for agent consumption):
- **`json` (Machine format)**: Emits a single unfragmented JSON object on standard output.
- **`table` (Interactive format)**: Emits a human-readable ASCII table truncated to terminal width.
- **`plain` (Pipeline format)**: Emits line-delimited key-value or TSV streams for shell piping.

### Standardized JSON Envelopes

**Success Envelope (stdout, exit code 0):**
```json
{
  "meta": {
    "portal": "portal-identifier",
    "query": "search query terms",
    "total": 142,
    "returned": 20,
    "page": 1,
    "totalPages": 8,
    "retrievedAt": "2026-10-22T18:00:00Z"
  },
  "results": [
    {
      "id": "item-12345",
      "title": "Senior Systems Engineer",
      "url": "https://example.com/items/item-12345",
      "date": "2026-10-20",
      "summary": "Brief description..."
    }
  ]
}
```

**Error Envelope (stderr, exit code 1):**
```json
{
  "error": {
    "code": "RATE_LIMITED | NOT_FOUND | PARSE_ERROR | MISSING_CREDENTIALS",
    "message": "Human-actionable diagnosis of the issue"
  }
}
```

### Credentials & Security Guardrails
- **Environment variables only:** Read required API keys or tokens strictly from environment variables (e.g. `{env:PORTAL_API_KEY}`). Never accept tokens via CLI argument flags, which leak into shell history and system process listings (`ps aux`).
- If credentials are required but missing, emit error code `MISSING_CREDENTIALS` on stderr and exit with code 1.

---

## 🛡️ 3. Resilient Scraping Architecture

When scraping SSR HTML or unstructured responses:

1. **Chunked Card Parsing (Isolate Card Failures)**:
   - Partition raw HTML into distinct card strings based on repeating container boundaries.
   - Parse each card inside an independent try/catch block.
   - If a single card has malformed markup or missing fields, log a debug warning and continue processing remaining cards; a single broken item must never crash the entire batch.
2. **Exponential Backoff with Jitter on 429/5xx**:
   - Enforce an internal polite rate limit (maximum 1 request per second).
   - Upon encountering `HTTP 429 Too Many Requests` or `5xx Server Error`, retry with exponential backoff and randomized jitter (e.g. 2s, 4s, 8s + random delay up to 500ms), up to a maximum of 3 attempts before returning an error.
3. **Honest User-Agent & robots.txt Compliance**:
   - State an informative User-Agent header (e.g. `CustomPortalCLI/1.0 (+https://github.com/company/repo)`).
   - Check `robots.txt` before crawling or executing recurring fetches.

---

## 🧪 4. Offline Contract Testing with Reject-Network Guard

To guarantee that CLI unit tests can run reliably in hermetic CI/CD pipelines without making outbound network requests:

1. **Recorded Fixture Replay**:
   - Save representative HTML/JSON responses as test fixtures (`tests/fixtures/sample_search.json`, `sample_detail.html`).
2. **Network Rejection Guard (`reject-network`)**:
   - Test suites must install a socket/fetch monkeypatch that immediately throws an assertion error if any test attempts to establish a real external network connection.
3. **Mandatory Live Smoke Test**:
   - Before activating a newly scaffolded portal CLI in an agent repository, execute an interactive one-shot smoke query against the live target to verify that current selectors and endpoints remain intact.
