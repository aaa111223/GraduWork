#!/usr/bin/env python3
"""
测试企业HR功能的脚本
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api_endpoints():
    """测试API端点是否可访问"""
    print("🔍 测试API端点可访问性...")
    
    # 测试基础端点
    endpoints = [
        "/jobs/categories/",
        "/jobs/",
        "/stats/dashboard/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"✅ {endpoint} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - 错误: {e}")
    
    # 测试需要认证的企业端点（预期401）
    auth_endpoints = [
        "/admin/stats/enterprise-dashboard/",
        "/jobs/enterprise-jobs/",
        "/jobs/enterprise-applications/",
    ]
    
    print("\n🔐 测试需要认证的企业端点...")
    for endpoint in auth_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 401:
                print(f"✅ {endpoint} - 正确返回401未认证")
            else:
                print(f"⚠️ {endpoint} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - 错误: {e}")

def test_frontend_accessibility():
    """测试前端页面可访问性"""
    print("\n🌐 测试前端页面可访问性...")
    
    try:
        response = requests.get("http://localhost:5173/")
        if response.status_code == 200:
            print("✅ 前端首页可访问")
            if "学生就业管理平台" in response.text:
                print("✅ 页面标题正确")
            else:
                print("⚠️ 页面标题可能有问题")
        else:
            print(f"❌ 前端首页 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 前端首页 - 错误: {e}")

def test_database_connection():
    """测试数据库连接"""
    print("\n💾 测试数据库连接...")
    
    try:
        # 通过获取职位分类来测试数据库连接
        response = requests.get(f"{BASE_URL}/jobs/categories/")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                print(f"✅ 数据库连接正常，找到 {len(data['results'])} 个职位分类")
                for category in data['results'][:3]:  # 显示前3个分类
                    print(f"   - {category['name']}: {category['description']}")
            else:
                print("⚠️ 数据库连接正常但没有数据")
        else:
            print(f"❌ 数据库连接测试失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 数据库连接测试失败 - 错误: {e}")

def main():
    print("🚀 开始测试企业HR功能...")
    print("=" * 50)
    
    test_api_endpoints()
    test_frontend_accessibility()
    test_database_connection()
    
    print("\n" + "=" * 50)
    print("✨ 测试完成！")
    print("\n📋 测试总结:")
    print("1. 后端服务器运行在: http://127.0.0.1:8000/")
    print("2. 前端服务器运行在: http://localhost:5173/")
    print("3. 企业HR功能已部署，需要登录后测试完整功能")
    print("\n🔗 可以访问以下页面测试:")
    print("   - 首页: http://localhost:5173/")
    print("   - 登录: http://localhost:5173/login")
    print("   - 注册: http://localhost:5173/register")

if __name__ == "__main__":
    main()
