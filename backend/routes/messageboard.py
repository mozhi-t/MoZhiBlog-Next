"""
MessageBoard Routes - 留言板接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import MessageBoard, get_db
from schemas import MessageBoardCreate, MessageBoardUpdate
from auth import get_current_admin

router = APIRouter(prefix="/api/messages", tags=["留言板"])


@router.get("")
def get_messages(db: Session = Depends(get_db)):
    """
    获取所有展示的留言列表（公开）
    """
    messages = db.query(MessageBoard).filter(
        MessageBoard.is_show == 1
    ).order_by(MessageBoard.create_time.desc()).all()

    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": m.id,
            "nickname": m.nickname,
            "email": m.email,
            "content": m.content,
            "create_time": m.create_time.isoformat() if m.create_time else None,
            "is_show": m.is_show
        } for m in messages]
    }


@router.post("")
def create_message(
    message_data: MessageBoardCreate,
    db: Session = Depends(get_db)
):
    """
    新增留言（公开接口）
    """
    message = MessageBoard(
        nickname=message_data.nickname,
        email=message_data.email,
        content=message_data.content,
        is_show=1
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": message.id,
            "nickname": message.nickname,
            "email": message.email,
            "content": message.content,
            "create_time": message.create_time.isoformat() if message.create_time else None,
            "is_show": message.is_show
        }
    }


# ==================== 管理员接口 ====================

@router.get("/all")
def get_all_messages(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    is_show: int = Query(None, description="展示状态筛选"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    获取所有留言（需管理员鉴权）
    """
    query = db.query(MessageBoard)

    if is_show is not None:
        query = query.filter(MessageBoard.is_show == is_show)

    total = query.count()

    messages = query.order_by(desc(MessageBoard.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [{
                "id": m.id,
                "nickname": m.nickname,
                "email": m.email,
                "content": m.content,
                "create_time": m.create_time.isoformat() if m.create_time else None,
                "is_show": m.is_show
            } for m in messages],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0
        }
    }


@router.put("/{message_id}")
def update_message(
    message_id: int,
    message_data: MessageBoardUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    编辑留言（需管理员鉴权）
    """
    message = db.query(MessageBoard).filter(MessageBoard.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="留言不存在"
        )

    update_data = message_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(message, key, value)

    db.commit()
    db.refresh(message)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": message.id,
            "nickname": message.nickname,
            "email": message.email,
            "content": message.content,
            "create_time": message.create_time.isoformat() if message.create_time else None,
            "is_show": message.is_show
        }
    }


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除留言（需管理员鉴权）
    """
    message = db.query(MessageBoard).filter(MessageBoard.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="留言不存在"
        )

    db.delete(message)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
