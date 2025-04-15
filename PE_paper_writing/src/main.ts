import './assets/main.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import vuetify from '@/plugins/vuetify.js'
import SvgIcon from '@/components/SvgIcon.vue'
import './assets/iconfont/iconfont.js'

import App from './App.vue'
import router from './router'

// 添加加载中的标记
document.documentElement.classList.add('loading')

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('SvgIcon', SvgIcon)
app.use(vuetify)

app.mount('#app')
