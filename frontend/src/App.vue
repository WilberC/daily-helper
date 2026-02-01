<script setup lang="ts">
import { computed } from 'vue'
import { NConfigProvider, NMessageProvider, NDialogProvider, darkTheme } from 'naive-ui'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const naiveTheme = computed(() => (themeStore.isDark ? darkTheme : null))

const themeOverrides = {
  common: {
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43',
    primaryColorSuppl: '#34d399',

    // Enhanced border radius for softer feel
    borderRadius: '12px',
    borderRadiusSmall: '8px',

    // Improved shadows
    boxShadow1: '0 1px 2px -1px rgba(0, 0, 0, 0.08), 0 1px 4px -1px rgba(0, 0, 0, 0.06)',
    boxShadow2: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    boxShadow3: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',

    // Typography
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    fontSizeMedium: '14px',
    fontSizeLarge: '16px',

    // Spacing
    heightMedium: '40px',
    heightLarge: '48px',
  },
  Card: {
    borderRadius: '16px',
    paddingMedium: '24px',
    paddingLarge: '32px',
    // Glassmorphic effect
    color: 'rgba(255, 255, 255, 0.85)',
    colorModal: 'rgb(255, 255, 255)',
    boxShadow:
      '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05), 0 0 20px rgba(24, 160, 88, 0.05)',
  },
  Button: {
    borderRadiusMedium: '10px',
    borderRadiusLarge: '12px',
    paddingMedium: '0 20px',
    paddingLarge: '0 24px',
    // Enhanced hover effects
    colorHoverPrimary: '#36ad6a',
    colorPressedPrimary: '#0c7a43',
  },
  Input: {
    borderRadius: '10px',
    heightMedium: '40px',
    heightLarge: '48px',
    paddingMedium: '0 14px',
    paddingLarge: '0 16px',
  },
  DataTable: {
    borderRadius: '12px',
    thPaddingMedium: '16px',
    tdPaddingMedium: '16px',
  },
  Dialog: {
    borderRadius: '20px',
    padding: '32px',
  },
  Tabs: {
    tabBorderRadius: '10px',
    tabPaddingMediumLine: '12px 20px',
  },
}

// Dark mode specific overrides
const darkThemeOverrides = {
  ...themeOverrides,
  Card: {
    ...themeOverrides.Card,
    color: 'rgba(31, 41, 55, 0.8)',
    colorModal: 'rgb(31, 41, 55)',
    boxShadow:
      '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2), 0 0 30px rgba(24, 160, 88, 0.1)',
  },
}

const currentThemeOverrides = computed(() =>
  themeStore.isDark ? darkThemeOverrides : themeOverrides,
)
</script>

<template>
  <n-config-provider :theme="naiveTheme" :theme-overrides="currentThemeOverrides">
    <n-message-provider>
      <n-dialog-provider>
        <div class="min-h-screen animate-fade-in">
          <RouterView />
        </div>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped></style>
