<script setup lang="ts">
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

// Initialize theme on mount
onMounted(() => {
  // Theme store will automatically apply the saved preference
})
</script>

<template>
  <div class="min-h-screen bg-surface-0 dark:bg-dark-bg text-surface-900 dark:text-dark-text">
    <RouterView />
  </div>
</template>

<style scoped></style>
