<template>
  <div class="feedback">
    <div class="page-header">
      <h1>我的反馈</h1>
      <p>提交意见建议，帮助我们改进平台</p>
    </div>

    <div class="feedback-content">
      <!-- 左侧：提交反馈 -->
      <div class="left-section">
        <el-card>
          <template #header>
            <span>提交反馈</span>
          </template>

          <el-form :model="feedbackForm" :rules="rules" ref="feedbackFormRef" label-width="100px">
            <el-form-item label="反馈类型" prop="category_id">
              <el-select v-model="feedbackForm.category_id" style="width: 100%" :loading="categoriesLoading">
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="反馈标题" prop="title">
              <el-input v-model="feedbackForm.title" placeholder="请输入反馈标题" />
            </el-form-item>

            <el-form-item label="详细描述" prop="content">
              <el-input
                v-model="feedbackForm.content"
                type="textarea"
                :rows="6"
                placeholder="请详细描述您的问题或建议..."
              />
            </el-form-item>

            <el-form-item label="联系电话">
              <el-input v-model="feedbackForm.contact_phone" placeholder="可选，便于我们联系您" />
            </el-form-item>

            <el-form-item label="联系邮箱">
              <el-input v-model="feedbackForm.contact_email" placeholder="可选，便于我们联系您" />
            </el-form-item>

            <el-form-item label="上传截图">
              <el-upload
                class="upload-demo"
                action="#"
                :before-upload="handleImageUpload"
                list-type="picture-card"
                accept="image/*"
                :limit="3"
              >
                <el-icon><Plus /></el-icon>
              </el-upload>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="submitFeedback" :loading="submitting">
                提交反馈
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>

      <!-- 右侧：我的反馈记录 -->
      <div class="right-section">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的反馈记录</span>
              <el-button size="small" @click="refreshFeedbacks">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>

          <div class="feedback-list">
            <div v-if="feedbacks.length === 0" class="no-data">
              暂无反馈记录
            </div>

            <div v-else>
              <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-item">
                <div class="feedback-header">
                  <h4>{{ feedback.title }}</h4>
                  <el-tag :type="getStatusType(feedback.status)">
                    {{ getStatusText(feedback.status) }}
                  </el-tag>
                </div>

                <div class="feedback-meta">
                  <span class="feedback-type">{{ feedback.category_name || '未分类' }}</span>
                  <span class="feedback-date">{{ formatDate(feedback.created_at) }}</span>
                </div>

                <div class="feedback-content-preview">
                  {{ feedback.content.substring(0, 100) }}{{ feedback.content.length > 100 ? '...' : '' }}
                </div>

                <div class="feedback-actions">
                  <el-button size="small" @click="viewFeedback(feedback)">查看详情</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    v-if="feedback.status === 'pending'"
                    @click="deleteFeedback(feedback)"
                  >
                    删除
                  </el-button>
                </div>

                <!-- 回复内容 -->
                <div v-if="feedback.admin_reply" class="feedback-reply">
                  <div class="reply-header">
                    <el-icon><ChatDotRound /></el-icon>
                    <span>管理员回复：</span>
                  </div>
                  <div class="reply-content">{{ feedback.admin_reply }}</div>
                  <div class="reply-date">{{ formatDate(feedback.updated_at) }}</div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 反馈详情对话框 -->
    <el-dialog v-model="showFeedbackDetail" title="反馈详情" width="600px">
      <div v-if="selectedFeedback" class="feedback-detail">
        <div class="detail-header">
          <h3>{{ selectedFeedback.title }}</h3>
          <el-tag :type="getStatusType(selectedFeedback.status)">
            {{ getStatusText(selectedFeedback.status) }}
          </el-tag>
        </div>

        <div class="detail-meta">
          <p><strong>反馈类型：</strong>{{ selectedFeedback.category_name || '未分类' }}</p>
          <p><strong>提交时间：</strong>{{ formatDate(selectedFeedback.created_at) }}</p>
          <p v-if="selectedFeedback.contact_phone"><strong>联系电话：</strong>{{ selectedFeedback.contact_phone }}</p>
          <p v-if="selectedFeedback.contact_email"><strong>联系邮箱：</strong>{{ selectedFeedback.contact_email }}</p>
        </div>

        <div class="detail-content">
          <h4>详细描述</h4>
          <p>{{ selectedFeedback.content }}</p>
        </div>

        <div v-if="selectedFeedback.admin_reply" class="detail-reply">
          <h4>管理员回复</h4>
          <div class="reply-box">
            <p>{{ selectedFeedback.admin_reply }}</p>
            <div class="reply-date">回复时间：{{ formatDate(selectedFeedback.updated_at) }}</div>
          </div>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showFeedbackDetail = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, ChatDotRound } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

// 响应式数据
const router = useRouter()
const userStore = useUserStore()
const submitting = ref(false)
const showFeedbackDetail = ref(false)
const selectedFeedback = ref(null)
const feedbackFormRef = ref()
const categoriesLoading = ref(false)

// 计算属性
const isLoggedIn = computed(() => userStore.isLoggedIn)

const feedbackForm = ref({
  category_id: null,
  title: '',
  content: '',
  contact_phone: '',
  contact_email: '',
  priority: 'medium'
})

const categories = ref([])
const feedbacks = ref([])

const rules = {
  category_id: [{ required: true, message: '请选择反馈类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入反馈标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入详细描述', trigger: 'blur' }]
}

// 辅助函数
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 获取反馈分类
const fetchCategories = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  categoriesLoading.value = true
  try {
    const response = await request.get('/feedback/categories/')
    categories.value = response.data.results || response.data || []
    console.log('反馈分类:', categories.value)
  } catch (error) {
    console.error('获取反馈分类失败:', error)
    ElMessage.error('获取反馈分类失败')
  } finally {
    categoriesLoading.value = false
  }
}

// 获取我的反馈记录
const fetchFeedbacks = async () => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  try {
    const response = await request.get('/feedback/')
    feedbacks.value = response.data.results || response.data || []
    console.log('我的反馈:', feedbacks.value)
  } catch (error) {
    console.error('获取反馈记录失败:', error)
    ElMessage.error('获取反馈记录失败')
  }
}

const getStatusType = (status) => {
  const statusMap = {
    'pending': 'info',
    'processing': 'warning',
    'resolved': 'success',
    'closed': ''
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'resolved': '已解决',
    'closed': '已关闭'
  }
  return statusMap[status] || status
}

const handleImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isValidSize = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isValidSize) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }

  return false // 阻止自动上传
}

const submitFeedback = async () => {
  try {
    await feedbackFormRef.value.validate()
    submitting.value = true

    // 提交反馈
    await request.post('/feedback/', feedbackForm.value)

    ElMessage.success('反馈提交成功，我们会尽快处理！')
    resetForm()
    // 刷新反馈列表
    await fetchFeedbacks()
  } catch (error) {
    console.error('提交反馈失败:', error)
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('提交反馈失败，请稍后重试')
    }
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  feedbackFormRef.value?.resetFields()
}

const refreshFeedbacks = async () => {
  await fetchFeedbacks()
  ElMessage.success('刷新成功')
}

const viewFeedback = (feedback) => {
  selectedFeedback.value = feedback
  showFeedbackDetail.value = true
}

const deleteFeedback = async (feedback) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除反馈"${feedback.title}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 调用API删除反馈
    await request.delete(`/feedback/${feedback.id}/`)
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

onMounted(async () => {
  await Promise.all([
    fetchCategories(),
    fetchFeedbacks()
  ])
})
</script>

<style scoped>
.feedback {
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

.feedback-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feedback-item {
  padding: 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 16px;
}

.feedback-item:last-child {
  margin-bottom: 0;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.feedback-header h4 {
  margin: 0;
  color: #2c3e50;
}

.feedback-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  color: #6c757d;
  font-size: 14px;
}

.feedback-content-preview {
  color: #495057;
  line-height: 1.5;
  margin-bottom: 12px;
}

.feedback-actions {
  display: flex;
  gap: 8px;
}

.feedback-reply {
  margin-top: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #409eff;
  font-weight: 500;
}

.reply-content {
  color: #495057;
  line-height: 1.5;
  margin-bottom: 8px;
}

.reply-date {
  color: #6c757d;
  font-size: 12px;
}

.no-data {
  text-align: center;
  color: #6c757d;
  padding: 40px;
}

.feedback-detail .detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.feedback-detail .detail-header h3 {
  margin: 0;
  color: #2c3e50;
}

.feedback-detail .detail-meta p {
  margin: 8px 0;
  color: #495057;
}

.feedback-detail .detail-content,
.feedback-detail .detail-reply {
  margin-bottom: 24px;
}

.feedback-detail h4 {
  color: #2c3e50;
  margin-bottom: 12px;
}

.reply-box {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.reply-box p {
  margin: 0 0 12px 0;
  color: #495057;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .feedback-content {
    grid-template-columns: 1fr;
  }

  .feedback-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .feedback-actions {
    justify-content: center;
  }
}
</style>
