import { createRouter, createWebHistory } from 'vue-router'
import { useUserInfoStore } from '@/stores/userinfo.store'
import HomeView from '../views/HomeView.vue'

const userInfoStore = useUserInfoStore()

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home/paperList',
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      children: [
        {
          path: 'paperList',
          name: 'paperList',
          component: () => import('@/components/paperList/paperListPage.vue'),
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      meta: {
        noAuth: true,
      },
      component: () => import('@/views/LoginView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  if (!to.meta.noAuth) {
    if (userInfoStore.authFormLocal()) {
      next()
      return
    } else {
      // 未登录，跳转到登录页
      router.push('/login')
      return // 停止当前路由守卫的执行
    }
  } else {
    next()
    return
  }
})

export default router
