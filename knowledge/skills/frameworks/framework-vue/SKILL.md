---
name: "framework-vue"
description: "Provides modular, high-performance development patterns using the Vue 3 ecosystem, covering the Composition API, TypeScript, Pinia, Vue Router, and reactivity optimizations."
---

# AI Skill: Vue.js Engineering (Vue Specialist)

This skill guides the AI to act as a specialist in developing modern, reactive web applications using the **Vue 3** ecosystem. Its main goal is to guide the AI and developers to design reusable components, manage state efficiently with Pinia, and apply the Composition API in a performant, typed way.

---

## 🧭 Vue 3 Development Guidelines

When working in this skill, guide code development by the following practices:

### 1. Composition API & `<script setup>`
- **Standard Practice**: Always use the Composition API with the `<script setup>` syntax, since it is cleaner, more performant, and has superior native support for TypeScript typing.
- **Clear Reactivity**: Use `ref` for isolated reactive primitive data and `reactive` exclusively for complex objects or cohesive component-internal state.
- **Computed vs Watch**:
  - Use `computed` to derive or transform state synchronously with automatic native caching.
  - Use `watch` or `watchEffect` only for asynchronous side effects or external imperative work (e.g., API calls, saving to localStorage).

### 2. Global State Management with Pinia
- **Pinia Stores**: Replace the old Vuex with Pinia. Define focused, modular stores (e.g., `useAuthStore`, `useCartStore`) using the Setup syntax (with `ref` and `computed`) to stay consistent with the Composition API.
- **Safe Destructuring**: Never destructure reactive store properties directly without using Pinia's `storeToRefs`, to avoid breaking Vue's native reactivity.

### 3. Vue Performance Optimization
- **Component Life Cycle**: Clean up manual event listeners (`window.addEventListener`), timers (`setInterval`), or Websocket connections in the `onUnmounted` or `onBeforeUnmount` hooks to avoid memory leaks.
- **List Virtualization**: For extensive lists (more than 100 items), prefer DOM virtualization techniques (e.g., `vue-virtual-scroller`) instead of rendering every element with `v-for`.
- **v-if vs v-show**: Use `v-if` when toggling is rare (avoiding rendering the node in the DOM) and `v-show` when the element toggles visibility frequently.

---

## 🛠️ Recommended Code Patterns (Integrated TypeScript)

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Definição de Props tipadas estritamente
const props = defineProps<{
  title: string;
  initialCount?: number;
}>();

// Definição de Emits tipados
const emit = defineEmits<{
  (e: 'update', count: number): void;
}>();

// Estados reativos
const count = ref(props.initialCount ?? 0);

// Estado derivado reativo (Computed)
const doubledCount = computed(() => count.value * 2);

function increment() {
  count.value++;
  emit('update', count.value);
}
</script>

<template>
  <div class="counter-card">
    <h3>{{ title }}</h3>
    <p>Contador: {{ count }} (Dobro: {{ doubledCount }})</p>
    <button @click="increment">Incrementar</button>
  </div>
</template>

<style scoped>
.counter-card {
  padding: 1rem;
  border-radius: 8px;
  background: var(--bg-surface);
}
</style>
```

---

## 🔗 Integration with Other Skills
- [frontend-developer](../../roles/frontend-developer/SKILL.md): Uses the Vue guidelines to orchestrate components and implement the project's visual Design System.
- [tech-typescript](../../languages/lang-typescript/SKILL.md): Provides the structural types that validate Vue props and stores.
