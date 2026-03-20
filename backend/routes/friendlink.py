"""
FriendLink Routes - 鍙嬮摼鎺ュ彛
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from auth import get_current_admin
from cache import cache
from models import FriendLink, get_db
from schemas import FriendLinkCreate, FriendLinkUpdate

router = APIRouter(prefix="/api/friend_links", tags=["鍙嬮摼"])

FRIEND_LINKS_CACHE_KEY = "friend_links:list"


def invalidate_friend_link_cache():
    cache.delete(FRIEND_LINKS_CACHE_KEY)


@router.get("")
def get_friend_links(db: Session = Depends(get_db)):
    """
    鑾峰彇鎵€鏈夊睍绀虹殑鍙嬮摼鍒楄〃锛堝叕寮€锛夛紝鎸夋潈閲嶅拰鍒涘缓鏃堕棿鎺掑簭
    """

    def load_friend_links():
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

    return cache.get_or_set(FRIEND_LINKS_CACHE_KEY, load_friend_links)


# ==================== 绠＄悊鍛樻帴鍙?====================

@router.post("")
def create_friend_link(
    link_data: FriendLinkCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    鏂板鍙嬮摼锛堥渶绠＄悊鍛橀壌鏉冿級
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
    invalidate_friend_link_cache()

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
    is_show: int = Query(None, description="show status filter"),
    weight: int = Query(None, description="weight filter"),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    鑾峰彇鎵€鏈夊弸閾撅紙闇€绠＄悊鍛橀壌鏉冿級
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
    缂栬緫鍙嬮摼锛堥渶绠＄悊鍛橀壌鏉冿級
    """
    link = db.query(FriendLink).filter(FriendLink.id == link_id).first()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="鍙嬮摼涓嶅瓨鍦?",
        )

    update_data = link_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(link, key, value)

    db.commit()
    db.refresh(link)
    invalidate_friend_link_cache()

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
    鍒犻櫎鍙嬮摼锛堥渶绠＄悊鍛橀壌鏉冿級
    """
    link = db.query(FriendLink).filter(FriendLink.id == link_id).first()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="鍙嬮摼涓嶅瓨鍦?",
        )

    db.delete(link)
    db.commit()
    invalidate_friend_link_cache()

    return {"code": 200, "msg": "鍒犻櫎鎴愬姛"}
