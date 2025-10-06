<template>
  <el-container class="main-layout">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <h2 class="logo">学生就业管理平台</h2>
      </div>
      <div class="header-right">
        <el-dropdown v-if="userStore.isLoggedIn" @command="handleUserCommand">
          <span class="user-info">
            <el-avatar :size="32" :src="userStore.user?.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span class="username">{{ userStore.user?.username }}</span>
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="feedback">我的反馈</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <div v-else class="auth-buttons">
          <el-button type="primary" @click="$router.push('/login')">登录</el-button>
          <el-button @click="$router.push('/register')">注册</el-button>
        </div>
      </div>
    </el-header>

    <el-container>
      <!-- 侧边导航栏 -->
      <el-aside width="200px" class="sidebar">
        <el-menu
          :default-active="$route.path"
          class="sidebar-menu"
          router
          :collapse="false"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-menu-item index="/my-employment" v-if="userStore.isLoggedIn">
            <el-icon><User /></el-icon>
            <span>我的就业</span>
          </el-menu-item>
          
          <el-menu-item index="/job-market">
            <el-icon><Briefcase /></el-icon>
            <span>就业市场</span>
          </el-menu-item>
          
          <el-menu-item index="/applications" v-if="userStore.isLoggedIn">
            <el-icon><Document /></el-icon>
            <span>申请与管理</span>
          </el-menu-item>
          
          <el-menu-item index="/system-management" v-if="userStore.isAdmin">
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </el-menu-item>
          
          <el-menu-item index="/profile" v-if="userStore.isLoggedIn">
            <el-icon><UserFilled /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
          
          <el-menu-item index="/feedback" v-if="userStore.isLoggedIn">
            <el-icon><ChatDotRound /></el-icon>
            <span>我的反馈</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'feedback':
      router.push('/feedback')
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('退出登录成功')
      router.push('/')
      break
  }
}
</script>

<style scoped>
.main-layout {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  flex-shrink: 0;
}

.header-left .logo {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: white;
}

.username {
  margin: 0 8px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.sidebar {
  background-color: #f5f5f5;
  border-right: 1px solid #e6e6e6;
  width: 200px;
  flex-shrink: 0;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  flex: 1;
  overflow-y: auto;
  width: 100%;
}

/* 确保容器正确填充 */
.el-container {
  width: 100%;
  flex: 1;
}

.el-container.is-vertical {
  height: 100%;
}
</style>
