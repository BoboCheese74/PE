<template>
  <v-dialog v-model="dialogVisible" fullscreen persistent transition="dialog-bottom-transition">
    <v-card class="paper-detail-dialog">
      <v-row no-gutters class="fill-height">
        <!-- 左侧进度区域 -->
        <v-col cols="3" class="progress-sidebar">
          <progress-sidebar
            :active-step="activeStep"
            :completed-steps="completedSteps"
            @step-change="changeStep"
            @save="saveAndReturn"
          />
        </v-col>

        <!-- 右侧表单区域 -->
        <v-col cols="9">
          <form-area
            :active-step="activeStep"
            :current-process="currentProcess"
            :process-data="processData"
            @update:process-data="updateProcessData"
            @step-complete="completeStep"
            @next-step="nextStep"
            @previous-step="previousStep"
          />
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import ProgressSidebar from './ProgressSidebar.vue'
import FormArea from './FormArea.vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  paperId: {
    type: String,
    default: '',
  },
})

const emits = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(props.visible)
const activeStep = ref('background')
const completedSteps = ref(new Set())
const processData = ref({
  background: {
    keywords: '',
    outline: '',
    outlineKeywords: '',
    content: '',
  },
  discussion1: {
    keywords: '',
    outline: '',
    outlineKeywords: '',
    content: '',
  },
  discussion2: {
    keywords: '',
    outline: '',
    outlineKeywords: '',
    content: '',
  },
  // 其他步骤的数据...
  baselineTable: {
    keywords: '',
    images: [],
    content: '',
  },
  regressionAnalysis: {
    keywords: '',
    images: [],
    content: '',
  },
  // 更多步骤...
})

// 监听外部可见性变化
watch(
  () => props.visible,
  (newValue) => {
    dialogVisible.value = newValue
  },
)

// 监听对话框关闭
watch(dialogVisible, (newValue) => {
  if (!newValue) {
    emits('update:visible', false)
  }
})

// 判断当前步骤类型
const currentProcess = computed(() => {
  const fourStepProcesses = ['background', 'discussion1', 'discussion2']
  return {
    type: fourStepProcesses.includes(activeStep.value) ? 'four-step' : 'two-step',
    title: getStepTitle(activeStep.value),
  }
})

// 获取步骤标题
function getStepTitle(step) {
  const titles = {
    background: '写背景',
    discussion1: '讨论(与现有文献的比较)',
    discussion2: '讨论(机制、生物削意义)',
    discussion3: '讨论(临床意义)',
    discussion4: '讨论(优势与局限性)',
    discussion5: '讨论(两组两组临床资料比较)',
    baselineTable: '结果(预测因素筛选并初步构建模型)',
    regressionAnalysis: '结果(列线图预测模型的构建及预测能力评价)',
    subgroupAnalysis: '方法(研究对象)',
    rcsCurve: '方法(数据采集)',
    rocCurve: '方法(分组和研究终点)',
    statisticalMethod: '方法(统计学方法)',
    fullText: '全文',
  }
  return titles[step] || step
}

// 更新进程数据
function updateProcessData(data) {
  processData.value = { ...processData.value, ...data }
}

// 完成当前步骤
function completeStep(step) {
  completedSteps.value.add(step)
}

// 前往下一步
function nextStep(currentSubStep) {
  // 实现步骤导航逻辑
  console.log(`Moving to next step from substep ${currentSubStep}`)
}

// 返回上一步
function previousStep(currentSubStep) {
  // 实现步骤导航逻辑
  console.log(`Moving to previous step from substep ${currentSubStep}`)
}

// 切换当前步骤
function changeStep(step) {
  activeStep.value = step
}

// 保存并返回
function saveAndReturn() {
  console.log('Saving paper details')
  // 在这里添加保存逻辑
  emits('save', processData.value)
  dialogVisible.value = false
}
</script>

<style lang="scss" scoped>
.paper-detail-dialog {
  display: flex;
  height: 100%;
  overflow: hidden;

  .progress-sidebar {
    border-right: 1px solid rgba(0, 0, 0, 0.12);
  }
}
</style>
