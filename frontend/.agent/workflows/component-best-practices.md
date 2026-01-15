---
description: Component Development Best Practices for Vue 3 + TypeScript
---

# Component Best Practices

This guide outlines best practices for creating and using components in the Daily Helper frontend.

## Component Architecture

### Folder Structure

```
src/components/
├── common/              # Reusable, generic components
│   ├── display/        # Display-only components (DataField, UserAvatar)
│   ├── feedback/       # User feedback (EmptyState, LoadingSpinner)
│   ├── form/           # Form-related (FormField, FormActions)
│   ├── typography/     # Text components (Heading, BodyText, Label)
│   └── utils/          # Utilities (Badge, Icon, Divider, Spacer)
├── layout/             # Layout components (PageContainer, ContentCard)
├── users/              # Feature-specific components
└── ThemeToggle.vue     # Standalone utilities
```

### Component Organization Rules

1. **Common components** → Generic, reusable across features
2. **Feature components** → Specific to a domain (e.g., `users/`, `tasks/`)
3. **Layout components** → Page structure and containers
4. **One component per file** → Named matching the file

## Writing Components

### Component Template

```vue
<script setup lang="ts">
import { computed, ref } from 'vue'

// 1. Define Props Interface
interface Props {
  title: string
  description?: string
  variant?: 'default' | 'primary' | 'danger'
}

// 2. Define Props with defaults
const props = withDefaults(defineProps<Props>(), {
  description: '',
  variant: 'default',
})

// 3. Define Emits
const emit = defineEmits<{
  submit: [value: string]
  cancel: []
}>()

// 4. Reactive state
const isLoading = ref(false)

// 5. Computed properties
const variantClasses = computed(() => {
  const variants = {
    default: 'bg-surface-0 dark:bg-surface-900',
    primary: 'bg-primary-50 dark:bg-primary-950',
    danger: 'bg-red-50 dark:bg-red-950',
  }
  return variants[props.variant]
})

// 6. Methods
const handleSubmit = () => {
  emit('submit', 'some value')
}
</script>

<template>
  <div :class="variantClasses">
    <h2>{{ title }}</h2>
    <p v-if="description">{{ description }}</p>
    <slot />
  </div>
</template>
```

### TypeScript Best Practices

#### Always Type Props

```typescript
// ✅ Good: Explicit types with interface
interface Props {
  userId: string
  isActive?: boolean
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  isActive: true,
  count: 0,
})

// ❌ Bad: No types
const props = defineProps(['userId', 'isActive'])
```

#### Type Emits

```typescript
// ✅ Good: Typed emits
const emit = defineEmits<{
  update: [id: string, value: number]
  delete: [id: string]
  cancel: []
}>()

// ❌ Bad: String-based emits
const emit = defineEmits(['update', 'delete'])
```

#### Type Composables and Refs

```typescript
// ✅ Good: Explicit typing
const count = ref<number>(0)
const user = ref<User | null>(null)
const items = ref<Item[]>([])

// ❌ Bad: Type inference can fail
const count = ref(0) // might not catch type errors
```

## Component Composition

### Use Existing Components

**Always check for existing components before creating new ones:**

```vue
<script setup lang="ts">
// ✅ Good: Reuse existing components
import PageContainer from '@/components/layout/PageContainer.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import ContentCard from '@/components/layout/ContentCard.vue'
import SectionHeading from '@/components/common/typography/SectionHeading.vue'
import BodyText from '@/components/common/typography/BodyText.vue'
import LoadingSpinner from '@/components/common/feedback/LoadingSpinner.vue'
import EmptyState from '@/components/common/feedback/EmptyState.vue'
</script>

<template>
  <PageContainer>
    <PageHeader title="Users" />

    <LoadingSpinner v-if="isLoading" />

    <EmptyState v-else-if="!users.length" message="No users found" icon="pi pi-users" />

    <ContentCard v-else>
      <SectionHeading>User List</SectionHeading>
      <BodyText>{{ users.length }} users</BodyText>
    </ContentCard>
  </PageContainer>
</template>
```

### Component Hierarchy

Build components from bottom-up:

```
PageWrapper
  └── PageContainer
        ├── PageHeader
        └── ContentCard
              ├── SectionHeading
              └── BodyText
```

### Slots for Flexibility

```vue
<script setup lang="ts">
// Parent component
</script>

<template>
  <ContentCard>
    <!-- Default slot -->
    <template #default>
      <SectionHeading>Main Content</SectionHeading>
    </template>

    <!-- Named slot for actions -->
    <template #actions>
      <Button label="Save" />
    </template>
  </ContentCard>
</template>
```

Component definition:

```vue
<template>
  <div class="card">
    <div class="card-header">
      <slot name="header" />
    </div>

    <div class="card-body">
      <slot />
    </div>

    <div v-if="$slots.actions" class="card-actions">
      <slot name="actions" />
    </div>
  </div>
</template>
```

## State Management

### Local State (ref/reactive)

Use for component-specific state:

```typescript
// Simple values
const count = ref(0)
const isVisible = ref(false)

// Objects
const form = reactive({
  name: '',
  email: '',
})
```

### Pinia Store

Use for shared/global state:

```typescript
// In component
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)
```

### When to Use Which?

- **ref/reactive**: UI state, form inputs, component-only data
- **Pinia**: User authentication, app settings, shared data
- **Props**: Parent → Child data flow
- **Emits**: Child → Parent events

## PrimeVue Integration

### Import PrimeVue Components

```typescript
// ✅ Good: Import specific components
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

// ❌ Bad: Don't import the whole library
import * as PrimeVue from 'primevue'
```

### Use PrimeVue for Complex UI

Prefer PrimeVue components for:

- Forms (InputText, Dropdown, Calendar)
- Data display (DataTable, Card, Panel)
- Navigation (Menu, TabView, Breadcrumb)
- Overlays (Dialog, Toast, Tooltip)

```vue
<script setup lang="ts">
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

const visible = ref(false)
</script>

<template>
  <Button label="Open Dialog" @click="visible = true" />

  <Dialog v-model:visible="visible" modal header="User Details" :style="{ width: '50rem' }">
    <div class="flex flex-col gap-4">
      <InputText v-model="name" placeholder="Name" />
    </div>
  </Dialog>
</template>
```

## Accessibility

### Semantic HTML

```vue
<!-- ✅ Good: Semantic elements -->
<nav>
  <ul>
    <li><a href="/home">Home</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Title</h1>
  </article>
</main>

<!-- ❌ Bad: Div soup -->
<div class="nav">
  <div class="item">Home</div>
</div>
```

### ARIA Labels

```vue
<!-- Buttons -->
<Button icon="pi pi-trash" aria-label="Delete item" @click="handleDelete" />

<!-- Icons -->
<i class="pi pi-info-circle" aria-hidden="true" />
<span class="sr-only">More information</span>

<!-- Form inputs -->
<label for="email">Email</label>
<InputText id="email" v-model="email" aria-required="true" aria-invalid="hasError" />
```

### Keyboard Navigation

Ensure interactive elements are keyboard accessible:

```vue
<div
  role="button"
  tabindex="0"
  @click="handleClick"
  @keydown.enter="handleClick"
  @keydown.space.prevent="handleClick"
>
  Clickable div
</div>
```

## Performance

### Use v-show vs v-if Appropriately

```vue
<!-- v-if: Complete removal/addition from DOM -->
<ExpensiveComponent v-if="showComponent" />

<!-- v-show: CSS display toggle (better for frequent toggles) -->
<div v-show="isVisible">Toggle me frequently</div>
```

### Lazy Load Heavy Components

```typescript
import { defineAsyncComponent } from 'vue'

const HeavyChart = defineAsyncComponent(() => import('./components/HeavyChart.vue'))
```

### Computed vs Methods

```typescript
// ✅ Good: Cached, only recalculates when dependencies change
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// ❌ Bad: Recalculates on every render
const getFullName = () => `${firstName.value} ${lastName.value}`
```

## Component Testing

Every component should have tests:

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from './MyComponent.vue'

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: {
        title: 'Test Title',
      },
    })

    expect(wrapper.text()).toContain('Test Title')
  })

  it('emits event on click', async () => {
    const wrapper = mount(MyComponent)
    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted()).toHaveProperty('submit')
  })
})
```

## Anti-Patterns

### ❌ God Components

Don't create massive components that do everything:

```vue
<!-- Bad: 500+ lines, handles everything -->
<script setup lang="ts">
// User logic, API calls, form handling, validation, etc.
</script>
```

Instead, split into smaller focused components.

### ❌ Prop Drilling

Don't pass props through many levels:

```vue
<!-- Bad -->
<GrandParent :user="user" />
<Parent :user="user" />
<Child :user="user" />
```

Use Pinia store or provide/inject for deep data sharing.

### ❌ Direct DOM Manipulation

```typescript
// ❌ Bad
document.getElementById('myElement').style.color = 'red'

// ✅ Good
const isError = ref(true)
// In template: :class="{ 'text-red-500': isError }"
```

### ❌ Mutating Props

```typescript
// ❌ Bad
const props = defineProps<{ items: Item[] }>()
props.items.push(newItem)

// ✅ Good
const localItems = ref([...props.items])
localItems.value.push(newItem)
// Or emit event to parent
```

## Checklist for New Components

- [ ] Component has a clear, single responsibility
- [ ] Props are typed with TypeScript interfaces
- [ ] Emits are typed
- [ ] Dark mode styles are included
- [ ] Accessibility attributes are added (aria-labels, etc.)
- [ ] Component is responsive (mobile, tablet, desktop)
- [ ] Existing components are reused where possible
- [ ] PrimeVue components are used for complex UI
- [ ] Component has unit tests
- [ ] Component is documented (JSDoc or comments)

## Resources

- [Vue 3 Documentation](https://vuejs.org)
- [TypeScript with Vue](https://vuejs.org/guide/typescript/overview.html)
- [PrimeVue Components](https://primevue.org/components)
- [Pinia Documentation](https://pinia.vuejs.org)
