<template>
  <div class="test-page">
    <h1>中文编码测试页面</h1>
    
    <div class="test-section">
      <h2>静态中文文本测试</h2>
      <p>这是一段中文文本：欢迎使用学生就业管理平台</p>
      <p>职位信息：Python后端开发工程师 - 科技有限公司 - 北京市</p>
    </div>

    <div class="test-section">
      <h2>API数据测试</h2>
      <el-button @click="testApi" type="primary">测试API数据</el-button>
      <div v-if="apiData" class="api-result">
        <h3>API返回数据：</h3>
        <pre>{{ JSON.stringify(apiData, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>动态数据测试</h2>
      <div v-for="job in jobs" :key="job.id" class="job-item">
        <h4>{{ job.title }}</h4>
        <p>公司：{{ job.company_name }}</p>
        <p>地点：{{ job.location }}</p>
        <p>经验：{{ job.experience_required }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const apiData = ref(null)
const jobs = ref([
  {
    id: 1,
    title: 'Python后端开发工程师',
    company_name: '科技有限公司',
    location: '北京市',
    experience_required: '3-5年'
  },
  {
    id: 2,
    title: 'Vue.js前端开发工程师',
    company_name: '互联网科技公司',
    location: '上海市',
    experience_required: '2-4年'
  }
])

const testApi = async () => {
  try {
    const response = await request.get('/jobs/')
    apiData.value = response.data
    ElMessage.success('API测试成功')
    console.log('API响应数据:', response.data)
  } catch (error) {
    console.error('API测试失败:', error)
    ElMessage.error('API测试失败: ' + error.message)
  }
}
</script>

<style scoped>
.test-page {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.job-item {
  background: #f8f9fa;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
}

.api-result {
  margin-top: 1rem;
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
