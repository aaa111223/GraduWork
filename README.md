# 学生就业管理平台

## 项目概述
基于前后端分离架构的学生就业管理平台，为学生、企业和管理员提供完整的就业服务解决方案。

## 技术栈

### 后端
- **框架**: Django 4.x + Django REST Framework
- **数据库**: MySQL 8.0
- **认证**: JWT (JSON Web Token) + Session
- **权限**: RBAC (基于角色的访问控制)
- **密码加密**: Bcrypt
- **API**: RESTful API

### 前端
- **框架**: Vue 3.x
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP客户端**: Axios

## 项目结构
```
GraduProject/
├── backend/                 # Django后端项目
│   ├── employment_platform/ # 主项目目录
│   ├── apps/               # 应用模块
│   │   ├── authentication/ # 认证模块
│   │   ├── users/          # 用户管理
│   │   ├── jobs/           # 职位管理
│   │   ├── applications/   # 申请管理
│   │   └── feedback/       # 反馈系统
│   ├── requirements.txt    # Python依赖
│   └── manage.py
├── frontend/               # Vue3前端项目
│   ├── src/
│   │   ├── components/     # 公共组件
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理
│   │   └── api/            # API接口
│   ├── package.json
│   └── vite.config.js
├── docs/                   # 项目文档
├── venv/                   # Python虚拟环境
└── README.md
```

## 功能模块

### 一级菜单
1. **首页** - 系统概览和统计信息
2. **我的就业** - 个人就业状态和进度
3. **就业市场** - 职位浏览和搜索
4. **申请与管理** - 求职申请管理
5. **系统管理** - 后台管理功能
6. **个人中心** - 用户信息管理
7. **我的反馈** - 用户反馈系统

### 用户角色
- **学生**: 浏览职位、投递简历、管理申请
- **企业HR**: 发布职位、筛选简历、管理招聘
- **管理员**: 系统管理、用户管理、数据统计
- **超级管理员**: 全系统权限管理

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 开发规范
- 遵循RESTful API设计原则
- 使用JWT进行身份认证
- 实现RBAC权限控制
- 前后端完全分离
- 统一错误处理和响应格式

## 部署说明
详见 `docs/deployment.md`

## 贡献指南
详见 `docs/contributing.md`
