import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import urql from '@urql/vue'

import App from './App.vue'
import router from './router'
import { urqlClient } from './config/api'

// Import global styles
import './assets/styles/main.css'
import 'primeicons/primeicons.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(urql, urqlClient)
app.use(PrimeVue)
app.use(ToastService)

app.mount('#app')
