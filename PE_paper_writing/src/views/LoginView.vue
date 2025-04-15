<template>
  <div class="page">
    <v-btn :icon="theme.global.current.value.dark ? 'mdi-weather-night' : 'mdi-weather-sunny'" class="theme-btn"
      variant="text" @click="toggleTheme"></v-btn>
    <v-card class="login-card" variant="tonal">
      <div class="card-header" :style="{ ...headerStyle, 'clip-path': sliderOffset }">
        <div class="in-content">
          <div class="tittle-content">
            <svg-icon class="logo" iconName="icon-icon_610d05dc8272f"></svg-icon>
            <h2 class="title">AI 工作台登录</h2>
          </div>
          <div class="comment">
            <h4>还没有账号？先去</h4>
            <h4 class="in-active" :style="cbStyle" @click="toggleForm">注册</h4>
            <h4>吧</h4>
          </div>
        </div>
        <div class="up-content">
          <div class="tittle-content">
            <svg-icon class="logo" iconName="icon-icon_610d05dc8272f"></svg-icon>
            <h2 class="title">AI 工作台注册</h2>
          </div>
          <div class="comment">
            <h4>已经注册了？快去</h4>
            <h4 class="up-active" :style="cbStyle" @click="toggleForm">登录</h4>
            <h4>吧</h4>
          </div>
        </div>
      </div>
      <div class="main-form">
        <v-sheet class="signup-sheet">
          <v-form ref="signupForm" class="signup-form">
            <v-text-field class="input username-input" v-model="signupUser.username" :rules="UPusernameRules"
              label="用户名"></v-text-field>

            <v-text-field class="input password-inpur" v-model="signupUser.password" :rules="UPpasswordRules"
              label="密码"></v-text-field>

            <v-text-field class="input invitation-code-input" v-model="signupUser.invitation_code"
              :rules="UPinvitationCodeRules" label="邀请码"></v-text-field>

            <div class="btn-content">
              <v-btn class="sigup-btn" color="success" type="submit" block>
                注册
              </v-btn>
            </div>

          </v-form>
        </v-sheet>
        <v-sheet class="signin-sheet">
          <v-form ref="signinForm" class="signin-form" @submit.prevent="siginBtn">
            <v-text-field class="input username-input" v-model="signinUser.username" :rules="INusernameRules"
              label="用户名"></v-text-field>

            <v-text-field class="input password-inpur" v-model="signinUser.password" :rules="INpasswordRules"
              label="密码"></v-text-field>

            <div class="btn-content">
              <v-btn class="sigin-btn" color="success" type="submit" block>
                登录
              </v-btn>
            </div>
          </v-form>
        </v-sheet>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTheme } from 'vuetify'
import { computed } from 'vue'
import { signupRules } from '@/rules/signupInfo.ts'
import { signinRules } from '@/rules/signinInfo.ts'
import { useSnackbar } from '@/plugins/snackbar.ts'
import router from '@/router'

const snackbar = useSnackbar()

// 登录表单————————————————————————————————————————————————————————
const signinUser = ref({
  username: '',
  password: '',
})
const signinForm = ref()
const INusernameRules = signinRules.username
const INpasswordRules = signinRules.password

const siginBtn = async () => {
  const isValid = await signinForm.value.validate()
  console.log('登录表单验证结果:', isValid)
  if (isValid) {
    // 这里可以添加登录逻辑
    snackbar.show({ text: '登录成功', location: 'top', })
    router.push('/')
  } else {
    console.log('登录失败')
    snackbar.show({ text: '登录失败', color: 'error' })
  }
}

// 注册表单————————————————————————————————————————————————————————
const signupUser = ref({
  username: '',
  password: '',
  invitation_code: '',
})

const signupForm = ref()

const UPusernameRules = signupRules.username
const UPpasswordRules = signupRules.password
const UPinvitationCodeRules = signupRules.invitationCode

// 动态样式—————————————————————————————————————————————————————————
// 这里的样式是为了实现登录和注册的切换
const isActive = ref(false)

const sliderOffset = computed(() => {
  return `rect(0 ${isActive.value ? 100 : 50}% 100% ${isActive.value ? 50 : 0}% round 0px)`
})

const toggleForm = () => {
  isActive.value = !isActive.value
}

// 主题切换——————————————————————————————————————————————————————————

const theme = useTheme()

const headerStyle = computed(() => {
  let isDark = theme.global.current.value.dark
  return {
    '--base-color': isDark ? '24, 45, 76' : '0, 175, 179',
  }
})

const cbStyle = computed(() => {
  let isDark = theme.global.current.value.dark
  return {
    'color': isDark ? 'rgb(0, 204, 255)' : 'rgba(0, 0, 255, 0.400)',
  }
})

function toggleTheme() {
  const newTheme = theme.global.current.value.dark ? 'light' : 'dark'
  theme.global.name.value = newTheme
  localStorage.setItem('theme', newTheme)
}
</script>

<style scoped lang="scss">
@use '@/assets/loginView/loginView.scss';

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
