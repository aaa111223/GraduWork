#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employment_platform.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.users.models import User, Role

def create_test_users():
    """创建测试用户"""
    
    # 创建角色
    student_role, created = Role.objects.get_or_create(
        name='student',
        defaults={
            'description': '学生用户',
            'permissions': ['view_jobs', 'apply_jobs', 'manage_profile']
        }
    )
    print(f"学生角色: {'创建' if created else '已存在'}")

    admin_role, created = Role.objects.get_or_create(
        name='admin',
        defaults={
            'description': '管理员',
            'permissions': ['manage_users', 'manage_jobs', 'manage_system']
        }
    )
    print(f"管理员角色: {'创建' if created else '已存在'}")

    # 创建测试学生用户
    try:
        student_user = User.objects.get(phone='13800138000')
        print(f"学生用户已存在: {student_user.phone}")
    except User.DoesNotExist:
        student_user = User.objects.create_user(
            phone='13800138000',
            email='student@example.com',
            user_type='student',
            real_name='张三',
            gender='M',
            password='123456'
        )
        student_user.roles.add(student_role)
        print(f"学生用户创建成功: {student_user.phone} / 123456")

    # 创建测试管理员用户
    try:
        admin_user = User.objects.get(phone='13800138001')
        print(f"管理员用户已存在: {admin_user.phone}")
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            phone='13800138001',
            email='admin@example.com',
            user_type='admin',
            real_name='管理员',
            password='admin123'
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_user.roles.add(admin_role)
        print(f"管理员用户创建成功: {admin_user.phone} / admin123")

    # 创建更多测试学生用户
    test_students = [
        {
            'phone': '13800138002',
            'email': 'lisi@example.com',
            'real_name': '李四',
            'gender': 'F'
        },
        {
            'phone': '13800138003',
            'email': 'wangwu@example.com',
            'real_name': '王五',
            'gender': 'M'
        }
    ]

    for student_data in test_students:
        try:
            user = User.objects.get(phone=student_data['phone'])
            print(f"测试学生用户已存在: {user.phone}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone=student_data['phone'],
                email=student_data['email'],
                user_type='student',
                real_name=student_data['real_name'],
                gender=student_data['gender'],
                password='123456'
            )
            user.roles.add(student_role)
            print(f"测试学生用户创建成功: {user.phone} / 123456")

    print("\n=== 测试用户创建完成 ===")
    print("学生用户:")
    print("  13800138000 / 123456 (张三)")
    print("  13800138002 / 123456 (李四)")
    print("  13800138003 / 123456 (王五)")
    print("管理员用户:")
    print("  13800138001 / admin123 (管理员)")

if __name__ == '__main__':
    create_test_users()
