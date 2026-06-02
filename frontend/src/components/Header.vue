<template>
  <header class="header">
    <div class="header-left">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ currentPath }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    
    <div class="header-right">
      <div class="user-info">
        <el-dropdown>
          <span class="user-name">
            <el-icon><UserFilled /></el-icon>
            {{ userName }}
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="showUserProfile = true">
                <el-icon><UserFilled /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item @click="handleLogout">
                <el-icon><ArrowRight /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <el-dialog title="个人资料" :visible.sync="showUserProfile" width="400px">
      <el-form :model="userProfile" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="userProfile.username" disabled />
        </el-form-item>
        <el-form-item label="角色">
          <el-input v-model="userProfile.role" disabled />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="userProfile.phone" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showUserProfile = false">关闭</el-button>
        <el-button type="primary" @click="saveProfile">保存</el-button>
      </template>
    </el-dialog>
  </header>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { UserFilled, ArrowDown, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useStore()

const showUserProfile = ref(false)

const pathNames = {
  '/': '仪表盘',
  '/files': '文件管理',
  '/ai-analysis': 'AI分析',
  '/users': '用户管理'
}

const currentPath = computed(() => pathNames[router.currentRoute.value.path] || '未知')
const userName = computed(() => store.getters['auth/userName'] || '用户')

const userProfile = reactive({
  username: '',
  role: '',
  phone: ''
})

const handleLogout = () => {
  store.dispatch('auth/logout')
  router.push('/login')
  ElMessage.info('已退出登录')
}

const saveProfile = () => {
  showUserProfile.value = false
  ElMessage.success('资料已保存')
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  margin-left: 20px;
}

.user-name {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background 0.2s;
}

.user-name:hover {
  background: #f5f5f5;
}

.user-name i {
  margin-right: 6px;
}
</style>
