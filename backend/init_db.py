"""
Database Init Script - 数据库初始化脚本
创建表并插入测试数据
"""
import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import config
from models import Base, Admin, Category, Tag, Article, Comment, FriendLink
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
        ]

        tags = []
        for tag_data in tags_data:
            tag = Tag(name=tag_data["name"], create_time=datetime.now())
            session.add(tag)
            tags.append(tag)

        session.flush()  # 获取标签ID
        print(f"✓ 插入 {len(tags_data)} 个标签")

        # 4. 插入文章（带标签ID和类型）
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

Composition API 为 Vue 应用带来了更好的代码组织和逻辑复用能力。通过遵循本文的最佳实践，你可以编写出更加清晰、可维护的 Vue 3 应用。
""",
                "category_id": categories[0].id,  # 技术
                "tag_id": tags[0].id,  # Vue3
                "type": 0,  # 文章
                "read_count": 128
            },
            {
                "title": "设计系统的美学：从苹果设计哲学学到的",
                "summary": "分析苹果设计系统的核心原则，探讨如何打造简洁优雅的用户界面。",
                "content": """# 设计系统的美学：从苹果设计哲学学到的

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

好的设计是看不见的。通过学习苹果的设计哲学，我们可以创造出更加优雅和易用的产品。
""",
                "category_id": categories[1].id,  # 设计
                "tag_id": tags[3].id,  # UI
                "type": 0,  # 文章
                "read_count": 256
            },
            {
                "title": "在忙碌的生活中寻找平衡",
                "summary": "分享一些关于时间管理，心态调整的思考与实践。",
                "content": """# 在忙碌的生活中寻找平衡

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

生活平衡不是一蹴而就的，需要我们不断调整和反思。希望这些建议对你有所帮助。
""",
                "category_id": categories[2].id,  # 生活
                "tag_id": tags[5].id,  # 生活
                "type": 0,  # 文章
                "read_count": 89
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

掌握 TypeScript 的类型系统可以显著提升代码质量和可维护性。
""",
                "category_id": categories[0].id,  # 技术
                "tag_id": tags[2].id,  # TypeScript
                "type": 0,  # 文章
                "read_count": 167
            },
            {
                "title": "极简主义：少即是多",
                "summary": "探讨极简主义生活方式带来的内心平静与效率提升。",
                "content": """# 极简主义：少即是多

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

少即是多。通过减少生活中的杂物，我们可以找到内心的平静。
""",
                "category_id": categories[2].id,  # 生活
                "tag_id": tags[6].id,  # 自我成长
                "type": 0,  # 文章
                "read_count": 203
            }
        ]

        for article_data in articles_data:
            article = Article(
                title=article_data["title"],
                summary=article_data["summary"],
                content=article_data["content"],
                category_id=article_data["category_id"],
                tag_id=article_data["tag_id"],
                type=article_data["type"],
                read_count=article_data["read_count"],
                create_time=datetime.now(),
                update_time=datetime.now()
            )
            session.add(article)

        session.flush()  # 获取文章ID
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
                "is_show": 1
            },
            {
                "username": "李四的设计笔记",
                "signature": "分享UI/UX设计经验",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=lisi",
                "link_url": "https://example2.com",
                "is_show": 1
            },
            {
                "username": "王五的生活随笔",
                "signature": "记录生活的点滴美好",
                "icon_url": "https://api.dicebear.com/7.x/identicon/svg?seed=wangwu",
                "link_url": "https://example3.com",
                "is_show": 1
            }
        ]

        for link_data in friendlinks_data:
            link = FriendLink(
                username=link_data["username"],
                signature=link_data["signature"],
                icon_url=link_data["icon_url"],
                link_url=link_data["link_url"],
                create_time=datetime.now(),
                is_show=link_data["is_show"]
            )
            session.add(link)

        print(f"✓ 插入 {len(friendlinks_data)} 个友链")

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
