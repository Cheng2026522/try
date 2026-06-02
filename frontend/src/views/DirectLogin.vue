<template>
  <div class="login-container">
    <div class="login-box">
      <h2>建设集团管理系统</h2>
      <p style="text-align: center; color: #666; margin-bottom: 20px;">欢迎登录</p>
      
      <div class="form-group">
        <label>用户名</label>
        <input 
          type="text" 
          v-model="username" 
          placeholder="请输入用户名"
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label>密码</label>
        <input 
          type="password" 
          v-model="password" 
          placeholder="请输入密码"
          class="form-input"
        />
      </div>
      
      <button @click="handleLogin" class="login-btn">登录</button>
      
      <div v-if="message" :class="['message', messageType]">{{ message }}</div>
      
      <div v-if="responseData" class="response-data">
        <h4>API返回数据:</h4>
        <pre>{{ JSON.stringify(responseData, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const message = ref('')
const messageType = ref('error')
const responseData = ref(null)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    message.value = '请输入用户名和密码'
    messageType.value = 'error'
    return
  }
  
  message.value = '登录中...'
  messageType.value = 'info'
  
  try {
    const response = await axios.post('/api/auth/login/', {
      username: username.value,
      password: password.value
    })
    
    responseData.value = response.data
    message.value = '登录成功!'
    messageType.value = 'success'
    
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('role', response.data.role)
    localStorage.setItem('user', JSON.stringify({
      id: response.data.user_id,
      username: response.data.username,
      role: response.data.role,
      phone: response.data.phone
    }))
    
    setTimeout(() => {
      router.push('/')
    }, 1500)
    
  } catch (error) {
    responseData.value = error.response?.data || error.message
    message.value = error.response?.data?.non_field_errors?.[0] || '登录失败: ' + (error.message || '未知错误')
    messageType.value = 'error'
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 450px;
}

.login-box h2 {
  text-align: center;
  color: #333;
  margin-bottom: 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #667eea;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.login-btn:hover {
  background: #764ba2;
}

.message {
  text-align: center;
  margin-top: 16px;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
}

.message.error {
  background: #fef0f0;
  color: #dc3545;
}

.message.success {
  background: #f0fdf4;
  color: #22c55e;
}

.message.info {
  background: #eff6ff;
  color: #3b82f6;
}

.response-data {
  margin-top: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 12px;
}

.response-data h4 {
  margin-bottom: 8px;
  color: #333;
}

.response-data pre {
  white-space: pre-wrap;
  word-break: break-all;
  color: #666;
}
</style>
