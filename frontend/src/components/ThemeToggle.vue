<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'
import { NButton, NIcon } from 'naive-ui'
import { Moon, Sunny } from '@vicons/ionicons5'

const themeStore = useThemeStore()
</script>

<template>
  <n-button
    circle
    quaternary
    @click="themeStore.toggleTheme"
    :aria-label="themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    class="transition-transform hover:scale-110"
  >
    <template #icon>
      <n-icon>
        <Sunny v-if="themeStore.isDark" />
        <Moon v-else />
      </n-icon>
    </template>
  </n-button>
</template>
