---
name: "framework-react"
description: "Provides engineering and architecture patterns for the React library (React 18+ / React 19) and its ecosystem. Covers functional components, advanced Hooks, Server Components (RSC), state management (Context, Zustand, TanStack Query), routing, performance optimization, and testing."
---

# AI Skill: React Engineering and Architecture (framework-react)

This skill guides the AI to act as a specialist in the **React** library (versions 18 and 19) and its modern ecosystem, aligned with the official documentation maintained by Meta ([react.dev](https://react.dev/)). It covers functional component architecture, React Server Components (RSC), Hooks, global and server state management, render optimization, and testing.

---

## 🧭 Component Architecture and React Server Components (RSC)

### 1. Separation Between Server Components and Client Components
- **Server Components (RSC - Default in React 19 / Next.js App Router)**:
  - Components that run exclusively on the server with no JavaScript bundle sent to the client.
  - Ideal for direct database access, internal APIs, and heavy static/dynamic rendering.
- **Client Components (`'use client'`)**:
  - Components hydrated in the browser that use local state (`useState`), effects (`useEffect`), or DOM event listeners (`onClick`, `onChange`).

### 2. Fundamental and Advanced Hook Patterns
```tsx
import React, { useState, useTransition, useId } from 'react';

interface SearchBoxProps {
  onSearch: (query: string) => void;
}

export const SearchBox: React.FC<SearchBoxProps> = ({ onSearch }) => {
  const [input, setInput] = useState('');
  const [isPending, startTransition] = useTransition();
  const inputId = useId();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    
    // Atualização de baixa prioridade sem congelar a interface
    startTransition(() => {
      onSearch(value);
    });
  };

  return (
    <div className="search-container">
      <label htmlFor={inputId}>Buscar Produtos:</label>
      <input
        id={inputId}
        type="text"
        value={input}
        onChange={handleChange}
        placeholder="Digite para pesquisar..."
      />
      {isPending && <span className="spinner">Atualizando resultados...</span>}
    </div>
  );
};
```

---

## 🛠️ Global State and Server State Management

### 1. Server State vs. UI State
- **Server State**: Use **TanStack Query (React Query)** or **SWR** for caching, automatic background revalidation, pagination, and asynchronous mutations with optimistic rollback.
- **Global UI State (Client State)**:
  - For simple state: React Context API.
  - For complex, high-performance state: **Zustand** or **Jotai** (avoiding unnecessary re-renders of the whole tree).

---

## ⚡ Performance Optimization and Web Vitals Measurement

1. **Avoid Unwanted Re-renders**:
   - Keep state as close as possible to where it is used (*Lift state up* only when necessary).
   - Use automatic compilation from the **React Compiler** (React 19) or deliberate manual memoization with `useCallback` and `useMemo`.
2. **Code-Splitting and Lazy Loading**:
   - Import heavy components dynamically via `React.lazy()` wrapped in `<Suspense fallback={<Loading />}>`.

---

## 🧪 Testing Strategies

- **React Testing Library & Vitest/Jest**:
  - Test behaviors visible from the end user's point of view (using selectors such as `getByRole`, `getByText`) instead of testing internal state implementation details.

---

## 🔗 Integration with Other Skills

- For complete interface development with TypeScript and accessibility (WCAG), see [frontend-developer](../../roles/frontend-developer/SKILL.md) and [lang-typescript](../../languages/lang-typescript/SKILL.md).
- To automate component and web application test suites, see [framework-testing-javascript](../framework-testing-javascript/SKILL.md) and [qa-engineer](../../roles/qa-engineer/SKILL.md).
- For protection against web vulnerabilities (XSS, CSRF, Secure Headers), see [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
