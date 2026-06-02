<template>
  <div class="user-management">
    <Sidebar />
    <div class="main-content">
      <Header />
      
      <div class="content-wrapper">
        <div class="toolbar">
          <el-button type="primary" @click="showAddUser = true">
            <el-icon><Plus /></el-icon>
            添加用户
          </el-button>
        </div>

        <div class="search-bar">
          <el-input v-model="searchQuery" placeholder="搜索用户名" @input="handleSearch">
            <template #append>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select v-model="selectedRole" placeholder="筛选角色">
            <el-option label="全部" value="" />
            <el-option label="管理员" value="admin" />
            <el-option label="项目经理" value="project_manager" />
            <el-option label="普通员工" value="staff" />
          </el-select>
        </div>

        <el-table :data="filteredUsers" border>
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="phone" label="联系电话" />
          <el-table-column prop="role" label="角色" :formatter="formatRole" />
          <el-table-column prop="is_active" label="状态" :formatter="formatActive" />
          <el-table-column prop="last_login" label="最后登录" :formatter="formatTime" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="editUser(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteUser(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-dialog title="添加用户" :visible.sync="showAddUser" width="450px">
          <el-form :model="userForm" label-width="100px">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="userForm.username" placeholder="请输入用户名" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="userForm.password" placeholder="请输入密码" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="userForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="角色">
              <el-select v-model="userForm.role" placeholder="请选择角色">
                <el-option label="管理员" value="admin" />
                <el-option label="项目经理" value="project_manager" />
                <el-option label="普通员工" value="staff" />
              </el-select>
            </el-form-item>
          </el-form>
          
          <template #footer>
            <el-button @click="showAddUser = false">取消</el-button>
            <el-button type="primary" @click="createUser">创建</el-button>
          </template>
        </el-dialog>

        <el-dialog title="编辑用户" :visible.sync="showEditUser" width="450px">
          <el-form :model="editForm" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="editForm.username" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="editForm.email" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="editForm.phone" />
            </el-form-item>
            <el-form-item label="角色">
              <el-select v-model="editForm.role">
                <el-option label="管理员" value="admin" />
                <el-option label="项目经理" value="project_manager" />
                <el-option label="普通员工" value="staff" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-switch v-model="editForm.is_active" active-text="启用" inactive-text="禁用" />
            </el-form-item>
          </el-form>
          
          <template #footer>
            <el-button @click="showEditUser = false">取消</el-button>
            <el-button type="primary" @click="updateUser">保存</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import api from '@/utils/api'

const store = useStore()

const searchQuery = ref('')
const selectedRole = ref('')
const showAddUser = ref(false)
const showEditUser = ref(false)

const users = ref([])
const editingUserId = ref(null)

const userForm = reactive({
  username: '',
  password: '',
  email: '',
  phone: '',
  role: 'staff'
})

const editForm = reactive({
  username: '',
  email: '',
  phone: '',
  role: 'staff',
  is_active: true
})

const filteredUsers = computed(() => {
  let result = users.value
  if (searchQuery.value) {
    result = result.filter(u => u.username.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  if (selectedRole.value) {
    result = result.filter(u => u.role === selectedRole.value)
  }
  return result
})

const formatRole = (row) => {
  const roles = { admin: '管理员', project_manager: '项目经理', staff: '普通员工' }
  return roles[row.role] || row.role
}

const formatActive = (row) => {
  return row.is_active ? '启用' : '禁用'
}

const formatTime = (row) => {
  return row.last_login?.substring(0, 19).replace('T', ' ') || '从未登录'
}

const handleSearch = () => {}

const fetchUsers = async () => {
  try {
    const response = await api.get('/auth/users/')
    users.value = response.data.results || response.data
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

const createUser = async () => {
  if (!userForm.username || !userForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  
  try {
    await api.post('/auth/register/', userForm)
    ElMessage.success('用户创建成功')
    showAddUser.value = false
    userForm.username = ''
    userForm.password = ''
    userForm.email = ''
    userForm.phone = ''
    userForm.role = 'staff'
    await fetchUsers()
  } catch (error) {
    ElMessage.error(error.response?.data?.username?.[0] || '用户创建失败')
  }
}

const editUser = (user) => {
  editingUserId.value = user.id
  editForm.username = user.username
  editForm.email = user.email || ''
  editForm.phone = user.phone || ''
  editForm.role = user.role
  editForm.is_active = user.is_active
  showEditUser.value = true
}

const updateUser = async () => {
  try {
    await api.patch(`/auth/users/${editingUserId.value}/`, {
      email: editForm.email,
      phone: editForm.phone,
      role: editForm.role,
      is_active: editForm.is_active
    })
    ElMessage.success('用户信息已更新')
    showEditUser.value = false
    await fetchUsers()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const deleteUser = async (user) => {
  try {
    await api.delete(`/auth/users/${user.id}/`)
    ElMessage.success('用户已删除')
    await fetchUsers()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-management {
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
</style>
