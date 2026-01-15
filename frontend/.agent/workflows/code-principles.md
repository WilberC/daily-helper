---
description: Frontend Code Principles and Architecture Guidelines
---

# Frontend Code Principles

This document outlines core coding principles and architectural guidelines for the Daily Helper frontend.

## Core Principles

### 1. **Type Safety First**

Always use TypeScript types. No `any` types unless absolutely necessary.

```typescript
// ✅ Good: Explicit types
interface User {
  id: string
  name: string
  email: string
}

const user: User = { id: '1', name: 'John', email: 'john@example.com' }

// ❌ Bad: Using 'any'
const user: any = { ... }
```

### 2. **Composition Over Inheritance**

Favor composables and component composition over complex inheritance.

```typescript
// ✅ Good: Composable
export function useUserData() {
  const user = ref<User | null>(null)
  const loading = ref(false)

  const fetchUser = async (id: string) => {
    loading.value = true
    user.value = await api.getUser(id)
    loading.value = false
  }

  return { user, loading, fetchUser }
}

// Usage
const { user, loading, fetchUser } = useUserData()
```

### 3. **Single Responsibility**

Each function, component, and file should have one clear purpose.

```typescript
// ✅ Good: Focused functions
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function formatDate(date: Date): string {
  return date.toLocaleDateString()
}

// ❌ Bad: Kitchen sink function
function processUser(user: any) {
  // Validates email
  // Formats name
  // Saves to database
  // Sends email
  // Updates UI
}
```

### 4. **Immutability**

Avoid mutating data. Create new objects/arrays instead.

```typescript
// ✅ Good: Immutable update
const updatedUsers = users.value.map((user) =>
  user.id === targetId ? { ...user, name: newName } : user,
)

// ❌ Bad: Direct mutation
users.value[0].name = newName
```

### 5. **Explicit Over Implicit**

Be explicit about intent. Avoid magic values and unclear logic.

```typescript
// ✅ Good: Clear intent
const MAX_LOGIN_ATTEMPTS = 3
if (loginAttempts >= MAX_LOGIN_ATTEMPTS) {
  lockAccount()
}

// ❌ Bad: Magic number
if (loginAttempts >= 3) {
  lockAccount()
}
```

## File Organization

### Directory Structure

```
src/
├── assets/           # Static assets (images, styles)
├── components/       # Vue components
│   ├── common/      # Reusable components
│   ├── layout/      # Layout components
│   └── [feature]/   # Feature-specific components
├── composables/      # Reusable composition functions
├── config/           # Configuration files
├── graphql/          # GraphQL queries, mutations, fragments
├── router/           # Vue Router configuration
├── stores/           # Pinia stores
├── types/            # TypeScript type definitions
├── utils/            # Utility functions
├── views/            # Page-level components
├── App.vue           # Root component
└── main.ts           # Application entry point
```

### File Naming Conventions

```
Components:     PascalCase.vue       (UserProfile.vue)
Composables:    camelCase.ts         (useAuth.ts)
Stores:         camelCase.ts         (userStore.ts)
Utils:          camelCase.ts         (formatDate.ts)
Types:          PascalCase.ts        (User.ts)
Views:          PascalCase.vue       (Dashboard.vue)
```

## TypeScript Guidelines

### Interface vs Type

Use `interface` for object shapes, `type` for unions and primitives:

```typescript
// ✅ Interface for objects
interface User {
  id: string
  name: string
}

// ✅ Type for unions
type Status = 'pending' | 'active' | 'inactive'
type Result = Success | Error

// ✅ Type for primitives
type UserId = string
type Count = number
```

### Avoid Type Assertions

```typescript
// ❌ Bad: Type assertion
const user = data as User

// ✅ Good: Type guard
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data && 'name' in data
}

if (isUser(data)) {
  // TypeScript knows data is User here
}
```

### Generics for Reusability

```typescript
// Reusable async function
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url)
  return response.json() as T
}

// Usage
const users = await fetchData<User[]>('/api/users')
```

## Composables

### Composable Structure

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  // State
  const count = ref(initialValue)

  // Computed
  const doubled = computed(() => count.value * 2)

  // Methods
  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => (count.value = initialValue)

  // Return public API
  return {
    count: readonly(count),
    doubled,
    increment,
    decrement,
    reset,
  }
}
```

### When to Create a Composable

Create a composable when:

- Logic is reused across multiple components
- Complex stateful logic needs to be abstracted
- You need to share reactive state without Pinia

Examples: `useAuth`, `useToast`, `usePagination`, `useDebounce`

## State Management (Pinia)

### Store Structure

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])

  // Getters
  const isAuthenticated = computed(() => currentUser.value !== null)
  const userCount = computed(() => users.value.length)

  // Actions
  async function fetchUsers() {
    const response = await fetch('/api/users')
    users.value = await response.json()
  }

  function setCurrentUser(user: User) {
    currentUser.value = user
  }

  function logout() {
    currentUser.value = null
  }

  return {
    // State
    currentUser,
    users,

    // Getters
    isAuthenticated,
    userCount,

    // Actions
    fetchUsers,
    setCurrentUser,
    logout,
  }
})
```

### Store Best Practices

1. **Use setup syntax** (composition API style)
2. **Don't access stores directly in components** - use computed or destructure
3. **Keep stores focused** - one store per domain
4. **Actions should be async** - handle errors within actions

```typescript
// ✅ Good: Use computed
const userStore = useUserStore()
const user = computed(() => userStore.currentUser)

// ❌ Bad: Direct access in template
{
  {
    userStore.currentUser.name
  }
}
```

## GraphQL

### Query Organization

```typescript
// graphql/queries/users.ts
import { gql } from '@urql/vue'

export const GET_USERS = gql`
  query GetUsers($limit: Int, $offset: Int) {
    users(limit: $limit, offset: $offset) {
      id
      name
      email
      createdAt
    }
  }
`

export const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      role
      profile {
        bio
        avatar
      }
    }
  }
`
```

### Using Queries in Components

```vue
<script setup lang="ts">
import { useQuery } from '@urql/vue'
import { GET_USERS } from '@/graphql/queries/users'

const { data, fetching, error } = useQuery({
  query: GET_USERS,
  variables: { limit: 10, offset: 0 },
})

const users = computed(() => data.value?.users ?? [])
</script>

<template>
  <LoadingSpinner v-if="fetching" />
  <ErrorMessage v-else-if="error" :error="error" />
  <UserList v-else :users="users" />
</template>
```

### Mutations

```typescript
// graphql/mutations/users.ts
import { gql } from '@urql/vue'

export const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
    }
  }
`
```

```vue
<script setup lang="ts">
import { useMutation } from '@urql/vue'
import { CREATE_USER } from '@/graphql/mutations/users'

const { executeMutation: createUser } = useMutation(CREATE_USER)

const handleSubmit = async (formData: CreateUserInput) => {
  const result = await createUser({ input: formData })

  if (result.error) {
    toast.add({ severity: 'error', summary: 'Error creating user' })
  } else {
    toast.add({ severity: 'success', summary: 'User created' })
  }
}
</script>
```

## Error Handling

### Try-Catch Pattern

```typescript
async function fetchUserData(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Failed to fetch user:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load user data',
    })
    throw error
  }
}
```

### Validation Errors

```typescript
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(8, 'Password must be at least 8 characters'),
})

try {
  await schema.validate(formData, { abortEarly: false })
} catch (error) {
  if (error instanceof yup.ValidationError) {
    const errors = error.inner.reduce(
      (acc, err) => {
        if (err.path) acc[err.path] = err.message
        return acc
      },
      {} as Record<string, string>,
    )

    // Set form errors
  }
}
```

## Performance

### Lazy Loading Routes

```typescript
// router/index.ts
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue'),
  },
  {
    path: '/users',
    component: () => import('@/views/Users.vue'),
  },
]
```

### Debouncing

```typescript
import { ref, watch } from 'vue'
import { debounce } from 'lodash-es'

const searchQuery = ref('')
const debouncedSearch = debounce((query: string) => {
  performSearch(query)
}, 300)

watch(searchQuery, (newQuery) => {
  debouncedSearch(newQuery)
})
```

### Virtual Scrolling for Long Lists

```vue
<script setup lang="ts">
import VirtualScroller from 'primevue/virtualscroller'
</script>

<template>
  <VirtualScroller :items="largeList" :itemSize="50" class="h-96">
    <template #item="{ item }">
      <div class="p-4">{{ item.name }}</div>
    </template>
  </VirtualScroller>
</template>
```

## Testing

### Unit Tests

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UserProfile from './UserProfile.vue'

describe('UserProfile', () => {
  it('displays user name', () => {
    const wrapper = mount(UserProfile, {
      props: {
        user: { id: '1', name: 'John Doe', email: 'john@example.com' },
      },
    })

    expect(wrapper.text()).toContain('John Doe')
  })

  it('emits edit event when button clicked', async () => {
    const wrapper = mount(UserProfile, {
      props: { user: mockUser },
    })

    await wrapper.find('[data-testid="edit-button"]').trigger('click')

    expect(wrapper.emitted('edit')).toBeTruthy()
  })
})
```

### Testing Composables

```typescript
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments count', () => {
    const { count, increment } = useCounter()

    expect(count.value).toBe(0)
    increment()
    expect(count.value).toBe(1)
  })
})
```

## Code Quality

### ESLint Rules

Follow the project's ESLint configuration:

- Run `npm run lint` before committing
- Fix auto-fixable issues with `npm run lint:fix`

### Prettier Formatting

- Run `npm run format` to format code
- Configure your editor to format on save

### Code Review Checklist

- [ ] No TypeScript errors (`npm run type-check`)
- [ ] No ESLint errors (`npm run lint`)
- [ ] Code is formatted (`npm run format`)
- [ ] All tests pass (`npm run test:unit`)
- [ ] Component has proper types
- [ ] Dark mode styles included
- [ ] Accessibility attributes added
- [ ] No console.log statements
- [ ] Error handling implemented
- [ ] Loading states handled

## Git Commit Messages

Follow conventional commits:

```
feat: add user profile page
fix: resolve login redirect issue
docs: update component documentation
style: format code with prettier
refactor: extract user validation logic
test: add tests for user store
chore: update dependencies
```

## Resources

- [Vue 3 Style Guide](https://vuejs.org/style-guide/)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- [Pinia Best Practices](https://pinia.vuejs.org/cookbook/)
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript)
