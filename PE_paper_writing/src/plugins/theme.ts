import { useTheme } from 'vuetify'

export function initTheme() {
  // 获取保存的主题
  const savedTheme = localStorage.getItem('theme')
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  // 决定使用哪个主题
  const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light')

  // 在 HTML 标签上设置主题类
  document.documentElement.classList.add(initialTheme)

  const theme = useTheme()
  theme.global.name.value = initialTheme

  // 移除加载中的标记
  document.documentElement.classList.remove('loading')
}

// 监听系统主题变化
export function watchSystemTheme() {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      const theme = useTheme()
      theme.global.name.value = e.matches ? 'dark' : 'light'
    }
  })
}
