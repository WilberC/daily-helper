<script setup lang="ts">
interface Props {
  for?: string
  required?: boolean
}

defineProps<Props>()
</script>

<template>
  <label 
    :for="for" 
    class="text-surface-700 dark:text-dark-text font-medium"
  >
    <slot />
    <span v-if="required" class="text-red-400">*</span>
  </label>
</template>
