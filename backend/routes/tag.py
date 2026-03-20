"""
Tag routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from auth import get_current_admin
from cache import cache
from logger import logger
from models import Article, Tag, get_db
from schemas import TagCreate, TagUpdate

router = APIRouter(prefix="/api/tags", tags=["tags"])

TAGS_CACHE_KEY = "tags:list"


def invalidate_tag_cache():
    cache.delete(TAGS_CACHE_KEY)
    cache.delete_prefix("articles:list:")


def build_tag_match_condition(tag_id: int):
    tag_id_str = str(tag_id)
    return or_(
        Article.tags == tag_id_str,
        Article.tags.like(f"{tag_id_str},%"),
        Article.tags.like(f"%,{tag_id_str}"),
        Article.tags.like(f"%,{tag_id_str},%"),
    )


def remove_tag_from_articles(tag_id: int, db: Session) -> int:
    tag_id_str = str(tag_id)
    articles = db.query(Article).filter(build_tag_match_condition(tag_id)).all()
    cleaned_count = 0

    for article in articles:
        tag_ids = [item.strip() for item in (article.tags or "").split(",") if item.strip()]
        next_tag_ids = [item for item in tag_ids if item != tag_id_str]
        next_tags = ",".join(next_tag_ids) if next_tag_ids else None

        if next_tags != article.tags:
            article.tags = next_tags
            cleaned_count += 1

    return cleaned_count


@router.get("")
def get_tags(db: Session = Depends(get_db)):
    def load_tags():
        tags = db.query(Tag).order_by(desc(Tag.create_time)).all()
        return {
            "code": 200,
            "msg": "success",
            "data": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "create_time": tag.create_time.isoformat() if tag.create_time else None,
                }
                for tag in tags
            ],
        }

    return cache.get_or_set(TAGS_CACHE_KEY, load_tags)


@router.get("/all")
def get_all_tags(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    query = db.query(Tag)
    total = query.count()

    tags = (
        query.order_by(desc(Tag.create_time))
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    items = []
    for tag in tags:
        article_count = db.query(Article).filter(build_tag_match_condition(tag.id)).count()
        items.append(
            {
                "id": tag.id,
                "name": tag.name,
                "create_time": tag.create_time.isoformat() if tag.create_time else None,
                "article_count": article_count,
            }
        )

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0,
        },
    }


@router.post("")
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag already exists.",
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
            "create_time": tag.create_time.isoformat() if tag.create_time else None,
        },
    }


@router.put("/{tag_id}")
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag does not exist.",
        )

    if tag_data.name and tag_data.name != tag.name:
        existing = db.query(Tag).filter(Tag.name == tag_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists.",
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
            "create_time": tag.create_time.isoformat() if tag.create_time else None,
        },
    }


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag does not exist.",
        )

    cleaned_articles = remove_tag_from_articles(tag_id, db)
    db.delete(tag)
    db.commit()
    invalidate_tag_cache()
    logger.info(
        "tag deleted - tag_id: %s, cleaned_articles: %s, author: %s",
        tag_id,
        cleaned_articles,
        admin.username,
    )

    return {"code": 200, "msg": "Delete successful."}
