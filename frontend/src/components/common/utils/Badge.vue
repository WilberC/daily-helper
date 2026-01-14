<script setup lang="ts">
import { computed } from 'vue'
import Tag from 'primevue/tag'

interface Props {
  variant?: 'admin' | 'staff' | 'active' | 'inactive' | 'info' | 'success' | 'warning' | 'danger'
  value?: string
}

const props = defineProps<Props>()

const severity = computed(() => {
  const severities = {
    admin: 'danger',
    staff: 'info',
    active: 'success',
    inactive: 'warning',
    info: 'info',
    success: 'success',
    warning: 'warning',
    danger: 'danger',
  }
  return props.variant ? severities[props.variant] : 'info'
})

const displayValue = computed(() => {
  if (props.value) return props.value
  
  const defaults = {
    admin: 'Admin',
    staff: 'Staff',
    active: 'Active',
    inactive: 'Inactive',
    info: 'Info',
    success: 'Success',
    warning: 'Warning',
    danger: 'Danger',
  }
  return props.variant ? defaults[props.variant] : ''
})
</script>

<template>
  <Tag :value="displayValue" :severity="severity as any">
    <slot />
  </Tag>
</template>
