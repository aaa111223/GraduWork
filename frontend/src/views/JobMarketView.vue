<template>
  <div class="job-market">
    <!-- 页面标题和搜索 -->
    <div class="page-header">
      <div class="header-content">
        <h1>就业市场</h1>
        <p>发现适合您的职业机会</p>

        <!-- 登录状态提示 -->
        <div v-if="!isLoggedIn" class="login-tip">
          <el-alert
            title="提示"
            description="登录后可以申请职位和收藏心仪的工作机会"
            type="info"
            show-icon
            :closable="false"
          >
            <template #default>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span>登录后可以申请职位和收藏心仪的工作机会</span>
                <el-button size="small" type="primary" @click="router.push('/login')">
                  立即登录
                </el-button>
              </div>
            </template>
          </el-alert>
        </div>

        <div v-else-if="!isStudent" class="user-tip">
          <el-alert
            title="提示"
            :description="getUserTypeMessage()"
            type="warning"
            show-icon
            :closable="false"
          />
        </div>


      </div>

      <!-- 搜索栏 -->
      <div class="search-section">
        <el-form :model="searchForm" inline>
          <el-form-item>
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索职位、公司"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-select v-model="searchForm.location" placeholder="工作地点" style="width: 150px" clearable>
              <el-option label="北京市" value="北京市" />
              <el-option label="上海市" value="上海市" />
              <el-option label="深圳市" value="深圳市" />
              <el-option label="广州市" value="广州市" />
              <el-option label="杭州市" value="杭州市" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-select v-model="searchForm.salary" placeholder="薪资范围" style="width: 150px" clearable>
              <el-option label="5K-10K" value="5K-10K" />
              <el-option label="10K-15K" value="10K-15K" />
              <el-option label="15K-25K" value="15K-25K" />
              <el-option label="25K以上" value="25K+" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="searchJobs">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- 筛选和排序 -->
    <div class="filter-section">
      <div class="filter-left">
        <el-radio-group v-model="filterForm.jobType" @change="handleFilterChange">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="full_time">全职</el-radio-button>
          <el-radio-button label="part_time">兼职</el-radio-button>
          <el-radio-button label="internship">实习</el-radio-button>
        </el-radio-group>
      </div>

      <div class="filter-right">
        <el-select v-model="filterForm.sortBy" @change="handleSortChange" style="width: 150px">
          <el-option label="最新发布" value="-created_at" />
          <el-option label="薪资最高" value="-salary_max" />
          <el-option label="薪资最低" value="salary_min" />
        </el-select>
      </div>
    </div>

    <!-- 职位列表 -->
    <div class="jobs-section">
      <div v-if="loading" class="loading-section">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>加载中...</span>
      </div>

      <div v-else-if="jobs.length === 0" class="empty-section">
        <el-empty description="暂无职位信息" />
      </div>

      <div v-else class="jobs-list">
        <el-row :gutter="20">
          <el-col :span="24" v-for="job in jobs" :key="job.id">
          <el-card class="job-card" @click="viewJobDetail(job)">
            <div class="job-content">
              <div class="job-main">
                <div class="job-header">
                  <h3 class="job-title">{{ job.title }}</h3>
                  <div class="job-salary">{{ job.salary_range }}</div>
                </div>

                <div class="job-info">
                  <span class="company-name">{{ job.company_name }}</span>
                  <span class="job-location">{{ job.location }}</span>
                  <span class="job-experience">{{ job.experience_required }}</span>
                </div>

                <div class="job-description">
                  {{ job.description }}
                </div>

                <div class="job-tags">
                  <el-tag v-for="tag in job.requirements?.split(', ') || []" :key="tag" size="small">
                    {{ tag }}
                  </el-tag>
                </div>
              </div>

              <div class="job-actions">
                <el-button
                  v-if="canApplyJob"
                  type="primary"
                  @click.stop="applyJob(job)"
                  :disabled="job.hasApplied"
                >
                  {{ job.hasApplied ? '已申请' : '立即申请' }}
                </el-button>
                <el-button
                  v-else
                  type="primary"
                  disabled
                  @click.stop="showApplyRestriction"
                >
                  {{ getApplyButtonText() }}
                </el-button>
                <el-button
                  @click.stop="toggleFavorite(job)"
                  :icon="job.isFavorite ? StarFilled : Star"
                  :type="job.isFavorite ? 'warning' : 'default'"
                >
                  {{ job.isFavorite ? '已收藏' : '收藏' }}
                </el-button>
              </div>
            </div>

            <div class="job-footer">
              <span class="publish-time">发布时间：{{ formatDate(job.created_at) }}</span>
            </div>
          </el-card>
        </el-col>
        </el-row>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 职位详情对话框 -->
    <el-dialog v-model="showJobDetail" :title="selectedJob?.title" width="800px">
      <div v-if="selectedJob" class="job-detail">
        <div class="detail-header">
          <h2>{{ selectedJob.title }}</h2>
          <div class="detail-salary">{{ selectedJob.salary_range }}</div>
        </div>

        <div class="detail-info">
          <p><strong>公司：</strong>{{ selectedJob.company_name }}</p>
          <p><strong>地点：</strong>{{ selectedJob.location }}</p>
          <p><strong>经验要求：</strong>{{ selectedJob.experience_required }}</p>
          <p><strong>学历要求：</strong>{{ selectedJob.education_required }}</p>
        </div>

        <div class="detail-description">
          <h3>职位描述</h3>
          <p>{{ selectedJob.description }}</p>
        </div>

        <div class="detail-requirements">
          <h3>任职要求</h3>
          <p>{{ selectedJob.requirements }}</p>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showJobDetail = false">关闭</el-button>
          <el-button
            v-if="canApplyJob"
            type="primary"
            @click="applyJob(selectedJob)"
            :disabled="selectedJob?.hasApplied"
          >
            {{ selectedJob?.hasApplied ? '已申请' : '立即申请' }}
          </el-button>
          <el-button
            v-else
            type="primary"
            disabled
            @click="showApplyRestriction"
          >
            {{ getApplyButtonText() }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Star, StarFilled, Loading } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

// 响应式数据
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const showJobDetail = ref(false)
const selectedJob = ref(null)

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)
const isStudent = computed(() => userStore.isStudent)
const isAdmin = computed(() => userStore.isAdmin)
const isEnterprise = computed(() => userStore.isEnterprise)

// 检查用户是否可以申请职位
const canApplyJob = computed(() => {
  return isLoggedIn.value && isStudent.value
})

const searchForm = ref({
  keyword: '',
  location: '',
  salary: ''
})

const filterForm = ref({
  jobType: '',
  sortBy: '-created_at'
})

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const jobs = ref([])

// 方法
const searchJobs = async () => {
  loading.value = true

  try {
    const params = {
      page: pagination.value.currentPage,
      page_size: pagination.value.pageSize,
      ordering: filterForm.value.sortBy
    }

    // 添加搜索参数
    if (searchForm.value.keyword) {
      params.search = searchForm.value.keyword
    }
    if (searchForm.value.location) {
      params.work_city = searchForm.value.location
    }
    if (searchForm.value.salary) {
      // 解析薪资范围
      const salaryRange = searchForm.value.salary
      if (salaryRange === '5K-10K') {
        params.salary_min = 5000
        params.salary_max = 10000
      } else if (salaryRange === '10K-15K') {
        params.salary_min = 10000
        params.salary_max = 15000
      } else if (salaryRange === '15K-25K') {
        params.salary_min = 15000
        params.salary_max = 25000
      } else if (salaryRange === '25K+') {
        params.salary_min = 25000
      }
    }

    // 添加职位类型过滤
    if (filterForm.value.jobType) {
      params.job_type = filterForm.value.jobType
    }

    const response = await request.get('/jobs/', { params })

    // 处理返回的数据
    const jobList = response.data.results || []

    // 如果用户已登录，获取收藏状态
    if (isLoggedIn.value) {
      await loadFavoriteStatus(jobList)
    }

    jobs.value = jobList.map(job => ({
      ...job,
      location: job.work_city || job.location,
      requirements: Array.isArray(job.skills_required) ? job.skills_required.join(', ') : job.skills_required,
      isFavorite: job.is_favorited || false,
      hasApplied: false // 这里可以后续添加已申请状态的检查
    }))

    pagination.value.total = response.data.count || 0

  } catch (error) {
    console.error('获取职位列表失败:', error)
    // 使用模拟数据作为后备
    await loadMockData()
  } finally {
    loading.value = false
  }
}

// 加载收藏状态
const loadFavoriteStatus = async (jobList) => {
  try {
    const favoriteResponse = await request.get('/jobs/favorites/')
    const favoriteJobIds = favoriteResponse.data.results.map(fav => fav.job.id)
    jobList.forEach(job => {
      job.is_favorited = favoriteJobIds.includes(job.id)
    })
  } catch (error) {
    console.error('获取收藏状态失败:', error)
  }
}

// 加载模拟数据
const loadMockData = async () => {
  jobs.value = [
    {
      id: 1,
      title: 'Python后端开发工程师',
      company_name: '科技有限公司',
      location: '北京市',
      salary_range: '15K-25K',
      experience_required: '3-5年',
      education_required: '本科',
      description: '负责后端系统开发和维护，参与系统架构设计',
      requirements: 'Python, Django, MySQL, Redis',
      created_at: '2025-09-20T10:00:00Z',
      isFavorite: false,
      hasApplied: false
    },
    {
      id: 2,
      title: 'Vue.js前端开发工程师',
      company_name: '互联网科技公司',
      location: '上海市',
      salary_range: '12K-20K',
      experience_required: '2-4年',
      education_required: '本科',
      description: '负责前端页面开发和用户体验优化',
      requirements: 'Vue.js, JavaScript, CSS, Element Plus',
      created_at: '2025-09-19T14:30:00Z',
      isFavorite: false,
      hasApplied: false
    },
    {
      id: 3,
      title: '产品经理',
      company_name: '创新科技公司',
      location: '深圳市',
      salary_range: '18K-30K',
      experience_required: '3-6年',
      education_required: '本科',
      description: '负责产品规划和需求分析，协调各部门合作',
      requirements: '产品设计, 用户研究, 项目管理',
      created_at: '2025-09-18T09:15:00Z',
      isFavorite: false,
      hasApplied: false
    }
  ]
  pagination.value.total = jobs.value.length
}

const handleFilterChange = () => {
  pagination.value.currentPage = 1
  searchJobs()
}

const handleSortChange = () => {
  pagination.value.currentPage = 1
  searchJobs()
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.currentPage = 1
  searchJobs()
}

const handleCurrentChange = (page) => {
  pagination.value.currentPage = page
  searchJobs()
}

const viewJobDetail = (job) => {
  selectedJob.value = job
  showJobDetail.value = true
}

// 获取用户类型提示信息
const getUserTypeMessage = () => {
  if (isAdmin.value) {
    return '管理员账户无法申请职位，如需申请请使用学生账户'
  } else if (isEnterprise.value) {
    return '企业用户无法申请职位，如需申请请使用学生账户'
  }
  return '当前用户类型无法申请职位，请使用学生账户'
}

// 获取申请按钮文本
const getApplyButtonText = () => {
  if (!isLoggedIn.value) {
    return '请先登录'
  } else if (isAdmin.value) {
    return '管理员无法申请'
  } else if (isEnterprise.value) {
    return '企业用户无法申请'
  }
  return '无法申请'
}

// 显示申请限制提示
const showApplyRestriction = () => {
  if (!isLoggedIn.value) {
    ElMessageBox.confirm(
      '申请职位需要登录，是否前往登录页面？',
      '需要登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      router.push('/login')
    }).catch(() => {})
  } else if (isAdmin.value) {
    ElMessage.warning('管理员账户无法申请职位，管理员主要负责系统管理和用户服务')
  } else if (isEnterprise.value) {
    ElMessage.warning('企业用户无法申请职位，企业用户主要负责发布职位和管理招聘')
  } else {
    ElMessage.warning('当前用户类型无法申请职位，请使用学生账户')
  }
}

const applyJob = async (job) => {
  // 检查登录状态
  if (!isLoggedIn.value) {
    showApplyRestriction()
    return
  }

  // 检查用户类型
  if (!canApplyJob.value) {
    showApplyRestriction()
    return
  }

  try {
    loading.value = true
    // 调用申请API
    await request.post(`/applications/`, {
      job_id: job.id,
      cover_letter: '我对这个职位很感兴趣，希望能有机会加入贵公司。'
    })

    ElMessage.success(`已成功申请职位：${job.title}`)

    // 更新职位的申请状态
    job.hasApplied = true

  } catch (error) {
    console.error('申请职位失败:', error)
    if (error.response?.status === 400) {
      ElMessage.warning('您已经申请过这个职位了')
    } else {
      ElMessage.error('申请失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const toggleFavorite = async (job) => {
  // 检查登录状态
  if (!isLoggedIn.value) {
    const result = await ElMessageBox.confirm(
      '收藏职位需要登录，是否前往登录页面？',
      '需要登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).catch(() => false)

    if (result) {
      router.push('/login')
    }
    return
  }

  try {
    if (job.isFavorite) {
      // 取消收藏 - 找到收藏记录并删除
      const favoritesResponse = await request.get('/jobs/favorites/')
      const favoriteRecord = favoritesResponse.data.results.find(fav => fav.job.id === job.id)
      if (favoriteRecord) {
        await request.delete(`/jobs/favorites/${favoriteRecord.id}/`)
        job.isFavorite = false
        ElMessage.success('已取消收藏')
      }
    } else {
      // 添加收藏
      await request.post('/jobs/favorites/', { job: job.id })
      job.isFavorite = true
      ElMessage.success('已收藏')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    const errorMsg = error.response?.data?.detail || error.response?.data?.error || '操作失败，请稍后重试'
    ElMessage.error(errorMsg)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}



onMounted(() => {
  searchJobs()
})
</script>

<style scoped>
.job-market {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.header-content h1 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.header-content p {
  margin: 0 0 20px 0;
  color: #6c757d;
}

.login-tip,
.user-tip {
  margin-bottom: 20px;
}

.login-tip .el-alert__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.search-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.job-card {
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.job-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.job-main {
  flex: 1;
  margin-right: 20px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.job-title {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.job-salary {
  color: #e74c3c;
  font-weight: 600;
  font-size: 16px;
}

.job-info {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  color: #6c757d;
  font-size: 14px;
}

.company-name {
  font-weight: 500;
  color: #495057;
}

.job-description {
  color: #6c757d;
  margin-bottom: 12px;
  line-height: 1.5;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.job-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 120px;
}

.job-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e9ecef;
  color: #6c757d;
  font-size: 12px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.job-detail .detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.job-detail .detail-header h2 {
  margin: 0;
  color: #2c3e50;
}

.job-detail .detail-salary {
  color: #e74c3c;
  font-weight: 600;
  font-size: 18px;
}

.job-detail .detail-info {
  margin-bottom: 24px;
}

.job-detail .detail-info p {
  margin: 8px 0;
  color: #495057;
}

.job-detail .detail-description,
.job-detail .detail-requirements {
  margin-bottom: 24px;
}

.job-detail h3 {
  color: #2c3e50;
  margin-bottom: 12px;
}

.job-detail p {
  line-height: 1.6;
  color: #6c757d;
}

@media (max-width: 768px) {
  .search-section .el-form {
    flex-direction: column;
  }

  .search-section .el-form-item {
    margin-right: 0;
    margin-bottom: 12px;
  }

  .filter-section {
    flex-direction: column;
    gap: 12px;
  }

  .job-content {
    flex-direction: column;
  }

  .job-main {
    margin-right: 0;
    margin-bottom: 16px;
  }

  .job-actions {
    flex-direction: row;
  }
}
</style>
