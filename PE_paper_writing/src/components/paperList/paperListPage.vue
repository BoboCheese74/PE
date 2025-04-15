<template>
  <div class="paper-list-page">
    <v-card class="mx-auto">
      <!-- 上半部分：搜索区域 -->
      <v-card-text class="search-section pa-4">
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="searchParams.title" label="标题" variant="outlined" density="compact" hide-details
              class="mb-2"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="searchParams.background" label="背景" variant="outlined" density="compact" hide-details
              class="mb-2"></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select v-model="searchParams.type" :items="typeOptions" label="类型" variant="outlined" density="compact"
              hide-details class="mb-2"></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="searchParams.createdAt" label="创建时间" variant="outlined" density="compact"
              hide-details class="mb-2" type="date"></v-text-field>
          </v-col>
        </v-row>

        <div class="d-flex justify-end mt-2">
          <v-btn color="primary" class="mr-2" prepend-icon="mdi-magnify" @click="handleSearch">
            查询
          </v-btn>
          <v-btn color="secondary" prepend-icon="mdi-refresh" @click="handleReset">
            重置
          </v-btn>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <!-- 下半部分：列表区域 -->
      <v-card-text class="list-section pa-4">
        <!-- 按钮行 -->
        <div class="d-flex justify-space-between mb-4">
          <v-btn color="primary" prepend-icon="mdi-plus" @click="showCreateDialog">
            新建
          </v-btn>
          <v-btn prepend-icon="mdi-download" @click="handleDownload">
            下载
          </v-btn>
        </div>

        <!-- 数据表格 -->
        <v-data-table :headers="headers" :items="filteredPapers" :items-per-page="10" class="datatable elevation-1">
          <template v-slot:item.actions="{ item }">
            <v-btn color="primary" variant="text" size="small" @click="viewDetails(item)">
              查看详情
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- 引入创建论文对话框组件 -->
    <create-paper-dialog v-model:visible="createDialogVisible" :type-options="typeOptions" @create="createPaper" />

    <!-- 在底部添加详情对话框 -->
    <paper-detail-dialog v-model:visible="detailDialogVisible" :paper-id="selectedPaperId" @save="handleDetailSave" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import CreatePaperDialog from './CreatePaperDialog.vue'
import PaperDetailDialog from '../paperDetail/PaperDetailDialog.vue'

// 搜索参数
const searchParams = reactive({
  title: '',
  background: '',
  type: null,
  createdAt: ''
})

// 类型选项
const typeOptions = ref(['学术论文', '研究报告', '综述', '书评'])

// 表头定义
const headers = [
  { title: '编号', key: 'id', align: 'start', sortable: true },
  { title: '标题', key: 'title', align: 'start', sortable: true },
  { title: '类型', key: 'type', align: 'start', sortable: true },
  { title: '背景', key: 'background', align: 'start', sortable: true },
  { title: '创建时间', key: 'createdAt', align: 'start', sortable: true },
  { title: '更新时间', key: 'updatedAt', align: 'start', sortable: true },
  { title: '操作', key: 'actions', align: 'center', sortable: false }
]

// 原始数据
const allPapers = ref([
  {
    id: '001',
    title: '人工智能在医疗领域的应用',
    type: '研究报告',
    background: '随着技术的发展，AI在医疗领域的应用越来越广泛...',
    createdAt: '2025-03-15',
    updatedAt: '2025-04-01'
  },
  {
    id: '002',
    title: '气候变化对全球农业的影响',
    type: '学术论文',
    background: '气候变化已经成为全球面临的重大挑战...',
    createdAt: '2025-02-20',
    updatedAt: '2025-03-05'
  },
  {
    id: '003',
    title: '量子计算的最新进展',
    type: '综述',
    background: '量子计算领域在近年来取得了重大突破...',
    createdAt: '2025-01-10',
    updatedAt: '2025-01-25'
  }
])

// 搜索状态
const isSearchActive = ref(false)

// 过滤后的数据（用于显示）
const filteredPapers = ref([...allPapers.value])

// 对话框可见性控制
const createDialogVisible = ref(false)

// 详情对话框状态
const detailDialogVisible = ref(false)
const selectedPaperId = ref('')

// 处理搜索
const handleSearch = () => {
  isSearchActive.value = true

  filteredPapers.value = allPapers.value.filter(paper => {
    // 标题搜索
    const titleMatch = !searchParams.title ||
      paper.title.toLowerCase().includes(searchParams.title.toLowerCase());

    // 背景搜索
    const backgroundMatch = !searchParams.background ||
      paper.background.toLowerCase().includes(searchParams.background.toLowerCase());

    // 类型搜索
    const typeMatch = !searchParams.type ||
      paper.type === searchParams.type;

    // 创建时间搜索
    const createdAtMatch = !searchParams.createdAt ||
      paper.createdAt === searchParams.createdAt;

    return titleMatch && backgroundMatch && typeMatch && createdAtMatch;
  });
}

// 处理重置
const handleReset = () => {
  // 清空所有搜索条件
  Object.keys(searchParams).forEach(key => {
    searchParams[key] = '';
  });

  // 恢复原始数据
  filteredPapers.value = [...allPapers.value];
  isSearchActive.value = false;
}

// 显示创建对话框
const showCreateDialog = () => {
  createDialogVisible.value = true;
}

// 处理新建论文
const createPaper = (paperData) => {
  console.log('创建新论文:', paperData);

  // 生成一个新ID
  const newId = String(allPapers.value.length + 1).padStart(3, '0');

  // 创建新论文对象
  const newPaper = {
    id: newId,
    title: paperData.title,
    type: paperData.type,
    background: paperData.background || '',
    createdAt: new Date().toISOString().split('T')[0],
    updatedAt: new Date().toISOString().split('T')[0]
  };

  // 添加到原始数据
  allPapers.value.unshift(newPaper);

  // 如果没有进行搜索或新添加的论文满足搜索条件，则添加到过滤后的数据中
  if (!isSearchActive.value) {
    filteredPapers.value.unshift(newPaper);
  } else {
    // 重新运行一次搜索，以确保新添加的论文如果满足搜索条件也会显示
    handleSearch();
  }
}

// 处理下载
const handleDownload = () => {
  console.log('下载数据', filteredPapers.value);
  // 这里添加下载逻辑
}

// 查看详情
const viewDetails = (item) => {
  console.log('查看详情:', item)
  selectedPaperId.value = item.id
  detailDialogVisible.value = true
}

// 处理详情保存
const handleDetailSave = (data) => {
  console.log('保存论文详情:', data)
  // 这里可以处理保存数据的逻辑
}
</script>

<style scoped lang="scss">
@use '@/assets/paperList/paperListPage.scss';

.paper-list-page {

  .list-section {
    min-height: 400px;
  }
}
</style>
