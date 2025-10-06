from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import JobApplication, Interview, ApplicationStatusLog
from .serializers import (
    JobApplicationCreateSerializer, JobApplicationListSerializer,
    JobApplicationDetailSerializer, JobApplicationUpdateSerializer,
    InterviewSerializer, ApplicationStatusLogSerializer
)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """职位申请视图集"""
    queryset = JobApplication.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'create':
            return JobApplicationCreateSerializer
        elif self.action == 'list':
            return JobApplicationListSerializer
        elif self.action in ['update', 'partial_update']:
            return JobApplicationUpdateSerializer
        else:
            return JobApplicationDetailSerializer

    def get_queryset(self):
        """获取查询集"""
        user = self.request.user

        # 学生只能看到自己的申请
        if hasattr(user, 'studentprofile'):
            return JobApplication.objects.filter(applicant__user=user).select_related('job', 'applicant__user')

        # 企业用户可以看到申请自己公司职位的申请
        elif hasattr(user, 'enterpriseprofile'):
            return JobApplication.objects.filter(job__company__user=user).select_related('job', 'applicant__user')

        # 管理员可以看到所有申请
        elif user.is_staff:
            return JobApplication.objects.all().select_related('job', 'applicant__user')

        return JobApplication.objects.none()

    def create(self, request, *args, **kwargs):
        """创建申请"""
        # 检查用户类型 - 只有学生用户可以申请职位
        if request.user.user_type != 'student':
            error_messages = {
                'admin': '管理员账户无法申请职位，管理员主要负责系统管理和用户服务',
                'enterprise': '企业用户无法申请职位，企业用户主要负责发布职位和管理招聘'
            }
            error_message = error_messages.get(request.user.user_type, '只有学生用户可以申请职位')
            return Response({'error': error_message}, status=status.HTTP_403_FORBIDDEN)

        # 检查用户是否有学生档案
        if not hasattr(request.user, 'studentprofile'):
            return Response({'error': '请先完善学生档案信息后再申请职位'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            response_serializer = JobApplicationDetailSerializer(application)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """批准申请"""
        application = self.get_object()

        # 检查权限：只有企业用户或管理员可以批准
        if not (hasattr(request.user, 'enterpriseprofile') or request.user.is_staff):
            return Response({'error': '无权限操作'}, status=status.HTTP_403_FORBIDDEN)

        # 检查是否为该职位的企业
        if hasattr(request.user, 'enterpriseprofile') and application.job.company.user != request.user:
            return Response({'error': '只能操作自己公司的职位申请'}, status=status.HTTP_403_FORBIDDEN)

        application.status = 'accepted'
        application.save()

        # 记录状态变更
        ApplicationStatusLog.objects.create(
            application=application,
            old_status='pending',
            new_status='accepted',
            changed_by=request.user,
            reason='申请已批准'
        )

        return Response({'message': '申请已批准'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝申请"""
        application = self.get_object()
        reason = request.data.get('reason', '')

        # 检查权限
        if not (hasattr(request.user, 'enterpriseprofile') or request.user.is_staff):
            return Response({'error': '无权限操作'}, status=status.HTTP_403_FORBIDDEN)

        # 检查是否为该职位的企业
        if hasattr(request.user, 'enterpriseprofile') and application.job.company.user != request.user:
            return Response({'error': '只能操作自己公司的职位申请'}, status=status.HTTP_403_FORBIDDEN)

        application.status = 'rejected'
        application.rejection_reason = reason
        application.save()

        # 记录状态变更
        ApplicationStatusLog.objects.create(
            application=application,
            old_status='pending',
            new_status='rejected',
            changed_by=request.user,
            reason=reason or '申请已拒绝'
        )

        return Response({'message': '申请已拒绝'}, status=status.HTTP_200_OK)


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()

    def list(self, request):
        return Response({'message': 'Interview list endpoint'}, status=status.HTTP_200_OK)

    def create(self, request):
        return Response({'message': 'Create interview endpoint'}, status=status.HTTP_200_OK)


class ApplicationStatusLogViewSet(viewsets.ModelViewSet):
    queryset = ApplicationStatusLog.objects.all()

    def list(self, request):
        return Response({'message': 'Application status log list endpoint'}, status=status.HTTP_200_OK)


class MyApplicationsView(APIView):
    def get(self, request):
        return Response({'message': 'My applications endpoint'}, status=status.HTTP_200_OK)


class EnterpriseApplicationsView(APIView):
    def get(self, request):
        return Response({'message': 'Enterprise applications endpoint'}, status=status.HTTP_200_OK)


class UpdateApplicationStatusView(APIView):
    def post(self, request, application_id):
        return Response({'message': 'Update application status endpoint'}, status=status.HTTP_200_OK)


class ScheduleInterviewView(APIView):
    def post(self, request, application_id):
        return Response({'message': 'Schedule interview endpoint'}, status=status.HTTP_200_OK)


class ApplicationStatisticsView(APIView):
    def get(self, request):
        return Response({'message': 'Application statistics endpoint'}, status=status.HTTP_200_OK)
