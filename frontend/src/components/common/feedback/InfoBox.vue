<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'info' | 'success' | 'warning' | 'error'
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'info',
})

const variantClasses = computed(() => {
  const variants = {
    info: {
      bg: 'bg-blue-950',
      border: 'border-blue-800',
      iconColor: 'text-blue-400',
      titleColor: 'text-blue-200',
      textColor: 'text-blue-300',
    },
    success: {
      bg: 'bg-green-950',
      border: 'border-green-800',
      iconColor: 'text-green-400',
      titleColor: 'text-green-200',
      textColor: 'text-green-300',
    },
    warning: {
      bg: 'bg-yellow-950',
      border: 'border-yellow-800',
      iconColor: 'text-yellow-400',
      titleColor: 'text-yellow-200',
      textColor: 'text-yellow-300',
    },
    error: {
      bg: 'bg-red-950',
      border: 'border-red-800',
      iconColor: 'text-red-400',
      titleColor: 'text-red-200',
      textColor: 'text-red-300',
    },
  }
  return variants[props.variant]
})

const defaultIcon = computed(() => {
  if (props.icon) return props.icon
  
  const icons = {
    info: 'pi-info-circle',
    success: 'pi-check-circle',
    warning: 'pi-exclamation-triangle',
    error: 'pi-times-circle',
  }
  return icons[props.variant]
})
</script>

<template>
  <div :class="[variantClasses.bg, variantClasses.border, 'border rounded-lg p-4']">
    <div class="flex items-start gap-3">
      <i :class="['pi', defaultIcon, variantClasses.iconColor, 'mt-1']"></i>
      <div class="flex-1">
        <slot :titleColor="variantClasses.titleColor" :textColor="variantClasses.textColor" />
      </div>
    </div>
  </div>
</template>
