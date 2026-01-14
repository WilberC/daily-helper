<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6'
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  as: 'h1',
  size: 'lg',
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-xl',
    md: 'text-2xl',
    lg: 'text-2xl',
    xl: 'text-3xl',
  }
  return sizes[props.size]
})
</script>

<template>
  <component 
    :is="as" 
    :class="[sizeClasses, 'font-bold text-surface-900 dark:text-dark-text']"
  >
    <slot />
  </component>
</template>
