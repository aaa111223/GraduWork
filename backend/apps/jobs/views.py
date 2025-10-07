# -*- coding: utf-8 -*-
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F
from .models import JobCategory, Job, JobFavorite
from .serializers import (
    JobCategorySerializer, JobListSerializer, JobDetailSerializer,
    JobCreateUpdateSerializer, JobFavoriteSerializer
)
from apps.applications.models import JobApplication
from apps.applications.serializers import JobApplicationListSerializer


class JobPagination(PageNumberPagination):
    """职位分页器"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class JobCategoryViewSet(viewsets.ModelViewSet):
    """职位分类视图集"""
    queryset = JobCategory.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = JobCategorySerializer
    permission_classes = [AllowAny]


class JobViewSet(viewsets.ModelViewSet):
    """职位视图集"""
    queryset = Job.objects.filter(status='published').select_related('company', 'category').order_by('-created_at')
    permission_classes = [AllowAny]
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'work_city', 'category', 'company']
    search_fields = ['title', 'description', 'skills_required', 'company__company_name']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'view_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'list':
            return JobListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        else:
            return JobDetailSerializer

    def get_queryset(self):
        """获取查询集"""
        queryset = super().get_queryset()

        # 薪资范围过滤
        salary_min = self.request.query_params.get('salary_min')
        salary_max = self.request.query_params.get('salary_max')
        if salary_min:
            queryset = queryset.filter(salary_min__gte=salary_min)
        if salary_max:
            queryset = queryset.filter(salary_max__lte=salary_max)

        # 经验要求过滤
        experience = self.request.query_params.get('experience')
        if experience:
            queryset = queryset.filter(experience_required__icontains=experience)

        # 技能要求过滤
        skills = self.request.query_params.get('skills')
        if skills:
            skill_list = skills.split(',')
            for skill in skill_list:
                queryset = queryset.filter(skills_required__icontains=skill.strip())

        return queryset

    def perform_create(self, serializer):
        """创建职位时自动关联当前企业用户"""
        if self.request.user.is_authenticated and self.request.user.user_type == 'enterprise':
            try:
                enterprise_profile = self.request.user.enterpriseprofile
                serializer.save(company=enterprise_profile)
            except:
                raise ValidationError("企业档案不存在，无法发布职位")
        else:
            raise ValidationError("只有企业用户可以发布职位")

    def get_permissions(self):
        """根据动作设置权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """获取职位详情，增加浏览量"""
        instance = self.get_object()
        # 增加浏览量
        Job.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        # 重新获取实例以获取更新后的浏览量
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """获取最新职位"""
        limit = int(request.query_params.get('limit', 6))
        jobs = self.get_queryset()[:limit]
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def hot(self, request):
        """获取热门职位"""
        limit = int(request.query_params.get('limit', 6))
        jobs = self.get_queryset().order_by('-view_count', '-application_count')[:limit]
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """收藏职位"""
        if not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        job = self.get_object()
        favorite, created = JobFavorite.objects.get_or_create(
            user=request.user,
            job=job
        )

        if created:
            return Response({'message': '收藏成功'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '已经收藏过了'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """取消收藏职位"""
        if not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=status.HTTP_401_UNAUTHORIZED)

        job = self.get_object()
        try:
            favorite = JobFavorite.objects.get(user=request.user, job=job)
            favorite.delete()
            return Response({'message': '取消收藏成功'}, status=status.HTTP_200_OK)
        except JobFavorite.DoesNotExist:
            return Response({'message': '未收藏该职位'}, status=status.HTTP_404_NOT_FOUND)


class JobFavoriteViewSet(viewsets.ModelViewSet):
    """职位收藏视图集"""
    queryset = JobFavorite.objects.all()
    serializer_class = JobFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取当前用户的收藏"""
        return JobFavorite.objects.filter(user=self.request.user).select_related('job')


class JobSearchView(APIView):
    def get(self, request):
        return Response({'message': 'Job search endpoint'}, status=status.HTTP_200_OK)


class JobRecommendationView(APIView):
    def get(self, request):
        return Response({'message': 'Job recommendation endpoint'}, status=status.HTTP_200_OK)


class ToggleFavoriteView(APIView):
    def post(self, request, job_id):
        return Response({'message': 'Toggle favorite endpoint'}, status=status.HTTP_200_OK)


class EnterpriseJobViewSet(viewsets.ModelViewSet):
    """企业职位管理视图集"""
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """只返回当前企业用户发布的职位"""
        if self.request.user.user_type != 'enterprise':
            return Job.objects.none()

        try:
            enterprise_profile = self.request.user.enterpriseprofile
            return Job.objects.filter(company=enterprise_profile).order_by('-created_at')
        except:
            return Job.objects.none()

    def perform_create(self, serializer):
        """创建职位时自动关联当前企业"""
        try:
            enterprise_profile = self.request.user.enterpriseprofile
            serializer.save(company=enterprise_profile)
        except:
            raise ValidationError("企业档案不存在，无法发布职位")


class EnterpriseApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """企业简历管理视图集"""
    serializer_class = JobApplicationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """只返回申请当前企业职位的简历"""
        if self.request.user.user_type != 'enterprise':
            return JobApplication.objects.none()

        try:
            enterprise_profile = self.request.user.enterpriseprofile
            return JobApplication.objects.filter(
                job__company=enterprise_profile
            ).select_related('applicant', 'job').order_by('-applied_at')
        except:
            return JobApplication.objects.none()

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """更新申请状态"""
        application = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['pending', 'reviewing', 'interview', 'accepted', 'rejected']:
            return Response({'error': '无效的状态'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save()

        return Response({'message': '状态更新成功'}, status=status.HTTP_200_OK)
