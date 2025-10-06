# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import JobApplication, Interview, ApplicationStatusLog
from apps.jobs.serializers import JobListSerializer
from apps.users.serializers import StudentProfileSerializer


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """职位申请创建序列化器"""
    job_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = JobApplication
        fields = ['job_id', 'cover_letter', 'expected_salary']
    
    def validate_job_id(self, value):
        """验证职位ID"""
        from apps.jobs.models import Job
        try:
            job = Job.objects.get(id=value, status='published')
            return value
        except Job.DoesNotExist:
            raise serializers.ValidationError("职位不存在或已下线")
    
    def create(self, validated_data):
        """创建申请"""
        from apps.jobs.models import Job
        from apps.users.models import StudentProfile
        
        job_id = validated_data.pop('job_id')
        job = Job.objects.get(id=job_id)
        
        # 获取申请人的学生档案
        try:
            applicant = StudentProfile.objects.get(user=self.context['request'].user)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("请先完善学生档案信息")
        
        # 检查是否已经申请过
        if JobApplication.objects.filter(applicant=applicant, job=job).exists():
            raise serializers.ValidationError("您已经申请过这个职位了")
        
        # 创建申请
        application = JobApplication.objects.create(
            applicant=applicant,
            job=job,
            **validated_data
        )
        
        return application


class JobApplicationListSerializer(serializers.ModelSerializer):
    """职位申请列表序列化器"""
    job = JobListSerializer(read_only=True)
    applicant_name = serializers.CharField(source='applicant.user.real_name', read_only=True)
    applicant_phone = serializers.CharField(source='applicant.user.phone', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'applicant_name', 'applicant_phone', 'cover_letter',
            'expected_salary', 'status', 'status_display', 'applied_at', 'updated_at'
        ]


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    """职位申请详情序列化器"""
    job = JobListSerializer(read_only=True)
    applicant = StudentProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'applicant', 'cover_letter', 'resume', 'expected_salary',
            'status', 'status_display', 'hr_notes', 'rejection_reason',
            'applied_at', 'updated_at', 'reviewed_at'
        ]


class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    """职位申请更新序列化器"""
    
    class Meta:
        model = JobApplication
        fields = ['status', 'hr_notes', 'rejection_reason']
    
    def update(self, instance, validated_data):
        """更新申请状态"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # 记录状态变更日志
        if old_status != new_status:
            ApplicationStatusLog.objects.create(
                application=instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.context['request'].user,
                reason=validated_data.get('hr_notes', '')
            )
        
        return super().update(instance, validated_data)


class InterviewSerializer(serializers.ModelSerializer):
    """面试序列化器"""
    application = JobApplicationDetailSerializer(read_only=True)
    interviewer_name = serializers.CharField(source='interviewer.real_name', read_only=True)
    interview_type_display = serializers.CharField(source='get_interview_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'interviewer_name', 'interview_type', 'interview_type_display',
            'scheduled_time', 'duration', 'location', 'status', 'status_display',
            'score', 'feedback', 'notes', 'created_at', 'updated_at'
        ]


class ApplicationStatusLogSerializer(serializers.ModelSerializer):
    """申请状态日志序列化器"""
    changed_by_name = serializers.CharField(source='changed_by.real_name', read_only=True)
    
    class Meta:
        model = ApplicationStatusLog
        fields = [
            'id', 'old_status', 'new_status', 'changed_by_name', 'reason', 'created_at'
        ]
