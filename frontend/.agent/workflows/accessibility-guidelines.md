---
description: Accessibility (a11y) Guidelines and Best Practices
---

# Accessibility Guidelines

Ensure the Daily Helper application is usable by everyone, including people with disabilities.

## Core Principles (WCAG 2.1 AA)

### 1. **Perceivable**

Information must be presentable to users in ways they can perceive.

### 2. **Operable**

Interface components must be operable by all users.

### 3. **Understandable**

Information and operation must be understandable.

### 4. **Robust**

Content must be robust enough to work with assistive technologies.

## Color & Contrast

### Contrast Ratios (WCAG AA)

- **Normal text**: 4.5:1 minimum
- **Large text** (18pt+/14pt+ bold): 3:1 minimum
- **UI components**: 3:1 minimum

### Testing Colors

```css
/* ✅ Good: High contrast */
.text-surface-900 dark:text-dark-text
background: white / #0f172a

/* ❌ Bad: Low contrast */
.text-gray-400 on white background
```

**Tools:**

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Chrome DevTools Lighthouse

### Never Rely on Color Alone

```vue
<!-- ❌ Bad: Only color indicates error -->
<input class="border-red-500" />

<!-- ✅ Good: Color + icon + text -->
<div>
  <input
    class="border-red-500"
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <div id="email-error" class="flex items-center gap-2 text-red-500">
    <i class="pi pi-exclamation-circle" aria-hidden="true" />
    <ErrorText>Invalid email address</ErrorText>
  </div>
```

## Semantic HTML

### Use Proper Elements

```vue
<!-- ✅ Good: Semantic HTML -->
<nav>
  <ul>
    <li><a href="/home">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Title</h2>
      <p>Content</p>
    </section>
  </article>
</main>

<footer>
  <p>&copy; 2024 Daily Helper</p>
</footer>

<!-- ❌ Bad: Divs for everything -->
<div class="nav">
  <div class="nav-item">Home</div>
</div>
<div class="main">
  <div class="title">Page Title</div>
</div>
```

### Heading Hierarchy

```vue
<!-- ✅ Good: Proper hierarchy -->
<h1>Main Page Title</h1>
<h2>Section 1</h2>
<h3>Subsection 1.1</h3>
<h3>Subsection 1.2</h3>
<h2>Section 2</h2>

<!-- ❌ Bad: Skipping levels -->
<h1>Main Title</h1>
<h3>Section</h3>
<!-- Skipped h2 -->
```

## Keyboard Navigation

### Tab Order

Ensure logical tab order:

```vue
<!-- Implicit tab order (follows DOM order) -->
<form>
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">Submit</button>
</form>

<!-- Explicit tab order (avoid unless necessary) -->
<div tabindex="0">Custom focusable element</div>
```

**Tab Index Rules:**

- `tabindex="0"` - Natural tab order
- `tabindex="-1"` - Programmatically focusable, not in tab order
- `tabindex="1+"` - **Avoid!** Creates confusing tab order

### Keyboard Shortcuts

```vue
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const handleKeyPress = (e: KeyboardEvent) => {
  // Escape to close modals
  if (e.key === 'Escape') {
    closeModal()
  }

  // Enter on custom clickable elements
  if (e.key === 'Enter' || e.key === ' ') {
    handleAction()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyPress)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyPress)
})
</script>
```

### Focus Management

```vue
<script setup lang="ts">
import { ref, nextTick } from 'vue'

const inputRef = ref<HTMLInputElement>()
const isVisible = ref(false)

const openDialog = async () => {
  isVisible.value = true
  await nextTick()
  inputRef.value?.focus()
}
</script>

<template>
  <Dialog v-model:visible="isVisible">
    <InputText ref="inputRef" placeholder="Focus me on open" />
  </Dialog>
</template>
```

### Focus Indicators

```css
/* ✅ Good: Visible focus indicator */
.focus:outline-none
.focus:ring-2
.focus:ring-primary-500
.focus:ring-offset-2
.dark:focus:ring-offset-dark-bg

/* ❌ Bad: Removing focus without replacement */
.focus:outline-none
```

## ARIA Attributes

### Common ARIA Patterns

#### Buttons with Icons

```vue
<!-- Icon-only button needs aria-label -->
<Button icon="pi pi-trash" aria-label="Delete item" @click="handleDelete" />

<!-- Decorative icons should be hidden -->
<button>
  <i class="pi pi-check" aria-hidden="true" />
  <span>Save</span>
</button>
```

#### Form Fields

```vue
<div>
  <Label for="email">Email Address</Label>
  <InputText
    id="email"
    v-model="email"
    type="email"
    aria-required="true"
    aria-invalid="!!emailError"
    aria-describedby="email-error email-hint"
  />
  <small id="email-hint">We'll never share your email</small>
  <ErrorText v-if="emailError" id="email-error">
    {{ emailError }}
  </ErrorText>
</div>
```

#### Loading States

```vue
<div v-if="isLoading" role="status" aria-live="polite" aria-busy="true">
  <LoadingSpinner />
  <span class="sr-only">Loading content...</span>
</div>
```

#### Alerts & Messages

```vue
<!-- Success message -->
<div role="alert" aria-live="polite" class="bg-green-50 dark:bg-green-950 p-4">
  <i class="pi pi-check-circle" aria-hidden="true" />
  <span>Item saved successfully</span>
</div>

<!-- Error message -->
<div role="alert" aria-live="assertive" class="bg-red-50 dark:bg-red-950 p-4">
  <i class="pi pi-exclamation-triangle" aria-hidden="true" />
  <span>An error occurred</span>
</div>
```

#### Modals/Dialogs

```vue
<Dialog
  v-model:visible="visible"
  modal
  header="Confirm Action"
  role="dialog"
  aria-labelledby="dialog-header"
  aria-describedby="dialog-description"
>
  <template #header>
    <h2 id="dialog-header">Confirm Action</h2>
  </template>

  <p id="dialog-description">
    Are you sure you want to proceed?
  </p>

  <template #footer>
    <Button label="Cancel" @click="visible = false" />
    <Button label="Confirm" @click="handleConfirm" />
  </template>
</Dialog>
```

#### Navigation Landmarks

```vue
<template>
  <header role="banner">
    <nav aria-label="Main navigation">
      <!-- Main nav -->
    </nav>
  </header>

  <main role="main">
    <!-- Main content -->
  </main>

  <aside role="complementary" aria-label="Sidebar">
    <!-- Sidebar content -->
  </aside>

  <footer role="contentinfo">
    <!-- Footer -->
  </footer>
</template>
```

## Screen Reader Support

### Screen Reader Only Text

```vue
<style>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>

<template>
  <button>
    <i class="pi pi-search" aria-hidden="true" />
    <span class="sr-only">Search</span>
  </button>
</template>
```

### Live Regions

```vue
<script setup lang="ts">
const statusMessage = ref('')

const updateStatus = (message: string) => {
  statusMessage.value = message
}
</script>

<template>
  <!-- Announces changes to screen readers -->
  <div aria-live="polite" aria-atomic="true" class="sr-only">
    {{ statusMessage }}
  </div>
</template>
```

## Forms

### Labels

```vue
<!-- ✅ Good: Explicit label association -->
<div>
  <Label for="username">Username</Label>
  <InputText id="username" v-model="username" />
</div>

<!-- ✅ Also good: Implicit label association -->
<label>
  Username
  <InputText v-model="username" />
</label>

<!-- ❌ Bad: No label -->
<InputText placeholder="Username" />
```

### Required Fields

```vue
<div>
  <Label for="email">
    Email Address
    <span aria-label="required">*</span>
  </Label>
  <InputText
    id="email"
    v-model="email"
    required
    aria-required="true"
  />
</div>
```

### Error Messages

```vue
<div>
  <Label for="password">Password</Label>
  <InputText
    id="password"
    v-model="password"
    type="password"
    aria-invalid="!!passwordError"
    aria-describedby="password-error"
  />
  <ErrorText
    v-if="passwordError"
    id="password-error"
    role="alert"
  >
    {{ passwordError }}
  </ErrorText>
</div>
```

### Fieldsets & Legends

```vue
<fieldset>
  <legend>Personal Information</legend>

  <FormField label="First Name">
    <InputText v-model="firstName" />
  </FormField>

  <FormField label="Last Name">
    <InputText v-model="lastName" />
  </FormField>
</fieldset>
```

## Interactive Elements

### Links vs Buttons

```vue
<!-- ✅ Links: Navigate to different pages/sections -->
<a href="/about">About Us</a>

<!-- ✅ Buttons: Perform actions -->
<button @click="handleSave">Save</button>

<!-- ❌ Bad: Button styled as link for navigation -->
<button @click="router.push('/about')">About</button>

<!-- ❌ Bad: Link with click handler -->
<a href="#" @click.prevent="handleAction">Do Action</a>
```

### Custom Interactive Elements

```vue
<!-- If using non-button/link elements for interaction -->
<div
  role="button"
  tabindex="0"
  aria-pressed="isActive"
  @click="toggle"
  @keydown.enter="toggle"
  @keydown.space.prevent="toggle"
>
  Toggle me
</div>
```

### Disabled States

```vue
<!-- Disabled buttons should still be focusable for screen readers -->
<Button
  :disabled="isDisabled"
  aria-disabled="isDisabled"
  :title="isDisabled ? 'Complete the form to enable' : ''"
>
  Submit
</Button>
```

## Images & Media

### Alternative Text

```vue
<!-- ✅ Informative image -->
<img src="user-avatar.jpg" alt="John Doe's profile picture" />

<!-- ✅ Decorative image -->
<img src="decorative-pattern.svg" alt="" role="presentation" />

<!-- ✅ Complex image with description -->
<figure>
  <img
    src="sales-chart.png"
    alt="Sales chart showing growth"
    aria-describedby="chart-desc"
  />
  <figcaption id="chart-desc">
    Sales increased 25% in Q4 2024 compared to Q3
  </figcaption>
</figure>
```

### Icons

```vue
<!-- ✅ Decorative icon with text -->
<button>
  <i class="pi pi-save" aria-hidden="true" />
  <span>Save</span>
</button>

<!-- ✅ Icon-only button -->
<button aria-label="Save">
  <i class="pi pi-save" aria-hidden="true" />
</button>
```

## Tables

### Accessible Data Tables

```vue
<table>
  <caption>User List</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">John Doe</th>
      <td>john@example.com</td>
      <td>Admin</td>
    </tr>
  </tbody>
</table>
```

### PrimeVue DataTable

```vue
<DataTable :value="users" aria-label="User list">
  <Column field="name" header="Name" />
  <Column field="email" header="Email" />
</DataTable>
```

## Testing for Accessibility

### Automated Testing

```typescript
// Install: npm install -D @axe-core/playwright

import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('should not have accessibility violations', async ({ page }) => {
  await page.goto('/dashboard')

  const results = await new AxeBuilder({ page }).analyze()

  expect(results.violations).toEqual([])
})
```

### Manual Testing Checklist

- [ ] Navigate entire site using only keyboard (Tab, Enter, Escape)
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Verify color contrast ratios
- [ ] Test with browser zoom at 200%
- [ ] Disable JavaScript and verify core functionality
- [ ] Test in high contrast mode
- [ ] Verify focus indicators are visible
- [ ] Check all images have alt text
- [ ] Ensure form fields have labels

### Testing Tools

- **Browser Extensions:**
  - [axe DevTools](https://www.deque.com/axe/devtools/)
  - [WAVE](https://wave.webaim.org/extension/)
  - [Lighthouse](https://developers.google.com/web/tools/lighthouse) (built into Chrome)

- **Screen Readers:**
  - NVDA (Windows, free)
  - JAWS (Windows, paid)
  - VoiceOver (macOS/iOS, built-in)
  - TalkBack (Android, built-in)

## Common Mistakes to Avoid

❌ **Removing focus outlines without replacement**

```css
/* Don't do this */
* {
  outline: none;
}
```

❌ **Using placeholders as labels**

```vue
<InputText placeholder="Enter your email" />
```

❌ **Low contrast text**

```css
.text-gray-400 {
  color: #9ca3af;
} /* on white background */
```

❌ **Inaccessible custom select**

```vue
<div @click="toggle">
  <div>{{ selected }}</div>
  <div v-if="isOpen">
    <div v-for="option in options">{{ option }}</div>
  </div>
</div>
```

Use PrimeVue's Dropdown instead.

❌ **Missing alt text**

```vue
<img src="logo.png" />
```

## Resources

- [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Resources](https://webaim.org/resources/)
- [PrimeVue Accessibility](https://primevue.org/accessibility/)
- [Inclusive Components](https://inclusive-components.design/)
