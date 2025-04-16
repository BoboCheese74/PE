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
      <!-- 步骤1：关键词输入 -->
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

      <!-- 步骤2：提纲显示与编辑 -->
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
          :loading="loading"
          @click="regenerateOutline"
        >
          重新生成
        </v-btn>
        <v-divider></v-divider>
      </div>

      <!-- 步骤3：提纲关键词显示与编辑 -->
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
          :loading="loading"
          @click="regenerateContent"
        >
          重新生成
        </v-btn>
        <v-divider></v-divider>
      </div>

      <!-- 步骤4：正文显示与编辑 -->
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

    <!-- 步骤控制按钮 -->
    <div class="step-actions mt-6">
      <!-- 步骤1的生成按钮 -->
      <v-btn
        v-if="currentStep === '1'"
        color="primary"
        @click="generate1"
        :loading="loading"
        :disabled="loading || !localData.keywords"
      >
        生成
      </v-btn>

      <!-- 步骤2-4的导航按钮 -->
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

/**
 * 使用提示消息插件
 */
const snackbar = useSnackbar()

/**
 * 组件属性定义
 */
const props = defineProps({
  // 论文处理数据，包含关键词、提纲、提纲关键词和正文内容
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

/**
 * 组件事件定义
 */
const emits = defineEmits(['update:process-data', 'complete', 'next', 'previous'])

/**
 * 组件状态
 */
// 当前步骤，从1开始
const currentStep = ref('1')
// 本地数据，用于双向绑定
const localData = ref({ ...props.processData })
// 加载状态
const loading = ref(false)
// 错误信息
const errorMessage = ref('')

/**
 * 监听属性变化，同步到本地数据
 */
watch(
  () => props.processData,
  (newVal) => {
    localData.value = { ...newVal }
  },
  { deep: true },
)

/**
 * 更新数据并发出事件
 * 将本地数据同步回父组件
 */
function updateData() {
  emits('update:process-data', { ...localData.value })
}

/**
 * 步骤1：根据关键词生成提纲
 * 调用后端API生成论文提纲
 */
async function generate1() {
  try {
    loading.value = true

    // 调用API生成提纲
    const response = await generateOutlineAPI({
      title: localData.value.keywords, // 关键词作为title参数
      language: '中文', // 默认使用中文
      LLM: 'deepseek', // 默认使用deepseek模型
    })

    // 检查响应状态
    if (response.code === 200) {
      // 设置提纲内容
      localData.value.outline = response.data.outline

      // 更新数据
      updateData()

      // 进入下一步
      currentStep.value = '2'
      emits('next', currentStep.value)
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

/**
 * 步骤2：根据提纲生成关键词
 * 提取提纲中的关键词用于后续PubMed搜索
 */
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

/**
 * 步骤3：生成论文正文
 * 根据提纲关键词搜索PubMed，获取相关论文，然后生成正文
 */
async function fetchContentWithPubmed() {
  try {
    loading.value = true

    // 检查提纲关键词是否存在
    if (!localData.value.outlineKeywords || localData.value.outlineKeywords.length === 0) {
      snackbar.show({ text: '提纲关键词不能为空', color: 'warning' })
      return { success: false }
    }

    console.log('提纲关键词:', localData.value.outlineKeywords)

    // 1. 首先调用searchPubmedAPI获取相关论文
    const pubmedResponse = await searchPubmedAPI({
      keywords: localData.value.outlineKeywords,
    })

    if (pubmedResponse.code !== 200) {
      snackbar.show({
        text: pubmedResponse.message || 'PubMed搜索失败，请稍后重试',
        color: 'error',
      })
      return { success: false }
    }

    // 获取pubmed返回的papers数据
    // 后端返回的数据格式是 { papers: ['文献[1]:摘要内容', '文献[2]:摘要内容', ...] }
    // 需要将其连接成一个字符串
    let papers = String(pubmedResponse.data.papers || '')

    console.log('处理后的PubMed论文数据:', papers.substring(0, 100) + '...')

    // 2. 然后使用pubmed数据调用editAPI生成正文
    const editResponse = await editAPI({
      language: '中文',
      title: localData.value.keywords,
      LLM: 'deepseek',
      prompt_outline: localData.value.outline,
      paper: papers,
    })

    if (editResponse.code !== 200) {
      snackbar.show({
        text: editResponse.message || '生成正文失败，请稍后重试',
        color: 'error',
      })
      return { success: false }
    }

    // 将返回的正文内容设置到表单中
    localData.value.content = editResponse.data.paper_content

    // 更新数据
    updateData()

    return { success: true }
  } catch (error) {
    console.error('生成正文出错:', error)
    let errorMsg = '网络请求出错，请检查网络连接'

    // 添加更详细的错误信息
    if (error.response) {
      console.error('错误响应:', error.response.data)
      errorMsg = `错误(${error.response.status}): ${error.response.data.detail || errorMsg}`
    }

    snackbar.show({
      text: errorMsg,
      color: 'error',
    })
    return { success: false }
  } finally {
    loading.value = false
  }
}

/**
 * 重新生成提纲
 * 使用现有关键词重新生成提纲
 */
async function regenerate() {
  await generate1()
}

/**
 * 重新生成提纲关键词
 * 使用当前提纲重新生成关键词
 */
async function regenerateOutline() {
  const result = await fetchOutlineKeywords()
  if (result.success) {
    snackbar.show({ text: '提纲关键词已更新', color: 'success' })
  }
}

/**
 * 重新生成正文
 * 使用当前提纲关键词重新搜索PubMed并生成正文
 */
async function regenerateContent() {
  const result = await fetchContentWithPubmed()
  if (result.success) {
    snackbar.show({ text: '正文已更新', color: 'success' })
  }
}

/**
 * 处理下一步操作
 * 根据当前步骤执行不同操作，确保数据正确生成后再进入下一步
 */
async function nextStep() {
  // 先更新数据到父组件
  updateData()

  // 如果是最后一步，触发完成事件
  if (currentStep.value === '4') {
    emits('complete')
    return
  }

  const nextStepNum = parseInt(currentStep.value) + 1

  // 根据当前步骤执行不同操作
  if (currentStep.value === '2') {
    // 从步骤2到步骤3，需要生成提纲关键词
    const result = await fetchOutlineKeywords()
    // 只有成功时才进入下一步
    if (result.success) {
      currentStep.value = String(nextStepNum)
      emits('next', currentStep.value)
    }
  } else if (currentStep.value === '3') {
    // 从步骤3到步骤4，需要搜索PubMed并生成正文
    const result = await fetchContentWithPubmed()
    // 只有成功时才进入下一步
    if (result.success) {
      currentStep.value = String(nextStepNum)
      emits('next', currentStep.value)
    }
  } else {
    // 其他步骤直接进入下一步（目前只有从步骤1到步骤2）
    currentStep.value = String(nextStepNum)
    emits('next', currentStep.value)
  }
}

/**
 * 处理上一步操作
 * 保存当前数据并返回上一步
 */
function previousStep() {
  // 先更新数据到父组件
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
  /* 分隔线与按钮的组合样式 */
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

  /* 步骤操作按钮区域样式 */
  .step-actions {
    display: flex;
    justify-content: flex-end;
  }

  /* 错误消息样式 */
  .error-message {
    color: red;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
}
</style>
