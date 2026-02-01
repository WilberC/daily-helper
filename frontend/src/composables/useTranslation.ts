import { ref, watch } from 'vue'

// Supported languages
export type Language = 'en' | 'es'

// Translation object type - using interface to avoid circular reference
interface TranslationObject {
  [key: string]: string | TranslationObject
}

// Import translations
import { en } from '@/locales/en'
import { es } from '@/locales/es'

const translations: Record<Language, TranslationObject> = {
  en,
  es,
}

// Storage key for language preference
const STORAGE_KEY = 'daily-helper-lang'

// Detect browser language
function detectBrowserLanguage(): Language {
  const browserLang = navigator.language.toLowerCase()

  // Check if browser language starts with supported language code
  if (browserLang.startsWith('es')) return 'es'
  if (browserLang.startsWith('en')) return 'en'

  // Default to English
  return 'en'
}

// Get initial language
function getInitialLanguage(): Language {
  // 1. Check localStorage
  const stored = localStorage.getItem(STORAGE_KEY) as Language | null
  if (stored && (stored === 'en' || stored === 'es')) {
    return stored
  }

  // 2. Check browser language
  const detected = detectBrowserLanguage()

  // 3. Save detected language to localStorage
  localStorage.setItem(STORAGE_KEY, detected)

  return detected
}

// Current language state
const currentLang = ref<Language>(getInitialLanguage())

// Set document language attribute for SEO
function updateDocumentLang(lang: Language) {
  document.documentElement.lang = lang
}

// Initialize document language
updateDocumentLang(currentLang.value)

// Watch for language changes and update document
watch(currentLang, (newLang) => {
  updateDocumentLang(newLang)
})

/**
 * Get nested value from object using dot notation
 * @param obj - The object to search
 * @param path - Dot-separated path (e.g., 'users.form.username')
 * @returns The value at the path, or the path itself if not found
 */
function getNestedValue(obj: TranslationObject, path: string): string {
  const keys = path.split('.')
  let current: string | TranslationObject = obj

  for (const key of keys) {
    if (current && typeof current === 'object' && key in current) {
      current = current[key]
    } else {
      // Return the path if not found (for debugging)
      console.warn(`Translation key not found: ${path}`)
      return path
    }
  }

  return typeof current === 'string' ? current : path
}

/**
 * Replace parameters in a string
 * @param str - String with {param} placeholders
 * @param params - Object with parameter values
 * @returns String with replaced parameters
 */
function replaceParams(str: string, params: Record<string, string | number>): string {
  return str.replace(/\{(\w+)\}/g, (match, key) => {
    return params[key] !== undefined ? String(params[key]) : match
  })
}

/**
 * Translation function
 * @param key - Translation key (supports dot notation)
 * @param params - Optional parameters for interpolation
 * @returns Translated string
 */
function t(key: string, params?: Record<string, string | number>): string {
  const translation = getNestedValue(translations[currentLang.value], key)

  if (params) {
    return replaceParams(translation, params)
  }

  return translation
}

/**
 * Set current language
 * @param lang - Language code to set
 */
function setLang(lang: Language) {
  currentLang.value = lang
  localStorage.setItem(STORAGE_KEY, lang)
}

/**
 * Composable for translations
 */
export function useTranslation() {
  return {
    t,
    currentLang,
    setLang,
  }
}
