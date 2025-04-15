<template>
  <v-list>
    <template v-for="item in navigationItems" :key="item.title">
      <!-- 有子菜单的项目 -->
      <v-list-group v-if="item.children?.length" :value="item.title">
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" :prepend-icon="item.icon" :title="item.title"></v-list-item>
        </template>

        <!-- 递归渲染子菜单 -->
        <v-list-item v-for="child in item.children" :key="child.title" :value="child.title" :title="child.title"
          :prepend-icon="child.icon" :to="child.path" link></v-list-item>
      </v-list-group>

      <!-- 没有子菜单的项目 -->
      <v-list-item v-else :value="item.title" :title="item.title" :prepend-icon="item.icon" :to="item.path"
        link></v-list-item>
    </template>
  </v-list>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface NavigationItem {
  title: string
  icon?: string
  path?: string
  children?: NavigationItem[]
}

const navigationItems = ref<NavigationItem[]>([
  {
    title: '论文写作',
    icon: 'mdi-book-open-page-variant',
    children: [
      {
        title: '论文列表',
        icon: 'mdi-format-list-bulleted',
        path: '/home/paperList'
      },
    ]
  },
  {
    title: '个人信息',
    icon: 'mdi-account',
    children: [
      {
        title: '个人主页',
        icon: 'mdi-home-account',
        path: '/'
      },
      {
        title: '安全信息',
        icon: 'mdi-shield-account',
        path: '/'
      }
    ]
  }
])
</script>

<style scoped lang="scss">
@use '@/assets/layout/navigation/navigationPage.scss';
</style>
