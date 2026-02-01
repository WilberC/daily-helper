<script setup lang="ts">
import { computed } from 'vue'
import { NTag } from 'naive-ui'

interface Props {
  variant?: 'admin' | 'staff' | 'active' | 'inactive' | 'info' | 'success' | 'warning' | 'danger'
  value?: string
}

const props = defineProps<Props>()

const tagType = computed(() => {
  const typeMap = {
    admin: 'error',
    staff: 'warning',
    active: 'success',
    inactive: 'default',
    info: 'info',
    success: 'success',
    warning: 'warning',
    danger: 'error',
  } as const
  return props.variant ? typeMap[props.variant] : 'info'
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
  <n-tag :type="tagType" size="small" round>
    <slot>{{ displayValue }}</slot>
  </n-tag>
</template>
