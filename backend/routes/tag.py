"""
Tag Routes - 鏍囩鎺ュ彛
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from auth import get_current_admin
from cache import cache
from models import Article, Tag, get_db
from schemas import TagCreate, TagUpdate

router = APIRouter(prefix="/api/tags", tags=["鏍囩"])

TAGS_CACHE_KEY = "tags:list"


def invalidate_tag_cache():
    cache.delete(TAGS_CACHE_KEY)
    cache.delete_prefix("articles:list:")


@router.get("")
def get_tags(db: Session = Depends(get_db)):
    """
    鑾峰彇鎵€鏈夋爣绛惧垪琛紙鍏紑锛?
    """

    def load_tags():
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

    return cache.get_or_set(TAGS_CACHE_KEY, load_tags)


@router.get("/all")
def get_all_tags(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    鑾峰彇鎵€鏈夋爣绛惧垪琛紙闇€绠＄悊鍛橀壌鏉冿級
    """
    query = db.query(Tag)
    total = query.count()

    tags = query.order_by(desc(Tag.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

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


# ==================== 绠＄悊鍛樻帴鍙?====================

@router.post("")
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    鏂板鏍囩锛堥渶绠＄悊鍛橀壌鏉冿級
    """
    existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="鏍囩鍚嶇О宸插瓨鍦?",
        )

    tag = Tag(name=tag_data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    invalidate_tag_cache()

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
    缂栬緫鏍囩锛堥渶绠＄悊鍛橀壌鏉冿級
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="鏍囩涓嶅瓨鍦?",
        )

    if tag_data.name and tag_data.name != tag.name:
        existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="鏍囩鍚嶇О宸插瓨鍦?",
            )
        tag.name = tag_data.name

    db.commit()
    db.refresh(tag)
    invalidate_tag_cache()

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
    鍒犻櫎鏍囩锛堥渶绠＄悊鍛橀壌鏉冿級
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="鏍囩涓嶅瓨鍦?",
        )

    db.delete(tag)
    db.commit()
    invalidate_tag_cache()

    return {"code": 200, "msg": "鍒犻櫎鎴愬姛"}
