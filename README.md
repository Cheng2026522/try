# 🏗️ 建设集团管理系统

基于 Vue3 + Django 的企业级管理系统，提供文件管理、AI分析、用户管理等功能。

## 📋 技术栈

### 前端
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **UI组件**: Element Plus
- **状态管理**: Vuex
- **路由**: Vue Router
- **HTTP客户端**: Axios

### 后端
- **框架**: Django 6.0.4
- **API**: Django REST Framework
- **任务队列**: Celery + RabbitMQ
- **数据库**: SQLite (开发环境) / PostgreSQL (生产环境)

## 🛠️ 环境要求

| 依赖 | 版本 |
|------|------|
| Python | >= 3.10 |
| Node.js | >= 18.0 |
| RabbitMQ | >= 3.9 |
| Redis | >= 6.0 |

## 📦 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Cheng2026522/try.git
cd try
```

### 2. 后端环境配置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv Group_env

# 激活虚拟环境 (Windows)
Group_env\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source Group_env/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 3. 前端环境配置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

## 🚀 运行项目

### 启动后端服务

```bash
cd backend
Group_env\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

访问地址: http://localhost:8000

### 启动前端服务

```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 8084
```

访问地址: http://localhost:8084

### 启动Celery任务队列

```bash
cd backend
Group_env\Scripts\activate
celery -A project worker -l info
```

## 🌐 页面结构

| 页面 | 路径 | 说明 |
|------|------|------|
| 登录页面 | /login | 用户登录入口 |
| 仪表盘 | / | 系统首页/数据统计 |
| 文件管理 | /files | 文件上传、下载、分类 |
| AI分析 | /ai-analysis | 文档AI分析功能 |
| 用户管理 | /users | 用户CRUD（管理员权限） |

## 🔌 API接口

### 用户认证
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login/` | POST | 用户登录 |
| `/api/auth/register/` | POST | 用户注册 |
| `/api/auth/users/` | GET | 获取用户列表 |

### 文件管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/files/files/` | GET/POST | 文件列表/上传 |
| `/api/files/categories/` | GET/POST | 文件分类管理 |

### AI分析
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/results/` | GET | 分析结果列表 |
| `/api/ai/results/analyze/` | POST | 执行AI分析 |
| `/api/ai/history/` | GET | 分析历史记录 |

## 📁 项目结构

```
try/
├── backend/                    # Django后端
│   ├── apps/                  # 应用模块
│   │   ├── user_auth/         # 用户认证模块
│   │   ├── file_management/   # 文件管理模块
│   │   ├── ai_analysis/       # AI分析模块
│   │   └── links/             # 链接导航模块
│   ├── project/               # 项目配置
│   ├── manage.py              # Django管理命令
│   └── requirements.txt       # Python依赖
├── frontend/                  # Vue3前端
│   ├── src/                   # 源代码
│   │   ├── views/             # 页面组件
│   │   ├── components/        # 公共组件
│   │   ├── store/             # Vuex状态管理
│   │   ├── router/            # 路由配置
│   │   └── utils/             # 工具函数
│   ├── index.html             # HTML入口
│   ├── package.json           # Node依赖
│   └── vite.config.js         # Vite配置
├── .gitignore                 # Git忽略配置
└── README.md                  # 项目说明
```

## 👥 Git协作流程

### 分支规范

| 分支类型 | 命名规则 | 说明 |
|----------|----------|------|
| 主分支 | `master` | 生产环境代码 |
| 开发分支 | `develop` | 开发集成分支 |
| 功能分支 | `feature/*` | 新功能开发 |
| 修复分支 | `bugfix/*` | Bug修复 |

### 开发流程

```bash
# 1. 拉取最新代码
git checkout master
git pull origin master

# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 开发并提交代码
git add .
git commit -m "feat: add new feature"

# 4. 推送到远程分支
git push origin feature/new-feature

# 5. 创建Pull Request到develop分支
```

### 提交规范

```
feat: 新增功能
fix: 修复Bug
docs: 更新文档
style: 代码格式
refactor: 代码重构
test: 添加测试
chore: 构建/工具更新
```

## 🔐 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin |

## ⚙️ 管理后台

| 后台 | 地址 |
|------|------|
| Django Admin | http://localhost:8000/admin/ |
| RabbitMQ | http://localhost:15672/ (guest/guest) |
| 链接导航 | http://localhost:8000/ |

## ❓ 常见问题

### Q: 前端无法登录？
A: 请确保后端服务正常运行，检查CSRF配置，确认用户名密码正确。

### Q: 文件上传失败？
A: 检查文件大小限制（默认10MB），确保uploads目录有写入权限。

### Q: AI分析无响应？
A: 检查RabbitMQ服务是否启动，确保Celery worker正在运行。

## 📞 联系方式

如有问题请联系项目管理员。

---

*建设集团管理系统 v1.0*
