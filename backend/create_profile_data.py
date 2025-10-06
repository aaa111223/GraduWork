#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, date

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employment_platform.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.users.models import User, StudentProfile, JobIntention, Resume
from django.core.files.base import ContentFile

def create_profile_data():
    """为现有用户创建完整的档案数据"""
    
    # 获取所有学生用户
    student_users = User.objects.filter(user_type='student')
    
    for user in student_users:
        print(f"处理用户: {user.real_name} ({user.phone})")
        
        # 更新用户基本信息
        if not user.email or user.email == 'student@example.com':
            user.email = f"{user.phone}@example.com"
        if not user.gender:
            user.gender = 'M'
        if not user.address:
            user.address = f"北京市海淀区中关村大街{user.id}号"
        user.save()
        print(f"  - 更新用户基本信息")
        
        # 确保学生档案存在并完善
        try:
            profile = StudentProfile.objects.get(user=user)
            # 更新现有档案
            if not profile.gpa:
                profile.gpa = 3.5 + (user.id % 10) * 0.05  # 3.5-4.0之间的GPA
            if not profile.skills:
                skills_options = [
                    ['Python', 'Django', 'MySQL', 'Git'],
                    ['JavaScript', 'Vue.js', 'HTML', 'CSS'],
                    ['Java', 'Spring', 'MyBatis', 'Maven'],
                    ['React', 'Node.js', 'MongoDB', 'Express'],
                    ['C++', 'Algorithm', 'Data Structure', 'Linux']
                ]
                profile.skills = skills_options[user.id % len(skills_options)]
            profile.save()
            print(f"  - 更新学生档案")
        except StudentProfile.DoesNotExist:
            print(f"  - 学生档案不存在，跳过")
            continue
        
        # 创建求职意向
        job_intention, created = JobIntention.objects.get_or_create(
            user=user,
            defaults={
                'position': ['前端开发工程师', '后端开发工程师', '全栈开发工程师', '产品经理', 'UI设计师'][user.id % 5],
                'salary_range': ['10K-15K', '15K-25K', '25K-35K'][user.id % 3],
                'work_cities': [['北京市', '上海市'], ['深圳市', '广州市'], ['杭州市', '成都市']][user.id % 3],
                'job_type': 'full_time',
                'industry': ['互联网', '金融科技', '人工智能', '教育科技', '电商'][user.id % 5],
                'company_size': ['100-499人', '500-999人', '1000人以上'][user.id % 3],
                'other_requirements': '希望公司有良好的技术氛围和成长空间'
            }
        )
        if created:
            print(f"  - 创建求职意向: {job_intention.position}")
        else:
            print(f"  - 求职意向已存在: {job_intention.position}")
        
        # 创建示例简历记录（不创建实际文件）
        resume_names = [
            f"{user.real_name}_软件开发工程师_简历.pdf",
            f"{user.real_name}_个人简历_2025.docx"
        ]
        
        for i, resume_name in enumerate(resume_names):
            if user.id % 2 == i:  # 为不同用户创建不同数量的简历
                resume, created = Resume.objects.get_or_create(
                    user=user,
                    name=resume_name,
                    defaults={
                        'file': f'resumes/sample_{user.id}_{i}.pdf',  # 虚拟路径
                        'file_size': 1024 * 1024 * (2 + i),  # 2MB或3MB
                        'file_type': 'pdf' if resume_name.endswith('.pdf') else 'docx',
                        'is_default': i == 0
                    }
                )
                if created:
                    print(f"  - 创建简历记录: {resume_name}")
    
    print("\n=== 档案数据创建完成 ===")
    print(f"学生用户: {User.objects.filter(user_type='student').count()} 个")
    print(f"学生档案: {StudentProfile.objects.count()} 个")
    print(f"求职意向: {JobIntention.objects.count()} 个")
    print(f"简历记录: {Resume.objects.count()} 个")

if __name__ == '__main__':
    create_profile_data()
