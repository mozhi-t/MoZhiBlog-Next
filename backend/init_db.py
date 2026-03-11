"""
Database Init Script - 数据库初始化脚本
创建表并插入测试数据
"""
import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import config
from models import Base, Admin, Category, Tag, Article, Comment, FriendLink, Blacklist, MessageBoard
from auth import get_password_hash

# 创建数据库引擎
engine = create_engine(config.DATABASE_URL, echo=False)


def init_database():
    """初始化数据库"""
    print("=" * 50)
    print("开始初始化数据库...")
    print("=" * 50)

    # 创建数据库（如果不存在）
    db_name = config.DB_NAME
    temp_engine = create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}",
        echo=False
    )

    with temp_engine.connect() as conn:
        # 创建数据库
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()
        print(f"✓ 数据库 '{db_name}' 创建成功")

    temp_engine.dispose()

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✓ 所有数据表创建成功")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # ==================== 插入测试数据 ====================

        # 1. 插入管理员 (admin/123456)
        admin = Admin(
            username="admin",
            password=get_password_hash("123456"),
            email="admin@mozhiblog.com",
            create_time=datetime.now()
        )
        session.add(admin)
        print("✓ 插入管理员: admin / 123456")

        # 2. 插入分类
        categories_data = [
            {"name": "技术"},
            {"name": "设计"},
            {"name": "生活"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category(name=cat_data["name"], create_time=datetime.now())
            session.add(category)
            categories.append(category)

        session.flush()  # 获取分类ID
        print(f"✓ 插入 {len(categories_data)} 个分类")

        # 3. 插入标签
        tags_data = [
            {"name": "Vue3"},
            {"name": "前端"},
            {"name": "TypeScript"},
            {"name": "UI"},
            {"name": "UX"},
            {"name": "生活"},
            {"name": "自我成长"},
            {"name": "React"},
            {"name": "Node.js"},
            {"name": "Python"},
            {"name": "AI"},
            {"name": "产品"},
        ]

        tags = []
        for tag_data in tags_data:
            tag = Tag(name=tag_data["name"], create_time=datetime.now())
            session.add(tag)
            tags.append(tag)

        session.flush()  # 获取标签ID
        print(f"✓ 插入 {len(tags_data)} 个标签")

        # 4. 插入50篇文章，每篇有不同的创建和更新时间
        base_time = datetime(2024, 1, 1, 0, 0, 0)

        articles_data = [
            {
                "title": "探索 Vue 3 Composition API 的最佳实践",
                "summary": "深入理解 Vue 3 的 Composition API，学习如何编写更清晰、可维护的组件代码。",
                "content": """# 探索 Vue 3 Composition API 的最佳实践

Vue 3 引入了 Composition API，这是一项重大的架构改进。本文将深入探讨如何有效使用 Composition API 来构建可维护的应用。

## 什么是 Composition API？

Composition API 是 Vue 3 引入的一组 API，允许我们以更灵活的方式组织组件逻辑。相比于 Options API，Composition API 提供了更好的逻辑复用和代码组织能力。

## 核心 API

### setup()

`setup()` 是 Composition API 的入口点，它在组件创建之前执行，只会被调用一次。

```javascript
import { ref, computed } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    return { count, doubled }
  }
}
```

## 最佳实践

1. **使用组合函数复用逻辑**：将相关逻辑封装成可复用的函数
2. **保持代码简洁**：避免在 `setup()` 中编写过多逻辑
3. **合理组织代码**：按功能而非选项类型组织代码

## 总结

Composition API 为 Vue 应用带来了更好的代码组织和逻辑复用能力。
""",
                "category_id": categories[0].id,
                "tags": f"{tags[0].id},{tags[1].id}",
                "type": 0,
                "read_count": 128
            },
            {
                "title": "TypeScript 类型系统详解",
                "summary": "全面解析 TypeScript 的高级类型特性，提升代码类型安全。",
                "content": """# TypeScript 类型系统详解

TypeScript 的类型系统是其最强大的特性之一。本文将全面解析 TypeScript 的高级类型特性。

## 基础类型

```typescript
let name: string = "MoZhi"
let age: number = 25
let isDeveloper: boolean = true
```

## 高级类型

### 1. 联合类型
### 2. 交叉类型
### 3. 泛型

## 总结

掌握 TypeScript 的类型系统可以显著提升代码质量和可维护性。
""",
                "category_id": categories[0].id,
                "tags": f"{tags[2].id},{tags[1].id}",
                "type": 0,
                "read_count": 167
            },
            {
                "title": "React Hooks 深入理解",
                "summary": "从原理到实践，全面掌握 React Hooks 的使用技巧。",
                "content": """# React Hooks 深入理解

React Hooks 是 React 16.8 引入的新特性，让我们可以在不编写类组件的情况下使用状态和其他 React 特性。

## 常用 Hooks

### useState
### useEffect
### useContext

## 自定义 Hooks

通过自定义 Hooks 可以复用组件逻辑。
""",
                "category_id": categories[0].id,
                "tags": f"{tags[7].id},{tags[1].id}",
                "type": 0,
                "read_count": 234
            },
            {
                "title": "Node.js 性能优化实战",
                "summary": "分享 Node.js 应用性能优化的实用技巧和最佳实践。",
                "content": """# Node.js 性能优化实战

本文介绍如何优化 Node.js 应用的性能。

## 1. 异步编程
## 2. 缓存策略
## 3. 集群模式
## 4. 内存管理
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[1].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "Python 异步编程详解",
                "summary": "深入理解 Python 的 asyncio 模块和异步编程模式。",
                "content": """# Python 异步编程详解

异步编程是现代 Python 开发的重要技能。

## async/await
## asyncio 模块
## 异步上下文管理器
""",
                "category_id": categories[0].id,
                "tags": f"{tags[9].id},{tags[1].id}",
                "type": 0,
                "read_count": 156
            },
            {
                "title": "AI 大模型应用开发指南",
                "summary": "介绍如何基于 AI 大模型开发实用应用。",
                "content": """# AI 大模型应用开发指南

探索如何利用 AI 大模型构建智能应用。

## API 调用
## 提示工程
## 应用架构
""",
                "category_id": categories[0].id,
                "tags": f"{tags[10].id},{tags[1].id}",
                "type": 0,
                "read_count": 312
            },
            {
                "title": "设计系统的美学",
                "summary": "分析苹果设计系统的核心原则，探讨如何打造简洁优雅的用户界面。",
                "content": """# 设计系统的美学

苹果公司以其卓越的设计而闻名于世。

## 核心原则

### 1. 简洁性
### 2. 一致性
### 3. 反馈
""",
                "category_id": categories[1].id,
                "tags": f"{tags[3].id},{tags[4].id}",
                "type": 0,
                "read_count": 256
            },
            {
                "title": "用户体验设计原则",
                "summary": "分享提升用户体验的设计思路和实践方法。",
                "content": """# 用户体验设计原则

好的用户体验是产品成功的关键。

## 可用性
## 可访问性
## 情感设计
""",
                "category_id": categories[1].id,
                "tags": f"{tags[4].id},{tags[3].id}",
                "type": 0,
                "read_count": 198
            },
            {
                "title": "UI 动效设计指南",
                "summary": "学习如何设计流畅自然的界面动效。",
                "content": """# UI 动效设计指南

动效是提升用户体验的重要元素。

## 动效原则
## 实现技术
## 性能优化
""",
                "category_id": categories[1].id,
                "tags": f"{tags[3].id},{tags[1].id}",
                "type": 0,
                "read_count": 145
            },
            {
                "title": "色彩心理学在设计中的应用",
                "summary": "探讨颜色如何影响用户的感知和行为。",
                "content": """# 色彩心理学在设计中的应用

颜色是设计中最强有力的工具之一。

## 色彩基础
## 情感联想
## 实际应用
""",
                "category_id": categories[1].id,
                "tags": f"{tags[3].id},{tags[4].id}",
                "type": 0,
                "read_count": 176
            },
            {
                "title": "在忙碌的生活中寻找平衡",
                "summary": "分享关于时间管理，心态调整的思考与实践。",
                "content": """# 在忙碌的生活中寻找平衡

现代生活节奏越来越快，我们常常感到时间不够用。

## 认识自己
## 时间管理技巧
## 身心健康
""",
                "category_id": categories[2].id,
                "tags": f"{tags[5].id},{tags[6].id}",
                "type": 0,
                "read_count": 89
            },
            {
                "title": "极简主义：少即是多",
                "summary": "探讨极简主义生活方式带来的内心平静与效率提升。",
                "content": """# 极简主义：少即是多

极简主义不仅仅是一种设计风格，更是一种生活方式。

## 什么是极简主义？
## 实践步骤
## 心理益处
""",
                "category_id": categories[2].id,
                "tags": f"{tags[6].id},{tags[5].id}",
                "type": 0,
                "read_count": 203
            },
            {
                "title": "晨间习惯的科学",
                "summary": "如何通过优化晨间习惯提升一天的生产力。",
                "content": """# 晨间习惯的科学

清晨的习惯决定了整天的状态。

## 早起的好处
## 晨间仪式
## 能量管理
""",
                "category_id": categories[2].id,
                "tags": f"{tags[6].id},{tags[5].id}",
                "type": 0,
                "read_count": 167
            },
            {
                "title": "深度工作的艺术",
                "summary": "在 distractions 盛行的时代，如何培养深度工作的能力。",
                "content": """# 深度工作的艺术

深度工作是在无干扰状态下进行专业活动的的能力。

## 什么是深度工作？
## 障碍与解决方案
## 实践方法
""",
                "category_id": categories[2].id,
                "tags": f"{tags[6].id},{tags[1].id}",
                "type": 0,
                "read_count": 245
            },
            {
                "title": "阅读的力量",
                "summary": "为什么阅读是自我提升的最佳方式之一。",
                "content": """# 阅读的力量

阅读是人类进步的阶梯。

## 阅读的好处
## 如何养成阅读习惯
## 推荐书目
""",
                "category_id": categories[2].id,
                "tags": f"{tags[6].id},{tags[5].id}",
                "type": 0,
                "read_count": 134
            },
            {
                "title": "Vue 3 响应式原理深入解析",
                "summary": "深入理解 Vue 3 的响应式系统工作原理。",
                "content": """# Vue 3 响应式原理深入解析

Vue 3 的响应式系统是其核心特性之一。

## Proxy vs Object.defineProperty
## 依赖收集
## 触发更新
""",
                "category_id": categories[0].id,
                "tags": f"{tags[0].id},{tags[1].id}",
                "type": 0,
                "read_count": 287
            },
            {
                "title": "前端工程化实践",
                "summary": "从零搭建现代化的前端开发环境。",
                "content": """# 前端工程化实践

前端工程化是提升开发效率的关键。

## 构建工具
## 代码规范
## 自动化测试
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 198
            },
            {
                "title": "CSS Grid 布局完全指南",
                "summary": "掌握 CSS Grid 构建复杂布局的艺术。",
                "content": """# CSS Grid 布局完全指南

CSS Grid 是现代布局的强大工具。

## 基础概念
## 网格模板
## 响应式设计
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 223
            },
            {
                "title": "JavaScript 异步编程进阶",
                "summary": "深入理解 Promise、async/await 和事件循环。",
                "content": """# JavaScript 异步编程进阶

异步编程是 JavaScript 的核心概念。

## Promise
## async/await
## 事件循环
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 267
            },
            {
                "title": "微服务架构设计",
                "summary": "学习如何设计可靠的微服务系统。",
                "content": """# 微服务架构设计

微服务是现代后端开发的主流架构。

## 服务拆分
## 服务通信
## 故障处理
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[9].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "Docker 与 Kubernetes 实战",
                "summary": "掌握容器化技术和容器编排。",
                "content": """# Docker 与 Kubernetes 实战

容器技术是现代 DevOps 的基础。

## Docker 基础
## K8s 核心概念
## 部署实践
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[1].id}",
                "type": 0,
                "read_count": 234
            },
            {
                "title": "数据库设计与优化",
                "summary": "从理论到实践的数据库设计指南。",
                "content": """# 数据库设计与优化

良好的数据库设计是应用性能的基础。

## 规范化
## 索引优化
## 查询优化
""",
                "category_id": categories[0].id,
                "tags": f"{tags[9].id},{tags[8].id}",
                "type": 0,
                "read_count": 212
            },
            {
                "title": "API 设计最佳实践",
                "summary": "设计易用、可维护的 RESTful API。",
                "content": """# API 设计最佳实践

好的 API 设计能显著提升开发体验。

## RESTful 原则
## 版本控制
## 文档编写
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[1].id}",
                "type": 0,
                "read_count": 178
            },
            {
                "title": "产品经理的自我修养",
                "summary": "从技术转产品的心得与思考。",
                "content": """# 产品经理的自我修养

产品经理是连接技术与用户的桥梁。

## 用户思维
## 数据驱动
## 沟通协作
""",
                "category_id": categories[1].id,
                "tags": f"{tags[11].id},{tags[4].id}",
                "type": 0,
                "read_count": 156
            },
            {
                "title": "从 0 到 1 构建博客系统",
                "summary": "完整记录一个博客系统的开发历程。",
                "content": """# 从 0 到 1 构建博客系统

实战项目是提升技能的最佳方式。

## 技术选型
## 核心功能
## 部署上线
""",
                "category_id": categories[0].id,
                "tags": f"{tags[0].id},{tags[8].id},{tags[9].id}",
                "type": 0,
                "read_count": 345
            },
            {
                "title": "Git 协作流程指南",
                "summary": "团队开发中的 Git 工作流最佳实践。",
                "content": """# Git 协作流程指南

良好的 Git 协作流程能提升团队效率。

## 分支策略
## 提交规范
## 代码审查
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[8].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "Web 性能优化实战",
                "summary": "全面提升 Web 应用加载和运行性能。",
                "content": """# Web 性能优化实战

性能是用户体验的关键因素。

## 加载优化
## 渲染优化
## 资源优化
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 267
            },
            {
                "title": "函数式编程入门",
                "summary": "理解函数式编程的核心概念和优势。",
                "content": """# 函数式编程入门

函数式编程是一种强大的编程范式。

## 核心概念
## 函数组合
## 纯函数
""",
                "category_id": categories[0].id,
                "tags": f"{tags[2].id},{tags[1].id}",
                "type": 0,
                "read_count": 198
            },
            {
                "title": "代码可读性提升指南",
                "summary": "编写更容易理解和维护的代码。",
                "content": """# 代码可读性提升指南

可读性是代码质量的重要指标。

## 命名规范
## 函数设计
## 注释技巧
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[6].id}",
                "type": 0,
                "read_count": 234
            },
            {
                "title": "移动端适配完全指南",
                "summary": "解决移动端开发中的各种适配问题。",
                "content": """# 移动端适配完全指南

移动端适配是前端开发的重要技能。

## 视口设置
## 响应式布局
## 设备像素比
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 212
            },
            {
                "title": "网络安全基础",
                "summary": "Web 应用常见安全问题和防护措施。",
                "content": """# 网络安全基础

安全是 Web 开发中不可忽视的方面。

## XSS 攻击
## CSRF 防护
## HTTPS
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[8].id}",
                "type": 0,
                "read_count": 256
            },
            {
                "title": "测试驱动开发实践",
                "summary": "TDD 开发模式的完整指南。",
                "content": """# 测试驱动开发实践

TDD 能显著提升代码质量和信心。

## Red-Green-Refactor
## 测试金字塔
## mock 技术
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 178
            },
            {
                "title": "消息队列实战",
                "summary": "使用消息队列构建异步系统。",
                "content": """# 消息队列实战

消息队列是构建高并发系统的关键组件。

## 消息队列概念
## RabbitMQ 使用
## 最佳实践
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[9].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "缓存系统设计",
                "summary": "构建高效的缓存系统提升应用性能。",
                "content": """# 缓存系统设计

缓存是性能优化的利器。

## 缓存策略
## Redis 使用
## 缓存一致性
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[9].id}",
                "type": 0,
                "read_count": 223
            },
            {
                "title": "Elasticsearch 实战",
                "summary": "使用 Elasticsearch 构建全文搜索系统。",
                "content": """# Elasticsearch 实战

Elasticsearch 是强大的搜索和分析引擎。

## 核心概念
## 索引管理
## 查询语法
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[9].id}",
                "type": 0,
                "read_count": 167
            },
            {
                "title": "GraphQL 入门指南",
                "summary": "了解 GraphQL 的优势和适用场景。",
                "content": """# GraphQL 入门指南

GraphQL 是 RESTful API 的替代方案。

## 核心概念
##  schema 设计
## 与 REST 对比
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 198
            },
            {
                "title": "Serverless 架构实践",
                "summary": "无服务器架构的优势和挑战。",
                "content": """# Serverless 架构实践

Serverless 是云计算的新范式。

## FaaS 概念
## 优缺点分析
## 最佳实践
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[10].id}",
                "type": 0,
                "read_count": 234
            },
            {
                "title": "CI/CD  pipeline 设计",
                "summary": "构建高效的持续集成和持续部署流程。",
                "content": """# CI/CD pipeline 设计

自动化是 DevOps 的核心。

## 持续集成
## 持续部署
## 工具选择
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[1].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "Monorepo 实战指南",
                "summary": "使用 Monorepo 管理多项目代码库。",
                "content": """# Monorepo 实战指南

Monorepo 是管理大型代码库的方式。

## 工具对比
## 架构设计
## 工作流
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[8].id}",
                "type": 0,
                "read_count": 156
            },
            {
                "title": "TypeScript 装饰器详解",
                "summary": "深入理解 TypeScript 装饰器的使用。",
                "content": """# TypeScript 装饰器详解

装饰器是 TypeScript 的强大特性。

## 装饰器基础
## 类装饰器
## 方法装饰器
""",
                "category_id": categories[0].id,
                "tags": f"{tags[2].id},{tags[1].id}",
                "type": 0,
                "read_count": 167
            },
            {
                "title": "WebSocket 实时通信",
                "summary": "构建实时 Web 应用的完整指南。",
                "content": """# WebSocket 实时通信

WebSocket 实现了双向实时通信。

## 协议原理
## 实现方案
## 性能优化
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[8].id}",
                "type": 0,
                "read_count": 212
            },
            {
                "title": "PWA 开发指南",
                "summary": "构建可安装的 Web 应用。",
                "content": """# PWA 开发指南

PWA 让 Web 应用更接近原生体验。

## Service Worker
## Manifest
## 离线支持
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 178
            },
            {
                "title": "Canvas 图形编程",
                "summary": "使用 Canvas 创建高性能图形应用。",
                "content": """# Canvas 图形编程

Canvas 是 Web 2D 图形的基础。

## 基础绘图
## 动画实现
## 性能优化
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 189
            },
            {
                "title": "WebAssembly 入门",
                "summary": "在浏览器中运行高性能代码。",
                "content": """# WebAssembly 入门

WebAssembly 让 Web 应用接近原生性能原理介绍。

##
## Rust 集成
## 应用场景
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 223
            },
            {
                "title": "RxJS 响应式编程",
                "summary": "使用 RxJS 处理异步数据流。",
                "content": """# RxJS 响应式编程

RxJS 是强大的响应式编程库。

## Observable
## 操作符
## 实战应用
""",
                "category_id": categories[0].id,
                "tags": f"{tags[7].id},{tags[1].id}",
                "type": 0,
                "read_count": 198
            },
            {
                "title": "VS Code 插件开发",
                "summary": "从零开发 VS Code 插件提升开发效率。",
                "content": """# VS Code 插件开发

自定义插件可以大幅提升开发效率。

## 插件结构
## API 使用
## 发布流程
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 256
            },
            {
                "title": "正则表达式完全指南",
                "summary": "掌握强大的文本匹配能力。",
                "content": """# 正则表达式完全指南

正则表达式是处理文本的利器。

## 基础语法
## 高级特性
## 实战技巧
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[2].id}",
                "type": 0,
                "read_count": 289
            },
            {
                "title": "命令行工具开发",
                "summary": "使用 Node.js 构建 CLI 工具。",
                "content": """# 命令行工具开发

CLI 工具是提升开发效率的重要手段。

## 基础架构
## 参数解析
## 交互设计
""",
                "category_id": categories[0].id,
                "tags": f"{tags[8].id},{tags[1].id}",
                "type": 0,
                "read_count": 167
            },
            {
                "title": "Electron 桌面应用开发",
                "summary": "使用 Web 技术构建跨平台桌面应用。",
                "content": """# Electron 桌面应用开发

Electron 让 Web 技术进入桌面。

## 基础架构
## 进程通信
## 打包部署
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 212
            },
            {
                "title": "Three.js 3D 图形编程",
                "summary": "在浏览器中创建沉浸式 3D 体验。",
                "content": """# Three.js 3D 图形编程

Three.js 让 Web 3D 变得简单。

## 场景基础
## 材质光照
## 动画系统
""",
                "category_id": categories[0].id,
                "tags": f"{tags[1].id},{tags[3].id}",
                "type": 0,
                "read_count": 278
            },
            {
                "title": "Markdown 完全指南",
                "summary": "深入掌握 Markdown 写作技巧。",
                "content": """# Markdown 完全指南

Markdown 是技术文档的标配。

## 基础语法
## 扩展语法
## 工具推荐
""",
                "category_id": categories[2].id,
                "tags": f"{tags[6].id},{tags[1].id}",
                "type": 0,
                "read_count": 345
            },
        ]

        for i, article_data in enumerate(articles_data):
            # 为每篇文章生成不同的创建和更新时间
            create_time = base_time + timedelta(days=i*3, hours=i*2, minutes=i*5)
            update_time = create_time + timedelta(days=i%10+1, hours=i%5+1)

            article = Article(
                title=article_data["title"],
                summary=article_data["summary"],
                content=article_data["content"],
                category_id=article_data["category_id"],
                tags=article_data["tags"],
                type=article_data["type"],
                read_count=article_data["read_count"],
                create_time=create_time,
                update_time=update_time
            )
            session.add(article)

        session.flush()
        print(f"✓ 插入 {len(articles_data)} 篇文章")

        # 5. 插入评论
        comments_data = [
            {
                "article_id": 1,
                "nickname": "前端小白",
                "email": "xiaobai@example.com",
                "content": "这篇文章讲得很清楚，Composition API 确实很好用！",
                "is_approved": 1
            },
            {
                "article_id": 2,
                "nickname": "设计师阿花",
                "email": "designer@example.com",
                "content": "苹果的设计哲学确实值得学习，文中提到的几点我都深有感触。",
                "is_approved": 1
            },
            {
                "article_id": 3,
                "nickname": "程序员小王",
                "email": "wang@example.com",
                "content": "时间管理确实很重要，感谢分享！",
                "is_approved": 1
            }
        ]

        for comment_data in comments_data:
            comment = Comment(
                article_id=comment_data["article_id"],
                nickname=comment_data["nickname"],
                email=comment_data["email"],
                content=comment_data["content"],
                create_time=datetime.now(),
                is_approved=comment_data["is_approved"]
            )
            session.add(comment)

        print(f"✓ 插入 {len(comments_data)} 条评论")

        # 6. 插入友链
        friendlinks_data = [
            {
                "username": "张三的技术博客",
                "signature": "专注Python全栈开发",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=zhangsan",
                "link_url": "https://example1.com",
                "is_show": 1,
                "weight": 0  # 挚友
            },
            {
                "username": "李四的设计笔记",
                "signature": "分享UI/UX设计经验",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=lisi",
                "link_url": "https://example2.com",
                "is_show": 1,
                "weight": 0  # 挚友
            },
            {
                "username": "王五的生活随笔",
                "signature": "记录生活的点滴美好",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=wangwu",
                "link_url": "https://example3.com",
                "is_show": 1,
                "weight": 1  # 朋友
            },
            {
                "username": "赵六的编程小屋",
                "signature": "前端学习笔记",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=zhaoliu",
                "link_url": "https://example4.com",
                "is_show": 1,
                "weight": 1  # 朋友
            },
            {
                "username": "钱七的成长记录",
                "signature": "欢迎来访",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=qianqi",
                "link_url": "https://example5.com",
                "is_show": 1,
                "weight": 2  # 来客
            }
        ]

        for link_data in friendlinks_data:
            link = FriendLink(
                username=link_data["username"],
                signature=link_data["signature"],
                icon_url=link_data["icon_url"],
                link_url=link_data["link_url"],
                create_time=datetime.now(),
                is_show=link_data["is_show"],
                weight=link_data["weight"]
            )
            session.add(link)

        print(f"✓ 插入 {len(friendlinks_data)} 个友链")

        # 7. 插入留言板
        messages_data = [
            {
                "nickname": "前端开发者",
                "email": "frontend@example.com",
                "content": "博客主题非常简洁很喜欢，支持一下！",
                "is_show": 1
            },
            {
                "nickname": "路过的访客",
                "email": "visitor@example.com",
                "content": "文章写得很好，学到了很多知识",
                "is_show": 1
            },
            {
                "nickname": "技术爱好者",
                "email": "tech@example.com",
                "content": "期待作者更多关于Vue3的教程",
                "is_show": 1
            }
        ]

        for msg_data in messages_data:
            message = MessageBoard(
                nickname=msg_data["nickname"],
                email=msg_data["email"],
                content=msg_data["content"],
                create_time=datetime.now(),
                is_show=msg_data["is_show"]
            )
            session.add(message)

        print(f"✓ 插入 {len(messages_data)} 条留言")

        # 提交所有更改
        session.commit()
        print("\n" + "=" * 50)
        print("数据库初始化完成!")
        print("=" * 50)
        print("\n测试账号信息:")
        print("  用户名: admin")
        print("  密码: 123456")
        print("\n接口文档: http://localhost:8000/docs")

    except Exception as e:
        session.rollback()
        print(f"初始化失败: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_database()
