---
description: Internationalization (i18n) Guidelines and Implementation
---

# i18n Guidelines

This workflow ensures all components and views use the internationalization system for multi-language support.

## Core i18n System

### Translation Composable

The application uses `useTranslation` composable located at `src/composables/useTranslation.ts`:

```typescript
import { useTranslation } from '@/composables/useTranslation'

const { t, currentLang, setLang } = useTranslation()
```

### Available Functions

- **`t(key, params?)`** - Translate a key with optional parameters
- **`currentLang`** - Reactive ref to current language code ('en' | 'es')
- **`setLang(lang)`** - Change language and persist to localStorage

## Translation Keys Structure

All translations are organized in `src/locales/` with the following structure:

```typescript
{
  common: {
    welcome: 'Welcome',
    save: 'Save',
    cancel: 'Cancel',
    // ...
  },
  login: {
    title: 'Daily Helper',
    subtitle: 'Sign in to your account',
    username: 'Username',
    password: 'Password',
    // ...
  },
  users: {
    management: 'User Management',
    form: {
      username: 'Username',
      email: 'Email',
      // ...
    },
    // ...
  },
  validation: {
    required: '{field} is required',
    minLength: '{field} must be at least {min} characters',
    // ...
  }
}
```

## When Creating New Components

### 1. Import the Composable

Always import `useTranslation` at the top of your script:

```vue
<script setup lang="ts">
import { useTranslation } from '@/composables/useTranslation'

const { t } = useTranslation()
</script>
```

### 2. Replace All Hardcoded Strings

**❌ Bad - Hardcoded text:**
```vue
<template>
  <h1>User Management</h1>
  <n-button>Create User</n-button>
  <p>Welcome, {{ user.name }}!</p>
</template>
```

**✅ Good - Using translations:**
```vue
<template>
  <h1>{{ t('users.management') }}</h1>
  <n-button>{{ t('users.form.create') }}</n-button>
  <p>{{ t('common.welcome', { name: user.name }) }}</p>
</template>
```

### 3. Add Translation Keys

When creating new components, add the corresponding keys to both language files:

**src/locales/en.ts:**
```typescript
export const en = {
  // ... existing keys
  myNewFeature: {
    title: 'My New Feature',
    description: 'This is a new feature',
    action: 'Click here',
  },
}
```

**src/locales/es.ts:**
```typescript
export const es = {
  // ... existing keys
  myNewFeature: {
    title: 'Mi Nueva Función',
    description: 'Esta es una nueva función',
    action: 'Haz clic aquí',
  },
}
```

### 4. Use Nested Keys

Organize translation keys hierarchically using dot notation:

```typescript
t('users.form.username')        // users → form → username
t('dashboard.stats.total')      // dashboard → stats → total
t('validation.email.invalid')   // validation → email → invalid
```

### 5. Parameter Interpolation

For dynamic content, use parameter interpolation:

```vue
<template>
  <!-- Simple parameter -->
  <p>{{ t('common.greeting', { name: userName }) }}</p>

  <!-- Multiple parameters -->
  <p>{{ t('users.stats', { count: userCount, active: activeCount }) }}</p>
</template>
```

Translation keys with parameters:
```typescript
{
  common: {
    greeting: 'Hello, {name}!',
  },
  users: {
    stats: 'Total: {count}, Active: {active}',
  },
}
```

## Form Validation Messages

For form validation, use translation keys in your validation schema:

```typescript
import { useTranslation } from '@/composables/useTranslation'
import * as yup from 'yup'

const { t } = useTranslation()

const schema = yup.object({
  username: yup
    .string()
    .required(t('validation.required', { field: t('users.form.username') }))
    .min(3, t('validation.minLength', { field: t('users.form.username'), min: 3 })),
  email: yup
    .string()
    .required(t('validation.required', { field: t('users.form.email') }))
    .email(t('validation.email.invalid')),
})
```

## Component Checklist

When creating or modifying components, ensure:

- [ ] `useTranslation` composable is imported
- [ ] All visible text uses `t()` function
- [ ] Translation keys are added to both `en.ts` and `es.ts`
- [ ] Keys are organized hierarchically (e.g., `feature.section.item`)
- [ ] Dynamic content uses parameter interpolation
- [ ] Form validation messages use translation keys
- [ ] Placeholders and aria-labels are translated
- [ ] Error messages and success messages are translated

## Common Patterns

### Buttons
```vue
<n-button>{{ t('common.save') }}</n-button>
<n-button>{{ t('common.cancel') }}</n-button>
<n-button>{{ t('users.form.create') }}</n-button>
```

### Form Labels
```vue
<FormField :label="t('users.form.username')" for="username">
  <n-input
    id="username"
    v-model:value="username"
    :placeholder="t('users.form.enterUsername')"
  />
</FormField>
```

### Conditional Text
```vue
<p>
  {{
    userType === 'admin'
      ? t('users.types.admin')
      : t('users.types.normal')
  }}
</p>
```

### Lists and Tables
```vue
<n-data-table :columns="columns" :data="data" />

<script setup lang="ts">
const columns = [
  { title: t('users.table.username'), key: 'username' },
  { title: t('users.table.email'), key: 'email' },
  { title: t('users.table.role'), key: 'role' },
]
</script>
```

## Testing Translations

### Manual Testing
1. Switch language using the language selector
2. Verify all text changes to the selected language
3. Check that no hardcoded English text remains
4. Test parameter interpolation with different values

### Auto-Detection Testing
1. Clear localStorage
2. Change browser language settings
3. Reload the application
4. Verify correct language is detected

## Supported Languages

Currently supported languages:
- **English (en)** - Default
- **Spanish (es)**

To add a new language:
1. Create `src/locales/[code].ts` with all translation keys
2. Export it from `src/locales/index.ts`
3. Add it to the `translations` object in `useTranslation.ts`
4. Add it to the language selector options

## Best Practices

1. **Always use translation keys** - Never hardcode user-facing text
2. **Keep keys organized** - Use hierarchical structure (feature.section.item)
3. **Be consistent** - Use the same key for the same text across components
4. **Add both languages** - Always add keys to both `en.ts` and `es.ts` simultaneously
5. **Use parameters** - For dynamic content, use `{param}` syntax
6. **Test thoroughly** - Switch languages and verify all text is translated
7. **Meaningful keys** - Use descriptive key names (e.g., `users.form.createButton` not `btn1`)

## Common Mistakes to Avoid

❌ **Hardcoded text in template:**
```vue
<h1>Welcome</h1>
```

❌ **Missing translation in one language:**
```typescript
// en.ts has the key, but es.ts doesn't
```

❌ **Not using parameters for dynamic content:**
```vue
<p>Welcome, {{ user.name }}!</p>  <!-- Should use t() with params -->
```

❌ **Inconsistent key naming:**
```typescript
{ createBtn: 'Create' }  // Should be { form: { create: 'Create' } }
```

## Resources

- Translation composable: `src/composables/useTranslation.ts`
- English translations: `src/locales/en.ts`
- Spanish translations: `src/locales/es.ts`
- Language selector: `src/components/LanguageSelector.vue`
