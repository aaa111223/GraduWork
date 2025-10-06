<template>
  <div class="test-login">
    <h2>登录功能测试</h2>
    
    <div class="test-section">
      <h3>1. 直接API测试</h3>
      <button @click="testDirectAPI" :disabled="loading">测试直接API调用</button>
      <div v-if="directResult" class="result" :class="directResult.success ? 'success' : 'error'">
        {{ directResult.message }}
      </div>
    </div>
    
    <div class="test-section">
      <h3>2. Store测试</h3>
      <button @click="testStore" :disabled="loading">测试Store登录</button>
      <div v-if="storeResult" class="result" :class="storeResult.success ? 'success' : 'error'">
        {{ storeResult.message }}
      </div>
    </div>
    
    <div class="test-section">
      <h3>3. 错误测试</h3>
      <button @click="testError" :disabled="loading">测试错误处理</button>
      <div v-if="errorResult" class="result" :class="errorResult.success ? 'success' : 'error'">
        {{ errorResult.message }}
      </div>
    </div>
    
    <div class="test-section">
      <h3>4. 用户状态</h3>
      <div class="user-info">
        <p>登录状态: {{ userStore.isLoggedIn ? '已登录' : '未登录' }}</p>
        <p v-if="userStore.user">用户信息: {{ userStore.user.real_name }} ({{ userStore.user.phone }})</p>
        <p>Token: {{ userStore.token ? '存在' : '不存在' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

const userStore = useUserStore()
const loading = ref(false)
const directResult = ref(null)
const storeResult = ref(null)
const errorResult = ref(null)

const testDirectAPI = async () => {
  loading.value = true
  directResult.value = null
  
  try {
    const response = await request.post('/auth/login/', {
      phone: '13800138000',
      password: '123456'
    })
    
    directResult.value = {
      success: true,
      message: `✅ 直接API调用成功！用户: ${response.data.user?.real_name}`
    }
  } catch (error) {
    console.error('直接API测试错误:', error)
    directResult.value = {
      success: false,
      message: `❌ 直接API调用失败: ${error.response?.data?.non_field_errors?.[0] || error.message}`
    }
  } finally {
    loading.value = false
  }
}

const testStore = async () => {
  loading.value = true
  storeResult.value = null
  
  try {
    const result = await userStore.login({
      phone: '13800138000',
      password: '123456'
    })
    
    if (result.success) {
      storeResult.value = {
        success: true,
        message: `✅ Store登录成功！用户: ${userStore.user?.real_name}`
      }
    } else {
      storeResult.value = {
        success: false,
        message: `❌ Store登录失败: ${result.message}`
      }
    }
  } catch (error) {
    console.error('Store测试错误:', error)
    storeResult.value = {
      success: false,
      message: `❌ Store测试异常: ${error.message}`
    }
  } finally {
    loading.value = false
  }
}

const testError = async () => {
  loading.value = true
  errorResult.value = null
  
  try {
    const result = await userStore.login({
      phone: '13800138000',
      password: 'wrongpassword'
    })
    
    if (!result.success) {
      errorResult.value = {
        success: true,
        message: `✅ 错误处理正常: ${result.message}`
      }
    } else {
      errorResult.value = {
        success: false,
        message: `❌ 错误处理异常: 应该失败但成功了`
      }
    }
  } catch (error) {
    console.error('错误测试异常:', error)
    errorResult.value = {
      success: false,
      message: `❌ 错误测试异常: ${error.message}`
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.test-login {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.test-section {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-section h3 {
  margin-top: 0;
  color: #333;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover:not(:disabled) {
  background: #0056b3;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.result {
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px;
  font-weight: bold;
}

.result.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.result.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.user-info {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.user-info p {
  margin: 5px 0;
}
</style>
