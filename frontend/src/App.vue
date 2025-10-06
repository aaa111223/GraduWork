<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// ?????????????
onMounted(async () => {
  if (userStore.token) {
    try {
      await userStore.fetchUserInfo()
    } catch (error) {
      console.error('????????:', error)
      // ??token?????????
      userStore.logout()
    }
  }
})
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f0f2f5;
  color: #303133;
}

#app {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

/* Element Plus ??????? */
.el-button {
  border-radius: 6px;
}

.el-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-input__inner {
  border-radius: 6px;
}

.el-select .el-input__inner {
  border-radius: 6px;
}

/* ????????? */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* ??Element Plus????? */
.el-container {
  width: 100%;
}

.el-main {
  width: 100%;
  padding: 20px;
}

.el-row {
  width: 100%;
}

.el-col {
  width: 100%;
}

/* ????? */
@media (max-width: 768px) {
  .el-main {
    padding: 10px;
  }

  .el-card {
    margin-bottom: 10px;
  }
}
</style>
