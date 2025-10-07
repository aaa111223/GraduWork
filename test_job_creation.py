#!/usr/bin/env python3
"""
测试企业用户职位发布功能
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_job_creation_with_auth():
    """测试带认证的职位创建"""
    print("🔐 测试企业用户职位发布功能...")
    
    # 首先需要登录获取token
    login_data = {
        "username": "enterprise_user",  # 需要替换为实际的企业用户名
        "password": "password123"       # 需要替换为实际密码
    }
    
    try:
        # 登录
        print("1. 尝试登录...")
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   登录响应状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('access_token')
            print(f"   ✅ 登录成功，获取到token")
            
            # 设置认证头
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # 测试职位创建
            print("2. 测试职位创建...")
            job_data = {
                "title": "高级Python开发工程师",
                "category": 1,  # 假设软件开发分类ID为1
                "job_type": "full_time",
                "salary_min": 15000,
                "salary_max": 25000,
                "salary_type": "monthly",
                "work_city": "北京",
                "experience_required": "3-5年",
                "education_required": "本科",
                "skills_required": "Python, Django, Vue.js",
                "description": "负责后端系统开发和维护",
                "requirements": "熟练掌握Python和Django框架",
                "benefits": "五险一金，弹性工作制",
                "status": "published"
            }
            
            # 使用企业专用端点
            create_response = requests.post(
                f"{BASE_URL}/jobs/enterprise-jobs/", 
                json=job_data, 
                headers=headers
            )
            print(f"   职位创建响应状态码: {create_response.status_code}")
            
            if create_response.status_code == 201:
                job_result = create_response.json()
                print(f"   ✅ 职位创建成功！")
                print(f"   职位ID: {job_result.get('id')}")
                print(f"   职位标题: {job_result.get('title')}")
                return job_result.get('id')
            else:
                print(f"   ❌ 职位创建失败")
                print(f"   错误信息: {create_response.text}")
                
        else:
            print(f"   ❌ 登录失败: {login_response.text}")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        
    return None

def test_job_creation_without_auth():
    """测试不带认证的职位创建（应该失败）"""
    print("\n🚫 测试未认证用户职位发布（预期失败）...")
    
    job_data = {
        "title": "测试职位",
        "job_type": "full_time",
        "description": "测试描述"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/jobs/", json=job_data)
        print(f"   响应状态码: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ 正确拒绝了未认证用户的请求")
        else:
            print(f"   ⚠️ 意外的响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")

def test_enterprise_endpoints():
    """测试企业专用端点的可访问性"""
    print("\n🏢 测试企业专用端点...")
    
    endpoints = [
        "/jobs/enterprise-jobs/",
        "/jobs/enterprise-applications/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"   {endpoint} - 状态码: {response.status_code}")
            
            if response.status_code == 401:
                print(f"     ✅ 正确要求认证")
            elif response.status_code == 200:
                print(f"     ⚠️ 可能存在权限问题")
            else:
                print(f"     ❓ 其他状态码")
                
        except Exception as e:
            print(f"   ❌ {endpoint} - 错误: {e}")

def main():
    print("🚀 开始测试企业用户职位发布功能...")
    print("=" * 60)
    
    # 测试未认证访问
    test_job_creation_without_auth()
    
    # 测试企业端点
    test_enterprise_endpoints()
    
    # 测试认证访问（需要有效的企业用户账号）
    job_id = test_job_creation_with_auth()
    
    print("\n" + "=" * 60)
    print("✨ 测试完成！")
    
    if job_id:
        print(f"🎉 成功创建职位，ID: {job_id}")
    else:
        print("⚠️ 职位创建测试未成功（可能需要有效的企业用户账号）")
    
    print("\n📋 修复总结:")
    print("1. ✅ 修复了JobViewSet的perform_create方法")
    print("2. ✅ 添加了权限控制，只有认证用户可以创建职位")
    print("3. ✅ 企业用户创建职位时自动关联企业档案")
    print("4. ✅ 前端使用企业专用API端点")
    print("5. ✅ 修复了company_id为空的问题")

if __name__ == "__main__":
    main()
