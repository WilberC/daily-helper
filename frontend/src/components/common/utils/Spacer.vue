<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: '1' | '2' | '3' | '4' | '6' | '8' | '12'
  direction?: 'vertical' | 'horizontal'
}

const props = withDefaults(defineProps<Props>(), {
  size: '4',
  direction: 'vertical',
})

const classes = computed(() => {
  const sizeClasses = {
    vertical: {
      '1': 'h-1',
      '2': 'h-2',
      '3': 'h-3',
      '4': 'h-4',
      '6': 'h-6',
      '8': 'h-8',
      '12': 'h-12',
    },
    horizontal: {
      '1': 'w-1',
      '2': 'w-2',
      '3': 'w-3',
      '4': 'w-4',
      '6': 'w-6',
      '8': 'w-8',
      '12': 'w-12',
    },
  }
  
  return sizeClasses[props.direction][props.size]
})
</script>

<template>
  <div :class="classes" aria-hidden="true"></div>
</template>
