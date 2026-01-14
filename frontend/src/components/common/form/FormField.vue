<script setup lang="ts">
interface Props {
  label?: string
  error?: string
  required?: boolean
  for?: string
}

defineProps<Props>()
</script>

<template>
  <div class="flex flex-col gap-2">
    <label v-if="label" :for="for" class="text-surface-700 dark:text-dark-text font-medium">
      {{ label }}
      <span v-if="required" class="text-red-400">*</span>
    </label>
    
    <slot />
    
    <small v-if="error" class="text-sm text-red-400">{{ error }}</small>
  </div>
</template>
