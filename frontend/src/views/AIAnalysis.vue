<template>
  <div class="ai-analysis">
    <Sidebar />
    <div class="main-content">
      <Header />
      
      <div class="content-wrapper">
        <div class="file-selector">
          <el-select v-model="selectedFileId" placeholder="选择文件进行分析" @change="handleFileChange">
            <el-option v-for="file in availableFiles" :key="file.id" :label="file.filename" :value="file.id" />
          </el-select>
          
          <el-button v-if="selectedFile" type="primary" @click="startAnalysis" :disabled="isAnalyzing">
            <el-icon><Cpu /></el-icon>
            {{ isAnalyzing ? '分析中...' : '开始AI分析' }}
          </el-button>
        </div>

        <div v-if="selectedFile" class="analysis-content">
          <div class="analysis-header">
            <h2>{{ selectedFile.filename }}</h2>
            <p>文件类型: {{ formatFileType(selectedFile) }} | 大小: {{ formatSize(selectedFile.size) }}</p>
          </div>

          <div class="analysis-tabs">
            <el-tabs v-model="activeTab" type="card">
              <el-tab-pane label="分析结果" name="results">
                <div v-if="currentAnalysis" class="analysis-result">
                  <div class="result-header">
                    <span class="version-tag">版本 {{ currentAnalysis.version }}</span>
                    <span :class="['status-tag', currentAnalysis.status]">{{ formatStatus(currentAnalysis.status) }}</span>
                    <el-button v-if="currentAnalysis.status === 'completed'" type="primary" @click="showVersionSelect = true">
                      选择此版本
                    </el-button>
                  </div>
                  
                  <div class="result-content">
                    <div class="summary-section">
                      <h3>文档摘要</h3>
                      <el-textarea 
                        v-model="editSummary" 
                        :rows="6" 
                        placeholder="文档摘要内容..."
                        :disabled="!currentAnalysis.status === 'completed'"
                      />
                      <el-button v-if="currentAnalysis.status === 'completed'" type="success" @click="updateAnalysis">
                        保存修改
                      </el-button>
                    </div>
                    
                    <div class="info-section">
                      <h3>提取的关键信息</h3>
                      <el-table :data="extractedInfoList" border v-if="extractedInfoList.length">
                        <el-table-column prop="name" label="字段名" />
                        <el-table-column prop="value" label="值" />
                      </el-table>
                      <p v-else class="empty-text">暂无提取的信息</p>
                    </div>
                  </div>
                </div>
                
                <div v-else class="empty-state">
                  <el-icon class="empty-icon"><Files /></el-icon>
                  <p>暂无分析结果</p>
                  <el-button type="primary" @click="startAnalysis">开始分析</el-button>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="智能问答" name="qa">
                <div class="qa-section">
                  <el-input 
                    v-model="qaQuestion" 
                    placeholder="请输入您的问题..."
                    @keyup.enter="askQuestion"
                  >
                    <template #append>
                      <el-button type="primary" @click="askQuestion">提问</el-button>
                    </template>
                  </el-input>
                  
                  <div v-if="qaAnswer" class="qa-answer">
                    <h4>回答:</h4>
                    <p>{{ qaAnswer }}</p>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="版本历史" name="history">
                <el-table :data="analysisVersions" border>
                  <el-table-column prop="version" label="版本号" />
                  <el-table-column prop="status" label="状态" :formatter="formatStatus" />
                  <el-table-column prop="created_at" label="创建时间" :formatter="formatTime" />
                  <el-table-column prop="is_selected" label="是否选中" :formatter="formatSelected" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button size="small" @click="selectVersion(scope.row)">选择版本</el-button>
                      <el-button size="small" @click="viewVersion(scope.row)">查看详情</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>

        <div v-else class="no-file-selected">
          <el-icon class="big-icon"><Help /></el-icon>
          <p>请先选择一个文件进行分析</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Cpu, Files, Help } from '@element-plus/icons-vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const store = useStore()
const route = useRoute()

const selectedFileId = ref('')
const activeTab = ref('results')
const isAnalyzing = ref(false)
const editSummary = ref('')
const qaQuestion = ref('')
const qaAnswer = ref('')

const availableFiles = computed(() => store.getters['files/files'])
const selectedFile = computed(() => availableFiles.value.find(f => f.id === Number(selectedFileId.value)))
const analysisResults = computed(() => store.getters['aiAnalysis/analysisResults'])
const currentAnalysis = computed(() => {
  if (!selectedFile.value) return null
  return analysisResults.value.find(r => r.file === selectedFile.value.id && r.is_selected) ||
         analysisResults.value.filter(r => r.file === selectedFile.value.id).pop() || null
})

const analysisVersions = computed(() => {
  if (!selectedFile.value) return []
  return analysisResults.value.filter(r => r.file === selectedFile.value.id)
})

const extractedInfoList = computed(() => {
  if (!currentAnalysis.value?.extracted_info?.key_points) return []
  return currentAnalysis.value.extracted_info.key_points
})

const formatFileType = (file) => {
  const types = { document: '文档', image: '图片', spreadsheet: '表格', other: '其他' }
  return types[file.file_type] || file.file_type
}

const formatSize = (size) => {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)} KB`
  return `${(size / (1024 * 1024)).toFixed(2)} MB`
}

const formatStatus = (status) => {
  const statusMap = {
    pending: '待分析',
    processing: '分析中',
    completed: '已完成',
    failed: '失败'
  }
  return statusMap[status] || status
}

const formatTime = (time) => {
  return time?.substring(0, 19).replace('T', ' ') || '-'
}

const formatSelected = (row) => {
  return row.is_selected ? '是' : '否'
}

const handleFileChange = async (fileId) => {
  if (fileId) {
    await store.dispatch('aiAnalysis/fetchAnalysisResults')
    if (currentAnalysis.value) {
      editSummary.value = currentAnalysis.value.summary || ''
    }
  }
}

const startAnalysis = async () => {
  if (!selectedFileId.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  isAnalyzing.value = true
  try {
    await store.dispatch('aiAnalysis/startAnalysis', selectedFileId.value)
    ElMessage.success('分析任务已提交，请稍等...')
    
    setTimeout(async () => {
      await store.dispatch('aiAnalysis/fetchAnalysisResults')
      if (currentAnalysis.value) {
        editSummary.value = currentAnalysis.value.summary || ''
      }
      isAnalyzing.value = false
    }, 3000)
  } catch (error) {
    ElMessage.error('分析任务提交失败')
    isAnalyzing.value = false
  }
}

const updateAnalysis = async () => {
  if (!currentAnalysis.value) return
  
  try {
    await store.dispatch('aiAnalysis/updateAnalysis', {
      analysisId: currentAnalysis.value.id,
      data: { summary: editSummary.value }
    })
    ElMessage.success('分析结果已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const askQuestion = async () => {
  if (!qaQuestion.value.trim() || !currentAnalysis.value) {
    ElMessage.warning('请输入问题并确保已有分析结果')
    return
  }
  
  try {
    const response = await store.dispatch('aiAnalysis/qaAnalysis', {
      analysisId: currentAnalysis.value.id,
      question: qaQuestion.value
    })
    qaAnswer.value = response.answer
  } catch (error) {
    ElMessage.error('提问失败')
  }
}

const selectVersion = async (version) => {
  try {
    await store.dispatch('aiAnalysis/selectVersion', version.id)
    ElMessage.success('已选择此版本')
    editSummary.value = version.summary || ''
  } catch (error) {
    ElMessage.error('选择失败')
  }
}

const viewVersion = (version) => {
  editSummary.value = version.summary || ''
  activeTab.value = 'results'
}

onMounted(async () => {
  await store.dispatch('files/fetchFiles')
  await store.dispatch('aiAnalysis/fetchAnalysisResults')
  
  const fileId = route.query.fileId
  if (fileId) {
    selectedFileId.value = fileId
    if (currentAnalysis.value) {
      editSummary.value = currentAnalysis.value.summary || ''
    }
  }
})

watch(selectedFileId, () => {
  if (currentAnalysis.value) {
    editSummary.value = currentAnalysis.value.summary || ''
  }
})
</script>

<style scoped>
.ai-analysis {
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

.file-selector {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.file-selector .el-select {
  width: 400px;
}

.analysis-content {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.analysis-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.analysis-header h2 {
  margin: 0 0 8px;
  color: #333;
}

.analysis-header p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.version-tag {
  background: #e8f4fd;
  color: #3498db;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.status-tag.pending { background: #fff3e0; color: #f5a623; }
.status-tag.processing { background: #e8f4fd; color: #3498db; }
.status-tag.completed { background: #e8f5e9; color: #2ecc71; }
.status-tag.failed { background: #ffebee; color: #e74c3c; }

.result-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.summary-section, .info-section {
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
}

.summary-section h3, .info-section h3 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #666;
}

.empty-text {
  text-align: center;
  color: #999;
  padding: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

.empty-state p {
  color: #999;
  margin-bottom: 20px;
}

.no-file-selected {
  text-align: center;
  padding: 100px 20px;
}

.big-icon {
  font-size: 64px;
  color: #ccc;
  margin-bottom: 16px;
}

.no-file-selected p {
  color: #999;
}

.qa-section {
  max-width: 600px;
  margin: 0 auto;
}

.qa-answer {
  margin-top: 20px;
  padding: 16px;
  background: #e8f5e9;
  border-radius: 8px;
}

.qa-answer h4 {
  margin: 0 0 8px;
  color: #2ecc71;
  font-size: 14px;
}

.qa-answer p {
  margin: 0;
  color: #333;
}
</style>
