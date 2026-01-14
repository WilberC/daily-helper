<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'
import Button from 'primevue/button'

const themeStore = useThemeStore()
</script>

<template>
  <Button
    :icon="themeStore.isDark ? 'pi pi-sun' : 'pi pi-moon'"
    :aria-label="themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    severity="secondary"
    text
    rounded
    @click="themeStore.toggleTheme"
    v-tooltip.bottom="themeStore.isDark ? 'Light Mode' : 'Dark Mode'"
  />
</template>
