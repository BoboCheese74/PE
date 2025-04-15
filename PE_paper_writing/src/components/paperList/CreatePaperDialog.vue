<template>
  <v-dialog :model-value="visible" max-width="500" @update:model-value="onUpdateVisible">
    <v-card style="border-radius: 25px; padding: 10px;">
      <v-card-title class="d-flex justify-space-between align-center">
        新建论文
        <v-btn icon="mdi-close" variant="text" density="comfortable" @click="closeDialog"></v-btn>
      </v-card-title>

      <v-card-text class="pt-4">
        <v-radio-group v-model="paperData.language" inline>
          <v-radio label="中文" value="zh"></v-radio>
          <v-radio label="英文" value="en"></v-radio>
        </v-radio-group>

        <v-text-field v-model="paperData.title" label="标题" variant="outlined" density="compact"
          class="mb-4"></v-text-field>

        <v-text-field v-model="paperData.type" label="类型" variant="outlined" density="compact"
          class="mb-4"></v-text-field>
      </v-card-text>

      <v-card-actions class="pb-4 px-4">
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="elevated" @click="submitForm">
          创建
        </v-btn>
        <v-btn color="secondary" variant="text" @click="closeDialog">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  typeOptions: {
    type: Array,
    default: () => ['学术论文', '研究报告', '综述', '书评']
  }
})

const emits = defineEmits(['update:visible', 'create'])

const paperData = reactive({
  language: 'zh',
  title: '',
  type: ''
})

// 对话框状态更新
const onUpdateVisible = (newValue: boolean) => {
  emits('update:visible', newValue)

  // 如果对话框被关闭，重置表单
  if (!newValue) {
    resetForm()
  }
}

// 提交表单
const submitForm = () => {
  if (!paperData.title) {
    // 可以添加表单验证
    alert('请输入标题')
    return
  }

  // 提交数据到父组件
  emits('create', { ...paperData })

  // 关闭对话框
  closeDialog()
}

// 关闭对话框
const closeDialog = () => {
  emits('update:visible', false)
}

// 重置表单
const resetForm = () => {
  paperData.language = 'zh'
  paperData.title = ''
  paperData.type = null
}
</script>
