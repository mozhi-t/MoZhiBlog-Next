"""
Article routes.
"""
from datetime import timedelta
from time import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    decode_token,
    get_current_admin,
    get_current_admin_optional,
    get_password_hash,
    verify_password,
)
from cache import cache
from logger import logger
from models import Article, Category, Tag, get_db
from schemas import ArticleCreate, ArticlePasswordVerifyRequest, ArticleUpdate

router = APIRouter(prefix="/api/articles", tags=["articles"])

ARTICLE_TYPE_NORMAL = 0
ARTICLE_TYPE_TOP = 1
ARTICLE_TYPE_PASSWORD = 2

ARTICLE_ACCESS_HEADER = "x-article-access-token"
ARTICLE_ACCESS_EXPIRE_HOURS = 1
PASSWORD_VERIFY_LIMIT = 10
PASSWORD_VERIFY_WINDOW_SECONDS = 300

password_verify_records: dict[str, list[float]] = {}


def build_articles_cache_key(
    page: int,
    size: int,
    category_id: Optional[int],
    tag_id: Optional[int],
    keyword: Optional[str],
    article_type: Optional[int],
    merge_top: bool,
) -> str:
    keyword_part = (keyword or "").strip()
    return (
        "articles:list:"
        f"page={page}:size={size}:category_id={category_id}:tag_id={tag_id}:"
        f"keyword={keyword_part}:type={article_type}:merge_top={merge_top}"
    )


def invalidate_article_cache():
    cache.delete_prefix("articles:list:")
    cache.delete_prefix("articles:hot:")
    cache.delete("categories:list")
    cache.delete("tags:list")


def get_tags_from_ids(tags_str: Optional[str], db: Session):
    if not tags_str:
        return []

    tag_ids = [int(tid.strip()) for tid in tags_str.split(",") if tid.strip().isdigit()]
    if not tag_ids:
        return []

    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    return [{"id": tag.id, "name": tag.name} for tag in tags]


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_password_rate_limit(ip: str):
    now = time()
    attempts = password_verify_records.get(ip, [])
    recent_attempts = [attempt for attempt in attempts if now - attempt < PASSWORD_VERIFY_WINDOW_SECONDS]
    if len(recent_attempts) >= PASSWORD_VERIFY_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Password verification requests are too frequent.",
        )

    recent_attempts.append(now)
    password_verify_records[ip] = recent_attempts


def build_article_access_cookie(article_id: int) -> str:
    return create_access_token(
        {
            "sub": f"article:{article_id}",
            "article_id": article_id,
            "scope": "article_access",
        },
        expires_delta=timedelta(hours=ARTICLE_ACCESS_EXPIRE_HOURS),
    )


def has_article_access(request: Request, article_id: int) -> bool:
    token = request.headers.get(ARTICLE_ACCESS_HEADER)
    if not token:
        return False

    try:
        payload = decode_token(token)
    except HTTPException:
        return False

    return payload.get("scope") == "article_access" and payload.get("article_id") == article_id


def build_article_payload(
    article: Article,
    db: Session,
    *,
    include_content: bool = False,
    unlocked: bool = False,
    admin_view: bool = False,
):
    category = None
    if article.category_id:
        category_model = db.query(Category).filter(Category.id == article.category_id).first()
        if category_model:
            category = {"id": category_model.id, "name": category_model.name}

    is_protected = article.type == ARTICLE_TYPE_PASSWORD
    need_password = is_protected and not (unlocked or admin_view)

    payload = {
        "id": article.id,
        "title": article.title,
        "summary": article.summary,
        "category_id": article.category_id,
        "tags": article.tags,
        "type": article.type,
        "is_top": article.type == ARTICLE_TYPE_TOP,
        "need_password": need_password,
        "has_password": bool(article.access_password) if admin_view else False,
        "read_count": article.read_count,
        "create_time": article.create_time.isoformat() if article.create_time else None,
        "update_time": article.update_time.isoformat() if article.update_time else None,
        "category": category,
        "tag_list": get_tags_from_ids(article.tags, db),
    }

    if include_content:
        payload["content"] = None if need_password else article.content

    return payload


def validate_category(category_id: Optional[int], db: Session):
    if not category_id:
        return

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist.",
        )


def validate_tags(tags: Optional[str], db: Session):
    if not tags:
        return

    tag_ids = [int(tid.strip()) for tid in tags.split(",") if tid.strip().isdigit()]
    if not tag_ids:
        return

    existing_tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    if len(existing_tags) != len(tag_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some tags do not exist.",
        )


@router.get("")
def get_articles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    keyword: Optional[str] = Query(None, min_length=1, description="keyword"),
    type: Optional[int] = Query(None, description="article type"),
    merge_top: bool = Query(False, description="merge top articles into page 1"),
    db: Session = Depends(get_db),
):
    cache_key = build_articles_cache_key(page, size, category_id, tag_id, keyword, type, merge_top)
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        return cached_response

    query = db.query(Article)

    if keyword:
        like_keyword = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Article.title.ilike(like_keyword),
                Article.summary.ilike(like_keyword),
                Article.content.ilike(like_keyword),
            )
        )

    if category_id:
        query = query.filter(Article.category_id == category_id)

    if tag_id:
        query = query.filter(Article.tags.contains(str(tag_id)))

    if type is not None:
        query = query.filter(Article.type == type)

    total = query.count()
    pages = (total + size - 1) // size if size > 0 else 0

    if merge_top:
        top_query = query.filter(Article.type == ARTICLE_TYPE_TOP)
        normal_query = query.filter(Article.type != ARTICLE_TYPE_TOP)

        top_articles = []
        if page == 1:
            top_articles = top_query.order_by(desc(Article.create_time)).all()

        normal_articles = normal_query.order_by(desc(Article.create_time)) \
            .offset(max(page - 1, 0) * size) \
            .limit(size) \
            .all()

        articles = [*top_articles, *normal_articles]
        normal_total = normal_query.count()
        pages = max(1, (normal_total + size - 1) // size) if total > 0 else 0
    else:
        articles = query.order_by(desc(Article.create_time)) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()

    response = {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [build_article_payload(article, db) for article in articles],
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
        },
    }
    cache.set(cache_key, response)
    return response


@router.get("/hot")
def get_hot_articles(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    cache_key = f"articles:hot:limit={limit}"
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        return cached_response

    articles = db.query(Article).order_by(desc(Article.read_count)).limit(limit).all()
    response = {
        "code": 200,
        "msg": "success",
        "data": [
            {
                "id": article.id,
                "title": article.title,
                "is_top": article.type == ARTICLE_TYPE_TOP,
                "need_password": article.type == ARTICLE_TYPE_PASSWORD,
                "read_count": article.read_count,
                "create_time": article.create_time.isoformat() if article.create_time else None,
            }
            for article in articles
        ],
    }
    cache.set(cache_key, response)
    return response


@router.get("/{article_id}/reference")
def get_article_reference(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article does not exist.",
        )

    category = None
    if article.category_id:
        category_model = db.query(Category).filter(Category.id == article.category_id).first()
        if category_model:
            category = {"id": category_model.id, "name": category_model.name}

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "category": category,
            "type": article.type,
            "need_password": article.type == ARTICLE_TYPE_PASSWORD,
        },
    }


@router.get("/{article_id}")
def get_article(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_optional),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"article not found - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article does not exist.",
        )

    unlocked = admin is not None or article.type != ARTICLE_TYPE_PASSWORD or has_article_access(request, article_id)
    if unlocked:
        article.read_count += 1
        db.commit()
        db.refresh(article)
        cache.delete_prefix("articles:hot:")

    return {
        "code": 200,
        "msg": "success",
        "data": build_article_payload(
            article,
            db,
            include_content=True,
            unlocked=unlocked,
            admin_view=admin is not None,
        ),
    }


@router.post("/{article_id}/verify-password")
def verify_article_password_access(
    article_id: int,
    payload: ArticlePasswordVerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article does not exist.",
        )

    if article.type != ARTICLE_TYPE_PASSWORD:
        return {
            "code": 200,
            "msg": "success",
            "data": {"passed": True},
        }

    check_password_rate_limit(get_client_ip(request))
    passed = bool(article.access_password) and verify_password(payload.password, article.access_password)
    access_token = build_article_access_cookie(article_id) if passed else None

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "passed": passed,
            "access_token": access_token,
            "expires_in": ARTICLE_ACCESS_EXPIRE_HOURS * 3600 if passed else 0,
        },
    }


@router.post("")
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    validate_category(article_data.category_id, db)
    validate_tags(article_data.tags, db)

    if article_data.type == ARTICLE_TYPE_PASSWORD and not article_data.access_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password-protected articles must set an access password.",
        )

    article = Article(
        title=article_data.title,
        summary=article_data.summary,
        content=article_data.content,
        category_id=article_data.category_id,
        tags=article_data.tags,
        type=article_data.type,
        access_password=get_password_hash(article_data.access_password)
        if article_data.type == ARTICLE_TYPE_PASSWORD and article_data.access_password
        else None,
        read_count=0,
        create_time=article_data.create_time,
        update_time=article_data.update_time,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    invalidate_article_cache()

    logger.info(f"article created - article_id: {article.id}, author: {admin.username}")
    return {
        "code": 200,
        "msg": "success",
        "data": build_article_payload(article, db, include_content=True, unlocked=True, admin_view=True),
    }


@router.put("/{article_id}")
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    logger.info(f"article updated - article_id: {article_id}, author: {admin.username}")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"article not found - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article does not exist.",
        )

    update_data = article_data.model_dump(exclude_unset=True)
    validate_category(update_data.get("category_id"), db)
    validate_tags(update_data.get("tags"), db)

    next_type = update_data.get("type", article.type)
    raw_password = update_data.pop("access_password", None)

    if next_type == ARTICLE_TYPE_PASSWORD:
        if raw_password:
            update_data["access_password"] = get_password_hash(raw_password)
        elif not article.access_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password-protected articles must set an access password.",
            )
    else:
        update_data["access_password"] = None

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    invalidate_article_cache()

    return {
        "code": 200,
        "msg": "success",
        "data": build_article_payload(article, db, include_content=True, unlocked=True, admin_view=True),
    }


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    logger.info(f"article deleted - article_id: {article_id}, author: {admin.username}")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"article not found - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article does not exist.",
        )

    db.delete(article)
    db.commit()
    invalidate_article_cache()
    return {"code": 200, "msg": "Delete successful."}
