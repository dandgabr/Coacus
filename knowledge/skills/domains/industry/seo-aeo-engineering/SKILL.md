---
name: seo-aeo-engineering
description: "Provides Search Engine Optimization (SEO), Answer Engine Optimization (AEO/GEO), structured data (Schema.org JSON-LD), technical web architecture, and LLM search discovery based on Google Search Essentials, Schema.org, and llms.txt. Use when auditing site indexing, structuring technical metadata, optimizing Core Web Vitals for search, authoring machine-readable schemas, or designing content for AI answer engines."
---

# Search & Answer Engine Optimization Engineering (SEO & AEO)

Unify technical web architecture, machine-readable structured data (Schema.org JSON-LD), crawl budget management, and Generative Engine Optimization (GEO) for AI search platforms.

---

## 🏗️ 1. Technical Search Architecture & Crawlability (Google Search Essentials)

A site that cannot be efficiently fetched and rendered by search engine spiders cannot rank.

### A. The 5 Pillars of Technical SEO:
1. **Canonicalization & URL Hygiene (RFC 3986):**
   - Enforce canonical links on every page: `<link rel="canonical" href="https://example.com/canonical-path" />`.
   - Prevent duplicate indexation caused by tracking parameters (`utm_*`, `ref`), trailing slash variants, or HTTP vs. HTTPS mismatches.
2. **Server-Side Rendering (SSR) & Dynamic Hydration:**
   - Search crawlers render JavaScript using headless Chromium, but assign it a secondary, deferred processing queue (*two-wave indexing*).
   - Critical text, headings (`<h1>`–`<h3>`), schema metadata, and internal links MUST be present in initial server-rendered HTML.
3. **Robots Protocol & Crawl Directives (RFC 9309):**
   - Clear `robots.txt` directives separating public indexing routes from administrative/staging paths.
   - Use meta robots tags `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />`.
4. **XML Sitemaps Architecture:**
   - Keep sitemaps under 50,000 URLs and 50MB uncompressed; split into index sitemaps (`sitemap_index.xml`) for large catalogs.
   - Include only canonical, 200-OK pages; purge 301 redirects, 404s, and noindex pages from sitemaps.
5. **Core Web Vitals Optimization (Search Ranking Signals):**
   - **LCP (Largest Contentful Paint):** $\le 2.5\text{s}$ (pre-load critical hero images, self-host critical fonts, eliminate render-blocking CSS).
   - **INP (Interaction to Next Paint):** $\le 200\text{ms}$ (avoid heavy main-thread JavaScript tasks; yield to the compositor).
   - **CLS (Cumulative Layout Shift):** $\le 0.1$ (explicit `width` and `height` attributes on all images and embeds; reserve space for dynamic ads/banners).

---

## 🏷️ 2. Machine-Readable Structured Data (Schema.org JSON-LD)

Structure content to power rich snippets, knowledge graph cards, and AI answer engine extraction:

### Standard Technical Schemas:

#### SoftwareApplication / Developer Tool:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Coacus AI Suite",
  "operatingSystem": "All",
  "applicationCategory": "DeveloperApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "ratingCount": "128"
  }
}
</script>
```

#### TechArticle / Documentation:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "High-Performance Vector Indexing Architecture",
  "datePublished": "2026-05-12T08:00:00Z",
  "dateModified": "2026-10-15T12:00:00Z",
  "author": {
    "@type": "Organization",
    "name": "Engineering Team"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Coacus",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "description": "Comprehensive engineering guide on HNSW indexing and memory budgets."
}
</script>
```

---

## 🤖 3. Answer Engine Optimization (AEO / GEO / Perplexity / ChatGPT Search)

Generative AI search engines (Perplexity, ChatGPT Search, Claude Search, Google AI Overviews) synthesize answers by aggregating semantically dense passages from authoritative citations.

### A. The Inverted Pyramid & Direct-Answer Formatting
- **The First Sentence Rule:** The first sentence beneath any major heading (`<h2>`/`<h3>`) must provide a standalone, factually complete answer to the query without conversational preamble.
- **Syntactic Density:** Answer engines favor concise definition blocks ($40$–$60$ words) formatted as:
  - Definition sentences: *"[Term] is a [category] that [differentiating capability] by [mechanism]."*
  - Structured comparative tables and ordered procedural steps.

### B. The `llms.txt` and Markdown Feed Standard
To allow LLM crawlers to ingest clean, token-efficient technical documentation without HTML parsing overhead:
- Expose a `/llms.txt` manifest at the domain root adhering to the standard specification:
  - Title and brief summary of the project/product.
  - Curated, ordered markdown links to canonical documentation files.
  - Pointers to comprehensive markdown extracts (`/llms-full.txt`).

---

## 🔍 4. Programmatic Content & Internal Linking Topology

1. **Topical Hub-and-Spoke (Pillar Clusters):**
   - **Pillar Page:** Broad, high-level comprehensive guide targeting short-tail keyword volume.
   - **Cluster Spoke Pages:** Deep, highly specific technical articles answering long-tail queries.
   - **Bi-Directional Internal Links:** Every spoke page links back to the pillar page using descriptive anchor text; the pillar links to all cluster spokes.
2. **Descriptive Anchor Text Discipline:**
   - Never use generic anchor text (`click here`, `read more`, `source`).
   - Use semantically descriptive anchor text that names the exact destination concept (e.g. `read the database sharding architecture guide`).

---

## 📚 References & Standards

- Google Search Central. *Google Search Essentials & Technical Documentation*, 2026.
- W3C & Schema.org Consortium. *Schema.org Core Vocabulary Specification*, 2026.
- IETF. *RFC 9309: Robots Exclusion Protocol*, 2022.
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2 / Core Web Vitals*, 2024.
