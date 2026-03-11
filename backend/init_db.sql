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

少即是多。通过减少生活中的杂物，我们可以找到内心的平静。', 3, '7,6', 0, 203);

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
