<template>
  <div class="home">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <h1 v-if="!userStore.isLoggedIn">欢迎使用学生就业管理平台</h1>
        <h1 v-else-if="userStore.isStudent">欢迎回来，{{ userStore.user?.real_name || '同学' }}</h1>
        <h1 v-else-if="userStore.isEnterprise">欢迎回来，{{ userStore.user?.real_name || 'HR' }}</h1>
        <h1 v-else>欢迎使用学生就业管理平台</h1>

        <p v-if="!userStore.isLoggedIn">为学生提供全方位的就业服务，助力职业发展</p>
        <p v-else-if="userStore.isStudent">管理您的求职进度，发现更多就业机会</p>
        <p v-else-if="userStore.isEnterprise">高效管理招聘流程，发现优秀人才</p>
        <p v-else>为学生和企业提供专业的就业服务平台</p>

        <div class="banner-actions" v-if="!userStore.isLoggedIn">
          <el-button type="primary" size="large" @click="$router.push('/register')">立即注册</el-button>
          <el-button size="large" @click="$router.push('/login')">登录</el-button>
        </div>
        <div class="banner-actions" v-else-if="userStore.isStudent">
          <el-button type="primary" size="large" @click="$router.push('/job-market')">浏览职位</el-button>
          <el-button size="large" @click="$router.push('/my-employment')">我的就业</el-button>
        </div>
        <div class="banner-actions" v-else-if="userStore.isEnterprise">
          <el-button type="primary" size="large" @click="$router.push('/recruitment-management')">招聘管理</el-button>
          <el-button size="large" @click="$router.push('/job-market')">发布职位</el-button>
        </div>
      </div>
    </div>

    <!-- 统计数据 - 根据用户类型显示不同内容 -->
    <div class="stats-section">
      <!-- 学生用户或未登录用户看到的统计 -->
      <div v-if="!userStore.isEnterprise" class="stats-container">
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalUsers }}</div>
          <div class="stat-label">注册用户</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalJobs }}</div>
          <div class="stat-label">招聘职位</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <div class="stat-label">求职申请</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ stats.successfulPlacements }}</div>
          <div class="stat-label">成功就业</div>
        </div>
      </div>

      <!-- 企业用户看到的招聘统计 -->
      <div v-else class="stats-container">
        <div class="stat-card">
          <div class="stat-number">{{ enterpriseStats.publishedJobs }}</div>
          <div class="stat-label">发布职位</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ enterpriseStats.receivedApplications }}</div>
          <div class="stat-label">收到简历</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ enterpriseStats.scheduledInterviews }}</div>
          <div class="stat-label">安排面试</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ enterpriseStats.hiredCandidates }}</div>
          <div class="stat-label">成功录用</div>
        </div>
      </div>
    </div>

    <!-- 最新职位 / 企业快捷操作 -->
    <div class="jobs-section">
      <!-- 学生用户或未登录用户看到最新职位 -->
      <div v-if="!userStore.isEnterprise">
        <div class="section-header">
          <h2>最新职位</h2>
          <el-button type="primary" link @click="$router.push('/job-market')">查看更多</el-button>
        </div>
        <div class="jobs-grid">
          <div v-for="job in latestJobs" :key="job.id" class="job-card" @click="viewJobDetail(job.id)">
            <div class="job-header">
              <h3>{{ job.title }}</h3>
              <div class="salary">{{ job.salary_range }}</div>
            </div>
            <div class="job-info">
              <p class="company">{{ job.company_name }}</p>
              <p class="location">{{ job.location }}</p>
              <p class="experience">经验要求：{{ job.experience_required }}</p>
              <p class="category">{{ job.category_name }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 企业用户看到快捷操作 -->
      <div v-else>
        <div class="section-header">
          <h2>快捷操作</h2>
        </div>
        <div class="enterprise-actions">
          <el-card class="action-card" @click="$router.push('/recruitment-management')">
            <div class="action-icon">
              <el-icon size="32"><Briefcase /></el-icon>
            </div>
            <div class="action-title">职位管理</div>
            <div class="action-desc">发布、编辑和管理您的招聘职位</div>
          </el-card>

          <el-card class="action-card" @click="$router.push('/resume-management')">
            <div class="action-icon">
              <el-icon size="32"><Document /></el-icon>
            </div>
            <div class="action-title">简历管理</div>
            <div class="action-desc">查看和筛选收到的求职简历</div>
          </el-card>

          <el-card class="action-card" @click="$router.push('/interview-management')">
            <div class="action-icon">
              <el-icon size="32"><Calendar /></el-icon>
            </div>
            <div class="action-title">面试管理</div>
            <div class="action-desc">安排面试时间，记录面试结果</div>
          </el-card>

          <el-card class="action-card" @click="$router.push('/profile')">
            <div class="action-icon">
              <el-icon size="32"><OfficeBuilding /></el-icon>
            </div>
            <div class="action-title">企业信息</div>
            <div class="action-desc">管理企业基本信息和认证</div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 平台特色 -->
    <div class="features-section">
      <h2>平台特色</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>智能匹配</h3>
          <p>基于AI算法，为学生推荐最适合的职位</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>在线咨询</h3>
          <p>专业的就业指导老师在线答疑解惑</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>数据分析</h3>
          <p>详细的就业数据分析，助力职业规划</p>
        </div>
      </div>
    </div>

    <!-- 测试按钮 -->
    <div class="test-section">
      <el-button @click="testApiConnection" type="success">测试API连接</el-button>
      <el-button @click="testLogin" type="warning">测试登录</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { Briefcase, Document, Calendar, OfficeBuilding } from '@element-plus/icons-vue'
import request from '@/utils/request'

const userStore = useUserStore()

const stats = ref({
  totalUsers: 0,
  totalJobs: 0,
  totalApplications: 0,
  successfulPlacements: 0
})

const enterpriseStats = ref({
  publishedJobs: 0,
  receivedApplications: 0,
  scheduledInterviews: 0,
  hiredCandidates: 0
})

const latestJobs = ref([])

const fetchStats = async () => {
  try {
    if (userStore.isEnterprise) {
      // 企业用户获取招聘统计数据
      const response = await request.get('/admin/stats/enterprise-dashboard/')
      enterpriseStats.value = response.data
      console.log('获取企业统计数据成功:', enterpriseStats.value)
    } else {
      // 学生用户或未登录用户获取平台统计数据
      const response = await request.get('/stats/dashboard/')
      stats.value = response.data
      console.log('获取统计数据成功:', stats.value)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
    // 使用默认值
    if (userStore.isEnterprise) {
      enterpriseStats.value = {
        publishedJobs: 0,
        receivedApplications: 0,
        scheduledInterviews: 0,
        hiredCandidates: 0
      }
    } else {
      stats.value = {
        totalUsers: 0,
        totalJobs: 0,
        totalApplications: 0,
        successfulPlacements: 0
      }
    }
  }
}

const fetchLatestJobs = async () => {
  try {
    const response = await request.get('/jobs/latest/?limit=3')
    latestJobs.value = response.data || []
    console.log('获取最新职位成功:', latestJobs.value)
  } catch (error) {
    console.error('获取最新职位失败:', error)
    ElMessage.error('获取最新职位失败')
    // 使用空数组，不再使用模拟数据
    latestJobs.value = []
  }
}

// 测试API连接
const testApiConnection = async () => {
  try {
    const response = await request.get('/health/')
    console.log('API连接测试成功:', response.data)
    ElMessage.success('API连接正常')
  } catch (error) {
    console.error('API连接测试失败:', error)
    ElMessage.error('API连接失败: ' + (error.response?.data?.message || error.message))
  }
}

// 测试登录功能
const testLogin = async () => {
  try {
    const result = await userStore.login({
      phone: '13800138000',
      password: '123456'
    })
    if (result.success) {
      ElMessage.success('测试登录成功')
      // 刷新页面数据
      fetchStats()
      fetchLatestJobs()
    } else {
      ElMessage.error('测试登录失败: ' + result.message)
    }
  } catch (error) {
    console.error('测试登录错误:', error)
    ElMessage.error('测试登录错误')
  }
}

// 查看职位详情
const viewJobDetail = (jobId) => {
  // 暂时跳转到职位市场页面，后续可以实现职位详情页
  ElMessage.info(`查看职位详情: ${jobId}`)
  // $router.push(`/jobs/${jobId}`)
}

onMounted(() => {
  fetchStats()
  // 只有非企业用户才获取最新职位
  if (!userStore.isEnterprise) {
    fetchLatestJobs()
  }
})
</script>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
}

.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
}

.banner-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.banner-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.banner-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.stats-section {
  padding: 60px 0;
  background: #f8f9fa;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #6c757d;
}

.jobs-section, .features-section {
  padding: 60px 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2rem;
  color: #2c3e50;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.enterprise-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  padding: 30px 20px;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.action-icon {
  color: #409eff;
  margin-bottom: 15px;
}

.action-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.action-desc {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.job-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.job-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.job-header h3 {
  font-size: 1.2rem;
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

.salary {
  color: #e74c3c;
  font-weight: 600;
  font-size: 1.1rem;
}

.job-info p {
  margin: 0.5rem 0;
  color: #6c757d;
}

.company {
  font-weight: 500;
  color: #495057 !important;
}

.features-section {
  background: #f8f9fa;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2rem;
  color: #2c3e50;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #6c757d;
  line-height: 1.6;
}

.test-section {
  padding: 2rem;
  text-align: center;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.test-section .el-button {
  margin: 0 0.5rem;
}
</style>
