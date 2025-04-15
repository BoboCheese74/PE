<template>
  <div class="two-step-process">
    <!-- 步骤指示器 -->
    <v-stepper v-model="currentStep" class="mb-6">
      <v-stepper-header>
        <v-stepper-item value="1">步骤 1</v-stepper-item>
        <v-divider></v-divider>
        <v-stepper-item value="2">步骤 2</v-stepper-item>
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
          variant="outlined"
        ></v-text-field>
      </div>

      <!-- 图片上传区域 -->
      <div v-if="supportsImages" class="mb-6">
        <v-file-upload
          v-model="fileInputs"
          accept="image/png, image/jpeg, image/jpg"
          label="上传图表"
          title="只能上传jpg/png文件，且不超过500kb"
          :rules="fileRules"
          multiple
          show-size
          clearable
          density="compact"
          variant="outlined"
          @update:model-value="handleFileChange"
        ></v-file-upload>
      </div>

      <!-- 分隔线和重新生成按钮（步骤2） -->
      <div v-if="currentStep === '2'" class="divider-with-button my-4">
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

      <!-- 步骤2：正文 -->
      <div v-if="currentStep === '2'" class="mb-4">
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
      <v-btn v-if="currentStep === '1'" color="primary" @click="generate"> 生成 </v-btn>

      <div v-else class="d-flex">
        <v-btn variant="outlined" class="me-4" @click="previousStep"> 上一步 </v-btn>

        <v-btn color="primary" @click="complete"> 完成 </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  processData: {
    type: Object,
    default: () => ({
      keywords: '',
      images: [],
      content: '',
    }),
  },
  supportsImages: {
    type: Boolean,
    default: true,
  },
})

const emits = defineEmits(['update:process-data', 'complete', 'next', 'previous'])

const currentStep = ref('1')
const localData = ref({ ...props.processData })
const fileInputs = ref<File[]>([])

// 保存上次的文件集合，用于与新上传文件合并
const lastSelectedFiles = ref<File[]>([])

// 文件上传规则
const fileRules = [
  (v) =>
    !v ||
    !v.length ||
    v.reduce((size, file) => size + file.size, 0) < 500 * 1024 ||
    '文件大小总和不能超过500KB',
  (v) =>
    !v ||
    !v.length ||
    v.every((file) => ['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) ||
    '只允许jpg/png格式',
]

// 监听属性变化
watch(
  () => props.processData,
  (newVal) => {
    localData.value = { ...newVal }
  },
  { deep: true },
)

// 处理文件变化 - 改为合并文件而不是替换
function handleFileChange(files) {
  if (!files) {
    // 如果清空了文件，重置所有状态
    localData.value.images = []
    lastSelectedFiles.value = []
    return
  }

  // 检查是否是通过拖放添加的文件(文件数量增加了)或通过点击选择文件(完全替换)
  const isDragAndDrop =
    files.length > lastSelectedFiles.value.length && lastSelectedFiles.value.length > 0

  if (isDragAndDrop) {
    // 拖放情况：保留现有文件集合，不需要额外处理
    lastSelectedFiles.value = files
    localData.value.images = files
  } else {
    // 点击选择情况：合并旧文件和新文件
    // 为避免重复，创建一个Map用文件名和大小作为键
    const existingFilesMap = new Map()
    lastSelectedFiles.value.forEach((file) => {
      const key = `${file.name}_${file.size}`
      existingFilesMap.set(key, file)
    })

    // 添加新文件，避免重复
    files.forEach((file) => {
      const key = `${file.name}_${file.size}`
      existingFilesMap.set(key, file)
    })

    // 将合并后的文件集合转换回数组
    const mergedFiles = Array.from(existingFilesMap.values())

    // 更新组件的v-model和本地数据
    // 注意：这会触发v-file-upload的更新
    fileInputs.value = mergedFiles
    lastSelectedFiles.value = mergedFiles
    localData.value.images = mergedFiles
  }

  // 记录上传的文件数量
  console.log('当前文件数量:', localData.value.images.length)
}

// 更新数据并发出事件
function updateData() {
  emits('update:process-data', { ...localData.value })
}

// 生成内容
function generate() {
  console.log('生成基于关键词和图片的内容')
  console.log('已上传图片数量:', fileInputs.value?.length || 0)

  // 模拟API调用
  setTimeout(() => {
    localData.value.content = '这里是基于关键词和图片生成的内容...'
    updateData()
    currentStep.value = '2'
    emits('next', currentStep.value)
  }, 500)
}

// 重新生成内容
function regenerateContent() {
  console.log('重新生成内容')
  // 实现重新生成逻辑
}

// 上一步
function previousStep() {
  updateData()
  currentStep.value = '1'
  emits('previous', currentStep.value)
}

// 完成
function complete() {
  updateData()
  emits('complete')
}
</script>

<style lang="scss" scoped>
.two-step-process {
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
}
</style>
