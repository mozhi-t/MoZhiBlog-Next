# MoZhi Blog

一个前后端分离的个人博客项目。

前端基于 `Vue 3 + Vite + Pinia + Vue Router`，后端基于 `FastAPI + SQLAlchemy + MySQL`。项目包含公开博客页面、后台管理系统、文章分类/标签管理、说说管理、友链管理，以及支持 Markdown 编辑与预览的文章发布能力。

## 项目特性

- 博客首页、归档、分类、标签、搜索、文章详情等前台页面
- 后台登录与管理面板
- 文章管理：新建、编辑、删除、置顶、密码访问
- Markdown 编辑器与实时预览
- 分类、标签、友链、说说管理
- 热门文章统计
- Sitemap 接口
- 基于 JWT 的后台鉴权
- 登录失败次数限制与黑名单机制

## 技术栈

### 前端

- Vue 3
- Vite
- Pinia
- Vue Router
- Axios
- Marked
- Highlight.js
- Sass

### 后端

- FastAPI
- SQLAlchemy
- PyMySQL
- Pydantic
- Python-Dotenv
- Passlib / Bcrypt
- Uvicorn

## 目录结构

```text
mozhiblog-next/
├─ src/                     # Vue 前端源码
│  ├─ api/                  # 接口封装
│  ├─ components/           # 公共组件
│  ├─ config/               # 站点配置
│  ├─ router/               # 路由
│  ├─ stores/               # Pinia 状态管理
│  ├─ styles/               # 全局样式与 Markdown 样式
│  └─ views/                # 页面与后台页面
├─ public/                  # 静态资源
├─ backend/                 # FastAPI 后端
│  ├─ routes/               # 路由模块
│  ├─ sql/                  # 示例 SQL
│  ├─ auth.py               # 鉴权逻辑
│  ├─ config.py             # 后端配置
│  ├─ init_db.py            # 数据库初始化脚本
│  ├─ main.py               # 应用入口
│  ├─ models.py             # SQLAlchemy 模型
│  ├─ requirements.txt      # Python 依赖
│  └─ schemas.py            # Pydantic 模型
├─ dist/                    # 前端构建产物
├─ logs/                    # 运行日志
└─ README.md
```

## 核心功能说明

### 前台功能

- 首页文章列表
- 文章详情页
- 分类页、标签页、归档页
- 搜索页
- 友链页
- 说说页
- 自定义关于页

### 后台功能

- 管理员登录
- 仪表盘
- 文章管理与 Markdown 编辑
- 分类管理
- 标签管理
- 说说管理
- 友链管理
- 账号设置

## 环境要求

### 前端

- Node.js `^20.19.0 || >=22.12.0`
- npm

### 后端

- Python `3.10+` 建议
- MySQL `5.7+` 或 `8.0+`

## 本地开发

### 1. 安装前端依赖

```bash
npm install
```

### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置后端环境变量

在 `backend/` 目录新建 `.env` 文件：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=mozhiblog

JWT_SECRET=replace-with-your-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=2

CORS_ORIGINS=http://localhost:5173,http://localhost:5174
SITE_URL=https://blog.mozhi.top
API_PORT=8008

LOG_LEVEL=INFO
LOG_DIR=
LOG_BACKUP_COUNT=30
```

### 4. 初始化数据库

```bash
cd backend
python init_db.py
```

初始化脚本会自动：

- 创建数据库（如果不存在）
- 创建数据表
- 写入默认管理员
- 写入示例分类、标签、文章、友链数据

默认后台账号：

- 用户名：`admin`
- 密码：`123456`

### 5. 启动后端

```bash
cd backend
python main.py
```

后端默认地址：

- API 根地址：`http://localhost:8008`
- Swagger 文档：`http://localhost:8008/docs`
- ReDoc：`http://localhost:8008/redoc`

### 6. 启动前端

```bash
npm run dev
```

前端开发服务默认地址：

- 博客前台：`http://localhost:5173`
- 后台登录页：`http://localhost:5173/admin/login`

开发环境下，Vite 会把 `/api` 与 `/sitemap.xml` 代理到 `http://localhost:8008`。

## 前端环境变量

项目当前会读取以下前端环境变量：

```env
VITE_SITE_URL=https://blog.mozhi.top
VITE_API_BASE_URL=/api
VITE_TWIKOO_ENV_ID=https://twikoo-api.mozhix.top/
```

说明：

- `VITE_SITE_URL`：前端站点地址，用于 SEO 等场景
- `VITE_API_BASE_URL`：接口基地址
- `VITE_TWIKOO_ENV_ID`：Twikoo 评论服务地址

## 数据模型概要

### 管理员 `admin`

- 用户名
- 密码
- 邮箱
- 创建时间

### 文章 `article`

- 标题
- 摘要
- Markdown 正文
- 分类 ID
- 标签 ID 列表（逗号分隔）
- 类型
- 访问密码
- 阅读数
- 创建时间
- 更新时间

文章类型说明：

- `0`：普通文章
- `1`：置顶文章
- `2`：密码访问文章

### 分类 `category`

- 名称
- 创建时间

### 标签 `tag`

- 名称
- 创建时间

### 说说 `moment`

- 内容
- 访问密码
- 创建时间

### 友链 `friend_link`

- 名称
- 描述
- 头像
- 链接
- 是否展示
- 权重

## 文章发布方式

这个项目的文章不是存放在本地 Markdown 文件夹中，而是存进 MySQL 数据库。

发布流程如下：

1. 启动前后端服务
2. 打开后台 `http://localhost:5173/admin/login`
3. 使用管理员账号登录
4. 进入“文章管理”
5. 新建文章
6. 填写标题、摘要、分类、标签、文章类型、时间
7. 在正文区域直接编写 Markdown
8. 保存后文章写入数据库并在前台展示

如果你想先在本地准备文章内容，再复制进后台编辑器，可以使用 [docs/blog-post-template.md](docs/blog-post-template.md)。

## Markdown 支持说明

文章编辑器支持 Markdown，前端会对正文进行渲染，并增强代码块显示。适合编写：

- 技术教程
- 学习笔记
- 项目复盘
- 生活随笔

建议正文至少包含：

- 一级标题
- 导语
- 2 到 4 个二级标题
- 代码块或列表
- 总结

## 常用接口

### 后台鉴权

- `POST /api/admin/login`
- `GET /api/admin/me`
- `POST /api/admin/logout`
- `PUT /api/admin/settings`

### 文章

- `GET /api/articles`
- `GET /api/articles/hot`
- `GET /api/articles/{id}`
- `GET /api/articles/{id}/reference`
- `POST /api/articles`
- `PUT /api/articles/{id}`
- `DELETE /api/articles/{id}`
- `POST /api/articles/{id}/verify-password`

### 分类 / 标签 / 友链 / 说说

- `GET /api/categories`
- `GET /api/tags`
- `GET /api/friend_links`
- `GET /api/moments`

具体请求参数与返回结构建议直接查看 Swagger 文档。

## 生产构建

### 构建前端

```bash
npm run build
```

构建产物输出到 `dist/` 目录。

### 预览前端构建结果

```bash
npm run preview
```

### 后端生产启动示例

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8008
```

建议生产环境额外处理：

- 使用反向代理转发前端与 API
- 限制 CORS 来源
- 修改默认管理员密码
- 替换强随机 `JWT_SECRET`
- 使用正式 MySQL 账号
- 配置日志目录与备份策略

## 已知实现特点

- 标签字段当前以逗号分隔的 ID 字符串存储
- 文章与说说支持密码访问
- 登录失败达到上限后，来源 IP 会进入黑名单
- 热门文章列表基于阅读数排序

## 常见问题

### 1. 前端请求不到接口

检查：

- 后端是否已启动在 `8008`
- `VITE_API_BASE_URL` 是否正确
- 开发环境代理是否生效

### 2. 初始化数据库失败

检查：

- MySQL 是否启动
- `backend/.env` 中数据库账号密码是否正确
- 当前账号是否有建库建表权限

### 3. 后台无法登录

检查：

- 是否使用 `admin / 123456`
- 是否曾连续输错密码导致 IP 被拉黑
- 数据库中 `admin` 表是否已有管理员数据

## 后续可扩展方向

- 上传封面图与媒体资源
- 文章草稿 / 发布状态
- 评论管理后台
- RSS 自动生成
- Docker 化部署
- 自动化测试
- CI/CD 发布流程

## 文档补充

- 项目总说明：当前文件 `README.md`
- 博客发布模板：[docs/blog-post-template.md](docs/blog-post-template.md)
