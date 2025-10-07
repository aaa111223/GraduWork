# 学生就业管理平台

## 项目概述
基于前后端分离架构的学生就业管理平台，为学生、企业HR和管理员提供完整的就业服务解决方案。支持多角色权限管理、职位发布与申请、简历管理、数据统计等核心功能。

## 技术栈

### 后端技术
- **框架**: Django 5.2.6 + Django REST Framework 3.16.1
- **数据库**: SQLite3 (开发环境) / MySQL 8.0 (生产环境)
- **认证**: JWT (JSON Web Token) + Simple JWT 5.5.1
- **权限**: RBAC (基于角色的访问控制)
- **密码加密**: Bcrypt 4.3.0
- **API**: RESTful API
- **跨域**: Django CORS Headers 4.9.0
- **过滤**: Django Filter 25.2
- **图像处理**: Pillow 11.3.0
- **配置管理**: Python Decouple 3.8

### 前端技术
- **框架**: Vue 3.5.18 (Composition API)
- **构建工具**: Vite 7.0.6
- **UI组件库**: Element Plus 2.11.3
- **图标库**: Element Plus Icons Vue 2.3.2
- **状态管理**: Pinia 3.0.3
- **路由**: Vue Router 4.5.1
- **HTTP客户端**: Axios 1.12.2
- **代码规范**: ESLint 9.31.0
- **开发工具**: Vue DevTools 8.0.0

## 项目架构

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (Vue3)   │    │  后端 (Django)  │    │  数据库 (SQLite) │
│                 │    │                 │    │                 │
│ • Element Plus  │◄──►│ • REST API      │◄──►│ • 用户数据       │
│ • Pinia Store   │    │ • JWT 认证      │    │ • 职位数据       │
│ • Vue Router    │    │ • RBAC 权限     │    │ • 申请数据       │
│ • Axios HTTP    │    │ • Django Filter │    │ • 反馈数据       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 目录结构
```
GraduWork/
├── backend/                    # Django后端项目
│   ├── employment_platform/    # 主项目配置
│   │   ├── settings.py        # 项目设置
│   │   ├── urls.py            # 主路由配置
│   │   └── wsgi.py            # WSGI配置
│   ├── apps/                  # 应用模块
│   │   ├── authentication/    # 用户认证模块
│   │   ├── users/             # 用户管理模块
│   │   ├── jobs/              # 职位管理模块
│   │   ├── applications/      # 申请管理模块
│   │   ├── feedback/          # 反馈系统模块
│   │   └── admin_management/  # 管理员功能模块
│   ├── requirements.txt       # Python依赖包
│   ├── manage.py             # Django管理脚本
│   └── db.sqlite3            # SQLite数据库文件
├── frontend/                  # Vue3前端项目
│   ├── src/
│   │   ├── components/        # 公共组件
│   │   │   └── Layout/        # 布局组件
│   │   ├── views/             # 页面组件
│   │   │   ├── HomeView.vue           # 首页
│   │   │   ├── LoginView.vue          # 登录页
│   │   │   ├── RegisterView.vue       # 注册页
│   │   │   ├── JobMarketView.vue      # 就业市场
│   │   │   ├── MyEmploymentView.vue   # 我的就业
│   │   │   ├── ApplicationsView.vue   # 申请管理
│   │   │   ├── ProfileView.vue        # 个人中心
│   │   │   ├── FeedbackView.vue       # 反馈系统
│   │   │   ├── SystemManagementView.vue    # 系统管理
│   │   │   └── RecruitmentManagementView.vue # 招聘管理
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia状态管理
│   │   ├── utils/             # 工具函数
│   │   └── assets/            # 静态资源
│   ├── package.json          # 前端依赖配置
│   ├── vite.config.js        # Vite构建配置
│   └── eslint.config.js      # ESLint配置
├── .venv/                    # Python虚拟环境
├── docs/                     # 项目文档
└── README.md                 # 项目说明
```

## 功能模块

### 核心功能
1. **用户认证系统**
   - 用户注册/登录 (JWT认证)
   - 多角色权限管理 (RBAC)
   - 密码加密存储 (Bcrypt)

2. **职位管理系统**
   - 职位发布与编辑
   - 职位分类管理
   - 职位搜索与过滤
   - 职位收藏功能

3. **申请管理系统**
   - 简历投递
   - 申请状态跟踪
   - 面试安排
   - 录用通知

4. **用户管理系统**
   - 学生档案管理
   - 企业信息管理
   - 用户权限控制
   - 账户状态管理

5. **数据统计系统**
   - 就业统计分析
   - 企业招聘统计
   - 系统使用统计
   - 数据可视化展示

6. **反馈系统**
   - 用户反馈收集
   - 系统通知推送
   - 问题处理跟踪

### 用户角色与权限

#### 🎓 学生用户
- **就业市场**: 浏览职位、搜索筛选、查看详情
- **申请管理**: 投递简历、查看申请状态、管理面试
- **个人中心**: 完善个人信息、上传简历、查看统计
- **反馈系统**: 提交反馈、查看系统通知

#### 🏢 企业HR用户
- **招聘管理**: 发布职位、编辑职位、管理招聘流程
- **简历筛选**: 查看申请简历、筛选候选人、安排面试
- **企业统计**: 查看招聘数据、分析招聘效果
- **企业信息**: 管理企业资料、更新企业信息

#### 👨‍💼 管理员用户
- **系统管理**: 用户管理、职位审核、数据统计
- **用户管理**: 查看所有用户、管理用户状态、权限分配
- **职位管理**: 审核职位、管理职位分类、处理举报
- **反馈管理**: 处理用户反馈、发布系统通知

#### 🔧 超级管理员
- **全系统权限**: 所有功能的完整访问权限
- **系统配置**: 系统参数配置、安全设置
- **数据管理**: 数据备份、系统维护

## 快速开始

### 环境要求
- **Python**: 3.10+ (推荐 3.11)
- **Node.js**: 20.19.0+ 或 22.12.0+
- **数据库**: SQLite3 (开发) / MySQL 8.0+ (生产)
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 20.04+

### 安装与运行

#### 1. 克隆项目
```bash
git clone https://github.com/aaa111223/GraduWork.git
cd GraduWork
```

#### 2. 后端环境配置
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate
# 激活虚拟环境 (macOS/Linux)
source .venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户 (可选)
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver
```

#### 3. 前端环境配置
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 4. 访问系统
- **前端地址**: http://localhost:5173/
- **后端API**: http://localhost:8000/api/
- **管理后台**: http://localhost:8000/admin/

### 默认测试账户
系统提供以下测试账户用于快速体验：

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 学生 | student | 123456 | 学生用户测试账户 |
| 企业HR | hr | 123456 | 企业HR测试账户 |
| 管理员 | admin | 123456 | 管理员测试账户 |

## 开发规范

### 后端开发规范
- **API设计**: 遵循RESTful API设计原则
- **认证方式**: 使用JWT进行身份认证
- **权限控制**: 实现RBAC基于角色的访问控制
- **数据验证**: 使用Django REST Framework序列化器
- **错误处理**: 统一错误响应格式
- **代码风格**: 遵循PEP 8 Python编码规范

### 前端开发规范
- **组件化**: 使用Vue 3 Composition API
- **状态管理**: 使用Pinia进行状态管理
- **UI规范**: 基于Element Plus设计系统
- **路由管理**: 使用Vue Router 4进行页面路由
- **代码规范**: 使用ESLint进行代码检查
- **响应式设计**: 支持桌面端和移动端适配

### API接口规范
```javascript
// 成功响应格式
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 错误响应格式
{
  "code": 400,
  "message": "error message",
  "errors": { ... }
}
```

## 部署说明

### 开发环境部署
- 使用SQLite3数据库
- Django开发服务器 (端口8000)
- Vite开发服务器 (端口5173)

### 生产环境部署
- 使用MySQL/PostgreSQL数据库
- Nginx + Gunicorn部署Django
- 静态文件CDN部署
- HTTPS安全配置

详细部署文档请参考 `docs/deployment.md`

## 项目特色

### 🚀 技术亮点
- **现代化技术栈**: Vue 3 + Django 5 + Element Plus
- **响应式设计**: 支持桌面端和移动端
- **权限管理**: 完整的RBAC权限控制系统
- **数据可视化**: 丰富的统计图表展示
- **实时更新**: 基于WebSocket的实时通知

### 🎯 功能亮点
- **智能搜索**: 支持多条件职位搜索和过滤
- **简历管理**: 在线简历编辑和投递系统
- **数据统计**: 全面的就业和招聘数据分析
- **消息通知**: 实时的申请状态和系统通知
- **移动适配**: 完整的移动端用户体验

## 贡献指南

### 如何贡献
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发流程
1. 在Issues中讨论新功能或bug修复
2. 遵循项目的代码规范和提交规范
3. 确保所有测试通过
4. 更新相关文档

详细贡献指南请参考 `docs/contributing.md`

## 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式
- **项目维护者**: wei lee
- **邮箱**: 30249604@qq.com
- **GitHub**: [@aaa111223](https://github.com/aaa111223)

---
⭐ 如果这个项目对你有帮助，请给它一个星标！
