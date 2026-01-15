<script setup lang="ts">
/**
 * Displays error text with appropriate styling and semantics.
 * Automatically includes proper ARIA attributes for screen readers.
 * @component
 */

interface Props {
  /**
   * Error message to display
   */
  message?: string
}

withDefaults(defineProps<Props>(), {
  message: '',
})
</script>

<template>
  <div
    class="text-red-600 dark:text-red-400 text-sm mt-1 flex items-center gap-1"
    role="alert"
    aria-live="polite"
  >
    <i class="pi pi-exclamation-circle" aria-hidden="true" />
    <span v-if="message">{{ message }}</span>
    <slot v-else />
  </div>
</template>
