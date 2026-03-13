"""
Comment Routes - 评论接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import Comment, Article, get_db
from schemas import CommentCreate
from auth import get_current_admin
from logger import logger

router = APIRouter(prefix="/api/comments", tags=["评论"])


@router.get("/{article_id}")
def get_article_comments(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    获取指定文章的评论列表（公开）
    """
    logger.info(f"获取文章评论 - article_id: {article_id}")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.warning(f"文章不存在 - article_id: {article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    comments = db.query(Comment).filter(
        Comment.article_id == article_id,
        Comment.is_approved == 1
    ).order_by(desc(Comment.create_time)).all()

    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": c.id,
            "article_id": c.article_id,
            "nickname": c.nickname,
            "email": c.email,
            "content": c.content,
            "create_time": c.create_time.isoformat() if c.create_time else None,
            "is_approved": c.is_approved
        } for c in comments]
    }


@router.post("")
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db)
):
    """
    提交评论（访客填写，无需鉴权）
    """
    logger.info(f"提交评论 - article_id: {comment_data.article_id}, nickname: {comment_data.nickname}")

    article = db.query(Article).filter(Article.id == comment_data.article_id).first()
    if not article:
        logger.warning(f"文章不存在 - article_id: {comment_data.article_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    comment = Comment(
        article_id=comment_data.article_id,
        nickname=comment_data.nickname,
        email=comment_data.email,
        content=comment_data.content,
        is_approved=1
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": comment.id,
            "article_id": comment.article_id,
            "nickname": comment.nickname,
            "email": comment.email,
            "content": comment.content,
            "create_time": comment.create_time.isoformat() if comment.create_time else None,
            "is_approved": comment.is_approved
        }
    }


# ==================== 管理员接口 ====================

@router.get("/all")
def get_all_comments(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    is_approved: int = Query(None, description="审核状态筛选"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    获取所有评论（需管理员鉴权）
    """
    logger.info(f"获取所有评论 - page: {page}, size: {size}, is_approved: {is_approved}")
    query = db.query(Comment)

    if is_approved is not None:
        query = query.filter(Comment.is_approved == is_approved)

    total = query.count()

    comments = query.order_by(desc(Comment.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    items = []
    for comment in comments:
        article = db.query(Article).filter(Article.id == comment.article_id).first()
        items.append({
            "id": comment.id,
            "article_id": comment.article_id,
            "nickname": comment.nickname,
            "email": comment.email,
            "content": comment.content,
            "create_time": comment.create_time.isoformat() if comment.create_time else None,
            "is_approved": comment.is_approved,
            "article": {
                "id": article.id,
                "title": article.title
            } if article else None
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


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除评论（需管理员鉴权）
    """
    logger.info(f"删除评论 - comment_id: {comment_id}, author: {admin.username}")

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"评论不存在 - comment_id: {comment_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    db.delete(comment)
    db.commit()

    return {"code": 200, "msg": "删除成功"}


@router.put("/{comment_id}/approve")
def approve_comment(
    comment_id: int,
    is_approved: int = Query(0, description="审核状态 0:未通过 1:通过"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    审核评论（需管理员鉴权）
    """
    logger.info(f"审核评论 - comment_id: {comment_id}, is_approved: {is_approved}, author: {admin.username}")

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"评论不存在 - comment_id: {comment_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    comment.is_approved = is_approved
    db.commit()
    db.refresh(comment)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": comment.id,
            "article_id": comment.article_id,
            "nickname": comment.nickname,
            "email": comment.email,
            "content": comment.content,
            "create_time": comment.create_time.isoformat() if comment.create_time else None,
            "is_approved": comment.is_approved
        }
    }
