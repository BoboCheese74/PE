import js from '@eslint/js'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import vuePlugin from 'eslint-plugin-vue'
import type { Linter } from 'eslint'

const config: Linter.FlatConfig[] = [
  // JavaScript 基础配置
  js.configs.recommended,

  // TypeScript 配置
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin as any, // 使用类型断言解决类型不匹配问题
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
    },
  },

  // Vue 配置
  {
    files: ['**/*.vue'],
    plugins: {
      vue: vuePlugin,
    },
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },

  // 通用配置
  {
    files: ['**/*.{js,ts,vue}'],
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    },
  },
]

export default config
