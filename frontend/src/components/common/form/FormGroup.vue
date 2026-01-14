<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  layout?: 'stack' | 'grid'
}

const props = withDefaults(defineProps<Props>(), {
  layout: 'stack',
})

const layoutClasses = computed(() => {
  return props.layout === 'stack' 
    ? 'space-y-6' 
    : 'grid grid-cols-1 md:grid-cols-2 gap-6'
})
</script>

<template>
  <div :class="layoutClasses">
    <slot />
  </div>
</template>
