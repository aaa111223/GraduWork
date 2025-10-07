<template>
  <div class="system-management">
    <div class="page-header">
      <h1>系统管理</h1>
      <p>管理平台用户、职位和系统设置</p>
    </div>

    <!-- 统计概览 -->
    <div class="stats-overview">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.totalUsers }}</div>
          <div class="stat-label">总用户数</div>
        </div>
        <el-icon class="stat-icon"><User /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.totalJobs }}</div>
          <div class="stat-label">总职位数</div>
        </div>
        <el-icon class="stat-icon"><Briefcase /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.totalApplications }}</div>
          <div class="stat-label">总申请数</div>
        </div>
        <el-icon class="stat-icon"><Document /></el-icon>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ stats.todayVisits }}</div>
          <div class="stat-label">今日访问</div>
        </div>
        <el-icon class="stat-icon"><View /></el-icon>
      </el-card>
    </div>

    <!-- 管理标签页 -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <div class="tab-content">
          <div class="table-header">
            <div class="header-left">
              <el-input
                v-model="userSearch"
                placeholder="搜索用户"
                style="width: 200px"
                clearable
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
            <div class="header-right">
              <el-button type="primary" @click="addUser">
                <el-icon><Plus /></el-icon>
                添加用户
              </el-button>
            </div>
          </div>

          <el-table :data="users" v-loading="loading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="phone" label="手机号" width="130" />
            <el-table-column prop="email" label="邮箱" width="200" />
            <el-table-column prop="role" label="角色" width="100">
              <template #default="scope">
                <el-tag :type="getRoleType(scope.row.role)">
                  {{ getRoleText(scope.row.role) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                  {{ scope.row.status === 'active' ? '正常' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="registerDate" label="注册时间" width="120" />
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button size="small" @click="editUser(scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    :type="scope.row.status === 'active' ? 'warning' : 'success'"
                    @click="toggleUserStatus(scope.row)"
                  >
                    {{ scope.row.status === 'active' ? '禁用' : '启用' }}
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteUser(scope.row)">
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 职位管理 -->
      <el-tab-pane label="职位管理" name="jobs">
        <div class="tab-content">
          <div class="table-header">
            <div class="header-left">
              <el-select v-model="jobStatusFilter" style="width: 150px" @change="filterJobs">
                <el-option label="全部状态" value="" />
                <el-option label="已发布" value="published" />
                <el-option label="草稿" value="draft" />
                <el-option label="已下线" value="offline" />
              </el-select>
            </div>
            <div class="header-right">
              <el-button type="primary" @click="addJob">
                <el-icon><Plus /></el-icon>
                发布职位
              </el-button>
            </div>
          </div>

          <el-table :data="jobs" v-loading="loading" style="width: 100%">
            <el-table-column prop="title" label="职位名称" width="200" />
            <el-table-column prop="companyName" label="公司名称" width="150" />
            <el-table-column prop="location" label="工作地点" width="100" />
            <el-table-column prop="salary" label="薪资" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getJobStatusType(scope.row.status)">
                  {{ getJobStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="publishDate" label="发布时间" width="120" />
            <el-table-column prop="applicants" label="申请人数" width="100" />
            <el-table-column label="操作" width="260" fixed="right">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button size="small" @click="editJob(scope.row)">编辑</el-button>
                  <el-button size="small" type="info" @click="changeJobStatus(scope.row)">
                    {{ scope.row.status === 'published' ? '下线' : '发布' }}
                  </el-button>
                  <el-button size="small" type="warning" @click="viewApplicants(scope.row)">
                    申请者
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteJob(scope.row)">
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 反馈管理 -->
      <el-tab-pane label="反馈管理" name="feedbacks">
        <div class="tab-content">
          <el-table :data="feedbacks" v-loading="loading" style="width: 100%">
            <el-table-column prop="title" label="反馈标题" width="200" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="scope">
                <el-tag size="small">{{ getFeedbackTypeText(scope.row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="userName" label="用户" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getFeedbackStatusType(scope.row.status)">
                  {{ getFeedbackStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="submitDate" label="提交时间" width="120" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button size="small" @click="viewFeedback(scope.row)">查看</el-button>
                  <el-button
                    size="small"
                    type="primary"
                    v-if="scope.row.status === 'pending'"
                    @click="replyFeedback(scope.row)"
                  >
                    回复
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteFeedback(scope.row)">
                    删除
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 系统设置 -->
      <el-tab-pane label="系统设置" name="settings">
        <div class="tab-content">
          <el-card>
            <template #header>
              <span>基本设置</span>
            </template>

            <el-form :model="systemSettings" label-width="120px">
              <el-form-item label="平台名称">
                <el-input v-model="systemSettings.platformName" />
              </el-form-item>

              <el-form-item label="联系邮箱">
                <el-input v-model="systemSettings.contactEmail" />
              </el-form-item>

              <el-form-item label="客服电话">
                <el-input v-model="systemSettings.servicePhone" />
              </el-form-item>

              <el-form-item label="用户注册">
                <el-switch v-model="systemSettings.allowRegister" />
              </el-form-item>

              <el-form-item label="邮件通知">
                <el-switch v-model="systemSettings.emailNotification" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="saveSettings">保存设置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  Briefcase,
  Document,
  View,
  Search,
  Plus
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

// 响应式数据
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const activeTab = ref('users')
const userSearch = ref('')
const jobStatusFilter = ref('')

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)
const isAdmin = computed(() => userStore.isAdmin)

const stats = ref({
  totalUsers: 0,
  totalJobs: 0,
  totalApplications: 0,
  todayVisits: 0
})

const users = ref([])
const jobs = ref([])
const feedbacks = ref([])

// 辅助函数
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 获取仪表板统计数据
const fetchDashboardStats = async () => {
  if (!isAdmin.value) {
    router.push('/login')
    return
  }

  try {
    const response = await request.get('/admin/dashboard/stats/')
    const data = response.data

    stats.value = {
      totalUsers: data.user_stats.total,
      totalJobs: data.job_stats.total,
      totalApplications: data.application_stats.total,
      todayVisits: data.user_stats.today_new + data.application_stats.today_new
    }

    console.log('仪表板统计:', stats.value)
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 获取用户列表
const fetchUsers = async () => {
  if (!isAdmin.value) return

  loading.value = true
  try {
    const params = {}
    if (userSearch.value) {
      params.search = userSearch.value
    }

    const response = await request.get('/admin/users/', { params })
    users.value = response.data.results.map(user => ({
      id: user.id,
      name: user.real_name || user.phone,
      phone: user.phone,
      email: user.email || '-',
      role: user.user_type,
      status: user.is_active ? 'active' : 'disabled',
      registerDate: formatDate(user.created_at),
      rawData: user
    }))

    console.log('用户列表:', users.value)
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 获取职位列表
const fetchJobs = async () => {
  if (!isAdmin.value) return

  loading.value = true
  try {
    const params = {}
    if (jobStatusFilter.value) {
      params.status = jobStatusFilter.value
    }

    const response = await request.get('/admin/jobs/', { params })
    jobs.value = response.data.results.map(job => ({
      id: job.id,
      title: job.title,
      companyName: job.company_name,
      location: job.work_city,
      salary: job.salary_range,
      status: job.status,
      publishDate: formatDate(job.created_at),
      applicants: job.application_count || 0,
      rawData: job
    }))

    console.log('职位列表:', jobs.value)
  } catch (error) {
    console.error('获取职位列表失败:', error)
    ElMessage.error('获取职位列表失败')
  } finally {
    loading.value = false
  }
}

// 获取反馈列表
const fetchFeedbacks = async () => {
  if (!isAdmin.value) return

  loading.value = true
  try {
    const response = await request.get('/admin/feedbacks/')
    feedbacks.value = response.data.results.map(feedback => ({
      id: feedback.id,
      title: feedback.title,
      type: feedback.category_name || '未分类',
      userName: feedback.user.real_name || feedback.user.phone,
      status: feedback.status,
      submitDate: formatDate(feedback.created_at),
      rawData: feedback
    }))

    console.log('反馈列表:', feedbacks.value)
  } catch (error) {
    console.error('获取反馈列表失败:', error)
    ElMessage.error('获取反馈列表失败')
  } finally {
    loading.value = false
  }
}

const systemSettings = ref({
  platformName: '学生就业管理平台',
  contactEmail: 'admin@example.com',
  servicePhone: '400-123-4567',
  allowRegister: true,
  emailNotification: true
})

// 方法
const handleTabChange = async (tabName) => {
  console.log('切换到标签页:', tabName)

  // 根据标签页加载对应数据
  switch (tabName) {
    case 'users':
      await fetchUsers()
      break
    case 'jobs':
      await fetchJobs()
      break
    case 'feedbacks':
      await fetchFeedbacks()
      break
  }
}

const getRoleType = (role) => {
  const roleMap = {
    'admin': 'danger',
    'student': 'success',
    'enterprise': 'warning'
  }
  return roleMap[role] || ''
}

const getRoleText = (role) => {
  const roleMap = {
    'admin': '管理员',
    'student': '学生',
    'enterprise': '企业'
  }
  return roleMap[role] || role
}

const getJobStatusType = (status) => {
  const statusMap = {
    'published': 'success',
    'draft': 'info',
    'closed': 'danger'
  }
  return statusMap[status] || ''
}

const getJobStatusText = (status) => {
  const statusMap = {
    'published': '已发布',
    'draft': '草稿',
    'closed': '已关闭'
  }
  return statusMap[status] || status
}

const getFeedbackTypeText = (type) => {
  const typeMap = {
    'suggestion': '功能建议',
    'bug': '问题反馈',
    'question': '使用咨询',
    'other': '其他'
  }
  return typeMap[type] || type
}

const getFeedbackStatusType = (status) => {
  const statusMap = {
    'pending': 'warning',
    'processing': 'info',
    'replied': 'success',
    'closed': ''
  }
  return statusMap[status] || ''
}

const getFeedbackStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'resolved': '已解决',
    'closed': '已关闭'
  }
  return statusMap[status] || status
}

const getFeedbackStatusColor = (status) => {
  const colorMap = {
    'pending': '#E6A23C',
    'processing': '#409EFF',
    'resolved': '#67C23A',
    'closed': '#909399'
  }
  return colorMap[status] || '#909399'
}

// 获取申请状态颜色
const getStatusColor = (status) => {
  const colorMap = {
    'pending': '#909399',
    'reviewing': '#E6A23C',
    'interview': '#409EFF',
    'accepted': '#67C23A',
    'rejected': '#F56C6C',
    'withdrawn': '#909399'
  }
  return colorMap[status] || '#909399'
}

const addUser = () => {
  ElMessage.info('添加用户功能开发中')
}

const editUser = async (user) => {
  try {
    const { value: formData } = await ElMessageBox.prompt(
      `<div style="text-align: left;">
        <div style="margin-bottom: 12px;">
          <label style="display: block; margin-bottom: 4px; font-weight: bold;">真实姓名:</label>
          <input id="edit-real-name" type="text" value="${user.rawData?.real_name || ''}"
                 style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" />
        </div>
        <div style="margin-bottom: 12px;">
          <label style="display: block; margin-bottom: 4px; font-weight: bold;">邮箱:</label>
          <input id="edit-email" type="email" value="${user.rawData?.email || ''}"
                 style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" />
        </div>
        <div style="margin-bottom: 12px;">
          <label style="display: block; margin-bottom: 4px; font-weight: bold;">用户状态:</label>
          <select id="edit-status" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <option value="true" ${user.rawData?.is_active ? 'selected' : ''}>正常</option>
            <option value="false" ${!user.rawData?.is_active ? 'selected' : ''}>禁用</option>
          </select>
        </div>
      </div>`,
      `编辑用户 - ${user.name}`,
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '保存',
        cancelButtonText: '取消',
        inputType: 'text',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            const realName = document.getElementById('edit-real-name')?.value || ''
            const email = document.getElementById('edit-email')?.value || ''
            const isActive = document.getElementById('edit-status')?.value === 'true'

            instance.inputValue = JSON.stringify({
              real_name: realName,
              email: email,
              is_active: isActive
            })
          }
          done()
        }
      }
    )

    if (formData) {
      const updateData = JSON.parse(formData)
      await request.patch(`/admin/users/${user.id}/`, updateData)
      ElMessage.success('用户信息更新成功')
      // 刷新用户列表
      await fetchUsers()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('编辑用户失败:', error)
      ElMessage.error('编辑用户失败')
    }
  }
}

const toggleUserStatus = async (user) => {
  try {
    const action = user.status === 'active' ? '禁用' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}用户 ${user.name} 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await request.post(`/admin/users/${user.id}/toggle_status/`)
    user.status = user.status === 'active' ? 'disabled' : 'active'
    ElMessage.success(`${action}用户成功`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('切换用户状态失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

const deleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 ${user.name} 吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await request.delete(`/admin/users/${user.id}/`)
    ElMessage.success('用户删除成功')
    // 刷新用户列表
    await fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除用户失败')
    }
  }
}

const filterJobs = async () => {
  await fetchJobs()
}

const addJob = () => {
  ElMessage.info('发布职位功能开发中')
}

const editJob = (job) => {
  ElMessage.info(`编辑职位：${job.title}`)
}

const changeJobStatus = async (job) => {
  try {
    const newStatus = job.status === 'published' ? 'closed' : 'published'
    const action = newStatus === 'published' ? '发布' : '下线'

    await ElMessageBox.confirm(
      `确定要${action}职位"${job.title}"吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await request.post(`/admin/jobs/${job.id}/change_status/`, {
      status: newStatus
    })

    job.status = newStatus
    ElMessage.success(`职位${action}成功`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('更改职位状态失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

const viewApplicants = async (job) => {
  try {
    const response = await request.get(`/admin/jobs/${job.id}/applications/`)
    const applications = response.data.results || []

    if (applications.length === 0) {
      ElMessage.info(`职位"${job.title}"暂无申请者`)
      return
    }

    // 构建申请者列表HTML
    const applicantsHtml = applications.map((app, index) => `
      <div style="padding: 12px; border-bottom: 1px solid #eee; ${index === applications.length - 1 ? 'border-bottom: none;' : ''}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <strong style="color: #409EFF;">${app.user_name}</strong>
          <span style="color: ${getStatusColor(app.status)}; font-size: 12px; padding: 2px 8px; background: ${getStatusColor(app.status)}20; border-radius: 12px;">
            ${app.status_display}
          </span>
        </div>
        <div style="font-size: 14px; color: #666; margin-bottom: 4px;">
          <span>📱 ${app.user_phone}</span>
          <span style="margin-left: 16px;">📅 ${formatDate(app.applied_at)}</span>
        </div>
        ${app.cover_letter ? `<div style="font-size: 13px; color: #888; background: #f5f5f5; padding: 8px; border-radius: 4px; margin-top: 8px;">💬 ${app.cover_letter}</div>` : ''}
      </div>
    `).join('')

    ElMessageBox.alert(
      `<div style="max-height: 400px; overflow-y: auto;">
        <h4 style="margin-bottom: 16px; color: #409EFF;">职位申请者 - ${job.title}</h4>
        <div style="margin-bottom: 12px; color: #666;">共 ${applications.length} 位申请者</div>
        ${applicantsHtml}
      </div>`,
      '申请者列表',
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '确定',
        customClass: 'applicants-dialog'
      }
    )
  } catch (error) {
    console.error('获取申请者失败:', error)
    ElMessage.error('获取申请者失败')
  }
}

const deleteJob = async (job) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除职位"${job.title}"吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await request.delete(`/admin/jobs/${job.id}/`)
    ElMessage.success('职位删除成功')
    // 刷新职位列表
    await fetchJobs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除职位失败:', error)
      ElMessage.error('删除职位失败')
    }
  }
}

const viewFeedback = (feedback) => {
  const statusColor = getFeedbackStatusColor(feedback.status)
  const typeText = getFeedbackTypeText(feedback.type)

  ElMessageBox.alert(
    `<div style="text-align: left; max-height: 500px; overflow-y: auto;">
      <h4 style="margin-bottom: 16px; color: #409EFF;">${feedback.title}</h4>

      <div style="margin-bottom: 16px;">
        <div style="margin-bottom: 8px;">
          <strong>反馈类型:</strong>
          <span style="color: #409EFF; background: #409EFF20; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
            ${typeText}
          </span>
        </div>
        <div style="margin-bottom: 8px;">
          <strong>反馈状态:</strong>
          <span style="color: ${statusColor}; background: ${statusColor}20; padding: 2px 8px; border-radius: 12px; font-size: 12px;">
            ${getFeedbackStatusText(feedback.status)}
          </span>
        </div>
        <div style="margin-bottom: 8px;"><strong>提交用户:</strong> ${feedback.userName}</div>
        <div style="margin-bottom: 8px;"><strong>提交时间:</strong> ${feedback.submitDate}</div>
      </div>

      <div style="margin-bottom: 16px;">
        <h5 style="color: #666; margin-bottom: 8px;">反馈内容</h5>
        <div style="background: #f8f9fa; padding: 12px; border-radius: 4px; line-height: 1.5;">
          ${feedback.rawData?.content || '无详细内容'}
        </div>
      </div>

      ${feedback.rawData?.admin_reply ? `
        <div>
          <h5 style="color: #666; margin-bottom: 8px;">管理员回复</h5>
          <div style="background: #e8f5e8; padding: 12px; border-radius: 4px; line-height: 1.5; border-left: 4px solid #67C23A;">
            ${feedback.rawData.admin_reply}
          </div>
        </div>
      ` : ''}
    </div>`,
    '反馈详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定',
      customClass: 'feedback-detail-dialog'
    }
  )
}

const replyFeedback = async (feedback) => {
  try {
    const { value: reply } = await ElMessageBox.prompt(
      '请输入回复内容',
      `回复反馈：${feedback.title}`,
      {
        confirmButtonText: '发送回复',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '请输入回复内容...'
      }
    )

    if (!reply || !reply.trim()) {
      ElMessage.warning('回复内容不能为空')
      return
    }

    await request.post(`/admin/feedbacks/${feedback.id}/reply/`, {
      reply: reply.trim()
    })

    ElMessage.success('回复成功')
    // 刷新反馈列表
    await fetchFeedbacks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('回复反馈失败:', error)
      ElMessage.error('回复失败')
    }
  }
}

const deleteFeedback = async (feedback) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除反馈"${feedback.title}"吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await request.delete(`/admin/feedbacks/${feedback.id}/`)
    ElMessage.success('反馈删除成功')
    // 刷新反馈列表
    await fetchFeedbacks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除反馈失败:', error)
      ElMessage.error('删除反馈失败')
    }
  }
}

const saveSettings = async () => {
  try {
    await request.post('/admin/system/settings/', systemSettings.value)
    ElMessage.success('系统设置保存成功')
  } catch (error) {
    console.error('保存系统设置失败:', error)
    ElMessage.error('保存系统设置失败')
  }
}

// 获取系统设置
const fetchSystemSettings = async () => {
  try {
    const response = await request.get('/admin/system/settings/')
    systemSettings.value = response.data
  } catch (error) {
    console.error('获取系统设置失败:', error)
  }
}

onMounted(async () => {
  // 检查管理员权限
  if (!isAdmin.value) {
    ElMessage.error('您没有访问权限')
    router.push('/login')
    return
  }

  // 加载初始数据
  await Promise.all([
    fetchDashboardStats(),
    fetchUsers(),  // 默认显示用户管理标签页
    fetchSystemSettings()  // 加载系统设置
  ])
})
</script>

<style scoped>
.system-management {
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

.stat-card {
  position: relative;
}

.stat-card .el-card__body {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.stat-icon {
  font-size: 2rem;
  color: #409eff;
  opacity: 0.3;
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

/* 操作按钮样式 */
.action-buttons {
  display: flex !important;
  gap: 6px;
  align-items: center;
  flex-wrap: nowrap !important;
  justify-content: flex-start;
  white-space: nowrap;
}

.action-buttons .el-button {
  margin: 0 !important;
  min-width: 50px;
  font-size: 11px;
  padding: 4px 8px;
  flex-shrink: 1;
  white-space: nowrap;
}

.action-buttons .el-button + .el-button {
  margin-left: 0 !important;
}

/* 确保表格单元格内容水平排列 */
.el-table :deep(.el-table__cell) {
  padding: 8px 12px;
}

.el-table :deep(.el-table__cell .cell) {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

/* 强制操作列按钮水平排列 */
.el-table :deep(.el-table__cell .cell .action-buttons) {
  display: flex !important;
  flex-direction: row !important;
  gap: 6px;
  align-items: center;
  flex-wrap: nowrap !important;
  width: 100%;
  overflow: hidden;
}

.el-table :deep(.el-table__cell .cell .action-buttons .el-button) {
  margin: 0 !important;
  flex-shrink: 1;
  min-width: 50px;
  font-size: 11px;
  padding: 4px 8px;
  white-space: nowrap;
}

/* 表格样式优化 */
.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table :deep(.el-table__header) {
  background-color: #fafafa;
}

.el-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 操作列固定样式 */
.el-table :deep(.el-table__fixed-right) {
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .table-header {
    flex-direction: column;
    gap: 12px;
  }

  /* 移动端操作按钮优化 */
  .action-buttons {
    flex-direction: column;
    gap: 4px;
    align-items: stretch;
  }

  .action-buttons .el-button {
    width: 100%;
    min-width: auto;
  }
}
</style>
