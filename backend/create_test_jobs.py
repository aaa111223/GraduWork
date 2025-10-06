#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employment_platform.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.users.models import User, EnterpriseProfile, StudentProfile
from apps.jobs.models import Job, JobCategory
from apps.applications.models import JobApplication

def create_test_data():
    """创建测试数据"""
    
    # 创建职位分类
    categories = [
        {'name': '软件开发', 'description': '软件开发相关职位'},
        {'name': '产品设计', 'description': '产品设计相关职位'},
        {'name': '市场营销', 'description': '市场营销相关职位'},
        {'name': '人力资源', 'description': '人力资源相关职位'},
        {'name': '财务会计', 'description': '财务会计相关职位'},
    ]
    
    for cat_data in categories:
        category, created = JobCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        print(f"职位分类: {category.name} {'创建' if created else '已存在'}")
    
    # 创建企业用户和企业档案
    enterprise_users = [
        {
            'phone': '13900139001',
            'email': 'hr1@techcorp.com',
            'real_name': '张经理',
            'company_name': '北京科技有限公司',
            'company_code': 'BJKJ001',
            'industry': '互联网',
            'company_size': '100-500人',
            'company_address': '北京市海淀区中关村大街1号',
            'company_description': '专注于企业级软件开发的科技公司'
        },
        {
            'phone': '13900139002',
            'email': 'hr2@innovate.com',
            'real_name': '李总监',
            'company_name': '上海创新科技公司',
            'company_code': 'SHCX001',
            'industry': '人工智能',
            'company_size': '500-1000人',
            'company_address': '上海市浦东新区张江高科技园区',
            'company_description': '领先的人工智能解决方案提供商'
        },
        {
            'phone': '13900139003',
            'email': 'hr3@future.com',
            'real_name': '王主管',
            'company_name': '深圳未来科技',
            'company_code': 'SZWL001',
            'industry': '金融科技',
            'company_size': '50-100人',
            'company_address': '深圳市南山区科技园',
            'company_description': '专注金融科技创新的初创公司'
        }
    ]
    
    enterprise_profiles = []
    for ent_data in enterprise_users:
        try:
            user = User.objects.get(phone=ent_data['phone'])
            print(f"企业用户已存在: {user.phone}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone=ent_data['phone'],
                email=ent_data['email'],
                user_type='enterprise',
                real_name=ent_data['real_name'],
                password='123456'
            )
            print(f"企业用户创建成功: {user.phone}")
        
        try:
            profile = EnterpriseProfile.objects.get(user=user)
            print(f"企业档案已存在: {profile.company_name}")
        except EnterpriseProfile.DoesNotExist:
            profile = EnterpriseProfile.objects.create(
                user=user,
                company_name=ent_data['company_name'],
                company_code=ent_data['company_code'],
                industry=ent_data['industry'],
                company_size=ent_data['company_size'],
                company_address=ent_data['company_address'],
                company_description=ent_data['company_description'],
                is_verified=True
            )
            print(f"企业档案创建成功: {profile.company_name}")
        
        enterprise_profiles.append(profile)
    
    # 创建测试职位
    jobs_data = [
        {
            'title': 'Python后端开发工程师',
            'category': '软件开发',
            'job_type': 'full_time',
            'salary_min': 15000,
            'salary_max': 25000,
            'work_city': '北京市',
            'work_address': '北京市海淀区中关村大街1号',
            'experience_required': '3-5年',
            'education_required': '本科',
            'skills_required': ['Python', 'Django', 'MySQL', 'Redis', 'Linux'],
            'description': '负责公司核心业务系统的后端开发，包括API设计、数据库设计、系统架构优化等工作。',
            'responsibilities': '1. 负责后端API开发和维护\n2. 数据库设计和优化\n3. 系统性能调优\n4. 代码审查和技术分享',
            'benefits': '五险一金、年终奖、带薪年假、技能培训、弹性工作',
            'recruitment_count': 3,
            'company_index': 0
        },
        {
            'title': 'Vue.js前端开发工程师',
            'category': '软件开发',
            'job_type': 'full_time',
            'salary_min': 12000,
            'salary_max': 20000,
            'work_city': '上海市',
            'work_address': '上海市浦东新区张江高科技园区',
            'experience_required': '2-4年',
            'education_required': '本科',
            'skills_required': ['Vue.js', 'JavaScript', 'TypeScript', 'Element Plus', 'Webpack'],
            'description': '负责前端页面开发和用户体验优化，与后端团队协作完成产品功能开发。',
            'responsibilities': '1. 前端页面开发和维护\n2. 用户交互体验优化\n3. 前端架构设计\n4. 跨浏览器兼容性处理',
            'benefits': '六险一金、股票期权、免费午餐、健身房、团建活动',
            'recruitment_count': 2,
            'company_index': 1
        },
        {
            'title': '产品经理',
            'category': '产品设计',
            'job_type': 'full_time',
            'salary_min': 18000,
            'salary_max': 30000,
            'work_city': '深圳市',
            'work_address': '深圳市南山区科技园',
            'experience_required': '3-6年',
            'education_required': '本科',
            'skills_required': ['产品设计', '用户研究', '项目管理', 'Axure', 'Figma'],
            'description': '负责产品规划和需求分析，协调各部门资源推进产品开发进度。',
            'responsibilities': '1. 产品需求分析和规划\n2. 用户调研和数据分析\n3. 产品原型设计\n4. 跨部门协调沟通',
            'benefits': '高薪酬、期权激励、灵活办公、学习津贴、年度旅游',
            'recruitment_count': 1,
            'company_index': 2
        },
        {
            'title': 'Java开发工程师',
            'category': '软件开发',
            'job_type': 'full_time',
            'salary_min': 16000,
            'salary_max': 28000,
            'work_city': '北京市',
            'work_address': '北京市海淀区中关村大街1号',
            'experience_required': '2-5年',
            'education_required': '本科',
            'skills_required': ['Java', 'Spring Boot', 'MyBatis', 'MySQL', 'Docker'],
            'description': '参与企业级应用系统开发，负责核心业务模块的设计和实现。',
            'responsibilities': '1. Java应用开发\n2. 系统架构设计\n3. 数据库设计\n4. 单元测试编写',
            'benefits': '竞争性薪酬、绩效奖金、技术培训、职业发展',
            'recruitment_count': 5,
            'company_index': 0
        },
        {
            'title': 'UI/UX设计师',
            'category': '产品设计',
            'job_type': 'full_time',
            'salary_min': 10000,
            'salary_max': 18000,
            'work_city': '上海市',
            'work_address': '上海市浦东新区张江高科技园区',
            'experience_required': '1-3年',
            'education_required': '本科',
            'skills_required': ['Figma', 'Sketch', 'Adobe Creative Suite', '用户体验设计'],
            'description': '负责产品界面设计和用户体验优化，创造优秀的视觉效果。',
            'responsibilities': '1. 产品界面设计\n2. 用户体验研究\n3. 设计规范制定\n4. 与开发团队协作',
            'benefits': '创意环境、设计工具、培训机会、弹性工作时间',
            'recruitment_count': 2,
            'company_index': 1
        }
    ]
    
    for job_data in jobs_data:
        category = JobCategory.objects.get(name=job_data['category'])
        company = enterprise_profiles[job_data['company_index']]
        
        job, created = Job.objects.get_or_create(
            title=job_data['title'],
            company=company,
            defaults={
                'category': category,
                'job_type': job_data['job_type'],
                'salary_min': job_data['salary_min'],
                'salary_max': job_data['salary_max'],
                'work_city': job_data['work_city'],
                'work_address': job_data['work_address'],
                'experience_required': job_data['experience_required'],
                'education_required': job_data['education_required'],
                'skills_required': job_data['skills_required'],
                'description': job_data['description'],
                'responsibilities': job_data['responsibilities'],
                'benefits': job_data['benefits'],
                'recruitment_count': job_data['recruitment_count'],
                'status': 'published',
                'published_at': datetime.now()
            }
        )
        print(f"职位: {job.title} {'创建' if created else '已存在'}")
    
    # 创建一些测试申请
    student_users = User.objects.filter(user_type='student')[:3]
    jobs = Job.objects.all()[:3]

    for i, student_user in enumerate(student_users):
        # 确保学生有档案
        student_profile, created = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'student_id': f'2021{str(i+1).zfill(6)}',
                'school': '北京大学',
                'major': '计算机科学与技术',
                'grade': '2021级',
                'graduation_date': datetime(2025, 6, 30).date(),
                'gpa': 3.5 + i * 0.2
            }
        )
        if created:
            print(f"学生档案创建: {student_user.real_name}")

        for j, job in enumerate(jobs):
            if i <= j:  # 创建一些申请记录
                application, created = JobApplication.objects.get_or_create(
                    applicant=student_profile,
                    job=job,
                    defaults={
                        'status': ['pending', 'reviewing', 'accepted'][j % 3],
                        'cover_letter': f'我对{job.title}职位非常感兴趣，希望能够加入贵公司。',
                        'expected_salary': job.salary_min + 1000
                    }
                )
                if created:
                    print(f"申请记录创建: {student_user.real_name} -> {job.title}")
    
    print("\n=== 测试数据创建完成 ===")
    print(f"职位分类: {JobCategory.objects.count()} 个")
    print(f"企业档案: {EnterpriseProfile.objects.count()} 个")
    print(f"职位信息: {Job.objects.count()} 个")
    print(f"申请记录: {JobApplication.objects.count()} 个")

if __name__ == '__main__':
    create_test_data()
