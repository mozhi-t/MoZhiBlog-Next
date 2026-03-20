import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { injectAnalyticsSdkScripts } from './config/site'
import './styles/global.scss'
import 'highlight.js/styles/github.css'

const app = createApp(App)

injectAnalyticsSdkScripts()

// Use Pinia for state management
app.use(createPinia())

// Use Vue Router
app.use(router)

// Mount app
app.mount('#app')
