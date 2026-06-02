<template>
  <div class="file-management">
    <Sidebar />
    <div class="main-content">
      <Header />
      
      <div class="content-wrapper">
        <div class="toolbar">
          <el-button type="primary" @click="showUpload = true">
            <el-icon><Upload /></el-icon>
            上传文件
          </el-button>
          
          <el-button @click="showCategoryModal = true">
            <el-icon><Plus /></el-icon>
            添加分类
          </el-button>
        </div>

        <div class="search-bar">
          <el-input v-model="searchQuery" placeholder="搜索文件名" @input="handleSearch">
            <template #append>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select v-model="selectedCategory" placeholder="选择分类">
            <el-option label="全部" value="" />
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </div>

        <el-table :data="filteredFiles" border>
          <el-table-column prop="filename" label="文件名" />
          <el-table-column prop="category_name" label="分类" />
          <el-table-column prop="file_type" label="类型" :formatter="formatFileType" />
          <el-table-column prop="size" label="大小" :formatter="formatSize" />
          <el-table-column prop="uploaded_at" label="上传时间" :formatter="formatTime" />
          <el-table-column prop="is_analyzed" label="是否分析" :formatter="formatAnalyzed" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="downloadFile(scope.row)">下载</el-button>
              <el-button size="small" type="primary" @click="goToAnalysis(scope.row)">分析</el-button>
              <el-button size="small" type="danger" @click="deleteFile(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-dialog title="上传文件" :visible.sync="showUpload" width="500px">
          <el-form :model="uploadForm" label-width="80px">
            <el-form-item label="文件">
              <el-upload
                class="upload-demo"
                :action="uploadUrl"
                :headers="uploadHeaders"
                :file-list="uploadFileList"
                :before-upload="beforeUpload"
                :on-success="onUploadSuccess"
                :on-error="onUploadError"
              >
                <el-button type="primary">点击上传</el-button>
              </el-upload>
            </el-form-item>
            <el-form-item label="分类">
              <el-select v-model="uploadForm.category">
                <el-option label="未分类" :value="null" />
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="描述">
              <el-textarea v-model="uploadForm.description" rows="3" placeholder="请输入文件描述" />
            </el-form-item>
          </el-form>
          
          <template #footer>
            <el-button @click="showUpload = false">取消</el-button>
            <el-button type="primary" @click="handleUpload">上传</el-button>
          </template>
        </el-dialog>

        <el-dialog title="添加分类" :visible.sync="showCategoryModal" width="400px">
          <el-form :model="categoryForm" label-width="80px">
            <el-form-item label="分类名称">
              <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
            </el-form-item>
            <el-form-item label="描述">
              <el-textarea v-model="categoryForm.description" rows="3" placeholder="请输入分类描述" />
            </el-form-item>
          </el-form>
          
          <template #footer>
            <el-button @click="showCategoryModal = false">取消</el-button>
            <el-button type="primary" @click="createCategory">创建</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { Upload, Plus, Search } from '@element-plus/icons-vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const router = useRouter()
const store = useStore()

const showUpload = ref(false)
const showCategoryModal = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
const uploadFileList = ref([])

const uploadForm = reactive({
  category: null,
  description: ''
})

const categoryForm = reactive({
  name: '',
  description: ''
})

const files = computed(() => store.getters['files/files'])
const categories = computed(() => store.getters['files/categories'])

const filteredFiles = computed(() => {
  let result = files.value
  if (searchQuery.value) {
    result = result.filter(f => f.filename.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  if (selectedCategory.value) {
    result = result.filter(f => f.category === Number(selectedCategory.value))
  }
  return result
})

const uploadUrl = '/api/files/files/'
const uploadHeaders = {
  Authorization: `Token ${localStorage.getItem('token')}`
}

const formatFileType = (row) => {
  const types = { document: '文档', image: '图片', spreadsheet: '表格', other: '其他' }
  return types[row.file_type] || row.file_type
}

const formatSize = (row) => {
  const size = row.size
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)} KB`
  return `${(size / (1024 * 1024)).toFixed(2)} MB`
}

const formatTime = (row) => {
  return row.uploaded_at?.substring(0, 19).replace('T', ' ') || '-'
}

const formatAnalyzed = (row) => {
  return row.is_analyzed ? '是' : '否'
}

const handleSearch = () => {}

const beforeUpload = (file) => {
  uploadFileList.value = [{ name: file.name, status: 'ready' }]
  return false
}

const handleUpload = async () => {
  const formData = new FormData()
  const file = uploadFileList.value[0]?.raw
  if (!file) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  formData.append('file', file)
  if (uploadForm.category) {
    formData.append('category', uploadForm.category)
  }
  if (uploadForm.description) {
    formData.append('description', uploadForm.description)
  }
  
  try {
    await store.dispatch('files/uploadFile', formData)
    ElMessage.success('文件上传成功')
    showUpload.value = false
    uploadFileList.value = []
    uploadForm.category = null
    uploadForm.description = ''
  } catch (error) {
    ElMessage.error('文件上传失败')
  }
}

const onUploadSuccess = () => {}
const onUploadError = () => {}

const createCategory = async () => {
  if (!categoryForm.name) {
    ElMessage.warning('请输入分类名称')
    return
  }
  
  try {
    await store.dispatch('files/createCategory', categoryForm)
    ElMessage.success('分类创建成功')
    showCategoryModal.value = false
    categoryForm.name = ''
    categoryForm.description = ''
  } catch (error) {
    ElMessage.error('分类创建失败')
  }
}

const downloadFile = (row) => {
  window.open(`/api/files/download/${row.id}/`, '_blank')
}

const goToAnalysis = (row) => {
  router.push({ path: '/ai-analysis', query: { fileId: row.id } })
}

const deleteFile = async (row) => {
  try {
    await store.dispatch('files/deleteFile', row.id)
    ElMessage.success('文件删除成功')
  } catch (error) {
    ElMessage.error('文件删除失败')
  }
}

onMounted(async () => {
  await store.dispatch('files/fetchFiles')
  await store.dispatch('files/fetchCategories')
})
</script>

<style scoped>
.file-management {
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

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.search-bar .el-input {
  width: 300px;
}

.search-bar .el-select {
  width: 150px;
}

.upload-demo {
  margin-bottom: 10px;
}
</style>
