<script setup lang="ts">
interface Props {
  label: string
  value?: string | number
}

defineProps<Props>()
</script>

<template>
  <div>
    <p class="text-sm text-surface-500 dark:text-dark-text-secondary">{{ label }}</p>
    <p class="text-lg font-medium text-surface-900 dark:text-dark-text">
      <slot>{{ value }}</slot>
    </p>
  </div>
</template>
