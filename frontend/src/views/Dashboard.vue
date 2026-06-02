<template>
  <div class="dashboard">
    <Sidebar />
    <div class="main-content">
      <Header />
      
      <div class="content-wrapper">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon file-icon">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.totalFiles }}</p>
              <p class="stat-label">总文件数</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon analysis-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.analyzedFiles }}</p>
              <p class="stat-label">已分析文件</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon user-icon">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.totalUsers }}</p>
              <p class="stat-label">用户数</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon category-icon">
              <el-icon><CollectionTag /></el-icon>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.totalCategories }}</p>
              <p class="stat-label">分类数</p>
            </div>
          </div>
        </div>

        <div class="chart-row">
          <div class="chart-card">
            <h3>文件类型分布</h3>
            <div ref="fileTypeChart" class="chart-container"></div>
          </div>
          
          <div class="chart-card">
            <h3>分析状态统计</h3>
            <div ref="analysisStatusChart" class="chart-container"></div>
          </div>
        </div>

        <div class="recent-files">
          <h3>最近上传的文件</h3>
          <el-table :data="recentFiles" border>
            <el-table-column prop="filename" label="文件名" />
            <el-table-column prop="file_type" label="类型" :formatter="formatFileType" />
            <el-table-column prop="uploaded_at" label="上传时间" :formatter="formatTime" />
            <el-table-column prop="is_analyzed" label="是否分析" :formatter="formatAnalyzed" />
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { FolderOpened, DataAnalysis, UserFilled, CollectionTag } from '@element-plus/icons-vue'
import { useStore } from 'vuex'

const store = useStore()

const fileTypeChart = ref(null)
const analysisStatusChart = ref(null)

const stats = reactive({
  totalFiles: 0,
  analyzedFiles: 0,
  totalUsers: 5,
  totalCategories: 3
})

const recentFiles = ref([])

const formatFileType = (row) => {
  const types = { document: '文档', image: '图片', spreadsheet: '表格', other: '其他' }
  return types[row.file_type] || row.file_type
}

const formatTime = (row) => {
  return row.uploaded_at?.substring(0, 10) || '-'
}

const formatAnalyzed = (row) => {
  return row.is_analyzed ? '是' : '否'
}

const initCharts = () => {
  if (fileTypeChart.value) {
    const chart = echarts.init(fileTypeChart.value)
    chart.setOption({
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 35, name: '文档' },
          { value: 20, name: '图片' },
          { value: 25, name: '表格' },
          { value: 20, name: '其他' }
        ],
        label: { show: true },
        emphasis: {
          label: { show: true, fontSize: 16 }
        }
      }]
    })
  }
  
  if (analysisStatusChart.value) {
    const chart = echarts.init(analysisStatusChart.value)
    chart.setOption({
      xAxis: { type: 'category', data: ['待分析', '分析中', '已完成', '失败'] },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: [10, 5, 25, 3],
        itemStyle: {
          color: ['#f5a623', '#3498db', '#2ecc71', '#e74c3c']
        }
      }]
    })
  }
}

onMounted(async () => {
  try {
    await store.dispatch('files/fetchFiles')
    const files = store.getters['files/files']
    stats.totalFiles = files.length
    stats.analyzedFiles = files.filter(f => f.is_analyzed).length
    recentFiles.value = files.slice(0, 5)
    
    await nextTick()
    initCharts()
    
    window.addEventListener('resize', initCharts)
  } catch (error) {
    console.error('Failed to fetch data:', error)
  }
})
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.content-wrapper {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  font-size: 24px;
}

.file-icon { background: #e8f4fd; color: #3498db; }
.analysis-icon { background: #e8f5e9; color: #2ecc71; }
.user-icon { background: #fff3e0; color: #f5a623; }
.category-icon { background: #fce4ec; color: #e91e63; }

.stat-info { flex: 1; }
.stat-value { font-size: 24px; font-weight: bold; color: #333; margin: 0; }
.stat-label { font-size: 14px; color: #999; margin: 4px 0 0; }

.chart-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-card h3 {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}

.chart-container {
  height: 250px;
}

.recent-files {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.recent-files h3 {
  margin-bottom: 20px;
  color: #333;
  font-size: 16px;
}
</style>
