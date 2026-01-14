<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  name: string
  size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl'
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'base',
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    base: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
  }
  return sizes[props.size]
})
</script>

<template>
  <i :class="['pi', name, sizeClasses, color]"></i>
</template>
