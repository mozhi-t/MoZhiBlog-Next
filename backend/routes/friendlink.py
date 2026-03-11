"""
FriendLink Routes - 友链接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import FriendLink, get_db
from schemas import FriendLinkCreate, FriendLinkUpdate
from auth import get_current_admin

router = APIRouter(prefix="/api/friend_links", tags=["友链"])


@router.get("")
def get_friend_links(db: Session = Depends(get_db)):
    """
    获取所有展示的友链列表（公开），按权重和创建时间排序
    """
    links = db.query(FriendLink).filter(
        FriendLink.is_show == 1
    ).order_by(FriendLink.weight.asc(), FriendLink.create_time.desc()).all()

    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": l.id,
            "username": l.username,
            "signature": l.signature,
            "icon_url": l.icon_url,
            "link_url": l.link_url,
            "create_time": l.create_time.isoformat() if l.create_time else None,
            "is_show": l.is_show,
            "weight": l.weight
        } for l in links]
    }


# ==================== 管理员接口 ====================

@router.post("")
def create_friend_link(
    link_data: FriendLinkCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    新增友链（需管理员鉴权）
    """
    link = FriendLink(
        username=link_data.username,
        signature=link_data.signature,
        icon_url=link_data.icon_url,
        link_url=link_data.link_url,
        is_show=1,
        weight=link_data.weight if link_data.weight is not None else 2
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": link.id,
            "username": link.username,
            "signature": link.signature,
            "icon_url": link.icon_url,
            "link_url": link.link_url,
            "create_time": link.create_time.isoformat() if link.create_time else None,
            "is_show": link.is_show,
            "weight": link.weight
        }
    }


@router.get("/all")
def get_all_friend_links(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    is_show: int = Query(None, description="展示状态筛选"),
    weight: int = Query(None, description="权重筛选: 0-挚友, 1-朋友, 2-来客"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    获取所有友链（需管理员鉴权）
    """
    query = db.query(FriendLink)

    if is_show is not None:
        query = query.filter(FriendLink.is_show == is_show)

    if weight is not None:
        query = query.filter(FriendLink.weight == weight)

    total = query.count()

    links = query.order_by(FriendLink.weight.asc(), desc(FriendLink.create_time))\
        .offset((page - 1) * size)\
        .limit(size)\
        .all()

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [{
                "id": l.id,
                "username": l.username,
                "signature": l.signature,
                "icon_url": l.icon_url,
                "link_url": l.link_url,
                "create_time": l.create_time.isoformat() if l.create_time else None,
                "is_show": l.is_show,
                "weight": l.weight
            } for l in links],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0
        }
    }


@router.put("/{link_id}")
def update_friend_link(
    link_id: int,
    link_data: FriendLinkUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    编辑友链（需管理员鉴权）
    """
    link = db.query(FriendLink).filter(FriendLink.id == link_id).first()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="友链不存在"
        )

    update_data = link_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(link, key, value)

    db.commit()
    db.refresh(link)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": link.id,
            "username": link.username,
            "signature": link.signature,
            "icon_url": link.icon_url,
            "link_url": link.link_url,
            "create_time": link.create_time.isoformat() if link.create_time else None,
            "is_show": link.is_show,
            "weight": link.weight
        }
    }


@router.delete("/{link_id}")
def delete_friend_link(
    link_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除友链（需管理员鉴权）
    """
    link = db.query(FriendLink).filter(FriendLink.id == link_id).first()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="友链不存在"
        )

    db.delete(link)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
