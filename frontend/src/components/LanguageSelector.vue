<script setup lang="ts">
import { computed } from 'vue'
import { NSelect, type SelectOption } from 'naive-ui'
import { useTranslation } from '@/composables/useTranslation'
import type { Language } from '@/composables/useTranslation'

const { currentLang, setLang } = useTranslation()

const languageOptions: SelectOption[] = [
  { label: '🇺🇸 English', value: 'en' },
  { label: '🇪🇸 Español', value: 'es' },
]

const selectedLanguage = computed({
  get: () => currentLang.value,
  set: (value: Language) => setLang(value),
})
</script>

<template>
  <n-select
    v-model:value="selectedLanguage"
    :options="languageOptions"
    :consistent-menu-width="false"
    class="w-40"
    size="medium"
  />
</template>

<style scoped>
/* Additional styling if needed */
</style>
