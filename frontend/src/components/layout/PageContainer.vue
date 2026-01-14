<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'
}

const props = withDefaults(defineProps<Props>(), {
  maxWidth: 'xl',
})

const maxWidthClasses = computed(() => {
  const widths = {
    sm: 'max-w-3xl',
    md: 'max-w-5xl',
    lg: 'max-w-6xl',
    xl: 'max-w-7xl',
    '2xl': 'max-w-screen-2xl',
    full: 'max-w-full',
  }
  return widths[props.maxWidth]
})
</script>

<template>
  <main :class="[maxWidthClasses, 'mx-auto px-4 sm:px-6 lg:px-8 py-8']">
    <slot />
  </main>
</template>
