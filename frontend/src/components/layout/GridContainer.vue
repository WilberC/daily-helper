<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  cols?: '1' | '2' | '3' | '4' | '6' | '12'
  gap?: '2' | '4' | '6' | '8'
  responsive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  cols: '1',
  gap: '6',
  responsive: true,
})

const classes = computed(() => {
  const colClasses = {
    '1': 'grid-cols-1',
    '2': props.responsive ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-2',
    '3': props.responsive ? 'grid-cols-1 md:grid-cols-3' : 'grid-cols-3',
    '4': props.responsive ? 'grid-cols-1 md:grid-cols-4' : 'grid-cols-4',
    '6': props.responsive ? 'grid-cols-1 md:grid-cols-6' : 'grid-cols-6',
    '12': props.responsive ? 'grid-cols-1 md:grid-cols-12' : 'grid-cols-12',
  }
  
  const gapClasses = {
    '2': 'gap-2',
    '4': 'gap-4',
    '6': 'gap-6',
    '8': 'gap-8',
  }
  
  return [
    'grid',
    colClasses[props.cols],
    gapClasses[props.gap],
  ]
})
</script>

<template>
  <div :class="classes">
    <slot />
  </div>
</template>
