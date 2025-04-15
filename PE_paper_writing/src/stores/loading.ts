import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
  const isLoading = ref(false)

  function start() {
    isLoading.value = true
  }

  function end() {
    isLoading.value = false
  }

  return {
    isLoading,
    start,
    end,
  }
})
