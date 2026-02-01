<script setup lang="ts">
import { NFormItem } from 'naive-ui'

interface Props {
  label?: string
  error?: string
  required?: boolean
  for?: string
}

defineProps<Props>()
</script>

<template>
  <n-form-item
    :label="label"
    :validation-status="error ? 'error' : undefined"
    :feedback="error"
    :required="required"
  >
    <slot />
  </n-form-item>
</template>
