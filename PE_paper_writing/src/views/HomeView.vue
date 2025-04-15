<template>
  <v-layout class="rounded rounded-md border">
    <v-app-bar class="bar">
      <template v-slot:prepend>
        <svg-icon class="logo" iconName="icon-icon_610d05dc8272f"></svg-icon>
      </template>
      <v-app-bar-title class="title">AI 工作台</v-app-bar-title>
      <headerPage></headerPage>
    </v-app-bar>

    <v-navigation-drawer class="navigation" permanent>
      <navigationPage />
    </v-navigation-drawer>

    <v-main class="main-view">
      <div class="pa-4">
        <router-view></router-view>
      </div>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import headerPage from '@/components/layout/header/headerPage.vue';
import navigationPage from '@/components/layout/navigation/navigationPage.vue';

</script>

<style scoped src="@/assets/homeView/homeView.scss" />
