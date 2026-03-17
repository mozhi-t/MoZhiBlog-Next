"""
Moment routes.
"""
from datetime import timedelta
from time import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import desc
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
from models import Moment, get_db
from schemas import MomentCreate, MomentPasswordVerifyRequest, MomentUpdate

router = APIRouter(prefix="/api/moments", tags=["moments"])

MOMENT_ACCESS_HEADER = "x-moment-access-token"
MOMENT_ACCESS_EXPIRE_HOURS = 24
PASSWORD_VERIFY_LIMIT = 10
PASSWORD_VERIFY_WINDOW_SECONDS = 300

password_verify_records: dict[str, list[float]] = {}


def build_moments_cache_key(page: int, size: int) -> str:
    return f"moments:list:page={page}:size={size}"


def invalidate_moment_cache():
    cache.delete_prefix("moments:list:")


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


def build_moment_access_token(moment_id: int) -> str:
    return create_access_token(
        {
            "sub": f"moment:{moment_id}",
            "moment_id": moment_id,
            "scope": "moment_access",
        },
        expires_delta=timedelta(hours=MOMENT_ACCESS_EXPIRE_HOURS),
    )


def has_moment_access(request: Request, moment_id: int) -> bool:
    token = request.headers.get(MOMENT_ACCESS_HEADER)
    if not token:
        return False

    try:
        payload = decode_token(token)
    except HTTPException:
        return False

    return payload.get("scope") == "moment_access" and payload.get("moment_id") == moment_id


def build_moment_payload(moment: Moment, *, unlocked: bool = False, admin_view: bool = False):
    need_password = bool(moment.access_password) and not (unlocked or admin_view)
    return {
        "id": moment.id,
        "content": None if need_password else moment.content,
        "need_password": need_password,
        "has_password": bool(moment.access_password) if admin_view else False,
        "create_time": moment.create_time.isoformat() if moment.create_time else None,
        "update_time": moment.update_time.isoformat() if moment.update_time else None,
    }


@router.get("")
def get_moments(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_optional),
):
    cache_key = build_moments_cache_key(page, size)
    cached_response = cache.get(cache_key)

    if cached_response is not None and admin is None:
        items = []
        for item in cached_response["data"]["items"]:
            unlocked = not item["need_password"] or has_moment_access(request, item["id"])
            if unlocked:
                moment = db.query(Moment).filter(Moment.id == item["id"]).first()
                items.append(build_moment_payload(moment, unlocked=True))
            else:
                items.append(item)

        return {
            "code": 200,
            "msg": "success",
            "data": {
                **cached_response["data"],
                "items": items,
            },
        }

    query = db.query(Moment)
    total = query.count()
    moments = query.order_by(desc(Moment.create_time)).offset((page - 1) * size).limit(size).all()

    response = {
        "code": 200,
        "msg": "success",
        "data": {
            "items": [
                build_moment_payload(
                    moment,
                    unlocked=admin is not None or has_moment_access(request, moment.id),
                    admin_view=admin is not None,
                )
                for moment in moments
            ],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0,
        },
    }

    if admin is None:
        cache.set(
            cache_key,
            {
                "code": 200,
                "msg": "success",
                "data": {
                    **response["data"],
                    "items": [build_moment_payload(moment) for moment in moments],
                },
            },
        )

    return response


@router.get("/{moment_id}")
def get_moment(
    moment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_optional),
):
    moment = db.query(Moment).filter(Moment.id == moment_id).first()
    if not moment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moment does not exist.",
        )

    unlocked = admin is not None or not moment.access_password or has_moment_access(request, moment_id)
    return {
        "code": 200,
        "msg": "success",
        "data": build_moment_payload(moment, unlocked=unlocked, admin_view=admin is not None),
    }


@router.post("/{moment_id}/verify-password")
def verify_moment_password_access(
    moment_id: int,
    payload: MomentPasswordVerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    moment = db.query(Moment).filter(Moment.id == moment_id).first()
    if not moment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moment does not exist.",
        )

    if not moment.access_password:
        return {
            "code": 200,
            "msg": "success",
            "data": {"passed": True},
        }

    check_password_rate_limit(get_client_ip(request))
    passed = verify_password(payload.password, moment.access_password)
    access_token = build_moment_access_token(moment_id) if passed else None

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "passed": passed,
            "access_token": access_token,
            "expires_in": MOMENT_ACCESS_EXPIRE_HOURS * 3600 if passed else 0,
        },
    }


@router.post("")
def create_moment(
    moment_data: MomentCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    moment = Moment(
        content=moment_data.content,
        access_password=get_password_hash(moment_data.access_password) if moment_data.access_password else None,
        create_time=moment_data.create_time,
        update_time=moment_data.update_time,
    )
    db.add(moment)
    db.commit()
    db.refresh(moment)
    invalidate_moment_cache()

    logger.info(f"moment created - moment_id: {moment.id}, author: {admin.username}")
    return {
        "code": 200,
        "msg": "success",
        "data": build_moment_payload(moment, unlocked=True, admin_view=True),
    }


@router.put("/{moment_id}")
def update_moment(
    moment_id: int,
    moment_data: MomentUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    moment = db.query(Moment).filter(Moment.id == moment_id).first()
    if not moment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moment does not exist.",
        )

    update_data = moment_data.model_dump(exclude_unset=True)

    if "access_password" in update_data:
        raw_password = update_data["access_password"]
        update_data["access_password"] = get_password_hash(raw_password) if raw_password else None

    for key, value in update_data.items():
        setattr(moment, key, value)

    db.commit()
    db.refresh(moment)
    invalidate_moment_cache()

    logger.info(f"moment updated - moment_id: {moment.id}, author: {admin.username}")
    return {
        "code": 200,
        "msg": "success",
        "data": build_moment_payload(moment, unlocked=True, admin_view=True),
    }


@router.delete("/{moment_id}")
def delete_moment(
    moment_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    moment = db.query(Moment).filter(Moment.id == moment_id).first()
    if not moment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moment does not exist.",
        )

    db.delete(moment)
    db.commit()
    invalidate_moment_cache()

    logger.info(f"moment deleted - moment_id: {moment_id}, author: {admin.username}")
    return {"code": 200, "msg": "Delete successful."}
