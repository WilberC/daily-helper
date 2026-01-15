---
description: Styling Guidelines - TailwindCSS, PrimeVue, Color Palette & Dark Mode
---

# Styling Guidelines

This document outlines best practices for styling in the Daily Helper frontend application.

## Technology Stack

- **CSS Framework**: TailwindCSS 3.4+
- **UI Component Library**: PrimeVue 4.3+ with Aura theme preset
- **Theme System**: Custom emerald-based color palette with light/dark modes
- **CSS Layers**: Ordered as `tailwind-base → primevue → tailwind-utilities`

## Color Palette

### Primary Colors (Emerald)

Use the emerald color palette for primary actions, highlights, and brand identity:

```css
primary-50  → #ecfdf5 (lightest)
primary-100 → #d1fae5
primary-200 → #a7f3d0
primary-300 → #6ee7b7
primary-400 → #34d399
primary-500 → #10b981 (DEFAULT)
primary-600 → #059669
primary-700 → #047857
primary-800 → #065f46
primary-900 → #064e3b
primary-950 → #022c22 (darkest)
```

### Dark Mode Colors

Custom dark mode palette defined in `tailwind.config.js`:

```css
dark-bg             → #0f172a (background)
dark-surface        → #1e293b (cards/panels)
dark-border         → #334155 (borders)
dark-text           → #f1f5f9 (primary text)
dark-text-secondary → #94a3b8 (secondary text)
```

### Surface Colors (PrimeVue)

PrimeVue provides semantic surface colors that automatically adapt to light/dark mode:

```
surface-0   → White (light) / #0f172a (dark) - Main background
surface-50  → Lightest shade
surface-100 → Very light shade
...
surface-800 → Very dark shade
surface-900 → #1e293b (dark) - Card backgrounds
surface-950 → Darkest shade
```

## Dark Mode Implementation

### Activating Dark Mode

Dark mode is controlled by the `.dark` class on the `<html>` element:

```typescript
// In theme store
document.documentElement.classList.toggle('dark')
```

### Dark Mode Styling Patterns

**Always use Tailwind's dark: variant for conditional styling:**

```vue
<!-- Correct: Using dark: variant -->
<div class="bg-surface-0 dark:bg-dark-bg text-surface-900 dark:text-dark-text">

<!-- Incorrect: Don't use manual class switching -->
<div :class="isDark ? 'bg-dark-bg' : 'bg-white'">
```

**Common Dark Mode Classes:**

```css
/* Backgrounds */
bg-surface-0 dark:bg-dark-bg           /* Main background */
bg-surface-0 dark:bg-surface-900       /* Card backgrounds */
bg-white dark:bg-surface-800           /* Alternative surfaces */

/* Text */
text-surface-900 dark:text-dark-text           /* Primary text */
text-surface-700 dark:text-dark-text-secondary /* Secondary text */

/* Borders */
border-surface-200 dark:border-surface-700     /* Standard borders */
border-surface-300 dark:border-dark-border     /* Emphasized borders */

/* Hover States */
hover:bg-surface-100 dark:hover:bg-surface-800 /* Hover backgrounds */
```

## Component Styling Best Practices

### 1. Use Existing Components First

Before creating custom styles, check if a component exists in:

- `src/components/common/` - Reusable UI components
- `src/components/layout/` - Layout components
- PrimeVue library - Pre-built components

### 2. Semantic Component Structure

```vue
<template>
  <!-- Use layout components -->
  <PageWrapper>
    <PageContainer>
      <PageHeader title="Page Title" />

      <ContentCard padding="md">
        <SectionHeading>Section</SectionHeading>
        <BodyText>Content here</BodyText>
      </ContentCard>
    </PageContainer>
  </PageWrapper>
</template>
```

### 3. Typography Components

Use typography components instead of raw HTML:

```vue
<!-- Correct ✓ -->
<PageHeading>Main Title</PageHeading>
<SectionHeading>Section Title</SectionHeading>
<SubHeading>Subsection Title</SubHeading>
<BodyText>Regular text content</BodyText>
<Label>Form label</Label>
<ErrorText>Error message</ErrorText>

<!-- Incorrect ✗ -->
<h1 class="text-3xl font-bold">Main Title</h1>
<p class="text-gray-600">Regular text</p>
```

### 4. Consistent Spacing

Use Tailwind's spacing scale consistently:

```css
/* Padding/Margin Scale */
p-2, m-2   → 0.5rem (8px)   - Tight spacing
p-4, m-4   → 1rem (16px)    - Default small
p-6, m-6   → 1.5rem (24px)  - Default medium
p-8, m-8   → 2rem (32px)    - Default large
p-12, m-12 → 3rem (48px)    - Extra large
```

### 5. PrimeVue Component Integration

When using PrimeVue components, leverage their built-in theme support:

```vue
<script setup>
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
</script>

<template>
  <!-- PrimeVue components automatically adapt to theme -->
  <Button label="Primary Action" severity="primary" />
  <Button label="Secondary" severity="secondary" />
  <Button label="Danger" severity="danger" />

  <!-- Use 'text' variant for subtle actions -->
  <Button label="Text Button" text />

  <!-- Use 'outlined' for secondary emphasis -->
  <Button label="Outlined" outlined />
</template>
```

## CSS Layer System

The app uses CSS layers for proper style precedence:

```css
/* In main.css */
@layer tailwind-base, primevue, tailwind-utilities;

@layer tailwind-base {
  @tailwind base;
}

@layer tailwind-utilities {
  @tailwind components;
  @tailwind utilities;
}
```

**When to use each layer:**

- `@layer base` - Global resets and defaults
- `primevue` - PrimeVue component styles (auto-managed)
- `@layer utilities` - Custom utility classes

## Custom Utility Classes

### Scrollbar Styles

Dark mode scrollbar utility available:

```vue
<div class="overflow-auto scrollbar-dark">
  <!-- Content -->
</div>
```

### Creating New Utilities

Add new utilities in `main.css`:

```css
@layer utilities {
  .glass-morphism {
    @apply bg-white/10 dark:bg-black/10 backdrop-blur-lg;
  }

  .text-balance {
    text-wrap: balance;
  }
}
```

## Responsive Design

Use Tailwind's mobile-first breakpoints:

```vue
<template>
  <div
    class="
    grid
    grid-cols-1          /* Mobile: 1 column */
    md:grid-cols-2       /* Tablet: 2 columns */
    lg:grid-cols-3       /* Desktop: 3 columns */
    gap-4 md:gap-6       /* Responsive gap */
  "
  >
    <!-- Grid items -->
  </div>
</template>
```

**Breakpoints:**

- `sm:` - 640px (Phone landscape)
- `md:` - 768px (Tablet)
- `lg:` - 1024px (Desktop)
- `xl:` - 1280px (Large desktop)
- `2xl:` - 1536px (Extra large)

## Common Patterns

### Card with Dark Mode Support

```vue
<div
  class="
  bg-surface-0 dark:bg-surface-900
  border border-surface-200 dark:border-surface-700
  rounded-lg p-6
  shadow-sm dark:shadow-lg
"
>
  <!-- Content -->
</div>
```

### Interactive Elements

```vue
<button
  class="
  px-4 py-2 rounded-lg
  bg-primary-600 dark:bg-primary-500
  text-white
  hover:bg-primary-700 dark:hover:bg-primary-400
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
  dark:focus:ring-offset-dark-bg
"
>
  Click me
</button>
```

### Input Fields

```vue
<input
  class="
  w-full px-4 py-2 rounded-lg
  bg-surface-0 dark:bg-surface-800
  border border-surface-300 dark:border-surface-600
  text-surface-900 dark:text-dark-text
  placeholder:text-surface-400 dark:placeholder:text-surface-500
  focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20
  transition-colors
"
/>
```

## Anti-Patterns to Avoid

❌ **Don't use arbitrary colors**

```vue
<!-- Bad -->
<div class="bg-blue-500 text-gray-800">
```

✅ **Use semantic color tokens**

```vue
<!-- Good -->
<div class="bg-primary-600 text-surface-900 dark:text-dark-text">
```

❌ **Don't inline styles**

```vue
<!-- Bad -->
<div style="color: #10b981">
```

✅ **Use Tailwind classes**

```vue
<!-- Good -->
<div class="text-primary-500">
```

❌ **Don't create component-specific CSS files**

```vue
<!-- Bad: MyComponent.vue -->
<style scoped>
.my-custom-class {
  background: #10b981;
}
</style>
```

✅ **Use Tailwind utility classes or create shared utilities**

```vue
<!-- Good -->
<template>
  <div class="bg-primary-500">
</template>
```

## Testing Dark Mode

Always test components in both light and dark modes:

1. Use the `ThemeToggle` component in your development layout
2. Verify all text is readable in both modes
3. Check interactive states (hover, focus, active) in both modes
4. Ensure proper contrast ratios for accessibility

## Resources

- [TailwindCSS Documentation](https://tailwindcss.com)
- [PrimeVue Documentation](https://primevue.org)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
