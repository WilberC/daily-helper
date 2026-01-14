import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
import urql from '@urql/vue'

import App from './App.vue'
import router from './router'
import { urqlClient } from './config/api'

// Import global styles
import './assets/styles/main.css'
import 'primeicons/primeicons.css'

// Custom theme preset with vibrant emerald color palette for both light and dark modes
const CustomPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{emerald.50}',
            100: '{emerald.100}',
            200: '{emerald.200}',
            300: '{emerald.300}',
            400: '{emerald.400}',
            500: '{emerald.500}',
            600: '{emerald.600}',
            700: '{emerald.700}',
            800: '{emerald.800}',
            900: '{emerald.900}',
            950: '{emerald.950}'
        },
        colorScheme: {
            light: {
                primary: {
                    color: '{emerald.600}',
                    contrastColor: '#ffffff',
                    hoverColor: '{emerald.700}',
                    activeColor: '{emerald.700}'
                },
                highlight: {
                    background: '{emerald.50}',
                    focusBackground: '{emerald.100}',
                    color: '{emerald.700}',
                    focusColor: '{emerald.800}'
                }
            },
            dark: {
                primary: {
                    color: '{emerald.400}',
                    contrastColor: '{surface.900}',
                    hoverColor: '{emerald.300}',
                    activeColor: '{emerald.300}'
                },
                highlight: {
                    background: '{emerald.950}',
                    focusBackground: '{emerald.900}',
                    color: '{emerald.300}',
                    focusColor: '{emerald.200}'
                },
                surface: {
                    0: '#0f172a',
                    50: '{slate.50}',
                    100: '{slate.100}',
                    200: '{slate.200}',
                    300: '{slate.300}',
                    400: '{slate.400}',
                    500: '{slate.500}',
                    600: '{slate.600}',
                    700: '{slate.700}',
                    800: '{slate.800}',
                    900: '#1e293b',
                    950: '#0f172a'
                }
            }
        }
    }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(urql, urqlClient)
app.use(PrimeVue, {
    theme: {
        preset: CustomPreset,
        options: {
            darkModeSelector: '.dark',
            cssLayer: {
                name: 'primevue',
                order: 'tailwind-base, primevue, tailwind-utilities'
            }
        }
    }
})
app.use(ToastService)
app.directive('tooltip', Tooltip)

app.mount('#app')

