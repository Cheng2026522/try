<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>建设集团管理</h1>
    </div>
    
    <nav class="sidebar-nav">
      <el-menu :default-active="activeMenu" mode="vertical">
        <el-menu-item index="/">
          <el-icon><DataBoard /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        
        <el-menu-item index="/files">
          <el-icon><FolderOpened /></el-icon>
          <span>文件管理</span>
        </el-menu-item>
        
        <el-menu-item index="/ai-analysis">
          <el-icon><Cpu /></el-icon>
          <span>AI分析</span>
        </el-menu-item>
        
        <el-menu-item v-if="isAdmin" index="/users">
          <el-icon><UserFilled /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { DataBoard, FolderOpened, Cpu, UserFilled } from '@element-plus/icons-vue'

const router = useRouter()
const store = useStore()

const activeMenu = computed(() => router.currentRoute.value.path)
const isAdmin = computed(() => store.getters['auth/userRole'] === 'admin')
</script>

<style scoped>
.sidebar {
  width: 220px;
  background: #2c3e50;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  background: #1a252f;
  border-bottom: 1px solid #34495e;
}

.sidebar-header h1 {
  font-size: 16px;
  margin: 0;
  font-weight: 600;
}

.sidebar-nav {
  flex: 1;
  padding-top: 20px;
}

.el-menu {
  background: transparent;
  border-right: none;
}

.el-menu-item {
  color: #bdc3c7;
  height: 48px;
  line-height: 48px;
}

.el-menu-item:hover,
.el-menu-item.is-active {
  background: #34495e;
  color: white;
}

.el-menu-item i {
  margin-right: 8px;
}
</style>
