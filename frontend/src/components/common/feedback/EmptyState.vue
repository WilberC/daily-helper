<script setup lang="ts">
interface Props {
  icon?: string
  title?: string
  description?: string
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'pi-inbox',
  title: 'No data available',
  description: 'There is nothing to display at the moment.',
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <i :class="['pi', icon, 'text-6xl text-surface-400 dark:text-surface-600 mb-4']"></i>
    <h3 class="text-xl font-semibold text-surface-700 dark:text-dark-text mb-2">
      {{ title }}
    </h3>
    <p class="text-surface-600 dark:text-dark-text-secondary mb-6 max-w-md">
      {{ description }}
    </p>
    <slot name="action" />
  </div>
</template>
