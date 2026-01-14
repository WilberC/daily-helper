<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  direction?: 'row' | 'col'
  justify?: 'start' | 'center' | 'end' | 'between' | 'around'
  align?: 'start' | 'center' | 'end' | 'stretch'
  gap?: '1' | '2' | '3' | '4' | '6' | '8'
}

const props = withDefaults(defineProps<Props>(), {
  direction: 'row',
  justify: 'start',
  align: 'start',
  gap: '4',
})

const classes = computed(() => {
  const directionClass = props.direction === 'row' ? 'flex-row' : 'flex-col'
  
  const justifyClasses = {
    start: 'justify-start',
    center: 'justify-center',
    end: 'justify-end',
    between: 'justify-between',
    around: 'justify-around',
  }
  
  const alignClasses = {
    start: 'items-start',
    center: 'items-center',
    end: 'items-end',
    stretch: 'items-stretch',
  }
  
  const gapClasses = {
    '1': 'gap-1',
    '2': 'gap-2',
    '3': 'gap-3',
    '4': 'gap-4',
    '6': 'gap-6',
    '8': 'gap-8',
  }
  
  return [
    'flex',
    directionClass,
    justifyClasses[props.justify],
    alignClasses[props.align],
    gapClasses[props.gap],
  ]
})
</script>

<template>
  <div :class="classes">
    <slot />
  </div>
</template>
