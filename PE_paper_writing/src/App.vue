<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useSnackbar } from '@/plugins/snackbar.ts'
import { onMounted } from 'vue'
import { initTheme, watchSystemTheme } from '@/plugins/theme'
import type { Anchor } from 'vuetify'

const snackbar = useSnackbar()

onMounted(() => {
  initTheme()
  watchSystemTheme()
})
</script>

<template>
  <v-app>
    <!-- 现有内容 -->
    <router-view />

    <!-- 添加 Snackbar 组件 -->
    <v-snackbar v-model="snackbar.isVisible.value" :color="snackbar.color.value" :timeout="snackbar.timeout.value"
      :location="snackbar.location.value" :variant="snackbar.variant.value">
      {{ snackbar.message.value }}
    </v-snackbar>
  </v-app>
</template>

<style scoped></style>
