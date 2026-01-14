<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  padding?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
})

const paddingClasses = computed(() => {
  const paddings = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }
  return paddings[props.padding]
})
</script>

<template>
  <div :class="[paddingClasses, 'bg-surface-0 dark:bg-surface-900 rounded-lg border border-surface-200 dark:border-surface-700']">
    <slot />
  </div>
</template>
