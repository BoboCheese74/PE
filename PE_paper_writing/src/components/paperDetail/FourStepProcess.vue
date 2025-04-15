<template>
  <div class="four-step-process">
    <!-- 步骤指示器 -->
    <v-stepper v-model="currentStep" class="mb-6">
      <v-stepper-header>
        <v-stepper-item value="1">步骤 1</v-stepper-item>
        <v-divider></v-divider>
        <v-stepper-item value="2">步骤 2</v-stepper-item>
        <v-divider></v-divider>
        <v-stepper-item value="3">步骤 3</v-stepper-item>
        <v-divider></v-divider>
        <v-stepper-item value="4">步骤 4</v-stepper-item>
      </v-stepper-header>
    </v-stepper>

    <!-- 步骤内容 -->
    <div class="step-content">
      <!-- 步骤1：关键词 -->
      <div class="mb-4">
        <v-text-field
          v-model="localData.keywords"
          label="关键词"
          hint="请输入相关关键词，用逗号分隔"
          :rules="paperRules.keywords"
          variant="outlined"
        ></v-text-field>
      </div>

      <!-- 分隔线和重新生成按钮（步骤2-4） -->
      <div v-if="currentStep >= 2" class="divider-with-button my-4">
        <v-divider></v-divider>
        <v-btn
          variant="text"
          color="primary"
          class="mx-2 regenerate-btn"
          :loading="loading"
          @click="regenerate"
        >
          重新生成
        </v-btn>
        <v-divider></v-divider>
      </div>

      <!-- 步骤2：提纲 -->
      <div v-if="currentStep >= 2" class="mb-4">
        <v-textarea
          v-model="localData.outline"
          :rules="paperRules.outline"
          label="提纲"
          variant="outlined"
          auto-grow
          rows="5"
        ></v-textarea>
      </div>

      <!-- 分隔线和重新生成按钮（步骤3-4） -->
      <div v-if="currentStep >= 3" class="divider-with-button my-4">
        <v-divider></v-divider>
        <v-btn
          variant="text"
          color="primary"
          class="mx-2 regenerate-btn"
          @click="regenerateOutline"
        >
          重新生成
        </v-btn>
        <v-divider></v-divider>
      </div>

      <!-- 步骤3：提纲关键词 -->
      <div v-if="currentStep >= 3" class="mb-4">
        <v-textarea
          v-model="localData.outlineKeywords"
          label="提纲关键词"
          variant="outlined"
          auto-grow
          rows="3"
        ></v-textarea>
      </div>

      <!-- 分隔线和重新生成按钮（步骤4） -->
      <div v-if="currentStep >= 4" class="divider-with-button my-4">
        <v-divider></v-divider>
        <v-btn
          variant="text"
          color="primary"
          class="mx-2 regenerate-btn"
          @click="regenerateContent"
        >
          重新生成
        </v-btn>
        <v-divider></v-divider>
      </div>

      <!-- 步骤4：正文 -->
      <div v-if="currentStep >= 4" class="mb-4">
        <v-textarea
          v-model="localData.content"
          label="正文"
          variant="outlined"
          auto-grow
          rows="10"
        ></v-textarea>
      </div>
    </div>

    <!-- 步骤按钮 -->
    <div class="step-actions mt-6">
      <v-btn
        v-if="currentStep === '1'"
        color="primary"
        @click="generate1"
        :loading="loading"
        :disabled="loading || !localData.keywords"
      >
        生成
      </v-btn>

      <div v-else class="d-flex">
        <v-btn v-if="currentStep > 1" variant="outlined" class="me-4" @click="previousStep">
          上一步
        </v-btn>

        <v-btn color="primary" :loading="loading" @click="nextStep">
          {{ currentStep === '4' ? '完成' : '下一步' }}
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue'
import { generateOutlineAPI, getKeywordAPI, searchPubmedAPI, editAPI } from '@/apis/paper'
import { useSnackbar } from '@/plugins/snackbar.ts'
import { paperRules } from '@/rules/paper4'

const snackbar = useSnackbar()

const props = defineProps({
  processData: {
    type: Object,
    default: () => ({
      keywords: '',
      outline: '',
      outlineKeywords: '',
      content: '',
    }),
  },
})

const emits = defineEmits(['update:process-data', 'complete', 'next', 'previous'])

const currentStep = ref('1')
const localData = ref({ ...props.processData })
const loading = ref(false)
const errorMessage = ref('')

// 监听属性变化
watch(
  () => props.processData,
  (newVal) => {
    localData.value = { ...newVal }
  },
  { deep: true },
)

// 更新数据并发出事件
function updateData() {
  emits('update:process-data', { ...localData.value })
}

// 生成内容（步骤1）
async function generate1() {
  try {
    loading.value = true

    // 调用API生成提纲
    const response = await generateOutlineAPI({
      title: localData.value.keywords, // 关键词作为title参数
      language: '中文', // 默认中文
      LLM: 'deepseek', // 默认LLM模型
    })

    // 检查响应状态
    if (response.code === 200) {
      // 设置提纲内容
      localData.value.outline = response.data.outline

      // 更新数据
      updateData()

      // 进入下一步
      currentStep.value = '2'
    } else {
      // 处理非200状态码
      errorMessage.value = response.message || '生成提纲失败，请稍后重试'
      snackbar.show({ text: errorMessage.value, color: 'error' })
    }
  } catch (error) {
    // 处理API调用异常
    errorMessage.value = '网络请求出错，请检查网络连接'
    snackbar.show({ text: errorMessage.value, color: 'error' })
  } finally {
    loading.value = false
  }
}

async function generate2() {}

// 生成提纲关键词（步骤2）
async function fetchOutlineKeywords() {
  try {
    loading.value = true

    // 调用API获取提纲关键词
    const response = await getKeywordAPI({
      content: localData.value.outline,
    })

    console.log('获取关键词API响应:', response)

    // 检查响应状态
    if (response.code === 200) {
      // 设置提纲关键词内容
      localData.value.outlineKeywords = String(response.data.keywords)

      // 更新数据
      updateData()
      return { success: true }
    } else {
      // 处理非200状态码
      const errorMsg = response.message || '获取提纲关键词失败，请稍后重试'
      snackbar.show({ text: errorMsg, color: 'error' })
      return { success: false }
    }
  } catch (error) {
    // 处理API调用异常
    console.error('获取提纲关键词出错:', error)
    snackbar.show({
      text: '网络请求出错，请检查网络连接',
      color: 'error',
    })
    return { success: false }
  } finally {
    loading.value = false
  }
}

// 重新生成内容
function regenerate() {
  generate1()
  // 实现重新生成逻辑
}

// 重新生成提纲关键词
async function regenerateOutline() {
  console.log('重新生成提纲关键词')
  await fetchOutlineKeywords()
  // 注意：这里不需要改变步骤，只是更新关键词
}

// 重新生成正文
function regenerateContent() {
  console.log('重新生成正文')
  // 实现重新生成逻辑
}

// 下一步 - 添加步骤3对接searchPubmedAPI和editAPI
async function nextStep() {
  updateData()

  if (currentStep.value === '4') {
    emits('complete')
    return
  }

  const nextStepNum = parseInt(currentStep.value) + 1

  // 当从步骤2进入步骤3时，调用getKeywordAPI
  if (currentStep.value === '2') {
    const result = await fetchOutlineKeywords()

    // 只有成功时才进入下一步
    if (result.success) {
      currentStep.value = String(nextStepNum)
      emits('next', currentStep.value)
    }
  }
  // 当从步骤3进入步骤4时，调用searchPubmedAPI和editAPI
  else if (currentStep.value === '3') {
    try {
      loading.value = true

      // 检查提纲关键词是否存在
      if (!localData.value.outlineKeywords || localData.value.outlineKeywords.length === 0) {
        snackbar.show({ text: '提纲关键词不能为空', color: 'warning' })
        loading.value = false
        return
      }

      console.log('提纲关键词:', localData.value.outlineKeywords)

      // 1. 首先调用searchPubmedAPI
      const pubmedResponse = await searchPubmedAPI({
        keywords: localData.value.outlineKeywords,
      })

      if (pubmedResponse.code !== 200) {
        snackbar.show({
          text: pubmedResponse.message || 'PubMed搜索失败，请稍后重试',
          color: 'error',
        })
        loading.value = false
        return
      }

      // 获取pubmed返回的papers数据
      const papers = String(pubmedResponse.data.papers)

      console.log('获取到PubMed论文数据:', papers)
      console.log('提纲内容:', localData.value.outline)
      console.log('关键词:', localData.value.keywords)

      // 2. 然后使用pubmed数据调用editAPI
      const editResponse = await editAPI({
        language: '中文',
        title: localData.value.keywords,
        prompt_outline: localData.value.outline,
        paper: papers,
        LLM: 'deepseek',
      })

      if (editResponse.code !== 200) {
        snackbar.show({
          text: editResponse.message || '生成正文失败，请稍后重试',
          color: 'error',
        })
        loading.value = false
        return
      }

      // 将返回的正文内容设置到表单中
      localData.value.content = editResponse.data.paper_content

      // 更新数据
      updateData()

      // 进入下一步
      currentStep.value = String(nextStepNum)
      emits('next', currentStep.value)
    } catch (error) {
      console.error('生成正文出错:', error)
      snackbar.show({
        text: '网络请求出错，请检查网络连接',
        color: 'error',
      })
    } finally {
      loading.value = false
    }
  } else {
    // 其他步骤直接进入下一步
    currentStep.value = String(nextStepNum)
    emits('next', currentStep.value)
  }
}

// 上一步
function previousStep() {
  updateData()

  const prevStepNum = parseInt(currentStep.value) - 1
  if (prevStepNum >= 1) {
    currentStep.value = String(prevStepNum)
    emits('previous', currentStep.value)
  }
}
</script>

<style lang="scss" scoped>
.four-step-process {
  .divider-with-button {
    position: relative;
    display: flex;
    align-items: center;

    .v-divider {
      flex-grow: 1;
    }

    .regenerate-btn {
      white-space: nowrap;
    }
  }

  .step-actions {
    display: flex;
    justify-content: flex-end;
  }

  .error-message {
    color: red;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
}
</style>
