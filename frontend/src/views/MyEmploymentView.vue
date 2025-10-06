<template>
  <div class="my-employment">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1>我的就业</h1>
        <p>管理您的求职进度和就业信息</p>
      </div>
      <div class="header-right" v-if="currentUser">
        <div class="user-info">
          <el-avatar :src="currentUser.avatar" :size="50">
            {{ currentUser.real_name?.charAt(0) || 'U' }}
          </el-avatar>
          <div class="user-details">
            <div class="user-name">{{ currentUser.real_name || '未设置姓名' }}</div>
            <div class="user-type">{{ currentUser.user_type === 'student' ? '学生用户' : '用户' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards" v-loading="statsLoading">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.appliedJobs }}</div>
          <div class="stat-label">已申请职位</div>
        </div>
        <el-icon class="stat-icon"><Document /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.interviews }}</div>
          <div class="stat-label">面试邀请</div>
        </div>
        <el-icon class="stat-icon"><ChatDotRound /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.offers }}</div>
          <div class="stat-label">收到Offer</div>
        </div>
        <el-icon class="stat-icon"><Trophy /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.favoriteJobs }}</div>
          <div class="stat-label">收藏职位</div>
        </div>
        <el-icon class="stat-icon"><Star /></el-icon>
      </el-card>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧：申请记录 -->
      <div class="left-section">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的申请记录</span>
              <el-button type="primary" size="small" @click="refreshApplications">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>

          <el-table :data="applications" style="width: 100%" v-loading="applicationsLoading">
            <el-table-column prop="jobTitle" label="职位名称" min-width="180" show-overflow-tooltip />
            <el-table-column prop="companyName" label="公司名称" min-width="140" show-overflow-tooltip />
            <el-table-column prop="jobLocation" label="工作地点" width="100" />
            <el-table-column prop="expectedSalary" label="期望薪资" width="100" />
            <el-table-column prop="appliedDate" label="申请时间" width="110" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ scope.row.statusText }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" @click="viewApplication(scope.row)">查看</el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="withdrawApplication(scope.row)"
                  :disabled="!canWithdraw(scope.row.status)"
                >
                  撤回
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 空状态 -->
          <div v-if="!applicationsLoading && applications.length === 0" class="no-data">
            <el-empty description="暂无申请记录">
              <el-button type="primary" @click="$router.push('/job-market')">
                去申请职位
              </el-button>
            </el-empty>
          </div>
        </el-card>
      </div>

      <!-- 右侧：快捷操作 -->
      <div class="right-section">
        <!-- 申请状态分析 -->
        <el-card>
          <template #header>
            <span>申请状态分析</span>
          </template>

          <div class="status-analysis" v-loading="applicationsLoading">
            <div class="status-item" v-for="(count, status) in statusCounts" :key="status">
              <div class="status-label">{{ getStatusText(status) }}</div>
              <div class="status-count" :style="{ color: getStatusColor(status) }">{{ count }}</div>
            </div>
          </div>
        </el-card>

        <el-card style="margin-top: 20px;">
          <template #header>
            <span>快捷操作</span>
          </template>

          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/job-market')" block>
              <el-icon><Search /></el-icon>
              浏览职位
            </el-button>

            <el-button @click="$router.push('/profile')" block>
              <el-icon><User /></el-icon>
              完善简历
            </el-button>

            <el-button @click="showResumeDialog = true" block>
              <el-icon><Document /></el-icon>
              上传简历
            </el-button>

            <el-button @click="$router.push('/feedback')" block>
              <el-icon><ChatDotRound /></el-icon>
              意见反馈
            </el-button>
          </div>
        </el-card>

        <!-- 面试提醒 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>近期面试</span>
          </template>

          <div v-if="upcomingInterviews.length === 0" class="no-data">
            暂无面试安排
          </div>

          <div v-else>
            <div v-for="interview in upcomingInterviews" :key="interview.id" class="interview-item">
              <div class="interview-info">
                <h4>{{ interview.jobTitle }}</h4>
                <p>{{ interview.companyName }}</p>
                <p class="interview-time">
                  <el-icon><Clock /></el-icon>
                  {{ interview.interviewTime }}
                </p>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 简历上传对话框 -->
    <el-dialog v-model="showResumeDialog" title="上传简历" width="500px">
      <el-upload
        class="upload-demo"
        drag
        action="#"
        :before-upload="handleResumeUpload"
        accept=".pdf,.doc,.docx"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传 PDF/DOC/DOCX 文件，且不超过 10MB
          </div>
        </template>
      </el-upload>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showResumeDialog = false">取消</el-button>
          <el-button type="primary" @click="showResumeDialog = false">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document,
  ChatDotRound,
  Trophy,
  Star,
  Refresh,
  Search,
  User,
  Clock,
  UploadFilled
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

// 响应式数据
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const showResumeDialog = ref(false)
const applicationsLoading = ref(false)
const statsLoading = ref(false)

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)
const currentUser = computed(() => userStore.user)

const stats = ref({
  appliedJobs: 0,
  interviews: 0,
  offers: 0,
  favoriteJobs: 0
})

const applications = ref([])
const upcomingInterviews = ref([])
const favoriteJobs = ref([])

// 计算申请状态统计
const statusCounts = computed(() => {
  const counts = {}
  applications.value.forEach(app => {
    counts[app.status] = (counts[app.status] || 0) + 1
  })
  return counts
})

// 方法
const getStatusType = (status) => {
  const statusMap = {
    'pending': '',
    'reviewing': 'warning',
    'interview': 'warning',
    'accepted': 'success',
    'rejected': 'danger',
    'withdrawn': 'info'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待审核',
    'reviewing': '审核中',
    'interview': '面试中',
    'accepted': '已录用',
    'rejected': '已拒绝',
    'withdrawn': '已撤回'
  }
  return statusMap[status] || status
}

const getJobTypeText = (jobType) => {
  const typeMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'contract': '合同工',
    'freelance': '自由职业'
  }
  return typeMap[jobType] || jobType || '未知'
}

// 判断是否可以撤回申请
const canWithdraw = (status) => {
  // 只有待审核和审核中的申请可以撤回
  return ['pending', 'reviewing'].includes(status)
}

// 获取申请记录
const fetchApplications = async () => {
  applicationsLoading.value = true
  try {
    const response = await request.get('/applications/')
    const applicationList = response.data.results || response.data || []

    applications.value = applicationList.map(app => ({
      id: app.id,
      jobTitle: app.job?.title || '未知职位',
      companyName: app.job?.company_name || '未知公司',
      appliedDate: formatDate(app.applied_at),
      status: app.status,
      statusText: getStatusText(app.status), // 使用本地化的状态文本
      coverLetter: app.cover_letter || '',
      expectedSalary: app.expected_salary ? `${parseFloat(app.expected_salary).toLocaleString()}元` : '面议',
      jobLocation: app.job?.work_city || '未知',
      jobSalaryRange: app.job?.salary_range || '面议',
      jobType: app.job?.job_type || '',
      experienceRequired: app.job?.experience_required || '',
      educationRequired: app.job?.education_required || '',
      skillsRequired: app.job?.skills_required || [],
      jobDescription: app.job?.description || '',
      companyIndustry: app.job?.company_industry || '',
      companySize: app.job?.company_size || '',
      rawData: app
    }))

    console.log('申请记录:', applications.value)
  } catch (error) {
    console.error('获取申请记录失败:', error)
    ElMessage.error('获取申请记录失败')
  } finally {
    applicationsLoading.value = false
  }
}

// 获取收藏职位
const fetchFavoriteJobs = async () => {
  try {
    const response = await request.get('/jobs/favorites/')
    favoriteJobs.value = response.data.results || response.data || []
  } catch (error) {
    console.error('获取收藏职位失败:', error)
  }
}

// 获取统计数据
const fetchStats = async () => {
  statsLoading.value = true
  try {
    // 并行获取各种数据
    const [applicationsRes, favoritesRes] = await Promise.all([
      request.get('/applications/'),
      request.get('/jobs/favorites/').catch(() => ({ data: { results: [] } }))
    ])

    const applicationList = applicationsRes.data.results || applicationsRes.data || []
    const favoriteList = favoritesRes.data.results || favoritesRes.data || []

    // 计算统计数据
    stats.value = {
      appliedJobs: applicationList.length,
      interviews: applicationList.filter(app => app.status === 'interview').length,
      offers: applicationList.filter(app => app.status === 'accepted').length,
      favoriteJobs: favoriteList.length
    }

    console.log('统计数据:', stats.value)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    statsLoading.value = false
  }
}

const refreshApplications = async () => {
  await Promise.all([
    fetchApplications(),
    fetchStats(),
    fetchFavoriteJobs()
  ])
  ElMessage.success('刷新成功')
}

const viewApplication = (application) => {
  // 显示申请详情
  const skillsText = Array.isArray(application.skillsRequired)
    ? application.skillsRequired.join(', ')
    : application.skillsRequired || '无'

  ElMessageBox.alert(
    `
    <div style="text-align: left; max-height: 500px; overflow-y: auto;">
      <h4 style="margin-bottom: 16px; color: #409EFF;">${application.jobTitle}</h4>

      <div style="margin-bottom: 16px;">
        <h5 style="color: #666; margin-bottom: 8px;">基本信息</h5>
        <p><strong>公司:</strong> ${application.companyName}</p>
        <p><strong>行业:</strong> ${application.companyIndustry}</p>
        <p><strong>公司规模:</strong> ${application.companySize}</p>
        <p><strong>工作地点:</strong> ${application.jobLocation}</p>
        <p><strong>薪资范围:</strong> ${application.jobSalaryRange}</p>
        <p><strong>工作类型:</strong> ${getJobTypeText(application.jobType)}</p>
        <p><strong>经验要求:</strong> ${application.experienceRequired}</p>
        <p><strong>学历要求:</strong> ${application.educationRequired}</p>
        <p><strong>技能要求:</strong> ${skillsText}</p>
      </div>

      <div style="margin-bottom: 16px;">
        <h5 style="color: #666; margin-bottom: 8px;">申请信息</h5>
        <p><strong>申请时间:</strong> ${application.appliedDate}</p>
        <p><strong>申请状态:</strong> <span style="color: ${getStatusColor(application.status)}">${application.statusText}</span></p>
        <p><strong>期望薪资:</strong> ${application.expectedSalary}</p>
      </div>

      ${application.jobDescription ? `<div style="margin-bottom: 16px;"><h5 style="color: #666; margin-bottom: 8px;">职位描述</h5><div style="background: #f8f9fa; padding: 12px; border-radius: 4px; line-height: 1.5;">${application.jobDescription}</div></div>` : ''}

      ${application.coverLetter ? `<div><h5 style="color: #666; margin-bottom: 8px;">求职信</h5><div style="background: #f5f5f5; padding: 12px; border-radius: 4px; line-height: 1.5;">${application.coverLetter}</div></div>` : ''}
    </div>
    `,
    '申请详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定',
      customClass: 'application-detail-dialog'
    }
  )
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colorMap = {
    'pending': '#909399',
    'reviewing': '#E6A23C',
    'interview': '#E6A23C',
    'accepted': '#67C23A',
    'rejected': '#F56C6C',
    'withdrawn': '#909399'
  }
  return colorMap[status] || '#909399'
}

const withdrawApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      `确定要撤回对"${application.jobTitle}"的申请吗？撤回后将无法恢复。`,
      '撤回申请',
      {
        confirmButtonText: '确定撤回',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 调用撤回API
    await request.patch(`/applications/${application.id}/`, {
      status: 'withdrawn'
    })

    ElMessage.success('申请已撤回')
    await refreshApplications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('撤回申请失败:', error)
      const errorMsg = error.response?.data?.error || error.response?.data?.message || '撤回申请失败'
      ElMessage.error(errorMsg)
    }
  }
}

const handleResumeUpload = async (file) => {
  const isValidType = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type)
  const isValidSize = file.size / 1024 / 1024 < 10

  if (!isValidType) {
    ElMessage.error('只能上传 PDF/DOC/DOCX 格式的文件!')
    return false
  }
  if (!isValidSize) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }

  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', file.name)
    formData.append('is_default', 'true')

    // 上传简历
    await request.post('/users/users/resumes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    ElMessage.success('简历上传成功!')
    showResumeDialog.value = false

    // 刷新用户信息
    await userStore.fetchUserInfo()

  } catch (error) {
    console.error('简历上传失败:', error)
    const errorMsg = error.response?.data?.error || '简历上传失败，请稍后重试'
    ElMessage.error(errorMsg)
  }

  return false // 阻止自动上传
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化时间
const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 获取面试安排
const fetchInterviews = async () => {
  try {
    // 这里可以添加面试API调用
    // const response = await request.get('/interviews/')
    // upcomingInterviews.value = response.data.results || []

    // 暂时使用模拟数据
    upcomingInterviews.value = []
  } catch (error) {
    console.error('获取面试安排失败:', error)
  }
}

// 初始化数据
const initializeData = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    await Promise.all([
      fetchApplications(),
      fetchStats(),
      fetchFavoriteJobs(),
      fetchInterviews()
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initializeData()
})
</script>

<style scoped>
.my-employment {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.header-left h1 {
  margin: 0 0 8px 0;
  color: white;
  font-size: 2rem;
}

.header-left p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  text-align: right;
}

.user-name {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.user-type {
  font-size: 14px;
  opacity: 0.8;
}

.status-analysis {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.status-item {
  text-align: center;
  padding: 12px;
  border-radius: 8px;
  background: #f8f9fa;
}

.status-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.status-count {
  font-size: 24px;
  font-weight: bold;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-card .el-card__body {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  color: #6c757d;
  font-size: 14px;
}

.stat-icon {
  font-size: 2rem;
  color: #409eff;
  opacity: 0.3;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.no-data {
  text-align: center;
  color: #6c757d;
  padding: 20px;
}

.interview-item {
  padding: 12px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 12px;
}

.interview-item:last-child {
  margin-bottom: 0;
}

.interview-info h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.interview-info p {
  margin: 4px 0;
  color: #6c757d;
  font-size: 14px;
}

.interview-time {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #409eff !important;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
