<template>
  <div class="form-area pa-6">
    <h2 class="text-h4 mb-6">{{ currentProcess.title }}</h2>

    <four-step-process
      v-if="currentProcess.type === 'four-step'"
      :process-data="getProcessData"
      @update:process-data="updateData"
      @complete="completeStep"
      @next="nextStep"
      @previous="previousStep"
    />

    <two-step-process
      v-else
      :process-data="getProcessData"
      :supports-images="supportsImages"
      @update:process-data="updateData"
      @complete="completeStep"
      @next="nextStep"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import FourStepProcess from './FourStepProcess.vue'
import TwoStepProcess from './TwoStepProcess.vue'

const props = defineProps({
  activeStep: {
    type: String,
    required: true,
  },
  currentProcess: {
    type: Object,
    required: true,
  },
  processData: {
    type: Object,
    required: true,
  },
})

const emits = defineEmits(['update:process-data', 'step-complete', 'next-step', 'previous-step'])

// 获取当前步骤的数据
const getProcessData = computed(() => {
  return props.processData[props.activeStep] || {}
})

// 确定当前步骤是否支持图片上传
const supportsImages = computed(() => {
  const imageSteps = [
    'discussion3',
    'discussion4',
    'discussion5',
    'baselineTable',
    'regressionAnalysis',
    'subgroupAnalysis',
    'rcsCurve',
    'rocCurve',
    'statisticalMethod',
  ]
  return imageSteps.includes(props.activeStep)
})

// 更新数据
function updateData(data) {
  emits('update:process-data', { [props.activeStep]: data })
}

// 完成步骤
function completeStep() {
  emits('step-complete', props.activeStep)
}

// 下一步
function nextStep(subStep) {
  emits('next-step', subStep)
}

// 上一步
function previousStep(subStep) {
  emits('previous-step', subStep)
}
</script>

<style lang="scss" scoped>
.form-area {
  height: 100%;
  overflow-y: auto;
}
</style>
