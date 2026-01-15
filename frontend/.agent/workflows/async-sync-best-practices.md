---
description: Best practices for async/sync in Strawberry GraphQL with Django
---

# Async/Sync Best Practices

This guide covers best practices for handling asynchronous and synchronous code when working with the Daily Helper backend GraphQL API.

## GraphQL Query Patterns

### Using URQL Client

The frontend uses URQL (Universal React Query Library) for Vue to handle GraphQL requests.

```typescript
import { useQuery, useMutation } from '@urql/vue'
import { computed } from 'vue'

// Query
const { data, fetching, error, executeQuery } = useQuery({
  query: GET_USERS_QUERY,
  variables: { limit: 10 },
})

// Access reactive data
const users = computed(() => data.value?.users ?? [])

// Mutation
const { executeMutation } = useMutation(CREATE_USER_MUTATION)

const createUser = async (input: CreateUserInput) => {
  const result = await executeMutation({ input })
  return result
}
```

### Query Best Practices

#### 1. **Always Handle Loading States**

```vue
<script setup lang="ts">
const { data, fetching, error } = useQuery({ query: GET_DATA })
</script>

<template>
  <LoadingSpinner v-if="fetching" />
  <ErrorState v-else-if="error" :error="error" />
  <DataDisplay v-else :data="data" />
</template>
```

#### 2. **Use Computed for Derived Data**

```typescript
// ✅ Good: Reactive computed value
const users = computed(() => data.value?.users ?? [])
const userCount = computed(() => users.value.length)

// ❌ Bad: Direct access (not reactive)
const users = data.value?.users ?? []
```

#### 3. **Handle Null/Undefined Gracefully**

```typescript
// ✅ Good: Defensive access with fallbacks
const userName = computed(() => data.value?.user?.name ?? 'Unknown')
const items = computed(() => data.value?.items ?? [])

// ❌ Bad: Assumes data exists
const userName = data.value.user.name // Can crash!
```

## Mutations

### Mutation Patterns

```typescript
import { useMutation } from '@urql/vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const { executeMutation: createUser } = useMutation(CREATE_USER_MUTATION)

const handleCreateUser = async (formData: CreateUserInput) => {
  try {
    const result = await createUser({ input: formData })

    if (result.error) {
      throw new Error(result.error.message)
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'User created successfully',
    })

    return result.data
  } catch (error) {
    console.error('Failed to create user:', error)

    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error instanceof Error ? error.message : 'Failed to create user',
    })

    throw error
  }
}
```

### Optimistic Updates

For better UX, update the UI immediately before the server responds:

```typescript
const { executeMutation } = useMutation(DELETE_USER_MUTATION)

const deleteUser = async (userId: string) => {
  // Optimistically remove from local state
  users.value = users.value.filter((u) => u.id !== userId)

  try {
    const result = await executeMutation({ id: userId })

    if (result.error) {
      // Revert on error
      await refetchUsers()
      throw new Error(result.error.message)
    }

    toast.add({ severity: 'success', summary: 'User deleted' })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Failed to delete user' })
    throw error
  }
}
```

## Polling & Real-time Updates

### Polling Strategy

```typescript
import { useQuery } from '@urql/vue'

// Poll every 30 seconds
const { data, fetching } = useQuery({
  query: GET_NOTIFICATIONS,
  requestPolicy: 'network-only',
  context: {
    pollInterval: 30000, // 30 seconds
  },
})
```

### Manual Refetch

```typescript
const { data, executeQuery } = useQuery({
  query: GET_USERS,
  pause: true, // Don't auto-execute
})

// Fetch manually
const loadUsers = () => {
  executeQuery({ requestPolicy: 'network-only' })
}

// Fetch on mount
onMounted(() => {
  loadUsers()
})
```

## Error Handling

### GraphQL Error Types

```typescript
interface GraphQLError {
  message: string
  path?: string[]
  extensions?: {
    code?: string
    [key: string]: any
  }
}

const handleGraphQLError = (error: CombinedError) => {
  if (error.networkError) {
    // Network issue
    toast.add({
      severity: 'error',
      summary: 'Network Error',
      detail: 'Please check your internet connection',
    })
  } else if (error.graphQLErrors.length > 0) {
    // GraphQL errors
    error.graphQLErrors.forEach((err) => {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: err.message,
      })
    })
  }
}
```

### Retry Logic

```typescript
const { data, error, executeQuery } = useQuery({
  query: GET_DATA,
  requestPolicy: 'network-only',
})

const retryFetch = async (maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    const result = await executeQuery()

    if (!result.error) {
      return result
    }

    // Wait before retry (exponential backoff)
    await new Promise((resolve) => setTimeout(resolve, 1000 * Math.pow(2, i)))
  }

  throw new Error('Max retries exceeded')
}
```

## Concurrent Requests

### Parallel Queries

```typescript
import { useQuery } from '@urql/vue'

// Execute queries in parallel
const usersQuery = useQuery({ query: GET_USERS })
const postsQuery = useQuery({ query: GET_POSTS })
const commentsQuery = useQuery({ query: GET_COMMENTS })

const isLoading = computed(
  () => usersQuery.fetching.value || postsQuery.fetching.value || commentsQuery.fetching.value,
)

const hasError = computed(
  () => usersQuery.error.value || postsQuery.error.value || commentsQuery.error.value,
)
```

### Sequential Queries (Dependencies)

```typescript
import { ref, watch } from 'vue'

const userId = ref<string | null>(null)

// First query
const { data: userData } = useQuery({
  query: GET_USER,
  variables: { id: userId },
})

// Second query depends on first
const { data: postsData } = useQuery({
  query: GET_USER_POSTS,
  variables: computed(() => ({ userId: userData.value?.user?.id })),
  pause: computed(() => !userData.value?.user?.id), // Wait for user data
})
```

## Request Caching

### Cache Policies

```typescript
// Default: Use cache, then network
const { data } = useQuery({
  query: GET_USERS,
  requestPolicy: 'cache-first',
})

// Always fetch fresh data
const { data } = useQuery({
  query: GET_LIVE_DATA,
  requestPolicy: 'network-only',
})

// Cache only (offline)
const { data } = useQuery({
  query: GET_STATIC_DATA,
  requestPolicy: 'cache-only',
})

// Cache, then network in background
const { data } = useQuery({
  query: GET_FEED,
  requestPolicy: 'cache-and-network',
})
```

### Invalidate Cache

```typescript
import { useClient } from '@urql/vue'

const client = useClient()

// Clear specific query from cache
const invalidateUsers = () => {
  client.reexecuteOperation({
    key: 'users-query-key',
    context: { requestPolicy: 'network-only' },
  })
}

// Clear all cache
const clearCache = () => {
  client.cache.clear()
}
```

## Debouncing & Throttling

### Debounced Search

```typescript
import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'

const searchQuery = ref('')
const debouncedQuery = ref('')

const debouncedSearch = useDebounceFn((value: string) => {
  debouncedQuery.value = value
}, 300)

watch(searchQuery, (newValue) => {
  debouncedSearch(newValue)
})

// Query uses debounced value
const { data } = useQuery({
  query: SEARCH_USERS,
  variables: computed(() => ({ query: debouncedQuery.value })),
  pause: computed(() => !debouncedQuery.value),
})
```

### Throttled Updates

```typescript
import { useThrottleFn } from '@vueuse/core'

const handleScroll = useThrottleFn(() => {
  // Handle scroll event
  loadMore()
}, 1000) // Max once per second
```

## Pagination

### Offset-based Pagination

```typescript
import { ref, computed } from 'vue'

const page = ref(1)
const pageSize = ref(10)

const { data, fetching } = useQuery({
  query: GET_USERS,
  variables: computed(() => ({
    limit: pageSize.value,
    offset: (page.value - 1) * pageSize.value,
  })),
})

const totalPages = computed(() => Math.ceil((data.value?.usersCount ?? 0) / pageSize.value))

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
  }
}
```

### Cursor-based Pagination

```typescript
const cursor = ref<string | null>(null)

const { data, fetching } = useQuery({
  query: GET_POSTS,
  variables: computed(() => ({
    first: 20,
    after: cursor.value,
  })),
})

const hasNextPage = computed(() => data.value?.posts?.pageInfo?.hasNextPage ?? false)

const loadMore = () => {
  cursor.value = data.value?.posts?.pageInfo?.endCursor
}
```

## Form Submissions

### Async Form Handling

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useMutation } from '@urql/vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const isSubmitting = ref(false)
const { executeMutation: createUser } = useMutation(CREATE_USER)

const formData = ref({
  name: '',
  email: '',
})

const handleSubmit = async () => {
  isSubmitting.value = true

  try {
    const result = await createUser({ input: formData.value })

    if (result.error) {
      throw new Error(result.error.message)
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'User created successfully',
    })

    // Reset form
    formData.value = { name: '', email: '' }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error instanceof Error ? error.message : 'Failed to submit',
    })
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <InputText v-model="formData.name" />
    <InputText v-model="formData.email" />
    <Button type="submit" :loading="isSubmitting" :disabled="isSubmitting"> Submit </Button>
  </form>
</template>
```

## Best Practices Summary

### ✅ Do:

- Always handle loading, error, and success states
- Use computed properties for derived data
- Implement proper error handling with user feedback
- Use debouncing for search/input fields
- Cache queries appropriately
- Handle null/undefined safely with fallbacks
- Show loading indicators during async operations
- Provide optimistic updates for better UX

### ❌ Don't:

- Access query data without null checks
- Ignore error states
- Make queries inside loops
- Fetch data on every render
- Use `any` types for GraphQL responses
- Block UI during background updates
- Retry infinitely without limits
- Mutate query results directly

## Resources

- [URQL Documentation](https://formidable.com/open-source/urql/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [VueUse Utilities](https://vueuse.org/)
