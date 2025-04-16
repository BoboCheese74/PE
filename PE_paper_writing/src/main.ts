import './assets/main.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import vuetify from '@/plugins/vuetify.js'
import SvgIcon from '@/components/SvgIcon.vue'
import './assets/iconfont/iconfont.js'

import App from './App.vue'

// 添加加载中的标记
document.documentElement.classList.add('loading')

const app = createApp(App)

async function asyncRegister() {
  const createPinia = (await import('pinia')).createPinia
  app.use(createPinia())
  const router = (await import('@/router')).default
  app.use(router)
  app.component('SvgIcon', SvgIcon)
  app.use(vuetify)
  app.mount('#app')
}

asyncRegister()
