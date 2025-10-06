<template>
  <div class="applications">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>申请与管理</h1>
      <p>管理您的求职申请和面试安排</p>
    </div>

    <!-- 统计概览 -->
    <div class="stats-overview">
      <el-card class="stat-item">
        <div class="stat-content">
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <div class="stat-label">总申请数</div>
        </div>
      </el-card>

      <el-card class="stat-item">
        <div class="stat-content">
          <div class="stat-number">{{ stats.pendingApplications }}</div>
          <div class="stat-label">待处理</div>
        </div>
      </el-card>

      <el-card class="stat-item">
        <div class="stat-content">
          <div class="stat-number">{{ stats.interviewInvitations }}</div>
          <div class="stat-label">面试邀请</div>
        </div>
      </el-card>

      <el-card class="stat-item">
        <div class="stat-content">
          <div class="stat-number">{{ stats.offers }}</div>
          <div class="stat-label">收到Offer</div>
        </div>
      </el-card>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <!-- 申请记录 -->
      <el-tab-pane label="申请记录" name="applications">
        <div class="tab-content">
          <div class="table-header">
            <div class="header-left">
              <el-select v-model="applicationFilter" @change="filterApplications" style="width: 150px">
                <el-option label="全部状态" value="" />
                <el-option label="待审核" value="pending" />
                <el-option label="审核中" value="reviewing" />
                <el-option label="面试中" value="interview" />
                <el-option label="已录用" value="accepted" />
                <el-option label="已拒绝" value="rejected" />
                <el-option label="已撤回" value="withdrawn" />
              </el-select>
            </div>
            <div class="header-right">
              <el-button @click="refreshApplications" :loading="loading">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </div>

          <el-table :data="filteredApplications" v-loading="loading" style="width: 100%">
            <el-table-column prop="jobTitle" label="职位名称" width="200" />
            <el-table-column prop="companyName" label="公司名称" width="150" />
            <el-table-column prop="appliedDate" label="申请时间" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="salary" label="薪资" width="120" />
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button size="small" @click="viewApplication(scope.row)">查看</el-button>
                <el-button
                  size="small"
                  type="warning"
                  v-if="scope.row.status === 'interview'"
                  @click="scheduleInterview(scope.row)"
                >
                  安排面试
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  v-if="['pending', 'reviewing'].includes(scope.row.status)"
                  @click="withdrawApplication(scope.row)"
                >
                  撤回
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 面试安排 -->
      <el-tab-pane label="面试安排" name="interviews">
        <div class="tab-content">
          <div class="interview-calendar">
            <el-calendar v-model="calendarDate">
              <template #date-cell="{ data }">
                <div class="calendar-cell">
                  <div class="date-number">{{ data.day.split('-').slice(-1)[0] }}</div>
                  <div v-if="getInterviewsForDate(data.day).length > 0" class="interview-indicator">
                    <el-badge :value="getInterviewsForDate(data.day).length" type="primary" />
                  </div>
                </div>
              </template>
            </el-calendar>
          </div>

          <div class="interview-list">
            <h3>近期面试安排</h3>
            <div v-if="upcomingInterviews.length === 0" class="no-data">
              暂无面试安排
            </div>
            <div v-else>
              <el-card v-for="interview in upcomingInterviews" :key="interview.id" class="interview-card">
                <div class="interview-info">
                  <div class="interview-main">
                    <h4>{{ interview.jobTitle }}</h4>
                    <p class="company">{{ interview.companyName }}</p>
                    <p class="interview-time">
                      <el-icon><Clock /></el-icon>
                      {{ interview.interviewTime }}
                    </p>
                    <p class="interview-type">
                      <el-tag size="small">{{ interview.type }}</el-tag>
                    </p>
                  </div>
                  <div class="interview-actions">
                    <el-button size="small" @click="viewInterviewDetail(interview)">详情</el-button>
                    <el-button size="small" type="success" @click="confirmInterview(interview)">
                      确认参加
                    </el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- Offer管理 -->
      <el-tab-pane label="Offer管理" name="offers">
        <div class="tab-content">
          <div v-if="offers.length === 0" class="no-data">
            暂无Offer信息
          </div>
          <div v-else>
            <el-card v-for="offer in offers" :key="offer.id" class="offer-card">
              <div class="offer-header">
                <h3>{{ offer.jobTitle }}</h3>
                <el-tag :type="offer.status === 'pending' ? 'warning' : 'success'">
                  {{ offer.status === 'pending' ? '待回复' : '已接受' }}
                </el-tag>
              </div>

              <div class="offer-details">
                <p><strong>公司：</strong>{{ offer.companyName }}</p>
                <p><strong>薪资：</strong>{{ offer.salary }}</p>
                <p><strong>入职时间：</strong>{{ offer.startDate }}</p>
                <p><strong>回复截止：</strong>{{ offer.deadline }}</p>
              </div>

              <div class="offer-actions" v-if="offer.status === 'pending'">
                <el-button type="success" @click="acceptOffer(offer)">接受Offer</el-button>
                <el-button type="danger" @click="rejectOffer(offer)">拒绝Offer</el-button>
                <el-button @click="negotiateOffer(offer)">协商条件</el-button>
              </div>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 申请详情对话框 -->
    <el-dialog v-model="showApplicationDetail" title="申请详情" width="600px">
      <div v-if="selectedApplication" class="application-detail">
        <h3>{{ selectedApplication.jobTitle }}</h3>
        <p><strong>公司：</strong>{{ selectedApplication.companyName }}</p>
        <p><strong>申请时间：</strong>{{ selectedApplication.appliedDate }}</p>
        <p><strong>当前状态：</strong>{{ getStatusText(selectedApplication.status) }}</p>
        <p><strong>薪资范围：</strong>{{ selectedApplication.salary }}</p>

        <div class="timeline">
          <h4>申请进度</h4>
          <el-timeline>
            <el-timeline-item timestamp="2025-09-20 10:00" placement="top">
              简历投递成功
            </el-timeline-item>
            <el-timeline-item timestamp="2025-09-21 14:30" placement="top" v-if="selectedApplication.status !== 'submitted'">
              HR已查看简历
            </el-timeline-item>
            <el-timeline-item timestamp="2025-09-22 09:15" placement="top" v-if="selectedApplication.status === 'interview'">
              收到面试邀请
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showApplicationDetail = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Clock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

// 响应式数据
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const activeTab = ref('applications')
const applicationFilter = ref('')
const showApplicationDetail = ref(false)
const selectedApplication = ref(null)
const calendarDate = ref(new Date())

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)
const currentUser = computed(() => userStore.user)

const stats = ref({
  totalApplications: 0,
  pendingApplications: 0,
  interviewInvitations: 0,
  offers: 0
})

const applications = ref([])

const upcomingInterviews = ref([
  {
    id: 1,
    jobTitle: 'Python后端开发工程师',
    companyName: '科技有限公司',
    interviewTime: '2025-09-22 14:00',
    type: '技术面试',
    date: '2025-09-22'
  }
])

const offers = ref([
  {
    id: 1,
    jobTitle: 'Java开发工程师',
    companyName: '大型互联网公司',
    salary: '20K-30K',
    startDate: '2025-10-15',
    deadline: '2025-09-25',
    status: 'pending'
  }
])

// 计算属性
const filteredApplications = computed(() => {
  if (!applicationFilter.value) return applications.value
  return applications.value.filter(app => app.status === applicationFilter.value)
})

// 辅助函数
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 获取申请数据
const fetchApplications = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const response = await request.get('/applications/')
    const applicationList = response.data.results || response.data || []

    applications.value = applicationList.map(app => ({
      id: app.id,
      jobTitle: app.job?.title || '未知职位',
      companyName: app.job?.company_name || '未知公司',
      appliedDate: formatDate(app.applied_at),
      status: app.status,
      salary: app.job?.salary_range || '面议',
      rawData: app
    }))

    // 计算统计数据
    updateStats(applicationList)

    console.log('申请数据:', applications.value)
    console.log('统计数据:', stats.value)
  } catch (error) {
    console.error('获取申请数据失败:', error)
    ElMessage.error('获取申请数据失败')
  } finally {
    loading.value = false
  }
}

// 更新统计数据
const updateStats = (applicationList) => {
  stats.value = {
    totalApplications: applicationList.length,
    pendingApplications: applicationList.filter(app =>
      app.status === 'pending' || app.status === 'reviewing'
    ).length,
    interviewInvitations: applicationList.filter(app =>
      app.status === 'interview'
    ).length,
    offers: applicationList.filter(app =>
      app.status === 'accepted'
    ).length
  }
}

// 方法
const getStatusType = (status) => {
  const statusMap = {
    'pending': '',
    'reviewing': 'info',
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

const getInterviewsForDate = (date) => {
  return upcomingInterviews.value.filter(interview => interview.date === date)
}

const handleTabChange = (tabName) => {
  console.log('切换到标签页:', tabName)
}

const filterApplications = () => {
  // 筛选逻辑已通过计算属性实现
}

const refreshApplications = async () => {
  await fetchApplications()
  ElMessage.success('刷新成功')
}

const viewApplication = (application) => {
  selectedApplication.value = application
  showApplicationDetail.value = true
}

const scheduleInterview = (application) => {
  ElMessage.info(`安排面试：${application.jobTitle}`)
}

const withdrawApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      `确定要撤回对"${application.jobTitle}"的申请吗？`,
      '确认撤回',
      {
        confirmButtonText: '确定撤回',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 调用API撤回申请
    await request.patch(`/applications/${application.id}/`, {
      status: 'withdrawn'
    })

    ElMessage.success('申请已撤回')
    // 刷新数据
    await fetchApplications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('撤回申请失败:', error)
      ElMessage.error('撤回申请失败')
    }
  }
}

const viewInterviewDetail = (interview) => {
  ElMessage.info(`查看面试详情：${interview.jobTitle}`)
}

const confirmInterview = (interview) => {
  ElMessage.success(`已确认参加面试：${interview.jobTitle}`)
}

const acceptOffer = (offer) => {
  ElMessage.success(`已接受Offer：${offer.jobTitle}`)
  offer.status = 'accepted'
}

const rejectOffer = (offer) => {
  ElMessage.warning(`已拒绝Offer：${offer.jobTitle}`)
}

const negotiateOffer = (offer) => {
  ElMessage.info(`协商Offer条件：${offer.jobTitle}`)
}

onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.applications {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.page-header p {
  margin: 0;
  color: #6c757d;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-item .el-card__body {
  padding: 20px;
  text-align: center;
}

.stat-content .stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-content .stat-label {
  color: #6c757d;
  font-size: 14px;
}

.tab-content {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.interview-calendar {
  margin-bottom: 24px;
}

.calendar-cell {
  position: relative;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.date-number {
  font-size: 14px;
}

.interview-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
}

.interview-list h3 {
  color: #2c3e50;
  margin-bottom: 16px;
}

.interview-card {
  margin-bottom: 16px;
}

.interview-card .el-card__body {
  padding: 16px;
}

.interview-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.interview-main h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.interview-main p {
  margin: 4px 0;
  color: #6c757d;
  font-size: 14px;
}

.interview-main .company {
  font-weight: 500;
  color: #495057;
}

.interview-time {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #409eff !important;
}

.interview-actions {
  display: flex;
  gap: 8px;
}

.offer-card {
  margin-bottom: 20px;
}

.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.offer-header h3 {
  margin: 0;
  color: #2c3e50;
}

.offer-details p {
  margin: 8px 0;
  color: #495057;
}

.offer-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

.no-data {
  text-align: center;
  color: #6c757d;
  padding: 40px;
  font-size: 16px;
}

.application-detail h3 {
  color: #2c3e50;
  margin-bottom: 16px;
}

.application-detail p {
  margin: 8px 0;
  color: #495057;
}

.timeline {
  margin-top: 24px;
}

.timeline h4 {
  color: #2c3e50;
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .table-header {
    flex-direction: column;
    gap: 12px;
  }

  .interview-info {
    flex-direction: column;
    gap: 12px;
  }

  .interview-actions {
    align-self: stretch;
  }

  .offer-actions {
    flex-direction: column;
  }
}
</style>
