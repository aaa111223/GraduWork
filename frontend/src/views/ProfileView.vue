<template>
  <div class="profile">
    <div class="page-header">
      <h1>个人中心</h1>
      <p>管理您的个人信息和简历</p>
    </div>

    <div class="profile-content">
      <!-- 左侧：个人信息 -->
      <div class="left-section">
        <el-card>
          <template #header>
            <span>基本信息</span>
          </template>

          <div class="profile-info">
            <div class="avatar-section">
              <el-avatar :size="80" :src="userInfo.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <el-button size="small" @click="uploadAvatar">更换头像</el-button>
            </div>

            <el-form :model="userInfo" label-width="80px" v-loading="loading">
              <el-form-item label="姓名">
                <el-input v-model="userInfo.real_name" placeholder="请输入真实姓名" />
              </el-form-item>

              <el-form-item label="手机号">
                <el-input v-model="userInfo.phone" disabled />
              </el-form-item>

              <el-form-item label="邮箱">
                <el-input v-model="userInfo.email" placeholder="请输入邮箱地址" />
              </el-form-item>

              <el-form-item label="性别">
                <el-radio-group v-model="userInfo.gender">
                  <el-radio label="M">男</el-radio>
                  <el-radio label="F">女</el-radio>
                  <el-radio label="O">其他</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="出生日期">
                <el-date-picker v-model="userInfo.birth_date" type="date" placeholder="请选择出生日期" />
              </el-form-item>

              <el-form-item label="地址">
                <el-input v-model="userInfo.address" type="textarea" placeholder="请输入详细地址" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="saveProfile" :loading="loading">保存信息</el-button>
              </el-form-item>
            </el-form>

            <!-- 学生档案信息 -->
            <el-card v-if="userStore.isStudent" style="margin-top: 20px;">
              <template #header>
                <span>学生档案</span>
              </template>

              <el-form :model="studentProfile" label-width="80px">
                <el-form-item label="学号">
                  <el-input v-model="studentProfile.student_id" placeholder="请输入学号" />
                </el-form-item>

                <el-form-item label="学校">
                  <el-input v-model="studentProfile.school" placeholder="请输入学校名称" />
                </el-form-item>

                <el-form-item label="专业">
                  <el-input v-model="studentProfile.major" placeholder="请输入专业名称" />
                </el-form-item>

                <el-form-item label="年级">
                  <el-input v-model="studentProfile.grade" placeholder="如：2021级" />
                </el-form-item>

                <el-form-item label="毕业时间">
                  <el-date-picker v-model="studentProfile.graduation_date" type="date" placeholder="请选择毕业时间" />
                </el-form-item>

                <el-form-item label="GPA">
                  <el-input-number v-model="studentProfile.gpa" :min="0" :max="4" :precision="2" placeholder="请输入GPA" />
                </el-form-item>

                <el-form-item label="技能">
                  <el-select v-model="studentProfile.skills" multiple filterable allow-create placeholder="请选择或输入技能" style="width: 100%">
                    <el-option v-for="skill in commonSkills" :key="skill" :label="skill" :value="skill" />
                  </el-select>
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="saveStudentProfile" :loading="loading">保存学生档案</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
        </el-card>
      </div>

      <!-- 右侧：简历管理 -->
      <div class="right-section">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>简历管理</span>
              <el-button type="primary" size="small" @click="showResumeDialog = true">
                <el-icon><Plus /></el-icon>
                上传简历
              </el-button>
            </div>
          </template>

          <div class="resume-list">
            <div v-if="resumes.length === 0" class="no-data">
              暂无简历，请上传您的简历
            </div>

            <div v-else>
              <div v-for="resume in resumes" :key="resume.id" class="resume-item">
                <div class="resume-info">
                  <h4>{{ resume.name }}</h4>
                  <p>上传时间：{{ new Date(resume.created_at).toLocaleDateString() }}</p>
                  <p>文件大小：{{ resume.file_size_display }}</p>
                  <p>文件类型：{{ resume.file_type.toUpperCase() }}</p>
                  <el-tag v-if="resume.is_default" type="success" size="small">默认简历</el-tag>
                </div>
                <div class="resume-actions">
                  <el-button size="small" @click="previewResume(resume)">预览</el-button>
                  <el-button size="small" @click="downloadResume(resume)">下载</el-button>
                  <el-button size="small" type="danger" @click="deleteResume(resume)">删除</el-button>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 求职意向 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>求职意向</span>
          </template>

          <el-form :model="jobIntention" label-width="100px" v-loading="loading">
            <el-form-item label="期望职位">
              <el-input v-model="jobIntention.position" placeholder="如：前端开发工程师" />
            </el-form-item>

            <el-form-item label="期望薪资">
              <el-select v-model="jobIntention.salary_range" style="width: 100%" placeholder="请选择期望薪资">
                <el-option label="3K-5K" value="3K-5K" />
                <el-option label="5K-10K" value="5K-10K" />
                <el-option label="10K-15K" value="10K-15K" />
                <el-option label="15K-25K" value="15K-25K" />
                <el-option label="25K-35K" value="25K-35K" />
                <el-option label="35K以上" value="35K+" />
              </el-select>
            </el-form-item>

            <el-form-item label="期望城市">
              <el-select v-model="jobIntention.work_cities" multiple style="width: 100%" placeholder="请选择期望工作城市">
                <el-option label="北京市" value="北京市" />
                <el-option label="上海市" value="上海市" />
                <el-option label="深圳市" value="深圳市" />
                <el-option label="广州市" value="广州市" />
                <el-option label="杭州市" value="杭州市" />
                <el-option label="成都市" value="成都市" />
                <el-option label="西安市" value="西安市" />
                <el-option label="南京市" value="南京市" />
              </el-select>
            </el-form-item>

            <el-form-item label="工作类型">
              <el-radio-group v-model="jobIntention.job_type">
                <el-radio label="full_time">全职</el-radio>
                <el-radio label="part_time">兼职</el-radio>
                <el-radio label="internship">实习</el-radio>
                <el-radio label="contract">合同工</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="期望行业">
              <el-input v-model="jobIntention.industry" placeholder="如：互联网、金融、教育等" />
            </el-form-item>

            <el-form-item label="公司规模">
              <el-select v-model="jobIntention.company_size" style="width: 100%" placeholder="请选择期望公司规模">
                <el-option label="不限" value="" />
                <el-option label="20人以下" value="20人以下" />
                <el-option label="20-99人" value="20-99人" />
                <el-option label="100-499人" value="100-499人" />
                <el-option label="500-999人" value="500-999人" />
                <el-option label="1000人以上" value="1000人以上" />
              </el-select>
            </el-form-item>

            <el-form-item label="其他要求">
              <el-input v-model="jobIntention.other_requirements" type="textarea" placeholder="其他特殊要求或期望" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveJobIntention" :loading="loading">保存意向</el-button>
            </el-form-item>
          </el-form>
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
          <el-button type="primary" @click="confirmUpload">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Plus, UploadFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

const userStore = useUserStore()
const showResumeDialog = ref(false)
const loading = ref(false)

// 常用技能列表
const commonSkills = ref([
  'Java', 'Python', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
  'React', 'Vue.js', 'Angular', 'Node.js', 'Express', 'Spring', 'Django', 'Flask',
  'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
  'Git', 'Linux', 'AWS', 'Azure', 'HTML', 'CSS', 'Sass', 'Less',
  'Webpack', 'Vite', 'Maven', 'Gradle', 'Jenkins', 'CI/CD'
])

const userInfo = ref({
  real_name: '',
  phone: '',
  email: '',
  gender: '',
  birth_date: null,
  address: '',
  avatar: ''
})

const studentProfile = ref({
  student_id: '',
  school: '',
  major: '',
  grade: '',
  graduation_date: null,
  gpa: null,
  skills: []
})

const resumes = ref([])

const jobIntention = ref({
  position: '',
  salary_range: '',
  work_cities: [],
  job_type: 'full_time',
  industry: '',
  company_size: '',
  other_requirements: ''
})

// 通用错误处理函数
const handleError = (error, defaultMessage) => {
  console.error(defaultMessage + ':', error)
  let errorMessage = defaultMessage
  if (error.response && error.response.data) {
    if (typeof error.response.data === 'string') {
      errorMessage = error.response.data
    } else if (error.response.data.message) {
      errorMessage = error.response.data.message
    } else if (error.response.data.detail) {
      errorMessage = error.response.data.detail
    } else {
      const errors = []
      for (const [field, messages] of Object.entries(error.response.data)) {
        if (Array.isArray(messages)) {
          errors.push(`${field}: ${messages.join(', ')}`)
        } else {
          errors.push(`${field}: ${messages}`)
        }
      }
      if (errors.length > 0) {
        errorMessage = errors.join('; ')
      }
    }
  }
  ElMessage.error(errorMessage)
  return errorMessage
}

// 获取用户完整信息
const fetchUserProfile = async () => {
  try {
    loading.value = true
    const response = await request.get('/users/users/profile/')
    const data = response.data

    // 更新用户基本信息
    userInfo.value = {
      real_name: data.real_name || '',
      phone: data.phone || '',
      email: data.email || '',
      gender: data.gender || '',
      birth_date: data.birth_date || null,
      address: data.address || '',
      avatar: data.avatar || ''
    }

    // 更新学生档案信息
    if (data.student_profile) {
      studentProfile.value = {
        student_id: data.student_profile.student_id || '',
        school: data.student_profile.school || '',
        major: data.student_profile.major || '',
        grade: data.student_profile.grade || '',
        graduation_date: data.student_profile.graduation_date || null,
        gpa: data.student_profile.gpa ? parseFloat(data.student_profile.gpa) : null,
        skills: data.student_profile.skills || []
      }
    }

    // 更新求职意向
    if (data.job_intention) {
      jobIntention.value = {
        position: data.job_intention.position || '',
        salary_range: data.job_intention.salary_range || '',
        work_cities: data.job_intention.work_cities || [],
        job_type: data.job_intention.job_type || 'full_time',
        industry: data.job_intention.industry || '',
        company_size: data.job_intention.company_size || '',
        other_requirements: data.job_intention.other_requirements || ''
      }
    }

    // 更新简历列表
    resumes.value = data.resumes || []

  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  } finally {
    loading.value = false
  }
}

// 保存用户基本信息
const saveProfile = async () => {
  try {
    loading.value = true
    // 只发送允许更新的字段，过滤掉空值和不需要的字段
    const updateData = {}

    if (userInfo.value.real_name) {
      updateData.real_name = userInfo.value.real_name
    }
    if (userInfo.value.email) {
      updateData.email = userInfo.value.email
    }
    if (userInfo.value.gender) {
      updateData.gender = userInfo.value.gender
    }
    if (userInfo.value.birth_date) {
      // 确保日期格式为 YYYY-MM-DD
      const date = new Date(userInfo.value.birth_date)
      if (!isNaN(date.getTime())) {
        updateData.birth_date = date.toISOString().split('T')[0]
      }
    }
    if (userInfo.value.address) {
      updateData.address = userInfo.value.address
    }
    // 注意：avatar 字段不在这里处理，应该有单独的头像上传功能

    const response = await request.put('/users/users/update_profile/', updateData)
    ElMessage.success('个人信息保存成功')
    // 更新store中的用户信息
    await userStore.fetchUserInfo()
  } catch (error) {
    handleError(error, '保存个人信息失败')
  } finally {
    loading.value = false
  }
}

// 保存学生档案
const saveStudentProfile = async () => {
  try {
    loading.value = true
    // 准备学生档案数据，过滤空值
    const profileData = {}

    if (studentProfile.value.student_id) {
      profileData.student_id = studentProfile.value.student_id
    }
    if (studentProfile.value.school) {
      profileData.school = studentProfile.value.school
    }
    if (studentProfile.value.major) {
      profileData.major = studentProfile.value.major
    }
    if (studentProfile.value.grade) {
      profileData.grade = studentProfile.value.grade
    }
    if (studentProfile.value.graduation_date) {
      // 如果毕业日期是Date对象，转换为字符串
      if (studentProfile.value.graduation_date instanceof Date) {
        profileData.graduation_date = studentProfile.value.graduation_date.toISOString().split('T')[0]
      } else {
        profileData.graduation_date = studentProfile.value.graduation_date
      }
    }
    if (studentProfile.value.gpa !== null && studentProfile.value.gpa !== undefined) {
      profileData.gpa = studentProfile.value.gpa
    }
    if (studentProfile.value.skills && studentProfile.value.skills.length > 0) {
      profileData.skills = studentProfile.value.skills
    }

    await request.put('/users/student-profiles/update_current/', profileData)
    ElMessage.success('学生档案保存成功')
    // 更新用户信息
    await fetchUserProfile()
  } catch (error) {
    handleError(error, '保存学生档案失败')
  } finally {
    loading.value = false
  }
}

// 保存求职意向
const saveJobIntention = async () => {
  try {
    loading.value = true
    await request.post('/users/users/job_intention/', jobIntention.value)
    ElMessage.success('求职意向保存成功')
  } catch (error) {
    handleError(error, '保存求职意向失败')
  } finally {
    loading.value = false
  }
}

// 获取简历列表
const fetchResumes = async () => {
  try {
    const response = await request.get('/users/users/resumes/')
    resumes.value = response.data
  } catch (error) {
    console.error('获取简历列表失败:', error)
    ElMessage.error('获取简历列表失败')
  }
}

// 处理简历上传
const uploadedFile = ref(null)

const handleResumeUpload = (file) => {
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

  uploadedFile.value = file
  return false // 阻止自动上传
}

// 确认上传简历
const confirmUpload = async () => {
  if (!uploadedFile.value) {
    ElMessage.error('请选择要上传的文件')
    return
  }

  try {
    loading.value = true
    const formData = new FormData()
    formData.append('file', uploadedFile.value)
    formData.append('name', uploadedFile.value.name)

    await request.post('/users/users/resumes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    showResumeDialog.value = false
    uploadedFile.value = null
    ElMessage.success('简历上传成功!')
    await fetchResumes()
  } catch (error) {
    console.error('简历上传失败:', error)
    ElMessage.error('简历上传失败')
  } finally {
    loading.value = false
  }
}

// 预览简历
const previewResume = (resume) => {
  if (resume.file) {
    window.open(resume.file, '_blank')
  } else {
    ElMessage.info('无法预览该简历')
  }
}

// 下载简历
const downloadResume = async (resume) => {
  try {
    const response = await request.get(`/users/users/resumes/${resume.id}/`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', resume.name)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    ElMessage.success('简历下载成功')
  } catch (error) {
    console.error('简历下载失败:', error)
    ElMessage.error('简历下载失败')
  }
}

// 删除简历
const deleteResume = async (resume) => {
  try {
    await ElMessageBox.confirm('确定要删除这份简历吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await request.delete(`/users/users/resumes/${resume.id}/`)
    ElMessage.success('简历删除成功')
    await fetchResumes()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('简历删除失败:', error)
      ElMessage.error('简历删除失败')
    }
  }
}

// 头像上传
const uploadAvatar = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/jpeg,image/jpg,image/png,image/gif'
  input.onchange = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // 验证文件大小 (5MB)
    if (file.size > 5 * 1024 * 1024) {
      ElMessage.error('文件大小不能超过5MB')
      return
    }

    // 验证文件类型
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if (!allowedTypes.includes(file.type)) {
      ElMessage.error('只支持 JPEG、PNG、GIF 格式的图片')
      return
    }

    try {
      loading.value = true
      const formData = new FormData()
      formData.append('avatar', file)

      const response = await request.post('/users/users/upload_avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      ElMessage.success('头像上传成功')
      // 更新用户信息
      await fetchUserProfile()
    } catch (error) {
      handleError(error, '头像上传失败')
    } finally {
      loading.value = false
    }
  }
  input.click()
}

onMounted(() => {
  fetchUserProfile()
})
</script>

<style scoped>
.profile {
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

.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}

.avatar-section .el-button {
  margin-top: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resume-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 12px;
}

.resume-item:last-child {
  margin-bottom: 0;
}

.resume-info h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.resume-info p {
  margin: 4px 0;
  color: #6c757d;
  font-size: 14px;
}

.resume-actions {
  display: flex;
  gap: 8px;
}

.no-data {
  text-align: center;
  color: #6c757d;
  padding: 40px;
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }

  .resume-item {
    flex-direction: column;
    gap: 12px;
  }

  .resume-actions {
    align-self: stretch;
    justify-content: center;
  }
}
</style>
