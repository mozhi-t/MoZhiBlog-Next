"""
Tag Routes - 标签接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import Tag, Article, get_db
from schemas import TagCreate, TagUpdate
from auth import get_current_admin

router = APIRouter(prefix="/api/tags", tags=["标签"])


@router.get("")
def get_tags(db: Session = Depends(get_db)):
    """
    获取所有标签列表（公开）
    """
    tags = db.query(Tag).order_by(desc(Tag.create_time)).all()
    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": t.id,
            "name": t.name,
            "create_time": t.create_time.isoformat() if t.create_time else None
        } for t in tags]
    }


@router.get("/all")
def get_all_tags(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    获取所有标签列表（需管理员鉴权）
    """
    query = db.query(Tag)
    total = query.count()

    tags = query.order_by(desc(Tag.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    # 获取每个标签的文章数量
    items = []
    for tag in tags:
        article_count = db.query(Article).filter(Article.tag_id == tag.id).count()
        items.append({
            "id": tag.id,
            "name": tag.name,
            "create_time": tag.create_time.isoformat() if tag.create_time else None,
            "article_count": article_count
        })

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


# ==================== 管理员接口 ====================

@router.post("")
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    新增标签（需管理员鉴权）
    """
    existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标签名称已存在"
        )

    tag = Tag(name=tag_data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": tag.id,
            "name": tag.name,
            "create_time": tag.create_time.isoformat() if tag.create_time else None
        }
    }


@router.put("/{tag_id}")
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    编辑标签（需管理员鉴权）
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )

    if tag_data.name and tag_data.name != tag.name:
        existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="标签名称已存在"
            )
        tag.name = tag_data.name

    db.commit()
    db.refresh(tag)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": tag.id,
            "name": tag.name,
            "create_time": tag.create_time.isoformat() if tag.create_time else None
        }
    }


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除标签（需管理员鉴权）
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )

    db.delete(tag)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
