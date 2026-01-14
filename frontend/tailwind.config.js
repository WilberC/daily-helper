import primeui from 'tailwindcss-primeui'

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Dark mode color palette
        'dark-bg': '#0f172a',
        'dark-surface': '#1e293b',
        'dark-border': '#334155',
        'dark-text': '#f1f5f9',
        'dark-text-secondary': '#94a3b8',
        // Primary emerald accent
        'primary': {
          DEFAULT: '#10b981',
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
          950: '#022c22'
        }
      },
    },
  },
  plugins: [primeui],
}
