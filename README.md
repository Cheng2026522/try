# 建设集团管理系统

基于 Vue 3 + Django 6.0.4 的前后端分离企业管理系统。

## 🛠️ 技术栈

| 分类 | 技术 | 版本 |
| :--- | :--- | :--- |
| 前端框架 | Vue | 3.x |
| 前端构建 | Vite | 6.x |
| UI 组件 | Element Plus | - |
| 状态管理 | Vuex | - |
| 路由 | Vue Router | - |
| 后端框架 | Django | 6.0.4 |
| API 框架 | Django REST Framework | - |
| 任务队列 | Celery | - |
| 数据库 | MySQL | 5.7+/8.x |
| 消息代理 | RabbitMQ | - |

## 📁 项目结构

```
tare_project/
├── backend/                    # Django 后端服务
│   ├── apps/
│   │   ├── user_auth/          # 用户认证模块
│   │   │   ├── models.py       # 自定义用户模型
│   │   │   ├── views.py        # 登录/注册接口
│   │   │   └── admin.py        # 用户管理后台
│   │   ├── file_management/    # 文件管理模块
│   │   │   ├── models.py       # 文件/分类模型
│   │   │   ├── views.py        # 文件上传/下载接口
│   │   │   └── admin.py        # 文件管理后台
│   │   ├── ai_analysis/        # AI 分析模块
│   │   │   ├── models.py       # 分析结果模型
│   │   │   ├── views.py        # AI 分析接口
│   │   │   ├── tasks.py        # Celery 异步任务
│   │   │   └── admin.py        # 分析管理后台
│   │   └── links/              # 链接导航模块
│   │       └── views.py        # 系统链接汇总页面
│   ├── project/                # Django 配置
│   │   ├── settings.py         # 项目配置
│   │   └── urls.py             # 路由配置
│   ├── manage.py               # Django 管理命令
│   └── requirements.txt        # Python 依赖
├── frontend/                   # Vue 前端应用
│   ├── src/
│   │   ├── views/              # 页面组件
│   │   │   ├── DirectLogin.vue # 登录页面
│   │   │   ├── Dashboard.vue   # 仪表盘首页
│   │   │   ├── FileManagement.vue # 文件管理
│   │   │   ├── AIAnalysis.vue  # AI 分析
│   │   │   └── UserManagement.vue # 用户管理
│   │   ├── components/         # 公共组件
│   │   │   ├── Header.vue      # 顶部导航
│   │   │   └── Sidebar.vue     # 侧边栏
│   │   ├── store/              # Vuex 状态管理
│   │   ├── router/             # 路由配置
│   │   └── utils/              # 工具函数
│   └── package.json            # Node.js 依赖
├── start_backend.bat           # 后端一键启动脚本
├── start_frontend.bat          # 前端一键启动脚本
└── README.md                   # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 5.7+ 或 8.x
- RabbitMQ 3.8+（可选，用于异步任务）

### 启动步骤

#### 1. 克隆项目

```bash
git clone https://github.com/Cheng2026522/try.git
cd try
```

#### 2. 启动后端服务

**方式一：使用启动脚本（推荐）**

```bash
# Windows
start_backend.bat
```

**方式二：手动启动**

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（首次运行）
python -m venv Group_env
Group_env\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

#### 3. 启动前端服务

**方式一：使用启动脚本（推荐）**

```bash
# Windows
start_frontend.bat
```

**方式二：手动启动**

```bash
# 进入前端目录
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

### 启动 Celery 异步任务（可选）

```bash
# 在 backend 目录下执行
celery -A project worker --loglevel=info
```

## 🔗 服务访问地址

| 服务 | 地址 | 说明 |
| :--- | :--- | :--- |
| 前端页面 | http://localhost:8084/ | Vue 开发服务器 |
| 后端 API | http://localhost:8000/ | Django REST API |
| 管理后台 | http://localhost:8000/admin/ | Django Admin |
| 链接导航 | http://localhost:8000/links/ | 系统链接汇总页面 |
| RabbitMQ | http://localhost:15672/ | 消息队列管理 |

## 👤 测试账号

| 角色 | 用户名 | 密码 | 联系电话 |
| :--- | :--- | :--- | :--- |
| 管理员 | admin | admin | 13800138000 |

## 📡 API 接口说明

### 用户认证

| 接口 | 方法 | 路径 | 说明 |
| :--- | :--- | :--- | :--- |
| 用户登录 | POST | `/api/auth/login/` | 用户名密码登录 |
| 用户注册 | POST | `/api/auth/register/` | 新用户注册 |
| 用户列表 | GET | `/api/auth/users/` | 获取用户列表（管理员） |
| 用户详情 | GET | `/api/auth/users/{id}/` | 获取用户详情 |

### 文件管理

| 接口 | 方法 | 路径 | 说明 |
| :--- | :--- | :--- | :--- |
| 文件列表 | GET | `/api/files/files/` | 获取文件列表 |
| 文件上传 | POST | `/api/files/files/` | 上传文件 |
| 文件下载 | GET | `/api/files/download/{id}/` | 下载文件 |
| 文件删除 | DELETE | `/api/files/files/{id}/` | 删除文件 |
| 分类列表 | GET | `/api/files/categories/` | 获取分类列表 |
| 分类创建 | POST | `/api/files/categories/` | 创建分类 |

### AI 分析

| 接口 | 方法 | 路径 | 说明 |
| :--- | :--- | :--- | :--- |
| 分析列表 | GET | `/api/ai/results/` | 获取分析结果 |
| 开始分析 | POST | `/api/ai/results/analyze/` | 对文件进行 AI 分析 |
| 分析问答 | POST | `/api/ai/results/{id}/qa/` | 智能问答 |
| 选择版本 | POST | `/api/ai/results/{id}/select_version/` | 选择分析版本 |

## 🔧 配置说明

### 数据库配置

修改 `backend/project/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'construction_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}
```

### CORS 配置

```python
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost:8084',
]
```

## 📝 开发说明

1. **前端开发**：进入 `frontend` 目录，运行 `npm run dev` 启动开发服务器
2. **后端开发**：进入 `backend` 目录，运行 `python manage.py runserver` 启动开发服务器
3. **数据库迁移**：修改模型后，运行 `python manage.py makemigrations` 和 `python manage.py migrate`
4. **代码提交**：使用 Git 管理代码，提交前请确保代码通过测试

## 📄 许可证

MIT License

---

**建设集团管理系统 v1.0** | 最后更新：2026-06-03