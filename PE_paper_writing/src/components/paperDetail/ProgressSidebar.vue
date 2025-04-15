<template>
  <div class="progress-sidebar">
    <v-btn
      color="primary"
      class="save-btn ma-4"
      prepend-icon="mdi-content-save"
      @click="$emit('save')"
    >
      保存并返回
    </v-btn>

    <v-list>
      <v-list-item
        v-for="item in menuItems"
        :key="item.id"
        :title="item.title"
        :value="item.id"
        :active="activeStep === item.id"
        @click="$emit('step-change', item.id)"
        :prepend-icon="isCompleted(item.id) ? 'mdi-check-circle' : ''"
        :class="{ 'completed-step': isCompleted(item.id) }"
      >
        <template v-if="!isCompleted(item.id) && item.icon" v-slot:prepend>
          <v-icon>{{ item.icon }}</v-icon>
        </template>
      </v-list-item>
    </v-list>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  activeStep: {
    type: String,
    required: true,
  },
  completedSteps: {
    type: Set,
    required: true,
  },
})

defineEmits(['step-change', 'save'])

const menuItems = [
  { id: 'background', title: '写背景', icon: 'mdi-text-box-outline' },
  { id: 'discussion1', title: '讨论(与现有文献的比较)', icon: 'mdi-format-paragraph' },
  { id: 'discussion2', title: '讨论(机制、生物削意义)', icon: 'mdi-format-paragraph' },
  { id: 'discussion3', title: '讨论(临床意义)', icon: 'mdi-format-paragraph' },
  { id: 'discussion4', title: '讨论(优势与局限性)', icon: 'mdi-format-paragraph' },
  { id: 'discussion5', title: '讨论(两组两组临床资料比较)', icon: 'mdi-format-paragraph' },
  { id: 'baselineTable', title: '结果(预测因素筛选并初步构建模型)', icon: 'mdi-table' },
  {
    id: 'regressionAnalysis',
    title: '结果(列线图预测模型的构建及预测能力评价)',
    icon: 'mdi-chart-line',
  },
  { id: 'subgroupAnalysis', title: '方法(研究对象)', icon: 'mdi-account-group' },
  { id: 'rcsCurve', title: '方法(数据采集)', icon: 'mdi-chart-bell-curve' },
  { id: 'rocCurve', title: '方法(分组和研究终点)', icon: 'mdi-chart-arc' },
  { id: 'statisticalMethod', title: '方法(统计学方法)', icon: 'mdi-calculator' },
  { id: 'fullText', title: '全文', icon: 'mdi-file-document' },
]

function isCompleted(stepId) {
  return props.completedSteps.has(stepId)
}
</script>

<style lang="scss" scoped>
.progress-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;

  .save-btn {
    align-self: flex-start;
  }

  .v-list {
    flex-grow: 1;
    padding: 0;

    .v-list-item {
      border-radius: 0;

      &.completed-step {
        background-color: rgba(76, 175, 80, 0.1);

        .v-icon {
          color: #4caf50;
        }
      }

      &.v-list-item--active {
        background-color: rgba(25, 118, 210, 0.1);
      }
    }
  }
}
</style>
