<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'primary' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
})

const variantClasses = computed(() => {
  const variants = {
    default: 'text-surface-700 dark:text-dark-text',
    primary: 'text-surface-900 dark:text-dark-text',
    secondary: 'text-surface-600 dark:text-dark-text-secondary',
  }
  return variants[props.variant]
})
</script>

<template>
  <h2 :class="[variantClasses, 'text-xl font-semibold']">
    <slot />
  </h2>
</template>
