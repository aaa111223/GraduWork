from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from apps.users.models import User, StudentProfile, EnterpriseProfile
from apps.jobs.models import Job
from apps.applications.models import JobApplication
from apps.feedback.models import Feedback, SystemNotification
from apps.users.serializers import UserSerializer
from apps.jobs.serializers import JobListSerializer
from apps.feedback.serializers import FeedbackListSerializer

User = get_user_model()


class AdminDashboardStatsView(APIView):
    """管理员仪表板统计数据"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        # 用户统计
        total_users = User.objects.count()
        student_users = User.objects.filter(user_type='student').count()
        enterprise_users = User.objects.filter(user_type='enterprise').count()
        admin_users = User.objects.filter(user_type='admin').count()
        
        # 职位统计
        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(status='published').count()
        draft_jobs = Job.objects.filter(status='draft').count()
        
        # 申请统计
        total_applications = JobApplication.objects.count()
        pending_applications = JobApplication.objects.filter(status='pending').count()
        accepted_applications = JobApplication.objects.filter(status='accepted').count()
        
        # 反馈统计
        total_feedbacks = Feedback.objects.count()
        pending_feedbacks = Feedback.objects.filter(status='pending').count()
        
        # 今日统计
        today = timezone.now().date()
        today_users = User.objects.filter(created_at__date=today).count()
        today_applications = JobApplication.objects.filter(applied_at__date=today).count()
        today_feedbacks = Feedback.objects.filter(created_at__date=today).count()
        
        # 最近7天用户注册趋势
        week_ago = timezone.now() - timedelta(days=7)
        daily_registrations = []
        for i in range(7):
            date = (timezone.now() - timedelta(days=6-i)).date()
            count = User.objects.filter(created_at__date=date).count()
            daily_registrations.append({
                'date': date.strftime('%m-%d'),
                'count': count
            })
        
        return Response({
            'user_stats': {
                'total': total_users,
                'students': student_users,
                'enterprises': enterprise_users,
                'admins': admin_users,
                'today_new': today_users
            },
            'job_stats': {
                'total': total_jobs,
                'active': active_jobs,
                'draft': draft_jobs
            },
            'application_stats': {
                'total': total_applications,
                'pending': pending_applications,
                'accepted': accepted_applications,
                'today_new': today_applications
            },
            'feedback_stats': {
                'total': total_feedbacks,
                'pending': pending_feedbacks,
                'today_new': today_feedbacks
            },
            'trends': {
                'daily_registrations': daily_registrations
            }
        })


class AdminUserManagementViewSet(viewsets.ModelViewSet):
    """管理员用户管理"""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        user_type = self.request.query_params.get('user_type', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if search:
            queryset = queryset.filter(
                Q(real_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        
        if user_type:
            queryset = queryset.filter(user_type=user_type)
            
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """切换用户状态"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f'用户已{"启用" if user.is_active else "禁用"}',
            'is_active': user.is_active
        })
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        new_password = request.data.get('new_password', '123456')
        user.set_password(new_password)
        user.save()
        
        return Response({'message': '密码重置成功'})


class AdminJobManagementViewSet(viewsets.ModelViewSet):
    """管理员职位管理"""
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        search = self.request.query_params.get('search', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(company_name__icontains=search) |
                Q(work_city__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """更改职位状态"""
        job = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in ['published', 'draft', 'closed']:
            job.status = new_status
            job.save()
            return Response({'message': '职位状态更新成功'})
        
        return Response({'error': '无效的状态'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """获取职位申请列表"""
        job = self.get_object()
        applications = JobApplication.objects.filter(job=job).select_related('applicant__user').order_by('-applied_at')

        data = []
        for app in applications:
            data.append({
                'id': app.id,
                'user_name': app.applicant.user.real_name or app.applicant.user.phone,
                'user_phone': app.applicant.user.phone,
                'status': app.status,
                'status_display': app.get_status_display(),
                'applied_at': app.applied_at,
                'cover_letter': app.cover_letter
            })

        return Response({'results': data})


class AdminFeedbackManagementViewSet(viewsets.ModelViewSet):
    """管理员反馈管理"""
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        category = self.request.query_params.get('category', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """回复反馈"""
        feedback = self.get_object()
        reply_content = request.data.get('reply')
        
        if not reply_content:
            return Response({'error': '回复内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        feedback.admin_reply = reply_content
        feedback.status = 'resolved'
        feedback.resolved_at = timezone.now()
        feedback.save()
        
        # 创建系统通知
        SystemNotification.objects.create(
            title='反馈已回复',
            content=f'您的反馈"{feedback.title}"已收到管理员回复',
            notification_type='feedback',
            recipient=feedback.user,
            related_object_id=feedback.id,
            related_object_type='feedback'
        )
        
        return Response({'message': '回复成功'})
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """更改反馈状态"""
        feedback = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in ['pending', 'processing', 'resolved', 'closed']:
            feedback.status = new_status
            if new_status == 'resolved':
                feedback.resolved_at = timezone.now()
            feedback.save()
            return Response({'message': '反馈状态更新成功'})
        
        return Response({'error': '无效的状态'}, status=status.HTTP_400_BAD_REQUEST)


class AdminSystemSettingsView(APIView):
    """管理员系统设置"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """获取系统设置"""
        # 这里可以从数据库或配置文件中获取设置
        settings = {
            'platform_name': '学生就业管理平台',
            'contact_email': 'admin@example.com',
            'service_phone': '400-123-4567',
            'allow_register': True,
            'email_notification': True,
            'max_upload_size': 10,  # MB
            'session_timeout': 30,  # minutes
        }
        return Response(settings)
    
    def post(self, request):
        """保存系统设置"""
        # 这里可以将设置保存到数据库或配置文件
        settings = request.data
        
        # 验证设置数据
        required_fields = ['platform_name', 'contact_email', 'service_phone']
        for field in required_fields:
            if not settings.get(field):
                return Response(
                    {'error': f'{field} 不能为空'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # 这里应该保存到数据库或配置文件
        # 暂时只返回成功消息
        
        return Response({'message': '系统设置保存成功'})
