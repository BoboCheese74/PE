<template>
  <div class="page">
    <v-text-field
      v-model="searchQuery"
      :class="{ expanded: isSearching }"
      class="search-field"
      density="compact"
      hide-details
      placeholder="搜索..."
      variant="solo"
      prepend-inner-icon="mdi-magnify"
      clearable
      :readonly="!isSearching"
      @click="handleClick"
      @focus="handleFocus"
      @blur="handleBlur"
      @click:clear="handleClear"
    ></v-text-field>

    <v-btn
      :icon="theme.global.current.value.dark ? 'mdi-weather-night' : 'mdi-weather-sunny'"
      class="theme-btn"
      @click="toggleTheme"
    ></v-btn>
  </div>
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { ref } from 'vue'

const theme = useTheme()
const isSearching = ref(false)
const searchQuery = ref('')

const handleClick = () => {
  if (!isSearching.value) {
    isSearching.value = true
  }
}

const handleFocus = () => {
  if (!isSearching.value) {
    isSearching.value = true
  }
}

const handleBlur = () => {
  if (!searchQuery.value) {
    isSearching.value = false
  }
}

const handleClear = () => {
  searchQuery.value = ''
  isSearching.value = false
}

function toggleTheme() {
  const newTheme = theme.global.current.value.dark ? 'light' : 'dark'
  theme.global.name.value = newTheme
  localStorage.setItem('theme', newTheme)
}
</script>

<style scoped lang="scss">
@use '@/assets/layout/header/headerPage.scss';
</style>
