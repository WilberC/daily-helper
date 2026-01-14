<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  username?: string
  size?: 'sm' | 'md' | 'lg'
  isAdmin?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  isAdmin: false,
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-12 h-12 text-lg',
  }
  return sizes[props.size]
})

const iconClass = computed(() => {
  return props.isAdmin ? 'pi-shield' : 'pi-user'
})

const colorClass = computed(() => {
  return props.isAdmin ? 'text-red-400' : 'text-blue-400'
})
</script>

<template>
  <div 
    :class="[sizeClasses, 'flex items-center justify-center rounded-full bg-surface-100 dark:bg-surface-800']"
    :title="username"
  >
    <i :class="['pi', iconClass, colorClass]"></i>
  </div>
</template>
