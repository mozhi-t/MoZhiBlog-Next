"""
Article Routes - 文章接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from models import Article, Category, Tag, get_db
from schemas import (
    ArticleCreate, ArticleUpdate, ArticleListResponse,
    ArticleDetailResponse, Response, PaginatedResponse
)
from auth import get_current_admin

router = APIRouter(prefix="/api/articles", tags=["文章"])


@router.get("")
def get_articles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    type: Optional[int] = Query(None, description="文章类型筛选: 0-文章, 1-说说"),
    db: Session = Depends(get_db)
):
    """
    获取文章列表（公开）
    """
    query = db.query(Article)

    # 分类筛选
    if category_id:
        query = query.filter(Article.category_id == category_id)

    # 标签筛选
    if tag_id:
        query = query.filter(Article.tag_id == tag_id)

    # 类型筛选
    if type is not None:
        query = query.filter(Article.type == type)

    # 总数
    total = query.count()

    # 分页
    articles = query.order_by(desc(Article.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    # 转换结果
    items = []
    for article in articles:
        # 获取分类信息
        category = None
        if article.category_id:
            cat = db.query(Category).filter(Category.id == article.category_id).first()
            if cat:
                category = {"id": cat.id, "name": cat.name}

        # 获取标签信息
        tag = None
        if article.tag_id:
            t = db.query(Tag).filter(Tag.id == article.tag_id).first()
            if t:
                tag = {"id": t.id, "name": t.name}

        item = {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "category_id": article.category_id,
            "tag_id": article.tag_id,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "category": category,
            "tag": tag
        }
        items.append(item)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0
        }
    }


@router.get("/hot")
def get_hot_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    获取热门文章（公开）
    """
    articles = db.query(Article).order_by(
        desc(Article.read_count)
    ).limit(limit).all()

    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": a.id,
            "title": a.title,
            "read_count": a.read_count,
            "create_time": a.create_time.isoformat() if a.create_time else None
        } for a in articles]
    }


@router.get("/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    获取单篇文章详情（公开）
    - 访问时阅读量+1
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 阅读量+1
    article.read_count += 1
    db.commit()

    # 获取分类
    category = None
    if article.category_id:
        cat = db.query(Category).filter(Category.id == article.category_id).first()
        if cat:
            category = {"id": cat.id, "name": cat.name}

    # 获取标签
    tag = None
    if article.tag_id:
        t = db.query(Tag).filter(Tag.id == article.tag_id).first()
        if t:
            tag = {"id": t.id, "name": t.name}

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tag_id": article.tag_id,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "category": category,
            "tag": tag
        }
    }


# ==================== 管理员接口 ====================

@router.post("")
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    发布新文章（需管理员鉴权）
    """
    # 检查分类是否存在
    if article_data.category_id:
        category = db.query(Category).filter(Category.id == article_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类不存在"
            )

    # 检查标签是否存在
    if article_data.tag_id:
        tag = db.query(Tag).filter(Tag.id == article_data.tag_id).first()
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="标签不存在"
            )

    # 创建文章
    article = Article(
        title=article_data.title,
        summary=article_data.summary,
        content=article_data.content,
        category_id=article_data.category_id,
        tag_id=article_data.tag_id,
        type=article_data.type,
        read_count=0
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tag_id": article.tag_id,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None
        }
    }


@router.put("/{article_id}")
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    编辑文章（需管理员鉴权）
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 更新字段
    update_data = article_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tag_id": article.tag_id,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None
        }
    }


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除文章（需管理员鉴权）
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    db.delete(article)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
