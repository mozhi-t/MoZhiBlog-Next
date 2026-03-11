-- ============================================
-- MoZhi Blog 数据库初始化SQL
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `mozhiblog` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `mozhiblog`;

-- ============================================
-- 1. 管理员表
-- ============================================
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员表';

-- ============================================
-- 2. 分类表
-- ============================================
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- ============================================
-- 3. 标签表
-- ============================================
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL COMMENT '标签名称',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';

-- ============================================
-- 4. 文章表
-- ============================================
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL COMMENT '文章标题',
  `summary` VARCHAR(500) DEFAULT NULL COMMENT '文章摘要',
  `content` TEXT NOT NULL COMMENT '文章内容',
  `category_id` INT DEFAULT NULL COMMENT '分类ID',
  `tags` VARCHAR(200) DEFAULT NULL COMMENT '标签ID列表，用逗号分隔，如 "1,2,3"',
  `type` TINYINT DEFAULT 0 COMMENT '文章类型: 0-文章, 1-说说',
  `read_count` INT DEFAULT 0 COMMENT '阅读数',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_create_time` (`create_time`),
  FOREIGN KEY (`category_id`) REFERENCES `category`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章表';

-- ============================================
-- 5. 评论表
-- ============================================
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `article_id` INT NOT NULL COMMENT '文章ID',
  `nickname` VARCHAR(50) NOT NULL COMMENT '昵称',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `content` VARCHAR(1000) NOT NULL COMMENT '评论内容',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
  `is_approved` TINYINT DEFAULT 1 COMMENT '是否审核: 0-未审核, 1-已审核',
  PRIMARY KEY (`id`),
  KEY `idx_article_id` (`article_id`),
  FOREIGN KEY (`article_id`) REFERENCES `article`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- ============================================
-- 6. 友链表
-- ============================================
DROP TABLE IF EXISTS `friend_link`;
CREATE TABLE `friend_link` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL COMMENT '友链名称',
  `signature` VARCHAR(200) DEFAULT NULL COMMENT '个性签名',
  `icon_url` VARCHAR(500) DEFAULT NULL COMMENT '图标URL',
  `link_url` VARCHAR(500) NOT NULL COMMENT '链接地址',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_show` TINYINT DEFAULT 1 COMMENT '是否显示: 0-隐藏, 1-显示',
  `weight` TINYINT DEFAULT 2 COMMENT '权重: 0-挚友, 1-朋友, 2-来客',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='友链表';

-- ============================================
-- 7. IP黑名单表
-- ============================================
DROP TABLE IF EXISTS `blacklist`;
CREATE TABLE `blacklist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ip` VARCHAR(50) NOT NULL COMMENT 'IP地址',
  `failed_attempts` INT DEFAULT 0 COMMENT '登录失败次数',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='IP黑名单表';

-- ============================================
-- 8. 留言板表
-- ============================================
DROP TABLE IF EXISTS `message_board`;
CREATE TABLE `message_board` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(50) NOT NULL COMMENT '昵称',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `content` VARCHAR(1000) NOT NULL COMMENT '留言内容',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '留言时间',
  `is_show` TINYINT DEFAULT 1 COMMENT '是否显示: 0-隐藏, 1-显示',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='留言板表';

-- ============================================
-- 插入测试数据
-- ============================================

-- 1. 插入管理员 (admin / 123456)
-- 密码哈希值: $2b$12$10wNDvY0C6fFUCxHGf/wiuzcKAhO2.W4AhqJN.9ocxbnrnoJqWTOa
INSERT INTO `admin` (`username`, `password`, `email`) VALUES
('admin', '$2b$12$10wNDvY0C6fFUCxHGf/wiuzcKAhO2.W4AhqJN.9ocxbnrnoJqWTOa', 'admin@mozhiblog.com');

-- 2. 插入分类
INSERT INTO `category` (`name`) VALUES
('技术'),
('设计'),
('生活');

-- 3. 插入标签
INSERT INTO `tag` (`name`) VALUES
('Vue3'),
('前端'),
('TypeScript'),
('UI'),
('UX'),
('生活'),
('自我成长');

-- 4. 插入文章（多标签用逗号分隔）
INSERT INTO `article` (`title`, `summary`, `content`, `category_id`, `tags`, `type`, `read_count`) VALUES
('探索 Vue 3 Composition API 的最佳实践', '深入理解 Vue 3 的 Composition API，学习如何编写更清晰、可维护的组件代码。', '# 探索 Vue 3 Composition API 的最佳实践

Vue 3 引入了 Composition API，这是一项重大的架构改进。本文将深入探讨如何有效使用 Composition API 来构建可维护的应用。

## 什么是 Composition API？

Composition API 是 Vue 3 引入的一组 API，允许我们以更灵活的方式组织组件逻辑。相比于 Options API，Composition API 提供了更好的逻辑复用和代码组织能力。

## 核心 API

### setup()

`setup()` 是 Composition API 的入口点，它在组件创建之前执行，只会被调用一次。

```javascript
import { ref, computed } from ''vue''

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

Composition API 为 Vue 应用带来了更好的代码组织和逻辑复用能力。通过遵循本文的最佳实践，你可以编写出更加清晰、可维护的 Vue 3 应用。', 1, '1,2', 0, 128),

('设计系统的美学：从苹果设计哲学学到的', '分析苹果设计系统的核心原则，探讨如何打造简洁优雅的用户界面。', '# 设计系统的美学：从苹果设计哲学学到的

苹果公司以其卓越的设计而闻名于世。在这篇文章中，我们将探讨苹果的设计哲学以及如何将其应用到我们的产品中。

## 核心原则

### 1. 简洁性

> "简单是复杂的终极形式。" — 列奥纳多·达·芬奇

苹果的设计始终追求简洁。每一个元素都有其存在的理由。

### 2. 一致性

保持视觉和交互的一致性，让用户感到熟悉和舒适。

### 3. 反馈

每一个操作都应该有及时的反馈，让用户知道发生了什么。

## 实践应用

在设计你的产品时，请考虑：

- 使用留白来创造呼吸空间
- 保持颜色和字体的统一性
- 添加微交互来增强用户体验

## 总结

好的设计是看不见的。通过学习苹果的设计哲学，我们可以创造出更加优雅和易用的产品。', 2, '4,5', 0, 256),

('在忙碌的生活中寻找平衡', '分享一些关于时间管理，心态调整的思考与实践。', '# 在忙碌的生活中寻找平衡

现代生活节奏越来越快，我们常常感到时间不够用。这篇文章分享一些我在寻找生活平衡方面的经验。

## 认识自己

首先，你需要了解自己的生活节奏。什么时间你最高效？什么时候你需要休息？

## 时间管理技巧

### 1. 番茄工作法

设定25分钟专注工作，然后休息5分钟。这种方法可以帮助你保持专注同时避免疲劳。

### 2. 优先级排序

每天早上花10分钟确定当天最重要的三件事。先完成这些，再处理其他的。

### 3. 学会说"不"

不是所有的邀请或任务都需要接受。学会拒绝，保护你的时间。

## 身心健康

- 保持规律作息
- 适量运动
- 定期冥想

## 总结

生活平衡不是一蹴而就的，需要我们不断调整和反思。希望这些建议对你有所帮助。', 3, '6,7', 0, 89),

('TypeScript 类型系统详解', '全面解析 TypeScript 的高级类型特性，提升代码类型安全。', '# TypeScript 类型系统详解

TypeScript 的类型系统是其最强大的特性之一。本文将全面解析 TypeScript 的高级类型特性。

## 基础类型

```typescript
let name: string = "MoZhi"
let age: number = 25
let isDeveloper: boolean = true
```

## 高级类型

### 1. 联合类型

```typescript
type ID = string | number
```

### 2. 交叉类型

```typescript
type Extended = Type1 & Type2
```

### 3. 泛型

```typescript
function identity<T>(arg: T): T {
  return arg
}
```

## 总结

掌握 TypeScript 的类型系统可以显著提升代码质量和可维护性。', 1, '3,2', 0, 167),

('极简主义：少即是多', '探讨极简主义生活方式带来的内心平静与效率提升。', '# 极简主义：少即是多

极简主义不仅仅是一种设计风格，更是一种生活方式。

## 什么是极简主义？

极简主义是刻意地倡导我们所需的最少物品，并专注于生活中真正重要的事情。

## 实践步骤

1. **审视物品**：问自己"这件东西真的必要吗？"
2. **减少物品**：只保留真正需要的东西
3. **简化决策**：减少选择可以节省精力

## 心理益处

- 减少焦虑
- 更专注
- 更自由

## 总结

少即是多。通过减少生活中的杂物，我们可以找到内心的平静。', 3, '7,6', 0, 203),

('Node.js 性能优化实战', '分享 Node.js 应用性能优化的实用技巧和最佳实践。', '# Node.js 性能优化实战

Node.js 是构建高性能后端服务的热门选择。本文将介绍一些实用的性能优化技巧。

## 1. 事件循环优化

了解事件循环的工作原理，避免阻塞主线程。

## 2. 内存管理

合理使用内存，及时清理不再使用的对象。

## 3. 流处理

使用流来处理大文件，避免内存溢出。

## 4. 集群模式

利用 Node.js 集群模块充分利用多核 CPU。

## 总结

性能优化是一个持续的过程，需要不断监控和改进。', 1, '1,3', 0, 198),

('CSS Grid 布局完全指南', '深入学习 CSS Grid 布局系统，打造复杂的网页布局。', '# CSS Grid 布局完全指南

CSS Grid 是现代网页布局的强大工具。

## 基本概念

- 网格容器
- 网格项
- 网格线

## 常用属性

```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
```

## 响应式设计

Grid 布局让响应式设计变得更加简单。

## 总结

掌握 CSS Grid 可以大大提升你的布局能力。', 1, '1,4', 0, 234),

('Docker 入门与实践', '从零开始学习 Docker 容器化技术。', '# Docker 入门与实践

Docker 改变了软件的部署方式。

## 什么是 Docker？

Docker 是一个容器化平台，可以将应用及其依赖打包成容器。

## 基本命令

```bash
docker build -t myapp .
docker run -p 8080:80 myapp
docker ps
```

## Dockerfile 最佳实践

1. 减少镜像层数
2. 使用 .dockerignore
3. 多阶段构建

## 总结

Docker 是现代 DevOps 的基础技能。', 1, '1,8', 0, 176),

('HTTP 协议深度解析', '全面理解 HTTP 协议的工作原理。', '# HTTP 协议深度解析

HTTP 是互联网的基础协议之一。

## 请求方法

- GET: 获取资源
- POST: 创建资源
- PUT: 更新资源
- DELETE: 删除资源

## 状态码

- 200: 成功
- 301: 重定向
- 404: 未找到
- 500: 服务器错误

## 总结

深入理解 HTTP 协议是 Web 开发的基础。', 1, '1,9', 0, 145),

('Git 高级技巧', '提升 Git 使用效率的进阶技巧。', '# Git 高级技巧

掌握这些 Git 技巧可以大大提高你的开发效率。

## 1. 交互式变基

```bash
git rebase -i
```

## 2. 贮藏技巧

```bash
git stash push -m "work in progress"
```

## 3. 子模块

管理大型项目的依赖仓库。

## 总结

Git 是开发者必备技能，不断学习可以更加熟练。', 1, '1,10', 0, 189),

('算法复杂度分析', '学习如何分析算法的时间空间复杂度。', '# 算法复杂度分析

算法复杂度是衡量算法效率的重要指标。

## 时间复杂度

- O(1): 常数时间
- O(log n): 对数时间
- O(n): 线性时间
- O(n²): 平方时间

## 空间复杂度

分析算法所需的内存空间。

## 总结

理解复杂度分析可以帮助我们写出更高效的代码。', 1, '1,3', 0, 156),

('React Hooks 深入理解', '全面掌握 React Hooks 的使用技巧。', '# React Hooks 深入理解

React Hooks 是 React 16.8 引入的重大特性。

## 常用 Hooks

- useState: 状态管理
- useEffect: 副作用处理
- useContext: 上下文
- useReducer: 复杂状态

## 自定义 Hook

封装可复用的逻辑。

## 总结

Hooks 让函数组件更加强大。', 1, '1,2', 0, 221),

('微服务架构设计', '探讨微服务的设计原则与实践。', '# 微服务架构设计

微服务架构是现代后端开发的重要模式。

## 核心原则

1. 单一职责
2. 独立部署
3. 松耦合
4. 高内聚

## 服务通信

- REST API
- gRPC
- 消息队列

## 总结

微服务架构需要成熟的 DevOps 能力支持。', 1, '1,8', 0, 167),

('数据库索引优化', '学习如何优化数据库查询性能。', '# 数据库索引优化

索引是提升数据库查询性能的关键。

## 索引类型

- B-Tree 索引
- 哈希索引
- 全文索引

## 优化技巧

1. 选择合适的列
2. 避免过多索引
3. 使用复合索引

## 总结

正确的索引可以大幅提升查询速度。', 1, '1,11', 0, 198),

('JavaScript 异步编程', '深入理解 Promise、Async/Await。', '# JavaScript 异步编程

异步编程是 JavaScript 的核心概念。

## 回调函数

```javascript
fs.readFile(''file.txt'', (err, data) => {
  console.log(data)
})
```

## Promise

```javascript
fetch(''/api/data'')
  .then(res => res.json())
  .then(data => console.log(data))
```

## Async/Await

```javascript
async function fetchData() {
  const res = await fetch(''/api/data'')
  const data = await res.json()
  return data
}
```

## 总结

异步编程让 JavaScript 更加优雅。', 1, '1,2', 0, 234),

('Web 安全实战', '常见 Web 安全漏洞与防护措施。', '# Web 安全实战

Web 安全是每个开发者都必须重视的话题。

## 常见漏洞

1. XSS 跨站脚本
2. CSRF 跨站请求伪造
3. SQL 注入
4. 文件上传漏洞

## 防护措施

- 输入验证
- 输出编码
- 使用 HTTPS
- 安全的认证机制

## 总结

安全防护需要贯穿整个开发过程。', 1, '1,9', 0, 187),

('Python 数据分析入门', '使用 Python 进行数据分析的基础教程。', '# Python 数据分析入门

Python 是数据分析的首选语言。

## 核心库

- NumPy: 数值计算
- Pandas: 数据处理
- Matplotlib: 数据可视化

## 基本操作

```python
import pandas as pd
df = pd.read_csv(''data.csv'')
df.describe()
```

## 总结

掌握数据分析技能可以带来更多机会。', 2, '4,11', 0, 156),

('RESTful API 设计规范', '设计优雅的 RESTful API 接口。', '# RESTful API 设计规范

RESTful API 是现代 Web 服务的主流架构风格。

## 设计原则

1. 使用名词而非动词
2. 使用 HTTP 方法语义
3. 返回合适的状态码
4. 版本化你的 API

## 最佳实践

- 使用分页
- 过滤和排序
- 错误处理标准化

## 总结

好的 API 设计提升开发者体验。', 1, '1,9', 0, 198),

(' Vim 使用技巧', '提升 Vim 使用效率的实用技巧。', '# Vim 使用技巧

Vim 是强大的文本编辑器。

## 基础操作

- i: 进入插入模式
- Esc: 返回普通模式
- :w: 保存
- :q: 退出

## 高效技巧

1. 快速移动：w, b, e, 0, $
2. 文本对象：iw, aw, i", a"
3. 宏录制：q, @

## 总结

Vim 需要长期练习才能熟练掌握。', 1, '1,10', 0, 145),

('正则表达式完全指南', '掌握强大的文本匹配技能。', '# 正则表达式完全指南

正则表达式是处理文本的利器。

## 基础语法

- .: 任意字符
- *: 零个或多个
- +: 一个或多个
- ?: 零个或一个

## 常用模式

```regex
邮箱: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
手机: ^1[3-9]\d{9}$
```

## 总结

正则表达式需要大量练习才能熟练。', 1, '1,3', 0, 178),

('函数式编程入门', '学习函数式编程的核心概念。', '# 函数式编程入门

函数式编程是一种重要的编程范式。

## 核心概念

1. 纯函数
2. 不可变性
3. 高阶函数
4. 柯里化

## JavaScript 实现

```javascript
const compose = (...fns) =>
  fns.reduce((f, g) => (...args) => f(g(...args)))
```

## 总结

函数式编程可以写出更简洁的代码。', 1, '1,3', 0, 167),

('代码重构的艺术', '如何安全地进行代码重构。', '# 代码重构的艺术

重构是保持代码健康的必要手段。

## 重构时机

- 代码重复
- 函数过长
- 类过大
- 命名不清晰

## 常用技术

1. 提取函数
2. 内联函数
3. 移动方法
4. 重命名

## 总结

重构需要循序渐进，步步为营。', 1, '1,10', 0, 189),

('GraphQL 实战', '构建高效的 GraphQL API。', '# GraphQL 实战

GraphQL 是 Facebook 推出的 API 查询语言。

## 核心概念

- Schema: 类型定义
- Query: 查询
- Mutation: 修改
- Resolver: 解析器

## 优势

1. 按需获取数据
2. 强类型系统
3. 减少请求次数

## 总结

GraphQL 是 REST 的有力替代方案。', 1, '1,9', 0, 176),

('Vue3 响应式原理深度解析', '理解 Vue3 响应式系统的内部实现。', '# Vue3 响应式原理深度解析

Vue3 的响应式系统是其核心特性。

## Proxy vs Object.defineProperty

Vue3 使用 Proxy 替代了 Object.defineProperty。

## 核心 API

- reactive
- ref
- computed
- watch

## 源码分析

理解源码可以更好地使用 Vue3。

## 总结

深入理解原理才能更好地使用框架。', 1, '1,2', 0, 234),

('测试驱动开发 TDD', '掌握 TDD 开发方法。', '# 测试驱动开发 TDD

TDD 是一种重要的开发方法论。

## 开发流程

1. 红灯：写一个失败的测试
2. 绿灯：写最少的代码让测试通过
3. 重构：改善代码结构

## 测试框架

- Jest
- Vitest
- Mocha

## 总结

TDD 可以提高代码质量和信心。', 1, '1,10', 0, 156),

('CSS 动画实战', '创建流畅的 CSS 动画效果。', '# CSS 动画实战 动画可以让网页

CSS更加生动。

## 动画属性

```css
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
```

## 性能优化

1. 使用 transform 和 opacity
2. 避免动画布局属性
3. 使用 will-change

## 总结

好的动画提升用户体验。', 1, '1,4', 0, 198),

('MongoDB 进阶指南', '深入学习 MongoDB 数据库。', '# MongoDB 进阶指南

MongoDB 是最流行的 NoSQL 数据库。

## 核心概念

- Document: 文档
- Collection: 集合
- Field: 字段

## 查询优化

1. 创建索引
2. 投影查询
3. 聚合管道

## 总结

MongoDB 适合快速迭代的项目。', 1, '1,11', 0, 167),

('前端工程化实践', '构建现代前端工作流。', '# 前端工程化实践

前端工程化是现代前端开发的必备。

## 核心工具

- 包管理器：npm, yarn, pnpm
- 构建工具：Vite, Webpack
- 代码规范：ESLint, Prettier

## 自动化

1. CI/CD
2. 自动化测试
3. 自动化部署

## 总结

工程化提升开发效率和代码质量。', 1, '1,2', 0, 212),

('Rust 编程入门', '学习高性能系统编程语言。', '# Rust 编程入门

Rust 是一门注重安全和性能的系统编程语言。

## 核心特性

1. 所有权系统
2. 生命周期
3. 模式匹配

## Hello World

```rust
fn main() {
    println!("Hello, world!");
}
```

## 总结

Rust 可以编写高效安全的系统级代码。', 1, '1,3', 0, 145),

('Linux 命令行实战', '提升 Linux 命令行使用效率。', '# Linux 命令行实战

熟练使用命令行是开发者的必备技能。

## 常用命令

- ls, cd, pwd: 文件操作
- grep, awk, sed: 文本处理
- find, xargs: 文件查找

## 技巧

1. 使用别名
2. 配置 .bashrc
3. 掌握管道

## 总结

命令行是提升效率的神器。', 1, '1,10', 0, 178),

('Flutter 移动开发入门', '使用 Flutter 构建跨平台应用。', '# Flutter 移动开发入门

Flutter 是 Google 的跨平台 UI 框架。

## 核心概念

- Widget: 组件
- State: 状态
- BuildContext: 上下文

## 基础代码

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(child: Text(''Hello'')),
      ),
    );
  }
}
```

## 总结

Flutter 可以一套代码运行多端。', 1, '1,12', 0, 189),

('AWS 云服务入门', '学习亚马逊云服务基础知识。', '# AWS 云服务入门

AWS 是全球最大的云服务平台。

## 核心服务

- EC2: 云服务器
- S3: 对象存储
- RDS: 数据库服务
- Lambda: 无服务器计算

## 最佳实践

1. 使用 IAM 管理权限
2. 开启账单警报
3. 使用标签管理资源

## 总结

云技能是现代开发者的必备。', 1, '1,8', 0, 156),

('GraphQL vs REST', '对比两种 API 设计风格。', '# GraphQL vs REST

GraphQL 和 REST 是两种不同的 API 设计风格。

## REST 特点

- 资源导向
- 标准 HTTP 方法
- 固定端点

## GraphQL 特点

- 查询语言
- 按需获取
- 强类型

## 选择建议

根据项目需求选择合适的风格。

## 总结

两种风格各有优劣。', 1, '1,9', 0, 167),

('WebAssembly 实战', '在浏览器中运行高性能代码。', '# WebAssembly 实战

WebAssembly 是浏览器的新能力。

## 什么是 WebAssembly？

一种可移植的低级语言，可以在浏览器中运行。

## 使用场景

1. 图像处理
2. 游戏
3. 加密计算

## 总结

Wasm 扩展了 Web 的能力边界。', 1, '1,2', 0, 145),

('NestJS 后端框架', '构建可扩展的 Node.js 后端。', '# NestJS 后端框架

NestJS 是 Node.js 的企业级框架。

## 核心概念

- Module: 模块
- Controller: 控制器
- Service: 服务
- Provider: 提供者

## 依赖注入

NestJS 的核心特性。

## 总结

NestJS 让 Node.js 开发更加规范。', 1, '1,8', 0, 198),

('Canvas 图形编程', '使用 HTML5 Canvas 绘制图形。', '# Canvas 图形编程

Canvas 是 HTML5 的重要特性。

## 基础绘制

```javascript
ctx.fillRect(0, 0, 100, 100)
ctx.beginPath()
ctx.arc(50, 50, 40, 0, Math.PI * 2)
ctx.fill()
```

## 动画实现

使用 requestAnimationFrame 实现动画。

## 总结

Canvas 可以创建丰富的图形效果。', 1, '1,4', 0, 176),

('数据结构与算法', '常见数据结构的实现与应用。', '# 数据结构与算法

数据结构和算法是编程的基础。

## 常见数据结构

- 数组
- 链表
- 树
- 图

## 排序算法

- 冒泡排序
- 快速排序
- 归并排序

## 总结

扎实的基础是进阶的前提。', 1, '1,3', 0, 189),

('Redis 缓存实战', '使用 Redis 提升应用性能。', '# Redis 缓存实战

Redis 是高性能的内存数据库。

## 数据类型

- String: 字符串
- Hash: 哈希
- List: 列表
- Set: 集合
- Sorted Set: 有序集合

## 应用场景

1. 缓存
2. 会话存储
3. 分布式锁

## 总结

Redis 是提升性能的利器。', 1, '1,11', 0, 212),

('RxJS 响应式编程', '学习响应式编程范式。', '# RxJS 响应式编程

RxJS 是 JavaScript 的响应式编程库。

## 核心概念

- Observable: 可观察对象
- Observer: 观察者
- Operator: 操作符
- Subject: 主题

## 操作符

```javascript
from([1,2,3]).pipe(
  map(x => x * 2),
  filter(x => x > 2)
)
```

## 总结

RxJS 让异步代码更加优雅。', 1, '1,2', 0, 167),

('CI/CD 持续集成', '构建自动化部署流程。', '# CI/CD 持续集成

CI/CD 是现代软件交付的重要实践。

## CI 流程

1. 代码提交
2. 自动测试
3. 构建镜像

## CD 流程

1. 自动部署
2. 监控回滚
3. 持续交付

## 工具选择

- Jenkins
- GitHub Actions
- GitLab CI

## 总结

自动化是提升交付效率的关键。', 1, '1,8', 0, 178),

('Webpack 深入理解', '掌握 Webpack 构建工具。', '# Webpack 深入理解

Webpack 是流行的模块打包工具。

## 核心概念

- Entry: 入口
- Output: 输出
- Loader: 加载器
- Plugin: 插件

## 性能优化

1. 代码分割
2. 懒加载
3. 缓存优化

## 总结

深入理解 webpack 原理很有必要。', 1, '1,2', 0, 189),

('移动端性能优化', '提升移动端网页加载速度。', '# 移动端性能优化

移动端性能对用户体验至关重要。

## 优化策略优化

1. 图片
2. 懒加载
3. 代码分割
4. CDN 加速

## 性能指标

- FCP: 首次内容绘制
- LCP: 最大内容绘制
- FID: 首次输入延迟

## 总结

性能优化需要持续关注。', 1, '1,2', 0, 201),

('Elasticsearch 搜索实战', '构建强大的搜索功能。', '# Elasticsearch 搜索实战

Elasticsearch 是分布式搜索引擎。

## 核心概念

- Index: 索引
- Document: 文档
- Type: 类型

## 查询语法

```json
{
  "query": {
    "match": {
      "title": "Vue"
    }
  }
}
```

## 总结

Elasticsearch 可以实现强大的搜索功能。', 1, '1,11', 0, 176),

('Serverless 架构入门', '无服务器架构实践。', '# Serverless 架构入门

Serverless 是云计算的新范式。

## 核心概念

- Function: 函数
- Trigger: 触发器
- Event: 事件

## 云函数

云函数让开发者专注业务逻辑。

## 优势

1. 降低运维成本
2. 按需付费
3. 自动扩缩容

## 总结

Serverless 是未来云原生趋势。', 1, '1,8', 0, 167),

('Web 性能指标详解', '深入理解核心 Web 性能指标。', '# Web 性能指标详解

理解性能指标是优化的基础。

## Core Web Vitals

1. LCP: 最大内容绘制
2. FID: 首次输入延迟
3. CLS: 累积布局偏移

## 优化方法

针对每个指标进行专项优化。

## 工具

- Lighthouse
- PageSpeed Insights
- Chrome DevTools

## 总结

性能是用户体验的关键因素。', 1, '1,2', 0, 198),

('Koa.js 框架深入', '学习轻量级 Node.js 框架。', '# Koa.js 框架深入

Koa 是 Express 原班人马打造的现代框架。

## 核心特性

1. 中间件机制
2. 异步 async/await
3. 极简设计

## 基础用法

```javascript
const app = new Koa()
app.use(ctx => {
  ctx.body = ''Hello Koa''
})
app.listen(3000)
```

## 总结

Koa 的设计理念非常优雅。', 1, '1,8', 0, 156),

('PostgreSQL 数据库进阶', '深入学习功能强大的关系型数据库。', '# PostgreSQL 数据库进阶

PostgreSQL 是功能最强大的开源数据库。

## 高级特性

1. JSONB 支持
2. 全文搜索
3. 窗口函数
4. 物化视图

## 性能优化

1. 索引策略
2. 查询优化
3. 连接池

## 总结

PostgreSQL 适合复杂业务场景。', 1, '1,11', 0, 189);

-- 5. 插入评论
INSERT INTO `comment` (`article_id`, `nickname`, `email`, `content`, `is_approved`) VALUES
(1, '前端小白', 'xiaobai@example.com', '这篇文章讲得很清楚，Composition API 确实很好用！', 1),
(2, '设计师阿花', 'designer@example.com', '苹果的设计哲学确实值得学习，文中提到的几点我都深有感触。', 1),
(3, '程序员小王', 'wang@example.com', '时间管理确实很重要，感谢分享！', 1);

-- 6. 插入友链（带权重）
INSERT INTO `friend_link` (`username`, `signature`, `icon_url`, `link_url`, `is_show`, `weight`) VALUES
('张三的技术博客', '专注Python全栈开发', 'https://api.dicebear.com/7.x/identicon/svg?seed=zhangsan', 'https://example1.com', 1, 0),
('李四的设计笔记', '分享UI/UX设计经验', 'https://api.dicebear.com/7.x/identicon/svg?seed=lisi', 'https://example2.com', 1, 0),
('王五的生活随笔', '记录生活的点滴美好', 'https://api.dicebear.com/7.x/identicon/svg?seed=wangwu', 'https://example3.com', 1, 1),
('赵六的编程小屋', '前端学习笔记', 'https://api.dicebear.com/7.x/identicon/svg?seed=zhaoliu', 'https://example4.com', 1, 1),
('钱七的成长记录', '欢迎来访', 'https://api.dicebear.com/7.x/identicon/svg?seed=qianqi', 'https://example5.com', 1, 2);

-- 7. 插入留言板
INSERT INTO `message_board` (`nickname`, `email`, `content`, `is_show`) VALUES
('前端开发者', 'frontend@example.com', '博客主题非常简洁很喜欢，支持一下！', 1),
('路过的访客', 'visitor@example.com', '文章写得很好，学到了很多知识', 1),
('技术爱好者', 'tech@example.com', '期待作者更多关于Vue3的教程', 1);

-- ============================================
-- 数据库初始化完成
-- ============================================
