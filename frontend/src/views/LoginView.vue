<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>用户登录</h2>
          <p>欢迎回到学生就业管理平台</p>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        size="large"
      >
        <el-form-item prop="phone">
          <el-input
            v-model="loginForm.phone"
            placeholder="请输入手机号"
            prefix-icon="Phone"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <div class="form-options">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <div class="register-link">
            还没有账号？
            <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
          </div>
        </el-form-item>
      </el-form>

      <!-- 测试账号 -->
      <div class="test-accounts">
        <el-divider>测试账号</el-divider>
        <div class="test-account-list">
          <div class="test-account-item">
            <span class="account-type">学生账号:</span>
            <span class="account-info">13800138000 / 123456</span>
            <el-button size="small" @click="fillTestAccount('student')">使用</el-button>
          </div>
          <div class="test-account-item">
            <span class="account-type">管理员:</span>
            <span class="account-info">13800138001 / admin123</span>
            <el-button size="small" @click="fillTestAccount('admin')">使用</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  phone: '',
  password: '',
  remember: false
})

const loginRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    const result = await userStore.login({
      phone: loginForm.phone,
      password: loginForm.password
    })

    if (result.success) {
      ElMessage.success('登录成功')
      // 获取用户信息
      await userStore.fetchUserInfo()
      // 跳转到首页或之前的页面
      const redirect = router.currentRoute.value.query.redirect || '/'
      router.push(redirect)
    } else {
      ElMessage.error(result.message || '登录失败')
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

const fillTestAccount = (type) => {
  if (type === 'student') {
    loginForm.phone = '13800138000'
    loginForm.password = '123456'
  } else if (type === 'admin') {
    loginForm.phone = '13800138001'
    loginForm.password = 'admin123'
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.card-header {
  text-align: center;
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
  font-weight: bold;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.register-link {
  text-align: center;
  width: 100%;
  color: #909399;
  font-size: 14px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-input__inner) {
  height: 48px;
  line-height: 48px;
}

:deep(.el-button) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.test-accounts {
  margin-top: 24px;
}

.test-account-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.test-account-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 14px;
}

.account-type {
  font-weight: 500;
  color: #495057;
  min-width: 70px;
}

.account-info {
  color: #6c757d;
  flex: 1;
  margin: 0 12px;
}

@media (max-width: 480px) {
  .test-account-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .account-info {
    margin: 0;
  }
}
</style>
