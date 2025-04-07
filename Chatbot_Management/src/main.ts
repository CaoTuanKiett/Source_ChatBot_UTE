import './assets/styles/index.less'

import { VueQueryPlugin } from '@tanstack/vue-query'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import Vue3Marquee from 'vue3-marquee'

// // import ChatbotUI from 'chatbot-ui-ute'
// import ChatbotUI from 'chatbot-ui-ute'
// import 'chatbot-ui-ute/dist/style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import Curtain from './components/Curtain.vue'
import i18n from './i18n'
import router from './router'
import { useAuthStore } from './stores/auth'

startApp()

async function startApp() {
    const app = createApp(App)
    const initializingApp = createApp(Curtain, { show: true, spinner: true })

    // app.use(ChatbotUI)
    // app.component('ChatbotUI', ChatbotUI)
    app.use(createPinia())
    app.use(VueQueryPlugin)
    app.use(i18n)
    app.use(router)
    app.use(Vue3Marquee)
    app.use(ElementPlus)
    // app.use(AOS)

    try {
        initializingApp.mount('#app')
        console.info(
            ':::startApp -> Attempting to auto refresh token before startup, also persisting auth data into store'
        )
        const authStore = useAuthStore()
        await authStore.doPersistAuthData()
        console.info(':::startApp -> Persisted auth data into store')
    } catch {
        // TODO: catch error to start app on success or failure
    } finally {
        initializingApp.unmount()
    }

    app.mount('#app')
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true // Chỉ chạy một lần
    })
}
