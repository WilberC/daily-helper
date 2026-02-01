<script setup lang="ts">
import { NAlert } from 'naive-ui'
import { computed } from 'vue'

interface Props {
  variant?: 'info' | 'success' | 'warning' | 'error'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'info',
})

const alertType = computed(() => {
  const map = {
    info: 'info',
    success: 'success',
    warning: 'warning',
    error: 'error',
  } as const
  return map[props.variant]
})
</script>

<template>
  <n-alert :type="alertType" class="rounded-lg">
    <slot />
  </n-alert>
</template>
