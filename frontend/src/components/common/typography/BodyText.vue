<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'xs' | 'sm' | 'base' | 'lg'
  weight?: 'normal' | 'medium' | 'semibold'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'base',
  weight: 'normal',
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    base: 'text-base',
    lg: 'text-lg',
  }
  return sizes[props.size]
})

const weightClasses = computed(() => {
  const weights = {
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
  }
  return weights[props.weight]
})
</script>

<template>
  <p :class="[sizeClasses, weightClasses, 'text-surface-700 dark:text-dark-text-secondary']">
    <slot />
  </p>
</template>
