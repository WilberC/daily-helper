import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
    // Initialize from localStorage or default to light mode
    const isDark = ref<boolean>(localStorage.getItem('theme') === 'dark')

    // Watch for changes and update localStorage + document class
    watch(isDark, (newValue) => {
        localStorage.setItem('theme', newValue ? 'dark' : 'light')
        updateDocumentClass(newValue)
    }, { immediate: true })

    function updateDocumentClass(dark: boolean) {
        if (dark) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
    }

    function toggleTheme() {
        isDark.value = !isDark.value
    }

    function setTheme(dark: boolean) {
        isDark.value = dark
    }

    return {
        isDark,
        toggleTheme,
        setTheme
    }
})
