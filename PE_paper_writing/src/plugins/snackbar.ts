import { ref } from 'vue'

interface SnackbarOptions {
  text: string
  color?: string
  variant?: string
  location?: string
  timeout?: number
}

const isVisible = ref(false)
const message = ref('')
const color = ref('success')
const timeout = ref(3000)
const location = ref('bottom')
const variant = ref('tonal')

export function useSnackbar() {
  const show = (options: SnackbarOptions) => {
    message.value = options.text
    location.value = options.location || 'top'
    color.value = options.color || 'success'
    timeout.value = options.timeout || 3000
    isVisible.value = true
    variant.value = options.variant || 'tonal'
  }

  return {
    isVisible,
    message,
    color,
    timeout,
    show,
    location,
    variant,
  }
}
