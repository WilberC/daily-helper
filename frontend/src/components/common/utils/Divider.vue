<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  spacing?: '2' | '4' | '6' | '8'
}

const props = withDefaults(defineProps<Props>(), {
  spacing: '4',
})

const spacingClasses = computed(() => {
  const spacings = {
    '2': 'my-2',
    '4': 'my-4',
    '6': 'my-6',
    '8': 'my-8',
  }
  return spacings[props.spacing]
})
</script>

<template>
  <hr :class="[spacingClasses, 'border-t border-surface-200 dark:border-surface-700']" />
</template>
