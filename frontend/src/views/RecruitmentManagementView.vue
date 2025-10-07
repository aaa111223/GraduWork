<template>
  <div class="recruitment-management">
    <div class="page-header">
      <h1>招聘管理</h1>
      <p>管理您的职位发布和招聘流程</p>
    </div>

    <el-tabs v-model="activeTab" class="management-tabs">
      <!-- 职位管理 -->
      <el-tab-pane label="职位管理" name="jobs">
        <div class="tab-content">
          <div class="content-header">
            <div class="header-left">
              <h3>我的职位</h3>
              <span class="count">共 {{ jobs.length }} 个职位</span>
            </div>
            <div class="header-right">
              <el-button type="primary" @click="showJobDialog = true">
                <el-icon><Plus /></el-icon>
                发布职位
              </el-button>
            </div>
          </div>

          <div class="filter-bar">
            <el-input
              v-model="jobSearch"
              placeholder="搜索职位标题"
              style="width: 200px"
              clearable
            />
            <el-select v-model="jobStatusFilter" placeholder="职位状态" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
              <el-option label="已暂停" value="paused" />
              <el-option label="已关闭" value="closed" />
            </el-select>
            <el-button @click="fetchJobs">搜索</el-button>
          </div>

          <el-table :data="filteredJobs" v-loading="jobsLoading">
            <el-table-column prop="title" label="职位标题" min-width="200" />
            <el-table-column prop="job_type" label="工作类型" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ getJobTypeText(row.job_type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="salary_range" label="薪资范围" width="150" />
            <el-table-column prop="work_city" label="工作地点" width="120" />
            <el-table-column prop="application_count" label="申请数" width="80" />
            <el-table-column prop="view_count" label="浏览数" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="发布时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="240" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="editJob(row)">编辑</el-button>
                  <el-button size="small" type="info" @click="viewApplications(row)">
                    简历({{ row.application_count }})
                  </el-button>
                  <el-dropdown @command="(command) => handleJobAction(command, row)">
                    <el-button size="small">
                      更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="pause" v-if="row.status === 'published'">
                          暂停招聘
                        </el-dropdown-item>
                        <el-dropdown-item command="resume" v-if="row.status === 'paused'">
                          恢复招聘
                        </el-dropdown-item>
                        <el-dropdown-item command="close">关闭职位</el-dropdown-item>
                        <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 简历管理 -->
      <el-tab-pane label="简历管理" name="resumes">
        <div class="tab-content">
          <div class="content-header">
            <div class="header-left">
              <h3>收到的简历</h3>
              <span class="count">共 {{ applications.length }} 份简历</span>
            </div>
          </div>

          <div class="filter-bar">
            <el-select v-model="applicationStatusFilter" placeholder="申请状态" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="待审核" value="pending" />
              <el-option label="审核中" value="reviewing" />
              <el-option label="面试中" value="interview" />
              <el-option label="已录用" value="accepted" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
            <el-select v-model="selectedJobFilter" placeholder="筛选职位" style="width: 200px">
              <el-option label="全部职位" value="" />
              <el-option
                v-for="job in jobs"
                :key="job.id"
                :label="job.title"
                :value="job.id"
              />
            </el-select>
            <el-button @click="fetchApplications">筛选</el-button>
          </div>

          <el-table :data="filteredApplications" v-loading="applicationsLoading">
            <el-table-column prop="applicant_name" label="姓名" width="100" />
            <el-table-column prop="job_title" label="申请职位" min-width="200" />
            <el-table-column prop="phone" label="联系电话" width="120" />
            <el-table-column prop="education" label="学历" width="100" />
            <el-table-column prop="experience" label="工作经验" width="100" />
            <el-table-column prop="expected_salary" label="期望薪资" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getApplicationStatusType(row.status)" size="small">
                  {{ getApplicationStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="applied_at" label="申请时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.applied_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="{ row }">
                <div class="action-buttons">
                  <el-button size="small" @click="viewResume(row)">查看简历</el-button>
                  <el-dropdown @command="(command) => handleApplicationAction(command, row)">
                    <el-button size="small">
                      操作<el-icon class="el-icon--right"><arrow-down /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="approve" v-if="row.status === 'pending'">
                          通过初筛
                        </el-dropdown-item>
                        <el-dropdown-item command="interview" v-if="row.status === 'reviewing'">
                          安排面试
                        </el-dropdown-item>
                        <el-dropdown-item command="accept" v-if="row.status === 'interview'">
                          录用
                        </el-dropdown-item>
                        <el-dropdown-item command="reject" divided>拒绝</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 面试管理 -->
      <el-tab-pane label="面试管理" name="interviews">
        <div class="tab-content">
          <div class="content-header">
            <div class="header-left">
              <h3>面试安排</h3>
              <span class="count">共 {{ interviews.length }} 场面试</span>
            </div>
            <div class="header-right">
              <el-button type="primary" @click="showInterviewDialog = true">
                <el-icon><Plus /></el-icon>
                安排面试
              </el-button>
            </div>
          </div>

          <el-table :data="interviews" v-loading="interviewsLoading">
            <el-table-column prop="candidate_name" label="候选人" width="100" />
            <el-table-column prop="job_title" label="申请职位" min-width="200" />
            <el-table-column prop="interview_type" label="面试类型" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ getInterviewTypeText(row.interview_type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="scheduled_time" label="面试时间" width="150">
              <template #default="{ row }">
                {{ formatDateTime(row.scheduled_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="duration" label="时长(分钟)" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getInterviewStatusType(row.status)" size="small">
                  {{ getInterviewStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="评分" width="80" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editInterview(row)">编辑</el-button>
                <el-button size="small" type="info" @click="viewInterviewDetail(row)">
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 职位发布/编辑对话框 -->
    <el-dialog
      v-model="showJobDialog"
      :title="editingJob ? '编辑职位' : '发布职位'"
      width="800px"
      @close="resetJobForm"
    >
      <el-form :model="jobForm" :rules="jobRules" ref="jobFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职位标题" prop="title">
              <el-input v-model="jobForm.title" placeholder="请输入职位标题" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工作类型" prop="job_type">
              <el-select v-model="jobForm.job_type" placeholder="请选择工作类型">
                <el-option label="全职" value="full_time" />
                <el-option label="兼职" value="part_time" />
                <el-option label="实习" value="internship" />
                <el-option label="合同工" value="contract" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工作城市" prop="work_city">
              <el-input v-model="jobForm.work_city" placeholder="请输入工作城市" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="招聘人数" prop="recruitment_count">
              <el-input-number v-model="jobForm.recruitment_count" :min="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最低薪资" prop="salary_min">
              <el-input-number v-model="jobForm.salary_min" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最高薪资" prop="salary_max">
              <el-input-number v-model="jobForm.salary_max" :min="0" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="工作地址" prop="work_address">
          <el-input v-model="jobForm.work_address" placeholder="请输入详细工作地址" />
        </el-form-item>

        <el-form-item label="经验要求" prop="experience_required">
          <el-input v-model="jobForm.experience_required" placeholder="如：3-5年" />
        </el-form-item>

        <el-form-item label="学历要求" prop="education_required">
          <el-input v-model="jobForm.education_required" placeholder="如：本科及以上" />
        </el-form-item>

        <el-form-item label="职位描述" prop="description">
          <el-input
            v-model="jobForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述职位要求和工作内容"
          />
        </el-form-item>

        <el-form-item label="岗位职责" prop="responsibilities">
          <el-input
            v-model="jobForm.responsibilities"
            type="textarea"
            :rows="3"
            placeholder="请描述主要工作职责"
          />
        </el-form-item>

        <el-form-item label="福利待遇" prop="benefits">
          <el-input
            v-model="jobForm.benefits"
            type="textarea"
            :rows="2"
            placeholder="请描述福利待遇"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showJobDialog = false">取消</el-button>
        <el-button @click="saveJobAsDraft">保存草稿</el-button>
        <el-button type="primary" @click="publishJob">发布职位</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, ArrowDown } from '@element-plus/icons-vue'
import request from '@/utils/request'

const userStore = useUserStore()

// 响应式数据
const activeTab = ref('jobs')
const jobsLoading = ref(false)
const applicationsLoading = ref(false)
const interviewsLoading = ref(false)

// 职位相关数据
const jobs = ref([])
const jobSearch = ref('')
const jobStatusFilter = ref('')
const showJobDialog = ref(false)
const editingJob = ref(null)
const jobFormRef = ref()

// 简历相关数据
const applications = ref([])
const applicationStatusFilter = ref('')
const selectedJobFilter = ref('')

// 面试相关数据
const interviews = ref([])
const showInterviewDialog = ref(false)

// 职位表单数据
const jobForm = ref({
  title: '',
  job_type: '',
  work_city: '',
  work_address: '',
  salary_min: null,
  salary_max: null,
  recruitment_count: 1,
  experience_required: '',
  education_required: '',
  description: '',
  responsibilities: '',
  benefits: ''
})

// 表单验证规则
const jobRules = {
  title: [{ required: true, message: '请输入职位标题', trigger: 'blur' }],
  job_type: [{ required: true, message: '请选择工作类型', trigger: 'change' }],
  work_city: [{ required: true, message: '请输入工作城市', trigger: 'blur' }],
  work_address: [{ required: true, message: '请输入工作地址', trigger: 'blur' }],
  description: [{ required: true, message: '请输入职位描述', trigger: 'blur' }],
  responsibilities: [{ required: true, message: '请输入岗位职责', trigger: 'blur' }]
}

// 计算属性
const filteredJobs = computed(() => {
  let filtered = jobs.value

  if (jobSearch.value) {
    filtered = filtered.filter(job =>
      job.title.toLowerCase().includes(jobSearch.value.toLowerCase())
    )
  }

  if (jobStatusFilter.value) {
    filtered = filtered.filter(job => job.status === jobStatusFilter.value)
  }

  return filtered
})

const filteredApplications = computed(() => {
  let filtered = applications.value

  if (applicationStatusFilter.value) {
    filtered = filtered.filter(app => app.status === applicationStatusFilter.value)
  }

  if (selectedJobFilter.value) {
    filtered = filtered.filter(app => app.job_id === selectedJobFilter.value)
  }

  return filtered
})

// 工具函数
const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const formatDateTime = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

const getJobTypeText = (type) => {
  const types = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'contract': '合同工'
  }
  return types[type] || type
}

const getStatusText = (status) => {
  const statuses = {
    'draft': '草稿',
    'published': '已发布',
    'paused': '已暂停',
    'closed': '已关闭'
  }
  return statuses[status] || status
}

const getStatusType = (status) => {
  const types = {
    'draft': 'info',
    'published': 'success',
    'paused': 'warning',
    'closed': 'danger'
  }
  return types[status] || ''
}

const getApplicationStatusText = (status) => {
  const statuses = {
    'pending': '待审核',
    'reviewing': '审核中',
    'interview': '面试中',
    'accepted': '已录用',
    'rejected': '已拒绝',
    'withdrawn': '已撤回'
  }
  return statuses[status] || status
}

const getApplicationStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'reviewing': 'primary',
    'interview': 'info',
    'accepted': 'success',
    'rejected': 'danger',
    'withdrawn': 'info'
  }
  return types[status] || ''
}

const getInterviewTypeText = (type) => {
  const types = {
    'phone': '电话面试',
    'video': '视频面试',
    'onsite': '现场面试',
    'group': '群面'
  }
  return types[type] || type
}

const getInterviewStatusText = (status) => {
  const statuses = {
    'scheduled': '已安排',
    'confirmed': '已确认',
    'completed': '已完成',
    'cancelled': '已取消',
    'rescheduled': '已改期'
  }
  return statuses[status] || status
}

const getInterviewStatusType = (status) => {
  const types = {
    'scheduled': 'warning',
    'confirmed': 'primary',
    'completed': 'success',
    'cancelled': 'danger',
    'rescheduled': 'info'
  }
  return types[status] || ''
}

// API调用方法
const fetchJobs = async () => {
  try {
    jobsLoading.value = true
    const response = await request.get('/jobs/enterprise-jobs/')
    jobs.value = response.data.results || response.data || []
  } catch (error) {
    console.error('获取职位列表失败:', error)
    ElMessage.error('获取职位列表失败')
  } finally {
    jobsLoading.value = false
  }
}

const fetchApplications = async () => {
  try {
    applicationsLoading.value = true
    const response = await request.get('/jobs/enterprise-applications/')
    applications.value = response.data.results || response.data || []
  } catch (error) {
    console.error('获取简历列表失败:', error)
    ElMessage.error('获取简历列表失败')
  } finally {
    applicationsLoading.value = false
  }
}

const fetchInterviews = async () => {
  try {
    interviewsLoading.value = true
    // TODO: 实现面试管理API
    // const response = await request.get('/interviews/enterprise-interviews/')
    // interviews.value = response.data.results || response.data || []
    interviews.value = [] // 暂时返回空数组
  } catch (error) {
    console.error('获取面试列表失败:', error)
    ElMessage.error('获取面试列表失败')
  } finally {
    interviewsLoading.value = false
  }
}

// 职位操作方法
const editJob = (job) => {
  editingJob.value = job
  jobForm.value = { ...job }
  showJobDialog.value = true
}

const resetJobForm = () => {
  editingJob.value = null
  jobForm.value = {
    title: '',
    job_type: '',
    work_city: '',
    work_address: '',
    salary_min: null,
    salary_max: null,
    recruitment_count: 1,
    experience_required: '',
    education_required: '',
    description: '',
    responsibilities: '',
    benefits: ''
  }
  if (jobFormRef.value) {
    jobFormRef.value.resetFields()
  }
}

const saveJobAsDraft = async () => {
  try {
    await jobFormRef.value.validate()
    const jobData = { ...jobForm.value, status: 'draft' }

    if (editingJob.value) {
      await request.put(`/jobs/enterprise-jobs/${editingJob.value.id}/`, jobData)
      ElMessage.success('职位草稿保存成功')
    } else {
      await request.post('/jobs/enterprise-jobs/', jobData)
      ElMessage.success('职位草稿创建成功')
    }

    showJobDialog.value = false
    await fetchJobs()
  } catch (error) {
    console.error('保存职位失败:', error)
    ElMessage.error('保存职位失败')
  }
}

const publishJob = async () => {
  try {
    await jobFormRef.value.validate()
    const jobData = { ...jobForm.value, status: 'published' }

    if (editingJob.value) {
      await request.put(`/jobs/enterprise-jobs/${editingJob.value.id}/`, jobData)
      ElMessage.success('职位更新并发布成功')
    } else {
      await request.post('/jobs/enterprise-jobs/', jobData)
      ElMessage.success('职位发布成功')
    }

    showJobDialog.value = false
    await fetchJobs()
  } catch (error) {
    console.error('发布职位失败:', error)
    ElMessage.error('发布职位失败')
  }
}

const handleJobAction = async (command, job) => {
  try {
    switch (command) {
      case 'pause':
        await request.patch(`/jobs/enterprise-jobs/${job.id}/`, { status: 'paused' })
        ElMessage.success('职位已暂停')
        break
      case 'resume':
        await request.patch(`/jobs/enterprise-jobs/${job.id}/`, { status: 'published' })
        ElMessage.success('职位已恢复')
        break
      case 'close':
        await request.patch(`/jobs/enterprise-jobs/${job.id}/`, { status: 'closed' })
        ElMessage.success('职位已关闭')
        break
      case 'delete':
        await ElMessageBox.confirm('确定要删除这个职位吗？', '确认删除', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await request.delete(`/jobs/enterprise-jobs/${job.id}/`)
        ElMessage.success('职位已删除')
        break
    }
    await fetchJobs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

const viewApplications = (job) => {
  selectedJobFilter.value = job.id
  activeTab.value = 'resumes'
  fetchApplications()
}

// 简历操作方法
const viewResume = (application) => {
  ElMessage.info(`查看简历功能开发中: ${application.applicant_name}`)
}

const handleApplicationAction = async (command, application) => {
  try {
    switch (command) {
      case 'approve':
        await request.patch(`/jobs/enterprise-applications/${application.id}/update_status/`, { status: 'reviewing' })
        ElMessage.success('已通过初筛')
        break
      case 'interview':
        await request.patch(`/jobs/enterprise-applications/${application.id}/update_status/`, { status: 'interview' })
        ElMessage.success('已安排面试')
        break
      case 'accept':
        await request.patch(`/jobs/enterprise-applications/${application.id}/update_status/`, { status: 'accepted' })
        ElMessage.success('已录用')
        break
      case 'reject':
        await request.patch(`/jobs/enterprise-applications/${application.id}/update_status/`, { status: 'rejected' })
        ElMessage.success('已拒绝')
        break
    }
    await fetchApplications()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 面试操作方法
const editInterview = (interview) => {
  ElMessage.info(`编辑面试功能开发中: ${interview.candidate_name}`)
}

const viewInterviewDetail = (interview) => {
  ElMessage.info(`查看面试详情功能开发中: ${interview.candidate_name}`)
}

// 生命周期
onMounted(() => {
  fetchJobs()
  fetchApplications()
  fetchInterviews()
})
</script>

<style scoped>
.recruitment-management {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-header h1 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 16px;
}

.management-tabs {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.management-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 30px;
  background: #fafafa;
  border-radius: 8px 8px 0 0;
}

.management-tabs :deep(.el-tabs__content) {
  padding: 0;
}

.tab-content {
  padding: 30px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left h3 {
  margin: 0 10px 0 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
  display: inline-block;
}

.count {
  color: #909399;
  font-size: 14px;
}

.filter-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

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

/* 操作按钮样式 */
.action-buttons {
  display: flex !important;
  gap: 6px;
  align-items: center;
  flex-wrap: nowrap !important;
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

.action-buttons .el-dropdown {
  margin: 0 !important;
  flex-shrink: 1;
}

.action-buttons .el-dropdown .el-button {
  margin: 0 !important;
  min-width: 50px;
  font-size: 11px;
  padding: 4px 8px;
}

/* 操作列固定样式 */
.el-table :deep(.el-table__fixed-right) {
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
}

.el-dialog :deep(.el-dialog__header) {
  background-color: #fafafa;
  padding: 20px 30px;
  border-radius: 8px 8px 0 0;
}

.el-dialog :deep(.el-dialog__body) {
  padding: 30px;
}

.el-dialog :deep(.el-dialog__footer) {
  padding: 20px 30px;
  background-color: #fafafa;
  border-radius: 0 0 8px 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recruitment-management {
    padding: 10px;
  }

  .page-header {
    padding: 20px;
  }

  .tab-content {
    padding: 20px;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-bar > * {
    width: 100% !important;
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

  .action-buttons .el-dropdown {
    width: 100%;
  }

  .action-buttons .el-dropdown .el-button {
    width: 100%;
  }
}
</style>
