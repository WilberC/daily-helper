<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  align?: 'left' | 'center' | 'right'
}

const props = withDefaults(defineProps<Props>(), {
  align: 'left',
})

const alignClasses = computed(() => {
  const aligns = {
    left: 'justify-start',
    center: 'justify-center',
    right: 'justify-end',
  }
  return aligns[props.align]
})
</script>

<template>
  <div :class="['flex gap-4', alignClasses]">
    <slot />
  </div>
</template>
