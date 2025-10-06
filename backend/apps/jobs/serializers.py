# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Job, JobCategory, JobFavorite
from apps.users.models import EnterpriseProfile


class JobCategorySerializer(serializers.ModelSerializer):
    """职位分类序列化器"""
    
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description', 'parent', 'sort_order', 'is_active', 'created_at']


class EnterpriseProfileSimpleSerializer(serializers.ModelSerializer):
    """企业档案简单序列化器"""
    
    class Meta:
        model = EnterpriseProfile
        fields = ['id', 'company_name', 'industry', 'company_size', 'company_address', 'is_verified']


class JobListSerializer(serializers.ModelSerializer):
    """职位列表序列化器"""
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_industry = serializers.CharField(source='company.industry', read_only=True)
    company_size = serializers.CharField(source='company.company_size', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    salary_range = serializers.SerializerMethodField()
    location = serializers.CharField(source='work_city', read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'company_industry', 'company_size',
            'category_name', 'job_type', 'salary_range', 'location', 'work_city',
            'experience_required', 'education_required', 'skills_required',
            'description', 'recruitment_count', 'status', 'view_count',
            'application_count', 'is_favorited', 'created_at', 'updated_at', 'published_at'
        ]
    
    def get_salary_range(self, obj):
        """获取薪资范围字符串"""
        if obj.salary_min and obj.salary_max:
            if obj.salary_type == 'monthly':
                return f"{int(obj.salary_min/1000)}K-{int(obj.salary_max/1000)}K"
            elif obj.salary_type == 'yearly':
                return f"{int(obj.salary_min/10000)}万-{int(obj.salary_max/10000)}万"
            else:
                return f"{obj.salary_min}-{obj.salary_max}"
        elif obj.salary_min:
            return f"{int(obj.salary_min/1000)}K+"
        else:
            return "面议"

    def get_is_favorited(self, obj):
        """检查当前用户是否收藏了该职位"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return JobFavorite.objects.filter(user=request.user, job=obj).exists()
        return False


class JobDetailSerializer(serializers.ModelSerializer):
    """职位详情序列化器"""
    company = EnterpriseProfileSimpleSerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    salary_range = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'category', 'job_type', 'salary_min',
            'salary_max', 'salary_type', 'salary_range', 'work_city', 'work_address',
            'experience_required', 'education_required', 'skills_required',
            'description', 'responsibilities', 'benefits', 'recruitment_count',
            'application_deadline', 'status', 'view_count', 'application_count',
            'is_favorited', 'created_at', 'updated_at', 'published_at'
        ]
    
    def get_salary_range(self, obj):
        """获取薪资范围字符串"""
        if obj.salary_min and obj.salary_max:
            if obj.salary_type == 'monthly':
                return f"{int(obj.salary_min/1000)}K-{int(obj.salary_max/1000)}K"
            elif obj.salary_type == 'yearly':
                return f"{int(obj.salary_min/10000)}万-{int(obj.salary_max/10000)}万"
            else:
                return f"{obj.salary_min}-{obj.salary_max}"
        elif obj.salary_min:
            return f"{int(obj.salary_min/1000)}K+"
        else:
            return "面议"
    
    def get_is_favorited(self, obj):
        """检查当前用户是否收藏了该职位"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return JobFavorite.objects.filter(user=request.user, job=obj).exists()
        return False


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    """职位创建/更新序列化器"""
    
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'job_type', 'salary_min', 'salary_max',
            'salary_type', 'work_city', 'work_address', 'experience_required',
            'education_required', 'skills_required', 'description',
            'responsibilities', 'benefits', 'recruitment_count',
            'application_deadline', 'status'
        ]
    
    def validate(self, data):
        """验证数据"""
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError("最低薪资不能高于最高薪资")
        return data


class JobFavoriteSerializer(serializers.ModelSerializer):
    """职位收藏序列化器"""
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = JobFavorite
        fields = ['id', 'job', 'created_at']
