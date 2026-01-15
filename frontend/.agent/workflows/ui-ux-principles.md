---
description: UI/UX Design Principles and Patterns
---

# UI/UX Design Principles

This guide establishes design principles and patterns for creating consistent, accessible, and delightful user experiences in Daily Helper.

## Core Design Principles

### 1. **Consistency**

Maintain visual and functional consistency throughout the application.

- Use the same component for similar actions
- Apply consistent spacing, colors, and typography
- Follow established patterns for navigation and interactions

### 2. **Clarity**

Every element should clearly communicate its purpose.

- Use clear, action-oriented labels
- Provide immediate feedback for user actions
- Show loading states and progress indicators
- Display helpful error messages

### 3. **Efficiency**

Minimize cognitive load and steps required to complete tasks.

- Reduce the number of clicks needed
- Use smart defaults and auto-complete
- Group related actions together
- Provide keyboard shortcuts for power users

### 4. **Accessibility**

Design for all users, including those with disabilities.

- Maintain proper color contrast (WCAG AA minimum)
- Support keyboard navigation
- Include ARIA labels and semantic HTML
- Provide text alternatives for visual content

### 5. **Responsiveness**

Ensure the app works seamlessly across all device sizes.

- Mobile-first approach
- Touch-friendly tap targets (minimum 44x44px)
- Responsive layouts and components
- Test on real devices

## Layout Patterns

### Page Structure Template

```vue
<template>
  <PageWrapper>
    <PageContainer>
      <!-- Header with title and actions -->
      <PageHeader title="Page Title">
        <template #actions>
          <Button label="Primary Action" />
        </template>
      </PageHeader>

      <!-- Main content area -->
      <div class="space-y-6">
        <ContentCard>
          <SectionHeading>Section 1</SectionHeading>
          <!-- Content -->
        </ContentCard>

        <ContentCard>
          <SectionHeading>Section 2</SectionHeading>
          <!-- Content -->
        </ContentCard>
      </div>
    </PageContainer>
  </PageWrapper>
</template>
```

### Grid Layouts

```vue
<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <ContentCard v-for="item in items" :key="item.id">
    <!-- Card content -->
  </ContentCard>
</div>
```

### List Views

```vue
<div class="space-y-4">
  <ContentCard
    v-for="item in items"
    :key="item.id"
    padding="sm"
  >
    <div class="flex items-center justify-between">
      <div>
        <SubHeading>{{ item.title }}</SubHeading>
        <BodyText>{{ item.description }}</BodyText>
      </div>
      <Button icon="pi pi-chevron-right" text rounded />
    </div>
  </ContentCard>
</div>
```

## Interactive States

### Loading States

**Always show loading indicators for async operations:**

```vue
<script setup lang="ts">
import LoadingSpinner from '@/components/common/feedback/LoadingSpinner.vue'

const isLoading = ref(true)
</script>

<template>
  <LoadingSpinner v-if="isLoading" />
  <div v-else>
    <!-- Content -->
  </div>
</template>
```

### Empty States

**Provide helpful empty states:**

```vue
<script setup lang="ts">
import EmptyState from '@/components/common/feedback/EmptyState.vue'
</script>

<template>
  <EmptyState
    v-if="!items.length"
    icon="pi pi-inbox"
    message="No items found"
    description="Create your first item to get started"
  >
    <template #actions>
      <Button label="Create Item" @click="createItem" />
    </template>
  </EmptyState>
</template>
```

### Error States

**Show clear, actionable error messages:**

```vue
<script setup lang="ts">
import { useToast } from 'primevue/usetoast'

const toast = useToast()

const handleError = (error: Error) => {
  toast.add({
    severity: 'error',
    summary: 'Error',
    detail: error.message || 'Something went wrong',
    life: 5000,
  })
}
</script>
```

### Success Feedback

**Confirm successful actions:**

```vue
const handleSuccess = () => { toast.add({ severity: 'success', summary: 'Success', detail: 'Item
saved successfully', life: 3000 }) }
```

## Form Design

### Form Layout

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Form sections -->
    <FormGroup title="Personal Information">
      <FormField label="Full Name" required :error="errors.name">
        <InputText v-model="form.name" placeholder="Enter your name" />
      </FormField>

      <FormField label="Email" required :error="errors.email">
        <InputText v-model="form.email" type="email" placeholder="email@example.com" />
      </FormField>
    </FormGroup>

    <!-- Actions -->
    <FormActions>
      <Button label="Cancel" severity="secondary" outlined @click="handleCancel" />
      <Button label="Save" type="submit" :loading="isSubmitting" />
    </FormActions>
  </form>
</template>
```

### Form Validation

Use VeeValidate with Yup for form validation:

```typescript
import { useForm } from 'vee-validate'
import * as yup from 'yup'

const schema = yup.object({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  age: yup.number().positive().integer().min(18, 'Must be 18 or older'),
})

const { errors, handleSubmit, defineField } = useForm({
  validationSchema: schema,
})

const [name] = defineField('name')
const [email] = defineField('email')
```

### Required Fields

```vue
<FormField label="Name" required>
  <InputText v-model="name" />
</FormField>
```

## Navigation Patterns

### Breadcrumbs

```vue
<script setup lang="ts">
import Breadcrumb from 'primevue/breadcrumb'

const items = ref([
  { label: 'Home', to: '/' },
  { label: 'Users', to: '/users' },
  { label: 'Profile' },
])
</script>

<template>
  <Breadcrumb :model="items" class="mb-4" />
</template>
```

### Tab Navigation

```vue
<script setup lang="ts">
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
</script>

<template>
  <TabView>
    <TabPanel header="Overview">
      <p>Overview content</p>
    </TabPanel>
    <TabPanel header="Details">
      <p>Details content</p>
    </TabPanel>
  </TabView>
</template>
```

## Data Display

### Tables

```vue
<script setup lang="ts">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
</script>

<template>
  <DataTable :value="users" paginator :rows="10" :rowsPerPageOptions="[5, 10, 20]" stripedRows>
    <Column field="name" header="Name" sortable />
    <Column field="email" header="Email" sortable />
    <Column field="role" header="Role">
      <template #body="{ data }">
        <Badge :value="data.role" />
      </template>
    </Column>
    <Column header="Actions">
      <template #body="{ data }">
        <Button icon="pi pi-pencil" text rounded />
        <Button icon="pi pi-trash" severity="danger" text rounded />
      </template>
    </Column>
  </DataTable>
</template>
```

### Cards with Actions

```vue
<template>
  <ContentCard>
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <SubHeading>{{ title }}</SubHeading>
        <BodyText>{{ description }}</BodyText>
      </div>

      <div class="flex gap-2">
        <Button icon="pi pi-pencil" text rounded />
        <Button icon="pi pi-trash" severity="danger" text rounded />
      </div>
    </div>
  </ContentCard>
</template>
```

## Modal/Dialog Design

### Confirmation Dialogs

```vue
<script setup lang="ts">
import { useConfirm } from 'primevue/useconfirm'

const confirm = useConfirm()

const confirmDelete = () => {
  confirm.require({
    message: 'Are you sure you want to delete this item?',
    header: 'Confirm Deletion',
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'Cancel',
    acceptLabel: 'Delete',
    rejectProps: {
      outlined: true,
      severity: 'secondary',
    },
    acceptProps: {
      severity: 'danger',
    },
    accept: () => {
      // Handle deletion
    },
  })
}
</script>
```

### Form Dialogs

```vue
<script setup lang="ts">
import Dialog from 'primevue/dialog'

const visible = ref(false)
</script>

<template>
  <Dialog v-model:visible="visible" modal header="Add New User" :style="{ width: '32rem' }">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <FormField label="Name">
        <InputText v-model="name" />
      </FormField>

      <FormActions>
        <Button label="Cancel" outlined @click="visible = false" />
        <Button label="Save" type="submit" />
      </FormActions>
    </form>
  </Dialog>
</template>
```

## Spacing & Rhythm

### Consistent Spacing Scale

Use TailwindCSS spacing utilities:

```css
gap-2, space-y-2   → 0.5rem (8px)   - Tight
gap-4, space-y-4   → 1rem (16px)    - Small
gap-6, space-y-6   → 1.5rem (24px)  - Medium (default for sections)
gap-8, space-y-8   → 2rem (32px)    - Large
gap-12, space-y-12 → 3rem (48px)    - Extra large
```

### Vertical Rhythm

```vue
<template>
  <PageContainer>
    <!-- Use space-y-* for consistent vertical spacing -->
    <div class="space-y-6">
      <section>...</section>
      <section>...</section>
      <section>...</section>
    </div>
  </PageContainer>
</template>
```

## Animation & Transitions

### Subtle Transitions

```vue
<template>
  <!-- Hover transitions -->
  <button class="transition-colors duration-200 hover:bg-primary-700">Click me</button>

  <!-- Transform transitions -->
  <div class="transition-transform duration-200 hover:scale-105">Hover to scale</div>
</template>
```

### Vue Transitions

```vue
<template>
  <Transition name="fade">
    <div v-if="show">Fade in/out</div>
  </Transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

## Responsive Patterns

### Mobile Navigation

```vue
<template>
  <!-- Desktop: Horizontal menu -->
  <nav class="hidden md:flex gap-4">
    <a href="/dashboard">Dashboard</a>
    <a href="/users">Users</a>
  </nav>

  <!-- Mobile: Hamburger menu -->
  <Button icon="pi pi-bars" class="md:hidden" @click="mobileMenuVisible = true" />
</template>
```

### Responsive Typography

```vue
<template>
  <!-- Scale text sizes responsively -->
  <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">Responsive Heading</h1>

  <p class="text-sm md:text-base">Responsive body text</p>
</template>
```

## Accessibility Checklist

- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Sufficient color contrast (4.5:1 for normal text)
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Focus indicators are visible
- [ ] ARIA labels on icon buttons
- [ ] Form inputs have associated labels
- [ ] Error messages are announced to screen readers
- [ ] Images have alt text
- [ ] Interactive elements have proper roles

## Common UI Patterns

### Search with Filter

```vue
<template>
  <div class="space-y-4">
    <div class="flex gap-4">
      <InputText v-model="search" placeholder="Search..." class="flex-1">
        <template #prefix>
          <i class="pi pi-search" />
        </template>
      </InputText>

      <Dropdown v-model="filter" :options="filterOptions" placeholder="Filter by" />
    </div>

    <!-- Results -->
  </div>
</template>
```

### Action Confirmation

```vue
<script setup lang="ts">
const handleDelete = () => {
  confirm.require({
    message: 'This action cannot be undone. Continue?',
    header: 'Confirm Action',
    icon: 'pi pi-exclamation-triangle',
    accept: () => performDelete(),
  })
}
</script>
```

### Bulk Actions

```vue
<template>
  <div class="space-y-4">
    <!-- Selection toolbar -->
    <div
      v-if="selectedItems.length"
      class="flex items-center gap-4 p-4 bg-primary-50 dark:bg-primary-950 rounded-lg"
    >
      <span>{{ selectedItems.length }} items selected</span>
      <Button label="Delete" severity="danger" outlined />
      <Button label="Export" outlined />
    </div>

    <!-- Items list -->
  </div>
</template>
```

## Resources

- [PrimeVue Templates](https://primevue.org/templates)
- [Material Design Guidelines](https://m3.material.io/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
