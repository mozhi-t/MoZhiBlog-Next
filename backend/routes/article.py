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
from logger import logger

router = APIRouter(prefix="/api/articles", tags=["文章"])


def get_tags_from_ids(tags_str: str, db: Session):
    if not tags_str:
        return []

    tag_ids = [int(tid.strip()) for tid in tags_str.split(',') if tid.strip().isdigit()]
    if not tag_ids:
        return []

    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    return [{"id": t.id, "name": t.name} for t in tags]


def parse_tags_for_filter(tags_str: str):
    if not tags_str:
        return None
    # 支持逗号分隔的多个标签ID
    tag_ids = [int(tid.strip()) for tid in tags_str.split(',') if tid.strip().isdigit()]
    return tag_ids[0] if tag_ids else None


@router.get("")
def get_articles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    type: Optional[int] = Query(None, description="文章类型筛选: 0-文章, 1-说说"),
    db: Session = Depends(get_db)
):
    logger.info(f"获取文章列表 - page: {page}, size: {size}, category_id: {category_id}, tag_id: {tag_id}, type: {type}")
    query = db.query(Article)

    # 分类筛选
    if category_id:
        query = query.filter(Article.category_id == category_id)

    # 标签筛选
    if tag_id:
        # 筛选包含指定标签的文章
        query = query.filter(Article.tags.contains(str(tag_id)))

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

        # 获取标签信息列表
        tag_list = get_tags_from_ids(article.tags, db)

        item = {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "category_id": article.category_id,
            "tags": article.tags,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "category": category,
            "tag_list": tag_list
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
    logger.info(f"获取热门文章 - limit: {limit}")
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
    logger.info(f"获取文章详情 - article_id: {article_id}")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"文章不存在 - article_id: {article_id}")
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

    # 获取标签列表
    tag_list = get_tags_from_ids(article.tags, db)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tags": article.tags,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "category": category,
            "tag_list": tag_list
        }
    }


# ==================== 管理员接口 ====================
@router.post("")
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    logger.info(f"创建文章 - title: {article_data.title}, author: {admin.username}")
    # 检查分类是否存在
    if article_data.category_id:
        category = db.query(Category).filter(Category.id == article_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类不存在"
            )

    # 验证标签是否存在
    if article_data.tags:
        tag_ids = [int(tid.strip()) for tid in article_data.tags.split(',') if tid.strip().isdigit()]
        existing_tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        if len(existing_tags) != len(tag_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分标签不存在"
            )

    # 创建文章
    article = Article(
        title=article_data.title,
        summary=article_data.summary,
        content=article_data.content,
        category_id=article_data.category_id,
        tags=article_data.tags,
        type=article_data.type,
        read_count=0
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    # 获取标签列表
    tag_list = get_tags_from_ids(article.tags, db)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tags": article.tags,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "tag_list": tag_list
        }
    }


@router.put("/{article_id}")
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    logger.info(f"更新文章 - article_id: {article_id}, author: {admin.username}")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"文章不存在 - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 验证标签是否存在
    if article_data.tags:
        tag_ids = [int(tid.strip()) for tid in article_data.tags.split(',') if tid.strip().isdigit()]
        existing_tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        if len(existing_tags) != len(tag_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分标签不存在"
            )

    # 更新字段
    update_data = article_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    # 获取标签列表
    tag_list = get_tags_from_ids(article.tags, db)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category_id": article.category_id,
            "tags": article.tags,
            "type": article.type,
            "read_count": article.read_count,
            "create_time": article.create_time.isoformat() if article.create_time else None,
            "update_time": article.update_time.isoformat() if article.update_time else None,
            "tag_list": tag_list
        }
    }


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    logger.info(f"删除文章 - article_id: {article_id}, author: {admin.username}")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"文章不存在 - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    db.delete(article)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
