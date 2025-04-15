import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

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
      // meta: {
      //   noAuth: true,
      // },
      component: () => import('@/views/LoginView.vue'),
    },
  ],
})

export default router
