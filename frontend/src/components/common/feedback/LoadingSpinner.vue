<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  fullscreen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  fullscreen: false,
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  }
  return sizes[props.size]
})
</script>

<template>
  <div 
    v-if="fullscreen"
    class="fixed inset-0 bg-surface-900/50 dark:bg-black/50 flex items-center justify-center z-50"
  >
    <i :class="['pi pi-spinner pi-spin text-primary', sizeClasses]"></i>
  </div>
  <div v-else class="flex items-center justify-center p-4">
    <i :class="['pi pi-spinner pi-spin text-primary', sizeClasses]"></i>
  </div>
</template>
